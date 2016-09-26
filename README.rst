Steno3D Parser: .grd
********************

.. image:: https://travis-ci.org/3ptscience/steno3d-surfer.svg?branch=master
    :target: https://travis-ci.org/3ptscience/steno3d-surfer

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: https://github.com/3ptscience/steno3d-surfer/blob/master/LICENSE

.. image:: https://img.shields.io/badge/download-PyPI-yellow.svg
    :target: https://pypi.python.org/pypi/steno3d_surfer

Welcome to the Surfer .grd file parser plugin for `Steno3D <https://www.steno3d.com>`_
by `3point Science <https://www.3ptscience.com>`_. This repository supplements the
`Steno3D Python client library <https://github.com/3ptscience/steno3dpy>`_.

To install this parser, simply

.. code::

    pip install steno3d_surfer

On import, this parser plugs in to the `steno3d.parsers` module. It can be
used as follows:

.. code:: python

    import steno3d
    import steno3d_surfer
    parser = steno3d.parsers.grd('yourfile.grd')
    (grd_project,) = parser.parse()

This parser supports
`Surfer 6 binary <http://geospatialdesigns.com/surfer6_format.htm>`_,
`Surfer 7 binary <http://geospatialdesigns.com/surfer7_format.htm>`_, and
`ASCII <http://hs.umt.edu/geosciences/faculty/sheriff/equipment-techniques-and-cheats/surfergrids.pdf>`_
.grd files. Currently, this parser, does not support Surfer 7 Fault Info.

If you are interested in additional features you may
`submit an issue <https://github.com/3ptscience/steno3d-surfer/issues>`_
or consider directly contributing to the
`github repository <https://github.com/3ptscience/steno3d-surfer>`_. `Parser
guidelines <https://python.steno3d.com/en/latest/content/parsers.html>`_
are available online.

To learn more, about Steno3D, visit `steno3d.com <https://www.steno3d.com>`_, the
`Steno3D source repository <https://github.com/3ptscience/steno3dpy>`_, and our
`online documentation <https://steno3d.com/docs>`_.
