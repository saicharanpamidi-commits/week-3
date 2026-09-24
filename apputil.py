import seaborn as sns
import pandas as pd
import numpy as np


# Exercise 3 data. the task functions take no arguments, so the
# data is loaded once here, when the file is imported.
URL = ("https://raw.githubusercontent.com/melaniewalsh/"
       "Intro-Cultural-Analytics/master/book/data/"
       "bellevue_almshouse_modified.csv")

df_bellevue = pd.read_csv(URL)


# Exercise 1
def fibonacci(n):
    """Return the nth number of the Fibonacci series."""

    # base case: fibonacci(0) is 0, fibonacci(1) is 1
    if n < 2:
        return n

    # no print in here. this calls itself thousands of times and
    # would flood the screen.
    return fibonacci(n - 1) + fibonacci(n - 2)


# Exercise 2
def to_binary(n):
    """Return the binary representation of an integer."""

    # 0 and 1 are already binary
    if n < 2:
        return n

    # n % 2 is the last binary digit and n // 2 is everything before
    # it. multiply the front part by 10 to make room for that digit.
    return to_binary(n // 2) * 10 + n % 2


# Exercise 3
def clean_gender(df):
    """Replace the junk values in the gender column with NaN."""

    # gender should only be 'm' or 'w'. '?', 'g' and 'h' are typos,
    # and pandas won't count them as missing unless we swap them out.
    df = df.copy()
    df['gender'] = df['gender'].replace(['?', 'g', 'h'], np.nan)
    return df


def task_1():
    """List the column names, fewest missing values first."""

    print("--- Exercise 3, task 1 ---")

    print("Messy data: gender shows 0 missing values, but look at "
          "what's in it:")
    print(df_bellevue['gender'].value_counts().to_string())
    print("'?', 'g' and 'h' are typos. Pandas treats them as real "
          "values because they're strings, not NaN.")
    print("After cleaning, gender goes from 0 missing to 5.")

    df = clean_gender(df_bellevue)
    missing = df.isna().sum().sort_values()

    print("Missing values per column, after cleaning:")
    print(missing.to_string())

    return list(missing.index)


def task_2():
    """Count the admissions for each year in the data."""

    print("--- Exercise 3, task 2 ---")

    df = df_bellevue.copy()

    print(f"Messy data: date_in is stored as {df['date_in'].dtype}, "
          f"not a date, so it gets converted first.")
    df['year'] = pd.to_datetime(df['date_in']).dt.year

    counts = df.groupby('year').size()
    result = counts.reset_index(name='total_admissions')

    print(f"Found {len(result)} years in the data.")

    return result


def task_3():
    """Return the average age for each gender."""

    print("--- Exercise 3, task 3 ---")

    missing_age = df_bellevue['age'].isna().sum()
    print(f"Messy data: {missing_age} rows have no age. mean() "
          f"skips them.")
    print("Junk gender values are dropped first, so only 'm' and "
          "'w' are averaged.")

    df = clean_gender(df_bellevue)
    return df.groupby('gender')['age'].mean()


def task_4():
    """Return the 5 most common professions, most common first."""

    print("--- Exercise 3, task 4 ---")

    missing_job = df_bellevue['profession'].isna().sum()
    print(f"Messy data: {missing_job} rows have no profession.")
    print("'married', 'spinster' and 'widow' aren't jobs either. For "
          "a lot of the women, the clerk wrote down marital status "
          "instead of a profession.")

    # value_counts() already sorts most common first
    counts = df_bellevue['profession'].value_counts()
    return list(counts.head(5).index)