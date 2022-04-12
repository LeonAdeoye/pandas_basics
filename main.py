import pandas as pd
from numpy import NAN

df = pd.DataFrame(
    {
        "Name": [
            "Braund, Mr. Owen Harris",
            "Allen, Mr. William Henry",
            "Bonnell, Miss. Elizabeth",
            "Adeoye Chloe Harper Shiori",
            "Adeoye Ethan Horatio",
            "Adeoye Saori",
            "Adeoye Leon"
        ],
        "Class": [1, 1, 2, 2, 2, 2, 3],
        "Age": [22, 35, 58, 5, 12, 47, 49],
        "Sex": ["male", "male", "female", "female", "male", "female", "male"]
    }
)


def dataframe_basic():
    df.to_json("titanic.json")
    result = pd.read_json("titanic.json")
    print(f'After writing and reading a JSON file:\n{result}')
    # When selecting a single column of a pandas DataFrame, the result is a pandas Series.
    # To select the column, use the column label in between square brackets [].
    print(df["Age"])
    # You can create a Series from scratch as well:
    family_ages = pd.Series([12, 5, 49, 47], name="Age")
    print(family_ages)
    print(f'\nThe maximum age in the family is: {family_ages.max()}')
    print(f'describe the family_ages series: {family_ages.describe()}')
    print(f'Shape of the family_ages series: {family_ages.shape}')
    print(f'Head of the family_ages series:\n{family_ages.head()}')
    print(f'The result of df[["Age", "Sex"]].shape: {df[["Age", "Sex"]].shape}')


def dataframe_filtering():
    # To select rows based on a conditional expression, use a condition inside the selection brackets [].
    print(f'df[df["Age"] >= 35] = {df[df["Age"] >= 35]}')
    # Returns true or false if age less than 35
    print(f'df["Age"] < 35 =\n{df["Age"] < 35}')
    # Similar conditional expression, the isin() function returns True for each row the values are in the provided list.
    # To filter the rows based on such a function, use the conditional function inside the selection brackets [].
    # In this case, the condition inside the selection brackets checks for which rows the class column is either 2 or 3.
    print(f'\ndf[df["Class"].isin([1, 3])] =\n{df[df["Class"].isin([1, 3])]}')
    # The above is equivalent to filtering for class = 2 or 3 and combining the two statements with | operator:
    print(f'\ndf[(df["Class"] == 2) | (df["Class"] == 3)] ={df[(df["Class"] == 1) | (df["Class"] == 3)]}')
    # The loc/iloc operators are required in front of the selection brackets [].
    # When using loc/iloc, the part before the comma is the rows you want,
    # and the part after the comma is the columns you want to select.
    # Use the loc attribute to return one or more specified row(s)
    print(f'\ndf.loc[df["Age"] > 35, "Name"] =\n{df.loc[df["Age"] > 35, "Name"]}')
    # When specifically interested in certain rows and/or columns based on their position in the table,
    # use the iloc operator in front of the selection brackets [].
    print(f'\ndf.iloc[1:4, 1: 2] =\n{df.iloc[1:4, 1: 3]}')
    print(df.loc[[0, 1]])


def dataframe_derived():
    # To create a new column, use the [] brackets with the new column name on the left side of the assignment.
    df["Class_Cost"] = df["Class"] * 1000
    df["unit"] = df["Class_Cost"] / df["Class"]
    df_renamed = df.rename(
        columns={
            "Class": "Class_Level",
            "Class_Cost": "Cost"
        }
    )
    print(f'\n{ + df_renamed.head(6)}')
    print(df.head(2))


def dataframe_summary():
    print(f'\ndf[["Age", "Class_Cost"]].mean() =\n{df[["Age", "Class_Cost"]].mean()}')
    # Average age for male versus female
    print(f'\nAverage age grouped by sex => df[["Sex", "Age"]].groupby("Sex").mean() =\n{df[["Sex", "Age"]].groupby("Sex").mean()}')
    # In the previous example, we explicitly selected the 2 columns first.
    # If not, the mean method is applied to each column containing numerical columns:
    print(f'\nAverage of all numerical values grouped by sex: df.groupby("Sex").mean() =\n{df.groupby("Sex").mean()}')
    print(df.groupby("Sex")["Class_Cost"].mean())
    # The value_counts() method counts the number of records for each category in a column.
    print(df["Class"].value_counts())
    # Above is a shortcut, as it's actually a groupby combined with counting the number of records within each group:
    print(df.groupby("Class")["Class"].count())


def dataframe_cleaning():
    dirty_df = pd.read_csv("dirtydata.csv")
    # One way to deal with empty cells is to remove rows that contain empty cells.
    # Removing a few rows will not have a big impact on the result.
    # By default, the dropna() method returns a new DataFrame, and will not change the original.
    # If you want to change the original DataFrame, use the inplace = True argument
    dirty_df.dropna(inplace=True)
    # Another way of dealing with empty cells is to insert a new value instead.
    # This way you do not have to delete entire rows just because of some empty cells.
    # The fillna() method allows us to replace empty cells with a value:
    dirty_df.fillna(130, inplace=True)
    # To only replace empty values for one column, specify the column name for the DataFrame:
    dirty_df["Calories"].fillna(130, inplace=True)
    # A common way to replace empty cells, is to calculate the mean, median or mode value of the column.
    # Pandas uses the mean() median() and mode() methods to calculate the respective values for a specified column:
    mean_value = dirty_df["Calories"].mean()
    dirty_df["Calories"].fillna(mean_value, inplace=True)
    # One way to fix wrong values is to replace them with something else.
    # To replace wrong data for larger data sets you can create some rules.
    # For example, set some boundaries for legal values, and replace any values that are outside the boundaries.
    for x in dirty_df.index:
        if dirty_df.loc[x, "Duration"] > 60:
            dirty_df.loc[x, "Duration"] = 60
    # Another way of handling wrong data is to remove the rows that contain wrong data.
    for x in dirty_df.index:
        if dirty_df.loc[x, "Duration"] > 60:
            dirty_df.drop(x, inplace=True)
    # To discover duplicates, we can use the duplicated() method.
    # The duplicated() method returns a Boolean values for each row:
    print(dirty_df.duplicated())
    # To remove duplicates:
    dirty_df.drop_duplicates(inplace=True)
    # The result from the converting in the example below gave us a NaT value, which can be handled as a NULL value,
    # and we can remove the row by using the dropna() method.
    dirty_df['Date'] = pd.to_datetime(dirty_df['Date'])
    # Remove rows with a NULL value in the "Date" column:
    dirty_df.dropna(subset=['Date'], inplace=True)
    print(dirty_df)


def dataframe_from_dict_with_various_operations():
    dictionary = {'col1': [100, NAN, NAN, NAN, 5, 6, 6, 6, 2, 77], 'col2': [4, 5, NAN, 7, 8, 9, 1, 1, 7, 7], 'country': ['Japan', 'Brazil', 'Cuba', 'Vietnam', 'Thailand', 'Singapore', 'Hong Kong', 'France', 'Italy', 'Brazil']}
    dataframe = pd.DataFrame.from_dict(dictionary)
    print(dataframe.head(6))
    print(f'\nThe first column values of the dataframe created from a dictionary are:\n{dataframe.col1}')
    print(f'\nThe first and second column values of the dataframe can be accessed using an array of column names:\n{dataframe[["col1", "col2"]] }')
    # To get unique values in a column:
    print(dataframe.col1.unique())
    # Filter rows using an AND clause of two different values:
    print(f'Filter on specific values across columns => dataframe[(dataframe.col1 == 6) & (dataframe.col2 == 1)]: {dataframe[(dataframe.col1 == 6) & (dataframe.col2 == 1)]}')
    print(f'Get the first row (0) and first column (0) cell value => dataframe.iloc[0, 0]: {dataframe.iloc[0, 0]}')
    print(f'Get the last row (-1) and the first column (0) cell value => dataframe.iloc[-1, 0]:{dataframe.iloc[-1, 0]}')
    print(f'Get the last row (-1) and last column (-1) cell value => dataframe.iloc[-1, -1]: {dataframe.iloc[-1, -1]}')
    print(f'Get rows 4 to 5 (3:6) and last column (-1) cell value => dataframe.iloc[3:6, -1]:\n{dataframe.iloc[3:6, -1]}')

    # Instead of 0-based integer index, you can create your own index "in place" in a copy of you dataframe.
    country_dataframe = dataframe.copy()
    country_dataframe.set_index('country', inplace=True)
    print(country_dataframe.head())
    print(f'Get the first row (0) and first column (0) cell value => country_dataframe.iloc[0, 0]: {country_dataframe.iloc[0, 0]}')
    print(f'Get the last row (-1) and the first column (0) cell value => country_dataframe.iloc[-1, 0]: {country_dataframe.iloc[-1, 0]}')
    print(f'Get the last row (-1) and last column (-1) cell value => country_dataframe.iloc[-1, -1]: {country_dataframe.iloc[-1, -1]}')
    print(f'Get rows 4 to 5 (3:6) and last column (-1) cell value => country_dataframe.iloc[3:6, -1]:\n{country_dataframe.iloc[3:6, -1]}')
    print(f'get all rows with brazil in country using index:\n{country_dataframe.loc["Brazil"]}')
    print(f'get a summary of null column values (Numpy.NAN) => country_dataframe.isnull().sum():\n{country_dataframe.isnull().sum()}')
    country_dataframe.dropna(inplace=True)
    print(f'get a summary of null column values (Numpy.NAN) => country_dataframe.isnull().sum():\n{country_dataframe.isnull().sum()}')
    # Condition-based updating using apply function and lambda
    country_dataframe["lambda_binary"] = country_dataframe["col1"].apply(lambda x: 1 if x % 2 == 0 else 0)
    print(f'Run head on specific value == 0:\n{country_dataframe[country_dataframe["lambda_binary"] == 0].head()}')
    print(f'Run head on specific value == 1:\n{country_dataframe[country_dataframe["lambda_binary"] == 1].head()}')
    # Output dataframe:
    country_dataframe.to_json('countries.json')
    print(country_dataframe.to_json())
    country_dataframe.to_csv('countries.csv')
    print(country_dataframe.to_csv())
    country_dataframe.to_html('countries.html')
    print(country_dataframe.to_html())
    # To delete a dataframe
    del country_dataframe


if __name__ == '__main__':
    dataframe_basic()
    dataframe_filtering()
    dataframe_derived()
    dataframe_summary()
    dataframe_cleaning()
    dataframe_from_dict_with_various_operations()



