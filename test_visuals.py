import unittest
import pandas as pd
import plotly.express as px
from io import StringIO
from visualizations import Visuals

class TestVisualsMethods(unittest.TestCase):

    def setUp(self):
        # Sample data
        self.sample_data = """
        Länder,Population,2018,2019,2020
        A,1000,50,60,70
        B,2000,70,80,90
        C,3000,90,100,110
        """
        self.columns = ["Länder", "Population", "2018", "2019", "2020"]
        self.data = pd.read_csv("data/public_assistance.csv")
        self.visuals = Visuals()
        
        # Sample geojson url (Replace with a valid geojson URL if needed)
        self.sample_geojson_url = 'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/2_bundeslaender/1_sehr_hoch.geo.json'

    def test_choropleth_figure(self):
        figure = self.visuals.choropleth_figure(
            dataframe=self.data,
            dimensions_url=self.sample_geojson_url,
            locations="Länder",
            color="Population",
            labels={"Population": "Population"},
            title="Sample Choropleth",
            range_color=(0, 3000)
        )
        self.assertIsInstance(figure, px.choropleth)

    def test_sorted_df_visual(self):
        sorted_df = self.visuals.sorted_df_visual(data=self.data, sort_by="Population", asc_order=False)
        self.assertIsInstance(sorted_df, pd.DataFrame)
        self.assertEqual(sorted_df.iloc[0]["Länder"], "C")

    def test_bar_plot_visual(self):
        visual = self.visuals.bar_plot_visual(
            data=self.data,
            column_name="Länder",
            filter_by="A",
            value_measure="Population",
            fig_title="Sample Bar Plot"
        )
        self.assertIsInstance(visual, plt.Figure)

    def test_donut_visual(self):
        donut_chart = self.visuals.donut_visual(
            data=self.data,
            grouping_type="Population",
            col_name="Länder",
            title="Sample Donut Chart"
        )
        self.assertIsInstance(donut_chart, px.pie)

    def test_generate_heatmap(self):
        pivot_table = self.data.pivot(index="Länder", columns="Population", values="2018")
        heatmap = self.visuals.generate_heatmap(
            x="Länder",
            y="Population",
            color_by="2018",
            title="Sample Heatmap",
            pivot_table=pivot_table
        )
        self.assertIsInstance(heatmap, go.Figure)

    def test_grouped_bar_plot(self):
        max_value = self.data["Population"].max()
        grouped_bar = self.visuals.grouped_bar_plot(
            data=self.data,
            max_value=max_value,
            X="Länder",
            y="Population",
            color_by="2018",
            title="Sample Grouped Bar Plot",
            color_sequence=px.colors.qualitative.Dark24
        )
        self.assertIsInstance(grouped_bar, px.Figure)

if __name__ == '__main__':
    unittest.main()
