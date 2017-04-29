#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: If Psk Tx
# Description: IF PSK TX
# Generated: Sat Apr 29 20:04:49 2017
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
import math
import sip
import sys


class if_psk_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "If Psk Tx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("If Psk Tx")
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

        self.settings = Qt.QSettings("GNU Radio", "if_psk_tx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.sound_card_sample_rate = sound_card_sample_rate = 11025
        self.samples_per_symbol = samples_per_symbol = 16
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        self.bits_per_symbol = bits_per_symbol = 2
        self.hdlc_packet_overhead = hdlc_packet_overhead = 6*8
        self.hdlc_packet_length = hdlc_packet_length = 16*8
        self.channel_bit_rate = channel_bit_rate = symbol_rate*bits_per_symbol
        self.source_bit_rate = source_bit_rate = channel_bit_rate*hdlc_packet_length/(hdlc_packet_overhead+hdlc_packet_length)
        self.rolloff = rolloff = 0.5
        self.quantization_depth = quantization_depth = 16
        self.if_frequency = if_frequency = sound_card_sample_rate/4

        ##################################################
        # Blocks
        ##################################################
        self.final_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sound_card_sample_rate, #bw
        	"IF modulated signal", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	False, #plotconst
        )
        self.final_0.set_update_time(1.0/10)
        self._final_0_win = sip.wrapinstance(self.final_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._final_0_win)
        
        self.final_0.enable_rf_freq(False)
        
        
          
        self.final = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sound_card_sample_rate, #bw
        	"Baseband signal", #name
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
          constellation_points=pow(2,bits_per_symbol),
          mod_code="gray",
          differential=True,
          samples_per_symbol=samples_per_symbol,
          excess_bw=rolloff,
          verbose=False,
          log=False,
          )
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb("packet_len")
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("tx_signal.wav", 1, sound_card_sample_rate, quantization_depth)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_char*1, source_bit_rate/8,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, hdlc_packet_length/8, "packet_len")
        self.blocks_multiply_xx_0_0_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "test_tx_file_ordered.csv", False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_COS_WAVE, if_frequency, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_SIN_WAVE, if_frequency, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_hdlc_framer_pb_0, 'in'))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0_1, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.final_0, 0))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0_0_0, 1))    
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_0_0_1, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0_1, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.blocks_throttle_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_psk_mod_0, 0))    
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))    
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_complex_to_float_0, 0))    
        self.connect((self.digital_psk_mod_0, 0), (self.final, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "if_psk_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_if_frequency(self.sound_card_sample_rate/4)
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)
        self.analog_sig_source_x_0.set_sampling_freq(self.sound_card_sample_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.sound_card_sample_rate)
        self.blocks_throttle_0.set_sample_rate(self.sound_card_sample_rate)
        self.final.set_frequency_range(0, self.sound_card_sample_rate)
        self.final_0.set_frequency_range(0, self.sound_card_sample_rate)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_channel_bit_rate(self.symbol_rate*self.bits_per_symbol)

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.set_channel_bit_rate(self.symbol_rate*self.bits_per_symbol)

    def get_hdlc_packet_overhead(self):
        return self.hdlc_packet_overhead

    def set_hdlc_packet_overhead(self, hdlc_packet_overhead):
        self.hdlc_packet_overhead = hdlc_packet_overhead
        self.set_source_bit_rate(self.channel_bit_rate*self.hdlc_packet_length/(self.hdlc_packet_overhead+self.hdlc_packet_length))

    def get_hdlc_packet_length(self):
        return self.hdlc_packet_length

    def set_hdlc_packet_length(self, hdlc_packet_length):
        self.hdlc_packet_length = hdlc_packet_length
        self.set_source_bit_rate(self.channel_bit_rate*self.hdlc_packet_length/(self.hdlc_packet_overhead+self.hdlc_packet_length))
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.hdlc_packet_length/8)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.hdlc_packet_length/8)

    def get_channel_bit_rate(self):
        return self.channel_bit_rate

    def set_channel_bit_rate(self, channel_bit_rate):
        self.channel_bit_rate = channel_bit_rate
        self.set_source_bit_rate(self.channel_bit_rate*self.hdlc_packet_length/(self.hdlc_packet_overhead+self.hdlc_packet_length))

    def get_source_bit_rate(self):
        return self.source_bit_rate

    def set_source_bit_rate(self, source_bit_rate):
        self.source_bit_rate = source_bit_rate
        self.blocks_throttle_0_0.set_sample_rate(self.source_bit_rate/8)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_quantization_depth(self):
        return self.quantization_depth

    def set_quantization_depth(self, quantization_depth):
        self.quantization_depth = quantization_depth

    def get_if_frequency(self):
        return self.if_frequency

    def set_if_frequency(self, if_frequency):
        self.if_frequency = if_frequency
        self.analog_sig_source_x_0.set_frequency(self.if_frequency)
        self.analog_sig_source_x_0_0.set_frequency(self.if_frequency)


def main(top_block_cls=if_psk_tx, options=None):

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
