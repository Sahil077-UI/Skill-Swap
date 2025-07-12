import mysql.connector
from backend.client.client_model import Client


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Onedayiwill",
        port=3306,
        database="skillswap_hub"
    )


def save_client_to_db(client):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clients (
                name, age, gender, aadhar, phone, address,
                username, pin, teach_skills, learn_skills, profile_photo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            client.name,
            client.age,
            client.gender,
            client.id,
            client.ph_no,
            client.address,
            client.username,
            client.pin,
            client.teach_skills,
            client.learn_skills,
            client.profile_photo
        ))

        conn.commit()
        print("✅ Client saved to database.")
        return True
    except mysql.connector.Error as err:
        print("❌ Database Error:", err)
        return False
    finally:
        cursor.close()
        conn.close()


def load_clients_from_db():
    clients = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()

        for row in rows:
            c = Client()
            c.id = row['aadhar']
            c.name = row['name']
            c.age = row['age']
            c.gender = row['gender']
            c.ph_no = row['phone']
            c.address = row['address']
            c.username = row['username']
            c.pin = row['pin']
            c.teach_skills = row['teach_skills']
            c.learn_skills = row['learn_skills']
            c.profile_photo = row.get('profile_photo', '')
            c.created_at = row['created_at']
            clients.append(c)

        print(f"✅ Loaded {len(clients)} client(s) from database.")
    except mysql.connector.Error as err:
        print("❌ Error loading clients:", err)
    finally:
        cursor.close()
        conn.close()

    return clients


def update_client_in_db(client):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clients SET
                name=%s,
                age=%s,
                gender=%s,
                phone=%s,
                address=%s,
                pin=%s,
                teach_skills=%s,
                learn_skills=%s,
                profile_photo=%s
            WHERE aadhar=%s
        """, (
            client.name,
            client.age,
            client.gender,
            client.ph_no,
            client.address,
            client.pin,
            client.teach_skills,
            client.learn_skills,
            client.profile_photo,
            client.id
        ))

        conn.commit()
        print("✅ Client updated in database.")
    except mysql.connector.Error as err:
        print("❌ Failed to update client:", err)
    finally:
        cursor.close()
        conn.close()


def get_admin_by_username(username):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print("❌ Error loading admin:", err)
        return None
    finally:
        cursor.close()
        conn.close()


def save_admin_to_db(username, hashed_pin):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO admins (username, pin) VALUES (%s, %s)", (username, hashed_pin))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()


def save_connection_request(sender_username, receiver_username):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if receiver has blocked the sender
    cursor.execute("""
        SELECT id FROM blocked_users
        WHERE blocker_username = %s AND blocked_username = %s
    """, (receiver_username, sender_username))

    if cursor.fetchone():
        return False  # Blocked, cannot send

    # Check if request already exists
    cursor.execute("""
        SELECT id FROM connection_requests
        WHERE sender_username = %s AND receiver_username = %s
    """, (sender_username, receiver_username))

    if cursor.fetchone():
        return False

    # Insert the request
    cursor.execute("""
        INSERT INTO connection_requests (sender_username, receiver_username, status)
        VALUES (%s, %s, 'pending')
    """, (sender_username, receiver_username))

    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_requests_received(username):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM connection_requests WHERE receiver_username = %s
        """, (username,))
        return cursor.fetchall()
    except:
        return []
    finally:
        cursor.close()
        conn.close()


def get_requests_sent(username):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM connection_requests WHERE sender_username = %s
        """, (username,))
        return cursor.fetchall()
    except:
        return []
    finally:
        cursor.close()
        conn.close()


def update_request_status(request_id, new_status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE connection_requests
            SET status = %s
            WHERE id = %s
        """, (new_status, request_id))
        conn.commit()
    except mysql.connector.Error as err:
        print("❌ Failed to update request:", err)
    finally:
        cursor.close()
        conn.close()


def get_confirmed_connections(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get blocked users (optional, if filtering)
    cursor.execute("""
        SELECT blocked_username FROM blocked_users WHERE blocker_username = %s
        UNION
        SELECT blocker_username FROM blocked_users WHERE blocked_username = %s
    """, (username, username))
    blocked = set(row['blocked_username'] for row in cursor.fetchall())

    # Get confirmed connections
    cursor.execute("""
        SELECT * FROM connection_requests
        WHERE status = 'accept'
        AND (sender_username = %s OR receiver_username = %s)
    """, (username, username))

    all_connections = cursor.fetchall()
    cursor.close()
    conn.close()

    # Filter out blocked users
    filtered = []
    for conn in all_connections:
        other_user = conn['receiver_username'] if conn['sender_username'] == username else conn['sender_username']
        if other_user not in blocked:
            filtered.append(conn)

    return filtered


def save_message(sender, receiver, message):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # or 'skillapp_user' if you created a limited user
            password="Onedayiwill",
            database="skillswap_hub"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (sender_username, receiver_username, message, is_read)
            VALUES (%s, %s, %s, FALSE)
        """, (sender, receiver, message))
        conn.commit()
    except mysql.connector.Error as err:
        print("❌ Error saving message:", err)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def get_chat_messages(user1, user2):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            database="skillswap_hub"
        )

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM messages
            WHERE (sender_username = %s AND receiver_username = %s)
               OR (sender_username = %s AND receiver_username = %s)
            ORDER BY timestamp ASC
        """, (user1, user2, user2, user1))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def mark_messages_as_read(sender, receiver):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            database="skillswap_hub"
        )
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages
            SET is_read = TRUE
            WHERE sender_username = %s AND receiver_username = %s AND is_read = FALSE
        """, (sender, receiver))
        conn.commit()
        print(f"✅ Marked messages from {sender} to {receiver} as read.")
    except mysql.connector.Error as err:
        print("❌ Error marking messages as read:", err)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def get_unread_message_count(username):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            database="skillswap_hub"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT sender_username, COUNT(*) AS count
            FROM messages
            WHERE receiver_username = %s AND is_read = FALSE
            GROUP BY sender_username
        """, (username,))
        results = cursor.fetchall()
        return {row['sender_username']: row['count'] for row in results}
    finally:
        cursor.close()
        conn.close()


def delete_client_from_db(username):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            database="skillswap_hub"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE username = %s", (username,))
        conn.commit()
        print(f"🗑️ Deleted client '{username}'")
    except mysql.connector.Error as err:
        print("❌ Error deleting client:", err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def log_admin_action(admin_username, action, target_username, details=""):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            database="skillswap_hub"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO admin_logs (admin_username, action, target_username, details)
            VALUES (%s, %s, %s, %s)
        """, (admin_username, action, target_username, details))
        conn.commit()
        print(
            f"Logged admin action: {action} on {target_username} by {admin_username}")
    except mysql.connector.Error as err:
        print("❌ Error logging admin action:", err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_group_chat(group_name, admin_username):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insert into group_chats
        cursor.execute("""
            INSERT INTO group_chats (name, admin_username)
            VALUES (%s, %s)
        """, (group_name, admin_username))
        group_id = cursor.lastrowid

        # Add the admin as the first member
        cursor.execute("""
            INSERT INTO group_members (group_id, member_username, added_by)
            VALUES (%s, %s, %s)
        """, (group_id, admin_username, admin_username))

        conn.commit()
        print(
            f"✅ Group '{group_name}' created with ID {group_id} by {admin_username}")
        return group_id
    except mysql.connector.Error as err:
        print("❌ Error creating group:", err)
        return None
    finally:
        cursor.close()
        conn.close()


def add_member_to_group(group_id, new_member_username, added_by):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check group size
        cursor.execute(
            "SELECT COUNT(*) FROM group_members WHERE group_id = %s", (group_id,))
        member_count = cursor.fetchone()[0]
        if member_count >= 4:
            return "limit_reached"

        # Check if user is already in group
        cursor.execute("""
            SELECT * FROM group_members
            WHERE group_id = %s AND member_username = %s
        """, (group_id, new_member_username))
        if cursor.fetchone():
            return "already_member"

        cursor.execute("""
            INSERT INTO group_members (group_id, member_username, added_by)
            VALUES (%s, %s, %s)
        """, (group_id, new_member_username, added_by))

        conn.commit()
        return "success"
    except mysql.connector.Error as err:
        print("❌ Error adding member:", err)
        return "error"
    finally:
        cursor.close()
        conn.close()


def remove_member_from_group(group_id, member_username):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM group_members
            WHERE group_id = %s AND member_username = %s
        """, (group_id, member_username))

        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("❌ Error removing member:", err)
        return False
    finally:
        cursor.close()
        conn.close()


def get_group_by_id(group_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM group_chats WHERE id = %s", (group_id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print("❌ Error fetching group:", err)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_group_members(group_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM group_members
            WHERE group_id = %s
        """, (group_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("❌ Error fetching group members:", err)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def save_group_message(group_id, sender_username, message):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO group_messages (group_id, sender_username, message)
            VALUES (%s, %s, %s)
        """, (group_id, sender_username, message))
        conn.commit()
        print(
            f"💬 Saved group message from {sender_username} in group {group_id}")
    except mysql.connector.Error as err:
        print("❌ Error saving group message:", err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_group_messages(group_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM group_messages
            WHERE group_id = %s
            ORDER BY timestamp ASC
        """, (group_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("❌ Error fetching group messages:", err)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_groups_for_user(username):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT g.* FROM group_chats g
            JOIN group_members m ON g.id = m.group_id
            WHERE m.member_username = %s
        """, (username,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("❌ Error loading user groups:", err)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_client_by_username(username):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM clients WHERE username = %s", (username,))
        row = cursor.fetchone()

        if row:
            client = Client()
            client.id = row['aadhar']
            client.name = row['name']
            client.age = row['age']
            client.gender = row['gender']
            client.ph_no = row['phone']
            client.address = row['address']
            client.username = row['username']
            client.pin = row['pin']
            client.teach_skills = row['teach_skills']
            client.learn_skills = row['learn_skills']
            client.profile_photo = row.get('profile_photo', '')
            client.created_at = row['created_at']
            return client
        else:
            return None
    except mysql.connector.Error as err:
        print("❌ Error loading client:", err)
        return None
    finally:
        cursor.close()
        conn.close()


def save_global_message(username, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO global_messages (sender_username, message) VALUES (%s, %s)",
        (username, message)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_global_messages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT g.*, c.name, c.profile_photo
        FROM global_messages g
        JOIN clients c ON g.sender_username = c.username
        ORDER BY g.timestamp ASC
    """)
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages


def remove_confirmed_connection(user1, user2):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM connection_requests
        WHERE (
            (sender_username = %s AND receiver_username = %s)
            OR
            (sender_username = %s AND receiver_username = %s)
        )
        AND status = 'accept'
    """, (user1, user2, user2, user1))
    conn.commit()
    cursor.close()
    conn.close()


def block_user(blocker, blocked):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO blocked_users (blocker_username, blocked_username)
        VALUES (%s, %s)
    """, (blocker, blocked))
    conn.commit()
    cursor.close()
    conn.close()


def is_user_blocked(blocker, blocked):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM blocked_users
            WHERE blocker_username = %s AND blocked_username = %s
        """, (blocker, blocked))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        print(
            f"❌ Error checking block status between {blocker} and {blocked}:", err)
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def unblock_user(blocker, blocked):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM blocked_users
        WHERE blocker_username = %s AND blocked_username = %s
    """, (blocker, blocked))
    conn.commit()
    cursor.close()
    conn.close()


def get_unread_personal_message_count(sender_username, receiver_username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM messages
        WHERE sender_username = %s AND receiver_username = %s AND is_read = 0
    """, (sender_username, receiver_username))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


def get_client_by_id(client_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def update_client_password(username, hashed_pin):
    """Store a *hashed* PIN for the given username."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE clients SET pin = %s WHERE username = %s",
            (hashed_pin, username)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("❌ Password update error:", err)
        return False
    finally:
        cursor.close()
        conn.close()


def get_sent_requests(sender_username):
    """
    Returns a list of usernames to whom the given sender has sent a connection request (status: pending).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT receiver_username 
            FROM connection_requests 
            WHERE sender_username = %s AND status = 'pending'
        """, (sender_username,))
        results = cursor.fetchall()
        return [row['receiver_username'] for row in results]
    except:
        return []
    finally:
        cursor.close()
        conn.close()


def get_accepted_matches(username):
    """
    Returns a list of usernames who have accepted a mutual match (status: accepted).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN sender_username = %s THEN receiver_username 
                    ELSE sender_username 
                END AS match_user
            FROM connection_requests
            WHERE (sender_username = %s OR receiver_username = %s)
              AND status = 'accepted'
        """, (username, username, username))
        results = cursor.fetchall()
        return [row['match_user'] for row in results]
    except:
        return []
    finally:
        cursor.close()
        conn.close()

def delete_group_and_messages(group_id):
    """
    Deletes a group and all its related messages and members.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Delete messages
        cursor.execute("DELETE FROM group_messages WHERE group_id = %s", (group_id,))
        print(f"🗑 Deleted messages: {cursor.rowcount}")

        # Delete members
        cursor.execute("DELETE FROM group_members WHERE group_id = %s", (group_id,))
        print(f"🗑 Deleted members: {cursor.rowcount}")

        # Delete group (table name is group_chats)
        cursor.execute("DELETE FROM group_chats WHERE id = %s", (group_id,))
        print(f"🗑 Deleted group record: {cursor.rowcount}")

        conn.commit()
        return True

    except Exception as e:
        print(f"❌ Error deleting group {group_id}: {e}")
        return False

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass