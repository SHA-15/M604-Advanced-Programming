from visualizations import eda
from visualizations import plots


public = eda.PublicAssistance("data/public_assistance.csv", ";", 5, 7)

public.file_processing(["Year", "Länder", "TypeCode", "PublicAssistance", "Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"])

public.dtype_conversion("Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)")

public.filter_data()

public.data_group(cols=["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"], group_element="Länder")
public.data_group(cols=["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"], group_element="PublicAssistance")

print(public.Länder_df.tail(16))
'''
public_assistance = plots.Visuals()

public_assistance.choropleth_figure(dataframe=public.Länder_df, dimensions_url="https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/2_bundeslaender/1_sehr_hoch.geo.json", 
locations="Länder", 
color="NetExpenditure(TEUR)", 
labels={"NetExpenditure(TEUR)": "Net Expenditure in Thousand Euros"}, 
title="Net Expenditure By State in Deutschland", 
range_color=(0, public.Länder_df["NetExpenditure(TEUR)"].max(),
))

public_assistance.sorted_df_visual(data=public.PublicAssistance_df, sort_by="PublicAssistance", asc_order=True)

public_assistance.bar_plot_visual(data=public.df, column_name="PublicAssistance", filter_by="Subsistence payments", fig_title="Revenue by Public Assistance and Länder", value_measure="Revenue(TEUR)")

public_assistance.donut_visual(data=public.PublicAssistance_df, grouping_type="NetExpenditure(TEUR)", col_name="PublicAssistance", title="Total Net Expenditure by Public Assistance (% of Total)", in_percent=True)
'''

'''
# Second Dataset

basic_security = eda.BasicSecurity("data/basic_security_benefits.csv", ";", 6, 4)

basic_security.file_processing(["Länder", "Gender", "Q1", "Q2", "Q3", "Q4"])

basic_security.dtype_conversion("Q1", "Q2", "Q3", "Q4")

basic_security.filter_data()

basic_security.pivot_table(columns=["Q1", "Q2", "Q3", "Q4"], group_element=["Länder", "Gender"], values="Total", index="Gender", column_header="Länder")

print("\nNow Look Down!")
print(basic_security.LänderGender_df.head())
print("\nNow Look at pivot")
print(basic_security.pivot_table.head())
basics = plots.Visuals()

basic_security.data_group(cols=["Q1", "Q2", "Q3", "Q4"], group_element="Gender", include_total=True)

melted_df, max_quarterly_value = basic_security.max_quarterly_assessment(data=basic_security.LänderGender_df, cols=["Länder", "Q1", "Q2", "Q3", "Q4"], var_assignment="Quarter", value_name="Value")

basics.donut_visual(data=basic_security.Gender_df, grouping_type="Total", col_name="Gender", title="Total Basic Security Benefits Recipients by Gender")

basics.generate_heatmap(x="Länder", y="Gender", color_by="Total Value", title="Total Recipients of Basic Security Benefits", pivot_table=basic_security.pivot_table)

basics.grouped_bar_plot(data=melted_df, max_value=max_quarterly_value, X="Länder", y="Value", color_by="Quarter", title="Quarterly Values for Each Länder", color_sequence=["purple", "blueviolet", "lightblue", "azure"])
'''
