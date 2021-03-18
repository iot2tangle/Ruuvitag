import math

def twos_complement(value, bits):
    if (value & (1 << (bits - 1))) != 0:
        value = value - (1 << bits)
    return value

def rshift(val, n):
    """
    Arithmetic right shift, preserves sign bit.
    https://stackoverflow.com/a/5833119 .
    """
    return (val % 0x100000000) >> n


class Df5Decoder(object):
    """
    Decodes data from RuuviTag with Data Format 5
    Protocol specification:
    https://github.com/ruuvi/ruuvi-sensor-protocols
    """

    def _get_temperature(self, data):
        """Return temperature in celsius"""
        if data[8:9] == 0x7FFF:
            return None

        temperature = twos_complement((data[8] << 8) + data[9], 16) / 200
        return round(temperature, 2)

    def _get_humidity(self, data):
        """Return humidity %"""
        if data[10:11] == 0xFFFF:
            return None

        humidity = ((data[10] & 0xFF) << 8 | data[11] & 0xFF) / 400
        return round(humidity, 2)

    def _get_pressure(self, data):
        """Return air pressure hPa"""
        if data[12:13] == 0xFFFF:
            return None

        pressure = ((data[12] & 0xFF) << 8 | data[13] & 0xFF) + 50000
        return round((pressure / 100), 2)

    def _get_acceleration(self, data):
        """Return acceleration mG"""
        if (data[14:15] == 0x7FFF or
                data[16:17] == 0x7FFF or
                data[18:19] == 0x7FFF):
            return (None, None, None)

        acc_x = twos_complement((data[14] << 8) + data[15], 16)
        acc_y = twos_complement((data[16] << 8) + data[17], 16)
        acc_z = twos_complement((data[18] << 8) + data[19], 16)
        return (acc_x, acc_y, acc_z)

    def _get_powerinfo(self, data):
        """Return battery voltage and tx power"""
        power_info = (data[20] & 0xFF) << 8 | (data[21] & 0xFF)
        battery_voltage = rshift(power_info, 5) + 1600
        tx_power = (power_info & 0b11111) * 2 - 40

        if rshift(power_info, 5) == 0b11111111111:
            battery_voltage = None
        if (power_info & 0b11111) == 0b11111:
            tx_power = None

        return (round(battery_voltage, 3), tx_power)

    def _get_battery(self, data):
        """Return battery mV"""
        battery_voltage = self._get_powerinfo(data)[0]
        return battery_voltage

    def _get_txpower(self, data):
        """Return transmit power"""
        tx_power = self._get_powerinfo(data)[1]
        return tx_power

    def _get_movementcounter(self, data):
        return data[22] & 0xFF

    def _get_measurementsequencenumber(self, data):
        measurementSequenceNumber = (data[23] & 0xFF) << 8 | data[24] & 0xFF
        return measurementSequenceNumber

    def _get_mac(self, data):
        return ''.join('{:02x}'.format(x) for x in data[25:31])

    def decode_data(self, data):
        """
        Decode sensor data.

        Returns:
            dict: Sensor values
        """
        try:
            byte_data = [ x for x in data ] # integer list 
            acc_x, acc_y, acc_z = self._get_acceleration(byte_data)
            return {
                'data_format': 5,
                'humidity': self._get_humidity(byte_data),
                'temperature': self._get_temperature(byte_data),
                'pressure': self._get_pressure(byte_data),
                'acceleration_x': acc_x,
                'acceleration_y': acc_y,
                'acceleration_z': acc_z,
                'tx_power': self._get_txpower(byte_data),
                'battery': self._get_battery(byte_data),
                'movement_counter': self._get_movementcounter(byte_data),
                'measurement_sequence_number': self._get_measurementsequencenumber(byte_data),
                'mac': self._get_mac(byte_data)
            }
        except Exception:
            print('Error - Ruuvi Data Value: is not valid')
            return None
