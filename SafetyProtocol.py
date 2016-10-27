#!/usr/bin/en 

import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIR = 4

print "The Safety Protocol (CTRL-C to exit)"

GPIO.setup(GPIO_PIR,GPIO.IN)   

Current_State  = 0
Previous_State = 0


try:
  print "Calibrating the PIR"
  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0    
  print "  Ready"     
  # Loop until user quits with CTRL-C
  while True :
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      print "  Motion detected!"
      publish.single("[Target topic]", "Motion detected!", hostname="[Target address]")
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      print "  Ready"
      Previous_State=0
    # Wait for 10 milliseconds
    time.sleep(0.01)      
      
except KeyboardInterrupt:
  print "  Quit" 
  # Reset GPIO settings
  GPIO.cleanup()