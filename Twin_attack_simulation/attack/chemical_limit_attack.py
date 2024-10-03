import zmq
import time
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5878")  


if __name__ == "__main__":
    count=0
    while True:
        count+=1
        attack_message_1 = {
            'type':'chemical',
                'component':'P201',
                'command':'marker change',
                'attack-value': 3.25
        }
        socket.send_json(attack_message_1)
        print("Attack messages sent successfully!")
        if(count==7):
            break
        time.sleep(1)