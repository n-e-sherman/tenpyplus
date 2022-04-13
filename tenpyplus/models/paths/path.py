
from tenpyplus.infrastructure import Object
import numpy as np

def make_ramp(ramp='linear', v=1.0, dt=0.1):

    if ramp == 'linear':
        ti = -1.0 / v
        ts = np.array(list(np.arange(-1.0 / v, 0, dt)) + [0])
        return ts, make_linear_ramp(v)
    elif ramp == 'smooth':
        ts = np.array(list(np.arange(-1.5 / v, 0, dt)) + [0])
        return ts, make_smooth_ramp(v)
    else:
        raise NotImplementedError('ramp choice ' + ramp + ' not implemented.')
        np.array(list(np.arange(self.ti + self.dt, 0, self.dt)) + [0])

def make_linear_ramp(v):

    def linear_ramp(t):
        return v*t

    return linear_ramp

def make_smooth_ramp(v):

    def smooth_ramp(t):
        return v*t - ( (4.0) / (27.0) ) * (v*t)**3
    return smooth_ramp

class DirectPath(Object):

    def __init__(self, **data):

        super().__init__(**data)
        self.ts, self.eps = make_ramp(ramp=self.ramp, v=self.v, dt=self.dt)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'ramp': data.get('ramp','linear'), 
                           'v': data.get('v',1.0), 
                           'dt': data.get('dt', 0.1)})
        
    def make_function(self, p0, pf):

        def f(t):
            return -1.0 * p0 * self.eps(t) + (1.0 + self.eps(t)) * pf
        return f

    @property
    def mongo_type(self):
        from ._data import MongoDirectPath
        return MongoDirectPath

    @property
    def t0(self):
        return np.min(self.ts)

    @property
    def tf(self):
        return np.max(self.ts)
    
    
class SymmetricPath(DirectPath):

    def __init__(self, **data):
        super().__init__(**data)
        self.ts = np.array(list(self.ts) + list(abs(self.ts[::-1]))[1:])

    def make_function(self, p0, pf):

        def f(t):
            return ( -1.0 * p0 * self.eps(t) ) + ( (1.0 + self.eps(t)) * (0.5*(pf + p0)) )
        return f

    @property
    def mongo_type(self):
        from ._data import MongoSymmetricPath
        return MongoSymmetricPath







