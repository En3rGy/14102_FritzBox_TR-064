# coding: UTF-8

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

        self.test.debug_input_value[self.test.PIN_I_SUID] = self.cred["PIN_I_SUID"]
        self.test.debug_input_value[self.test.PIN_I_SPW] = self.cred["PIN_I_SPW"]
        self.test.debug_input_value[self.test.PIN_I_SFBIP] = self.cred["PIN_I_SFBIP"]

        self.test.on_init()
        print("Leaving setUp")

    def test_discover(self):
        print("Entering test_discover")
        self.test.debug_input_value[self.test.PIN_I_SUID] = self.cred["PIN_I_SUID"]
        self.test.debug_input_value[self.test.PIN_I_SPW] = self.cred["PIN_I_SPW"]
        self.test.debug_input_value[self.test.PIN_I_SFBIP] = str()

        ret = self.test.discover_fb()
        self.assertNotEqual("", ret.netloc)
        self.assertNotEqual("", ret.path)
        print("Leaving test_discover_with_ip")

    def test_discover_with_ip(self):
        print("Entering test_discover_with_ip")
        ret = self.test.discover_fb()
        print("ret = {}".format(ret))
        self.assertNotEqual("", ret.netloc)
        self.assertNotEqual("", ret.path)
        print("Leaving test_discover_with_ip")

    def test_service_data(self):
        print("Entering test_service_data")
        ret = self.test.print_service_data()
        self.assertNotEqual("", ret)
        print("Leaving test_service_data")

    def test_soap_req(self):
        print("Entering test_soap_req")
        ain = self.cred["AIN"]
        req = '{"serviceType":"urn:dslforum-org:service:X_AVM-DE_Homeauto:1", ' \
              '"action_name":"GetSpecificDeviceInfos","argumentList":{"NewAIN":"' + ain + '"}}'

        self.test.on_input_value(self.test.PIN_I_NSOAPJSON, req)
        print("Leaving test_soap_req")

    def test_no_route(self):
        print("Entering test_no_route")
        self.test.debug_input_value[self.test.PIN_I_SFBIP] = "192.168.173.115"
        self.test.init_com()
        self.assertTrue(True)
        print("Leaving test_no_route")

    def test_mac_error(self):
        print("Entering test_mac_error")
        real_mac = self.cred["REAL_MAC"]
        self.test.on_input_value(self.test.PIN_I_SMAC2, real_mac)
        ret = self.test.debug_output_value[self.test.PIN_O_BMAC2AVAIL]  # type: bool
        self.assertTrue(ret)
        self.test.on_input_value(self.test.PIN_I_SMAC3, "MAC_ERROR")
        ret = self.test.debug_output_value[self.test.PIN_O_BMAC3AVAIL]
        self.assertFalse(ret)
        print("Leaving test_mac_error")


if __name__ == '__main__':
    unittest.main()
