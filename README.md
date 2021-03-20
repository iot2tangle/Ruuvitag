# Ruuvitag-I2T
Python code to read several Ruuvitag device data and send it to IOTA-Tangle over Streams Gateway

## Dependencies
```
sudo pip3 install bluepy
```

## Run
```
cd ~
git clone --recursive https://github.com/iot2tangle/Ruuvitag-I2T.git
cd Ruuvitag-I2T
```

Edit config.json file, add the MAC addresses of all your devices and the GW address
```
nano config.json
```

Run (with sudo)
```
sudo python3 ruuvitag-i2t.py
```

