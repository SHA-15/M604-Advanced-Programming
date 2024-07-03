'''
EDA and Visualizations for the streamlit application. This section manipulates the different datasets altogether and provides the visualizations for retrieval.
'''
import chardet
import pandas as pd

class Dataset:
    '''
    Utilize the file management, dataframe libraries to manipulate the provided datasets for analysis. The datasets are cleaned of all malformations using pandas library and provided visualization actions that will present relationships between elements of the dataset.
    '''

    def __init__(self, path_to_file, delimiter, skiprows, skipfooter):
        self.path_to_file  = path_to_file
        self.delimiter = delimiter
        self.skiprows = skiprows
        self.skipfooter = skipfooter

        self.df = None

    def encoding_detection(func):
        def wrapping_function(self, *args, **kwargs):

            with open(self.path_to_file, "rb") as data_file:
                output = chardet.detect(data_file.read())
                encoding = output["encoding"]
                print(f"\nCSV file encoding: {encoding}")

            
            return func(self, encoding, *args, *kwargs)
        return wrapping_function


    def dtype_conversion(self, *args: str) -> pd.DataFrame:
        
        for col in args:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        self.df = self.df.fillna(0)

        print(self.df[list(args)].head(10))

        return self.df
    
    def filter_data(self, region_col="Länder"):

        self.df = self.df[~self.df.apply(lambda r: r.astype(str).str.contains("Total").any(), axis=1)]

        self.df.reset_index(drop=False, inplace=True)

        self.df[region_col] = self.df["Länder"].astype(str)

        print(self.df.head(10))

        return

    def data_group(self, cols: list[str], group_element, include_total=False) -> pd.DataFrame:
        var_name = f"{group_element}_df"

        grouped_data = self.df.groupby(group_element)[cols].sum().reset_index()

        if include_total:
            grouped_data["Total"] = grouped_data[cols].sum(axis=1)

        setattr(self, var_name, grouped_data)

        print(f"\nGrouped DataFrame with sums: \n{grouped_data.head()}")

        return grouped_data
    


class PublicAssistance(Dataset):

    def __init__(self, path_to_file, delimiter, skiprows, skipfooter):
        super().__init__(path_to_file, delimiter, skiprows, skipfooter)
    
    @Dataset.encoding_detection
    def file_processing(self, encoding: str, columns: list[str]) -> pd.DataFrame:
        with open(self.path_to_file, "r", encoding=encoding) as data_file:
            file_contents = data_file.read()
            print("\n", file_contents[:500])


        df = pd.read_csv(self.path_to_file, encoding=encoding, delimiter=self.delimiter, skiprows=self.skiprows, engine="python")
        df.columns = columns

        print("\n", df.head(10))

        self.df = df

    
class BasicSecurity(Dataset):

    def __init__(self, path_to_file, delimiter, skiprows, skipfooter):
        super().__init__(path_to_file, delimiter, skiprows, skipfooter)

    @Dataset.encoding_detection
    def file_processing(self, encoding: str, columns: list[str]) -> pd.DataFrame:
        with open(self.path_to_file, "r", encoding=encoding) as data_file:
            file_contents = data_file.read()
            print("\n", file_contents[:500])


        df = pd.read_csv(self.path_to_file, encoding=encoding, delimiter=self.delimiter, skiprows=self.skiprows, skipfooter=self.skipfooter, engine="python")

        df = df.drop(0).reset_index(drop=True)

        df = df.iloc[:, [0 , 1, 30, 31, 32, 33]]

        df.columns = columns

        print("\n", df.head(10))

        self.df = df

    def modify_for_pivot(func) -> pd.DataFrame:
        def wrapper_function(self, columns: list[str], group_element: list[str], **kwargs) -> pd.DataFrame:
            grouped_data = self.df.groupby(list(group_element))[columns].sum().reset_index()
            
            grouped_data[kwargs["values"]] = grouped_data[columns].sum(axis=1)
            
            setattr(self, f"{group_element[0] + group_element[1]}_df", grouped_data)
            print(f"\nGrouped DataFrame with sums: \n{grouped_data.head()}")

            values = kwargs.get("values")
            index = kwargs.get("index")
            column_header = kwargs.get("column_header")
            
            return func(self, values, index, column_header, grouped_data)
        return wrapper_function
    
    @modify_for_pivot
    def pivot_table(self, values: str, index: str, column_header: str, grouped_data: pd.DataFrame) -> pd.DataFrame:
        
        pivot_table = grouped_data.pivot_table(values=values, index=index, columns=column_header)
        
        setattr(self, "pivot_table", pivot_table)

        print(pivot_table.head(20))

        return pivot_table
    

    def max_quarterly_assessment(self, data: pd.DataFrame, cols: list[str], var_assignment: str, value_name: str) -> pd.DataFrame:

        quarter_view = data[cols]

        max_value = quarter_view[cols[1:]].max().max()

        elongate_df = pd.melt(quarter_view, id_vars=[cols[0]], var_name=var_assignment, value_name=value_name)

        return elongate_df, max_value


class Subsistence(Dataset):

    def __init__(self, path_to_file, delimiter, skiprows, skipfooter):
        super().__init__(path_to_file, delimiter, skiprows, skipfooter)

    @Dataset.encoding_detection
    def file_processing(self, encoding: str) -> pd.DataFrame:
        with open(self.path_to_file, "r", encoding=encoding) as data_file:
            file_contents = data_file.read()
            print("\n", file_contents[:500])

        df = pd.read_csv(self.path_to_file, encoding=encoding, delimiter=';', skiprows=self.skiprows, skipfooter=self.skipfooter, engine="python")

        df.rename(
            columns=
            {
            "Unnamed: 0": "Länder", 
            "Unnamed: 1": "Year",
            "Male": "Non-Institution German Males",
            "Male.1": "Non-Institution Foreign Males",
            "Male.2": "Total Non-Insitution Males",
            "Male.3": "Institution German Males",
            "Male.4": "Insitution Foreign Males",
            "Male.5": "Total Institution Males",
            "Male.6": "Total German Males",
            "Male.7": "Total Foreign Males",
            "Male.8": "Total Males",
            "Female": "Non-Institution German Females",
            "Female.1": "Non-Institution Foreign Females",
            "Female.2": "Total Non-Insitution Females",
            "Female.3": "Institution German Females",
            "Female.4": "Insitution Foreign Females",
            "Female.5": "Total Institution Females",
            "Female.6": "Total German Females",
            "Female.7": "Total Foreign Females",
            "Female.8": "Total Females",
            "Total": "Non-Institution Germans Total",
            "Total.1": "Non-Institution Foreign Total",
            "Total.2": "Non-Institution Total",
            "Total.3": "Institution Germans Total",
            "Total.4": "Institution Foreign Total",
            "Total.5": "Institution Total",
            "Total.6": "Germans Total",
            "Total.7": "Foreign Total",
            "Total.8": "Total",
            "Date": "Year"}, 
            inplace=True)
        
        df = df.iloc[1:]

        df.Year = df["Year"].str[:4]

        self.df = df
        print("This is revised dataframe of the subsistence recipients\n", df.head())


    def filter_data(self, year_start: int, year_end: int) -> pd.DataFrame:
        filtered_df = self.df[self.df["Year"].between(year_start, year_end)]

        setattr(self, "filtered_df", filtered_df)

        print(f"Filtered data between {year_start} & {year_end}\n", filtered_df.head(15))


