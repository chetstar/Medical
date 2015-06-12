import unittest
import uncut
import pandas as pd
from pandas.util.testing import assert_series_equal
from pandas.util.testing import assert_frame_equal

from StringIO import StringIO

class TestExplode(unittest.TestCase):
    """
    Main Test Class
    """
    def test_fix_city_names(self):
        wrong_cities = {'city':['Almda','Berkly','Oaklan']}
        correct_cities = {'city':['ALAMEDA', 'BERKELEY', 'OAKLAND']}

        desired_result = pd.DataFrame(correct_cities)
        actual_result = uncut.fix_city_names(pd.DataFrame(wrong_cities))

        try:
            assert_frame_equal(desired_result, actual_result)
        except AssertionError as e:
            print(desired_result)
            print(actual_result)
            raise e

if __name__ == '__main__':
    unittest.main()
