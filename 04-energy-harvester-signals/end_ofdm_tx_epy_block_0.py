"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, vlen=32, interpolation=32):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Random phase generator',   # will show up in GRC
            in_sig=[],
            out_sig=[(np.complex64, vlen*interpolation)]
        )
        self.vlen = vlen

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        size = len(output_items[0])
        # output_items[0][:] = np.zeros(output_items[0].shape,dtype=np.complex64)
        output_items[0][:, :self.vlen] = np.exp(1j *np.random.uniform(0, 2*np.pi, (size,self.vlen)))
        output_items[0][:, 0] = 0 
        return size
