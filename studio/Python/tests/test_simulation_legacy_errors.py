'''
This unit test suite tests functionality of the
Tinymovr Studio using a simulated Tinymovr
device, which is suitable for unit testing.
'''
import random
import time
import can

import tinymovr
from tinymovr import Tinymovr
from tinymovr.constants import ErrorIDs
from tinymovr.iface import IFace
from tinymovr.iface.can_bus import CANBus
from tinymovr.units import get_registry

import unittest

ureg = get_registry()
A = ureg.ampere
ticks = ureg.ticks
s = ureg.second

bustype = "insilico"
channel = "test"


def get_tm() -> Tinymovr:
    can_bus: can.Bus = can.Bus(bustype=bustype, channel=channel)
    iface: IFace = CANBus(can_bus)
    return Tinymovr(node_id=1, iface=iface)

class TestSimulationLegacy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tm: Tinymovr = get_tm()

    def setUp(self):
        self.tm.reset()

    def test_get_device_info(self):
        '''
        Test getting of device info
        '''
        info = self.tm.device_info
        self.assertGreaterEqual(info.fw_major, 0)
        self.assertGreaterEqual(info.fw_minor, 7)

    def test_get_error_idle(self):
        '''
        Test successful getting of correct error codes
        in various scenarios
        '''
        self.assertFalse(self.tm.state.errors)
        
    def test_get_error_nocalib(self):
        '''
        Test successful getting of correct error codes
        in various scenarios
        '''        
        self.tm.position_control()
        self.assertIn(ErrorIDs.InvalidState, self.tm.state.errors)

    def test_get_error_calib(self):
        '''
        Test successful getting of correct error codes
        in various scenarios
        '''        
        self.tm.calibrate() # no need to wait cause it's simulation
        self.tm.position_control()
        self.assertFalse(self.tm.state.errors)


if __name__ == '__main__':
    unittest.main()