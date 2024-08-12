import eventlet
eventlet.monkey_patch()

import time
import csv
from datetime import datetime
from flask import Flask, render_template

import socketio
import threading

# Flask app and Socket.IO server setup
app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins='*',ping_timeout=60, ping_interval=60)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# # Background task to receive ZMQ messages and emit them via Socket.IO
# def background_task():
#     while True:
#         message = socket.recv_multipart()
#         print(message)
#         json_string = message[0].decode('utf-8')
#         data = json.loads(json_string)
#         sio.emit('update_data', data)
#         time.sleep(1)  # Optional sleep to control message frequency

# Socket.IO event handlers
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

# Start background task
# eventlet.spawn(background_task)

# Run the server


class flow_sensor:
    def __init__(self,sensor_name,max_flow_rate):
        self.flow_rate=0
        self.name=sensor_name
        self.max_flow_rate=max_flow_rate
    def set_flow_rate(self,val,level_sensor):
        self.flow_rate=val
        level_sensor.set_level_val()
        collect_data()
        print(f'flow rate {self.flow_rate}')
    def start_flow(self,lvl_sens):
        print(f'{self.name} flow started')
        val=self.max_flow_rate/4
        for sensor in lvl_sens:
            for i in range(4):
                self.set_flow_rate(val*(i+1),sensor)
                time.sleep(1)
    def set_attack_flow(self,attack_data):
        self.flow_rate=attack_data
        
    def stop_flow(self):
        print(f'{self.name} flow stopped')
        self.flow_rate=0

class walve:
    def __init__(self,walve_name,flow_sensor):
        self.state=0
        self.name=walve_name
        self.ass_flow_sensor=flow_sensor
    def open_walve(self,sensor):
        self.state=1
        self.ass_flow_sensor.start_flow(sensor)
    def close_walve(self):
        self.state=0
        self.ass_flow_sensor.stop_flow()

class backpush_level_sensor:
    def __init__(self,name,initial_level,incom_flow_sensor,out_sensor,capacity,low,high,delta):
        self.incoming_sensor=incom_flow_sensor
        self.name=name
        self.outgoing_sensor=out_sensor
        self.level_value=initial_level
        self.capacity=capacity
        self.low_level=low
        self.high_level=high
        self.delta=delta
    def set_level_val(self):
        incs=0
        for i in self.incoming_sensor:
            incs+=i.flow_rate
        self.level_value+=((self.delta*((incs)-(self.outgoing_sensor.flow_rate)))*0.001)
        print(f'{self.name} level {self.level_value}')

class level_sensor:
    def __init__(self,name,initial_level,incom_flow_sensor,out_sensor,capacity,low,high,delta):
        self.incoming_sensor=incom_flow_sensor
        self.name=name
        self.outgoing_sensor=out_sensor
        self.level_value=initial_level
        self.capacity=capacity
        self.low_level=low
        self.high_level=high
        self.delta=delta
    def set_attack_level(self,attack_val):
        # with open("log.txt",'a') as f:
        #     f.write("called")
            
        self.level_value=attack_val
    def set_level_val(self):
        self.level_value+=((self.delta*((self.incoming_sensor.flow_rate)-(self.outgoing_sensor.flow_rate)))*0.001)
        print(f'{self.name} level {self.level_value}')

        
class tank_sensor:
    def __init__(self,lit):
        self.tank_level=(lit.level_value*0.001)
        self.ass_lit_sensor=lit
    def update_tabk_level(self):
        self.tank_level=(self.ass_lit_sensor.level_value)

class chemical_sensor:
    def __init__(self,initial_val,level_Sensor,chemical_monitored):
        self.chemical_value=(initial_val/level_Sensor.level_value)
        self.chemical_monitored=chemical_monitored

chemical_dosing_limit={'NaCl':1.5,'HCl':7.25,'NaOCl':4.25,'Cl2':0.5,'ORP':750,'TDS':500}

class dosing_actuator:
    def __init__(self,chemical_sensor,dosing_type):
        self.assc_sensor=chemical_sensor
        self.dosing_value=0
        self.type=dosing_type
        self.chemical_limit=chemical_dosing_limit[self.type]
    def check_dosing_level(self,level_sensor):
        if((self.chemical_limit)<(self.assc_sensor.chemical_value)):
            temp=(self.assc_sensor.chemical_value)-(self.chemical_limit)
            self.dosing_value=((0-temp))
            self.assc_sensor.chemical_value-=(temp)
        else:
            temp=(self.chemical_limit)-(self.assc_sensor.chemical_value)
            self.assc_sensor.chemical_value+=(temp)
            self.dosing_value=(temp)
    def set_chem_limit(self,val):
        self.chemical_limit=val

class phsensor:
    def __init__(self,clh_Sensor):
        self.ph_value=7
        self.assc_chemical_sensor=clh_Sensor
        self.update_ph_val()
    def update_ph_val(self):
        if(self.assc_chemical_sensor.chemical_value<0.2):
            self.ph_value=14
        elif(self.assc_chemical_sensor.chemical_value>0.5):
            self.ph_value=0
        else:
            self.ph_value=7

class phvalidator:
    def __init__(self,phsensor,chemical_sensor):
        self.assc_chemical_sensor=chemical_sensor
        self.phsensor=phsensor
        self.name="NaHSO3 Neutraliser"
        self.dosing_value=0
    def maintain_ph_dosing(self):
        if(self.phsensor.ph_value==0):
            temp=((self.assc_chemical_sensor.chemical_value-0.5)/2.75)*8.07
            self.dosing_value=temp
            self.phsensor.ph_value=7

# BACK WASH
FIT501=flow_sensor('FIT501',2.789)
P401=walve('P401',FIT501)

  
# STAGE - 01
FIT101=flow_sensor('FIT101',2.654)
MV101=walve('MV101',FIT101)
FIT201=flow_sensor('FIT201',2.471)
P101=walve('P101',FIT201)
LIT101=backpush_level_sensor('LIT101',550,[FIT101,FIT501],FIT201,1500,200,1250,29.34)
T101=tank_sensor(LIT101)
count=0


# STAGE - 02
FIT301=flow_sensor('FIT301',2.521)
P301=walve('P301',FIT301)
LIT201=level_sensor('LIT201',250,FIT201,FIT301,1200,200,1250,15.34)
AIT201=chemical_sensor(256.347,LIT201,'NaCl')
P201=dosing_actuator(AIT201,'NaCl')
AIT202=chemical_sensor(2627.678,LIT201,'HCl')
P202=dosing_actuator(AIT202,'HCl')
AIT203=chemical_sensor(1537.678,LIT201,'NaOCl')
P203=dosing_actuator(AIT203,'NaOCl')


# STAGE - 03
FIT401=flow_sensor('FIT301',3.198)
MV401=walve('MV401',FIT401)
LIT301=level_sensor('LIT301',220,FIT301,FIT401,1200,200,1250,21.478)
AIT301=chemical_sensor(235.97,LIT301,'Cl2')
DPH101=phsensor(AIT301)
PHP101=phvalidator(DPH101,AIT301)

# STAGE BACKWASH

LIT401=level_sensor('LIT401',250,FIT401,FIT501,1200,200,1250,17.549)
AIT401=chemical_sensor((824*200),LIT401,'ORP')
AIT402=chemical_sensor((660*200),LIT401,'TDS')
DP401=dosing_actuator(AIT401,'ORP')
DP402=dosing_actuator(AIT402,'TDS')


print(f'dosing level {PHP101.dosing_value}')
def write_into_csv(data):
    with open('SWAT_STAGE1_DATA.csv','a') as f:
        fields=['Timestamp','FIT101','MV101','LIT101','P101','FIT201','LIT201','AIT201','P201','P201_CL','AIT202','P202','P202_CL','AIT203','P203','P203_CL','P301','FIT301','LIT301','AIT301','DPH101','PHP101','FIT401','MV401','LIT401','AIT401','AIT402','DP401','DP402','P401','FIT501','LIT101 Markers','LIT201 Markers','LIT301 Markers','LIT401 Markers','Chemical Markers']
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writerow(data)


@sio.event
def attack(sid,data):
    print("attack encountered")
    with open('log.txt','a') as f:
        f.write(str(data)+"\n")
    if(data['type']=='valve'):
        if(data['component']=='MV101'):
            if(data['attack_type']=='open'):
                MV101.open_walve([LIT101])
            else:
                MV101.close_walve()
        elif(data['component']=='P101'):
            if(data['attack_type']=='open'):
                P101.open_walve([LIT101,LIT201])
            else:
                P101.close_walve()   
        elif(data['component']=='P301'):
            if(data['attack_type']=='open'):
                P301.open_walve([LIT201,LIT301])
            else:
                P301.close_walve()
        elif(data['component']=='MV401'):
            if(data['attack_type']=='open'):
                MV401.open_walve([LIT301,LIT401])
            else:
                MV401.close_walve()  
        elif(data['component']=='P401'):
            if(data['attack_type']=='open'):
                P401.open_walve([LIT101,LIT401])
            else:
                P401.close_walve()
    elif(data['type']=="flowrate"):
        if(data['component']=='FIT101'):
            FIT101.set_attack_flow(data['flow_rate'])
        if(data['component']=='FIT201'):
            FIT201.set_attack_flow(data['flow_rate'])
        if(data['component']=='FIT301'):
            FIT301.set_attack_flow(data['flow_rate'])
        if(data['component']=='FIT401'):
            FIT401.set_attack_flow(data['flow_rate'])
        if(data['component']=='FIT501'):
            FIT501.set_attack_flow(data['flow_rate'])
    elif(data['type']=="level_static_attack"):
        if(data['component']=='LIT101'):
            LIT101.level_value=data['level_val']
        if(data['component']=='LIT201'):
            LIT201.level_value=data['level_val']
        if(data['component']=='LIT301'):
            LIT301.level_value=data['level_val']
        if(data['component']=='LIT401'):
            LIT401.level_value=data['level_val']
    elif(data['type']=="chemical_attack"):
        if(data['component']=='P201'):
            # with open('log.txt','a') as f:
            #     f.write("p101 case detced")
            P201.set_chem_limit(data['chemical_val'])
        if(data['component']=='P202'):
            P202.set_chem_limit(data['chemical_val'])
        if(data['component']=='P203'):
            P203.set_chem_limit(data['chemical_val'])
    # elif(data['type']=="level_gradual_attack"):
    #     if(data['component']=='LIT101'):
    #         LIT101.delta+=data['devi_val']



def collect_data():
    d=datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    data={
        'Timestamp':d,
        'FIT101':FIT101.flow_rate,
        'MV101':MV101.state,
        'LIT101':LIT101.level_value,
        'P101':P101.state,
        'FIT201':FIT201.flow_rate,
        'LIT201':LIT201.level_value,
        'AIT201':AIT201.chemical_value,
        'P201':P201.dosing_value,
        'P201_CL':P201.chemical_limit,
        'AIT202':AIT202.chemical_value,
        'P202':P202.dosing_value,
        'P202_CL':P202.chemical_limit,
        'AIT203':AIT203.chemical_value,
        'P203':P203.dosing_value,
        'P203_CL':P203.chemical_limit,
        'P301':P301.state,
        'FIT301':FIT301.flow_rate,
        'LIT301':LIT301.level_value,
        'AIT301':AIT301.chemical_value,
        'DPH101':DPH101.ph_value,
        'PHP101':PHP101.dosing_value,
        'FIT401':FIT401.flow_rate,
        'MV401':MV401.state,
        'LIT401':LIT401.level_value,
        'AIT401':AIT401.chemical_value,
        'AIT402':AIT402.chemical_value,
        'DP401':DP401.dosing_value,
        'DP402':DP402.dosing_value,
        'P401':P401.state,
        'FIT501':FIT501.flow_rate,
        'LIT101 Markers':{'CAP':LIT101.capacity,'LR':LIT101.low_level,'HR':LIT101.high_level},
        'LIT201 Markers':{'CAP':LIT201.capacity,'LR':LIT201.low_level,'HR':LIT201.high_level},
        'LIT301 Markers':{'CAP':LIT301.capacity,'LR':LIT301.low_level,'HR':LIT301.high_level},
        'LIT401 Markers':{'CAP':LIT401.capacity,'LR':LIT401.low_level,'HR':LIT401.high_level},
        'Chemical Markers':chemical_dosing_limit
        }
    write_into_csv(data)
    sio.emit('update_data',data)
    return data

def process_loop():
    global count
    while(True):
        print(f'count = {count}')
        LIT101.set_level_val()
        LIT201.set_level_val()
        LIT301.set_level_val()
        LIT401.set_level_val()
        count+=1
        if(count==60):
            P101.open_walve([LIT101,LIT201])
        elif(count==120):
            MV101.open_walve([LIT101])
        elif(count==180):
            P101.close_walve()
        elif(count==240):
            MV101.close_walve()
        elif(count==300):
            P101.open_walve([LIT101,LIT201])
        elif(count==(360)):
            P101.close_walve()
            P201.check_dosing_level(LIT201)
            P202.check_dosing_level(LIT201)
            P203.check_dosing_level(LIT201)
        elif(count==(420)):
            P301.open_walve([LIT201,LIT301]) 
        elif(count==(480)):
            P301.close_walve()
        elif(count==(540)):
            PHP101.maintain_ph_dosing()
            MV401.open_walve([LIT401])
        elif(count==(600)):
            MV401.close_walve()
        elif(count==(660)):
            DP401.check_dosing_level(LIT401)
            DP402.check_dosing_level(LIT401)
        elif(count==720):
            P401.open_walve([LIT101,LIT401])
        elif(count==780):
            count=1
        # message=collect_data()
        # sio.emit('update_data',message)
        print(collect_data())
        time.sleep(1)
if __name__ == '__main__':
    threading.Thread(target=lambda: eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)).start()
    process_loop()