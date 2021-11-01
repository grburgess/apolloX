# -*- coding: utf-8 -*-

"""Top-level package for apollox."""

__author__ = """J. Michael Burgess"""
__email__ = "jburgess@mpe.mpg.de"

from .apollo_data import ApolloDetectorData
from .utils import ApolloTime, apollo_met_from_utc, utc_from_apollo_met

from . import _version

__version__ = _version.get_versions()["version"]
