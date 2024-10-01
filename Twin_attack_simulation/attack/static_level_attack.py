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
                'type': 'level',
                'component': 'LIT101',
                'command': 'static',       
                'attack-value': 100       
            }
        socket.send_json(attack_message_1)
        print("Attack messages sent successfully!")
        if(count==7):
            break
        time.sleep(1)
        

