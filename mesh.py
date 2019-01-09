import threading
import Adafruit_DHT as dht
from picamera import PiCamera
from time import sleep
import os
import sys

import RPi.GPIO as GPIO
import serial
import time
import datetime
import socket

fire = 90
rip = 23 
DHT22_1 = 4
DHT22_2 = 6




ser = serial.Serial("/dev/ttyS0", 115200)
print(ser.portstr)

serialFromArduino = serial.Serial("/dev/ttyACM0", 14400)
print(serialFromArduino .portstr)
serialFromArduino.flushInput()


GPIO.setmode(GPIO.BCM)
GPIO.setup(rip, GPIO.IN)

camera = PiCamera() #camera

local_data = bytearray([0xCA, 0xFF, 0xFF, 0x04, 0x11, 0x0B, 0x09, 0x01, 0xF0])
remote_data = bytearray([0xCA, 0x80, 0x02, 0x04, 0x21, 0x0B, 0x09, 0x01, 0xF0])

ble32 = bytearray([0xCA, 0x80, 0x35, 0x04, 0x21, 0x0B, 0x04, 0x01, 0xF0])

led_state = [0, 0, 0, 0, 0, 0, 0]



def localLedOnOff(on_off, delay):
	if on_off == 1:
		local_data[7] = 0x01
	else:
		local_data[7] = 0x00
	ser.write(local_data)
	time.sleep(delay)
	

def remoteLedOnOff(which, on_off, delay):
	if which ==1:
		remote_data[2] = 0x02
	elif which == 2:
		remote_data[2] = 0x04
	elif which == 3:
		remote_data[2] = 0x35
	elif which == 4:
		remote_data[2] = 0x37


	if on_off == 1:
		remote_data[7] = 0x01
	else:
		remote_data[7] = 0x00

	ser.write(remote_data)
	time.sleep(delay)

def remote_32(on_off, delay):
	if on_off == 1:
		ble32[7] = 0x01
	else:
		ble32[7] = 0x00

	ser.write(ble32)
	time.sleep(delay)


def allLedOnoff(on_off):
	arr = [1,2,3,4]

	if on_off == 1:
		localLedOnOff(1, 0.5)
		for i in arr:
			remoteLedOnOff(i, 1, 0.5)
		remote_32(1, 0.5)
		
	else:
		localLedOnOff(0, 0.5)
		for i in arr:
			remoteLedOnOff(i, 0, 0.5)
		remote_32(0, 0.5)

def toggle(idx):
	if led_state[idx] == 1: 
		 led_state[idx] = 0

	else:
		led_state[idx] = 1

def exitPrint(which, con):
	exit_Ldata1 = bytearray([0xCA, 0xFF, 0xFF, 0x04, 0x11, 0x0B, 0x0A, 0x01, 0xF0])
	exit_Ldata2 = bytearray([0xCA, 0xFF, 0xFF, 0x04, 0x11, 0x0B, 0x0B, 0x01, 0xF0])
	exit_Rdata1 = bytearray([0xCA, 0x80, 0x02, 0x04, 0x21, 0x0B, 0x0A, 0x01, 0xF0])
	exit_Rdata2 = bytearray([0xCA, 0x80, 0x02, 0x04, 0x21, 0x0B, 0x0B, 0x01, 0xF0])
	exit_Rdata3 = bytearray([0xCA, 0x80, 0x04, 0x04, 0x21, 0x0B, 0x0A, 0x01, 0xF0])
	exit_Rdata4 = bytearray([0xCA, 0x80, 0x04, 0x04, 0x21, 0x0B, 0x0B, 0x01, 0xF0])
	
	exit_Rdata5 = bytearray([0xCA, 0x80, 0x35, 0x04, 0x21, 0x0B, 0x0A, 0x01, 0xF0])
	exit_Rdata6 = bytearray([0xCA, 0x80, 0x37, 0x04, 0x21, 0x0B, 0x0A, 0x01, 0xF0])

	exit_Rdata7 = bytearray([0xCA, 0x80, 0x35, 0x04, 0x21, 0x0B, 0x0B, 0x01, 0xF0])

	exit_Rdata8 = bytearray([0xCA, 0x80, 0x32, 0x04, 0x21, 0x0B, 0x03, 0x01, 0xF0])
	exit_Rdata9 = bytearray([0xCA, 0x80, 0x32, 0x04, 0x21, 0x0B, 0x09, 0x01, 0xF0])

	exit_Rdata10 = bytearray([0xCA, 0x80, 0x33, 0x04, 0x21, 0x0B, 0x03, 0x01, 0xF0])
	exit_Rdata11 = bytearray([0xCA, 0x80, 0x33, 0x04, 0x21, 0x0B, 0x09, 0x01, 0xF0])

	exit_Rdata12 = bytearray([0xCA, 0x80, 0x41, 0x04, 0x21, 0x0B, 0x03, 0x01, 0xF0])
	exit_Rdata13 = bytearray([0xCA, 0x80, 0x41, 0x04, 0x21, 0x0B, 0x09, 0x01, 0xF0])

	if which == 1 and con == 1 :
		exit_Ldata1[7] = 0x01
		exit_Ldata2[7] = 0x01
	elif which == 1 and con == 0:
		exit_Ldata1[7] = 0x00
		exit_Ldata2[7] = 0x00
	elif which == 2 and con == 1 :
		exit_Rdata1[7] = 0x01
		exit_Rdata2[7] = 0x01
	elif which == 2 and con == 0:
		exit_Rdata1[7] = 0x00
		exit_Rdata2[7] = 0x00
	
	if con == 1:
		exit_Rdata3[7] = 0x01
		exit_Rdata4[7] = 0x01
		exit_Rdata5[7] = 0x01
		exit_Rdata6[7] = 0x01
		exit_Rdata7[7] = 0x01

		exit_Rdata8[7] = 0x01
		exit_Rdata9[7] = 0x01

		exit_Rdata10[7] = 0x01
		exit_Rdata11[7] = 0x01

		exit_Rdata12[7] = 0x01
		exit_Rdata13[7] = 0x01

	else:	
		exit_Rdata3[7] = 0x00
		exit_Rdata4[7] = 0x00
		exit_Rdata5[7] = 0x00
		exit_Rdata6[7] = 0x00
		exit_Rdata7[7] = 0x00

		exit_Rdata8[7] = 0x00
		exit_Rdata9[7] = 0x00

		exit_Rdata10[7] = 0x00
		exit_Rdata11[7] = 0x00

		exit_Rdata12[7] = 0x00
		exit_Rdata13[7] = 0x00




	if which == 1:
		ser.write(exit_Rdata4)
		time.sleep(0.5)
		ser.write(exit_Rdata3)
		time.sleep(0.5)		
		ser.write(exit_Ldata1)
		time.sleep(0.5)
		ser.write(exit_Ldata2)
		time.sleep(5.5)
		
		
	elif which == 2:
		ser.write(exit_Rdata3)
		time.sleep(0.5)
		ser.write(exit_Rdata4)
		time.sleep(0.5)		
		ser.write(exit_Rdata1)
		time.sleep(0.5)
		ser.write(exit_Rdata2)
		time.sleep(5.5)
		
	ser.write(exit_Rdata8)
	ser.write(exit_Rdata9)
	time.sleep(3)

	ser.write(exit_Rdata10)
	ser.write(exit_Rdata11)
	time.sleep(3)

	ser.write(exit_Rdata12)
	ser.write(exit_Rdata13)
	time.sleep(4)

	ser.write(exit_Rdata5)
	ser.write(exit_Rdata6)
	ser.write(exit_Rdata7)


		
		 
def fireTimer():
	h1,t1 = dht.read_retry(dht.DHT22, DHT22_1)
	h2,t2 = dht.read_retry(dht.DHT22, DHT22_2)

	print 'Temp = {0:0.1f}*C Humidity= {1:0.1f}%'.format(t1,h1)
	print 'Temp2 = {0:0.1f}*C Humidity= {1:0.1f}%'.format(t2,h2)

	if ( h1 >=  fire) :	
		exitPrint(1, 1)
		#print("fire1")
	
	elif h2 < fire:
		exitPrint(1, 0)
		#print("x")

	if ( h2 >=  fire)  :
		exitPrint(2, 1)
		#print("fire2")

	elif h1 < fire:
		exitPrint(2, 0)
 		#print("x")

	timer = threading.Timer(2, fireTimer)	
	timer.start()

def faceDetect():
	if GPIO.input(rip): 
		print "Waiting ... "
		time.sleep(1)

		print "Dectecting..."
		camera.start_preview()
		sleep(1)

		now = datetime.datetime.now()
		name = now.strftime('%Y.%m.%d.%H.%M.%S') + '.jpg'
		camera.capture(name)
		camera.stop_preview()
		os.system('scp -P 12713 /home/pi/' + name + ' root@203.241.228.111:/root/yun/photo')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = name
		sock.sendto(data.encode(), ('203.241.228.111',33333) )
		serverData, serverAddr = sock.recvfrom(200)
		clientReceive = serverData.decode()

		if clientReceive == '1':
			print("ray")

		elif clientReceive == '2':
			print("xiumin")	

		elif clientReceive == '3':
			print("chen")

		elif clientReceive == '4':
			print("yun")
			toggle(0)
			localLedOnOff(led_state[0], 0.3)

		elif clientReceive == '5':
			print("dio")
		else:
			print("fail")
	
	timer = threading.Timer(5,faceDetect)
	timer.start()
	
def ble():
	while(serialFromArduino.inWaiting()  > 0 ):
			input = ord(serialFromArduino.read(1)) - ord('0')
			print(input)
			if input >= 1 and input <=7:
				toggle(input-1)
				if input == 1:
					localLedOnOff(led_state[input-1], 0.3)
				elif input == 6:
					remote_32(led_state[input-1], 0.3)
				elif input == 7:
					allLedOnoff(led_state[input-1])
			 	else:
					remoteLedOnOff(input-1, led_state[input-1], 0.3)

	timer = threading.Timer(0.1, ble)
	timer.start()

if __name__ == '__main__':
	ble()	
	fireTimer()
	#faceDetect()
	


