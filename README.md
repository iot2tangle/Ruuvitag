# Ruuvitag

The **Ruuvitag** is a OpenSource Bluetooth BLE beacon with several sensors. Is equipped with an temperature sensor, humidity sensor, pressure sensor and accelerometer.

This Repository contains the source code and the steps to follow to be able to obtain data from all the ***Ruuvitag*** that you have in your environment and send it, in an organized way, to the ***Tangle***, ***DLT*** of the **[IOTA Network](https://www.iota.org/)** through the **[Streams](https://www.iota.org/solutions/streams)** layer.

## Setting up your Ruuvitag Devices

It is necessary to have a computer with a Bluetooth adapter that supports BLE (Bluetooth 4.0 or 5.0), here the code will be executed that will collect all the data from the Ruuvitags and then send it to the Gateway. A Raspberry Pi can also be used for this.

It is not necessary to change the firmware of the *Ruuvitags* for a particular one. You can use the Official Firmware offered by *Ruuvi* and that comes from the factory in the device, however, you must make sure that you have updated the *Ruuvitag* with the *last official firmware*, since the code of this repository only recognizes the new data format of the Ruuvitag *"Data Format 5"* or *"RAWv2"*. If you have an old Ruuvitag, it may be in RAWv1 format, if so, when you run this code it will let you know.

## Software Configuration:

### 1) Set Ruuvitags

Set the Ruuvitags in the desired physical position. Make sure the data format of your Ruuvitag is "Data Format 5". If you are not sure what version you have, continue with the steps, the code will notify you if your device needs to be updated or not.

In case you need to update it, please refer to the following web page:
https://lab.ruuvi.com/dfu/

### 2) Install dependencies
Make sure you have Python3 and pip3 installed on your system.
```
sudo pip3 install bluepy
```

### 3) Copy the repository to the local file system of your computer.
```
cd ~
git clone --recursive https://github.com/iot2tangle/Ruuvitag.git
cd Ruuvitag
```

### 4) Edit the file *config.json*

Edit ***config.json** file, add the ***MAC addresses*** **\*** of all your *Ruuvitag devices*, the *http_address* (with the port) that will have the *I2T Streams HTTP Gateway* running, and the *interval* in seconds between the data collection. 
```
    "MAC-Ruuvitag-devices": [
        "xx:xx:xx:xx:xx:xx",
        "yy:yy:yy:yy:yy:yy",
        "zz:zz:zz:zz:zz:zz"
    ],
    "HTTP-address": "http://192.168.1.116:8080/bundle_data",
    "interval": 30
```
**\*** *To consult the MAC addresses of the devices, we recommend nRF Connect (free OpenSource software) of NordicSemiconductor available in Desktop: on Windows, macOS and Linux. and in Mobile: on Android and iOS (The mobile version is very simple and more comfortable to debug).* 

#### 5) Run (with sudo)
```
sudo python3 ruuvitag-i2t.py
```

After this, the code will be in charge of collecting all the Ruuvitags from your environment and sending the data to the *GW* and then to the *Tangle* in the established interval.

The following capture shows the system collecting data from one Ruuvitag and sending data to Tangle:

![Sending data to the Tangle](https://i.postimg.cc/MT1pf5q9/Screenshot-from-2021-03-21-23-34-22.png)
	
# Setting up the Streams HTTP Gateway

## Preparation

Install Rust if you don't have it already. More info about Rust here https://www.rust-lang.org/tools/install

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Make sure you also have the build dependencies installed, if not run:  

```
sudo apt update
sudo apt install build-essential pkg-config libssl-dev
```

## Installing the Streams Gateway
Get the Streams Gateway repository
https://github.com/iot2tangle/Streams-http-gateway

```
git clone https://github.com/iot2tangle/Streams-http-gateway
```

Navigate to the root of **Streams-http-gateway** directory and edit the **config.json** file to define yours *device names*, *endpoint*, *port*, you can also change the IOTA Full Node used, among others.

## Start the Streams Server

### Sending messages to the Tangle

Run the Streams Gateway:

```
cargo run --release  
```

This will compile and start the *Streams HTTP Gateway*. Note that the compilation process may take from 3 to 25 minutes (Pi3 took us around 15/25 mins, Pi4 8 mins and VPS or desktop machines will generally compile under the 5 mins) depending on the device you are using as host.
You will only go through the compilation process once and any restart done later will take a few seconds to have the Gateway working.

Once started, the ***Channel Id*** will be displayed, and the gateway will be open waiting for data to send to the Tangle.


