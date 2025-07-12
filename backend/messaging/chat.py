from backend.database.database_utils import mark_messages_as_read
from flask import request, render_template, redirect, url_for, session
from backend.database.database_utils import get_confirmed_connections, save_message, get_chat_messages
import mysql.connector

class ChatPanel:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/messages/<username>', methods=['GET', 'POST'], endpoint='chat_with_user')
        def chat_with_user(username):
            print("📨 Entered chat_with_user route")

            if 'username' not in session:
                return redirect(url_for('client_login'))

            current_user = session['username']
            print("📌 Current user:", current_user)
            print("📌 Chatting with:", username)

            connections = get_confirmed_connections(current_user)
            connected_usernames = [
                conn['sender_username'] if conn['receiver_username'] == current_user else conn['receiver_username']
                for conn in connections
            ]
            if username not in connected_usernames:
                return "⚠️ You're not connected with this user."

            # ✅ Mark messages as read
            mark_messages_as_read(sender=username, receiver=current_user)

            if request.method == 'POST':
                message = request.form['message'].strip()
                if message:
                    save_message(current_user, username, message)

                    # ✅ Log activity: Sent message
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="Onedayiwill",
                            database="skillswap_hub"
                        )
                        cursor = conn.cursor()
                        activity_text = f"Sent message to {username}"
                        cursor.execute(
                            "INSERT INTO client_logs (username, activity, timestamp) VALUES (%s, %s, NOW())",
                            (current_user, activity_text)
                        )
                        conn.commit()
                    except mysql.connector.Error as err:
                        print("❌ Logging Error:", err)
                    finally:
                        if 'cursor' in locals(): cursor.close()
                        if 'conn' in locals(): conn.close()

            chat_history = get_chat_messages(current_user, username)

            return render_template(
                'Messaging/chat.html',
                current_user=current_user,
                target_user=username,
                messages=chat_history
            )
