
import time
import csv
from datetime import datetime
import threading


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
LIT101=backpush_level_sensor('LIT101',500,[FIT101,FIT501],FIT201,1500,200,1250,29.34)
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


def collect_data():
    LIT101.set_level_val()
    LIT201.set_level_val()
    LIT301.set_level_val()
    LIT401.set_level_val()
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
    return data
import zmq
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:12349")
context1 = zmq.Context()
socket = context1.socket(zmq.SUB)
socket.connect("tcp://localhost:5877")
socket.setsockopt(zmq.SUBSCRIBE, b"")
state_lock = threading.Lock()
def recevie_data():
    while True:
        socket.setsockopt(zmq.SUBSCRIBE, b"")
        with state_lock:
            message = socket.recv_multipart()
            d=message[0].decode('UTF-8')
            data=d
            f=eval(data)
            print(f)
            data=f
            if(data['type']=='valve'):
                if(data['component']=='MV101'):
                    if(data['command']=='open'):
                        MV101.open_walve([LIT101])
                        print("MV101 STATE"+str(MV101.state))
                    else:
                        MV101.close_walve()
                elif(data['component']=='P101'):
                    if(data['command']=='open'):
                        P101.open_walve([LIT101,LIT201])
                    else:
                        P101.close_walve()
                        P201.check_dosing_level(LIT201)
                        P202.check_dosing_level(LIT201)
                        P203.check_dosing_level(LIT201)   
                elif(data['component']=='P301'):
                    if(data['command']=='open'):
                        P301.open_walve([LIT201,LIT301]) 
                    else:
                        P301.close_walve()
                        PHP101.maintain_ph_dosing()        
                elif(data['component']=='MV401'):
                    if(data['command']=='open'):
                        MV401.open_walve([LIT401])
                    else:
                        MV401.close_walve()
                        DP401.check_dosing_level(LIT401)
                        DP402.check_dosing_level(LIT401)
 
        time.sleep(1)
def send_data():
    while True:
        while state_lock:
            data=collect_data()
            publisher.send_json(data)
            time.sleep(1)
if __name__ == '__main__':
    th1=threading.Thread(target=send_data)
    th2=threading.Thread(target=recevie_data)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
   
