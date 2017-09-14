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
from bokeh.layouts import layout, widgetbox, row, column
from bokeh.client import push_session
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import MultiSelect, CheckboxGroup, Div
from bokeh.palettes import linear_palette, viridis
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

# Create a columndatasource to hold the names of the active data frames.
data_source = ColumnDataSource(
    data=dict(
        active=[],
    )
)

"""
# CONTROLS
Define the Controls (for variable name use in the functions below.)
These need to be added to the controls list at the bottom of the file.
"""

compound_sel = MultiSelect(
    title="Compound",
    options=list(input_src.data.keys()),
    # value=[list(input_src.data.keys())[0]]
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
        # active_cmpd_l = data_source.data['active'] PROBLEM <--
        active_cmpd_l = compound_sel.value
        print('Checking frame: {}'.format(frame.keys()))
        print('df_species', df_species)
        print('active_cmpd_l', active_cmpd_l)
        if df_species in active_cmpd_l and\
            bool(
                set(bonds_l) &
                set(frame.characteristics['Inter-atom distances'])):
            displayed_df_l.append(frame)

    # From this, set the data_source active column to the active frames
    data_source.data = dict(active=displayed_df_l)

    return


def create_figures():
    """
    Creates the figure to be returned. Right now this function is in
    a testing state, and much of it should change.
    """

    # Get the current/active compounds from data_source.data.active
    active_frames = data_source.data['active']

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
    # To generate an intuitive color palette:
    # Each dataframes should each have a
    df_count = len(active_frames)

    # Create sub-sets of colors, outputs a list of colors
    color_break = viridis(df_count)

    # enumerate through the data frames to be used and the index value.
    # enumerate() is used as zip() failes when there is only one item.
    for idx, df in enumerate(active_frames):

        # Declare the source from the current frame:
        fig_source = ColumnDataSource(df)

        # Count the number of bonds to generate the color sub-set
        bond_count = len(bonds_l)
        # Get the 'pair' or range of color palettes to use
        if idx == 0:
            col_start = 0
            col_end = 1
        else:
            col_start = idx - 1
            col_end = idx
        # use the start and end to generate intermediate colors.
        bond_pallet = linear_palette(
            color_break[col_start:col_end], bond_count)

        # Iterate over the bonds selected.
        # TODO: iterates over all available bonds, rather than the selected
        for idxx, bond in enumerate(bonds_l):

            # Count the number of bonds for color generation
            bond_color = bond_pallet[idx]

            active_bond = 'RDF_' + bond
            fig.line(  # Draw a line plot
                source=fig_source,
                x='r',
                y=active_bond,
                legend=df.characteristics['Aluminate Species'][0],
                color=bond_color,
                line_width=1.5
            )

            fig.circle(  # Draw a circle/dot plot
                source=fig_source,
                x='r',
                y=active_bond,
                legend=df.characteristics['Aluminate Species'][0],
                color=bond_color,
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


def update():
    """
    Function that runs upon initialization and whenever the user
    interacts with an input.

    .. todo:: Consider turning this into a decorator for use in/on the
    other controls callback functions.
    """
    print(input_src.data)
    print(data_source.data)

    # Get the list of active data frames based on user input.
    select_RDFs()
    # data_source.data.active = compound_sel.value

    return


def selector_update(attr, old, new):

    # Declare a new bond label list.
    new_bond_labels = list()

    # use the seelcted values to build the compound list
    for x in compound_sel.value:
        new_bond_labels.extend(input_src.data[x])

    # create a list of unique (set) for the bond_grp labels.
    bonds_grp.labels = list(set(new_bond_labels))
    update()
    return


def click_update(new):
    update()
    return


compound_sel.on_change('value', selector_update)
bonds_grp.on_click(click_update)

# INITIALIZE THE APPLICATION
select_RDFs()
# Create the figures based on the retrieved dataframe list.
initial_fig = create_figures()
# Create the new info div
initial_div = create_div()
# Add the new layout to the curdoc() function.
update()

curdoc().add_root(create_layout(initial_fig, initial_div))

# Run update to load the default dataset
curdoc().title = "RDV Viewer"
