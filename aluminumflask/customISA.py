"""
=================================
Custom ISA classes for Pyluminate
=================================

This module implements the custom implementation of some
ISA classes.

"""

from isatools.model.v1 import \
    DataFile, OntologySource, Investigation


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


class amount_concentration(OntologySource):
    """
    Define custom ontology sources for Pyluminate.
    """
    name = 'Amount Concentration'





class new_ontology_source():
    pass


def new_ontology_annotation(ontology_source):
    pass


def assign_sample():
    pass


def assign_source():
    pass


def new_publication():
    pass


def new_study():
    pass


def new_assay():
    pass


def generate_json():
    pass
