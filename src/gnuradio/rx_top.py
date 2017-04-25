#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rx Top
# Generated: Sat Apr 22 09:25:33 2017
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
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys


class rx_top(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Rx Top")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Rx Top")
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

        self.settings = Qt.QSettings("GNU Radio", "rx_top")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.sound_card_sample_rate = sound_card_sample_rate = 96000
        self.samples_per_symbol = samples_per_symbol = 19
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        self.bits_per_symbol = bits_per_symbol = 1
        
        self.variable_rrc_filter_taps = variable_rrc_filter_taps = firdes.root_raised_cosine(1, sound_card_sample_rate, symbol_rate, 0.5, 70)
          
        self.rolloff = rolloff = 0.5
        self.bit_rate = bit_rate = symbol_rate/bits_per_symbol

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0 = qtgui.sink_c(
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
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        
        self.qtgui_sink_x_0.enable_rf_freq(False)
        
        
          
        self.low_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, sound_card_sample_rate, sound_card_sample_rate/4, sound_card_sample_rate/8, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, sound_card_sample_rate, sound_card_sample_rate/4, sound_card_sample_rate/8, firdes.WIN_HAMMING, 6.76))
        self.digital_psk_demod_0 = digital.psk.psk_demod(
          constellation_points=bits_per_symbol*2,
          differential=True,
          samples_per_symbol=samples_per_symbol,
          excess_bw=rolloff,
          phase_bw=6.28/100.0,
          timing_bw=6.28/100.0,
          mod_code="gray",
          verbose=False,
          log=True,
          )
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(32, 500)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('tx_signal.wav', False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_tagged_file_sink_0 = blocks.tagged_file_sink(gr.sizeof_char*1, bit_rate)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'burst')
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_SIN_WAVE, sound_card_sample_rate/4, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_COS_WAVE, sound_card_sample_rate/4, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_psk_demod_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_sink_x_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_file_sink_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.digital_psk_demod_0, 0), (self.digital_hdlc_deframer_bp_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rx_top")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)
        self.qtgui_sink_x_0.set_frequency_range(0, self.sound_card_sample_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.sound_card_sample_rate, self.sound_card_sample_rate/4, self.sound_card_sample_rate/8, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.sound_card_sample_rate, self.sound_card_sample_rate/4, self.sound_card_sample_rate/8, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.sound_card_sample_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.sound_card_sample_rate)
        self.analog_sig_source_x_0_0.set_frequency(self.sound_card_sample_rate/4)
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
        self.set_bit_rate(self.symbol_rate/self.bits_per_symbol)

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.set_bit_rate(self.symbol_rate/self.bits_per_symbol)

    def get_variable_rrc_filter_taps(self):
        return self.variable_rrc_filter_taps

    def set_variable_rrc_filter_taps(self, variable_rrc_filter_taps):
        self.variable_rrc_filter_taps = variable_rrc_filter_taps

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate


def main(top_block_cls=rx_top, options=None):

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
