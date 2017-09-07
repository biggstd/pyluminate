"""
===================
RDF Reader Utilites
===================

This module contains helper functions for importing RDF data by
reading a metadata file generated by ISA-tools.
"""

import pandas as pd
import json


def create_pandas_df(path):
    """
    Create a pandas dataframe from a given path. This function is specific
    for the type of RDF data produced by Maxime (and David?).

    It reads the csv, and removes the erroneously created '#' column.
    Although it may be better to use some string manipulation to remove this
    character prior to processing with pandas read_csv function.
    """
    # Read the csv file
    df = pd.read_csv(
        filepath_or_buffer=path,
        index_col=False,
        sep='\s+'  # Split by whitespace
    )

    # Move the columns to deal with the leading hashtag
    df_mod = df[df.columns[:-1]]
    df_mod.columns = df.columns[1:]

    return df_mod


def read_rdf(json_metadata_path, char_types):
    """Construct dataframes with the needed metadata attached.
    Returns a list of pandas dataframe objects.
    """

    # Open the file.
    with open(json_metadata_path, 'r') as f:
        metadata = json.load(f)

    # Create an empty list to append the paths to.
    data_frame_list = []

    # Iterate through the studies.
    for studies in metadata['studies']:
        for assays in studies['assays']:
            for char in assays['characteristicCategories']:
                if char['characteristicType']['termSource'] in char_types:
                    # We found a matching termSource, get the annotationValue
                    dimer_type = char['characteristicType']['annotationValue']
                    for data_file in assays['dataFiles']:
                        # Create the new dataframe
                        new_data_frame = create_pandas_df(data_file['name'])
                        # Add the desired metadata to the data frame:
                        new_data_frame['dimer'] = dimer_type
                        data_frame_list.append(new_data_frame)

    # data_frame = pd.concat(data_frame_list, ignore_index=True)

    # Drop RCN_Al-Ob   RCN_Al-Oh columns for now.
    # data_frame.drop('RCN_Al-Ob', 1, inplace=True)
    # data_frame.drop('RCN_Al-Oh', 1, inplace=True)

    # data_frame = data_frame.melt(
    #     id_vars=["r", 'dimer'],
    #     value_vars=['RDF_Al-Ob', 'RDF_Al-Oh'],
    #     value_name="inter atom distance",
    #     var_name="Atom Pair"
    # )

    return data_frame_list
