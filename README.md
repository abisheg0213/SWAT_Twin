**Digital Twin for Water Treatment Plant**

**Project Overview :**
This project showcases the implementation of a digital twin for a water treatment plant, leveraging Python to simulate real-time operations and control mechanisms. The digital twin replicates the behavior of the plant, facilitating monitoring, analysis, and optimization of the water treatment process. It encompasses various stages, including raw water pumping, ultrafiltration, chemical treatment, dechlorination, pH maintenance, and reverse osmosis (RO). Sensor data is collected and logged for further analysis, ensuring the system operates within desired parameters.

**Key Features :**
1. Real-time Simulation: Emulates the dynamic behavior of the water treatment plant with real-time data logging.
2. Modular Design: Each component (sensors, valves, actuators) is modular, allowing for easy adjustments and scalability.
3. Data-Driven Insights: Continuous data collection facilitates in-depth analysis, predictive maintenance, and optimization.
4. Chemical and pH Monitoring: Ensures water quality by maintaining proper chemical levels and pH balance.
5. Automated Control: Simulates automated control mechanisms to manage flow rates, chemical dosing, and water levels.

**Implementation Details**
***Classes and Their Functions***
1. FlowSensor: Monitors and regulates water flow rates.
2. Valve: Controls the start/stop of water flow through pipes.
3. LevelSensor: Tracks and manages water levels in tanks, adjusts based on incoming/outgoing flow.
4. ChemicalSensor: Measures the concentration of specific chemicals in the water.
5. DosingActuator: Adjusts chemical dosing to maintain required concentrations.
6. PHSensor: Monitors and updates the pH level based on chemical content.
7. PHValidator: Maintains the pH balance by adjusting chemical dosing as needed.
8. TankSensor: Monitors the overall water level in a tank, ensuring it stays within specified limits.

**Flow Control and Data Collection**
Initialization: Setup sensors, valves, and actuators with initial parameters.
Simulated Operations: Start and stop water flow through different stages based on predefined intervals.
Real-time Data Logging: Collect sensor data at each step and log it into a CSV file for analysis.
Chemical and pH Management: Monitor and adjust chemical concentrations and pH levels to ensure water quality.

**Data Structure**
Data is logged into a CSV file named SWAT_STAGE1_DATA.csv, capturing the following fields:

1. Timestamp
2. Flow rates (FIT101, FIT201, FIT301, etc.)
3. Valve states (MV101, P101, etc.)
4. Water levels (LIT101, LIT201, etc.)
5. Chemical concentrations (AIT201, AIT202, etc.)
6. Dosing values (P201, P202, etc.)
7. pH values (DPH101)
8. Capacity, low, and high-level markers for tanks
9. Chemical dosing limits

**Procedure to Run the Digital Twin**
1. Make sure python is installed in the system
2. Clone the repository and navigate to the project directory.
3. Run the simulation script to start the digital twin.

```
git clone https://github.com/abisheg0213/SWAT_Twin
cd Stage-05 Back Wash
py swat_twin.py
```
