import unittest
import shutil
import re
from pathlib import Path

from optapp.parameters import ParameterGrid, FloatParameter, BoolParameter
from test import testenv

class ParameterGridTest(unittest.TestCase):
    def setUp(self):
        self.pars = [
            FloatParameter("tol", 1e-4, 1, 10),
            FloatParameter("C", 1, 3, 10),
            BoolParameter("fit_intercept")
        ]

    def test_generate_parameter_grid(self):
        pg = ParameterGrid(self.pars)
        pg_pars = pg.parameter_vector
        self.assertIsInstance(pg_pars, dict)
        for k in pg_pars.keys():
            self.assertIsInstance(pg_pars[k], list)
        return pg

    def test_generate_parameter_combinations(self):
        pg = self.test_generate_parameter_grid()
        par_combs = pg.generate_combs()
        pg_pars = pg.parameter_vector

        n_combs = 1
        for k in pg_pars.keys():
            n_combs *= pg.get_parameter_count(k)

        self.assertEqual(n_combs, len(par_combs[1]))

if __name__ == '__main__':
    unittest.main()
