from flask import Flask
from backend.client.client import ClientPanel
from backend.admin.admin import AdminPanel
from flask import render_template
from backend.messaging.support_chat import SupportChat
from backend.messaging.group_chat import GroupChatPanel
from backend.messaging.chat import ChatPanel
from flask_socketio import SocketIO
from flask_socketio import emit, join_room
from backend.messaging.video_socket import register_video_events

app = Flask(__name__)
# app.secret_key = 'your_secret_key'
app.secret_key = "your_secure_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

# Register client routes
ClientPanel(app)
AdminPanel(app)
ChatPanel(app)
SupportChat(app)
GroupChatPanel(app)
register_video_events(socketio)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('user-joined', room=room)

@socketio.on('signal')
def on_signal(data):
    room = data['room']
    emit('signal', data, room=room, include_self=False)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)