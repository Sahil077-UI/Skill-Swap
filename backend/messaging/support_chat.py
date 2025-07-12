from flask import render_template, request, redirect, url_for, session
from datetime import datetime
import mysql.connector

class SupportChat:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            database="skillswap_hub"
        )

    def register_routes(self):
        @self.app.route('/client_support', methods=['GET', 'POST'])
        def client_support():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            username = session['username']

            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            if request.method == 'POST':
                message = request.form['message'].strip()
                if message:
                    cursor.execute("""
                        INSERT INTO support_messages (sender, receiver, message, is_read, timestamp)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (username, 'admin', message, False, datetime.now()))
                    conn.commit()

            cursor.execute("""
                SELECT * FROM support_messages
                WHERE sender = %s OR receiver = %s
                ORDER BY timestamp
            """, (username, username))

            messages = cursor.fetchall()
            cursor.close()
            conn.close()

            return render_template('Messaging/client_support.html', messages=messages, username=username)

        @self.app.route('/admin_support', methods=['GET', 'POST'])
        def admin_support():
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            if request.method == 'POST':
                sender = request.form['sender']
                message = request.form['message'].strip()
                if message:
                    cursor.execute("""
                        INSERT INTO support_messages (sender, receiver, message, is_read, timestamp)
                        VALUES (%s, %s, %s, %s, %s)
                    """, ('admin', sender, message, False, datetime.now()))
                    conn.commit()

            cursor.execute("""
                SELECT DISTINCT sender FROM support_messages WHERE receiver = 'admin'
            """)
            clients = [row['sender'] for row in cursor.fetchall()]

            inbox = {}
            for client in clients:
                cursor.execute("""
                    SELECT * FROM support_messages
                    WHERE sender = %s OR receiver = %s
                    ORDER BY timestamp
                """, (client, client))
                inbox[client] = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('Messaging/admin_support.html', inbox=inbox)