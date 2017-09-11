"""
=============================
RDF Visualization Application
=============================

This application will create an interactive Bokeh application.
"""

# Basic imports
import os
import sys
import collections
# Bokeh imports
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import MultiSelect, CheckboxGroup, Div
from bokeh.palettes import Category20
from bokeh.io import curdoc
# Local, relative module imports
sys.path.append(os.getcwd())
from vis.utils import read_rdf

# Create the static HTML divs.
app_intro_div = Div(
    text=open(os.path.join(
        os.path.dirname(__file__),
        "templates",
        "rdf_title.html")).read(), width=800
)

# From the metadata, load the desired data into pandas dataframes.
# Each dataframe has an attribute attached by the read_rdf function.
# This characteristics attribute is a dictioary of values. The entires
# for 'Inter-atom distances' are the bonds within that dataframe.
metadata_path = os.path.join(os.getcwd(), 'metadata.json')
dataframes = read_rdf(metadata_path, char_types=['Aluminate Species'])

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

# From these characteristics, generate a ColumnDataSource for the dynamic
# inputs to use.
input_src = ColumnDataSource(data=available_cmpds_dict)

"""
# CONTROLS
Define the Controls (for variable name use in the functions below.)
These need to be added to the controls list at the bottom of the file.
"""

compound_sel = MultiSelect(
    title="Compound",
    options=list(input_src.data.keys()),
    value=[list(input_src.data.keys())[0]]
)

bonds_grp = CheckboxGroup(
    # labels=[],  # field is filled out by the update() function.
    # bonds_grp.active gives the index list of those items selected.
)


def select_RDFs():
    """
    Examines the input(s) and loads the appropriate dataframes.
    Returns a list of pandas dataframes.
    """

    # Create an empty list of dataframes that will be displayed:
    displayed_df_l = list()

    # Set the list of bonds to those selected in the input.
    bonds_active_index = bonds_grp.active
    # Get the current bond_grps labels:
    curr_bnds_labels = bonds_grp.labels
    # Build the current bonds
    bonds_l = [curr_bnds_labels[ii] for ii in bonds_active_index]

    for frame in dataframes:
        # Get the frame's compound.
        df_species = frame.characteristics['Aluminate Species'][0]
        # Get the selected compound.
        active_cmpd_l = compound_sel.value
        if df_species in active_cmpd_l and\
            bool(
                set(bonds_l) &
                set(frame.characteristics['Inter-atom distances'])):
            displayed_df_l.append(frame)

    return displayed_df_l


def create_figures(active_frames):
    """
    Creates the figure to be returned. Right now this function is in
    a testing state, and much of it should change.
    """

    # Get the active dataframes to be plotted:
    # active_frames = select_RDFs()

    # Get the current bond_grps labels and the index of the selected:
    bonds_active_index = bonds_grp.active
    curr_bnds_labels = bonds_grp.labels
    # Get the selected bonds to be plotted:
    bonds_l = [curr_bnds_labels[ii] for ii in bonds_active_index]

    # Declare the figure:
    fig = figure(width=800)

    # Add the hover tool:
    # TODO: needs to take from the characteristics metadata dict.
    fig.add_tools(HoverTool(tooltips=[
        ("Radius", "@r"),
    ]))

    # Declare the colors to be used:
    # TODO: look for a more robust way to handle colors
    colors = Category20[len(dataframes)]

    # Iterate through the data frames to be used.
    for (df, df_color) in zip(active_frames, colors):

        # Declare the source from the current frame:
        fig_source = ColumnDataSource(df)

        # Iterate over the bonds selected.
        # TODO: iterates over all available bonds, rather than the selected
        for bond in bonds_l:
            active_bond = 'RDF_' + bond
            fig.line(  # Draw a line plot
                source=fig_source,
                x='r',
                y=active_bond,
                legend=df.characteristics['Aluminate Species'][0],
                color=df_color,
                line_width=1.5
            )
            fig.circle(  # Draw a line plot
                source=fig_source,
                x='r',
                y=active_bond,
                legend=df.characteristics['Aluminate Species'][0],
                color=df_color,
                # line_width=1.5
            )

    return fig


# Create a widget box for the inputs to be carried in.
# Define a sizing_mode
sizing_mode = 'fixed'

# Create a widget box for the static widgets, and one for the dynamnic.
static_widgets = widgetbox(compound_sel, width=400, height=100)
dynamnic_widgets = widgetbox(bonds_grp, sizing_mode=sizing_mode)


def create_div():
    """
    Creates the informationn div html element. This funciton will
    eventually display desired meta-data pulled from the .json file.
    """

    # It is cleaner to extract the desired data prior to building
    # the output string.
    div = Div(
        text="This is only a test.\n {0}".format(input_src.data),
        width=200,
        height=100
    )

    return div


def create_layout(fig, div):
    """
    Creates the layout of the application. This funciton controls where
    the created objects appear on the webpage. This function should take
    the new objects to be placed in the layout.
    """
    my_layout = layout([
        [app_intro_div],
        [static_widgets, dynamnic_widgets],
        [fig, div],
    ], sizing_mode=sizing_mode)

    return my_layout


# Define the update function
# TODO: Create a decorator so that I can re-use code for the other type
# of callback function?
def update():
    """
    Function that runs upon initialization and whenever the user
    interacts with an input.
    """

    # Get the list of active data frames based on user input.
    active_frame_list = select_RDFs()

    # Create the figures based on the retrieved dataframe list.
    new_fig = create_figures(active_frame_list)

    # Create the new info div
    new_div = create_div()

    # Add the new layout to the curdoc() function.
    curdoc().clear()
    curdoc().add_root(create_layout(new_fig, new_div))

    return


def selector_update(attr, old, new):

    # Declare a new bond label list.
    new_bond_labels = list()

    for x in compound_sel.value:
        new_bond_labels.extend(input_src.data[x])

    bonds_grp.labels = list(set(new_bond_labels))
    update()
    pass


def click_update(new):
    update()
    return


compound_sel.on_change('value', selector_update)
bonds_grp.on_click(click_update)

# Run update to load the default dataset
update()
curdoc().title = "RDV Viewer"
