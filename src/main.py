####################################################
# RaspberryPI RX/TX
# Description: RX/TX based on GNURadio for Raspberry
# Version: 1.0.0
####################################################


##############
# LIBRAIRIES #
##############

#System librairies
import sys
import os
import getopt
import time

#GNURadio objects
from gr.if_psk_rx_rpi import if_psk_rx_rpi
from gr.if_psk_tx_rpi import if_psk_tx_rpi


################
# DEFAULT CONF #
################

_def_modulation_type = "QPSK"
_def_sample_rate = 11025
_def_tx_directory_doing = "~/pi_radio/tx/doing/"
_def_tx_directory_done = "~/pi_radio/tx/done/"
_def_tx_directory_waiting = "~/pi_radio/tx/waiting/"
_def_rx_directory_doing = "./"
_def_rx_directory_done = "~/pi_radio/rx/done/"
_def_rx_directory_recovering = "~/pi_radio/rx/recovering/"


###########
# OBJECTS #
###########

#RXTX
class pi_radio_rxtx():

    def __init__(self,
        modulation_type=_def_modulation_type,
        sample_rate=_def_sample_rate):
        
        self._modulation_type = modulation_type
        self._sample_rate = sample_rate

    def set_modulation(self, modulation_type=_def_modulation_type):
        self._modulation_type = modulation_type

    def set_sample_rate(self, sample_rate=_def_sample_rate):
        self._sample_rate = sample_rate

    def receive(self, wait=False):
        print "%s RX starting" % self._modulation_type
        if self._modulation_type == "BPSK":
            rx = if_psk_rx_rpi(bits_per_symbol=1, sound_card_sample_rate=self._sample_rate)
        elif self._modulation_type == "QPSK":
            rx = if_psk_rx_rpi(bits_per_symbol=2, sound_card_sample_rate=self._sample_rate)
        elif self._modulation_type == "8PSK":
            rx = if_psk_rx_rpi(bits_per_symbol=3, sound_card_sample_rate=self._sample_rate)
#        elif self._modulation_type == "ASK":
#            rx = if_ask_rx_rpi(sound_card_sampling_rate=self._sampling_rate)
        else:
            rx = if_psk_rx_rpi(bits_per_symbol=2, sound_card_sample_rate=self._sample_rate)
        rx.start()
        print "RX started"
        if wait:
            print "waiting for RX end"
            rx.wait()
            print "RX done"

    def transmit(self, file_name, wait=False):
        print "%s TX starting" % self._modulation_type
        if self._modulation_type == "BPSK":
            tx = if_psk_tx_rpi(bits_per_symbol=1, tx_file=file_name, sound_card_sample_rate=self._sample_rate)
        elif self._modulation_type == "QPSK":
            tx = if_psk_tx_rpi(bits_per_symbol=2, tx_file=file_name, sound_card_sample_rate=self._sample_rate)
        elif self._modulation_type == "8PSK":
            tx = if_psk_tx_rpi(bits_per_symbol=3, tx_file=file_name, sound_card_sample_rate=self._sample_rate)
#        elif self._modulation_type == "ASK":
#            tx = if_ask_tx_rpi(tx_file=file_name, sound_card_sample_rate=self._sample_rate)
        else:
            tx = if_psk_tx_rpi(bits_per_symbol=2, tx_file=file_name, sound_card_sample_rate=self._sample_rate)
        tx.start()
        print "TX started"
        if wait:
            print "waiting for TX end"
            tx.wait()
            print "TX finished"

#File manager
class pi_radio_file_manager():

    def __init__(self,
        tx_directory_doing=_def_tx_directory_doing, 
        tx_directory_done=_def_tx_directory_done, 
        tx_directory_waiting=_def_tx_directory_waiting,
        rx_directory_doing=_def_rx_directory_doing,
        rx_directory_done=_def_rx_directory_done,
        rx_directory_recovering=_def_rx_directory_recovering):

        self._fec = "ZFEC"
        self._tar = "TAR/BZIP"
        self._tx_directory_doing = tx_directory_doing
        self._tx_directory_done = tx_directory_done
        self._tx_directory_waiting = tx_directory_waiting
        self._rx_directory_doing = rx_directory_doing
        self._rx_directory_done = rx_directory_done
        self._rx_directory_recovering = rx_directory_recovering
#TODO: Check folders exists and are writeable if not try to create or raise an exception

    def check_file_is_not_used(self, file_name):
        if os.path.exists(file_name):
            try:
                os.rename(file_name, file_name)
                return True
            except OSError as e:
                print 'Access-error on file "' + file_name + '"! \n' + str(e)
                return False
    
#    def check_payload(self):

#    def create_payload(self):
        #CREATE ARCHIVE COMPRESSED
        #CREATE FEC FILES
        #CREATE ARCHIVE PAYLOAD

    #Return first file found in a waiting directory or empty string if nothing found
    def detect_file_in_waiting_folder(self):
#        try:
            found_files = os.listdir(self._tx_directory_waiting)
            print 'File found'
#            if len(found_files) == 0:
#                return ""
#            else:
            return os.path.join(self._tx_directory_waiting, found_files[0])
#        except Exception, e:
#            print 'No file found'
#            return ""

#Exceptions handler
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

    
#############
# FUNCTIONS #
#############

#Version
def get_version():
    return "1.0.0"

#Help
def help():
    print "RaspberryPI RX/TX based on GNURadio"
    print "Version: %s" % get_version()

#Basic RXTX demo: usage example / basic self transmission from existing file
def basic_rxtx_demo():
    try:
        transmission_duration = 15
        print "Starting a %d seconds duplex transmission demo" % transmission_duration
        rxtx = pi_radio_rxtx()
        rxtx.receive()
        rxtx.transmit(file_name="gr/test_tx_file_ordered.csv")
        #Wait for x seconds of transmission
        time.sleep(transmission_duration)
        print "Duplex transmission demo done"
    except Exception, msg:
        raise Usage(msg)

#Basic auto TX demo: usage example / basic file detection and transmission
def basic_auto_tx_demo():
    try:
        print "Starting an automatic payload transmission demo"
        file_manager = pi_radio_file_manager()
        file_detected_and_ready = False
        while file_detected_and_ready == False:
            file_detected = file_manager.detect_file_in_waiting_folder()
            if file_detected != "":
                file_usable = file_manager.check_file_is_not_used()
                if file_usable:
                    file_detected_and_ready = True
            else:
                time.sleep(1)
        payload = file_manager.create_payload(file_name=file_detected)
        print "Payload ready"
        rxtx = pi_radio_rxtx()
        rxtx.transmit(file_name=payload, wait=True)
        print "Payload transmission done"

    except Exception, msg:
        raise Usage(msg)

#Main function
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            for o, a in opts:
                if o in ("-h", "--help"):
                    help()
                    sys.exit(0)
        
        except getopt.error, msg:
            raise Usage(msg)

        #Business code here
        basic_rxtx_demo()
        basic_auto_tx_demo()

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2


########
# MAIN #
########

#Standalone execution
if __name__ == "__main__":
    sys.exit(main())





#Web remote control on a later version
#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def hello_world():
#    return 'Hello World!'
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80)

