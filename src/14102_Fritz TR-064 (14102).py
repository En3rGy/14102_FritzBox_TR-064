# coding: UTF-8
import re
import urllib2
import ssl
import urlparse
import socket
import struct
import hashlib
import threading
import json
import time
import fritz_lib.fritz as fritz

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class FritzTR_064_14102_14102(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "FritzBox")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_SUID=1
        self.PIN_I_SPW=2
        self.PIN_I_SFBIP=3
        self.PIN_I_BWIFI1ON=4
        self.PIN_I_BWIFI2ON=5
        self.PIN_I_BWIFI3ON=6
        self.PIN_I_BWIFIGUESTON=7
        self.PIN_I_SMAC1=8
        self.PIN_I_SMAC2=9
        self.PIN_I_SMAC3=10
        self.PIN_I_SMAC_CSV=11
        self.PIN_I_STELNO=12
        self.PIN_I_BDIAL=13
        self.PIN_I_BABEA=14
        self.PIN_I_BREBOOT=15
        self.PIN_I_NSOAPJSON=16
        self.PIN_I_NUPDATERATE=17
        self.PIN_O_SWIFI1SSID=1
        self.PIN_O_BRMWLAN1ONOFF=2
        self.PIN_O_SWIFI2SSID=3
        self.PIN_O_BRMWLAN2ONOFF=4
        self.PIN_O_SWIFI3SSID=5
        self.PIN_O_BRMWLAN3ONOFF=6
        self.PIN_O_SWIFIGUESTSSID=7
        self.PIN_O_BRMWLANGUESTONOFF=8
        self.PIN_O_BMAC1AVAIL=9
        self.PIN_O_BMAC2AVAIL=10
        self.PIN_O_BMAC3AVAIL=11
        self.PIN_O_BMAC_CSV_AVAIL=12
        self.PIN_O_BGUESTAVAIL=13
        self.PIN_O_BABEA=14
        self.PIN_O_SSOAPRPLY=15
        self.PIN_O_INSTANCE_ID=16

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.sbc_data_lock = threading.Lock()
        self.g_out_sbc = {}  # type: {int, object}
        self.guest_wifi_idx = 0  # type: int
        self.time_out = 3  # type: int
        self.debug = False

    def set_output_value_sbc(self, pin, val):
        # type:  (int, any) -> None
        self.sbc_data_lock.acquire()
        if pin in self.g_out_sbc:
            if self.g_out_sbc[pin] == val:
                print (str(time.time()) + " # SBC: pin " + str(pin) + " <- data not send / " + str(val).decode("utf-8"))
                self.sbc_data_lock.release()
                return

        self._set_output_value(pin, val)
        self.g_out_sbc[pin] = val
        self.sbc_data_lock.release()

    def log_msg(self, text):
        self.DEBUG.add_message("14102: {}".format(text))

    def log_data(self, key, value):
        self.DEBUG.set_value("14102: {}".format(key), str(value))

    def ensure_fritz_box_init(self):
        """
        Takes care, that global variable exists and initialises the connection to FritzBox.
        :return: -
        :exception: Exception()
        """
        if "fritz_box" not in globals():
            global fritz_box
            fritz_box = fritz.FritzBox()
            try:
                fritz_box.user = str(self._get_input_value(self.PIN_I_SUID))
                fritz_box.password = str(self._get_input_value(self.PIN_I_SPW))
                fritz_box.discover(self.FRAMEWORK.get_homeserver_private_ip())
                self.log_data("ensure_fritz_box_init | FritzBox", "{}://{}:{}".format(fritz_box.protocol,
                                                                                     fritz_box.ip,
                                                                                     fritz_box.port))
            except Exception as e:
                raise Exception("Exception in ensure_fritz_box_init: {}".format(e))

    def do_regex(self, match_str, text):
        match = re.findall(match_str, text, flags=re.S)

        if len(match) == 0:
            return ""

        return match[0]

    def get_guest_wifi_idx(self):
        if self.debug: print("DEBUG | Entering get_guest_wifi_idx()")
        self.ensure_fritz_box_init()
        global fritz_box

        wlan_if = []
        for service_name in fritz_box.services.keys():
            match = re.search(r"urn:dslforum-org:service:WLANConfiguration:([0-9])", service_name)
            if match is None:
                continue

            wlan_if.append(match.group(1))

        self.guest_wifi_idx = len(wlan_if)
        self.log_data("Guest WIFI Index", self.guest_wifi_idx)

    def update_status(self):
        interval = self._get_input_value(self.PIN_I_NUPDATERATE)
        if interval > 0:
            self.ensure_fritz_box_init()
            global fritz_box

            # work with wifi
            try:
                for nWifiIdx in range(1, (self.guest_wifi_idx + 1)):
                    service_name = "urn:dslforum-org:service:WLANConfiguration:" + str(nWifiIdx)
                    action = "GetInfo"
                    attr_list = {}
                    data = fritz_box.set_soap_action(service_name, action, attr_list)

                    # nOn = int(((data["NewStatus"] == "Up") and (data["NewEnable"] == '1')))
                    on = int(data["NewEnable"] == '1')
                    self.log_data("WIFI " + str(nWifiIdx), data["NewStatus"])

                    if nWifiIdx == 1:
                        self.set_output_value_sbc(self.PIN_O_BRMWLAN1ONOFF, on)
                        self.set_output_value_sbc(self.PIN_O_SWIFI1SSID, data["NewSSID"])

                    elif nWifiIdx == 2:
                        self.set_output_value_sbc(self.PIN_O_BRMWLAN2ONOFF, on)
                        self.set_output_value_sbc(self.PIN_O_SWIFI2SSID, data["NewSSID"])

                    elif nWifiIdx == 3:
                        self.set_output_value_sbc(self.PIN_O_BRMWLAN3ONOFF, on)
                        self.set_output_value_sbc(self.PIN_O_SWIFI3SSID, data["NewSSID"])

                    if nWifiIdx == self.guest_wifi_idx:
                        self.set_output_value_sbc(self.PIN_O_BRMWLANGUESTONOFF, on)
                        self.set_output_value_sbc(self.PIN_O_SWIFIGUESTSSID, data["NewSSID"])
            except Exception:
                self.log_msg("Unknown Error in wifi part of update_status")
            # End Wi-Fi

            # MAC attendance
            for i in range(self.PIN_I_SMAC1, (self.PIN_I_SMAC3 + 1)):
                try:
                    value = self._get_input_value(i)

                    if value == str() or value == 0:
                        continue

                    service_name = "urn:dslforum-org:service:Hosts:1"
                    action = "GetSpecificHostEntry"
                    attr_list = {"NewMACAddress": value}
                    data = fritz_box.set_soap_action(service_name, action, attr_list)

                    ret = 0
                    if data:
                        ret = int(data["NewActive"])

                    if i == self.PIN_I_SMAC1:
                        self.set_output_value_sbc(self.PIN_O_BMAC1AVAIL, ret)
                    elif i == self.PIN_I_SMAC2:
                        self.set_output_value_sbc(self.PIN_O_BMAC2AVAIL, ret)
                    elif i == self.PIN_I_SMAC3:
                        self.set_output_value_sbc(self.PIN_O_BMAC3AVAIL, ret)
                except Exception as e:
                    self.log_msg("In update_status (MAC attendance) | " + str(e))

            # generic mac address list
            mac_list = str(self._get_input_value(self.PIN_I_SMAC_CSV)).split(",")
            # if self.debug: print("### mac_list= {}".format(mac_list))
            result = str()
            for mac_addr in mac_list:
                match = re.match(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac_addr)
                if match is None:
                    self.log_msg("In update_status (Generic MAC address list), "
                                 "received an invalid MAC address: {}. Ignoring it.".format(mac_addr))
                    continue
                try:
                    service_name = "urn:dslforum-org:service:Hosts:1"
                    action = "GetSpecificHostEntry"
                    attr_list = {"NewMACAddress": mac_addr}
                    data = fritz_box.set_soap_action(service_name, action, attr_list)

                    if data:
                        ret = int(data["NewActive"])
                        result = result + str(ret) + ","
                except Exception as e:
                    self.log_msg("In update_status (Generic MAC address list), " + str(e))

            result = result[:-1]
            if result != str():
                self.set_output_value_sbc(self.PIN_O_BMAC_CSV_AVAIL, result)
            # end mac discovery

            # MAC in Guest WIFI
            try:
                service_name = "urn:dslforum-org:service:WLANConfiguration:1"
                action = "X_AVM-DE_GetWLANDeviceListPath"
                attr_list = {}
                data = fritz_box.set_soap_action(service_name, action, attr_list)
                path = data["NewX_AVM-DE_WLANDeviceListPath"]
                path = self.url_parsed.geturl() + path
                contents = self.get_data(path)
                ret = "<AssociatedDeviceGuest>1</AssociatedDeviceGuest>" in contents
                self.set_output_value_sbc(self.PIN_O_BGUESTAVAIL, ret)
            except Exception:
                pass
            # end MAC in Guest WIFI

            # AB
            try:
                service_name = "urn:dslforum-org:service:X_AVM-DE_TAM:1"
                action = "GetInfo"
                attr_list = {"NewIndex": "0"}
                data = fritz_box.set_soap_action(service_name, action, attr_list)
                if data:
                    on = int(data["NewEnable"] == '1')
                    self.set_output_value_sbc(self.PIN_O_BABEA, on)
            except Exception:
                pass
            # end AB

            t = threading.Timer(interval, self.update_status).start()
        else:
            print("Interval = 0 in update_status. Did nothing.")

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()
        self.ensure_fritz_box_init()
        global fritz_box

        module_id = self._get_module_id() # type: str
        self.set_output_value_sbc(self.PIN_O_INSTANCE_ID, module_id)
        self.update_status()

    def on_input_value(self, index, value):
        ############################################
        self.uId = self._get_input_value(self.PIN_I_SUID)
        self.pw = self._get_input_value(self.PIN_I_SPW)
        wifi_idx = 0
        interval = self._get_input_value(self.PIN_I_NUPDATERATE)
        ############################################

        # self.DEBUG.add_message("Set switch: " + str(self._get_input_value(self.PIN_I_BONOFF)))
        # self._set_output_value(self.PIN_O_BRMONOFF, grOn["data"])
        # self.DEBUG.set_value("Switch cmd", sUrl)

        if index == self.PIN_I_SUID or index == self.PIN_I_SPW:
            print("In on_input_value, no UID or PW")
            return

        if index == self.PIN_I_NUPDATERATE:
            if interval > 0:
                self.update_status()

        # work with wifi
        elif index == self.PIN_I_BWIFI1ON or index == self.PIN_I_BWIFI2ON or index == self.PIN_I_BWIFI3ON or \
                index == self.PIN_I_BWIFIGUESTON:

            wifi_on = int(value)
            if index == self.PIN_I_BWIFI1ON:
                wifi_idx = 1

            elif index == self.PIN_I_BWIFI2ON:
                wifi_idx = 2

            elif index == self.PIN_I_BWIFI3ON:
                wifi_idx = 3

            elif index == self.PIN_I_BWIFIGUESTON:
                wifi_idx = self.guest_wifi_idx

            # switch on wifi
            service_name = "urn:dslforum-org:service:WLANConfiguration:" + str(wifi_idx)
            action = "SetEnable"
            attr_list = {"NewEnable": str(wifi_on)}
            self.log_msg("WIFI SOLL: idx " + str(wifi_idx) + ", status " + str(wifi_on))
            fritz_box.set_soap_action(service_name, action, attr_list)

            # get wifi status
            action = "GetInfo"
            attr_list = {}
            data = fritz_box.set_soap_action(service_name, action, attr_list)
            self.log_data("SOAP Repl.", str(data))

            status = int(data["NewEnable"] == '1')

            if wifi_idx == self.guest_wifi_idx:
                self.set_output_value_sbc(self.PIN_O_BRMWLANGUESTONOFF, status)
                self.set_output_value_sbc(self.PIN_O_SWIFIGUESTSSID, data["NewSSID"])
                self.log_msg("RM Guest Wifi")

            if wifi_idx == 1:
                self.set_output_value_sbc(self.PIN_O_BRMWLAN1ONOFF, status)
                self.set_output_value_sbc(self.PIN_O_SWIFI1SSID, data["NewSSID"])
                self.log_msg("RM Wifi 1")

            elif wifi_idx == 2:
                self.set_output_value_sbc(self.PIN_O_BRMWLAN2ONOFF, status)
                self.set_output_value_sbc(self.PIN_O_SWIFI2SSID, data["NewSSID"])
                self.log_msg("RM Wifi 2")

            elif wifi_idx == 3:
                self.set_output_value_sbc(self.PIN_O_BRMWLAN3ONOFF, status)
                self.set_output_value_sbc(self.PIN_O_SWIFI3SSID, data["NewSSID"])
                self.log_msg("RM Wifi 3")

        # End Wifi

        elif index == self.PIN_I_SMAC1 or index == self.PIN_I_SMAC2 or index == self.PIN_I_SMAC3:
            service_name = "urn:dslforum-org:service:Hosts:1"
            action = "GetSpecificHostEntry"
            attr_list = {"NewMACAddress": value}
            data = fritz_box.set_soap_action(service_name, action, attr_list)

            ret = 0
            if data:
                ret = int(data["NewActive"])

            if index == self.PIN_I_SMAC1:
                self.set_output_value_sbc(self.PIN_O_BMAC1AVAIL, ret)
            elif index == self.PIN_I_SMAC2:
                self.set_output_value_sbc(self.PIN_O_BMAC2AVAIL, ret)
            elif index == self.PIN_I_SMAC3:
                self.set_output_value_sbc(self.PIN_O_BMAC3AVAIL, ret)

        elif index == self.PIN_I_SMAC_CSV:
            service_name = "urn:dslforum-org:service:Hosts:1"
            action = "GetSpecificHostEntry"

            mac_list = str(value).split(",")
            result = str()
            for mac_addr in mac_list:
                attr_list = {"NewMACAddress": mac_addr}
                data = fritz_box.set_soap_action(service_name, action, attr_list)

                if data:
                    ret = int(data["NewActive"])
                    result = result + str(ret) + ","

            result = result[:-1]
            self.set_output_value_sbc(self.PIN_O_BMAC_CSV_AVAIL, result)

        # end mac discovery

        elif index == self.PIN_I_BDIAL:
            service_name = "urn:dslforum-org:service:X_VoIP:1"
            if self.debug: print("DEBUG | on_input_value(pin=self.PIN_I_BDIAL, value={})".format(value))

            if value == 0 or value == "0":
                action = "X_AVM-DE_DialHangup"
                attr_list = {}
                fritz_box.set_soap_action(service_name, action, attr_list)
            else:
                action = "X_AVM-DE_DialNumber"
                attr_list = {"NewX_AVM-DE_PhoneNumber": "{}".format(self._get_input_value(self.PIN_I_STELNO))}
                fritz_box.set_soap_action(service_name, action, attr_list)
        # end dial / call

        # generic soap request
        elif index == self.PIN_I_NSOAPJSON:
            # e.g.: '{"serviceType":"urn:dslforum-org:service:WLANConfiguration:1",
            # "action_name":"SetEnable","argumentList":{"NewEnable":"1"}}'
            value = str(value)

            if value:
                value = value.replace("&quot;", '"')
                res = json.loads(value)
                service_name = res["serviceType"]
                action = res["action_name"]
                attr_list = res["argumentList"]

                data = str(fritz_box.set_soap_action(service_name, action, attr_list))
                data = data.replace("'", '"')  # exchange ' by "

                self.set_output_value_sbc(self.PIN_O_SSOAPRPLY, str(data))

        # Trigger Reboot
        elif index == self.PIN_I_BREBOOT:
            if value == 1:
                service_name = "urn:dslforum-org:service:DeviceConfig:1"
                action = "Reboot"
                attr_list = {}
                fritz_box.set_soap_action(service_name, action, attr_list)

        # AB ein/aus
        elif index == self.PIN_I_BABEA:
            service_name = "urn:dslforum-org:service:X_AVM-DE_TAM:1"
            action = "SetEnable"

            if value == 0:
                attr_list = {"NewIndex": "0", "NewEnable": "0"}
                fritz_box.set_soap_action(service_name, action, attr_list)

            else:
                attr_list = {"NewIndex": "0", "NewEnable": "1"}
                fritz_box.set_soap_action(service_name, action, attr_list)

            action = "GetInfo"
            attr_list = {"NewIndex": "0"}
            data = fritz_box.set_soap_action(service_name, action, attr_list)
            is_on = (data["NewEnable"] == '1')  # type: bool
            self.set_output_value_sbc(self.PIN_O_BABEA, is_on)

global fritz_box  # type: fritz.FritzBox()