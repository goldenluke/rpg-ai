from collections import deque

# memória limitada por sala
ROOM_MEMORY = {}

MAX_MEMORY = 30


def get_memory(room_id):
    if room_id not in ROOM_MEMORY:
        ROOM_MEMORY[room_id] = deque(maxlen=MAX_MEMORY)
    return ROOM_MEMORY[room_id]


def remember(room_id, texto):
    memoria = get_memory(room_id)
    memoria.append(texto)


def recall(room_id):
    memoria = get_memory(room_id)
    return list(memoria)
