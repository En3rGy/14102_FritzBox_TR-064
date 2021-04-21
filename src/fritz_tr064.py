# coding: UTF-8

import unittest
import time

# functional import

import re
import urllib2
import ssl
import urlparse
import socket
import struct
import hashlib
import threading
import time

import json


#########################################################

class hsl20_4:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_output_value = {}  # type: float
        debug_set_remanent = {}  # type: float
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
            self.debug_output_value[int(pin)] = value
            print "# Out: " + str(value) + " @ pin " + str(pin)

        def _get_input_value(self, pin):
            if pin in self.debug_input_value:
                return self.debug_input_value[pin]
            else:
                return 0

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
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_4_FritzBox")
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
        self.PIN_I_SMAC4 = 11
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
        self.PIN_O_BMAC4AVAIL = 12
        self.PIN_O_BGUESTAVAIL = 13
        self.PIN_O_BABEA = 14
        self.PIN_O_SSOAPRPLY = 15
        self.FRAMEWORK._run_in_context_thread(self.on_init)

    ########################################################################################################
    #### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
    ###################################################################################################!!!##

    fb_ip = ""  # type: str
    url_parsed = "" # type: urlparse
    service_descr = ""  # type: str
    nonce = ""  # type: str
    realm = ""  # type: str
    auth = ""  # type: str
    uId = ""  # type: str
    pw = ""  # type: str
    guest_wifi_idx = 0  # type: int
    time_out = 3  # type: int

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
            self.log_data("Error", "getServiceData: " + str(e))

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
        """

        :rtype: urlparse
        """
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

    def getData(self, p_sUrl):
        url_parsed = urlparse.urlparse(p_sUrl)

        # Build a SSL Context to disable certificate verification.
        ctx = ssl._create_unverified_context()
        response_data = ""

        try:
            # Build a http request and overwrite host header with the original hostname.
            request = urllib2.Request(p_sUrl, headers={'Host': url_parsed.hostname})
            # Open the URL and read the response.
            response = urllib2.urlopen(request, timeout=self.time_out, context=ctx)
            response_data = response.read()
        except Exception as e:
            self.log_data("Error", "getData: " + str(e))
        return response_data

    def print_service_data(self):
        print(self.service_descr)

    def init_com(self):
        self.uId = self._get_input_value(self.PIN_I_SUID)
        self.pw = self._get_input_value(self.PIN_I_SPW)

        if self.url_parsed == "":
            self.url_parsed = self.discover_fb()
            self.fb_ip = self.url_parsed.geturl()

            if not self.url_parsed:
                self.log_msg("Could not discover Frtz!Box")
                return False

            self.service_descr = self.getData(self.url_parsed.geturl())
            self.getGuestWifiIdx()

            self.url_parsed = urlparse.urlparse(self.url_parsed.scheme + "://" + self.url_parsed.netloc)
            self.fb_ip = self.url_parsed.geturl()
            self.log_data("Fritz!Box URL", self.url_parsed.geturl())

            # work with device info
            serviceData = self.get_service_data(self.service_descr, "urn:dslforum-org:service:DeviceInfo:1")

            # get security port
            data = self.set_soap_action(self.url_parsed, serviceData, "GetSecurityPort", {})

            if not 'NewSecurityPort' in data:
                self.log_msg("Could retrieve security port from Fritz!Box")
            else:
                sSPort = data['NewSecurityPort']
                url = 'https://' + self.url_parsed.hostname + ":" + sSPort
                self.url_parsed = urlparse.urlparse(url)
                self.fb_ip = self.url_parsed.geturl()
                self.log_data("Fritz!Box URL", self.url_parsed.geturl())

        return True

    def getSoapHeader(self):
        sHeader = ""

        if (self.auth == ""):
            sHeader = ('<s:Header>\n\t<h:InitChallenge ' +
                       'xmlns:h="http://soap-authentication.org/digest/2001/10/" ' +
                       's:mustUnderstand="1">\n\t\t' +
                       '<UserID>' + self.uId + '</UserID>\n\t</h:InitChallenge >\n' +
                       '</s:Header>')

        else:
            sHeader = ('<s:Header>\n\t<h:ClientAuth ' +
                       'xmlns:h="http://soap-authentication.org/digest/2001/10/" ' +
                       's:mustUnderstand="1">' +
                       '\n\t\t<Nonce>' + self.nonce + '</Nonce>' +
                       '\n\t\t<Auth>' + self.auth + '</Auth>' +
                       '\n\t\t<UserID>' + self.uId + '</UserID>' +
                       '\n\t\t<Realm>' + self.realm + '</Realm>\n\t</h:ClientAuth>\n</s:Header>')

        return sHeader

    ##
    ## @attr p_sFormerResp Response from a previous request
    def get_sopa_req(self, url_parsed, service_data, action, attr_list):

        url = (url_parsed.geturl() + service_data["controlURL"])
        url_parsed = urlparse.urlparse(url)

        # Build a SSL Context to disable certificate verification.
        html_hdr = {'Host': url_parsed.hostname,
                   'CONTENT-TYPE': 'text/xml; charset="utf-8"',
                   'SOAPACTION': '"' + service_data["serviceType"] + "#" + action + '"'}

        soap_hdr = self.getSoapHeader()

        data = ('<?xml version="1.0" encoding="utf-8"?>\n' +
                '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" ' +
                's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n' +
                soap_hdr + '\n<s:Body>\n\t<u:' + action + ' xmlns:u="' +
                service_data["serviceType"] + '">')

        for key in attr_list:
            data += ('\n\t\t<' + key + '>' + attr_list[key] + '</' + key + '>')

        data += ('\n\t</u:' + action + '>\n</s:Body>\n</s:Envelope>')

        return urllib2.Request(url_parsed.geturl(), data=data, headers=html_hdr)

    def get_auth_data(self, p_sData):
        self.nonce = self.do_regex("<Nonce>(.*?)<\\/Nonce>", p_sData)
        self.realm = self.do_regex("<Realm>(.*?)<\\/Realm>", p_sData)

        secret = hashlib.md5(self.uId + ":" + self.realm + ":" + self.pw)
        response = hashlib.md5(secret.hexdigest() + ":" + self.nonce)

        self.auth = response.hexdigest()
        # print ("\n" + self.auth + "\n")

    def set_soap_action(self, url_parsed, service_data, action, attr_list, secure=False):
        # Build a SSL Context to disable certificate verification.
        ctx = ssl._create_unverified_context()
        response_data = ""

        for x in range(0, 2):
            request = self.get_sopa_req(url_parsed, service_data, action, attr_list)

            try:
                response = urllib2.urlopen(request, timeout=self.time_out, context=ctx)
                response_data = response.read()
                # print (response_data + "\n\n")

                self.get_auth_data(response_data)

                sAuthStat = self.do_regex('<Status>(.*?)<\\/Status>', response_data)

                if (sAuthStat != "Unauthenticated"):
                    break

            except urllib2.HTTPError as e:
                response_data = e.read()
                self.log_msg("setSoapAction: " + response_data)

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

    def getGuestWifiIdx(self):
        wlanIF = re.findall("<serviceType>(urn:dslforum-org:service:WLANConfiguration:[0-9]<\\/serviceType>)",
                            self.service_descr, re.S)
        self.guest_wifi_idx = len(wlanIF)
        self.log_data("Guest WIFI Index", self.guest_wifi_idx)

    def updateStatus(self):
        self.log_msg("Status requested")

        nInterval = self._get_input_value(self.PIN_I_NUPDATERATE)
        if (nInterval > 0):
            if not self.init_com():
                return

            # work with wifi
            for nWifiIdx in range(1, (self.guest_wifi_idx + 1)):
                serviceData = self.get_service_data(self.service_descr,
                                                    "urn:dslforum-org:service:WLANConfiguration:" + str(nWifiIdx))

                # get wifi status
                attrList = {}  # {"NewEnable":"", "NewStatus":"", "NewSSID":""}
                data = self.set_soap_action(self.url_parsed, serviceData, "GetInfo", attrList)

                # nOn = int(((data["NewStatus"] == "Up") and (data["NewEnable"] == '1')))
                nOn = int(data["NewEnable"] == '1')
                self.log_data("WIFI " + str(nWifiIdx), data["NewStatus"])

                if nWifiIdx == 1:
                    self._set_output_value(self.PIN_O_BRMWLAN1ONOFF, nOn)
                    self._set_output_value(self.PIN_O_SWIFI1SSID, data["NewSSID"])

                elif nWifiIdx == 2:
                    self._set_output_value(self.PIN_O_BRMWLAN2ONOFF, nOn)
                    self._set_output_value(self.PIN_O_SWIFI2SSID, data["NewSSID"])

                elif nWifiIdx == 3:
                    self._set_output_value(self.PIN_O_BRMWLAN3ONOFF, nOn)
                    self._set_output_value(self.PIN_O_SWIFI3SSID, data["NewSSID"])

                if nWifiIdx == self.guest_wifi_idx:
                    self._set_output_value(self.PIN_O_BRMWLANGUESTONOFF, nOn)
                    self._set_output_value(self.PIN_O_SWIFIGUESTSSID, data["NewSSID"])
            ###End Wifi

            ###MAC attendence
            serviceData = self.get_service_data(self.service_descr, "urn:dslforum-org:service:Hosts:1")
            for i in range(self.PIN_I_SMAC1, (self.PIN_I_SMAC4 + 1)):
                value = self._get_input_value(i)

                if value == "":
                    continue

                attrList = {"NewMACAddress": value}
                data = self.set_soap_action(self.url_parsed, serviceData, "GetSpecificHostEntry", attrList)

                nRet = 0
                if (data):
                    nRet = int(data["NewActive"])

                if (i == self.PIN_I_SMAC1):
                    self._set_output_value(self.PIN_O_BMAC1AVAIL, nRet)
                elif (i == self.PIN_I_SMAC2):
                    self._set_output_value(self.PIN_O_BMAC2AVAIL, nRet)
                elif (i == self.PIN_I_SMAC3):
                    self._set_output_value(self.PIN_O_BMAC3AVAIL, nRet)
                elif (i == self.PIN_I_SMAC4):
                    self._set_output_value(self.PIN_O_BMAC4AVAIL, nRet)
            ### end mac discovery

            ###MAC in Guest WIFI
            try:
                serviceData = self.get_service_data(self.service_descr, "urn:dslforum-org:service:WLANConfiguration:1")
                attrList = {}
                data = self.set_soap_action(self.url_parsed, serviceData, "X_AVM-DE_GetWLANDeviceListPath", attrList)
                path = data["NewX_AVM-DE_WLANDeviceListPath"]
                path = self.url_parsed.geturl() + path
                contents = self.getData(path)
                nRet = "<AssociatedDeviceGuest>1</AssociatedDeviceGuest>" in contents
                self._set_output_value(self.PIN_O_BGUESTAVAIL, nRet)
            except Exception as e:
                pass
            ###end MAC in Guest WIFI

            ###AB
            try:
                serviceData = self.get_service_data(self.service_descr, "urn:dslforum-org:service:X_AVM-DE_TAM:1")
                attrList = {"NewIndex": "0"}
                data = self.set_soap_action(self.url_parsed, serviceData, "GetInfo", attrList)
                if (data):
                    nOn = int(data["NewEnable"] == '1')
                    self._set_output_value(self.PIN_O_BABEA, nOn)
            except Exception as e:
                pass
            ### end AB

            t = threading.Timer(nInterval, self.updateStatus).start()

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()
        self.fb_ip = self._get_input_value(self.PIN_I_SFBIP)
        self.updateStatus()

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
            return

        if not self.init_com():
            return

        if index == self.PIN_I_NUPDATERATE:
            if interval > 0:
                self.updateStatus()

        # work with wifi
        elif index == self.PIN_I_BWIFI1ON or index == self.PIN_I_BWIFI2ON or index == self.PIN_I_BWIFI3ON or index == self.PIN_I_BWIFIGUESTON:

            bWifiOn = int(value)
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
            attrList = {"NewEnable": str(bWifiOn)}
            self.log_msg("WIFI SOLL: idx " + str(wifi_idx) + ", status " + str(bWifiOn))
            data = self.set_soap_action(self.url_parsed, service_data, "SetEnable", attrList)

            # get wifi status
            attrList = {}
            data = self.set_soap_action(self.url_parsed, service_data, "GetInfo", attrList)
            self.log_data("SOAP Repl.", str(data))

            nOn = int(data["NewEnable"] == '1')

            if wifi_idx == self.guest_wifi_idx:
                self._set_output_value(self.PIN_O_BRMWLANGUESTONOFF, nOn)
                self._set_output_value(self.PIN_O_SWIFIGUESTSSID, data["NewSSID"])
                self.log_msg("RM Guest Wifi")

            if wifi_idx == 1:
                self._set_output_value(self.PIN_O_BRMWLAN1ONOFF, nOn)
                self._set_output_value(self.PIN_O_SWIFI1SSID, data["NewSSID"])
                self.log_msg("RM Wifi 1")

            elif wifi_idx == 2:
                self._set_output_value(self.PIN_O_BRMWLAN2ONOFF, nOn)
                self._set_output_value(self.PIN_O_SWIFI2SSID, data["NewSSID"])
                self.log_msg("RM Wifi 2")

            elif wifi_idx == 3:
                self._set_output_value(self.PIN_O_BRMWLAN3ONOFF, nOn)
                self._set_output_value(self.PIN_O_SWIFI3SSID, data["NewSSID"])
                self.log_msg("RM Wifi 3")

        ### End Wifi

        elif (
                index == self.PIN_I_SMAC1 or index == self.PIN_I_SMAC2 or index == self.PIN_I_SMAC3 or index == self.PIN_I_SMAC4):
            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:Hosts:1")

            attrList = {"NewMACAddress": value}
            data = self.set_soap_action(self.url_parsed, service_data, "GetSpecificHostEntry", attrList)

            nRet = 0
            if (data):
                nRet = int(data["NewActive"])

            if index == self.PIN_I_SMAC1:
                self._set_output_value(self.PIN_O_BMAC1AVAIL, nRet)
            elif index == self.PIN_I_SMAC2:
                self._set_output_value(self.PIN_O_BMAC2AVAIL, nRet)
            elif index == self.PIN_I_SMAC3:
                self._set_output_value(self.PIN_O_BMAC3AVAIL, nRet)
            elif index == self.PIN_I_SMAC4:
                self._set_output_value(self.PIN_O_BMAC4AVAIL, nRet)
        ### end mac discovery

        elif index == self.PIN_I_BDIAL:
            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:X_VoIP:1")

            if value == 0:
                attrList = {}
                data = self.set_soap_action(self.url_parsed, service_data, "X_AVM-DE_DialHangup", attrList)

            else:
                attrList = {"NewX_AVM-DE_PhoneNumber": self._get_input_value(self.PIN_I_STELNO)}
                data = self.set_soap_action(self.url_parsed, service_data, "X_AVM-DE_DialNumber", attrList)
        ### end dial / call

        ### generic soap request
        elif index == self.PIN_I_NSOAPJSON:
            # e.g.: '{"serviceType":"urn:dslforum-org:service:WLANConfiguration:1", "action_name":"SetEnable","argumentList":{"NewEnable":"1"}}'
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

                self._set_output_value(self.PIN_O_SSOAPRPLY, str(data))

        # Trigger Reboot
        elif index == self.PIN_I_BREBOOT:
            if value == 1:
                service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:DeviceConfig:1")
                attrList = {}
                data = self.set_soap_action(self.url_parsed, service_data, "Reboot", attrList)

        # AB ein/aus
        elif index == self.PIN_I_BABEA:
            service_data = self.get_service_data(self.service_descr, "urn:dslforum-org:service:X_AVM-DE_TAM:1")

            if value == 0:
                attrList = {"NewIndex": "0", "NewEnable": "0"}
                data = self.set_soap_action(self.url_parsed, service_data, "SetEnable", attrList)

            else:
                attrList = {"NewIndex": "0", "NewEnable": "1"}
                data = self.set_soap_action(self.url_parsed, service_data, "SetEnable", attrList)

            attrList = {"NewIndex": "0"}
            data = self.set_soap_action(self.url_parsed, service_data, "GetInfo", attrList)
            bOn = data["NewEnable"] == '1'
            self._set_output_value(self.PIN_O_BABEA, bOn)


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
        self.test.print_service_data()
        self.assertTrue(True)

    def test_soap_req(self):
        print("\n### test_soap_req")
        ain = self.cred["AIN"]
        req = '{"serviceType":"urn:dslforum-org:service:X_AVM-DE_Homeauto:1", "action_name":"GetSpecificDeviceInfos","argumentList":{"NewAIN":"' + ain + '"}}'

        self.test.on_input_value(self.test.PIN_I_NSOAPJSON, req)

        # test.m_url_parsed = test.discover("192.168.178.30")
        #
        # if (not test.m_url_parsed):
        #     print ("Discovery failed")
        #     quit()
        #
        # print "Discovery: \t" + test.m_url_parsed.geturl()
        #
        # if (not test.m_url_parsed):
        #     print "No data to continue. Quitting."
        #     quit()
        #
        # test.m_sServiceDscr = test.getData(test.m_url_parsed.geturl())
        #
        # test.m_url_parsed = urlparse.urlparse(test.m_url_parsed.scheme + "://" + test.m_url_parsed.netloc)
        # print "Plain URL: \t" + test.m_url_parsed.geturl()
        #
        # # work with device info
        # serviceData = test.getServiceData(test.m_sServiceDscr, "urn:dslforum-org:service:DeviceInfo:1")
        #
        # # get security port
        # data = test.setSoapAction(test.m_url_parsed, serviceData, "GetSecurityPort", {})
        # print "\n---"
        # print data
        # print "---\n"
        #
        # sSPort = data['NewSecurityPort']
        # url = 'https://' + test.m_url_parsed.hostname + ":" + sSPort
        # test.m_url_parsed = urlparse.urlparse(url)
        # print "Secure URL: \t" + test.m_url_parsed.geturl()
        #
        # data = test.updateStatus()
        #
        # # wlanIF = re.findall("<serviceType>(urn:dslforum-org:service:WLANConfiguration:[0-9]<\\/serviceType>)", test.m_sServiceDscr, re.S)
        # # print len(wlanIF)
        #
        # # work with wifi
        # # serviceData = test.getServiceData(test.m_sServiceDscr, "urn:dslforum-org:service:WLANConfiguration:" + nWifiIdx)
        # # attrList = {"NewEnable" : str(bWifiOn)}
        # # data = test.setSoapAction(test.m_url_parsed, serviceData, "SetEnable", attrList)
        # # print "\n---"
        # # print data
        # # print "---\n"
        # # serviceData = test.getServiceData(test.m_sServiceDscr, "urn:dslforum-org:service:DeviceConfig:1")
        # # attrList = {}
        # # print "done"
        # # data = test.setSoapAction(test.m_url_parsed, serviceData, "Reboot", attrList)
        #
        # # print "\n---"
        # # print data["NewEnable"]
        # # print "---\n"


if __name__ == '__main__':
    unittest.main()
