"""

============================
Visualization Helper Scripts
============================

A collection of helper scripts for plotting aluminate data.

"""

import os
import json
import webbrowser
# import numpy as np
import pandas as pd
# import bokeh as bk
# import holoviews as hv


def create_dataframes(json_metadata_path):
    """Construct dataframes with the needed metadata attached."""
    # Read the metadata json file constructed by ISASetup.py
    with open(json_metadata_path, 'r') as md_file:
        metadata = json.load(md_file)
    # create a dataframes for each csv found
    dataframe_list = []
    for study in metadata['studies']:
        # Store the doi/link
        for publication in study['publications']:
            doi = publication['doi']
            # This is buggy, just picks the last one.
            # They should all be the same the way I implemented it.
        for assay in study['assays']:
            for filename in assay['dataFiles']:
                dataframe = pd.read_csv(filename['name'])
                dataframe['doi'] = doi
                dataframe_list.append(dataframe)
    return pd.concat(dataframe_list)


def show_local_html(filename):
    """Specifies a local html file for viewing."""
    file_path = 'file://' + os.path.realpath(filename)
    webbrowser.open(file_path)
    return


def add_missing_columns(dataframe, metadata):
    """
    Adds missing columns based on the metadata given.

    Types of metadata to be converted to columns:

        + DOI / citation
        + Counter Ion
        + Temperature
        + OH_concentration
    """
    pass
