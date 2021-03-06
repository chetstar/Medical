"""Tests to add:

drop_useless_rows
wide_to_long_by_month
wide_to_long_by_aidcode
make_local_bitmask
keep_best_mcrank
long_to_wide_by_aidcode
merge_aidcode_info

"""

import unittest
import explode
import pandas as pd
from pandas.util.testing import assert_series_equal, assert_frame_equal
from StringIO import StringIO
import numpy as np

class TestExplode(unittest.TestCase):
    """
    Main Test Class
    """

    def test_make_eligibility_bitmask(self):
        """
        make_eligibility_bitmask should:
         *Accept a dataframe with an 'eligibilitystatus' column of string values.
         *Return a series object of the same length as the dataframe it recieved.
         *The returned series should contain True if the first character of the string is 
           less than or equal to 5 And False otherwise.
         *Gracefully deal with NaN values.
        """

        df = pd.DataFrame({'eligibilitystatus':[None, '001', '555', '600', '08B', None, '990']})
        desired_result = pd.Series([False,True,True,False,True,False,False])
        actual_result = explode.make_eligibility_bitmask(df)

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

    def test_make_duplicates_bitmask_best_fist(self):
        #Dupe eligibility best shown first.
        cins = ['000000000', '000000000', '000000000', '111111111']
        elig = ['001','002','003','001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})

        desired_result = pd.Series([True, False, False, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

    def test_make_duplicates_bitmask_worst_fist(self):
        #Dupe eligibility worst shown first.
        cins = ['000000000', '000000000', '000000000', '111111111']
        elig = ['003','002','001','001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})

        desired_result = pd.Series([False, False, True, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

    def test_make_duplicates_bitmask_multiple_nan(self):        
        #Handle multiple NaN Cins.
        cins = ['000000000', None, None, None, None, '111111111']
        elig = ['001', '001', '001', '002', '003', '001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})

        desired_result = pd.Series([True, False, False, False, False, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e
        
    def test_make_duplicates_bitmask_nan_elig(self):        
        #Handle Nan eligs
        cins = ['000000000', '000000000', '111111111', '111111111', '222222222']
        elig = ['001', None, None, None, '001']
        df = pd.DataFrame({'cin':cins, 'elig':elig})

        desired_result = pd.Series([True, False, True, False, True])
        actual_result = explode.make_duplicates_bitmask(df).sort_index()

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

    def test_drop_duplicate_rows(self):

        fake_file = pd.DataFrame({'id': [str(x).rjust(3) for x in range(18)]}
        ).to_string(index = False, header = False)

        df_iter = pd.read_fwf(StringIO(fake_file), 
                              colspecs = [(0,4)],
                              converters = {'id':str},
                              names = ['id'],
                              chunksize = 3,
                              iterator = True)

        mask = [False, False, False, #[]
                False, False, True, #[5]
                True, False, False, #[6]
                True, True, True, #[9,10,11]
                False, False, False, #[]
                False, True, False] #[16]

        dupemask = pd.Series(mask)
        
        desired_results = [[None,None,None],
                           [None,None,'5'],
                           ['6',None,None],
                           ['9','10','11'],
                           [None,None,None],
                           [None,'16',None]]

        for i, df in enumerate(df_iter):

            df = explode.drop_duplicate_rows(df, i, 3, dupemask)
            
            desired_result = pd.Series(data=desired_results[i],index = range(3*i, 3*(i+1))).dropna()
            actual_result = pd.Series(df['id'])

            try:
                assert_series_equal(desired_result, actual_result, check_dtype = False)
            except AssertionError as e:
                print('desired_result: {}'.format(desired_result))
                print('actual_result: {}'.format(actual_result))
                raise e
    
    def test_mcrank(self):
        #eligibilitystatus, full, respcount, ffp, aidcode, mcrank
        data = (
        [[True, True, True, 100, 1, 1],
         [True, True, True, 65, 1, 2],
         [True, True, True, 50, 1, 3], 
         [True, True, False, 100, 1, 4],
         [True, True, False, 65, 1, 5],
         [True, True, False, 50, 1, 6],
         [True, False, True, 100, 1, 7],
         [True, False, True, 65, 1, 8],
         [True, False, True, 50, 1, 9],
         [True, False, False, 100, 1, 10],
         [True, False, False, 65, 1, 11],
         [True, False, False, 50, 1, 12],
         [False, False, False, 50, 1, 13],
         [False, False, False, None, None, None]]
         )

        data = data + data[::-1] #Make sure it works in either order.
        elig, full, respcount, ffp, aidcode, mcrank = zip(*data)

        elig = pd.Series(elig)
        covered = pd.Series(full)
        local = pd.Series(respcount)
        df = pd.DataFrame({'ffp':ffp, 'aidcode':aidcode})
        
        desired_result = pd.Series(mcrank).fillna(value=np.nan)
        actual_result = pd.Series(explode.mcrank(df, elig, local, covered)['mcrank'])

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

    def test_make_disabled_bitmask(self):
        dw = pd.DataFrame({'disabledx':[0,0,1,1,2,3,None]})
        actual_result = explode.make_disabled_bitmask(dw)
        desired_result = pd.Series([False,False,True,True,False,False,False])

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

    def test_make_foster_bitmask(self):
        dw = pd.DataFrame({'fosterx':[0,0,1,1,2,3,None]})
        actual_result = explode.make_foster_bitmask(dw)
        desired_result = pd.Series([False,False,True,True,False,False,False])

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

    def test_make_covered_bitmask(self):
        dw = pd.DataFrame({'full':[0,0,1,1,2,3,None]})
        actual_result = explode.make_covered_bitmask(dw)
        desired_result = pd.Series([False,False,True,True,False,False,False])

        try:
            assert_series_equal(desired_result, actual_result)
        except AssertionError as e:
            print('desired_result: {}'.format(desired_result))
            print('actual_result: {}'.format(actual_result))
            raise e

if __name__ == '__main__':
    unittest.main()
