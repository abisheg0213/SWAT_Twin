import time
import csv
from datetime import datetime

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
        for i in range(4):
            self.set_flow_rate(val*(i+1),lvl_sens)
            time.sleep(1)
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
    def set_level_val(self):
        self.level_value+=((self.delta*((self.incoming_sensor.flow_rate)-(self.outgoing_sensor.flow_rate)))*0.001)
        print(f'{self.name} level {self.level_value}')

class tank_sensor:
    def __init__(self,lit):
        self.tank_level=(lit.level_value*0.001)
        self.ass_lit_sensor=lit
    def update_tabk_level(self):
        self.tank_level=(self.ass_lit_sensor.level_value)


FIT101=flow_sensor('FIT101',2.654)
MV101=walve('MV101',FIT101)
FIT201=flow_sensor('FIT201',2.471)
P101=walve('P101',FIT201)
LIT101=level_sensor('LIT101',550,FIT101,FIT201,1500,200,1250,9.34)
T101=tank_sensor(LIT101)
count=0

def write_into_csv(data):
    with open('SWAT_STAGE1_DATA.csv','a') as f:
        fields=['Timestamp','FIT101','MV101','LIT101','FIT201','P101','LIT101 Markers']
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writerow(data)


def collect_data():
    d=datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    data={
        'Timestamp':d,
        'FIT101':FIT101.flow_rate,
        'MV101':MV101.state,
        'LIT101':LIT101.level_value,
        'FIT201':FIT201.flow_rate,
        'P101':P101.state,
        'LIT101 Markers':{'CAP':LIT101.capacity,'LR':LIT101.low_level,'HR':LIT101.high_level}
    }
    write_into_csv(data)
    return data
while(True):
    print(f'count = {count}')
    LIT101.set_level_val()
    count+=1
    if(count==50):
        P101.open_walve(LIT101)
    elif(count==100):
        MV101.open_walve(LIT101)
    elif(count==150):
        P101.close_walve()
    elif(count==200):
        MV101.close_walve()
    elif(count==300):
        break;
    print(collect_data())
    time.sleep(1)
