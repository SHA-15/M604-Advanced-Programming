import unittest
import chardet
import pandas as pd
from io import StringIO
from visualizations.eda import Dataset, PublicAssistance, BasicSecurity

class TestDatasetMethods(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sample_data = """
        Länder,Population,2018,2019,2020
        A,1000,50,60,70
        B,2000,70,80,90
        C,3000,90,100,110
        Total,6000,210,240,270
        """
        self.columns = ["Länder", "Population", "2018", "2019", "2020"]
        
        # Using StringIO to simulate file reading
        self.data_file = StringIO(self.sample_data)
        
        self.public_assistance = PublicAssistance(self.data_file, delimiter=",", skiprows=0, skipfooter=0)
        self.basic_security = BasicSecurity(self.data_file, delimiter=",", skiprows=0, skipfooter=0)

    def test_encoding_detection(self):
        with self.data_file as f:
            encoding = chardet.detect(f.read().encode())["encoding"]
        self.assertEqual(encoding, "ascii")

    def test_file_processing(self):
        self.public_assistance.file_processing(encoding="ascii", columns=self.columns)
        self.assertEqual(self.public_assistance.df.columns.tolist(), self.columns)

    def test_dtype_conversion(self):
        self.public_assistance.file_processing(encoding="ascii", columns=self.columns)
        df = self.public_assistance.dtype_conversion("Population")
        self.assertTrue(pd.api.types.is_numeric_dtype(df["Population"]))

    def test_filter_data(self):
        self.public_assistance.file_processing(encoding="ascii", columns=self.columns)
        self.public_assistance.filter_data()
        self.assertFalse(self.public_assistance.df["Länder"].str.contains("Total").any())

    def test_data_group(self):
        self.public_assistance.file_processing(encoding="ascii", columns=self.columns)
        grouped_data = self.public_assistance.data_group(cols=["2018", "2019", "2020"], group_element="Länder", include_total=True)
        self.assertTrue("Total" in grouped_data.columns)

    def test_pivot_table(self):
        self.basic_security.file_processing(encoding="ascii", columns=self.columns)
        pivot_df = self.basic_security.pivot_table(values="Population", index="Länder", column_header="2018")
        self.assertTrue(isinstance(pivot_df, pd.DataFrame))

    def test_max_quarterly_assessment(self):
        self.basic_security.file_processing(encoding="ascii", columns=self.columns)
        elongate_df, max_value = self.basic_security.max_quarterly_assessment(self.basic_security.df, cols=["Länder", "2018", "2019", "2020"], var_assignment="Year", value_name="Value")
        self.assertTrue(isinstance(elongate_df, pd.DataFrame))
        self.assertTrue(isinstance(max_value, (int, float)))

if __name__ == "__main__":
    unittest.main()
