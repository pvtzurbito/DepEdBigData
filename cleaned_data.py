import pandas as pd
import io
import base64

def cleaned_data(csv_string=None):
    # If csv_string is provided, read from it; else, read from file
    if csv_string is not None: 
        decoder = base64.b64decode(csv_string)
        df = pd.read_csv(io.StringIO(decoder.decode('utf-8')), skiprows=4)
    else:
        df = pd.read_csv('data/SY 2023-2024 School Level Data on Official Enrollment 13.csv', encoding='latin-1', skiprows=4)
    
    df = df.dropna()
    df = df.drop_duplicates()
    if "Street Address" in df.columns:
        df = df.drop(columns="Street Address")

    # Clean the "School Name" column
    def clean_school_name(name):
        """Replaces school name abbreviations with full forms using string replacement."""
        name = name.replace(" ES", " Elementary School").replace(" HS", " High School")
        name = name.replace(" SHS", " Senior High School")
        name = name.replace(" NHS", " National High School")
        name = name.replace(" MNHS", " Memorial National High School")
        name = name.title()
        return name

    df["School Name"] = df["School Name"].apply(clean_school_name)

    # Fix capitalization
    columns_to_fix = ['Municipality', 'Province', 'Barangay']
    for column in columns_to_fix:
        if column in df.columns:
            df[column] = df[column].str.title()
    
    # Add ES, JHS, SHS columns if the necessary columns exist
    if all(col in df.columns for col in ['K Male', 'K Female', 'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female', 'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female', 'G6 Male', 'G6 Female']):
        df['ES'] = df['K Male'] + df['K Female'] + df['G1 Male'] + df['G1 Female'] + df['G2 Male'] + df['G2 Female'] + df['G3 Male'] + df['G3 Female'] + df['G4 Male'] + df['G4 Female'] + df['G5 Male'] + df['G5 Female'] + df['G6 Male'] + df['G6 Female']
    if all(col in df.columns for col in ['G7 Male', 'G7 Female', 'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female', 'JHS NG Male', 'JHS NG Female']):
        df['JHS'] = df['G7 Male'] + df['G7 Female'] + df['G8 Male'] + df['G8 Female'] + df['G9 Male'] + df['G9 Female'] + df['G10 Male'] + df['G10 Female'] + df['JHS NG Male'] + df['JHS NG Female']
    df['SHS'] = df.filter(regex='G1[1-2]|ACAD|ABM|HUMSS|GAS|STEM|TVL|ARTS').sum(axis=1)

    return df