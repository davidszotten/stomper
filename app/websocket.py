from collections import defaultdict
import json


participants = defaultdict(list)


def handle_websocket(user, socket):
    participants[user].append(socket)

    try:
        while True:
            message = socket.receive()
            if message is None:
                break

            try:
                message = json.loads(message)
            except ValueError:
                message = {}

            broadcast({
                user: len(sockets)
                for user, sockets in participants.items()
            })

    finally:
        socket.close()
        participants[user].remove(socket)
        if not participants[user]:
            participants.pop(user)


def send(user, message):
    sockets = participants.get(user, [])
    for socket in sockets:
        socket.send(json.dumps(message))


def broadcast(message):
    for user, sockets in participants.items():
        for socket in sockets:
            socket.send(json.dumps(message))
