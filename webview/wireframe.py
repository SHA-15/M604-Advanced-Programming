import streamlit
import altair
from visualizations import public_assist, pa, bsc, basics, melted_df, max_quarterly_value, sub_benefits, subsistence

class WebApp:
    '''
    The WebApp class connects the EDA conversion process with the visualizations to display onto the main streamlit application. The Class houses the methods to instantiate the streamlit web object window and calls upon all supplementary methods as its instantiated to create the sidebar, containers and visualizations within them.
    '''
    def __init__(self, title="Social Benefits Revenue & Expenditures", icon="🇩🇪"):
        '''
        The instantiation of the WebApp class produces the streamlit object and calls upon the container and setup configuration methods of streamlit. It uses the EDA.py and Plot.py imports and its subsequent objects to create the web interface.

        Inputs:
        - Title: Title of the Tab window and side bar object
        - Icon: The Icon represented on the sidebar and tab header

        Output:
        - streamlit web application object
        '''
        self.title = title
        self.icon = icon
        self.col: str = "PublicAssistance"
        self.filter_by_benefit: iter = pa.df[self.col].unique()
        self.values = ["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"]

        # Altair visualization sets the backgroun theme to darkmode
        altair.themes.enable("dark")

        # Method calls upon instantiation to load the visualizations directly as the program loads up, all parameters are defined within each function definition with their respective datasets
        self.page_configuration()
        self.develop_sidebar()
        self.establish_top_wireframe()
        self.middle_wireframe()
        self.second_dataset()
        self.thirdataset(data=sub_benefits.filtered_df)

    def page_configuration(self, theme="dark"):
        '''
        Utilizes streamlits .set_page_config() method to define the overall web object parameters and web page settings.
        '''
        streamlit.set_page_config(
            page_title=self.title,
            page_icon=self.icon,
            layout="wide",
            initial_sidebar_state="auto"
        )

        print("Streamlit Webpage Setup complete")        
        return
    
    def develop_sidebar(self):
        '''
        Creation of the sidebar object to allow user interaction with the dataset. Select options provide functionality into manipulating the data visualizations for a smoother experience.
        '''
        with streamlit.sidebar:

            streamlit.title(f"{self.icon} {self.title}")

            self.filter_by: iter = streamlit.selectbox("Filter by Type of Social Benefit", self.filter_by_benefit)
            self.value_measure: iter = streamlit.selectbox("Filter by Exp, Rev, NetExp", self.values)


            self.region: str = streamlit.multiselect("Select Bundesland", pa.Länder_df["Länder"].unique(), default=pa.Länder_df["Länder"].unique())

            streamlit.markdown("***")
            streamlit.markdown("This project is part of the M605A Advanced Programming Module in GISMA University of Applied Sciences")
            streamlit.markdown("🚀 Github Link: https://github.com/SHA-15/M605_Advanced_Programming")
            streamlit.markdown("Collaborators: Hamza Saleem | Durdona Juraeva")
            streamlit.markdown("***")

    def establish_top_wireframe(self):
        '''
        Creates the user first view container. The first container embodies the choropleth figure from the PublicAssistance Dataset, combined with the topic header and explanations.
        '''
        with streamlit.container():
            streamlit.header("Social Benefits: Subsistence and Basic Necessity Benefits", divider="rainbow")

            streamlit.subheader("Social Benefits Concentration By Bundesland")

            streamlit.markdown("Deutschland's tax contribution bracket is coupled with social benefit payments - supported by the Sozialamt. This dashboard highlights the overall expenditures within this sector and looks into two specific areas: Basic Security benefits & Subsistence Payments.")

            map_region_filter = pa.Länder_df[pa.Länder_df["Länder"].isin(self.region)] 



            deutschland_map = public_assist.choropleth_figure(
                                dataframe=map_region_filter,
                                dimensions_url="1_sehr_hoch.geo.json", 
                                locations="Länder", 
                                color=self.value_measure, 
                                labels={self.value_measure: f"{self.value_measure[:-5]}in Thousand Euros"}, 
                                title=f"{self.value_measure} By State in Deutschland", 
                                range_color=(0, pa.Länder_df["NetExpenditure(TEUR)"].max())
                                )
            streamlit.plotly_chart(deutschland_map, use_container_width=True)

    def middle_wireframe(self):
        '''
        The dataset is segregated within the function call to establish a second entity within the streamlit application. Housing the visualizations from the relationships within the first dataset. Outlines the barplot visualizations, table view and donut chart.
        '''
        with streamlit.container():
            
            barplot_visual = public_assist.bar_plot_visual(
                    data=pa.df, 
                    column_name=self.col, 
                    filter_by=self.filter_by, 
                    fig_title=f"{self.value_measure} by {self.filter_by}", 
                    value_measure=self.value_measure,
                    chosen_states=self.region)
            
            streamlit.plotly_chart(barplot_visual)

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
                do_visual = public_assist.donut_visual(data=pa.PublicAssistance_df, grouping_type=self.value_measure, col_name=self.col, in_percent=True)

                streamlit.plotly_chart(do_visual)

    def second_dataset(self):
        '''
        Encompasses the second dataset within a separate section of streamlit and provides the visualizations to seek the relationship and data analysis of the Basic Security Benefits.
        '''
        with streamlit.container():
            streamlit.subheader("Social Benefits: Basic Security Benefits", divider="violet")

            col1, col2 = streamlit.columns(2, gap="medium")

            with col1:
                do_chart = basics.donut_visual(data=bsc.Gender_df, grouping_type="Total", col_name="Gender")

                streamlit.plotly_chart(do_chart)
            
            with col2:
                htmp = basics.generate_heatmap(x="Länder", y="Gender", color_by="Total Value", title="Total Recipients of Basic Security Benefits", pivot_table=bsc.pivot_table)

                streamlit.plotly_chart(htmp)


            grouped_bar = basics.grouped_bar_plot(data=melted_df, max_value=max_quarterly_value, X="Länder", y="Value", color_by="Quarter", title="Quarterly Values for Each Länder", color_sequence=["purple", "blueviolet", "lightblue", "azure"])

            streamlit.plotly_chart(grouped_bar)


    def thirdataset(self, data: object):
        '''
        Focusing the Subsistence Payment section of the relationships in social benefits. The Subsistence Payments relationship over time.
        '''
        with streamlit.container():
            streamlit.subheader("Social Benefits: Subsistence Payment Recipients", divider="blue")
            
            
            
            visual_filter = data[sub_benefits.filtered_df["Länder"].isin(self.region)]

            visual = subsistence.line_progression_chart(data=visual_filter, X="Year", y="Total", hue="Länder", title="Total Recipients of Subsistence Benefits By Bundesland")

            streamlit.plotly_chart(visual)






                



        









