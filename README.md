# Ruuvitag

The **Ruuvitag** is a OpenSource Bluetooth BLE beacon with several sensors. Is equipped with an temperature sensor, humidity sensor, pressure sensor and accelerometer. Created by the ***Ruuvi*** company, tries to bring the user a BLE beacon with sensor quality and at a good price, totally OpenSource, so that users can create the codes they want. https://ruuvi.com/ruuvitag-specs/

<p align="center"> <img src="https://i.postimg.cc/HnM5hHT2/Screenshot-from-2021-03-22-14-50-07.png" width="430">

In this repository you will find explanations and step by step for the development of a system that every certain time interval (which you will set) will collect data from the internal sensors of one o more *Ruuvitag devices* in your environment, this data package will be sent to a special gateway designed by IOT2TANGLE that you will have on the local network, or even on an Raspberry Pi. This gateway will be in charge of adding these packages to Tangle Network of IOTA, through Streams.

## Available connectivity
- **[Ruuvitag-python](https://github.com/iot2tangle/Ruuvitag/tree/main/ruuvitag-python)** (*Ruuvitags* will send the sensors data through BLE to the system that is running the *Python Script* of this repository, it will be in charge of sending the data in an orderly way to the **[I2T HTTP Gateway](https://github.com/iot2tangle/Streams-http-gateway)** or **[Keepy](https://github.com/iot2tangle/Keepy)**

