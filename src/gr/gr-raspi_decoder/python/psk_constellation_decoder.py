#!/usr/bin/env python
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

##################
# LIBRARIES USED #
##################

#GNURadio specific libs
from gnuradio import gr
from gnuradio import blocks
from gnuradio.digital import digital_swig
from gnuradio.digital import modulation_utils
from gnuradio.digital.utils import mod_codes, gray_code

#Generic python libs
from math import pi, log
from cmath import exp


#########################
# DEFAULT CONFIGURATION #
#########################

# Default number of points in constellation and associated bits per symbol.
_def_bits_per_symbol = 2
_def_constellation_points = pow(2,_def_bits_per_symbol)
# Default symbols mapping
_def_mod_code = mod_codes.GRAY_CODE
# Default use of differential encoding
_def_differential = True


#############
# FUNCTIONS #
#############

#NB: COPIED FROM psk.py
#TODO: INCLUDE psk class for direct use of these functions / maintenability purposes

#Bits encoding
def create_encodings(mod_code, arity, differential):
    post_diff_code = None
    if mod_code not in mod_codes.codes:
        raise ValueError('That modulation code does not exist.')
    if mod_code == mod_codes.GRAY_CODE:
        if differential:
            pre_diff_code = gray_code.gray_code(arity)
            post_diff_code = None
        else:
            pre_diff_code = []
            post_diff_code = gray_code.gray_code(arity)
    elif mod_code == mod_codes.NO_CODE:
        pre_diff_code = []
        post_diff_code = None
    else:
        raise ValueError('That modulation code is not implemented for this constellation.')
    return (pre_diff_code, post_diff_code)
    
#Constellation generation
def psk_constellation(m=_def_constellation_points, mod_code=_def_mod_code,
                      differential=_def_differential):
    """
    Creates a PSK constellation object.
    """
    k = log(m) / log(2.0)
    if (k != int(k)):
        raise StandardError('Number of constellation points must be a power of two.')
    points = [exp(2*pi*(0+1j)*i/m) for i in range(0,m)]
    pre_diff_code, post_diff_code = create_encodings(mod_code, m, differential)
    if post_diff_code is not None:
        inverse_post_diff_code = mod_codes.invert_code(post_diff_code)
        points = [points[x] for x in inverse_post_diff_code]
    constellation = digital_swig.constellation_psk(points, pre_diff_code, m)
    return constellation


#######################################
# PSK constellation demodulator class #
#######################################

#The object inherits from hier_block2 for generic GNURadio methods
class psk_constellation_decoder(gr.hier_block2):
    """
    PSK constellation decoder block.
    """

###########
# Methods #
###########
    
    #PSK constellation demodulator constructor
    def __init__(self,
        bits_per_symbol=_def_bits_per_symbol,
        differential=_def_differential,
        mod_code=_def_mod_code,
        debug=False):
        #GNURadio constructor
        gr.hier_block2.__init__(self,
                "psk_constellation_demod",
				gr.io_signature(1, 1, gr.sizeof_gr_complex),
				gr.io_signature(1, 1, gr.sizeof_char))
        
        #Init internal attributes and basic building blocks
        self._bits_per_symbol = bits_per_symbol
        self._constellation_points = pow(2,bits_per_symbol)
        self._constellation = psk_constellation(self._constellation_points, mod_code, differential)
        self._constellation_decoder = digital_swig.constellation_decoder_cb(
            self._constellation.base())
        self._differential = differential
        self._mod_code = mod_code
        self._pre_diff_code = self._constellation.apply_pre_diff_code()
        if self._differential:
            self._diffdec = digital_swig.diff_decoder_bb(self._constellation_points)
        if self._pre_diff_code:
            self._symbol_mapper = digital_swig.map_bb(mod_codes.invert_code(self._constellation.pre_diff_code()))

        # unpack the k bit vector into a stream of bits
        self.unpack = blocks.unpack_k_bits_bb(self.bits_per_symbol())

        # Connect and Initialize base class
        self._blocks = [self, self._constellation_decoder]
        if self._differential:
            self._blocks.append(self._diffdec)
        if self._pre_diff_code:
            self._blocks.append(self._symbol_mapper)
        self._blocks += [self.unpack, self]
        if debug:
            self.debug_internal_state()
        self.connect(*self._blocks)

    def bits_per_symbol(self):   # staticmethod that's also callable on an instance
        return self._constellation.bits_per_symbol()

    #Debug internal state
    def debug_internal_state(self):
        print "Decoder configuration:"
        print "Constellation points:  %d"   % self._constellation_points
        if self._differential:
            print "Differential decoder enabled"
        else:
            print "Differential decoder disabled"
#        print "\nMapping:  %b"   % self.symbol_mapper

