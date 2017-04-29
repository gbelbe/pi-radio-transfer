#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: If Psk Rx
# Description: IF PSK RX
# Generated: Sat Apr 29 20:06:33 2017
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
import math
import raspi_decoder
import sip
import sys


class if_psk_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "If Psk Rx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("If Psk Rx")
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

        self.settings = Qt.QSettings("GNU Radio", "if_psk_rx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.if_decimation = if_decimation = 2
        self.sound_card_sample_rate = sound_card_sample_rate = 11025
        self.samples_per_symbol = samples_per_symbol = 16/if_decimation
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        self.bits_per_symbol = bits_per_symbol = 2
        self.rolloff = rolloff = 0.5
        self.hdlc_packet_overhead = hdlc_packet_overhead = 6*8
        self.hdlc_packet_length = hdlc_packet_length = 16*8
        self.channel_bit_rate = channel_bit_rate = symbol_rate*bits_per_symbol
        
        self.variable_rrc_filter_taps = variable_rrc_filter_taps = firdes.root_raised_cosine(1, sound_card_sample_rate/if_decimation, symbol_rate, rolloff, 11*samples_per_symbol)
          
        self.source_bit_rate = source_bit_rate = channel_bit_rate*hdlc_packet_length/(hdlc_packet_overhead+hdlc_packet_length)
        self.if_frequency = if_frequency = sound_card_sample_rate/4

        ##################################################
        # Blocks
        ##################################################
        self.raspi_decoder_psk_constellation_decoder_0 = raspi_decoder.psk_constellation_decoder(
          bits_per_symbol=bits_per_symbol,
          differential=True,
          mod_code="gray",
          debug=False,
          )
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
        	1024, #size
        	source_bit_rate, #samp_rate
        	"Received packets", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(True)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	1024, #size
        	channel_bit_rate, #samp_rate
        	"Decoded bits", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	1024, #size
        	sound_card_sample_rate/if_decimation, #samp_rate
        	"Frequency synchronizer state", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()
        
        labels = ["Frequency", "Phase", "Error", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	symbol_rate, #samp_rate
        	"Symbol synchronizer state", #name
        	3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["Error", "Rate", "Phase", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sound_card_sample_rate/if_decimation, #bw
        	"Phase synchronized baseband signal", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        
        self.qtgui_sink_x_0_0.enable_rf_freq(False)
        
        
          
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sound_card_sample_rate/if_decimation, #bw
        	"Baseband I&Q signal", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        
        self.qtgui_sink_x_0.enable_rf_freq(False)
        
        
          
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	1024, #size
        	"Synchronized symbols", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(if_decimation, firdes.low_pass(
        	1.66, sound_card_sample_rate, symbol_rate*(1+rolloff), sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(if_decimation, firdes.low_pass(
        	1.66, sound_card_sample_rate, symbol_rate*(1+rolloff), sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.final_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sound_card_sample_rate, #bw
        	"IF received signal", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	False, #plotconst
        )
        self.final_0.set_update_time(1.0/10)
        self._final_0_win = sip.wrapinstance(self.final_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._final_0_win)
        
        self.final_0.enable_rf_freq(False)
        
        
          
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samples_per_symbol, 2*math.pi/100, (variable_rrc_filter_taps), 32, 0, 3, 1)
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(hdlc_packet_length/8, hdlc_packet_length)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(2*math.pi/100*2, 8, True)
        self.blocks_wavfile_source_0 = blocks.wavfile_source("rx_signal.wav", False)
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_tagged_file_sink_0 = blocks.tagged_file_sink(gr.sizeof_char*1, source_bit_rate)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "burst")
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_COS_WAVE, if_frequency, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_SIN_WAVE, if_frequency, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_sink_x_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_file_sink_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_uchar_to_float_0_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_time_sink_x_1, 0))    
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.qtgui_time_sink_x_1_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.final_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_sink_x_0_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 1), (self.qtgui_time_sink_x_0_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_const_sink_x_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 1), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 3), (self.qtgui_time_sink_x_0, 2))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 2), (self.qtgui_time_sink_x_0, 1))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.raspi_decoder_psk_constellation_decoder_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.raspi_decoder_psk_constellation_decoder_0, 0), (self.blocks_uchar_to_float_0, 0))    
        self.connect((self.raspi_decoder_psk_constellation_decoder_0, 0), (self.digital_hdlc_deframer_bp_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "if_psk_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_if_decimation(self):
        return self.if_decimation

    def set_if_decimation(self, if_decimation):
        self.if_decimation = if_decimation
        self.set_samples_per_symbol(16/self.if_decimation)
        self.qtgui_sink_x_0.set_frequency_range(0, self.sound_card_sample_rate/self.if_decimation)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.sound_card_sample_rate/self.if_decimation)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.sound_card_sample_rate/self.if_decimation)

    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)
        self.analog_sig_source_x_0.set_sampling_freq(self.sound_card_sample_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.sound_card_sample_rate)
        self.blocks_throttle_0.set_sample_rate(self.sound_card_sample_rate)
        self.final_0.set_frequency_range(0, self.sound_card_sample_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.sound_card_sample_rate/self.if_decimation)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.sound_card_sample_rate/self.if_decimation)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.sound_card_sample_rate/self.if_decimation)
        self.set_if_frequency(self.sound_card_sample_rate/4)

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
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.symbol_rate)

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.set_channel_bit_rate(self.symbol_rate*self.bits_per_symbol)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))

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

    def get_channel_bit_rate(self):
        return self.channel_bit_rate

    def set_channel_bit_rate(self, channel_bit_rate):
        self.channel_bit_rate = channel_bit_rate
        self.set_source_bit_rate(self.channel_bit_rate*self.hdlc_packet_length/(self.hdlc_packet_overhead+self.hdlc_packet_length))
        self.qtgui_time_sink_x_1.set_samp_rate(self.channel_bit_rate)

    def get_variable_rrc_filter_taps(self):
        return self.variable_rrc_filter_taps

    def set_variable_rrc_filter_taps(self, variable_rrc_filter_taps):
        self.variable_rrc_filter_taps = variable_rrc_filter_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.variable_rrc_filter_taps))

    def get_source_bit_rate(self):
        return self.source_bit_rate

    def set_source_bit_rate(self, source_bit_rate):
        self.source_bit_rate = source_bit_rate
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.source_bit_rate)

    def get_if_frequency(self):
        return self.if_frequency

    def set_if_frequency(self, if_frequency):
        self.if_frequency = if_frequency
        self.analog_sig_source_x_0.set_frequency(self.if_frequency)
        self.analog_sig_source_x_0_0.set_frequency(self.if_frequency)


def main(top_block_cls=if_psk_rx, options=None):

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
