import pandas as pd
import json

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Select
from bokeh.layouts import layout, widgetbox
from bokeh.io import curdoc


def create_dataframes(json_metadata_path):
    """Construct dataframes with the needed metadata attached."""
    # Read the metadata json file constructed by ISASetup.py
    with open(json_metadata_path, 'r') as f:
        metadata = json.load(f)
    # create a dataframes for each csv found
    data_frame_list = []
    for study in metadata['studies']:
        # Store the doi/link
        for publication in study['publications']:
            doi = publication['doi']
        for assay in study['assays']:
            for filename in assay['dataFiles']:
                data = pd.read_csv(filename['name'])
                data['doi'] = doi
                data_frame_list.append(data)
    return pd.concat(data_frame_list, ignore_index=True)


al_data_frame = create_dataframes('data/nmr_metadata.json')
al_data_frame["counter_ion"].factorize()

# Create an empty column data source to be used by the plot.
source = ColumnDataSource(
    data=dict(
        x=[],
        y=[],
        doi=[],
    )
)

axis_map = {
    "Al_concentration": "Al Concentration",
    "OH_concentration": "OH Concentration",
    "wavelength": "Raman Peak Position cm-1",
    "counter_ion": "Counter Ion",
    "temperature": "Degrees Celsisus",
    "Al_ppm": "Al 27 ppm",
}

x_axis = Select(
    title="X Axis Selection",
    options=axis_map.keys(),
    value="Al Concentration"
)

x_axis.on_change('value', update)

y_axis = Select(
    title="Y Axis Selection",
    options=axis_map.keys(),
    value="Al 27 ppm"
)

hover = HoverTool(
    tooltips=[
        ("Aluminum Concentration", "@Al_concentration"),
        ("DOI", "@doi"),
    ]
)

plot = figure(
    plot_heigth=600,
    title="",
    toolbar_location=None,
    tools=[hover],
)

plot.circle(
    x="x",
    y="y",
    source=source,
    size=7,
)

def update():
    df = al_data_frame
    y_name = df[x_axis.value].values
    x_name = df[y_axis.value].values
    plot.title.text = "{} points selected.".format(len(df))
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        doi=df["doi"],
    )

controls = [x_axis, y_axis]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'

desc = Div(text="This is only a test.")

inputs = widgetbox(*controls, sizing_mode=sizing_mode,)

my_layout = layout([
    [desc],
    [inputs, plot],
], sizing_mode=sizing_mode)

update()

curdoc().add_root(my_layout)
curdoc().title = "Al Viewer"
