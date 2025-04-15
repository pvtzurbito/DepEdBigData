import pandas as pd

def cleaned_data():
    # Load and drop unnecessary data
    df = pd.read_csv('data/SY 2023-2024 School Level Data on Official Enrollment 13.csv', encoding='latin-1', skiprows=4)
    df = df.dropna()
    df = df.drop_duplicates()
    df = df.drop(columns="Street Address")

    # Clean the "School Name" column
    def clean_school_name(name):
        """Replaces school name abbreviations with full forms using string replacement."""
        name = name.replace(" ES", " Elementary School").replace(" HS", " High School")
        name = name.replace(" SHS", " Senior High School")
        return name.strip()

    df["School Name"] = df["School Name"].apply(clean_school_name)

    # Fix capitalization
    columns_to_fix = ['Municipality', 'Province', 'Barangay']
    for column in columns_to_fix:
        df[column] = df[column].str.title()

    return df
