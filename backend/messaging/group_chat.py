from flask import render_template, request, redirect, url_for, session
from backend.database.database_utils import (
    create_group_chat,
    get_group_by_id,
    add_member_to_group,
    remove_member_from_group,
    get_group_members,
    get_group_messages,
    save_group_message
)

class GroupChatPanel:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/create_group', methods=['GET', 'POST'])
        def create_group():
            if 'username' not in session:
                return redirect(url_for('client_login'))

            if request.method == 'POST':
                group_name = request.form['group_name'].strip()
                admin = session['username']
                group_id = create_group_chat(group_name, admin)
                if group_id:
                    return redirect(url_for('view_group', group_id=group_id))
                return "❌ Failed to create group."
            return render_template('Messaging/create_group.html')

        @self.app.route('/group/<int:group_id>')
        def view_group(group_id):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            group = get_group_by_id(group_id)
            if not group:
                return "⚠️ Group not found"

            members = get_group_members(group_id)
            current_user = session['username']
            is_admin = (group['admin_username'] == current_user)
            messages = get_group_messages(group_id)

            return render_template(
                'Messaging/group_view.html',
                group=group,
                members=members,
                messages=messages,
                is_admin=is_admin,
                current_user=current_user
            )

        @self.app.route('/group/<int:group_id>/message', methods=['POST'])
        def send_group_message(group_id):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            sender = session['username']
            message = request.form['message'].strip()
            if message:
                save_group_message(group_id, sender, message)
            return redirect(url_for('view_group', group_id=group_id))

        @self.app.route('/group/<int:group_id>/add_member', methods=['POST'])
        def add_group_member(group_id):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            added_by = session['username']
            new_member = request.form['new_member_username']  # ✅ Match this name with the HTML form

            result = add_member_to_group(group_id, new_member, added_by)

            if result == "limit_reached":
                return "❌ Cannot add more than 4 members."
            elif result == "already_member":
                return f"⚠️ {new_member} is already in the group."
            elif result == "success":
                return redirect(url_for('view_group', group_id=group_id))
            else:
                return "❌ Error adding member."


        @self.app.route('/group/<int:group_id>/remove_member/<member_username>', methods=['POST'])
        def remove_group_member(group_id, member_username):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            current_user = session['username']
            group = get_group_by_id(group_id)

            if group['admin_username'] != current_user:
                return "⛔ Only group admin can remove members."
            if member_username == current_user:
                return "⚠️ Admin can't remove themselves."

            remove_member_from_group(group_id, member_username)
            return redirect(url_for('view_group', group_id=group_id))
        
        @self.app.route('/group/<int:group_id>/chat', methods=['GET', 'POST'])
        def group_chat(group_id):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            username = session['username']

            group = get_group_by_id(group_id)
            if not group:
                return "⚠️ Group not found."

            members = get_group_members(group_id)
            member_usernames = [m['member_username'] for m in members]

            if username not in member_usernames:
                return "🚫 You are not a member of this group."

            if request.method == 'POST':
                message = request.form.get('message', '').strip()
                if message:
                    save_group_message(group_id, username, message)

            messages = get_group_messages(group_id)

            return render_template(
                'Messaging/group_chat.html',
                group=group,
                members=members,
                messages=messages,
                current_user=username
            )

        @self.app.route('/leave_group/<int:group_id>', methods=['POST'])
        def leave_group(group_id):
            if 'username' not in session:
                return redirect(url_for('client_login'))

            username = session['username']
            group = get_group_by_id(group_id)

            # Prevent group admin from leaving their own group
            if group and group['admin_username'] != username:
                remove_member_from_group(group_id, username)

            return redirect(url_for('client_profile'))