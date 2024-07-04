import unittest
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import pyplot as plt
from visualizations import Visuals

class TestVisuals(unittest.TestCase):
    """
    Unit tests for the Visuals class
    """
    
    def setUp(self):
        """
        Setting up the test environment by initializing the Visuals object and creating a sample DataFrame for testing.
        """
        self.visuals = Visuals()
        self.sample_df = pd.DataFrame({
            "Länder": ["Berlin", "Bayern", "Hamburg"],
            "NetExpenditure(TEUR)": [1000, 2000, 1500]
        })
        
    def test_choropleth_figure(self):
        """
        Testing the choropleth_figure method to ensure it returns a Plotly Figure object for the given sample DataFrame
        """
        choro = self.visuals.choropleth_figure(
            dataframe=self.sample_df,
            dimensions_url="1_sehr_hoch.geo.json",
            locations="Länder",
            color="NetExpenditure(TEUR)",
            labels={"NetExpenditure(TEUR)": "NetExpenditure in Thousand Euros"},
            title="Net Expenditure By State in Deutschland",
            range_color=(0, 2000)
        )
        self.assertIsInstance(choro, go.Figure)
        
    def test_sorted_df_visual(self):
        """
        Testing the sorted_df_visual method to ensure it returns a sorted DataFrame based on the specified column in ascending order
        """
        sorted_df = self.visuals.sorted_df_visual(data=self.sample_df, sort_by="NetExpenditure(TEUR)", asc_order=True)
        self.assertEqual(sorted_df.iloc[0]["Länder"], "Berlin")
        
    def test_bar_plot_visual(self):
        """
        Testing the bar_plot_visual method to ensure it returns a Matplotlib Figure object for the given sample DataFrame
        """
        bar_plot = self.visuals.bar_plot_visual(
            
            data=self.sample_df,
            column_name="Länder",
            filter_by="Berlin",
            value_measure="NetExpenditure(TEUR)",
            fig_title="Net Expenditure in Berlin"            
        )
        self.assertIsInstance(bar_plot, go.Figure)
        
    def test_donut_visual(self):
        """
        Testing the donut_visual method to ensure it returns a Plotly Figure pbject for the given sample DataFrame
        """
        donut_chart = self.visuals.donut_visual(
            data=self.sample_df,
            grouping_type="NetExpenditure(TEUR)",
            col_name="Länder"
        )
        self.assertIsInstance(donut_chart, go.Figure)
        
    def test_generate_heatmap(self):
        """
        Testing the generate_heatmap method to ensure it returns a Plotly Figure object for the given pivot table created from the sample DataFrame
        """
        pivot_table = pd.pivot_table(self.sample_df, values="NetExpenditure(TEUR)", index="Länder")
        heatmap = self.visuals.generate_heatmap(
            x="Länder",
            y="NetExpenditure(TEUR)",
            color_by="NetExpenditure(TEUR)",
            title="Heatmap of Net Expenditure",
            pivot_table=pivot_table
        )
        self.assertIsInstance(heatmap, go.Figure)
        
    def test_grouped_bar_plot(self):
        """
        Testing the grouped_bar_plot method to ensure it returns a Plotly Figure object for the given melted DataFrame
        """
        melted_df = pd.melt(self.sample_df, id_vars=["Länder"], var_name="Quarter", value_name="Value")
        grouped_bar = self.visuals.grouped_bar_plot(
            data = melted_df,
            max_value=2000,
            X="Länder",
            y="Value",
            color_by="Quarter",
            title="Grouped Bar Plot of Net Expenditure",
            color_sequence=px.colors.qualitative.Plotly
        )
        self.assertIsInstance(grouped_bar, go.Figure)
        
if __name__ == "__main__":
    unittest.main()