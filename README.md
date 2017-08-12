# Pyluminate

Under construction... Currently a collection of scripts.

**Overview**

Pyluminate is a backend to assist in the visualization of data concerning aluminate.
Its goal is to provide a visualizations of both the available literature data
concerning aluminum in basic conditions as well as data generated from the 
[IDREAM](http://efrc.pnnl.gov/idream/) project.

## TODO

- [x] Create a demo & presentation for August 15th or 14th?
- [x] Write the ISASetup.py script.
- [x] Import all data previously stored in R databases into `.csv` format.
- [x] Link the added databases within the ISA-script.
- [x] Create functions to handle generating columns.
- [ ] Finish the colum selection demo.
- [ ] Write functions for ISA metadata additions.

## Standardized Column Headers

At the moment it seems required to name the columns consistently within
their corresponding `.csv` files. The table below shows the headers used.

| CSV Header | Description |
-------------|--------------
`Al_concentration` | The concentration of aluminate in moles per liter (M).
`OH_concentration` | Concentration of hydroxide. *Not* the pH.
`wavelength`       | a wavelength peak, measured in cm<sup>-1</sup>.
`temperature`      | The temperature of the experiment, given in Celsius.
`Al_ppm`           | The peak of an <sup>27</sup>Al in ppm.

## Counter Ions tracked

The ISA metadata toolset contains some methods for handling materials.
Since the counter ions are easily deliniated (among a few possible elements)
it seems easier to simply store them as a list of factors. For convenience
the counter ions found so far are shown below.

| Counter ion symbol | element or description |
|--------------------|------------------------|
