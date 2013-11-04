#Need to install the PySerial library first

import sys, getopt
import serial
import time

def open(aport='/dev/ttyUSB0', abaudrate=115200) :
	return serial.Serial(
		port=aport,
		baudrate=abaudrate,     # baudrate
		bytesize=8,             # number of databits
		parity=serial.PARITY_NONE,
		stopbits=1,
		xonxoff=0,              # enable software flow control
		rtscts=0,               # disable RTS/CTS flow control
		timeout=None               # set a timeout value, None for waiting forever
	)

def printLog(sp):
	temp = sp.read()
	while ord(temp) != 0x04:
		write(temp)
		temp = sp.read()

if __name__ == "__main__":

	# Import Psyco if available
	try:
		import psyco
		psyco.full()
		print "Using Psyco..."
	except ImportError:
		pass

	conf = {
		'port': '/dev/ttyUSB0',
		'baud': 115200,
	}

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hqVewvrp:b:a:l:")
	except getopt.GetoptError, err:
		print str(err)
		sys.exit(2)

	for o, a in opts:
		if o == '-p':
			conf['port'] = a
		elif o == '-b':
			conf['baud'] = eval(a)
		else:
			assert False, "unhandled option"

	sp = open(conf['port'], conf['baud'])

#	print args[0]
#	print conf['port']
#	print conf['baud']

	write=sys.stdout.write

	isLoaded = False

	while True:
		print ''
		cmd = raw_input('>> ').split(' ');
		sp.flushInput()

		if cmd[0] == 'go':
			if not isLoaded:
				confirm = raw_input("No file has been loaded, are you sure to go? [Y/N]")
				if confirm == '' or confirm[0] == 'N' or confirm[0] == 'n':
					continue

			success = False
			while success == False:
				sp.write(chr(0x01))
				sp.write(chr(0x01))
				sp.flush()

				temp=sp.read()

				if ord(temp)==0x06:
					success = True
				else:
					print ord(temp)

					printLog(sp)

		elif cmd[0] == 'peek':
			if len(cmd) < 2:
				print "Incorrect command, should be 'peek addr'"
				continue

			addr = int(cmd[1], 16) & 0xffffffff

			success = False
			while success == False:
				sp.write(chr(0x01))
				sp.write(chr(0x02))

				for i in range(0,4):
					sp.write(chr(addr >> 24 & 0xff))
					addr = addr << 8

				sp.flush()

				temp=sp.read()

				if ord(temp)==0x06:
					success = True
				else:
					print ord(temp)

					printLog(sp)

		elif cmd[0] == 'poke':
			if len(cmd) < 3:
				print "Incorrect command, should be 'poke addr data'"
				continue

			addr = int(cmd[1], 16) & 0xffffffff
			data = int(cmd[2], 16) & 0xffffffff

			success = False
			while success == False:
				sp.write(chr(0x01))
				sp.write(chr(0x03))

				for i in range(0,4):
					sp.write(chr(addr >> 24 & 0xff))
					addr = addr << 8
				for i in range(0,4):
					sp.write(chr(data >> 24 & 0xff))
					data = data << 8

				sp.flush()

				temp=sp.read()

				if ord(temp)==0x06:
					success = True
				else:
					print ord(temp)

					printLog(sp)

		elif cmd[0] == 'load' or cmd[0] == 'verify':
			if len(cmd) < 2:
				print "Please input the filename"
				continue

			try:
				data = map(lambda c: ord(c), file(cmd[1],"rb").read())
			except:
				print "File not exist"
				continue

			temp = sp.read()
			buf = ""

			# while ord(temp)!=0x15:
			# 	buf += temp
			# 	temp = sp.read()

			# print buf
			dataLength = len(data)
			blockNum = (dataLength-1)/128+1
			print "The size of the image is ",dataLength,"!"
			print "Total block number is ",blockNum,"!"
			print "Download start,",blockNum,"block(s) in total!"

			for i in range(1,blockNum+1):
				success = False
				while success == False:
					sp.write(chr(0x01))
					if cmd[0] == 'load':
						sp.write(chr(0x00))
					else:
						sp.write(chr(0x04))
					sp.write(chr(i&0xFF))
					sp.write(chr(0xFF-i&0xFF))
					crc = 0x01+0xFF

					for j in range(0,128):
						if len(data)>(i-1)*128+j:
							sp.write(chr(data[(i-1)*128+j]))
							crc += data[(i-1)*128+j]
						else:
							sp.write(chr(0xff))
							crc += 0xff

					crc &= 0xff
					sp.write(chr(crc))
					sp.flush()

					# !important!
					# time.sleep(0.1)

					temp=sp.read()
					sp.flushInput()

					if ord(temp)==0x06:
						success = True
						print "Block",i,"has finished!"
					else:
						print ord(temp)
						print "Error,send again!"

						printLog(sp)

			sp.write(chr(0x04))
			sp.flush()
			temp=sp.read()

			if ord(temp)==0x06:
				if (cmd[0] == 'load'):
					isLoaded = True
				print "Download has finished!\n"
		elif cmd[0] == 'q' or cmd[0] == 'quit' or cmd[0] == 'exit':
			sys.exit(0)
		else:
			print "Invalid command!"


		printLog(sp)


	# while True:
	# 	write(sp.read())

	sp.close()