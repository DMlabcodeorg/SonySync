import pandas as pd
import os


def list_csv_files_with_classroom(classroom, directory="."):
    """
    List all .csv files in the specified directory with 'StarFish' in the filename.

    Args:
    - directory (str): The path to the directory to search in. Defaults to the current directory.

    Returns:
    - list: List of filenames that match the criteria.
    """
    # List all files that match the criteria
    csv_files_with_classroom = [f for f in os.listdir(directory) if f.endswith('.csv') and classroom in f]
    return csv_files_with_classroom


def integrate_csv_files(files):
    """
    Integrate multiple CSV files into a single DataFrame and add a column for filenames.

    Args:
    - files (list): List of CSV filenames.

    Returns:
    - DataFrame: Integrated DataFrame.
    """
    df_list = []

    for file in files:
        df = pd.read_csv(file)
        df['filename'] = file
        df_list.append(df)

    integrated_df = pd.concat(df_list, ignore_index=True)
    return integrated_df

if __name__ == "__main__":
    Classroom_list = [['Debbie_School', 'StarFish', ['2022', '2023']], ['Debbie_School', 'LittleFish', ['2022', '2023']], ['Debbie_School', 'LadyBugs', ['2022', '2023']]]
    for school, classroom, year_list in Classroom_list:
        file_list = list_csv_files_with_classroom(classroom)
        classroom_df = integrate_csv_files(file_list)
        classroom_df.to_csv('{}_{}.csv'.format(school, classroom), index=False)

