import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dropping null, duplicates, and unnecessary column
df = pd.read_csv('data/SY 2023-2024 School Level Data on Official Enrollment 13.csv', encoding='latin-1', skiprows=4)
df = df.dropna()
df = df.drop_duplicates()
df = df.drop(columns = "Street Address")

# Cleaning the "School Name" column to make it uniform
def clean_school_name(name):
  """Replaces school name abbreviations with full forms using string replacement."""
  name = name.replace(" ES", " Elementary School").replace(" HS", " High School")
  name = name.replace(" SHS", " Senior High School")
  return name.strip()
df["School Name"] = df["School Name"].apply(clean_school_name)

# Fixing capitalization
columns_to_fix = ['Municipality', 'Province', 'Barangay']
for column in columns_to_fix:
  df[column] = df[column].str.title()

def total_student_chart(df):
    #Question: Learners per grade level
    student_count={
    'Kindergarten': ['K Male', 'K Female'],
    'Grade 1': ['G1 Male', 'G1 Female'],
    'Grade 2': ['G2 Male', 'G2 Female'],
    'Grade 3': ['G3 Male', 'G3 Female'],
    'Grade 4': ['G4 Male', 'G4 Female'],
    'Grade 5': ['G5 Male', 'G5 Female'],
    'Grade 6': ['G6 Male', 'G6 Female'],
    'Grade 7': ['G7 Male', 'G7 Female'],
    'Grade 8': ['G8 Male', 'G8 Female'],
    'Grade 9': ['G9 Male', 'G9 Female'],
    'Grade 10': ['G10 Male', 'G10 Female'],
    'Grade 11': ['G11 ACAD - ABM Male', 'G11 ACAD - HUMSS Male', 'G11 ACAD STEM Male', 'G11 ACAD GAS Male', 'G11 ACAD PBM Male', 'G11 TVL Male', 'G11 SPORTS Male', 'G11 ACAD - ABM Female', 'G11 ACAD - HUMSS Female', 'G11 ACAD STEM Female', 'G11 ACAD GAS Female', 'G11 ACAD PBM Female', 'G11 TVL Female', 'G11 SPORTS Female'],
    'Grade 12': ['G12 ACAD - ABM Male', 'G12 ACAD - HUMSS Male', 'G12 ACAD STEM Male', 'G12 ACAD GAS Male', 'G12 ACAD PBM Male', 'G12 TVL Male', 'G12 SPORTS Male', 'G12 ACAD - ABM Female', 'G12 ACAD - HUMSS Female', 'G12 ACAD STEM Female', 'G12 ACAD GAS Female', 'G12 ACAD PBM Female', 'G12 TVL Female', 'G12 SPORTS Female'],
    'SNEd JHS' : ['JHS NG Male', 'JHS NG Female']
    }

    student_total = {}
    for grade, columns in student_count.items():
        df[columns[0]] = pd.to_numeric(df[columns[0]]).fillna(0)
        df[columns[1]] = pd.to_numeric(df[columns[1]]).fillna(0)
        student_total[grade] = df[columns[0]].sum()+df[columns[1]].sum()
        student_total = dict(sorted(student_total.items(), key=lambda item: item[1], reverse=False))
    
    colors=[]
    for grade in student_total.keys():
        if "Kindergaten" in grade:
           colors.append('#000249')
        elif "Grade 1" in grade or "Grade 2" in grade or "Grade 3" in grade or "Grade 4" in grade or "Grade 5" in grade or "Grade 6" in grade:
           colors.append('#0F4392')
        elif "Grade 7" in grade or "Grade 8" in grade or "Grade 9" in grade or "Grade 10" in grade:
           colors.append('#FF4949')
        else:
           colors.append('#DD1717')
    
    chart1 = go.Figure(data=[
       go.Bar(y = list(student_total.keys()),
              x = list(student_total.values()), 
              orientation='h',
              marker_color = colors
              )
    ])


    chart1.update_layout(
        yaxis_title="Grade Level",
        xaxis_title="Number of Learners",
        xaxis_tickangle=-90,
        title = 'Number of Enrollees per Grade Level'
    )

    return chart1


def top_enrollees(df):
    enrollment_columns = [
        'K Male', 'K Female', 'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
        'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
        'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female',
        'G7 Male', 'G7 Female', 'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female',
        'G10 Male', 'G10 Female', 'JHS NG Male', 'JHS NG Female',
        'G11 ACAD - ABM Male', 'G11 ACAD - ABM Female',
        'G11 ACAD - HUMSS Male', 'G11 ACAD - HUMSS Female',
        'G11 ACAD STEM Male', 'G11 ACAD STEM Female',
        'G11 ACAD GAS Male', 'G11 ACAD GAS Female',
        'G11 ACAD PBM Male', 'G11 ACAD PBM Female',
        'G11 TVL Male', 'G11 TVL Female',
        'G11 SPORTS Male', 'G11 SPORTS Female',
        'G11 ARTS Male', 'G11 ARTS Female',
        'G12 ACAD - ABM Male', 'G12 ACAD - ABM Female',
        'G12 ACAD - HUMSS Male', 'G12 ACAD - HUMSS Female',
        'G12 ACAD STEM Male', 'G12 ACAD STEM Female',
        'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
        'G12 ACAD PBM Male', 'G12 ACAD PBM Female',
        'G12 TVL Male', 'G12 TVL Female',
        'G12 SPORTS Male', 'G12 SPORTS Female',
        'G12 ARTS Male', 'G12 ARTS Female'
        ]


        # Sum across all grade level columns to get total enrollees per school
    df["Total Enrollees"] = df[enrollment_columns].sum(axis=1)

        # Group by region to get the total per region
    region_totals = df.groupby("Region")["Total Enrollees"].sum().reset_index()

        # Find region with the most enrollees
    top_region = region_totals.loc[region_totals["Total Enrollees"].idxmax()]
    bot_region = region_totals.loc[region_totals['Total Enrollees'].idxmin()]


    top_region['Total Enrollees'] = f'{top_region['Total Enrollees']:,}'
    bot_region['Total Enrollees'] = f'{bot_region['Total Enrollees']:,}'
    
    return top_region, bot_region


def total_enrollees_and_schools(df):
   # Define grade-level columns
    preschool_cols = df.filter(like="K ").columns
    elementary_cols = df.filter(regex="G[1-6] ").columns
    jhs_cols = df.filter(regex="G(7|8|9|10) ").columns
    SNEd_cols = df.filter(regex="JHS NG ").columns
    shs_cols = df.filter(regex="G(11|12) ").columns
    
    # Summarize enrollment counts per level
    df["Preschool"] = df[preschool_cols].sum(axis=1)
    df["Elementary"] = df[elementary_cols].sum(axis=1)
    df["JHS"] = df[jhs_cols].sum(axis=1)
    df["SNEd"] = df[SNEd_cols].sum(axis=1)
    df["SHS"] = df[shs_cols].sum(axis=1)
    
    # Calculate total enrollment per row
    df['Total Enrollment'] = df[['Preschool', 'Elementary', 'JHS', 'SNEd', 'SHS']].sum(axis=1)
    
    # Sum total enrollment across all rows
    overall_total = df['Total Enrollment'].sum()
    overall_total = f"{overall_total:,}"

    #Count of Schools
    school_count = df['School Name'].count()
    school_count = f"{school_count:,}"

    return overall_total, school_count

def school_types(df):
    # Combining columns "School Subclassification" and "Modifiec COC" for categorization
    df['School Type Combined'] = df['School Subclassification'] + ' ' + df['Modified COC']
    
    # Counting the number of schools per type
    school_type_counts = df.groupby(['School Type Combined', 'Sector']).size().reset_index(name='Number of Schools')
    
    #for descending order
    school_type_counts = school_type_counts.sort_values(by='Number of Schools', ascending = False)
    
    # Display as Table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=list(school_type_counts.columns),
                    fill_color='lightgray',
                    align='left',
                    line_color='black', 
                    font=dict(size=12, color='black')),
        cells=dict(values=[school_type_counts[col] for col in school_type_counts.columns],
                fill_color='white',
                align='left',
                line_color='black', 
                font=dict(size=11)))
    ])

    table_fig.update_layout(height=600, title  = 'Types and Number of School per Type')
    return table_fig