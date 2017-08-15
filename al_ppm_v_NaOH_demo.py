import pandas as pd
import numpy as np
import json
import os
import bokeh
from bokeh.io import output_notebook, output_file
import bokeh.plotting as bk


def create_dataframes(json_metadata_path):
    """Construct dataframes with the needed metadata attached."""
    # Read the metadata json file constructed by ISASetup.py
    with open(json_metadata_path, 'r') as f:
        metadata = json.load(f)
    # create a dataframes for each csv found
    dataFrame_list = []
    for study in metadata['studies']:
        # Store the doi/link
        for publication in study['publications']:
            doi = publication['doi']
        for assay in study['assays']:
            for filename in assay['dataFiles']:
                df = pd.read_csv(filename['name'])
                df['doi'] = doi
                dataFrame_list.append(df)
    return pd.concat(dataFrame_list, ignore_index=True)


data = create_dataframes('data/nmr_metadata.json')

fig = bk.figure(title='Al ppm v. [NaOH]')
fig.xaxis.axis_label = '[NaOH]'
fig.yaxis.axis_label = '27 Al ppm'
fig.scatter(data['OH_concentration'], data['Al_ppm'])
# bk.show(fig)
output_file("al_ppm_v_NaOH_demo.png")

