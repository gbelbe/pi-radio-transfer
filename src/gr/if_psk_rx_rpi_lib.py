#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: If Psk Rx Rpi
# Description: IF PSK RX for Raspeberry (headless)
# Generated: Sat Apr 29 20:39:38 2017
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import math
import raspi_decoder


class if_psk_rx_rpi(gr.top_block):

    def __init__(self, bits_per_symbol=2, rolloff=0.5, sound_card_sample_rate=22000):
        gr.top_block.__init__(self, "If Psk Rx Rpi")

#TODO: CHECK BOUNDARIES OF INPUT PARAMETERS

        ##################################################
        # Variables
        ##################################################
        self.if_decimation = if_decimation = 2
        self.sound_card_sample_rate = sound_card_sample_rate
        self.samples_per_symbol = samples_per_symbol = 16/if_decimation
        self.symbol_rate = symbol_rate = sound_card_sample_rate/if_decimation/samples_per_symbol
        self.bits_per_symbol = bits_per_symbol
        self.rolloff = rolloff
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
        self.low_pass_filter_0_0 = filter.fir_filter_fff(if_decimation, firdes.low_pass(
        	1.66, sound_card_sample_rate, symbol_rate*(1+rolloff), sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(if_decimation, firdes.low_pass(
        	1.66, sound_card_sample_rate, symbol_rate*(1+rolloff), sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samples_per_symbol, 2*math.pi/100, (variable_rrc_filter_taps), 32, 0, 3, 1)
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(hdlc_packet_length/8, hdlc_packet_length)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(2*math.pi/100*2, 8, True)
        self.blocks_tagged_file_sink_0 = blocks.tagged_file_sink(gr.sizeof_char*1, source_bit_rate)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "burst")
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.audio_source_0 = audio.source(sound_card_sample_rate, "", True)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_COS_WAVE, if_frequency, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(sound_card_sample_rate, analog.GR_SIN_WAVE, if_frequency, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_file_sink_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.raspi_decoder_psk_constellation_decoder_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.raspi_decoder_psk_constellation_decoder_0, 0), (self.digital_hdlc_deframer_bp_0, 0))    

    def get_if_decimation(self):
        return self.if_decimation

    def set_if_decimation(self, if_decimation):
        self.if_decimation = if_decimation
        self.set_samples_per_symbol(16/self.if_decimation)
        self.set_symbol_rate(self.sound_card_sample_rate/self.if_decimation/self.samples_per_symbol)

    def get_sound_card_sample_rate(self):
        return self.sound_card_sample_rate

    def set_sound_card_sample_rate(self, sound_card_sample_rate):
        self.sound_card_sample_rate = sound_card_sample_rate
        self.set_if_frequency(self.sound_card_sample_rate/4)
        self.analog_sig_source_x_0.set_sampling_freq(self.sound_card_sample_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.sound_card_sample_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.set_symbol_rate(self.sound_card_sample_rate/self.if_decimation/self.samples_per_symbol)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_symbol_rate(self.sound_card_sample_rate/self.if_decimation/self.samples_per_symbol)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_channel_bit_rate(self.symbol_rate*self.bits_per_symbol)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1.66, self.sound_card_sample_rate, self.symbol_rate*(1+self.rolloff), self.sound_card_sample_rate/8, firdes.WIN_HANN, 6.76))

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

    def get_variable_rrc_filter_taps(self):
        return self.variable_rrc_filter_taps

    def set_variable_rrc_filter_taps(self, variable_rrc_filter_taps):
        self.variable_rrc_filter_taps = variable_rrc_filter_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.variable_rrc_filter_taps))

    def get_source_bit_rate(self):
        return self.source_bit_rate

    def set_source_bit_rate(self, source_bit_rate):
        self.source_bit_rate = source_bit_rate

    def get_if_frequency(self):
        return self.if_frequency

    def set_if_frequency(self, if_frequency):
        self.if_frequency = if_frequency
        self.analog_sig_source_x_0.set_frequency(self.if_frequency)
        self.analog_sig_source_x_0_0.set_frequency(self.if_frequency)


def main(top_block_cls=if_psk_rx_rpi, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
