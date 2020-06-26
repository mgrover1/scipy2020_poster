# MetPy's Meteorological Data Parsing Abilities: From Surface to Upper Air [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mgrover1/scipy2020_poster/master)
## *Submission for SciPy 2020*

## Authors: [Max Grover¹](https://mgrover1.github.io/) and [Ryan May²](https://staff.ucar.edu/users/rmay)
### *¹University of Illinois at Urbana-Champaign* *²Unidata Program Center*
---

## Keywords
`Parsing`, `Meteorology`, `MetPy`, `Weather`, `Historical`

## Short Summary

Surface and upper air observations can now be parsed using MetPy, an open-source Python library for meteorological applications, supported by Unidata. A parser for METARs can be used to read in surface data, while the TTAA parser reads in upper air data. These new tools make it easy for the user to plot surface and upper air maps which are used to analyze weather systems.


## Abstract

Maps of surface station and upper air observations are used extensively by the meteorology community. Surface observations can be used to identify frontal boundaries, surface pressure anomalies, sea breezes, and numerous other surface-based features. Upper air observations provide a vertical dimension to the analysis, which is useful for identifying features such as the location of the jet stream. The General Meteorology Package (GEMPAK), originally developed three decades ago, has been used by the meteorology community to make surface and upper air maps for years. Unfortunately, GEMPAK has reached end-of-development status. Meanwhile, Python developers have made great strides in recent years by making meteorological data visualization easier for users. MetPy is a Python library built by the meteorology community and managed by Unidata. New functionality in MetPy now makes plotting surface and upper air data easier than was previously possible.

Most surface data is stored in METeorological Aerodrome Reports (METARs), while upper air data is encoded in TTAA and TTBB format, which are both text files. The variable formatting can be difficult to parse due to inconsistent generation procedures. This presentation focuses on the new functions in MetPy parse the METARs and TTAA/TTBBs from THREDDS servers and generate dataframes that can be used to create surface and upper air maps with less lines of code. With the declarative plotting interface, users can utilize GEMPAK-like syntax to create high quality maps. The simplified plotting functionality makes it easier for new users to Python to make publication-quality visualizations of surface and upper air data.

## References

Site locations from
2010-2019 Weather Graphics / www.weathergraphics.com / servicedesk@weathergraphics.com

May, R. M., Arms, S. C., Marsh, P., Bruning, E., Leeman, J. R., Goebbert, K., Thielen, J. E.,
    and Bruick, Z., 2020: MetPy: A Python Package for Meteorological Data.
    Version 0.12.1.post2, Unidata, Accessed 21 April 2020.
    [Available online at https://github.com/Unidata/MetPy.]
    doi:10.5065/D6WW7G29.
