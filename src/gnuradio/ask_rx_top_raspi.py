#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ask Rx Top Raspi
# Generated: Wed Apr 26 23:05:16 2017
##################################################

from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class ask_rx_top_raspi(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Ask Rx Top Raspi")

        ##################################################
        # Variables
        ##################################################
        self.sound_card_sample_rate = sound_card_sample_rate = 44000
        self.samples_per_symbol = samples_per_symbol = 19
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        self.bits_per_symbol = bits_per_symbol = 1
        
        self.variable_rrc_filter_taps = variable_rrc_filter_taps = firdes.root_raised_cosine(1, sound_card_sample_rate, symbol_rate, 0.5, 70)
          
        self.bit_rate = bit_rate = symbol_rate/bits_per_symbol

        ##################################################
        # Blocks
        ##################################################
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_fff(samples_per_symbol, 0.5, (variable_rrc_filter_taps), 32, 0, 1.5, 1)
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(32, 500)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, sound_card_sample_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-0.01, 0.01, 0)
        self.blocks_tagged_file_sink_0 = blocks.tagged_file_sink(gr.sizeof_char*1, bit_rate)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'burst')
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.audio_source_0 = audio.source(sound_card_sample_rate, '', True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.connect((self.audio_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_float_to_char_0, 0), (self.digital_hdlc_deframer_bp_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_file_sink_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_char_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.blocks_threshold_ff_0, 0))    

    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)
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
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.variable_rrc_filter_taps))

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate


def main(top_block_cls=ask_rx_top_raspi, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
