"""
====================
ISA Exploration Demo
====================

This module will create an implementation of ISA-tools to handle
metadata.

Original documentation for ISA-tools can be found on github. [1]_

.. [1] https://github.com/ISA-tools/isa-api/blob/master/isatools/examples/createSimpleISAJSON.py

-----------------------
Defining Custom Classes
-----------------------

First custom child classes of the DataFile class will be created.
These fill out default values for certain types of experiments.
"""

from isatools.model.v1 import *
from isatools.isajson import ISAJSONEncoder
import json


class extractedCSV(DataFile):
    """Class for the extracted data from a plot found within a publication.

    .. TODO: This may be the best place to expand some 'filler' attributes.
             Such as temperature and counter ion, which will probably be
             part of the metadata structure."""

    def __init__(self, filename='',
                 id_='',
                 generated_from=None,
                 comments=None):
        super().__init__(filename=filename,
                         id_=id_,
                         generated_from=generated_from,
                         comments=comments)
        self.label = "Plot-csv-extract"


class spectralImage(DataFile):
    """Child class for an image copy of the plot."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)
        self.label = "Plot-image"


def create_json_metadata():
    """

    Define Investigations

    Currently there is only one *investigation*, this is an abstraction n
    eeded to link the **studies** together.
    """

    Al_inv = Investigation(
        identifier='Al_investigation',
        title='Aluminate Investigation',
        description='Investigation into the properties of aluminate'
    )

    """
    Ontology Sources
    """
    amnt_conc = OntologySource(name='Amount Concentration')
    aluminum = OntologySource(name='Aluminum')
    hydroxide = OntologySource(name='Hydroxide')
    nmr = OntologySource(name='Nuclear Magnetic Resonance')
    raman = OntologySource(name='Raman Spectroscopy')

    """
    Define OntologyAnnotations
    """

    Al_iii = OntologyAnnotation(term='Al(III)', term_source=aluminum)
    NaOH = OntologyAnnotation(term='NaOH', term_source=hydroxide)
    ppm = OntologyAnnotation(term='ppm', term_source=nmr)
    Al_nmr = OntologyAnnotation(term='27 Al NMR', term_source=nmr)
    molarity = OntologyAnnotation(term='Molarity', term_source=amnt_conc)
    raman_peak = OntologyAnnotation(term='cm-1', term_source=raman)
    raman_spectra = OntologyAnnotation(term='raman spectra', term_source=raman)

    # Define the study
    nmr_study = Study(
        identifier='1d_nmr', title='1D NMR Studies',
        description='One dimensional NMR studies')
    raman_study = Study(
        identifier='raman', title='Raman Studies',
        description='Peaks from Raman Spectra')

    # Define the publication
    # TODO: Fix the tab indents here.
    sipos2006 = Publication(
        title='$^{27}\text{Al}$ NMR and Raman spectroscopic studies of alkaline\
               aluminate solutions with extremely high caustic content\
               - Does the octahedral species $\text{Al(OH)}_6^{-3}$ exist in\
               solution?',
        doi="10.1016/j.talanta.2006.02.008")

    # Define the assays
    sipos2006_nmr_assay = Assay(
        measurement_type=ppm,
        technology_type=Al_nmr,
        technology_platform='Bruker',
        units=[ppm, molarity])

    zhou_raman_assay = Assay(
        measurement_type=raman_peak,
        technology_type=raman_spectra,
        technology_platform='Unknown',
        units=[raman_peak, molarity]
    )

    # Create the links to the data files
    sipos2006_fig2_img = spectralImage(filename='data/sipos2006_fig2.png')
    sipos2006_fig2_csv = extractedCSV(filename='data/sipos2006-fig2.csv')

    # sipos2006_fig1_img = 
    sipos2006_fig1_csv = extractedCSV(filename='data/sipos_2006_figure_1.csv')
    sipos2006_tbl2_csv = extractedCSV(filename='data/sipos_2006_table2.csv')
    sipos2006_


    # Create the materials and samples
    al_source = Source(name='Al_source')
    al_sample = Sample(name='Al_sample', derives_from=[al_source])

    # Link the entries together
    Al_inv.studies.append(nmr_study)

    sipos2006_nmr_assay.data_files.append(sipos2006_fig2_img)
    sipos2006_nmr_assay.data_files.append(sipos2006_fig2_csv)

    nmr_study.assays.append(sipos2006_nmr_assay)
    nmr_study.publications.append(sipos2006)
    nmr_study.materials['sources'].append(al_source)

    nmr_metadata = json.dumps(
        Al_inv, cls=ISAJSONEncoder,
        sort_keys=True, indent=4, separators=(',', ': '))

    return nmr_metadata

def main():  # Create the JSON dump
    """
    The Main function!
    """
    nmr_metadata = create_json_metadata()
    print(nmr_metadata)
    """
    Another comment in the main function.
    """

    path = 'data/nmr_metadata.json'
    with open(path, 'w') as f:
        f.write(nmr_metadata)


if __name__ == '__main__':
    main()
