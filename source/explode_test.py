import unittest
import explode
import pandas as pd
from pandas.util.testing import assert_series_equal

class TestExplode(unittest.TestCase):
    """
    Main Test Class
    """

    def test_make_eligibility_bitmask(self):
        """
        make_eligibility_bitmask should:
         *Accept a dataframe with an 'eligibilitystatus' column of string values.
         *Gracefully deal with NaN values
         *return true if the first character of the string is less than or equal to 5.
         *Return a series object of the same length as the dataframe it recieved.
        """
        #What if the first character is alpha not numeric?
        
        df = pd.DataFrame({'eligibilitystatus':[None, '001', '555', '600', '08B', None]})

        desired_result = pd.Series([False,True,True,False,True,False])

        actual_result = explode.make_eligibility_bitmask(df)

        assert_series_equal(desired_result, actual_result)


if __name__ == '__main__':
    unittest.main()
