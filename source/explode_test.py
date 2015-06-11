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

    def test_make_duplicates_bitmask(self):
        #Must sort_index results because assert_series_equal fails if the orders don't match.

        #Dupe eligibility best shown first.
        cins = ['000000000', '000000000', '000000000', '111111111']
        elig = ['001','002','003','001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})
        desired_result = pd.Series([True, False, False, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()
        assert_series_equal(desired_result, actual_result)

        #Dupe eligibility worst shown first.
        cins = ['000000000', '000000000', '000000000', '111111111']
        elig = ['003','002','001','001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})
        desired_result = pd.Series([False, False, True, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()
        assert_series_equal(desired_result, actual_result)
        
        #Handle multiple NaN Cins.
        cins = ['000000000', None, None, None, None, '111111111']
        elig = ['001', '001', '001', '002', '003', '001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})
        desired_result = pd.Series([True, False, False, False, False, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()
        assert_series_equal(desired_result, actual_result)
        
        #Handle Nan eligs
        cins = ['000000000', '000000000', '111111111', '111111111', '222222222']
        elig = ['001', None, None, None, '001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})
        desired_result = pd.Series([True, False, True, False, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()
        assert_series_equal(desired_result, actual_result)

if __name__ == '__main__':
    unittest.main()
