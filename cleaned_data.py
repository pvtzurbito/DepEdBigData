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
    
    df['ES'] = df['K Male'] + df['K Female'] + df['G1 Male'] + df['G1 Female'] + df['G2 Male'] + df['G2 Female'] + df['G3 Male'] + df['G3 Female'] + df['G4 Male'] + df['G4 Female'] + df['G5 Male'] + df['G5 Female'] + df['G6 Male'] + df['G6 Female']
    df['JHS'] = df['G7 Male'] + df['G7 Female'] + df['G8 Male'] + df['G8 Female'] + df['G9 Male'] + df['G9 Female'] + df['G10 Male'] + df['G10 Female'] + df['JHS NG Male'] + df['JHS NG Female']
    df['SHS'] = df.filter(regex='G1[1-2]|ACAD|ABM|HUMSS|GAS|STEM|TVL|ARTS').sum(axis=1)

    return df