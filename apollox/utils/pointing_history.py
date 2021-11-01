from typing import Optional, Iterable

import numpy as np
import scipy.interpolate as interp
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time

from .apollo_time import ApolloTime


class PointingHistory:
    def __init__(
        self, pointing_file: str, t_zero: Optional[Time] = None
    ) -> None:

        pointing_data = np.genfromtxt(pointing_file)

        time = ApolloTime.from_met((pointing_data[:, 0] * u.hour).to(u.s).value)

        # zero the time if needed

        if t_zero is not None:

            trigger_time = ApolloTime.from_utc(t_zero)

            self._time = time - trigger_time.met

        else:

            self._time = time.met

        ra = pointing_data[:, 1]  # in hrs

        dec = pointing_data[:, 2]  # in degs

        # use skycoord to convert to degrees

        tmp = SkyCoord(ra * u.hour, dec * u.deg, frame="icrs")

        self._ra = tmp.ra.deg

        self._dec = tmp.dec.deg

        # create interpolations

        self._ra_time = interp.interp1d(self._time, self._ra)

        self._dec_time = interp.interp1d(self._time, self._dec)

    def ra(self, time) -> np.ndarray:

        return self._ra_time(time)

    def dec(self, time) -> np.ndarray:

        return self._dec_time(time)
