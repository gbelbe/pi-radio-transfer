#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Channel Block
# Generated: Sat Apr 29 19:27:06 2017
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
from gnuradio import channels
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys


class channel_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Channel Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Channel Block")
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

        self.settings = Qt.QSettings("GNU Radio", "channel_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.sound_card_sample_rate = sound_card_sample_rate = 22000
        self.samples_per_symbol = samples_per_symbol = 16
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        self.rx_frequency_error = rx_frequency_error = 100
        self.quantization_depth = quantization_depth = 16
        self.if_frequency = if_frequency = sound_card_sample_rate/4

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_1_2_0 = qtgui.time_sink_f(
        	500, #size
        	sound_card_sample_rate, #samp_rate
        	"Received signal", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1_2_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_2_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1_2_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1_2_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_1_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_2_0.enable_autoscale(True)
        self.qtgui_time_sink_x_1_2_0.enable_grid(False)
        self.qtgui_time_sink_x_1_2_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1_2_0.disable_legend()
        
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
                self.qtgui_time_sink_x_1_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_2_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_2_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_2_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1.66, sound_card_sample_rate, sound_card_sample_rate/4, sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1.66, sound_card_sample_rate, sound_card_sample_rate/4, sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.final = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sound_card_sample_rate, #bw
        	"Distorted baseband signal", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.final.set_update_time(1.0/10)
        self._final_win = sip.wrapinstance(self.final.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._final_win)
        
        self.final.enable_rf_freq(False)
        
        
          
        self.channels_fading_model_0 = channels.fading_model( 16, 0, False, 4.0, 0 )
        self.blocks_wavfile_source_0 = blocks.wavfile_source("tx_signal.wav", False)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("rx_signal.wav", 1, sound_card_sample_rate, quantization_depth)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_multiply_xx_0_0_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0_1 = analog.sig_source_f(sound_card_sample_rate, analog.GR_SIN_WAVE, if_frequency+rx_frequency_error, 1, 0)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_COS_WAVE, if_frequency+rx_frequency_error, 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_COS_WAVE, if_frequency, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_SIN_WAVE, if_frequency, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_0_1, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0_0_0, 1))    
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_0_0_1, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.channels_fading_model_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0_1, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_1_2_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.channels_fading_model_0, 0), (self.blocks_complex_to_float_0, 0))    
        self.connect((self.channels_fading_model_0, 0), (self.final, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "channel_block")
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
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.sound_card_sample_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.sound_card_sample_rate)
        self.blocks_throttle_0.set_sample_rate(self.sound_card_sample_rate)
        self.final.set_frequency_range(0, self.sound_card_sample_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.sound_card_sample_rate/4, self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.sound_card_sample_rate/4, self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.qtgui_time_sink_x_1_2_0.set_samp_rate(self.sound_card_sample_rate)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_rx_frequency_error(self):
        return self.rx_frequency_error

    def set_rx_frequency_error(self, rx_frequency_error):
        self.rx_frequency_error = rx_frequency_error
        self.analog_sig_source_x_0_0_0.set_frequency(self.if_frequency+self.rx_frequency_error)
        self.analog_sig_source_x_0_1.set_frequency(self.if_frequency+self.rx_frequency_error)

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
        self.analog_sig_source_x_0_0_0.set_frequency(self.if_frequency+self.rx_frequency_error)
        self.analog_sig_source_x_0_1.set_frequency(self.if_frequency+self.rx_frequency_error)


def main(top_block_cls=channel_block, options=None):

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
