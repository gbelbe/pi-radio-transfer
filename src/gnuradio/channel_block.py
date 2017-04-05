#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Channel Block
# Generated: Wed Apr  5 22:10:22 2017
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
from gnuradio import eng_notation
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
        self.sound_card_sample_rate = sound_card_sample_rate = 96000

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
        self.blocks_wavfile_source_0 = blocks.wavfile_source("tx_signal.wav", False)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("rx_signal.wav", 1, sound_card_sample_rate, 8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((1, ))
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 0.1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_1_2_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_add_xx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "channel_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.blocks_throttle_0.set_sample_rate(self.sound_card_sample_rate)
        self.qtgui_time_sink_x_1_2_0.set_samp_rate(self.sound_card_sample_rate)


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
