import numpy as n

__doc__ =  \
"""

    py_ica performs independent component analysis (ICA), 
    aka "cocktail party problem".

    c implementation of extended infomax by:
	    Sigurd Enghoff & Scott Makeig with contributions
	    from Tony Bell, Te-Won Lee, Tzyy-Ping Jung, Michael
	    Zibulevsky,
    
    wrapping was done by Uwe Schmitt.
    
"""

import _extended_infomax


class ExtendedInfomax(object):

    def __init__(self, maxsteps=None, lrate=None, eps=None, verbose=None):
	""" here you can set parameters different from defaultvalues """

        self.maxsteps= maxsteps
        self.lrate   = lrate
        self.nochange= eps
	self.verbose = verbose

    def run(self, data, nfac=None, weights=None):
	"""
	      Runs Exended Infomax.

	      Input:
	      	 	data    --  signals: one signal per row

			nfac    --  number of factors. 

			            default: data.shape[0], that is
				    number of chanels

                        weights --  initial value for W matrix
				      
	      Output:

	      		act     --  computed activision of components in W

			weights --  computed indepenedent components W
			            that is:  W * act ~ data

			resid   --  average residual:
	"""
	
	# resets all parameters to default values
        _extended_infomax.init_extended_ica() 

        # set parameters different from defaults:
        if self.verbose is not None:
            _extended_infomax.set_verbose(self.verbose)
        if self.maxsteps is not None:
            _extended_infomax.set_maxsteps(self.maxsteps)
        if self.lrate is not None:
            _extended_infomax.set_lrate(self.lrate)
        if self.nochange is not None:
            _extended_infomax.set_nochange(self.nochange)

        nc = data.shape[0]
        if weights is None:
            weights=n.random.random(size=(nc,nc))-.5

	# grant right memory layout:
        weights = n.require(weights, n.double, 'f_contiguous aligned writable')
        data = n.require(data, n.double, 'f_contiguous aligned writable')

        if nfac is None:
            # number of factors is number of chanels
            nfac = nc

	# run extended infomax
        _extended_infomax.run_extended_ica(data, weights, nfac)

	# extract return values
        act = data[:nfac, :]
        weights = weights[:,:nfac]

	# calculate average residual
        avg_resid = n.linalg.norm(n.dot(weights, act)-data) / \
	            (data.shape[0] * data.shape[1])

        return act, weights, avg_resid
