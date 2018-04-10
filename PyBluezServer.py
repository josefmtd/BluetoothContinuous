#!/usr/bin/python
import bluetooth
import subprocess
import sys
import time
import signal
import os

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

count = 0
port = 1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print "Accepted connection from ",address

while 1:
	data = client_sock.recv(1024)
	if data == "!AX":
		count += 1
		proc = subprocess.Popen("sudo axcall -r 1 YD0SHY-2", stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
		time.sleep(5)
		proc.stdin.write("Tes" + str(count) + "\n")
		time.sleep(3)
		os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
		client_sock.send("OK" + str(count) + "\n")
	elif data == "!EX":
		print "Bluetooth Terminated"
		break
	else:
		print "received data = [%s]" % data

client_sock.close()
server_sock.close()

