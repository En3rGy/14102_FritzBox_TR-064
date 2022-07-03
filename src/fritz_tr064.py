# coding: UTF-8

import unittest

# functional import

import re
import urllib2
import ssl
import urlparse
import socket
import struct
import hashlib
import threading

import json


#########################################################

class hsl20_4:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_output_value = {}  # type: {}
        debug_set_remanent = {}  # type: {}
        debug_input_value = {}

        def __init__(self, a, b):
            pass

        def _get_framework(self):
            f = hsl20_4.Framework()
            return f

        def _get_logger(self, a, b):
            return 0

        def _get_remanent(self, key):
            return 0

        def _set_remanent(self, key, val):
            self.debug_set_remanent = val

        def _set_output_value(self, pin, value):
            self.debug_output_value[int(pin)] = value  # type: []
            print "# Out: " + str(value) + " @ pin " + str(pin)

        def _get_input_value(self, pin):
            if pin in self.debug_input_value:
                return self.debug_input_value[pin]
            else:
                return 0

        def _get_module_id(self):
            return 123

    class Framework:
        def __init__(self):
            pass

        def _run_in_context_thread(self, a):
            pass

        def create_debug_section(self):
            d = hsl20_4.DebugHelper()
            return d

        def get_homeserver_private_ip(self):
            return "127.0.0.1"

        def get_instance_by_id(self, id):
            return ""

    class DebugHelper:
        def __init__(self):
            pass

        def set_value(self, cap, text):
            print("DEBUG value\t'" + str(cap) + "': " + str(text))

        def add_message(self, msg):
            print("Debug Msg\t" + str(msg))

        def add_exception(self, msg):
            print("EXCEPTION Msg\t" + str(msg))


#########################################################

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class FritzTR_064_14102_14102(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_3_FritzBox")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE, ())
        self.PIN_I_SUID = 1
        self.PIN_I_SPW = 2
        self.PIN_I_SFBIP = 3
        self.PIN_I_BWIFI1ON = 4
        self.PIN_I_BWIFI2ON = 5
        self.PIN_I_BWIFI3ON = 6
        self.PIN_I_BWIFIGUESTON = 7
        self.PIN_I_SMAC1 = 8
        self.PIN_I_SMAC2 = 9
        self.PIN_I_SMAC3 = 10
        self.PIN_I_SMAC_CSV = 11
        self.PIN_I_STELNO = 12
        self.PIN_I_BDIAL = 13
        self.PIN_I_BABEA = 14
        self.PIN_I_BREBOOT = 15
        self.PIN_I_NSOAPJSON = 16
        self.PIN_I_NUPDATERATE = 17
        self.PIN_O_SWIFI1SSID = 1
        self.PIN_O_BRMWLAN1ONOFF = 2
        self.PIN_O_SWIFI2SSID = 3
        self.PIN_O_BRMWLAN2ONOFF = 4
        self.PIN_O_SWIFI3SSID = 5
        self.PIN_O_BRMWLAN3ONOFF = 6
        self.PIN_O_SWIFIGUESTSSID = 7
        self.PIN_O_BRMWLANGUESTONOFF = 8
        self.PIN_O_BMAC1AVAIL = 9
        self.PIN_O_BMAC2AVAIL = 10
        self.PIN_O_BMAC3AVAIL = 11
        self.PIN_O_BMAC_CSV_AVAIL = 12
        self.PIN_O_BGUESTAVAIL = 13
        self.PIN_O_BABEA = 14
        self.PIN_O_SSOAPRPLY = 15
        self.PIN_O_INSTANCE_ID = 16

    ########################################################################################################
    #### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
    ###################################################################################################!!!##

    sbc_data_lock = threading.Lock()

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
        self.DEBUG.add_message("14102 (" + str(self.fb_ip) + "): " + str(text))

    def log_data(self, key, value):
        self.DEBUG.set_value("14102 (" + str(self.fb_ip) + ") " + str(key), str(value))

    def get_service_data(self, data, service_type):
        try:
            service_id = \
                re.findall('<serviceType>' + service_type + '<\\/serviceType>.*?<serviceId>(.*?)<\\/serviceId>', data,
                           flags=re.S)[0]
            control_url = \
                re.findall('<serviceType>' + service_type + '<\\/serviceType>.*?<controlURL>(.*?)<\\/controlURL>', data,
                           flags=re.S)[0]
            event_sub_url = \
                re.findall('<serviceType>' + service_type + '<\\/serviceType>.*?<eventSubURL>(.*?)<\\/eventSubURL>',
                           data, flags=re.S)[0]
            scpdurl = \
                re.findall('<serviceType>' + service_type + '<\\/serviceType>.*?<SCPDURL>(.*?)<\\/SCPDURL>', data,
                           flags=re.S)[0]

            return {"serviceType": service_type,
                    "serviceId": service_id,
                    "controlURL": control_url,
                    "eventSubURL": event_sub_url,
                    "SCPDURL": scpdurl}
        except Exception as e:
            self.log_data("Error", "get_service_data: " + str(e))
            return {}

    def do_regex(self, match_str, text):
        match = re.findall(match_str, text, flags=re.S)

        if len(match) == 0:
            return ""

        return match[0]

    def interface_addresses(self, family=socket.AF_INET):
        for fam, _, _, _, sockaddr in socket.getaddrinfo('', None, 0, 0, 0, socket.AI_NUMERICHOST):
            if family == fam:
                yield sockaddr[0]

    def discover_fb(self):
        fb_ip = self._get_input_value(self.PIN_I_SFBIP)
        if fb_ip:
            url_unparsed = "http://" + str(fb_ip) + ":49000/tr64desc.xml"
            url_parsed = urlparse.urlparse(url_unparsed)

            if url_parsed.netloc:
                return url_parsed

        # SSDP request msg from application
        MCAST_MSG = ('M-SEARCH * HTTP/1.1\r\n' +
                     'HOST: 239.255.255.250:1900\r\n' +
                     'MAN: "ssdp:discover"\r\n' +
                     'MX: 5\r\n' +
                     'ST: urn:dslforum-org:device:InternetGatewayDevice:1\r\n')

        MCAST_GRP = '239.255.255.250'
        MCAST_PORT = 1900

        # hsl20_3.Framework.get_homeserver_private_ip
        hs_ip = self.FRAMEWORK.get_homeserver_private_ip()

        # for address in self.interface_addresses():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # time to life fro multicast msg
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        # specify interface to use for multicast msg
        sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(hs_ip))

        sock.settimeout(1)

        try:
            sock.sendto(MCAST_MSG, (MCAST_GRP, MCAST_PORT))
        except socket.error as e:
            self.log_data("Error", "discover: " + str(e))
            sock.close()

        while True:
            try:
                data = sock.recv(1024)

                url_unparsed = self.do_regex('LOCATION: (.*)(?:\\n\\r|\\r\\n)SERVER:.*FRITZ!Box', data)
                url_parsed = urlparse.urlparse(url_unparsed)

                # (scheme='http', netloc='192.168.178.1:49000', path='/tr64desc.xml', params='', query='', fragment='')
                if url_parsed.netloc:
                    sock.close()
                    return url_parsed

            except socket.timeout:
                break

        sock.close()

    def get_security_port(self, p_url_parsed):

        url = p_url_parsed.geturl() + "/upnp/control/deviceinfo"
        url_parsed = urlparse.urlparse(url)

        # Build a SSL Context to disable certificate verification.
        ctx = ssl._create_unverified_context()
        response_data = ""

        headers = {'Host': url_parsed.hostname,
                   'CONTENT-TYPE': 'text/xml; charset="utf-8',
                   'SOAPACTION': "urn:dslforum-org:service:DeviceInfo:1#GetSecurityPort"}

        data = ('<?xml version="1.0"?>' +
                '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" ' +
                's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">' +
                '<s:Body><u:GetSecurityPort xmlns:u="urn:dslforum-' +
                'org:service:DeviceInfo:1"></u:GetSecurityPort>' +
                '</s:Body></s:Envelope>')

        try:
            # Build a http request and overwrite host header with the original hostname.
            request = urllib2.Request(url, data=data, headers=headers)

            # Open the URL and read the response.
            response = urllib2.urlopen(request, timeout=self.time_out, context=ctx)
            response_data = response.read()
        except Exception as e:
            self.log_data("Error", "getSecurityPort: " + str(e))

        return self.do_regex('<NewSecurityPort>(.*?)<\\/NewSecurityPort>', response_data)

    def get_data(self, url):
        url_parsed = urlparse.urlparse(url)

        # Build a SSL Context to disable certificate verification.
        ctx = ssl._create_unverified_context()
        response_data = ""

        try:
            # Build a http request and overwrite host header with the original hostname.
            request = urllib2.Request(url, headers={'Host': url_parsed.hostname})
            # Open the URL and read the response.
            response = urllib2.urlopen(request, timeout=self.time_out, context=ctx)
            response_data = response.read()
        except Exception as e:
            self.log_data("Error", "getData: " + str(e))
        return response_data

    def print_service_data(self):
        self.init_com()
        print(self.service_descr)
        return self.service_descr

    def init_com(self):
        # uid = self._get_input_value(self.PIN_I_SUID)
        # pw = self._get_input_value(self.PIN_I_SPW)

        self.url_parsed = self.discover_fb()
        self.fb_ip = self.url_parsed.geturl()

        if not self.url_parsed:
            self.log_msg("Could not discover Fritz!Box in init_com")
            return False

        self.service_descr = self.get_data(self.url_parsed.geturl())
        if not self.service_descr:
            self.log_msg("Could not retrieve service description in init_com")
            return False
        self.get_guest_wifi_idx()

        self.url_parsed = urlparse.urlparse(self.url_parsed.scheme + "://" + self.url_parsed.netloc)
        self.fb_ip = self.url_parsed.geturl()
        self.log_data("Fritz!Box URL", self.url_parsed.geturl())

        # work with device info
        service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:DeviceInfo:1")

        # get security port
        data = self.set_soap_action(self.url_parsed, service_data, "GetSecurityPort", {})

        if 'NewSecurityPort' not in data:
            self.log_msg("Could retrieve security port from Fritz!Box")
        else:
            sec_port = data['NewSecurityPort']
            url = 'https://' + self.url_parsed.hostname + ":" + sec_port
            self.url_parsed = urlparse.urlparse(url)
            self.fb_ip = self.url_parsed.geturl()
            self.log_data("Fritz!Box URL", self.url_parsed.geturl())

        return True

    def get_soap_header(self):
        if self.auth == "":
            header = ('<s:Header>\n\t<h:InitChallenge ' +
                      'xmlns:h="http://soap-authentication.org/digest/2001/10/" ' +
                      's:mustUnderstand="1">\n\t\t' +
                      '<UserID>' + str(self.uId) + '</UserID>\n\t</h:InitChallenge >\n' +
                      '</s:Header>')

        else:
            header = ('<s:Header>\n\t<h:ClientAuth ' +
                      'xmlns:h="http://soap-authentication.org/digest/2001/10/" ' +
                      's:mustUnderstand="1">' +
                      '\n\t\t<Nonce>' + self.nonce + '</Nonce>' +
                      '\n\t\t<Auth>' + self.auth + '</Auth>' +
                      '\n\t\t<UserID>' + str(self.uId) + '</UserID>' +
                      '\n\t\t<Realm>' + self.realm + '</Realm>\n\t</h:ClientAuth>\n</s:Header>')

        return header

    # @attr p_sFormerResp Response from a previous request
    def get_soap_req(self, url_parsed, service_data, action, attr_list):

        url = (url_parsed.geturl() + service_data["controlURL"])
        url_parsed = urlparse.urlparse(url)

        # Build a SSL Context to disable certificate verification.
        html_hdr = {'Host': url_parsed.hostname,
                    'CONTENT-TYPE': 'text/xml; charset="utf-8"',
                    'SOAPACTION': '"' + service_data["serviceType"] + "#" + action + '"'}

        soap_hdr = self.get_soap_header()

        data = ('<?xml version="1.0" encoding="utf-8"?>\n' +
                '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" ' +
                's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n' +
                soap_hdr + '\n<s:Body>\n\t<u:' + action + ' xmlns:u="' +
                service_data["serviceType"] + '">')

        for key in attr_list:
            data += ('\n\t\t<' + key + '>' + attr_list[key] + '</' + key + '>')

        data += ('\n\t</u:' + action + '>\n</s:Body>\n</s:Envelope>')

        return urllib2.Request(url_parsed.geturl(), data=data, headers=html_hdr)

    def get_auth_data(self, data):
        self.nonce = self.do_regex("<Nonce>(.*?)<\\/Nonce>", data)
        self.realm = self.do_regex("<Realm>(.*?)<\\/Realm>", data)

        secret = hashlib.md5(str(self.uId) + ":" + self.realm + ":" + self.pw)
        response = hashlib.md5(secret.hexdigest() + ":" + self.nonce)

        self.auth = response.hexdigest()
        # print ("\n" + self.auth + "\n")

    def set_soap_action(self, url_parsed, service_data, action, attr_list):
        # Build a SSL Context to disable certificate verification.
        ctx = ssl._create_unverified_context()
        response_data = ""

        for x in range(0, 2):
            request = self.get_soap_req(url_parsed, service_data, action, attr_list)

            try:
                response = urllib2.urlopen(request, timeout=self.time_out, context=ctx)
                response_data = response.read()

                self.get_auth_data(response_data)

                auth_stat = self.do_regex('<Status>(.*?)<\\/Status>', response_data)

                if auth_stat != "Unauthenticated":
                    break
                else:
                    if x == 1:
                        self.DEBUG.add_message("In set_soap_action, authentication failed")

            except urllib2.HTTPError as e:
                response_data = e.read()
                error_code = re.findall('<errorCode>(.*?)</errorCode>', response_data, flags=re.S)
                error_descr = re.findall('<errorDescription>(.*?)</errorDescription>', response_data, flags=re.S)
                self.log_msg("Error:         \t" + error_descr[0] + " (" + error_code[0] + ")" +
                             "\nservice_data:\t" + json.dumps(service_data) +
                             "\naction:      \t" + action +
                             "\nattr_list:   \t" + json.dumps(attr_list))

            # except Exception as e:
            #    self.DEBUG.add_message("setSoapAction: " + str(e))
            #    print ("setWifiActive loop" + str(x) + ": " + str(e))

        dic = {}
        response_data = self.do_regex(
            '<u:' + action + 'Response.*?>(?:\\n|)(.*?)(?:\\n|)<\\/u:' + action + 'Response>', response_data)
        # if response data is available; e.g. if a set command has been send, no return value is provided
        if response_data:
            response_data = re.findall('(<.*?<\\/.*?>)', response_data, flags=re.S)
            for i in range(0, len(response_data)):
                key = self.do_regex('<(.*?)>', response_data[i])
                val = self.do_regex('>(.*?)<', response_data[i])
                dic.update({key: val})
        return dic

    def get_guest_wifi_idx(self):
        wlan_if = re.findall("<serviceType>(urn:dslforum-org:service:WLANConfiguration:[0-9]<\\/serviceType>)",
                             self.service_descr, re.S)
        self.guest_wifi_idx = len(wlan_if)
        self.log_data("Guest WIFI Index", self.guest_wifi_idx)

    def update_status(self):
        self.log_msg("Enter update_status")

        interval = self._get_input_value(self.PIN_I_NUPDATERATE)
        if interval > 0:
            if not self.init_com():
                self.log_msg("Init_com failed in update_status")
                return

            # work with wifi
            try:
                for nWifiIdx in range(1, (self.guest_wifi_idx + 1)):
                    service_data = self.get_service_data(self.service_descr,
                                                         "urn:dslforum-org:service:WLANConfiguration:" + str(nWifiIdx))

                    # get wifi status
                    attr_list = {}  # {"NewEnable":"", "NewStatus":"", "NewSSID":""}
                    data = self.set_soap_action(self.url_parsed, service_data, "GetInfo", attr_list)

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
            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:Hosts:1")
            for i in range(self.PIN_I_SMAC1, (self.PIN_I_SMAC3 + 1)):
                try:
                    value = self._get_input_value(i)

                    if value == "":
                        continue

                    attr_list = {"NewMACAddress": value}
                    data = self.set_soap_action(self.url_parsed, service_data, "GetSpecificHostEntry", attr_list)

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
                    self.log_msg("In update_status (MAC attendance), " + str(e))

            # generic mac address list
            mac_list = str(self._get_input_value(self.PIN_I_SMAC_CSV)).split(",")
            result = str()
            for mac_addr in mac_list:
                try:
                    attr_list = {"NewMACAddress": mac_addr}
                    data = self.set_soap_action(self.url_parsed, service_data, "GetSpecificHostEntry", attr_list)

                    if data:
                        ret = int(data["NewActive"])
                        result = result + str(ret) + ","
                except Exception as e:
                    self.log_msg("In update_status (Generic MAC address list), " + str(e))

            result = result[:-1]
            self.set_output_value_sbc(self.PIN_O_BMAC_CSV_AVAIL, result)
            # end mac discovery

            # MAC in Guest WIFI
            try:
                service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:WLANConfiguration:1")
                attr_list = {}
                data = self.set_soap_action(self.url_parsed, service_data, "X_AVM-DE_GetWLANDeviceListPath", attr_list)
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
                service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:X_AVM-DE_TAM:1")
                attr_list = {"NewIndex": "0"}
                data = self.set_soap_action(self.url_parsed, service_data, "GetInfo", attr_list)
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
        self.g_out_sbc = {}  # type: {int, object}
        self.fb_ip = self._get_input_value(self.PIN_I_SFBIP)
        self.url_parsed = ""  # type: urlparse
        self.service_descr = ""  # type: str
        self.nonce = ""  # type: str
        self.realm = ""  # type: str
        self.auth = ""  # type: str
        self.uId = self._get_input_value(self.PIN_I_SUID) # type: str
        self.pw = self._get_input_value(self.PIN_I_SPW) # type: str
        self.guest_wifi_idx = 0  # type: int
        self.time_out = 3  # type: int
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

        if not self.init_com():
            print("Init com failed in on_input_value")
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

            service_data = self.get_service_data(self.service_descr,
                                                 "urn:dslforum-org:service:WLANConfiguration:" + str(wifi_idx))

            # switch on wifi
            attr_list = {"NewEnable": str(wifi_on)}
            self.log_msg("WIFI SOLL: idx " + str(wifi_idx) + ", status " + str(wifi_on))
            self.set_soap_action(self.url_parsed, service_data, "SetEnable", attr_list)

            # get wifi status
            attr_list = {}
            data = self.set_soap_action(self.url_parsed, service_data, "GetInfo", attr_list)
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
            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:Hosts:1")

            attr_list = {"NewMACAddress": value}
            data = self.set_soap_action(self.url_parsed, service_data, "GetSpecificHostEntry", attr_list)

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

            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:Hosts:1")

            mac_list = str(value).split(",")
            result = str()
            for mac_addr in mac_list:
                attr_list = {"NewMACAddress": mac_addr}
                data = self.set_soap_action(self.url_parsed, service_data, "GetSpecificHostEntry", attr_list)

                if data:
                    ret = int(data["NewActive"])
                    result = result + str(ret) + ","

            result = result[:-1]
            self.set_output_value_sbc(self.PIN_O_BMAC_CSV_AVAIL, result)

        # end mac discovery

        elif index == self.PIN_I_BDIAL:
            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:X_VoIP:1")

            if value == 0:
                attr_list = {}
                self.set_soap_action(self.url_parsed, service_data, "X_AVM-DE_DialHangup", attr_list)

            else:
                attr_list = {"NewX_AVM-DE_PhoneNumber": self._get_input_value(self.PIN_I_STELNO)}
                self.set_soap_action(self.url_parsed, service_data, "X_AVM-DE_DialNumber", attr_list)
        # end dial / call

        # generic soap request
        elif index == self.PIN_I_NSOAPJSON:
            # e.g.: '{"serviceType":"urn:dslforum-org:service:WLANConfiguration:1",
            # "action_name":"SetEnable","argumentList":{"NewEnable":"1"}}'
            value = str(value)

            if value:
                value = value.replace("&quot;", '"')
                res = json.loads(value)
                service_type = res["serviceType"]
                action_name = res["action_name"]
                argument_list = res["argumentList"]

                service_data = self.get_service_data(self.service_descr, service_type)
                data = str(self.set_soap_action(self.url_parsed, service_data, action_name, argument_list))
                data = data.replace("'", '"')  # exchange ' by "

                self.set_output_value_sbc(self.PIN_O_SSOAPRPLY, str(data))

        # Trigger Reboot
        elif index == self.PIN_I_BREBOOT:
            if value == 1:
                service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:DeviceConfig:1")
                attr_list = {}
                self.set_soap_action(self.url_parsed, service_data, "Reboot", attr_list)

        # AB ein/aus
        elif index == self.PIN_I_BABEA:
            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:X_AVM-DE_TAM:1")

            if value == 0:
                attr_list = {"NewIndex": "0", "NewEnable": "0"}
                self.set_soap_action(self.url_parsed, service_data, "SetEnable", attr_list)

            else:
                attr_list = {"NewIndex": "0", "NewEnable": "1"}
                self.set_soap_action(self.url_parsed, service_data, "SetEnable", attr_list)

            attr_list = {"NewIndex": "0"}
            data = self.set_soap_action(self.url_parsed, service_data, "GetInfo", attr_list)
            is_on = data["NewEnable"] == '1'  # type: bool
            self.set_output_value_sbc(self.PIN_O_BABEA, is_on)


################################################################################


class TestSequenceFunctions(unittest.TestCase):
    test = FritzTR_064_14102_14102(0)

    def setUp(self):
        print("\n###setUp")
        with open("credentials.txt") as f:
            self.cred = json.load(f)

        self.test = FritzTR_064_14102_14102(0)

        self.test.debug_input_value[self.test.PIN_I_SUID] = self.cred["PIN_I_SUID"]
        self.test.debug_input_value[self.test.PIN_I_SPW] = self.cred["PIN_I_SPW"]
        self.test.debug_input_value[self.test.PIN_I_SFBIP] = self.cred["PIN_I_SFBIP"]

        self.test.on_init()

    def test_discover_with_ip(self):
        print("\n### test_discover_with_ip")
        ret = self.test.discover_fb()
        print ret
        self.assertNotEqual("", ret.netloc)
        self.assertNotEqual("", ret.path)

    def test_service_data(self):
        print("\n### test_service_data")
        ret = self.test.print_service_data()
        self.assertNotEqual("", ret)

    def test_soap_req(self):
        print("\n### test_soap_req")
        ain = self.cred["AIN"]
        req = '{"serviceType":"urn:dslforum-org:service:X_AVM-DE_Homeauto:1", ' \
              '"action_name":"GetSpecificDeviceInfos","argumentList":{"NewAIN":"' + ain + '"}}'

        self.test.on_input_value(self.test.PIN_I_NSOAPJSON, req)

    def test_no_route(self):
        print("\n### test_no_route")
        self.test.debug_input_value[self.test.PIN_I_SFBIP] = "192.168.173.115"
        self.test.init_com()
        self.assertTrue(True)

    def test_mac_error(self):
        print("\n### test_mac_error")
        real_mac = self.cred["REAL_MAC"]
        self.test.on_input_value(self.test.PIN_I_SMAC2, real_mac)
        ret = self.test.debug_output_value[self.test.PIN_O_BMAC2AVAIL]  # type: bool
        self.assertTrue(ret)
        self.test.on_input_value(self.test.PIN_I_SMAC3, "MAC_ERROR")
        ret = self.test.debug_output_value[self.test.PIN_O_BMAC3AVAIL]
        self.assertFalse(ret)


if __name__ == '__main__':
    unittest.main()
