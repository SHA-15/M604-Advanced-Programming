'''
This section contributes towards data connection against the dataset .csv files extracted from the GENESIS-Online Database. The Parent and Child Classes adhere to common methods to capture file properties and process the csv files to be converted into Pandas Dataframe Objects
'''
import chardet
import pandas as pd

class Dataset:
    '''
    The Dataset Parent class acts as a baseline for accepting .csv files as input and utilizes encoding detection, data type conversion and numeric datatype filtering to parse data files into visualisable panda DataFrame Objects.
    '''

    def __init__(self, path_to_file: str, delimiter: str, skiprows: str, skipfooter: str) -> None:
        '''
        Instantiates the Dataset object with baseline file parameters:

        Inputs:
        - path_to_file: Provide the relative or absolute file path to retrieve the file
        - delimiter: Provide the special characters (, ; / |) to recognize column separators
        - skiprows: provides the top number of rows in the csv file to ignore
        - skipfooter: provides the bottom number of rows in the csv file to ignore
        '''
        self.path_to_file  = path_to_file
        self.delimiter = delimiter
        self.skiprows = skiprows
        self.skipfooter = skipfooter

        self.df = None

    def encoding_detection(func):
        '''
        A Decorator to retrieve the encoding type of the csv file to be used as input as part of the wrapping function (func)

        Inputs:
        - func: The callback function to be used in the wrapper function
        '''
        def wrapping_function(self, *args, **kwargs):
            try:
                with open(self.path_to_file, "rb") as data_file:
                    output = chardet.detect(data_file.read())
                    encoding = output["encoding"]
                    print(f"\nCSV file encoding: {encoding}")
            except FileNotFoundError as FE:
                print("File {0} was not found, check relative path".format(self.file_to_path))
                return
            except EncodingWarning:
                print("Encoding was not clearly identified")
                return
            finally:
                if encoding:
                    return func(self, encoding, *args, *kwargs)
                else:
                    print("Encoding was not identified from file")
                    return None
        return wrapping_function


    def dtype_conversion(self, *args: str) -> pd.DataFrame:
        '''
        Takes column names of a dataframe as string inputs and converts the datatypes of selected columns into int64

        Inputs:
        - *args: Accepts variable number of columns in the dataset

        Output:
        - pd.DataFrame: Original dataframe with type converted columns
        '''
        try:
            for col in args:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

            self.df = self.df.fillna(0)

            print(self.df[list(args)].head(10))
        except KeyError:
            print("Column value does not correspond to a column in the dataframe")
            return

        return self.df

    def filter_data(self, region_col="Länder"):
        '''
        Use case for row values containing "Total" and filters them out of the dataframe object

        Inputs:
        - region_col: Default set to 'Länder'
        '''
        try:
            self.df = self.df[~self.df.apply(lambda r: r.astype(str).str.contains("Total").any(), axis=1)]

            self.df.reset_index(drop=False, inplace=True)

            self.df[region_col] = self.df["Länder"].astype(str)
        except KeyError as KE:
            print("Column value does not correspond to a column in the dataframe thus filter was not completed")
        finally:
            return self.df

    def data_group(self, cols: list[str], group_element: str, include_total=False) -> pd.DataFrame:
        '''
        Provides a related dataframe dependent upon the "group_element" attribute of the original dataframe.

        Inputs:
        - cols: List of columns to sum when merged through groupby
        - group_element: Name of column to group by
        - include_total: boolean value to introduce a total column in the aggregation, False as default argument.

        Output:
        - Groupby Data Frame object
        '''
        var_name = f"{group_element}_df"
        try:
            grouped_data = self.df.groupby(group_element)[cols].sum().reset_index()

            if include_total:
                grouped_data["Total"] = grouped_data[cols].sum(axis=1)

            setattr(self, var_name, grouped_data)
            print(f"\nGrouped DataFrame with sums: \n{grouped_data.head()}")

            return grouped_data
        except KeyError:
            print(f"column argument {group_element} entered is not part of DataFrame {self.df.columns}")
        finally:
            print("Grouped Function process completed")


class PublicAssistance(Dataset):
    '''
    The child class inheriting from the Dataset class, focusing on the primary dataset public_assistance.
    '''

    def __init__(self, path_to_file, delimiter, skiprows, skipfooter):
        '''
        Instantiates the PublicAssistance class object with the same parameters as defined in the Dataset class with no additions
        '''
        super().__init__(path_to_file, delimiter, skiprows, skipfooter)
    
    @Dataset.encoding_detection
    def file_processing(self, encoding: str, columns: list[str]) -> pd.DataFrame:
        '''
        Utilises the decorator function defined in the Dataset Class to identify file encoding and reads the contents of the files prior to conversion to a dataframe object.
        '''
        try:
            with open(self.path_to_file, "r", encoding=encoding) as data_file:
                file_contents = data_file.read()
                print("\n", file_contents[:500])

            df = pd.read_csv(self.path_to_file, encoding=encoding, delimiter=self.delimiter, skiprows=self.skiprows, engine="python")
            df.columns = columns

            #print("\n", df.head(10))

            replaced_substring_1 = "ttemberg"
            replaced_substring_2 = "ingen"
            change_mechanism_1 = df["Länder"].str.endswith(replaced_substring_1)
            change_mechanism_2 = df["Länder"].str.endswith(replaced_substring_2)

            df.loc[change_mechanism_1, "Länder"] = "Baden-Württemberg"
            df.loc[change_mechanism_2, "Länder"] = "Thüringen"
            self.df = df

            return
        except FileNotFoundError:
            print("{0} File not detected, update the url argument provided".format(self.path_to_file))
            return
    

class BasicSecurity(Dataset):
    '''
    The child class inheriting from the Dataset class, focusing on the primary dataset public_assistance.
    '''
    def __init__(self, path_to_file, delimiter, skiprows, skipfooter):
        '''
        Instantiates the BasicSecurity class object with the same parameters as defined in the Dataset class with no additions
        '''
        super().__init__(path_to_file, delimiter, skiprows, skipfooter)

    @Dataset.encoding_detection
    def file_processing(self, encoding: str, columns: list[str]) -> pd.DataFrame:
        '''
        Utilises the decorator function defined in the Dataset Class to identify file encoding and reads the contents of the files prior to conversion to a dataframe object.

        Additionally, The function reduces the dataframe size by selecting the critical dataframe columns and assigns the dataframe object to the object property.
        '''
        try:
            with open(self.path_to_file, "r", encoding=encoding) as data_file:
                file_contents = data_file.read()
                print("\n", file_contents[:500])


            df = pd.read_csv(self.path_to_file, encoding=encoding, delimiter=self.delimiter, skiprows=self.skiprows, skipfooter=self.skipfooter, engine="python")

            df = df.drop(0).reset_index(drop=True)

            df = df.iloc[:, [0 , 1, 30, 31, 32, 33]]

            df.columns = columns

            replaced_substring_1 = "ttemberg"
            replaced_substring_2 = "ingen"
            change_mechanism_1 = df["Länder"].str.endswith(replaced_substring_1)
            change_mechanism_2 = df["Länder"].str.endswith(replaced_substring_2)

            df.loc[change_mechanism_1, "Länder"] = "Baden-Württemberg"
            df.loc[change_mechanism_2, "Länder"] = "Thüringen"

            self.df = df
        except FileNotFoundError:
            print("{0} File not detected, update the url argument provided".format(self.path_to_file))
            return

    def modify_for_pivot(func) -> pd.DataFrame:
        '''
        Decorator that groups data by defined columns and establish a pivot table in a dataframe.

        Input:
        - func: the callback function to be included in the wrapper function.

        Output:
        - produces the wrapper function with added functionality of the decorator. 
        '''
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
        '''
        Defines a pivot table derived from the original dataframe

        Inputs:
        - values: Pivot Table column "Values"
        - index: Pivot Table column "Index"
        - column header
        - grouped_data: the previously defined dataframe object grouped by

        Output:
        - Pivot Table in a Pandas Dataframe object
        '''
        try:
            pivot_table = grouped_data.pivot_table(values=values, index=index, columns=column_header)
        
            setattr(self, "pivot_table", pivot_table)

            #print(pivot_table.head(10))

            return pivot_table
        except KeyError:
                print(f"column argument {column_header}  & {values} entered is not part of DataFrame {grouped_data}", "Calling Function with baseline Dataset parameters")

    def max_quarterly_assessment(self, data: pd.DataFrame, cols: list[str], var_assignment: str, value_name: str) -> pd.DataFrame:
        '''
        Provides the expanded dataframe object and maximum quarterly values for further visualization

        Inputs:
        - data: the Dataframe object to extract the melted dataframe and max values
        - cols: The list of columns of quarters to attain max values
        - var_assignment: Melted Df parameter for var_name

        Outputs:
        - The Melted dataframe object
        - Maximum value from quarter columns
        '''
        try:
            quarter_view = data[cols]

            max_value = quarter_view[cols[1:]].max().max()

            elongate_df = pd.melt(quarter_view, id_vars=[cols[0]], var_name=var_assignment, value_name=value_name)

            return elongate_df, max_value
        except KeyError:
            print(f"{cols} are not found inside the Dataframe selection")



class Subsistence(Dataset):
    '''
    The Subsistence is deriving attributes and methods from the Parent Dataset class.
    '''
    def __init__(self, path_to_file, delimiter, skiprows, skipfooter):
        '''
        Instantiates the Subsistence class object with the same parameters as defined in the Dataset class with no additions
        '''
        super().__init__(path_to_file, delimiter, skiprows, skipfooter)

    @Dataset.encoding_detection
    def file_processing(self, encoding: str) -> pd.DataFrame:
        '''
        Utilizes the encoding decorator to retrieve the csv files encoding as an input parameter in the wrapper function. Optimizes the csv file to translate into a Dataframe object by removing unnecessary rows and footers.
        '''
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
        
        replaced_substring_1 = "ttemberg"
        replaced_substring_2 = "ingen"
        change_mechanism_1 = df["Länder"].str.endswith(replaced_substring_1)
        change_mechanism_2 = df["Länder"].str.endswith(replaced_substring_2)

        df.loc[change_mechanism_1, "Länder"] = "Baden-Württemberg"
        df.loc[change_mechanism_2, "Länder"] = "Thüringen"

        self.df = df
        #print("This is revised dataframe of the subsistence recipients\n", df.head())


    def filter_data(self, year_start: int, year_end: int) -> pd.DataFrame:
        '''
        Optimizes the dataframe to set as per a specified date range for analysis.

        Inputs:
        - year_start: The starting year range
        - year_end: The final filter year range
        '''
        filtered_df = self.df[self.df["Year"].between(year_start, year_end)]

        setattr(self, "filtered_df", filtered_df)

        #print(f"Filtered data between {year_start} & {year_end}\n", filtered_df.head(15))


