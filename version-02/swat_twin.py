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
        for sensor in lvl_sens:
            for i in range(4):
                self.set_flow_rate(val*(i+1),sensor)
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

class chemical_sensor:
    def __init__(self,initial_val,chemical_monitored):
        self.chemical_value=initial_val
        self.chemical_monitored="NaCl"

chemical_dosing_limit={'NaCl':1.5,'HCl':7.25,'NaOCl':4.25}

class dosing_actuator:
    def __init__(self,chemical_sensor,dosing_type):
        self.assc_sensor=chemical_sensor
        self.dosing_value=0
        self.type=dosing_type
    def check_dosing_level(self,level_sensor):
        if(level_sensor.level_value*chemical_dosing_limit[self.type]<self.assc_sensor.chemical_value):
            temp=self.assc_sensor.chemical_value-level_sensor.level_value*chemical_dosing_limit[self.type]
            self.dosing_value=(0-temp)
            self.assc_sensor.chemical_value-=(temp)
        else:
            temp=level_sensor.level_value*chemical_dosing_limit[self.type]-self.assc_sensor.chemical_value
            self.assc_sensor.chemical_value+=(temp)
            self.dosing_value=temp


FIT101=flow_sensor('FIT101',2.654)
MV101=walve('MV101',FIT101)
FIT201=flow_sensor('FIT201',2.471)
P101=walve('P101',FIT201)
LIT101=level_sensor('LIT101',550,FIT101,FIT201,1500,200,1250,29.34)
T101=tank_sensor(LIT101)
count=0
AIT201=chemical_sensor(256.347,'NaCl')
FIT301=flow_sensor('FIT301',2.521)
P301=walve('P301',FIT301)
LIT201=level_sensor('LIT201',250,FIT201,FIT301,1200,200,1250,15.34)
P201=dosing_actuator(AIT201,'NaCl')
AIT202=chemical_sensor(2627.678,'HCl')
P202=dosing_actuator(AIT202,'HCl')
AIT203=chemical_sensor(1537.678,'NaOCl')
P203=dosing_actuator(AIT203,'NaOCl')
def write_into_csv(data):
    with open('SWAT_STAGE1_DATA.csv','a') as f:
        fields=['Timestamp','FIT101','MV101','LIT101','FIT201','P101','LIT201','AIT201','P201','P301','FIT301','AIT202','P202','AIT203','P203','LIT201 Markers','LIT101 Markers']
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
        'LIT201':LIT201.level_value,
        'AIT201':AIT201.chemical_value,
        'P201':P201.dosing_value,
        'P301':P301.state,
        'FIT301':FIT301.flow_rate,
        'AIT202':AIT202.chemical_value,
        'P202':P202.dosing_value,
        'AIT203':AIT203.chemical_value,
        'P203':P203.dosing_value,
        'LIT201 Markers':{'CAP':LIT201.capacity,'LR':LIT201.low_level,'HR':LIT201.high_level},
        'LIT101 Markers':{'CAP':LIT101.capacity,'LR':LIT101.low_level,'HR':LIT101.high_level}
    }
    write_into_csv(data)
    return data
while(True):
    print(f'count = {count}')
    LIT101.set_level_val()
    LIT201.set_level_val()
    count+=1
    if(count==5):
        P101.open_walve([LIT101,LIT201])
    elif(count==10):
        MV101.open_walve([LIT101])
    elif(count==15):
        P101.close_walve()
    elif(count==20):
        MV101.close_walve()
    elif(count==25):
        P101.open_walve([LIT101,LIT201])
    elif(count==30):
        P101.close_walve()
        P201.check_dosing_level(LIT201)
        P202.check_dosing_level(LIT201)
        P203.check_dosing_level(LIT201)
        P301.open_walve([LIT201])  #LIT301 needs to be added here
    elif(count==35):
        break;
    print(collect_data())
    time.sleep(1)
