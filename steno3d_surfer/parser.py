from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from struct import unpack

import numpy as np

import steno3d


class grd(steno3d.parsers.BaseParser):                          # nopep8
    """class stl

    Parser class for Surfer .grd files This parser supports both
    Surfer 6 binary and ASCII files and Surfer 7 binary files.
    """

    extensions = ('grd',)

    def parse(self, project=None, verbose=True):
        """function parse

        Parses the .grd file (binary or ASCII) provided at parser
        instantiation into a Steno3D project.

        Optional input:
            project: Preexisting Steno3D project to add .grd file components
                     to. If not provided, a new project will be created.
            verbose: Print messages and warnings during file parsing.
                     (default: True)

        Output:
            tuple containing one Steno3D project with components parsed
            from the .grd file
        """

        warnings = set()

        if project is None:
            project = steno3d.Project(
                description='Project imported from ' + self.file_name
            )
        elif not isinstance(project, steno3d.Project):
            raise steno3d.parsers.ParseError('Only allowed input for parse is '
                                             'optional Steno3D project')

        f = open(self.file_name, 'rb')
        file_ident = unpack('4s', f.read(4))[0]
        f.close()
        if file_ident == b'DSRB':
            parse_fcn = self._surfer7bin
        elif file_ident == b'DSBB':
            parse_fcn = self._surfer6bin
        elif file_ident == b'DSAA':
            parse_fcn = self._surfer6ascii
        else:
            raise steno3d.parsers.ParseError(
                'Invalid file identifier for Surfer .grd file. First 4 '
                'characters must be DSRB, DSBB, or DSAA'
            )
        (origin, h1, h2, data) = parse_fcn(verbose, warnings)

    def _surfer7bin(self, verbose, warnings):
        #Surfer 7 binary
        with open(grdfile, 'br') as f:

        #     for i in range(4):
            print(unpack('4s', f.read(4))[0] == b'DSRB') #D S R B
        #     print(hex(unpack('<i', f.read(4))[0]))
            print(unpack('<i', f.read(4))[0]) #Size
            print(unpack('<i', f.read(4))[0]) #Version


            for i in range(4):
                print(unpack('c', f.read(1))[0]) #G R I D
        #     print(hex(unpack('<i', f.read(4))[0]))
            print(unpack('<i', f.read(4))[0]) #Size

            nrow = unpack('<i', f.read(4))[0]
            ncol = unpack('<i', f.read(4))[0]
            x0 = unpack('<d', f.read(8))[0]
            y0 = unpack('<d', f.read(8))[0]
            deltax = unpack('<d', f.read(8))[0]

            deltay = unpack('<d', f.read(8))[0]
            zmin = unpack('<d', f.read(8))[0]
            zmax = unpack('<d', f.read(8))[0]

            rot = unpack('<d', f.read(8))[0]
            blankval = unpack('<d', f.read(8))[0]

            #Data
            for i in range(4):
                print(unpack('c', f.read(1))[0]) #D A T A
            datalen = unpack('<i', f.read(4))[0]
            assert datalen == ncol*nrow*8
            data = np.zeros(ncol*nrow)
            for i in range(ncol*nrow):
                data[i] = unpack('<d', f.read(8))[0]
            data = np.where(data >= blankval, np.nan, data)

            #Fault Info
        #     for i in range(4):
        #         print(unpack('c', f.read(1))[0]) #F L T I


    def _surfer6bin(self, verbose, warnings):
        with open(self.file_name, 'br') as f:
            if unpack('4s', f.read(4))[0] != b'DSBB':
                raise steno3d.parsers.ParseError(
                    'Invalid file identifier for Surfer 6 binary .grd '
                    'file. First 4 characters must be DSBB'
                )
            nx = unpack('<h', f.read(2))[0]
            ny = unpack('<h', f.read(2))[0]
            xlo = unpack('<d', f.read(8))[0]
            xhi = unpack('<d', f.read(8))[0]
            ylo = unpack('<d', f.read(8))[0]
            yhi = unpack('<d', f.read(8))[0]
            zlo = unpack('<d', f.read(8))[0]
            zhi = unpack('<d', f.read(8))[0]
            xvals = np.linspace(xlo, xhi, nx)
            yvals = np.linspace(ylo, yhi, ny)
            data = np.ones(nx * ny)
            for i in range(nx * ny):
                zdata = unpack('<f', f.read(4))[0]
                if zdata >= 1.701410009187828e+38:
                    data[i] = np.nan
                else:
                    data[i] = zdata

        return ([xlo, ylo, 0], np.diff(xvals), np.diff(yvals), data)


    def _surfer6ascii(self, verbose, warnings):



    @staticmethod
    def _warn(warning, warnings, verbose):
        if warning in warnings:
            return
        warnings.add(warning)
        if verbose:
            print('  ' + warning)
