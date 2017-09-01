"""
===========
ISA Backend
===========
"""

from isatools.model.v1 import *
from isatools.isajson import ISAJSONEncoder
import json
import logging


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


class MaximeRDF(DataFile):
    """Class for the data from Maxime."""

    def __init__(self, filename='',
                 id_='',
                 generated_from=None,
                 comments=None):
        super().__init__(filename=filename,
                         id_=id_,
                         generated_from=generated_from,
                         comments=comments)
        self.label = "Maxime-RDF"


class MaximeVib(DataFile):
    """Class for the data from Maxime.
"""
    def __init__(self, filename='',
                 id_='',
                 generated_from=None,
                 comments=None):
        super().__init__(filename=filename,
                         id_=id_,
                         generated_from=generated_from,
                         comments=comments)
        self.label = "Maxime Vibrational Spectrum"


def create_metadata():
    """
    Returns an ISA-JSON object.

    :return:
    """

    """
    Ontology Sources
    """
    amnt_conc = OntologySource(name='Amount Concentration')
    # aluminum = OntologySource(name='Aluminum')
    # hydroxide = OntologySource(name='Hydroxide')
    nmr = OntologySource(name='Nuclear Magnetic Resonance')
    raman = OntologySource(name='Raman Spectroscopy')
    simulation = OntologySource(name="Simulated Data")

    """
    Ontology Annotations
    """
    ppm = OntologyAnnotation(term='ppm', term_source=nmr)
    Al_nmr = OntologyAnnotation(term='27 Al NMR', term_source=nmr)
    molarity = OntologyAnnotation(term='Molarity', term_source=amnt_conc)
    raman_peak = OntologyAnnotation(term='cm-1', term_source=raman)
    raman_spectra = OntologyAnnotation(term='raman spectra', term_source=raman)
    simulated_rdf = OntologyAnnotation(term='Simulated RDF', term_source=simulation)
    simulated_vibrational_spectra = OntologyAnnotation(
        term='Simulated vibrational spectrum',
        term_source=simulation)

    """
    Sipos 2006 Publication.
    """
    sipos_2006_pub = Publication(
        title=(
            '$^{27}\\text{Al}$ NMR and Raman spectroscopic studies of '
            'alkaline aluminate solutions with extremely high caustic '
            'content - Does the octahedral species $\\text{Al(OH)}_6^{-3}$ '
            'exist in solution?'),
        doi="10.1016/j.talanta.2006.02.008"
    )

    sipos2006_nmr_assay = Assay(
        measurement_type=ppm,
        technology_type=Al_nmr,
        technology_platform='Bruker',
        units=[ppm, molarity],
        data_files=[
            extractedCSV(filename='data/sipos2006-fig2.csv'),
            extractedCSV(filename='data/sipos_2006_table1_nmr.csv'),
            extractedCSV(filename='data/sipos_2006_table2.csv'),
            extractedCSV(filename='data/sipos_2006_fig3.csv'),
        ]
    )

    sipos2006_raman_assay = Assay(
        measurement_type=raman_peak,
        technology_type=raman_spectra,
        technology_platform='Unknown',
        units=[raman_peak, molarity],
        data_files=[
            extractedCSV(filename='data/sipos_2006_figure_1.csv'),
            extractedCSV(filename='data/sipos_2006_table1_raman.csv'),
        ]
    )

    sipos2006_raman_study = Study(
        identifier='raman',
        title='Raman Studies',
        description='Peaks from Raman Spectra',
        publications=[sipos_2006_pub],
        assays=[sipos2006_raman_assay],
    )

    sipos2006_nmr_study = Study(
        identifier='1d_nmr',
        title='1D NMR Studies',
        description='One dimensional NMR studies',
        publications=[sipos_2006_pub],
        assays=[sipos2006_nmr_assay]
    )



    """Zhou Publication"""
    zhou_thesis = Publication(
        title=(
            'Raman studies on the aluminate and carbonate '
            'anions in aqueous solutions.'),
        doi=(
            'http://collections.mun.ca/cdm/compoundobject/'
            'collection/theses2/id/222115/rec/6')
    )

    zhou_raman_assay = Assay(
        measurement_type=raman_peak,
        technology_type=raman_spectra,
        technology_platform='Unknown',
        units=[raman_peak, molarity],
        data_files=[
            extractedCSV(filename='data/zhou_thesis.csv')
        ]
    )

    zhou_raman_study = Study(
        identifier='Raman',
        title='Zhou Raman studies',
        description='Peaks from Raman Spectra',
        publications=[zhou_thesis],
        assays=[zhou_raman_assay]

    )

    #######################
    ## MAXIME
    #######################


    maxime_vib_assay = Assay(
        measurement_type=raman_peak,
        technology_type=raman_spectra,
        technology_platform='Unknown',
        units=[raman_peak, molarity],
        data_files=[
            MaximeVib(filename='data/d1.AlO.PWS'),
            MaximeVib(filename='data/d1.el.PWS'),

            MaximeVib(filename='data/d2.AlO.PWS'),
            MaximeVib(filename='data/d2.el.PWS'),

            MaximeVib(filename='data/d3.AlO.PWS'),
            MaximeVib(filename='data/d3.el.PWS'),

            MaximeVib(filename='data/d4.AlO.PWS'),
            MaximeVib(filename='data/d4.el.PWS'),

        ]
    )


    maxime_vibrational_dimer_study = Study(
        identifier="maxime_vibrational_dimer_study",
        title="Explore various aluminate dimers.",
        description=(
            "In the PWS files the vibrational power spectra are obtained from "
            "the atomic velocity autocorrelation function (VACF). These are the "
            "vibrational spectra you would obtain if you didn’t have any "
            "selection rule, so essentially you get all the possible bands "
            "with the correct frequencies but the intensities are not directly "
            "related to the IR or Raman ones. Still, you can definitely extract "
            "the frequencies corresponding to the most intense bands as you will "
            "very likely find those in the IR and/or Raman spectra."
        ),
        assays=[maxime_vib_assay]
    )

    ## MAXIME RDF ASSAY

    maxime_rdf_assay = Assay(
        measurement_type=raman_peak,
        technology_type=raman_spectra,
        technology_platform='Unknown',
        units=[raman_peak, molarity],
        characteristic_categories=[simulated_rdf],
        data_files=[
            MaximeRDF(filename='data/d1.rdf'),
            MaximeRDF(filename='data/d2.rdf'),
            MaximeRDF(filename='data/d3.rdf'),
            MaximeRDF(filename='data/d4.rdf'),
        ]
    )


    maxime_rdf_study = Study(
        identifier="maxime_rdf_study",
        title="Explore various aluminate dimers.",
        description=(
            "RDFs are obtained from the atomic positions. "
            "1st column: r (distance with respect to the 1st"
            " atom of the pair type) in angstroms."
            " The following columns are the RDFs for different "
            "pair types (i.e. ‘Al-O’) mentioned in the header, "
            "and finally the columns correspond to the running "
            "coordination numbers for these same pair types."
        ),
        assays=[maxime_rdf_assay]
    )

    ###########################################################################
    """Create the overall investigation."""
    Al_inv = Investigation(
        identifier='Al_investigation',
        title='Aluminate Investigation',
        description='Investigation into the properties of aluminate',
        studies=[
            sipos2006_raman_study,
            sipos2006_nmr_study,
            zhou_raman_study,
            maxime_rdf_study,
            maxime_vibrational_dimer_study,
        ]
    )

    """
    Create the metadata json entry.
    """
    metadata_json = json.dumps(
        Al_inv,
        cls=ISAJSONEncoder,
        sort_keys=True,
        indent=4,
        separators=(',', ':')
    )

    return metadata_json


def main():
    """Writes the aluminate json entry to a specified folder."""
    nmr_metadata = create_metadata()
    logging.info(nmr_metadata)
    path = '../data/nmr_metadata.json'
    with open(path, 'w') as f:
        f.write(nmr_metadata)

if __name__ == '__main__':
    main()
