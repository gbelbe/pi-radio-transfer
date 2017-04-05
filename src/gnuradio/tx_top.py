#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Top
# Generated: Wed Apr  5 22:02:03 2017
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
from gnuradio import filter
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
        self.sound_card_sample_rate = sound_card_sample_rate = 96000
        self.samples_per_symbol = samples_per_symbol = 19
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        
        self.variable_rrc_filter_taps = variable_rrc_filter_taps = firdes.root_raised_cosine(15, sound_card_sample_rate, symbol_rate, 0.5, 70)
          
        self.bits_per_symbol = bits_per_symbol = 1

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	500, #size
        	sound_card_sample_rate, #samp_rate
        	"Baseband TX signal", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
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
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(samples_per_symbol, (variable_rrc_filter_taps))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb("packet_len")
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf(([-1,1]), 1)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("tx_signal.wav", 1, sound_card_sample_rate, 8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 32, "packet_len")
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "./pi-radio-transfer/src/gnuradio/test_src_file.txt", True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_hdlc_framer_pb_0, 'in'))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))    
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_wavfile_sink_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_top")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)
        self.qtgui_time_sink_x_0.set_samp_rate(self.sound_card_sample_rate)
        self.blocks_throttle_0.set_sample_rate(self.sound_card_sample_rate)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_variable_rrc_filter_taps(self):
        return self.variable_rrc_filter_taps

    def set_variable_rrc_filter_taps(self, variable_rrc_filter_taps):
        self.variable_rrc_filter_taps = variable_rrc_filter_taps
        self.interp_fir_filter_xxx_0.set_taps((self.variable_rrc_filter_taps))

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
