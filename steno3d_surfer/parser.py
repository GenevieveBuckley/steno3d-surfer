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

    def parse(self, project=None, verbose=True, as_topo=True):
        """function parse

        Parses the .grd file (binary or ASCII) provided at parser
        instantiation into a Steno3D project.

        Optional input:
            project: Preexisting Steno3D project to add .grd file components
                     to. If not provided, a new project will be created.
            verbose: Print messages and warnings during file parsing.
                     (default: True)
            as_topo: If True, add data from grid file as topography.
                     Otherwise only add the data as color on a flat surface.
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

        surf = steno3d.Surface(
            project=project,
            mesh=steno3d.Mesh2DGrid(
                O=origin,
                h1=h1,
                h2=h2
            ),
            data=[
                dict(
                    location='N',
                    data=steno3d.DataArray(
                        array=data
                    )
                )
            ]
        )

        if as_topo:
            surf.mesh.Z = data

        if verbose and len(warnings) > 0:
            print('  If you are interested in contributing to unsupported '
                  'features, please visit\n'
                  '      https://github.com/3ptscience/steno3d-surfer')

        return (project,)


    def _surfer7bin(self, verbose, warnings):
        with open(self.file_name, 'rb') as f:
            if unpack('4s', f.read(4))[0] != b'DSRB':
                raise steno3d.parsers.ParseError(
                    'Invalid file identifier for Surfer 7 binary .grd '
                    'file. First 4 characters must be DSRB.'
                )
            f.read(8) #Size & Version

            section = unpack('4s', f.read(4))[0]
            if section != b'GRID':
                raise steno3d.parsers.ParseError(
                    'Unsupported Surfer 7 file structure. GRID keyword '
                    'must follow immediately after header but {} '
                    'encountered.'.format(section)
                )
            size = unpack('<i', f.read(4))[0]
            if size != 72:
                raise steno3d.parsers.ParseError(
                    'Surfer 7 GRID section is unrecognized size. Expected '
                    '72 but encountered {}'.format(size)
                )
            nrow = unpack('<i', f.read(4))[0]
            ncol = unpack('<i', f.read(4))[0]
            x0 = unpack('<d', f.read(8))[0]
            y0 = unpack('<d', f.read(8))[0]
            deltax = unpack('<d', f.read(8))[0]
            deltay = unpack('<d', f.read(8))[0]
            zmin = unpack('<d', f.read(8))[0]
            zmax = unpack('<d', f.read(8))[0]
            rot = unpack('<d', f.read(8))[0]
            if rot != 0:
                self._warn('Unsupported feature: Rotation != 0',
                           warnings, verbose)
            blankval = unpack('<d', f.read(8))[0]

            section = unpack('4s', f.read(4))[0]
            if section != b'DATA':
                raise steno3d.parsers.ParseError(
                    'Unsupported Surfer 7 file structure. DATA keyword '
                    'must follow immediately after GRID section but {} '
                    'encountered.'.format(section)
                )
            datalen = unpack('<i', f.read(4))[0]
            if datalen != ncol*nrow*8:
                raise steno3d.parsers.ParseERror(
                    'Surfer 7 DATA size does not match expected size from '
                    'columns and rows. Expected {} but encountered '
                    '{}'.format(ncol*nrow*8, datalen)
                )
            data = np.zeros(ncol*nrow)
            for i in range(ncol*nrow):
                data[i] = unpack('<d', f.read(8))[0]
            data = np.where(data >= blankval, np.nan, data)

            try:
                section = unpack('4s', f.read(4))[0]
                if section == b'FLTI':
                    self._warn('Unsupported feature: Fault Info',
                               warnings, verbose)
                else:
                    self._warn('Unrecognized keyword: {}'.format(section),
                               warnings, verbose)
                self._warn('Remainder of file ignored', warnings, verbose)
            except:
                pass

            return ([x0, y0, 0], np.ones(ncol-1)*deltax,
                    np.ones(nrow-1)*deltay,
                    data.reshape(ncol, nrow, order='F').flatten())


    def _surfer6bin(self, verbose, warnings):
        with open(self.file_name, 'rb') as f:
            if unpack('4s', f.read(4))[0] != b'DSBB':
                raise steno3d.parsers.ParseError(
                    'Invalid file identifier for Surfer 6 binary .grd '
                    'file. First 4 characters must be DSBB.'
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

        return ([xlo, ylo, 0], np.diff(xvals), np.diff(yvals),
                data.reshape(nx, ny, order='F').flatten())


    def _surfer6ascii(self, verbose, warnings):
        with open(self.file_name, 'r') as f:
            if f.readline().strip() != 'DSAA':
                raise steno3d.parsers.ParseError(
                    'Invalid file identifier for Surfer 6 ASCII .grd '
                    'file. First line must be DSAA'
                )
            [ncol, nrow] = [int(n) for n in f.readline().split()]
            [xmin, xmax] = [float(n) for n in f.readline().split()]
            [ymin, ymax] = [float(n) for n in f.readline().split()]
            [zmin, zmax] = [float(n) for n in f.readline().split()]
            data = np.zeros((nrow, ncol))
            for i in range(nrow):
                data[i, :] = [float(n) for n in f.readline().split()]

        return ([xmin, ymin, 0], np.diff(np.linspace(xmin, xmax, ncol)),
                np.diff(np.linspace(ymin, ymax, nrow)), data.flatten())


    @staticmethod
    def _warn(warning, warnings, verbose):
        if warning in warnings:
            return
        warnings.add(warning)
        if verbose:
            print('  ' + warning)
