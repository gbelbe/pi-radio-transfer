#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ask Tx Top Raspi
# Generated: Wed Apr 26 23:04:58 2017
##################################################

from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class ask_tx_top_raspi(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Ask Tx Top Raspi")

        ##################################################
        # Variables
        ##################################################
        self.sound_card_sample_rate = sound_card_sample_rate = 44000
        self.samples_per_symbol = samples_per_symbol = 19
        self.symbol_rate = symbol_rate = sound_card_sample_rate/samples_per_symbol
        self.bits_per_symbol = bits_per_symbol = 1
        
        self.variable_rrc_filter_taps = variable_rrc_filter_taps = firdes.root_raised_cosine(15, sound_card_sample_rate, symbol_rate, 0.5, 70)
          
        self.bit_rate = bit_rate = symbol_rate/bits_per_symbol

        ##################################################
        # Blocks
        ##################################################
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(samples_per_symbol, (variable_rrc_filter_taps))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb('packet_len')
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf(([-1,1]), 1)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_char*1, bit_rate,True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 32, "packet_len")
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, './test_src_file.txt', True)
        self.audio_sink_0 = audio.sink(int(sound_card_sample_rate), '', True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_hdlc_framer_pb_0, 'in'))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_1, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.blocks_throttle_1, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))    
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.audio_sink_0, 0))    

    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_symbol_rate(self.sound_card_sample_rate/self.samples_per_symbol)

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
        self.interp_fir_filter_xxx_0.set_taps((self.variable_rrc_filter_taps))

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.blocks_throttle_1.set_sample_rate(self.bit_rate)


def main(top_block_cls=ask_tx_top_raspi, options=None):

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
