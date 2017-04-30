####################################################
# RaspberryPI RX/TX
# Description: RX/TX based on GNURadio for Raspberry
# Version: 1.0.0
####################################################


##############
# LIBRAIRIES #
##############

#Standard librairies
import getopt
#https://docs.python.org/2/library/getopt.html
import logging
#https://docs.python.org/2/library/logging.html
import os
#https://docs.python.org/2/library/os.html
import sys
#https://docs.python.org/2/library/sys.html
import time
#https://docs.python.org/2/library/time.html
import shutil
#https://docs.python.org/2/library/shutil.html
import gzip
#https://docs.python.org/2/library/gzip.html
#import tarfile
#https://docs.python.org/2/library/tarfile.html

#External librairies
from zfec import filefec
#https://pypi.python.org/pypi/zfec

#GNURadio RASPI librairies
from gr.if_psk_rx_rpi_lib import if_psk_rx_rpi
from gr.if_psk_tx_rpi_lib import if_psk_tx_rpi


################
# DEFAULT CONF #
################

#Transmission parameters
#Physical layer
_def_modulation_type = "QPSK"
_def_sample_rate = 22000
#Source coding
_def_gzip_compress_level = 9
_def_zfec_required_parts = 5
_def_zfec_total_parts = 10

#Software parameters
#Logging
_def_logging_format = "%(asctime)-15s - %(levelname)s: %(message)s"
_def_logging_level = logging.INFO
#Folders
_def_rxtx_directory = "/home/pi_radio"
_def_tx_directory_doing = _def_rxtx_directory + "/tx/doing/"
_def_tx_directory_done = _def_rxtx_directory + "/tx/done/"
_def_tx_directory_waiting = _def_rxtx_directory + "/tx/waiting/"
_def_rx_directory_doing = "./"
_def_rx_directory_done = _def_rxtx_directory + "/rx/done/"
_def_rx_directory_recovering = _def_rxtx_directory + "/rx/recovering/"


###########
# CLASSES #
###########

#RXTX
#FIXME: WAIT DOESN'T GIVE BACK HAND IN TX
class pi_radio_rxtx():

    def __init__(self,
        modulation_type=None,
        sample_rate=None):

        self._modulation_type = modulation_type or _def_modulation_type
        self._sample_rate = sample_rate or _def_sample_rate

    def set_modulation(self, modulation_type=None):
        self._modulation_type = modulation_type or _def_modulation_type

    def set_sample_rate(self, sample_rate=None):
        self._sample_rate = sample_rate or _def_sample_rate

#TODO: Advanced transmission / advanced reception
#ALOHA LIKE PROTOCOL
#1.TX/RX: LISTEN
#2.TX: IF NO TRAFIC
#3.TX: SEND MAGIC PACKET WITH NUMBER OF FILES AND WILL TRANSMIT
#4.RX: SEND ACK PACKET WITH NUMBER OF FILES
#5.TX: IF EVERYTHING OK CONTINUE ELSE GO BACK TO 3
#6.TX: SEND FILE N + PAUSE AT END
#7.RX: WHEN PAUSE - MOVE FILE + SEND FILE RX / NO CHECK
#8.RX: TRY TO RECOVER FILE WITH FEC
#9.RX: OK / KO - RETRY

    def receive(self, wait=False):
        logging.debug("RX starting with parameters:")
        logging.debug("RX modulation: %s" % self._modulation_type)
        logging.debug("RX sample rate: %d" % self._sample_rate)
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
        logging.debug("RX started")
        if wait:
            logging.debug("waiting for RX end")
            rx.wait()
            logging.debug("RX done")

    def transmit(self, file_name, wait=False):
        logging.debug("TX starting")
        logging.debug("TX modulation: %s" % self._modulation_type)
        logging.debug("TX sample rate: %d" % self._sample_rate)
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
        logging.debug("TX started")
        if wait:
            logging.debug("waiting for TX end")
            tx.wait()
            logging.debug("TX finished")

#File manager
class pi_radio_file_manager():

    def __init__(self,
        tx_directory_doing=_def_tx_directory_doing, 
        tx_directory_done=_def_tx_directory_done, 
        tx_directory_waiting=_def_tx_directory_waiting,
        rx_directory_doing=_def_rx_directory_doing,
        rx_directory_done=_def_rx_directory_done,
        rx_directory_recovering=_def_rx_directory_recovering):

        self._tx_directory_doing = tx_directory_doing
        self._tx_directory_done = tx_directory_done
        self._tx_directory_waiting = tx_directory_waiting
        self._rx_directory_doing = rx_directory_doing
        self._rx_directory_done = rx_directory_done
        self._rx_directory_recovering = rx_directory_recovering
#TODO: Check folders exists and are writeable if not try to create or raise an exception

    def check_file_is_not_used(self, file_name):
        if os.path.exists(self._tx_directory_waiting + file_name):
            try:
                os.rename(self._tx_directory_waiting + file_name, self._tx_directory_waiting + file_name)
                return True
            except OSError as e:
                logging.error("Access-error on file " + file_name + ": " + str(e))
                return False
        else:
            raise Exception("Cannot check for file access on a non-existing file: " + file_name)

    def recover_payload(self, file_name):
        #Move file to working dir
        if os.path.exists(self._rx_directory_waiting + file_name):
            try:
                os.rename(self._rx_directory_waiting + file_name, self._rx_directory_doing + file_name)
                return self._rx_directory_doing + file_name
            except OSError as e:
                raise Exception("Cannot move file to working directory " + file_name + ": " + str(e))

    def create_payload(self, file_name):
        #Move file to working dir
        if os.path.exists(self._tx_directory_waiting + file_name):
            try:
                os.rename(self._tx_directory_waiting + file_name, self._tx_directory_doing + file_name)
                logging.debug("File moved to working directory")
            except OSError as e:
                raise Exception("Cannot move file to working directory " + file_name + ": " + str(e))

        #Compress file
        try:
            source_file = open(self._tx_directory_doing + file_name, 'rb')
            compressed_file_name = file_name + ".gz"
            target_file = gzip.open(self._tx_directory_doing + compressed_file_name, 'wb', _def_gzip_compress_level)
            shutil.copyfileobj(source_file, target_file)
            source_file.close()
            target_file.close()
            logging.debug("File compressed: %s" % compressed_file_name)
        except Exception, e:
            raise Exception("Cannot compress file " + file_name + ": " + str(e))

        #Create FEC files
        try:
            source_file = open(self._tx_directory_doing + compressed_file_name, 'rb')
            source_file_size = os.path.getsize(self._tx_directory_doing + compressed_file_name)
            filefec.encode_to_files(source_file, source_file_size, self._tx_directory_doing, file_name, _def_zfec_required_parts, _def_zfec_total_parts, suffix=".fec", overwrite=True, verbose=False)
            source_file.close()
            fec_files = []
            for fec_part in range (_def_zfec_total_parts):
                fec_file_name = self._tx_directory_doing + file_name + ".%02d"%fec_part + "_%02d"%_def_zfec_total_parts + ".fec"
                fec_files.append(fec_file_name)
            logging.debug("Error correction files created: %s" % ' + '.join(sorted(fec_files)))
        except Exception, e:
            raise Exception("Cannot create error correcting files " + file_name + ": " + str(e))

        return fec_files

    #Return first file found in a waiting directory or empty string if nothing found
    def detect_file_in_waiting_folder(self):
        try:
            found_files = os.listdir(self._tx_directory_waiting)
            if len(found_files) == 0:
                logging.debug("Folder is empty")
                return ""
            else:
                logging.debug("%d file(s) found: " % len(found_files) + ' + '.join(sorted(found_files)))
                return os.path.join(found_files[0])
        except Exception, e:
            logging.error("Error during file research: " + str(e))
            return ""

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
    print "Software usage:"
    print "$ python main.py [OPTIONS]"
    print "OPTIONS can be:"
    print "-c | --compression $LEVEL: set source coding compression level, where LEVEL can go from 0 (no compression) to 9 (max compression)"
    print "-d | --debug: increase logging level verbosity to debug"
    print "-m | --modulation $TYPE: set physical layer modulation used, where TYPE can be ASK, BPSK, QPSK, 8PSK"
    print "-r | --rate $RATE: set sound card sampling rate, where RATE depends on the sound card used (ex: 11000, 22000, 44100, 96000)"
    print "-s | --silent: decrease logging level verbosity to errors only"

#Basic RXTX demo: usage example / basic self transmission from existing file
def basic_rxtx_demo():
    try:
        transmission_duration = 15
        logging.info("Starting a %d seconds duplex transmission demo" % transmission_duration)
        rxtx = pi_radio_rxtx()
        rxtx.receive()
        rxtx.transmit(file_name="gr/test_tx_file_ordered.csv")
        #Wait for x seconds of transmission
        time.sleep(transmission_duration)
        logging.info("Duplex transmission demo done")
    except Exception, msg:
        raise Usage(msg)

#Basic auto TX demo: usage example / basic file detection and transmission
def basic_auto_tx_demo():
    try:
        detection_sleep_duration = 1
        logging.info("Starting an automatic payload transmission demo")
        file_manager = pi_radio_file_manager()
        file_detected_and_ready = False
        while file_detected_and_ready == False:
            file_detected = file_manager.detect_file_in_waiting_folder()
            if file_detected != "":
                file_usable = file_manager.check_file_is_not_used(file_name=file_detected)
                if file_usable:
                    file_detected_and_ready = True
            else:
                time.sleep(detection_sleep_duration)
        payload = file_manager.create_payload(file_name=file_detected)
        logging.info("Payload ready")
#        logging.info("Transmitting payload")
#TODO: ADVANCED PROTOCOL HERE
#        logging.info("Payload transmission done")

    except Exception, msg:
        raise Usage(msg)

#Basic auto RX demo: usage example / basic file reception and recovery
def basic_auto_rx_demo():
    try:
        logging.info("Payload reception done")
    except Exception, msg:
        raise Usage(msg)

#Main function
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "c:dhm:r:s", ["compress=","debug","help","modulation=","rate=","silent"])
            for o, a in opts:
                if o in ("-m", "--modulation"):
                #TODO: CHECK SUPPORTED COMPRESSION LEVELS HERE
                    global _def_gzip_compress_level
                    _def_gzip_compress_level = int(a)
                if o in ("-d", "--debug"):
                    logging.basicConfig(format=_def_logging_format, level=logging.DEBUG)
                if o in ("-h", "--help"):
                    help()
                    sys.exit(0)
                if o in ("-m", "--modulation"):
                #TODO: CHECK SUPPORTED MODULATIONS HERE AND ADD THEM IN HELP
                    global _def_modulation_type
                    _def_modulation_type = a
                if o in ("-r", "--rate"):
                #TODO: CHECK SUPPORTED RATES HERE AND ADD THEM IN HELP
                    global _def_sample_rate
                    _def_sample_rate = int(a)
                if o in ("-s", "--silent"):
                    logging.basicConfig(format=_def_logging_format, level=logging.ERROR)

            #If no specific loglevel has been set - call work only once so first call takes precedence
            logging.basicConfig(format=_def_logging_format, level=_def_logging_level)
        
        except getopt.error, msg:
            raise Usage(msg)

        #Business code here
        #basic_rxtx_demo()
        basic_auto_tx_demo()

    except Usage, err:
        print >>sys.stderr, logging.error(err.msg)
        print >>sys.stderr, "for help use -h or --help"
        return 2


########
# MAIN #
########

#Standalone execution
if __name__ == "__main__":
    sys.exit(main())




        
        #Create an archive file with all files
#        try:
#            tar = tarfile.open(self._tx_directory_doing + file_name + ".tar", mode="w", dereference=True, ignore_zeros=True, debug=3)
#            for fec_part in range (_def_zfec_total_parts):
#                fec_file_name = self._tx_directory_doing + file_name + ".%02d"%fec_part + "_%02d"%_def_zfec_total_parts + ".fec"
#                logging.debug("Adding file to archive: %s" % fec_file_name)
#                tar.add(fec_file_name)
#            tar.close()
#        except Exception, e:
#            raise Exception("Cannot create archive file " + file_name + ": " + str(e))


#Web remote control on a later version
#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def hello_world():
#    return 'Hello World!'
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80)

