# SkillSwapHub

SkillSwapHub is a Python Flask-based web application designed to connect users who want to **teach** and **learn** different skills. It offers a seamless experience for user registration, profile matching, real-time chatting, group discussions, support interaction, and even video calling.

---

## 🔧 Features

### 👤 Client Features
- Secure client registration with profile photo
- Teach and learn skills selection
- Profile editing and password reset (hashed PIN support)
- View matched users based on skill compatibility (fuzzy matching)
- Send and accept connection requests
- Private 1-on-1 messaging with read status

### 🧠 Skill Matching Engine
- Matches users by comparing:
  - Skills they want to **learn**
  - With other users who want to **teach**, and vice versa
- Uses Python’s `difflib.SequenceMatcher` for fuzzy matching

### 💬 Messaging System
- Direct personal messaging
- Seen/unseen badge with `is_read` tracking
- Group chat with admin-controlled membership
- Global message wall (public messages from users)
- Support ticket messaging for users and admins

### 📹 Video Calling (WebRTC)
- Socket.IO-powered signaling
- Real-time video chat between connected users

### 🔒 Admin Features
- Admin login system (with support for multiple admins)
- View/edit/delete client accounts
- View client activity logs
- Manage support requests from clients
- Admin action logging

---

## 🗃️ Database Structure

The project uses **MySQL** as its backend with tables like:

- `clients`
- `admins`
- `connection_requests`
- `messages`
- `group_chats`, `group_members`, `group_messages`
- `global_messages`
- `support_messages`
- `admin_logs`, `client_logs`
- `blocked_users`

## 🚀 Getting Started

## 🛠 Tech Stack

- **Backend**: Python, Flask, Flask-SocketIO
- **Database**: MySQL
- **Frontend**: HTML, CSS (Tailwind), JS
- **Real-Time Communication**: Socket.IO, WebRTC

---

## 🔐 Security Notes

- All passwords/PINs are stored **hashed** using a secure hashing algorithm.
- Users can block others; connection and message attempts are prevented accordingly.
- Admins have limited access based on roles (`super admin` vs normal admin).

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change or improve.
