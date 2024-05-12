# coding: UTF-8
import time
import unittest
import json

################################
# get the code
with open('framework_helper.py', 'r') as f1, open('../src/14102_Fritz TR-064 (14102).py', 'r') as f2:
    framework_code = f1.read()
    debug_code = f2.read()

exec (framework_code + debug_code)


################################################################################


class TestSequenceFunctions(unittest.TestCase):
    test = FritzTR_064_14102_14102(0)

    def setUp(self):
        print("Entering setUp")
        with open("credentials.txt") as f:
            self.cred = json.load(f)

        self.test = FritzTR_064_14102_14102(0)
        self.test.debug = True

        self.test.debug_input_value[self.test.PIN_I_SUID] = self.cred["PIN_I_SUID"]
        self.test.debug_input_value[self.test.PIN_I_SPW] = self.cred["PIN_I_SPW"]
        self.test.debug_input_value[self.test.PIN_I_SFBIP] = self.cred["PIN_I_SFBIP"]

        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 5
        self.test.on_init()
        print("Leaving setUp")

    def test_init(self):
        print("### Entering test_init")
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0

    def test_guest_wifi_idx(self):
        print("### Entering test_init")
        self.test.get_guest_wifi_idx()
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0

    def test_no_route(self):
        print("Entering test_no_route")
        self.test.debug_input_value[self.test.PIN_I_SFBIP] = "192.168.173.115"
        self.test.init_com()
        self.assertTrue(True)
        print("Leaving test_no_route")
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0

    def test_mac_error(self):
        print("Entering test_mac_error")
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0
        real_mac = self.cred["REAL_MAC"]
        self.test.on_input_value(self.test.PIN_I_SMAC2, real_mac)
        ret = self.test.debug_output_value[self.test.PIN_O_BMAC2AVAIL]  # type: bool
        self.assertTrue(ret)
        self.test.on_input_value(self.test.PIN_I_SMAC3, "MAC_ERROR")
        ret = self.test.debug_output_value[self.test.PIN_O_BMAC3AVAIL]
        self.assertFalse(ret)
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0
        print("Leaving test_mac_error")

    def test_dial(self):
        print("Entering test_dial")
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0
        self.test.on_input_value(self.test.PIN_I_BDIAL, "**620")
        time.sleep(2)
        self.test.on_input_value(self.test.PIN_I_BDIAL, "0")

if __name__ == '__main__':
    unittest.main()
