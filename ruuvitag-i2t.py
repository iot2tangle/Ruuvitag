from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate
import threading, time
from decoderf5 import Df5Decoder

def foo():
    print("Interrupcion")
    time.sleep(1)

def timestamp():
	return int(datetime.now().time().strftime("%Y%m%d%H%M%S"))

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if (dev.addr == "c5:95:16:e1:1e:ba"):
		
			dec = Df5Decoder()
			data = dec.json_i2t(dev.rawData)

			print(datetime.now().time(), data, dev.addr)
			scanner.clear()
			scanner.start()


scanner = Scanner().withDelegate(ScanDelegate())
scanner.start()


while True:
	if (timestamp()%20):
		scanner.process(1)		# Timeout 1 second
	else:
		foo()