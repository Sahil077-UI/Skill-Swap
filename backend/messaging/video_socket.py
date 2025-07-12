from flask_socketio import emit, join_room

def register_video_events(socketio):
    @socketio.on('join')
    def handle_join(data):
        room = get_room(data['from'], data['to'])
        join_room(room)
        emit('user-joined', {'user': data['from']}, room=room)
        print(f"🔗 {data['from']} joined room {room}")

    @socketio.on('offer')
    def handle_offer(data):
        room = get_room(data['from'], data['to'])
        emit('offer', data['offer'], room=room, include_self=False)
        print(f"📡 Offer from {data['from']} to {data['to']}")

    @socketio.on('answer')
    def handle_answer(data):
        room = get_room(data['from'], data['to'])
        emit('answer', data['answer'], room=room, include_self=False)
        print(f"✅ Answer from {data['from']} to {data['to']}")

    @socketio.on('ice-candidate')
    def handle_ice_candidate(data):
        room = get_room(data['from'], data['to'])
        emit('ice-candidate', data['candidate'], room=room, include_self=False)

    @socketio.on('end-call')
    def handle_end_call(data):
        room = get_room(data['from'], data['to'])
        emit('end-call', room=room, include_self=False)

# Utility to generate unique room name
def get_room(user1, user2):
    return '-'.join(sorted([user1, user2]))