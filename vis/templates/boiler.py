"""
===========================================
Boiler Plate for IDREAM Bokeh Visualization
===========================================
"""

import os
import sys
import collections
# Bokeh imports
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox, row, column
from bokeh.client import push_session
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import MultiSelect, CheckboxGroup, Div
from bokeh.palettes import linear_palette, viridis
from bokeh.io import curdoc
# Local, relative module imports
sys.path.append(os.getcwd())
from vis.utils import read_rdf


METADATA_PATH = os.path.join(os.getcwd(), 'metadata.json')
DATA_FRAMES = read_rdf(METADATA_PATH, char_types=['Aluminate Species'])


ACTIVE_DATA = collections.defaultdict(list)

for dataframe in DATA_FRAMES:
	al_cmpd = dataframe.characteristics['Aluminate Species']
	ACTIVE_DATA[al_cmpd].extend(al_cmpd)


# Create a bokeh data source for interactivity
SEL_DATA_FRAMES = ColumnDataSource(data=ACTIVE_DATA)

# Since we can se all the bonds and species at this point, we can build
# the input lists options. First create an empty dictionary. A collections
# defaultdict is used to ensure uncreated values are always lists.
available_cmpds_dict = collections.defaultdict(list)
for frame in dataframes:
    # Set the new, aluminate species key
    aluminate_cmpnd = frame.characteristics['Aluminate Species'][0]
    # Add (extend) these new lists of bonds to the current list.
    available_cmpds_dict[aluminate_cmpnd].extend(
        frame.characteristics['Inter-atom distances'])

