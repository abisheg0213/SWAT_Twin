import zmq
import time
import threading
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5877")
context1 = zmq.Context()
socket = context1.socket(zmq.SUB)
socket.connect("tcp://localhost:12349")
stage=1
def receive_data():
    print("****")
    global stage
    print(stage)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    message = socket.recv_multipart()
    d=message[0].decode('UTF-8')
    data=d
    f=eval(data)
    if(f['LIT101']<=500 and stage==1):
        print("attack found")
        publisher.send_json({
            'type':'valve',
                'component':'MV101',
                'command':'open'
        })
    if(f['LIT101']>=600 and stage==1):
        stage=2
        publisher.send_json({
            'type':'valve',
                'component':'MV101',
                'command':'close'
        })
    if(f['LIT201']<=250 and stage==2):
        print("attack found")
        publisher.send_json({
            'type':'valve',
                'component':'P101',
                'command':'open'
        })
    if(f['LIT201']>=350 and stage==2):
        stage=3
        print("attack found")
        publisher.send_json({
            'type':'valve',
                'component':'P101',
                'command':'close'
        })       
    if(f['LIT301']<=220 and stage==3):
        print("attack found")
        publisher.send_json({
            'type':'valve',
                'component':'P301',
                'command':'open'
        })
    if(f['LIT301']>=320 and stage==3):
        stage=4
        print("attack found")
        publisher.send_json({
            'type':'valve',
                'component':'P301',
                'command':'close'
        })
    if(f['LIT401']<=250 and stage==4):
        print("attack found")
        publisher.send_json({
            'type':'valve',
                'component':'MV401',
                'command':'open'
        })
    if(f['LIT401']>=350 and stage==4):
        stage=5
        print("attack found")
        publisher.send_json({
            'type':'valve',
                'component':'MV401',
                'command':'close'
        })
    return f
def send():
    while True:
        publisher.send_json({
            'type':'valve',
                'component':'MV101',
                'command':'open'
        })
def main_loop():
    while True:
        receive_data()
        time.sleep(1)
if __name__=="__main__":
    main_loop()