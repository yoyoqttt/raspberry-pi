import smbus
import time
import multiprocessing
import board
import busio as io
import adafruit_mlx90614
from time import sleep
from firebase import firebase


firebase = firebase.FirebaseApplication('https://hack-b7291-default-rtdb.firebaseio.com/', None)


i2c_mlx = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c_mlx)


PCF8591_ADDRESS = 0x48
PULSE_SENSOR_CHANNEL = 0
ECG_CHANNEL = 1

bus = smbus.SMBus(1) 

def read_pulse_sensor():
    try:
        while True:
           
            analog_value = bus.read_byte_data(PCF8591_ADDRESS, PULSE_SENSOR_CHANNEL)
            
           
            print("Pulse Sensor Value:", analog_value)


            pulse_data = {
                'value': analog_value,
                'timestamp': int(time.time())
            }
            result = firebase.put('/PulseSensorData', 'latest', pulse_data) 

            time.sleep(3) 

    except KeyboardInterrupt:
        print("Pulse sensor program terminated by the user.")

def read_ecg_data():
    try:
        while True:
         
            analog_value = bus.read_byte_data(PCF8591_ADDRESS, ECG_CHANNEL)
            
            
            print("ECG Raw Value:", analog_value)

        
            ecg_data = {
                'value': analog_value,
                'timestamp': int(time.time())
            }
            result = firebase.put('/ECGData', 'latest', ecg_data)  

            time.sleep(3)  
    except KeyboardInterrupt:
        print("ECG program terminated by the user.")

def read_temp_sensor():
    try:
        while True:
            ambient_temp = mlx.ambient_temperature
            object_temp = mlx.object_temperature

            print(f"Ambient Temperature: {ambient_temp:.2f} °C")
            print(f"Object Temperature: {object_temp:.2f} °C")

            
            temp_data = {
                'ambient_temperature': ambient_temp,
                'object_temperature': object_temp,
                'timestamp': int(time.time())
            }
            result = firebase.put('/TemperatureData', 'latest', temp_data) 

    except KeyboardInterrupt:
        print("Temperature sensor program terminated by the user.")

if name == "main":
    try:
        
        pulse_process = multiprocessing.Process(target=read_pulse_sensor)
        ecg_process = multiprocessing.Process(target=read_ecg_data)
        temp_process = multiprocessing.Process(target=read_temp_sensor)

        
        pulse_process.start()
        ecg_process.start()
        temp_process.start()

        
        pulse_process.join()
        ecg_process.join()
        temp_process.join()

    except KeyboardInterrupt:
        print("Main program terminated by the user.")
