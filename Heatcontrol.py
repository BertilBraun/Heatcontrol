import time
import datetime
import RPi.GPIO as GPIO
import TempSensor as TS
import LCD

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

f = open("/home/pi/Desktop/Schaltung/data.txt", "a")
f.write("started new\n")
f.close()
    
while True:
    
    if (len(TS.device_folder) != 2):
        print('failed --> No sensors')
        break
        
    innen = TS.read_temp(0)
    aussen = TS.read_temp(1)
    doing = ""

    if innen < 25:
        doing = "heat"
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
    elif innen > 27 and aussen < innen:
        doing = "cool"
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
    else:
        doing = "perfect"
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)

    LCD.lcd.message = 'Innen  : ' + str(innen) + 'ßC\n' + 'Aussen : ' + str(aussen) + 'ßC'

    output = "Innen: " + str(innen) + " Aussen: " + str(aussen) + " : " + doing + " : " + str(datetime.datetime.now()) + "\n"
    
    print(output)
    
    f = open("/home/pi/Desktop/Schaltung/data.txt", "a")
    f.write(output)
    f.close()
    
    time.sleep(1)
