import sys, threading, time, json
from datetime import datetime
sys.path.insert(1, './i2t-lib')
from iot2tangle import Bundle, Sender
from bluepy.btle import Scanner, DefaultDelegate
from decoderf5 import Df5Decoder


### LOAD 'config.json' FILE ###
config_json = json.load(open("config.json"))
device_names = config_json['MAC-Ruuvitag-devices']
http_url = config_json['HTTP-address']
interval = config_json['interval']
###############################

bundle = Bundle(device_names)

dec = Df5Decoder()	# Decoder Init

def foo():
    print(bundle.get_json())
    time.sleep(1)

def timestamp():
	return int(datetime.now().time().strftime("%Y%m%d%H%M%S"))

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

while True:
	if (timestamp()%20):
		scanner.process(1)		# Timeout 1 second
	else:
		foo()