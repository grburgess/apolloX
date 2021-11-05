import pandas as pd
import numpy as np
from typing import Optional


from astropy.time import Time
from datetime import datetime
import astropy.units as u
from threeML.utils.spectrum.binned_spectrum_set import BinnedSpectrumSet
from threeML.utils.spectrum.binned_spectrum import BinnedSpectrumWithDispersion
from threeML.utils.OGIP.response import InstrumentResponse
from threeML.utils.time_interval import TimeIntervalSet


from .utils import ApolloTime


class ApolloDetectorData:
    def __init__(
        self,
        file_name: str,
        instrument: str,
        response: InstrumentResponse,
        t_zero: Optional[Time] = None,
    ):

        """
        Reads in and processes data from the
        .dat files of Apollo


        :param file_name:
        :type file_name: str
        :param instrument:
        :type instrument: str
        :param response:
        :type response: InstrumentResponse
        :param t_zero:
        :type t_zero: Optional[Time]
        :returns:

        """
        data = np.genfromtxt(file_name)

        self._time = ApolloTime.from_met((data[:, 0] * u.hour).to(u.s).value)

        if t_zero is not None:

            trigger_time = ApolloTime.from_utc(t_zero)

            self._relative_time: np.ndarray = self._time.met - trigger_time.met

        else:

            self._relative_time = self._time.met

        self._tstart = self._relative_time - 4
        self._tstop = self._relative_time + 4

        self._counts = data[:, 1:]

        list_of_binned_spectra = []

        for start, stop, counts in zip(self._tstart, self._tstop, self._counts):

            exposure = stop - start

            tmp = BinnedSpectrumWithDispersion(
                counts,
                exposure,
                response,
                mission="Apollo",
                instrument=instrument,
                tstart=start,
                tstop=stop,
                is_poisson=True,
            )

            list_of_binned_spectra.append(tmp)

        time_intervals = TimeIntervalSet.from_starts_and_stops(
            self._tstart, self._tstop
        )

        self._data: BinnedSpectrumSet = BinnedSpectrumSet(
            list_of_binned_spectra, time_intervals=time_intervals
        )

    @property
    def binned_data(self) -> BinnedSpectrumWithDispersion:

        return self._data
