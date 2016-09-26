from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os import path
import unittest

from steno3d.parsers import ParseError
import steno3d
import steno3d_surfer

class TestSurfer(unittest.TestCase):

    def setUp(self):
        surfer_dir = path.split(path.realpath(steno3d_surfer.__file__))[0]
        self.assets = surfer_dir.split(path.sep)[:-1] + ['assets']

    def test_ascii(self):
        ascii_file = path.sep.join(self.assets + ['ascii.grd'])
        parser = steno3d.parsers.grd(ascii_file)
        projs = parser.parse()
        assert len(projs) == 1
        proj, = projs
        assert len(proj.resources) == 1
        assert isinstance(proj.resources[0], steno3d.Surface)
        assert isinstance(proj.resources[0].mesh, steno3d.Mesh2DGrid)
        assert proj.resources[0].mesh.nN == 5*7
        assert proj.resources[0].mesh.nC == 4*6

        parser = steno3d.parsers.AllParsers(ascii_file)
        parser.parse(proj)
        assert len(proj.resources) == 2
        assert isinstance(proj.resources[1], steno3d.Surface)
        assert isinstance(proj.resources[1].mesh, steno3d.Mesh2DGrid)
        assert proj.resources[1].mesh.nN == 5*7
        assert proj.resources[1].mesh.nC == 4*6

    def test_ascii_error(self):
        self.assertRaises(ParseError, lambda: steno3d.parsers.grd('junk.grd'))
        self.assertRaises(ParseError, lambda: steno3d.parsers.grd(5))

        bad_files = [
            'ascii_bad.grd',
        ]
        for f in bad_files:
            grdfile = path.sep.join(self.assets + [f])
            self.assertRaises(ParseError,
                              lambda: steno3d.parsers.grd(grdfile).parse())

    def test_bin6(self):
        # Not implemented!
        pass

    def test_bin7(self):
        # Not implemented!
        pass


if __name__ == '__main__':
    unittest.main()
