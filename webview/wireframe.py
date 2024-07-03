import streamlit
import altair
from visualizations import public_assist, pa, bsc, basics, melted_df, max_quarterly_value

class WebApp:

    def __init__(self, title="Social Benefits Revenue & Expenditures", icon="🇩🇪"):
        self.title = title
        self.icon = icon
        self.col: str = "PublicAssistance"
        self.filter_by_benefit: iter = pa.df[self.col].unique()
        self.values = ["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"]

        altair.themes.enable("dark")
        self.page_configuration()
        self.develop_sidebar()
        self.establish_top_wireframe()
        self.middle_wireframe()
        self.second_dataset()

    def page_configuration(self, theme="dark"):
        streamlit.set_page_config(
            page_title=self.title,
            page_icon=self.icon,
            layout="wide",
            initial_sidebar_state="auto"
        )

        print("Streamlit Webpage Setup complete")        
        return
    
    def develop_sidebar(self):
        with streamlit.sidebar:

            streamlit.title(f"{self.icon} {self.title}")

            self.filter_by: iter = streamlit.selectbox("Filter by Type of Social Benefit", self.filter_by_benefit)
            self.value_measure: iter = streamlit.selectbox("Filter by Exp, Rev, NetExp", self.values)


            streamlit.markdown("***")
            streamlit.markdown("This project is part of the M605A Advanced Programming Module in GISMA University of Applied Sciences")
            streamlit.markdown("🚀 Github Link: https://github.com/SHA-15/M605_Advanced_Programming")
            streamlit.markdown("Collaborators: Hamza Saleem | Durdona Juraeva")
            streamlit.markdown("***")

    def establish_top_wireframe(self):
        
        with streamlit.container():
            streamlit.header("Social Benefits: Subsistence and Basic Necessity Benefits", divider="rainbow")

            streamlit.subheader("Social Benefits Concentration By Bundesland")

            streamlit.markdown("Deutschland's tax contribution bracket is coupled with social benefit payments - supported by the Sozialamt. This dashboard highlights the overall expenditures within this sector and looks into two specific areas: Basic Security benefits & Subsistence Payments.")

            deutschland_map = public_assist.choropleth_figure(
                                dataframe=pa.Länder_df,
                                dimensions_url="https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/2_bundeslaender/1_sehr_hoch.geo.json", 
                                locations="Länder", 
                                color="NetExpenditure(TEUR)", 
                                labels={"NetExpenditure(TEUR)": "Net Expenditure in Thousand Euros"}, 
                                title="Net Expenditure By State in Deutschland", 
                                range_color=(0, pa.Länder_df["NetExpenditure(TEUR)"].max())
                                )
            streamlit.plotly_chart(deutschland_map, use_container_width=True)

    def middle_wireframe(self):
        
        with streamlit.container():
            
            barplot_visual = public_assist.bar_plot_visual(
                    data=pa.df, 
                    column_name=self.col, 
                    filter_by=self.filter_by, 
                    fig_title=f"{self.value_measure} by {self.filter_by}", value_measure=self.value_measure)
            
            streamlit.pyplot(barplot_visual)

            col1, col2 = streamlit.columns(2, gap="small")

            with col1:
                table_view = public_assist.sorted_df_visual(data=pa.PublicAssistance_df, sort_by="PublicAssistance", asc_order=True)

                streamlit.dataframe(
                    table_view,
                    hide_index=True,
                    width=None,
                    column_config={
                        "PublicAssistance": streamlit.column_config.TextColumn("Public Assistance",),
                        "Expenditure(TEUR)": streamlit.column_config.ProgressColumn(
                            "Expenditure(TEUR)",
                            format="%f",
                            min_value=0,
                            max_value=max(table_view["Expenditure(TEUR)"])
                        ),
                        "Revenue(TEUR)": streamlit.column_config.ProgressColumn(
                            "Revenue",
                            format="%f",
                            min_value=0,
                            max_value=max(table_view["Revenue(TEUR)"])
                        ),
                        "NetExpenditure(TEUR)": streamlit.column_config.ProgressColumn(
                            "NetExpenditure(TEUR)",
                            format="%f",
                            min_value=0,
                            max_value=max(table_view["NetExpenditure(TEUR)"])
                        )
                    }
                )

            with col2:
                do_visual = public_assist.donut_visual(data=pa.PublicAssistance_df, grouping_type=self.value_measure, col_name=self.col, title=f"{self.filter_by} by Social Benefit (% of Total)", in_percent=True)

                streamlit.plotly_chart(do_visual)

    def second_dataset(self):
        
        with streamlit.container():
            streamlit.subheader("Social Benefits: Basic Security Benefits", divider="violet")

            col1, col2 = streamlit.columns(2, gap="medium")

            with col1:
                do_chart = basics.donut_visual(data=bsc.Gender_df, grouping_type="Total", col_name="Gender", title="Total Basic Security Benefits Recipients by Gender")

                streamlit.plotly_chart(do_chart)
            
            with col2:
                htmp = basics.generate_heatmap(x="Länder", y="Gender", color_by="Total Value", title="Total Recipients of Basic Security Benefits", pivot_table=bsc.pivot_table)

                streamlit.plotly_chart(htmp)


            grouped_bar = basics.grouped_bar_plot(data=melted_df, max_value=max_quarterly_value, X="Länder", y="Value", color_by="Quarter", title="Quarterly Values for Each Länder", color_sequence=["purple", "blueviolet", "lightblue", "azure"])

            streamlit.plotly_chart(grouped_bar)


        


                



        









