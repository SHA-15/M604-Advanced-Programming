import unittest
import pandas as pd
from visualizations import PublicAssistance, BasicSecurity

class TestPublicAssistance(unittest.TestCase):
    """
    Unit tests for the PublicAssistance class
    """

    def setUp(self):
        """
        Setting up the environment by initializing the PublicAssistance object and processing the data file
        """
        self.pa = PublicAssistance("data/public_assistance.csv", ";", 5, 7)
        self.pa.file_processing(["Year", "Länder", "TypeCode", "PublicAssistance", "Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"])
        
    def test_dtype_conversion(self):
        """
        Testing the dtype_conversion method to ensure that specified columns are converted to numeric data dtypes.         
        """
        df = self.pa.dtype_conversion("Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)")
        self.assertTrue(pd.api.types.is_numeric_dtype(df["Expenditure(TEUR)"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(df["Revenue(TEUR)"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(df["NetExpenditure(TEUR)"]))
    
    def test_filter_data(self):
        """
        Testing the filter_data method to ensure that rows containing the word "Total" in the "Länder" column are removed.
        """
        self.pa.filter_data()
        self.assertNotIn("Total", self.pa.df["Länder"].values)
        
    def test_data_group(self):
        """
        Testing the data_group method to ensure that data is grouped correctly by the specified group_element and columns are correctly aggregated.
        """
        grouped_df = self.pa.data_group(cols=["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"], group_element="Länder")
        self.assertIn("Länder", grouped_df.columns)
        self.assertIn("Expenditure(TEUR)", grouped_df.columns)
        self.assertIn("Revenue(TEUR)", grouped_df.columns)
        self.assertIn("NetExpenditure(TEUR)", grouped_df.columns)
        
class TestBasicSecurity(unittest.TestCase):
    """
    Unit tests for the BasicSecurity class.
    """
    
    def setUp(self):
        """
        Setting up the test environment by initializing the BasicSecurity object, processing the data file, converting data types, and filtering data
        """
        self.bsc = BasicSecurity("data/basic_security_benefits.csv", ";", skiprows=6, skipfooter=4)
        self.bsc.file_processing(["Länder", "Gender", "Q1", "Q2", "Q3", "Q4"])
        self.bsc.dtype_conversion("Q1", "Q2", "Q3", "Q4")
        self.bsc.filter_data()
        
    def test_pivot_table(self):
        """
        Testing the pivot_table method to ensure that the pivot table is created correctly based on the specified parameters
        """
        self.bsc.data_group(cols=["Q1", "Q2", "Q3", "Q4"], group_element="Länder")
        self.bsc.data_group(cols=["Q1", "Q2", "Q3", "Q4"], group_element="Gender", include_total=True)
        pivot_table = self.bsc.pivot_table(columns=["Q1", "Q2", "Q3", "Q4"], group_element=["Länder", "Gender"], values="Total", index="Gender", column_header="Länder")
        self.assertIsNotNone(pivot_table)
        self.assertFalse(pivot_table.empty)
        
if __name__ == "__main__":
    unittest.main()