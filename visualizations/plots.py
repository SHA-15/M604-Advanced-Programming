from urllib.request import urlopen
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import seaborn as sns
import pandas as pd
import json


class Visuals:
    '''
    The class Visuals connects the Dataframe objects to convert them into visualizations for understanding feature relationships. The methods provided by the class provide bar, choropleths, heatmaps, donuts and line charts.
    '''
    def choropleth_figure(self, dataframe: pd.DataFrame, dimensions_url: str, locations: str ,color: str, labels: dict, title: str, range_color: tuple, color_continuous_scale="plasma", fig_templates="plotly_dark", fig_margins={"l":0, "r":0, "t":30, "b":0}) -> go.choropleth:
        '''
        Creates a plotly figure object -> choropleth image utilizing a json dimensions file and sizing parameters to segregate defined datapoints.

        Inputs:
        - dataframe: DataFrame object
        - dimensions: link to .json file with geographical parameters and matrix values
        - locations: String value to match JSON locations value
        - color: hue factor to label each section of as per geographical parameters
        - title: figure title
        - range_color: range of values to establish scale of color scaling
        - color_continuous_scale: similar to plotly parameter for color spectrum
        - fig_template: plotly defined template for dark mode
        - fig_margins: plotly figure margins

        Output:
        - Plotly Graph Objects figure: Chloropeth map figure
        '''
        with urlopen(dimensions_url) as dimension:
            bundesland = json.load(dimension)
        
        choro = px.choropleth(dataframe, geojson=bundesland, locations=locations, featureidkey="properties.name",
        color=color, labels=labels, title=title, color_continuous_scale=color_continuous_scale,
        range_color=range_color
        )

        choro.update_geos(fitbounds="locations", visible=False)

        choro.update_layout(
        template=fig_templates,
        margin=fig_margins,
        height=500
        )

        return choro
    
    def sorted_df_visual(self, data: pd.DataFrame, sort_by: str, asc_order: bool) -> pd.DataFrame:
        '''
        Produces a sorted dataframe defined by the sort_by parameter and returns the sorted Dataframe for a table visual

        Inputs:
        - data: the input pd.DataFrame
        - sort_by: Column to sort by
        - asc_order: Boolean to ascertain the sorting in either acending and descending order

        Output:
        - Sorted DataFrame object
        '''
        sorted_df = data.sort_values(by=sort_by, ascending=asc_order)

        print(sorted_df.head(10))

        return sorted_df
    
    def bar_plot_visual(self, data: pd.DataFrame, column_name: str, filter_by: str, value_measure: str, fig_title: str, type_area="Länder")-> plt.figure:
        '''
        Provides a bar plot visualization from a refined dataframe.

        Inputs: 
        - data : Dataframe object
        - column_name: x-axis column value
        - filter_by: Focus of Social Beneift to filter the dataframe
        - value_measure: Type of numerical feature to review in the visualization

        Output: 
        - Barplot plotly figure
        '''
        df_filter = data[data[column_name] == filter_by]

        visual = plt.figure(figsize=(8, 6))
        plt.style.use('dark_background')

        sns.barplot(data=df_filter, x=column_name, y=value_measure, hue=type_area, dodge=True)
        
        plt.title(fig_title)
        
        plt.xlabel(column_name)
        plt.ylabel(filter_by)
        
        plt.xticks(rotation=0, ha="right", color="white")
        plt.yticks(color="white")
        
        plt.legend(title=type_area, bbox_to_anchor=(1.05, 1), loc="upper left")
        
        return visual

    def donut_visual(self, data: pd.DataFrame, grouping_type: str, col_name: str, in_percent=False):
        '''
        Provides Donut Chart visualization.

        Inputs:
        - data: Dataframe object
        - grouping_type: Column Name as string value to groupby
        - col_name 

        Output:
        - Plotly Donut Chart
        '''
        if in_percent:
            totals = data[grouping_type].sum()
            data = data.copy()
            data["Percentage"] = data[grouping_type] / totals * 100

        do_chart = px.pie(data, values=grouping_type, names=col_name, hole=0.5)

        do_chart.update_traces(textposition='inside', textinfo='percent')
        do_chart.update_layout(
            margin=dict(l=0, r=0, t=50, b=10),
            height=350,
            template="plotly_dark",
            hovermode="closest",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        return do_chart

    def generate_heatmap(self, x: str, y: str, color_by: str, title: str, pivot_table: pd.DataFrame) -> go.Heatmap:
        '''
        Produce a heatmap visual from plotly.objects

        Input:
        - x: Values for the x-axis
        - y: Vertical Scale values (y-axis)
        - color_by: define the legend to color by
        - title
        - pivot_table: pivot table dataframe retrieved from the EDA

        Output:
        - Heatmap
        '''
        visual = px.imshow(pivot_table, labels={"x": x, "y": y, "color": color_by}, title=title)

        visual.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin={"l":0, "r":0, "t": 40, "b":10},
            height=300,
            template="plotly_dark",
            hovermode="closest"
        )
        # visual.show()
        return visual


    def grouped_bar_plot(self, data: pd.DataFrame, max_value: int, X: str, y: str, color_by: str, title: str, color_sequence: list[str], barmode="group") -> pd.DataFrame:
        '''
        Provides a coupled bar plot visualization of all Quarterly generations of data from the Security Benefits DataFrame

        Inputs:
        - data: pd.DataFrame
        - max_value: y_axis range value
        - X: DataFrame column for horizontal axis
        - y: DataFrame column for vertical axis
        - title
        - color_by: legend to differentiate each data bar
        - colorsequence: iterable to segregate each bar color
        - barmode: "group" default
        '''
        visual = px.bar(data, x=X, y=y, color=color_by, barmode=barmode, 
                        labels={y: y, X: X}, title=title,
                        color_discrete_sequence=color_sequence
                        )
        
        visual.update_yaxes(range=[0, max_value], tick0=0, dtick=(max_value // 5))

        visual.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin={"l":0, "r":0, "t":40, "b":10},
            height=800,
            template="plotly_dark",
            hovermode="closest"
        )

        # visual.show()
        return visual

    def line_progression_chart(self, data: pd.DataFrame, X: str, y: str, hue: str, title: str):
        '''
        A line plot for the Subsistence payments dataset

        Inputs:
        - data: pd.Dataframe object
        - X: Horizontal axis column value
        - y: Vertical axis column value
        - hue: color by column specification
        - title
        '''
        visual = px.line(data, x=X, y=y, color=hue, title=title)

        visual.update_layout(
            xaxis_title=X,
            yaxis_title=y,
            legend_title=hue,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin={"l":0, "r":0, "t":40, "b":10},
            height=800,
            template="plotly_dark",
            hovermode="closest"
        )
        return visual
