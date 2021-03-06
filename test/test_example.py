import pathlib
import sys

_here = pathlib.Path(__file__).resolve().parent
sys.path.append(str(_here / '../example'))

import example
import irregular_data


def test_example():
    example.main(num_epochs=3)


def test_irregular_data():
    irregular_data.variable_length_data()
    irregular_data.irregular_sampling()
    irregular_data.missing_data()
    irregular_data.informative_missingness()
