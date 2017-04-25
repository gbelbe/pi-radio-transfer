#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Top
# Generated: Thu Apr 20 00:20:22 2017
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys


class tx_top(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Tx Top")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tx Top")
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

        self.settings = Qt.QSettings("GNU Radio", "tx_top")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.sound_card_sample_rate = sound_card_sample_rate = 24000
        self.samples_per_symbol = samples_per_symbol = 19
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        self.rolloff = rolloff = 0.1
        self.bits_per_symbol = bits_per_symbol = 2

        ##################################################
        # Blocks
        ##################################################
        self.final = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sound_card_sample_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.final.set_update_time(1.0/10)
        self._final_win = sip.wrapinstance(self.final.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._final_win)
        
        self.final.enable_rf_freq(False)
        
        
          
        self.digital_psk_mod_0 = digital.psk.psk_mod(
          constellation_points=bits_per_symbol*2,
          mod_code="gray",
          differential=True,
          samples_per_symbol=samples_per_symbol,
          excess_bw=rolloff,
          verbose=False,
          log=False,
          )
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb('packet_len')
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('tx_signal.wav', 1, int(sound_card_sample_rate), 8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 32, "packet_len")
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/gbelbe/Develop/pi-radio-transfer/src/gnuradio/IMGP7081.JPG', False)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(sound_card_sample_rate, analog.GR_COS_WAVE, sound_card_sample_rate/4, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_hdlc_framer_pb_0, 'in'))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.digital_psk_mod_0, 0))    
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.digital_psk_mod_0, 0), (self.final, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_top")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)
        self.final.set_frequency_range(0, self.sound_card_sample_rate)
        self.blocks_throttle_0.set_sample_rate(self.sound_card_sample_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.sound_card_sample_rate)
        self.analog_sig_source_x_0.set_frequency(self.sound_card_sample_rate/4)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol


def main(top_block_cls=tx_top, options=None):

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
