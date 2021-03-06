import sys, threading, time, json
#from datetime import datetime
sys.path.insert(1, './i2t-lib')
from iot2tangle import Bundle, Sender
from bluepy.btle import Scanner, DefaultDelegate
from decoderf5 import Df5Decoder


### LOAD 'config.json' FILE ###
config_json = json.load(open("config.json"))
device_names = config_json['MAC-Ruuvitag-devices']
device_names = [ x.lower() for x in device_names ] # lowercase te MACs
http_url = config_json['HTTP-address']
interval = config_json['interval']
###############################
count = 0

bundle = Bundle(device_names) # Bundle init

dec = Df5Decoder()	# Decoder init

def foo():
	global count
	count = count + 1
	print("Data Collect " + str(count))
	print (" BUNDLE: " + str(bundle.get_json()) + "\n\n\t\tSending Data to Tangle...")
	Sender(bundle.get_json()).send_HTTP(http_url)

	time.sleep(1)

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if (any(dev.addr == i for i in device_names)):
			data = dec.json_i2t(dev.rawData)
			bundle.update(dev.addr, data)	# Update device data in the Bundle Class

			scanner.clear()
			scanner.start()

### Start BLE Scanner ###
scanner = Scanner().withDelegate(ScanDelegate())
scanner.start()
#########################
print("\n						----  RUUVITAG -- IOT2TANGLE  ----")
print(" Collecting the first data...\n")

while True:
	if ( int(time.time()) % interval ):
		scanner.process(1)		# Timeout 1 second
	else:
		foo()