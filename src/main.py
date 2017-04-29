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
import getopt
import time

#GNURadio objects
from gr.if_psk_rx_rpi import if_psk_rx_rpi
from gr.if_psk_tx_rpi import if_psk_tx_rpi


###########
# OBJECTS #
###########

#Business code
class pi_radio():

    def __init__(self):
        self._test = "test"

    def receive(self, wait=False):
        print "RX starting"
        rx = if_psk_rx_rpi()
        rx.start()
        print "RX started"
        if wait:
            print "waiting for RX end"
            rx.wait()
            print "RX done"

    def transmit(self, file_name, wait=False):
        print "TX starting"
        tx = if_psk_tx_rpi(tx_file=file_name)
        tx.start()
        print "TX started"
        if wait:
            print "waiting for TX end"
            tx.wait()
            print "TX finished"


#Exceptions handler
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


#############
# FUNCTIONS #
#############

#Version function
def get_version():
    return "1.0.0"

#Help function
def help():
    print "RaspberryPI RX/TX based on GNURadio"
    print "Version: %s" % get_version()

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
            #Usage example / basic self transmission possible
            rxtx = pi_radio()
            rxtx.transmit("gr/test_tx_file_ordered.csv")
            rxtx.receive()
            #Wait for 15 seconds of transmission
            time.sleep(15)
            
            
        except getopt.error, msg:
             raise Usage(msg)

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

