from .eda import PublicAssistance, BasicSecurity
from .plots import Visuals

pa = PublicAssistance("data/public_assistance.csv", ";", 5, 7)

pa.file_processing(["Year", "Länder", "TypeCode", "PublicAssistance", "Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"])

pa.dtype_conversion("Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)")

pa.filter_data()

pa.data_group(cols=["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"], group_element="Länder")
pa.data_group(cols=["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"], group_element="PublicAssistance")

public_assist = Visuals()
deutschland_map = public_assist.choropleth_figure(
    dataframe=pa.Länder_df,
    dimensions_url="https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/2_bundeslaender/1_sehr_hoch.geo.json", 
    locations="Länder", 
    color="NetExpenditure(TEUR)", 
    labels={"NetExpenditure(TEUR)": "Net Expenditure in Thousand Euros"}, 
    title="Net Expenditure By State in Deutschland", 
    range_color=(0, pa.Länder_df["NetExpenditure(TEUR)"].max())
    )

bsc = BasicSecurity("data/basic_security_benefits.csv", ";", skiprows=6, skipfooter=4)

bsc.file_processing(["Länder", "Gender", "Q1", "Q2", "Q3", "Q4"])

bsc.dtype_conversion("Q1", "Q2", "Q3", "Q4")

bsc.filter_data()

bsc.pivot_table(columns=["Q1", "Q2", "Q3", "Q4"], group_element=["Länder", "Gender"], values="Total", index="Gender", column_header="Länder")

bsc.data_group(cols=["Q1", "Q2", "Q3", "Q4"], group_element="Gender", include_total=True)

melted_df, max_quarterly_value = bsc.max_quarterly_assessment(data=bsc.LänderGender_df, cols=["Länder", "Q1", "Q2", "Q3", "Q4"], var_assignment="Quarter", value_name="Value")

basics = Visuals()
