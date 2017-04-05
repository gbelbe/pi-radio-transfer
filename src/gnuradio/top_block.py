#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed Apr  5 22:01:01 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 5000
        self.bits_per_symbol = bits_per_symbol = 1

        ##################################################
        # Blocks
        ##################################################
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb("packet_len")
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(32, 500)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf(([-1,1]), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, symbol_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-0.1, 0.1, 0)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_tagged_file_sink_0 = blocks.tagged_file_sink(gr.sizeof_char*1, symbol_rate/16)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 32, "packet_len")
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "burst")
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "/home/grembert/pi-radio-transfer/src/gnuradio/test_src_file.txt", True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_hdlc_framer_pb_0, 'in'))    
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_float_to_char_0, 0), (self.digital_hdlc_deframer_bp_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_file_sink_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_char_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.blocks_throttle_0.set_sample_rate(self.symbol_rate)

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
