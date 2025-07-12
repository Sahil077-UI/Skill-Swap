import mysql.connector
from flask import jsonify
from flask import render_template, request, redirect, url_for, session
from backend.database.database_utils import save_client_to_db, update_client_in_db, load_clients_from_db
from werkzeug.security import generate_password_hash, check_password_hash
from backend.client.client_model import Client
from backend.database.database_utils import save_connection_request
from backend.database.database_utils import get_requests_received, get_requests_sent
from backend.database.database_utils import update_request_status
from backend.database.database_utils import get_confirmed_connections
from backend.database.database_utils import get_unread_message_count
from backend.matching.skill_match import get_skill_matches
from backend.database.database_utils import get_client_by_id, update_client_password
from backend.database.database_utils import get_groups_for_user
from backend.database.database_utils import get_connection
from backend.database.database_utils import get_group_by_id,delete_group_and_messages
from backend.database.database_utils import get_client_by_username, update_client_password, get_sent_requests
from backend.database.database_utils import (
    get_all_global_messages,
    save_global_message,
    remove_confirmed_connection,
    block_user,
    unblock_user,
    is_user_blocked,
    save_message,
    get_chat_messages,
    mark_messages_as_read,
    get_unread_personal_message_count
)
from backend.database.database_utils import (
    get_client_by_username,
    get_confirmed_connections,
    get_groups_for_user
)


class ClientPanel:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def get_client_by_username(self, username):
        all_clients = load_clients_from_db()
        for client in all_clients:
            if client.username == username:
                return client
        return None

    def register_routes(self):
        @self.app.route('/client_register', methods=['GET', 'POST'])
        def client_register():
            if request.method == 'POST':
                c = Client()
                c.name = request.form['name']
                c.age = int(request.form['age'])
                c.gender = request.form['gender']
                c.id = int(request.form['aadhar'])
                c.ph_no = int(request.form['phone'])
                c.address = request.form['address']
                # optional
                c.location = request.form['location'] if 'location' in request.form else ""
                c.username = request.form['username']
                pin = request.form['pin']
                c.pin = generate_password_hash(pin)
                c.teach_skills = request.form['teach_skills']
                c.learn_skills = request.form['learn_skills']

                success = save_client_to_db(c)
                if success:
                    return redirect(url_for('client_login'))
                else:
                    return "Username already exists or database error."

            return render_template('Client/client_register.html')

        @self.app.route('/client_login', methods=['GET', 'POST'])
        def client_login():
            if request.method == 'POST':
                username = request.form['username']
                pin = request.form['pin']

                user = self.get_client_by_username(username)
                if user and check_password_hash(user.pin, pin):
                    session.permanent = True
                    session['client_logged_in'] = True
                    session['username'] = user.username
                    session['client_name'] = user.name
                    session['client_id'] = user.id

                    # Log login
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="Onedayiwill",
                            database="skillswap_hub"
                        )
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO client_logs (username, activity, timestamp) VALUES (%s, %s, NOW())",
                                    (username, "Logged in"))
                        conn.commit()
                    except mysql.connector.Error as err:
                        print("❌ Error logging activity:", err)
                    finally:
                        if cursor: cursor.close()
                        if conn: conn.close()
                    print("✅ SESSION AFTER LOGIN:", dict(session))
                    return redirect(url_for('client_profile'))

                else:
                    return "Invalid login credentials."

            return render_template('Client/client_login.html')

        @self.app.route('/client_profile')
        def client_profile():
            print("🧠 Session when accessing /client_profile:", dict(session))
            if 'username' not in session:
                return redirect(url_for('client_login'))

            user = self.get_client_by_username(session['username'])
            if not user:
                return "Client not found."

            # ✅ Log activity: Viewed profile
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO client_logs (username, activity, timestamp) VALUES (%s, %s, NOW())",
                    (user.username, "Viewed profile")
                )
                conn.commit()
            except mysql.connector.Error as err:
                print("❌ Error logging profile view:", err)
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            received_requests = get_requests_received(user.username)
            sent_requests = get_requests_sent(user.username)
            connections = get_confirmed_connections(user.username)
            unread_counts = get_unread_message_count(user.username)
            groups = get_groups_for_user(user.username)

            return render_template(
                'Client/client_profile.html',
                client=user,
                received_requests=received_requests,
                sent_requests=sent_requests,
                connections=connections,
                unread_counts=unread_counts,
                groups=groups
            )

        @self.app.route('/client_edit_profile', methods=['GET', 'POST'])
        def client_edit_profile():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            user = self.get_client_by_username(session['username'])
            if not user:
                return "User not found"

            if request.method == 'POST':
                user.name = request.form['name']
                user.age = int(request.form['age'])
                user.gender = request.form['gender']
                user.ph_no = int(request.form['phone'])
                user.address = request.form['address']
                user.location = request.form['location'] if 'location' in request.form else user.location
                user.teach_skills = request.form['teach_skills']
                user.learn_skills = request.form['learn_skills']
                if request.form['pin']:
                    user.pin = generate_password_hash(request.form['pin'])

                update_client_in_db(user)
                return redirect(url_for('client_profile'))

            return render_template('Client/client_edit.html', client=user)

        @self.app.route('/client_logout')
        def client_logout():
            username = session.get('username', 'unknown')

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Onedayiwill",
                    database="skillswap_hub"
                )
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO client_logs (username, activity, timestamp) VALUES (%s, %s, NOW())",
                    (username, "Logged out")
                )
                conn.commit()
            except mysql.connector.Error as err:
                print("❌ Error logging client logout:", err)
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            session.clear()
            return redirect(url_for('client_login'))


        @self.app.route('/client_matches')
        def client_matches():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            user = self.get_client_by_username(session['username'])

            # Get all potential matches
            matches = get_skill_matches(user)

            # Exclude blocked users
            filtered_matches = [
                match for match in matches
                if not is_user_blocked(user.username, match.username)
                and not is_user_blocked(match.username, user.username)
            ]

            # ✅ Get confirmed connections
            confirmed_connections = get_confirmed_connections(user.username)
            confirmed_usernames = {
                conn['sender_username'] if conn['receiver_username'] == user.username else conn['receiver_username']
                for conn in confirmed_connections
            }

            # ✅ Get pending requests sent by this user
            pending_usernames = set(get_sent_requests(user.username))  # Function returns list of usernames

            return render_template(
                'Client/client_matches.html',
                client=user,
                matches=filtered_matches,
                confirmed_usernames=confirmed_usernames,
                pending_usernames=pending_usernames
            )

        @self.app.route('/send_request/<username>', methods=['POST'])
        def send_request(username):
            if 'username' not in session:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "message": "Unauthorized"}), 401
                return redirect(url_for('client_login'))

            sender = session['username']
            receiver = username

            # ✅ Block check
            if is_user_blocked(sender, receiver) or is_user_blocked(receiver, sender):
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({
                        "success": False,
                        "message": "Cannot send request. You are blocked or have blocked this user."
                    }), 403
                return "❌ Cannot send request. You are blocked or have blocked this user."

            # ✅ Attempt to save the request
            success = save_connection_request(sender, receiver)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                if success:
                    return jsonify({"success": True, "message": "Request sent!"}), 200
                else:
                    return jsonify({"success": False, "message": "Request already sent or blocked."}), 400

            # ✅ Fallback for non-AJAX
            if success:
                return redirect(url_for('client_requests'))
            else:
                return "Request already sent or blocked."

        @self.app.route('/client_requests')
        def client_requests():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            user = self.get_client_by_username(session['username'])
            received_requests = get_requests_received(user.username)

            # Add sender_info to each request
            for req in received_requests:
                req['sender_info'] = get_client_by_username(req['sender_username'])

            return render_template(
                'Client/client_requests.html',
                client=user,
                received_requests=received_requests
            )

        @self.app.route('/handle_request/<int:request_id>/<action>', methods=['POST'])
        def handle_request(request_id, action):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            if action not in ['accept', 'reject']:
                return "Invalid action."

            update_request_status(request_id, action)
            return redirect(url_for('client_requests'))

        @self.app.route('/client_connections')
        def client_connections():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            user = self.get_client_by_username(session['username'])
            if not user:
                return "Client not found."

            connections = get_confirmed_connections(user.username)
            for conn in connections:
                other_user = conn['receiver_username'] if conn['sender_username'] == user.username else conn['sender_username']
                conn['is_blocked'] = is_user_blocked(user.username, other_user)

            return render_template(
                'Client/client_connections.html',
                client=user,
                connections=connections
            )

        @self.app.route('/client_info')
        def client_info():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            user = self.get_client_by_username(session['username'])
            if not user:
                return "Client not found."

            return render_template('Client/client_info.html', client=user)
        

        import os
        from werkzeug.utils import secure_filename

        UPLOAD_FOLDER = 'static/uploads/profile_photos'
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        @self.app.route('/upload_profile_photo', methods=['POST'])
        def upload_profile_photo():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            file = request.files.get('profile_photo')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                user = self.get_client_by_username(session['username'])
                user.profile_photo = filename
                update_client_in_db(user)

                return redirect(url_for('client_info'))

            return "Invalid file or upload error"
        
        @self.app.route('/remove_profile_photo', methods=['POST'])
        def remove_profile_photo():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            username = session['username']
            clients = load_clients_from_db()
            user = next((c for c in clients if c.username == username), None)

            if user:
                # Delete file from disk if it exists
                if user.profile_photo:
                    import os
                    file_path = os.path.join('static', 'uploads', 'profile_photos', user.profile_photo)
                    if os.path.exists(file_path):
                        os.remove(file_path)

                # Clear photo from DB
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE clients SET profile_photo = NULL WHERE username = %s", (username,))
                    conn.commit()
                finally:
                    cursor.close()
                    conn.close()

            return redirect(url_for('client_info'))
        
        @self.app.route('/client_chat')
        def client_chat():
            if not session.get('client_logged_in') or not session.get('username'):
                return redirect(url_for('client_login'))

            username = session['username']
            client = get_client_by_username(username)

            if not client:
                return "Client not found."

            # Get confirmed personal connections
            connections = get_confirmed_connections(username)

            personal_chats = []
            for conn in connections:
                other_user = conn['receiver_username'] if conn['sender_username'] == username else conn['sender_username']
                other_client = get_client_by_username(other_user)
                if other_client:
                    unread_count = get_unread_personal_message_count(other_user, username)
                    other_client.unread_count = unread_count  # dynamically attach attribute
                    personal_chats.append(other_client)

            # Get group chats (no unread count needed)
            group_chats = get_groups_for_user(username)

            return render_template(
                'Messaging/client_chat.html',
                client=client,
                personal_chats=personal_chats,
                group_chats=group_chats
            )
  
        @self.app.route('/chat_with_user/<username>', methods=['GET', 'POST'], endpoint='chat_with_user_route')
        def chat_with_user_view(username):
            if not session.get('client_logged_in') or not session.get('username'):
                return redirect(url_for('client_login'))

            current_user = session['username']

            # ❌ Block check (either user blocked the other)
            if is_user_blocked(current_user, username) or is_user_blocked(username, current_user):
                return "🚫 Chat unavailable. One of you has blocked the other."

            # 👥 Fetch both clients
            my_client = get_client_by_username(current_user)
            other_client = get_client_by_username(username)

            if not my_client or not other_client:
                return "❌ User not found."

            # 💬 Handle message send
            if request.method == 'POST':
                message = request.form.get('message', '').strip()
                if message:
                    save_message(current_user, username, message)

            # 📩 Load messages and mark as read
            messages = get_chat_messages(current_user, username)
            mark_messages_as_read(username, current_user)

            return render_template(
                'Messaging/chat.html',  # ✅ Use the correct template name
                current_user=current_user,
                target_user=username,
                messages=messages
            )

        @self.app.route('/global_chat', methods=['GET', 'POST'])
        def global_chat():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            if request.method == 'POST':
                message = request.form['message']
                if message.strip():
                    save_global_message(session['username'], message)

            messages = get_all_global_messages()
            client = get_client_by_username(session['username'])

            return render_template(
                'Messaging/global_chat.html',
                client=client,
                messages=messages
            )
        
        @self.app.route('/remove_match/<username>', methods=['POST'])
        def remove_match(username):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            user1 = session['username']
            user2 = username
            remove_confirmed_connection(user1, user2)
            return redirect(url_for('client_connections'))

        @self.app.route('/block_user/<username>', methods=['POST'])
        def block_user_route(username):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            blocker = session['username']
            block_user(blocker, username)
            return redirect(url_for('client_connections'))

        @self.app.route('/unblock_user/<username>', methods=['POST'])
        def unblock_user_route(username):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            blocker = session['username']
            unblock_user(blocker, username)
            return redirect(url_for('client_connections'))
        
        @self.app.route('/remove_connection/<username>', methods=['POST'])
        def remove_connection(username):
            if not session.get('client_logged_in'):
                return redirect(url_for('client_login'))

            current_user = session['client_username']
            remove_confirmed_connection(current_user, username)
            return redirect(url_for('client_connections'))

        @self.app.route('/block_user/<username>', methods=['POST'])
        def block(username):
            if not session.get('client_logged_in'):
                return redirect(url_for('client_login'))

            blocker = session['client_username']
            block_user(blocker, username)
            return redirect(url_for('client_connections'))

        @self.app.route('/unblock_user/<username>', methods=['POST'])
        def unblock(username):
            if not session.get('client_logged_in'):
                return redirect(url_for('client_login'))

            unblock_user(session['client_username'], username)
            return redirect(url_for('blocked_users'))

        @self.app.route('/blocked_users')
        def client_blocked_users():
            if not session.get('client_logged_in'):
                return redirect(url_for('client_login'))

            username = session['username']
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT blocked_username FROM blocked_users WHERE blocker_username = %s
                """, (username,))
                blocked = cursor.fetchall()
            except:
                blocked = []
            finally:
                cursor.close()
                conn.close()

            return render_template("client/client_blocked.html", blocked_users=blocked)
        
        @self.app.route('/video_call/<target_user>')
        def video_call(target_user):
            if not session.get('client_logged_in') or 'username' not in session:
                return redirect(url_for('client_login'))

            current_user = session['username']
            return render_template('messaging/video_call.html', current_user=current_user, target_user=target_user)

        @self.app.route('/change_password', methods=['POST'])
        def change_password():
            if not session.get('client_logged_in'):
                return jsonify({'success': False, 'message': 'Unauthorized'}), 401

            data = request.get_json() or {}
            current_password = data.get('current_password', '').strip()
            new_password      = data.get('new_password', '').strip()

            user = get_client_by_username(session['username'])
            if not user or not check_password_hash(user.pin, current_password):
                return jsonify({'success': False, 'message': 'Current password is incorrect'})

            new_hashed = generate_password_hash(new_password)
            if update_client_password(user.username, new_hashed):
                return jsonify({'success': True})

            return jsonify({'success': False, 'message': 'Failed to update password'})

        @self.app.route('/delete_group/<int:group_id>', methods=['POST'])
        def delete_group(group_id):
            if 'username' not in session:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "message": "Unauthorized"}), 401
                return redirect(url_for('client_login'))

            username = session['username']
            group = get_group_by_id(group_id)

            # ✅ Group not found or user is not the admin
            if not group or group['admin_username'] != username:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "message": "Forbidden"}), 403
                return "❌ Forbidden", 403

            # ✅ Proceed to delete group
            success = delete_group_and_messages(group_id)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                if success:
                    return jsonify({"success": True, "message": "Group deleted successfully."}), 200
                else:
                    return jsonify({"success": False, "message": "Failed to delete group."}), 500

            if success:
                return redirect(url_for('client_chat'))
            else:
                return "❌ Failed to delete group.", 500
