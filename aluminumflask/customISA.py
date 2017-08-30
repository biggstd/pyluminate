"""
=================================
Custom ISA classes for Pyluminate
=================================

This module implements the custom implementation of some
ISA classes.

"""

from isatools.model.v1 import *


class ExtractedCSV(DataFile):

    """

    Class for the extracted data from a plot found within a publication.

    """

    def __init__(self,
                 filename='',
                 id_='',
                 generated_from=None,
                 comments=None):
        super().__init__(filename=filename,
                         id_=id_,
                         generated_from=generated_from,
                         comments=comments)
        self.label = "Plot-csv-extract"

