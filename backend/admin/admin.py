from flask import render_template, request, redirect, url_for, session
from backend.database.database_utils import load_clients_from_db, get_admin_by_username
from werkzeug.security import check_password_hash, generate_password_hash
from backend.database.database_utils import save_admin_to_db, log_admin_action
import mysql.connector
from collections import Counter

class AdminPanel:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/admin_login', methods=['GET', 'POST'])
        def admin_login():
            if request.method == 'POST':
                username = request.form['username']
                pin = request.form['pin']

                admin = get_admin_by_username(username)
                if admin and check_password_hash(admin['pin'], pin):
                    session['admin_logged_in'] = True
                    session['admin_username'] = username
                    session['admin_role'] = admin.get('role', 'moderator')  # 'administrator' or 'moderator'

                    return redirect(url_for('admin_dashboard'))
                else:
                    return render_template('Admin/admin_login.html', error="Invalid username or PIN")

            return render_template('Admin/admin_login.html')

        @self.app.route('/admin_dashboard', methods=['GET'])
        def admin_dashboard():
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            from collections import Counter, defaultdict
            from datetime import datetime, timedelta
            import calendar

            clients = load_clients_from_db()
            total_clients = len(clients)

            # Counters
            skill_counter = Counter()
            address_counter = Counter()
            learn_skill_counter = Counter()
            male_count = female_count = other_count = 0

            for c in clients:
                teach_skills = [s.strip().lower() for s in c.teach_skills.split(',')]
                learn_skills = [s.strip().lower() for s in c.learn_skills.split(',')]
                skill_counter.update(teach_skills)
                learn_skill_counter.update(learn_skills)
                address_counter.update([c.address.strip().lower()])

                gender = c.gender.strip().lower()
                if gender == 'male':
                    male_count += 1
                elif gender == 'female':
                    female_count += 1
                elif gender == 'other':
                    other_count += 1

            top_skills = skill_counter.most_common(3)
            top_addresses = address_counter.most_common(3)
            top_learn_skills = learn_skill_counter.most_common(3)

            # Chart Data Initialization (Last 6 months)
            now = datetime.now()
            month_labels = []
            registered_counts = []
            active_counts = []
            inactive_counts = []

            # Skill Trends
            skill_trends = defaultdict(lambda: [0] * 6)

            # Login Heatmap Matrix [7 days][24 hours]
            login_heatmap = [[0 for _ in range(24)] for _ in range(7)]

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor(dictionary=True)

                # === ✅ Total Admins Count ===
                cursor.execute("SELECT COUNT(*) AS count FROM admins")
                admin_count = cursor.fetchone()['count']

                for i in range(5, -1, -1):
                    month_index = 5 - i
                    month_date = now.replace(day=1) - timedelta(days=30 * i)
                    start_date = month_date.replace(day=1)
                    end_day = calendar.monthrange(start_date.year, start_date.month)[1]
                    end_date = start_date.replace(day=end_day, hour=23, minute=59, second=59)

                    month_label = start_date.strftime('%b %Y')
                    month_labels.append(month_label)

                    # Total registered till this month
                    cursor.execute("""
                        SELECT COUNT(*) AS count FROM clients
                        WHERE created_at <= %s
                    """, (end_date,))
                    registered = cursor.fetchone()['count']
                    registered_counts.append(registered)

                    # Active users this month
                    cursor.execute("""
                        SELECT COUNT(DISTINCT username) AS count FROM client_logs
                        WHERE timestamp BETWEEN %s AND %s
                    """, (start_date, end_date))
                    active = cursor.fetchone()['count']
                    active_counts.append(active)

                    # Inactive users = registered - active
                    inactive = registered - active
                    inactive_counts.append(max(inactive, 0))

                    # Skill Trend Data (Top 3 skills only)
                    if top_skills:
                        skill_names = [s[0] for s in top_skills]
                        cursor.execute("""
                            SELECT teach_skills FROM clients
                            WHERE created_at BETWEEN %s AND %s
                        """, (start_date, end_date))
                        skill_rows = cursor.fetchall()
                        for row in skill_rows:
                            if row['teach_skills']:
                                skills = [s.strip().lower() for s in row['teach_skills'].split(',')]
                                for s in skills:
                                    if s in skill_names:
                                        skill_trends[s][month_index] += 1

                # Unread support messages
                cursor.execute("""
                    SELECT COUNT(*) AS unread_count 
                    FROM support_messages 
                    WHERE receiver = 'admin' AND is_read = FALSE
                """)
                unread_support = cursor.fetchone()['unread_count']

                # Recent client logs
                cursor.execute("""
                    SELECT username, activity, timestamp 
                    FROM client_logs 
                    ORDER BY timestamp DESC 
                    LIMIT 5
                """)
                recent_logs = cursor.fetchall()

                # Login heatmap data: weekday x hour
                cursor.execute("""
                    SELECT 
                        HOUR(timestamp) AS hour,
                        WEEKDAY(timestamp) AS weekday,
                        COUNT(*) AS count
                    FROM client_logs
                    GROUP BY weekday, hour
                """)
                heatmap_rows = cursor.fetchall()
                for row in heatmap_rows:
                    login_heatmap[row['weekday']][row['hour']] = row['count']

                # === Most Active Clients in Last 30 Days ===
                last_30_days = datetime.now() - timedelta(days=30)
                cursor.execute("""
                    SELECT username, COUNT(*) AS login_count
                    FROM client_logs
                    WHERE activity = 'logged in' AND timestamp >= %s
                    GROUP BY username
                    ORDER BY login_count DESC
                    LIMIT 5
                """, (last_30_days,))
                top_clients_data = cursor.fetchall()

                # Prepare labels and values for the pie chart
                pie_labels = [row['username'] for row in top_clients_data]
                pie_values = [row['login_count'] for row in top_clients_data]

            except mysql.connector.Error as err:
                print("MySQL Error:", err)
                unread_support = 0
                recent_logs = []
                month_labels = []
                registered_counts = []
                active_counts = []
                inactive_counts = []
                skill_trends = {}
                login_heatmap = []
                pie_labels = []
                pie_values = []
                admin_count = 0  # Fallback if DB fails

            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            return render_template(
                'Admin/admin_dashboard.html',
                total_clients=total_clients,
                top_skills=top_skills,
                top_addresses=top_addresses,
                top_learn_skills=top_learn_skills,
                male_count=male_count,
                female_count=female_count,
                other_count=other_count,
                unread_support=unread_support,
                recent_logs=recent_logs,
                month_labels=month_labels,
                chart_registered=registered_counts,
                chart_active=active_counts,
                chart_inactive=inactive_counts,
                skill_trends=skill_trends,
                heatmap_data=login_heatmap,
                pie_labels=pie_labels,
                pie_values=pie_values,
                total_admins=admin_count  # ✅ Passed to template
            )

        @self.app.route('/admin/clients')
        def admin_clients():
            if 'admin_logged_in' not in session:
                return redirect(url_for('admin_login'))

            clients = load_clients_from_db()

            # Apply filters
            search_name = request.args.get('search_name', '').strip().lower()
            filter_skill = request.args.get('filter_skill', '').strip().lower()
            filter_address = request.args.get('filter_address', '').strip().lower()

            filtered_clients = []
            for c in clients:
                if search_name and search_name not in c.name.lower():
                    continue
                if filter_skill and filter_skill not in c.teach_skills.lower():
                    continue
                if filter_address and filter_address not in c.address.lower():
                    continue
                filtered_clients.append(c)

            return render_template('Admin/client_data.html', clients=filtered_clients)

        @self.app.route('/admin_logout')
        def admin_logout():
            session.clear()
            return redirect(url_for('admin_login'))

        @self.app.route('/admin_register', methods=['GET', 'POST'])
        def admin_register():
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            if request.method == 'POST':
                username = request.form['username']
                pin = request.form['pin']
                hashed_pin = generate_password_hash(pin)
                success = save_admin_to_db(username, hashed_pin)
                if success:
                    return redirect(url_for('admin_dashboard'))
                return "Admin username already exists or error occurred."
            return render_template('Admin/admin_register.html')

        @self.app.route('/admin/view/<username>')
        def admin_view_client(username):
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            client = next((c for c in load_clients_from_db() if c.username == username), None)
            return render_template('Admin/admin_view_client.html', client=client)

        @self.app.route('/admin/edit/<username>', methods=['GET', 'POST'], endpoint='admin_edit_client')
        def admin_edit_client(username):
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            from backend.database.database_utils import update_client_in_db

            all_clients = load_clients_from_db()
            client = next((c for c in all_clients if c.username == username), None)
            if not client:
                return "Client not found"

            if request.method == 'POST':
                edited_fields = []

                if client.name != request.form['name']:
                    edited_fields.append(f"name: '{client.name}' → '{request.form['name']}'")
                    client.name = request.form['name']
                if str(client.age) != request.form['age']:
                    edited_fields.append(f"age: {client.age} → {request.form['age']}")
                    client.age = int(request.form['age'])
                if client.gender != request.form['gender']:
                    edited_fields.append(f"gender: '{client.gender}' → '{request.form['gender']}'")
                    client.gender = request.form['gender']
                if str(client.ph_no) != request.form['phone']:
                    edited_fields.append(f"phone: {client.ph_no} → {request.form['phone']}")
                    client.ph_no = int(request.form['phone'])
                if client.address != request.form['address']:
                    edited_fields.append(f"address: '{client.address}' → '{request.form['address']}'")
                    client.address = request.form['address']
                if client.teach_skills != request.form['teach_skills']:
                    edited_fields.append(f"teach_skills: '{client.teach_skills}' → '{request.form['teach_skills']}'")
                    client.teach_skills = request.form['teach_skills']
                if client.learn_skills != request.form['learn_skills']:
                    edited_fields.append(f"learn_skills: '{client.learn_skills}' → '{request.form['learn_skills']}'")
                    client.learn_skills = request.form['learn_skills']

                update_client_in_db(client)
                details = "; ".join(edited_fields) if edited_fields else "No changes made"
                log_admin_action(session.get('admin_username'), 'edit', username, details)

                return redirect(url_for('admin_clients'))

            return render_template('Admin/admin_edit_client.html', client=client)

        @self.app.route('/admin/delete/<username>', endpoint='admin_delete_client')
        def admin_delete_client(username):
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            if session.get('admin_role') != 'administrator':
                return "⛔ Access denied. Only administrators can delete clients."

            from backend.database.database_utils import delete_client_from_db
            delete_client_from_db(username)

            log_admin_action(
                session.get('admin_username', 'unknown_admin'),
                'delete',
                username,
                f"Deleted client: {username}"
            )

            return redirect(url_for('admin_clients'))

        @self.app.route('/admin_logs')
        def admin_logs():
            if not session.get('admin_logged_in') or session.get('admin_role') != 'administrator':
                return "🚫 Unauthorized access"

            search = request.args.get('search', '').strip().lower()

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM admin_logs ORDER BY timestamp DESC")
                logs = cursor.fetchall()

                if search:
                    logs = [
                        log for log in logs
                        if search in (log.get('admin_username') or '').lower()
                        or search in (log.get('action') or '').lower()
                        or search in (log.get('target_username') or '').lower()
                        or search in (log.get('details') or '').lower()
                    ]

                return render_template('Admin/admin_logs.html', logs=logs, search=search)

            except mysql.connector.Error as err:
                return f"❌ MySQL Error: {err}"

            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

        @self.app.route('/admin/add', methods=['GET', 'POST'])
        def add_new_admin():
            if not session.get('admin_logged_in') or session.get('admin_role') != 'administrator':
                return "🚫 Unauthorized access"

            if request.method == 'POST':
                new_username = request.form['username']
                new_pin = request.form['pin']
                hashed_pin = generate_password_hash(new_pin)

                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO admins (username, pin, role) VALUES (%s, %s, %s)
                    """, (new_username, hashed_pin, 'moderator'))
                    conn.commit()
                    return redirect(url_for('admin_dashboard'))
                except mysql.connector.Error as err:
                    return f"❌ Error: {err}"
                finally:
                    cursor.close()
                    conn.close()

            return render_template('Admin/add_admin.html')
        
        @self.app.route('/admin/client_activity_logs')
        def client_activity_logs():
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM client_logs ORDER BY timestamp DESC")
                logs = cursor.fetchall()
                return render_template('Admin/client_activity_logs.html', logs=logs)
            except mysql.connector.Error as err:
                return f"MySQL Error: {err}"
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

        @self.app.route('/admin/client_logs')
        def recent_client_activities():
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            import mysql.connector
            search = request.args.get('search', '').strip().lower()

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM client_logs ORDER BY timestamp DESC LIMIT 100")
                logs = cursor.fetchall()

                if search:
                    logs = [log for log in logs if search in log['username'].lower() or search in log['activity'].lower()]

            except mysql.connector.Error as err:
                return f"❌ MySQL Error: {err}"

            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            return render_template('Admin/recent_client_activities.html', logs=logs)

        @self.app.route('/client_status')
        def client_status():
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))

            search_username = request.args.get('search', '').strip().lower()

            from datetime import datetime, timedelta
            today = datetime.today()
            first_of_month = today.replace(day=1)

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor(dictionary=True)

                # Fetch last activity for all users
                cursor.execute("""
                    SELECT username, MAX(timestamp) AS last_active
                    FROM client_logs
                    GROUP BY username
                """)
                activity_map = {row['username'].lower(): row['last_active'] for row in cursor.fetchall()}

                # Fetch all clients with registration info
                cursor.execute("SELECT username, name, gender, address, created_at FROM clients")
                clients = cursor.fetchall()

                active_clients = []
                inactive_clients = []

                for client in clients:
                    uname = client['username'].lower()

                    if search_username and search_username not in uname:
                        continue

                    client['last_active'] = activity_map.get(uname)
                    if client['last_active'] and client['last_active'] >= first_of_month:
                        active_clients.append(client)
                    else:
                        inactive_clients.append(client)

            except mysql.connector.Error as err:
                print("❌ Error:", err)
                active_clients = []
                inactive_clients = []
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            return render_template(
                'Admin/client_status.html',
                active_clients=active_clients,
                inactive_clients=inactive_clients,
                search_username=search_username
            )