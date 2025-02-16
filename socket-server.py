import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kh11backend.settings")
django.setup()


from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from user.models import CallHistory
from django.contrib.auth import authenticate
import socketio
import eventlet
import eventlet.wsgi

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio, sio)

# Store authenticated users
connected_users = {}
connected_users_sid = {}

def get_sid(user):
    return connected_users_sid.get(user.username) or None


def verify_jwt_token(token):
    """ Verify JWT token and return the authenticated user """
    try:
        access_token = AccessToken(token)
        print("Decoded Token Payload:", access_token.payload)  # Debugging line
        user_id = access_token["user_id"]  # Ensure key exists
        user = User.objects.get(id=user_id)
        return user
    except KeyError:
        print("JWT payload missing 'user_id'")
    except Exception as e:
        print(f"JWT verification failed: {e}")
    return None
    

@sio.event()
def connect(sid, environ):
    sio.emit('ack', room=sid)
    
    
@sio.event 
def authenticate_user(sid, data):
    token = data.get('jwt')
    
    user = verify_jwt_token(token)
    print(user)
    if user:
        connected_users[sid] = user
        connected_users_sid[user.username] = sid
        sio.emit("authenticated", {"message": "Authentication successful"}, room=sid)
        users = User.objects.all()
        dataToSend = []
        for user in users:
            sid = get_sid(user)
            dataToSend.append({ 'username': user.username, 'sid': sid, 'online': (sid is not None) })    
        sio.emit("all_users", data=dataToSend, room=None)
        print(f"User {user.username} authenticated with SID {sid}")
    else:
        sio.emit("auth_error", {"message": "Invalid credentials"}, room=sid)
        

@sio.event
def get_all_users(sid):
    users = User.objects.all()
    
    dataToSend = []
    for user in users:
        sid = get_sid(user)
        dataToSend.append({ 'username': user.username, 'sid': sid, 'online': (sid is not None) })    
        
    sio.emit("all_users", data=dataToSend, room=sid)    
    
@sio.event
def offer(sid, data):
    """ Forward WebRTC offer to the target user """
    if sid not in connected_users:
        sio.emit("auth_error", {"message": "Unauthorized"}, room=sid)
        return

    target_sid = data["to"]
    data['from'] = connected_users[sid].username
    data['from-sid'] = sid
    sio.emit("offer", data, room=target_sid)

@sio.event
def answer(sid, data):
    """ Forward WebRTC answer """
    if sid not in connected_users:
        sio.emit("auth_error", {"message": "Unauthorized"}, room=sid)
        return

    target_sid = data["to"]
    sio.emit("answer", data, room=target_sid)
    
@sio.event
def end_call(sid, data):
    if sid not in connected_users:
        sio.emit("auth_error", {"message": "Unauthorized"}, room=sid)
        return
    
    target_sid = data['to']
    sio.emit('end_call', room=target_sid)
    
@sio.event 
def reject(sid, data):
    if sid not in connected_users:
        sio.emit("auth_error", { 'message': "Unauthorized" }, room=sid)
        
    target_sid = data['to']
    sio.emit('reject', data, room=target_sid)
    
    
@sio.event 
def end_call(sid, data):
    if sid not in connected_users:
        sio.emit("auth_error", { 'message': "Unauthorized" }, room=sid)
        
    target_sid = data['to']
    sio.emit("end_call", data, room=target_sid)
    
@sio.event 
def add_call_history(sid, data):
    if sid not in connected_users:
        sio.emit("auth_error", { 'message': "Unauthorized" }, room=sid)
        
    sender = connected_users[sid]
    receiver = connected_users[data['to']]
    
    new_call_history = CallHistory(sender=sender, receiver=receiver, duration=data['duration'], accepted=data['accepted'])    

@sio.event
def candidate(sid, data):
    """ Forward ICE candidate """
    if sid not in connected_users:
        sio.emit("auth_error", {"message": "Unauthorized"}, room=sid)
        return

    target_sid = data["to"]
    sio.emit("candidate", data, room=target_sid)

@sio.event
def disconnect(sid):
    """ Handle user disconnection """
    if sid in connected_users:
        print(f"User {connected_users[sid].username} disconnected")
        del connected_users[sid]
    print(f"Client disconnected: {sid}")
    
    users = User.objects.all()
    dataToSend = []
    for user in users:
        sid = get_sid(user)
        dataToSend.append({ 'username': user.username, 'sid': sid, 'online': (sid is not None) })    
    sio.emit("all_users", data=dataToSend, room=None)

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)
        
    
    