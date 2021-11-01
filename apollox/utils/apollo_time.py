from typing import Union, Iterable

from astropy.time import Time
from datetime import datetime
import astropy.units as u

APOLLO_LAUNCH_TIME = Time("1971-07-26T13:34:0", scale="utc", format="isot")


def apollo_met_from_utc(utc_time: Time) -> float:

    """
    Convert between an astropy Time in UTC to seconds
    :param utc_time:
    :type utc_time: Time
    :returns:

    """
    return (APOLLO_LAUNCH_TIME - utc_time).to(u.s)


def utc_from_apollo_met(met: float) -> Time:

    """
    Convert from MET (since apollo launch)
    and a Time object in UTC

    :param met:
    :type met: float
    :returns:

    """
    return APOLLO_LAUNCH_TIME + (met * u.s)


class ApolloTime:
    def __init__(self, met: Union[float, Iterable[float]]):

        """
        Creates an apollo time object to easily transform between MET
        seconds and UTC from astropy Time

        :param met:
        :type met: Union[float, Iterable[float]]
        :returns:

        """
        self._utc: Time = utc_from_apollo_met(met)
        self._met: Union[float, Iterable[float]] = met

    @classmethod
    def from_met(cls, met: Union[float, Iterable[float]]):

        return cls(met)

    @classmethod
    def from_utc(cls, utc: Time):

        return cls(apollo_met_from_utc(utc))

    @property
    def utc(self) -> Time:
        return self._utc

    @property
    def met(self) -> Union[float, Iterable[float]]:

        return self._met
