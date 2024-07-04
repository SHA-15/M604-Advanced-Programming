from .eda import PublicAssistance, BasicSecurity
from .plots import Visuals

# Public Assistance Dataframe
pa = PublicAssistance("data/public_assistance.csv", ";", 5, 7)
pa.file_processing(["Year", "Länder", "TypeCode", "PublicAssistance", "Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"])
pa.dtype_conversion("Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)")
pa.filter_data()
pa.data_group(cols=["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"], group_element="Länder")
pa.data_group(cols=["Expenditure(TEUR)", "Revenue(TEUR)", "NetExpenditure(TEUR)"], group_element="PublicAssistance")

# Basic Security Benefits DataFrame
bsc = BasicSecurity("data/basic_security_benefits.csv", ";", skiprows=6, skipfooter=4)
bsc.file_processing(["Länder", "Gender", "Q1", "Q2", "Q3", "Q4"])
bsc.dtype_conversion("Q1", "Q2", "Q3", "Q4")
bsc.filter_data()
bsc.pivot_table(columns=["Q1", "Q2", "Q3", "Q4"], group_element=["Länder", "Gender"], values="Total", index="Gender", column_header="Länder")
bsc.data_group(cols=["Q1", "Q2", "Q3", "Q4"], group_element="Gender", include_total=True)
melted_df, max_quarterly_value = bsc.max_quarterly_assessment(data=bsc.LänderGender_df, cols=["Länder", "Q1", "Q2", "Q3", "Q4"], var_assignment="Quarter", value_name="Value")



# Subsistence Benefit Recipients Dataframe
sub_benefits = eda.Subsistence(path_to_file="data/subsistence_benefits.csv", delimiter=";", skiprows=7, skipfooter=4)
sub_benefits.file_processing()
sub_benefits.dtype_conversion("Year", "Non-Institution German Males",
                              "Non-Institution Foreign Males",
                              "Total Non-Insitution Males",
                              "Institution German Males",
                              "Insitution Foreign Males",
                              "Total Institution Males",
                              "Total German Males",
                              "Total Foreign Males",
                              "Total Males",
                              "Non-Institution German Females",
                              "Non-Institution Foreign Females",
                              "Total Non-Insitution Females",
                              "Institution German Females",
                              "Insitution Foreign Females",
                              "Total Institution Females",
                              "Total German Females",
                              "Total Foreign Females",
                              "Total Females",
                              "Non-Institution Germans Total",
                              "Non-Institution Foreign Total",
                              "Non-Institution Total",
                              "Institution Germans Total",
                              "Institution Foreign Total",
                              "Institution Total",
                              "Germans Total",
                              "Foreign Total",
                              "Total",
                              )
sub_benefits.filter_data(year_start=2010, year_end=2022)

# Visualizations Module
public_assist = Visuals()
basics = Visuals()
subsistence = Visuals()



