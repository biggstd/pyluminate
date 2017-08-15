
import pandas as pd
import numpy as np
import json
import os
import bokeh

from bokeh.layouts import row, widgetbox
from bokeh.palettes import Spectral5
from bokeh.io import output_notebook, output_file, save
import bokeh.plotting as bk
from bokeh.models import Select
from bokeh.plotting import curdoc, figure

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
                data = pd.read_csv(filename['name'])
                data['doi'] = doi
                dataFrame_list.append(data)
    return pd.concat(dataFrame_list, ignore_index=True)

data = create_dataframes('data/nmr_metadata.json')
data['counter_ion'].factorize()
colormap = {
    'Na+': '#0072B2',
    'Li+': '#56B4E9',
    'K+': '#E69F00',
    'Cs+': '#009E73',
}
data['ion_colors'] = [colormap[x] for x in data['counter_ion']]

SIZES = list(range(6, 22, 3))
COLORS = Spectral5

columns = sorted(data.columns)
discrete = [x for x in columns if data[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(data[x].unique()) > 5]

def create_figure():
    xs = data[x.value].values
    ys = data[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    p = figure(plot_height=600, plot_width=800, tools='pan,box_zoom,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    # if x.value in discrete:
    #     p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        groups = pd.qcut(data[size.value].values, len(SIZES), duplicates='drop')
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        groups = pd.qcut(data[color.value].values, len(COLORS), duplicates='drop')
        c = [COLORS[xx] for xx in groups.codes]

        
    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p

def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='Al_ppm', 
    options=[
        'Al_ppm',
        'OH_concentration',
        'Al_concentration',
        'CI_concentration',
        'wavelength'
        ])
x.on_change('value', update)

y = Select(title='Y-Axis', value='OH_concentration', 
    options=[
        'Al_ppm',
        'Al_concentration',
        'OH_concentration',
        'CI_concentration',
        'wavelength'
        ])
y.on_change('value', update)

size = Select(title='Size', value='Al_concentration', 
    options=['counter_ion', 'Al_ppm'])
size.on_change('value', update)

color = Select(title='Color', value='None', 
    options=['ion_colors', 'Al_ppm'])
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"