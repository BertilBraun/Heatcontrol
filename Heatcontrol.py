import time
import datetime
import RPi.GPIO as GPIO
import TempSensor as TS
import LCD

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

path = "/home/pi/Desktop/Schaltung/data" + str(datetime.datetime.now()) + ".txt"

f = open(path, "w")
f.write("started new\n")

heatedLastTime = False
procedure = ""
    
while True:
    
    if (len(TS.device_folder) != 2):
        print('failed --> No sensors')
        break
        
    innen = TS.read_temp(0)
    aussen = TS.read_temp(1)
    

    if innen < 25:
	
        if not heatedLastTime:
            GPIO.output(6, GPIO.HIGH)
        else:
            GPIO.output(6, GPIO.LOW)
            
        procedure = "heat"
        heatedLastTime = False
		
        GPIO.output(5, GPIO.LOW)
		
    elif innen > 27 and aussen < innen:
	  
        if heatedLastTime:
            GPIO.output(6, GPIO.HIGH)
        else:
            GPIO.output(6, GPIO.LOW)
          
        procedure = "cool"
        heatedLastTime = True
		
        GPIO.output(5, GPIO.HIGH)		
			
    else:
	
        if heatedLastTime:
            GPIO.output(6, GPIO.HIGH)
        else:
            GPIO.output(6, GPIO.LOW)
            
        procedure = "perfect"
        heatedLastTime = False
		
        GPIO.output(5, GPIO.LOW)

    currentTime = str(datetime.datetime.now())
    message = 'Innen  : ' + str(innen) + 'ßC\n' + 'Aussen : ' + str(aussen) + 'ßC'
	
    LCD.lcd.message = message

    print(message + " : " + procedure + " : " + currentTime + "\n")
    f.write(message + " : " + procedure + " : " + currentTime + "\n")
    f.flush()
    
    time.sleep(1)
