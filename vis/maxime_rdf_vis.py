"""
=======================
Maxime RDF Calculations
=======================
"""

import os
import sys
import pandas as pd
from bokeh.palettes import Category20
from bokeh.models import Select
from bokeh.layouts import row, widgetbox
from bokeh.plotting import curdoc, figure
# Add the parent path so that bokeh --serve can see the `vis`
# module and import it.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vis.utils import read_rdf

# Read the desired metadata file:
# This returns a list of dataframes.
data_frames = read_rdf('metadata.json', char_types=['Aluminate Species'])

# Define colors and sizes to be used later.
SIZES = list(range(6, 22, 3))
COLORS = Category20[20]

# Data wrangling.
ysl = [df['RDF_Al-Ob'] for df in dataframes]
xsl = [df['r'] for df in dataframes]

def create_figure():

    # Assign the x and y values to those selected.
    xs = df[x_sel.value].values
    ys = df[y_sel.value].values

    # Get the titles from those selected.
    x_title = x_sel.value.title()
    y_title = y_sel.value.title()

    # Create a dictionary to pass to the bokeh plot.
    kw = dict()

    # Check if the x and y axis values are discrete.
    # if so use the low level dict key word to set the range appropriately.
    if x_sel.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y_sel.value in discrete:
        kw['y_range'] = sorted(set(ys))

    # Set a default size for the points
    # sz = 9
    # if size.value != 'None':
    #     if size.value in discrete:
    #         sz = [SIZES[xx] for xx in df[size.value].factorize()[0]]
    #     else:
    #         groups = pd.qcut(df[size.value].values, len(SIZES), duplicates='drop')
    #         sz = [SIZES[xx] for xx in groups.codes]
    # Set the default color
    c = '#31AADE'
    if color.value != 'None':
        if color.value in discrete:
            c = [COLORS[xx] for xx in df[color.value].factorize()[0]]
        else:
            groups = pd.qcut(
                df[color.value].values, len(SIZES), duplicates='drop')
            c = [COLORS[xx] for xx in groups.codes]
    # Assign the titles.
    fig = figure(
        plot_height=600,
        plot_width=800,
        tools='pan,box_zoom,reset',
        **kw,
    )
    fig.xaxis.axis_label = x_title
    fig.yaxis.axis_label = y_title
    fig.circle(
        x=xs,
        y=ys,
        color=c,
        # size=sz,
        line_color=None,
        alpha=0.7,
        hover_color='white',
        hover_alpha=0.5,
    )

    return fig


def update(attr, old, new):
    layout.children[1] = create_figure()
    return


# Create the inputs
x_sel = Select(
    title='X-Axis',
    value='r',
    options=columns)
x_sel.on_change('value', update)

y_sel = Select(
    title='Y-Axis',
    value='inter atom distance',
    options=columns)
y_sel.on_change('value', update)

# Create the color input.
color = Select(
    title='Color',
    value='None',
    options=['None'] + discrete + quantileable)
color.on_change('value', update)

# Create the size input
# size = Select(title='Size', value='None', options=['None'] + quantileable)
# size.on_change('value', update)

# Create a list of the controls
controls = widgetbox([x_sel, y_sel, color], width=200)

# Create the layout
layout = row(controls, create_figure())

# Add to the current doc.
curdoc().add_root(layout)
curdoc().title = "Maxime RDF"
