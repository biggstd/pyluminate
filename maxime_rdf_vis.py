"""
=======================
Maxime RDF Calculations
=======================

"""

import pandas as pd
import json
from bokeh.palettes import Category20
from bokeh.models import Select
# from bokeh.layouts import layout
from bokeh.layouts import row, widgetbox
from bokeh.plotting import curdoc, figure


def create_pandas_df(path):
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


def read_maximme_rdf(json_metadata_path, char_types):
    """Construct dataframes with the needed metadata attached."""

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
                    # We found a matching termSource, so get the annotationValue
                    dimer_type = char['characteristicType']['annotationValue']
                    for data_file in assays['dataFiles']:
                        # Create the new dataframe
                        new_data_frame = create_pandas_df(data_file['name'])
                        # Add the desired metadata to the data frame:
                        new_data_frame['dimer'] = dimer_type
                        data_frame_list.append(new_data_frame)
    data_frame =  pd.concat(data_frame_list, ignore_index=True)

    data_frame = data_frame.melt(
        id_vars=["r", 'dimer'],
        value_vars=['RDF_Al-Ob', 'RDF_Al-Oh', 'RCN_Al-Ob', 'RCN_Al-Oh'],
        value_name="inter atom distance",
        var_name="Atom Pair"
    )

    return data_frame


df = read_maximme_rdf('data/nmr_metadata.json', char_types=['Aluminate Species'])


SIZES = list(range(6, 22, 3))
COLORS = Category20[20]


columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(df[x].unique()) > 20]


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
            groups = pd.qcut(df[color.value].values, len(SIZES), duplicates='drop')
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
    fig.line(
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
x_sel = Select(title='X-Axis', value='r', options=columns)
x_sel.on_change('value', update)

y_sel = Select(title='Y-Axis', value='inter atom distance', options=columns)
y_sel.on_change('value', update)

# Create the color input.
color = Select(title='Color', value='None', options=['None'] + discrete + quantileable)
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
