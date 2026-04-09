"""
SPDX-FileCopyrightText: 2025 DESY and the Constellation authors
SPDX-License-Identifier: EUPL-1.2
"""

from threading import Lock

import serial

from constellation.core.configuration import Configuration
from constellation.core.monitoring import schedule_metric
from constellation.core.satellite import Satellite
from constellation.core.protocol.cscp1 import SatelliteState


class BTTB(Satellite):

    """---Provided Helper Methods---"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._serial_lock = Lock()
        self._serial_connection = serial.Serial()

    def _write_serial(self, text: str) -> None:
        """Encoding string and write to serial port (do not use directly)"""
        self.log.debug(f"Writing `{text}` to serial port")
        self._serial_connection.write(f"{text}\n".encode("ascii"))

    def _read_serial(self) -> str:
        """Read from serial port and decode string (do not use directly)"""
        text = self._serial_connection.readline().decode('ascii').strip()
        self.log.debug(f"Read `{text}` from serial port")
        return text

    def query(self, command: str) -> str:
        """Send command to serial port and return reply"""
        with self._serial_lock:
            self._write_serial(command)
            return self._read_serial()

    def query_ok(self, command: str) -> None:
        """Send command to serial port and check that reply is OK"""
        reply = self.query(command)
        if reply != "OK":
            raise Exception(f"Communication Error: command `{command}` returned `{reply}`")

    """---Implementation---"""
