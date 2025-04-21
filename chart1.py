import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

    color_map = {
        'Kindergarten': '#054a91',
        'Grade 1': '#3e7cb1',
        'Grade 2': '#3e7cb1',
        'Grade 3': '#3e7cb1',
        'Grade 4': '#3e7cb1',
        'Grade 5': '#3e7cb1',
        'Grade 6': '#3e7cb1',
        'Grade 7': '#81a4cd',
        'Grade 8': '#81a4cd',
        'Grade 9': '#81a4cd',
        'Grade 10': '#81a4cd',
        'Grade 11': '#f17300',
        'Grade 12': '#f17300',
        'SNEd JHS': '#81a4cd'
    }
    
    chart1 = go.Figure(data=[
       go.Bar(y = list(student_total.keys()),
              x = list(student_total.values()), 
              orientation='h',
              marker=dict(color=[color_map[grade] for grade in student_total.keys()])
              )
    ])


    chart1.update_layout(
        yaxis_title="Grade Level",
        xaxis_title="Number of Learners",
        xaxis_tickangle=-90,
        title = '<b>Number of Enrollees per Grade Level</b>',
        title_x=0.5,
        margin=dict(t=60, b=20, l=20, r=10),
        title_font=dict(size=17),
        font=dict(family='Inter'),

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

    school_type_counts['Number of Schools'] = school_type_counts['Number of Schools'].apply(lambda x: f"{x:,}")
    
    # Display as Table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=[f"<b><i>{col}</i></b>" for col in school_type_counts.columns],
                align='center',
                font=dict(size=15, color='white'),
                fill_color = '#054a91'
                ),
        cells=dict(values=[school_type_counts[col] for col in school_type_counts.columns],
                align='center',
                font=dict(size=15),
                fill_color = '#dbe4ee'
                ))
    ])

    table_fig.update_layout(
        height=450,
        width=615, 
        title = '<b>Types and Number of School per Type</b>',
        font=dict(family='Inter'),
        title_x=0.5,
        title_font=dict(size=17),
        margin=dict(t=60, b=20, l=10, r=10),
        )
    return table_fig


def schools_top(df):
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
    # Calculate total enrollment for each school by summing the columns
    df['Total Enrollees'] = df[enrollment_columns].sum(axis=1)

    # Sort the dataframe by total enrollment
    sorted_df = df.sort_values(by='Total Enrollees', ascending=False)

    # Find the school with the largest and smallest enrollment
    largest_school = sorted_df.iloc[0]  # School with the largest enrollment
    smallest_school = sorted_df.iloc[-1]  # School with the smallest enrollment

    return largest_school, smallest_school


def pie_chart(df):
        # TOTAL DISTRIBUTION OF MALE AND FEMALE STUDENTS IN THE PHILIPPINES
    # Filter out columns that end with 'Male' or 'Female' for ease of counting
    male_columns = [col for col in df.columns if col.strip().endswith('Male')]
    female_columns = [col for col in df.columns if col.strip().endswith('Female')]
    
    # Sum all male and female students
    total_male = df[male_columns].sum().sum()
    total_female = df[female_columns].sum().sum()
    
    # Prepare the summary DataFrame
    gender_distribution = pd.DataFrame({
        'Gender': ['Male', 'Female'],
        'Total Enrollment': [total_male, total_female]
    })

    colors = ['#054a91', '#f17300'] 
    
    # Create the pie chart with values + percentages visible and no hover
    fig = go.Figure(data=[go.Pie(
        labels=gender_distribution['Gender'],
        values=gender_distribution['Total Enrollment'],
        textinfo='label+value+percent',
        textposition='outside',
        hoverinfo='skip',  # disables hover
        pull=[0.05, 0],
        marker=dict(colors=colors),
        showlegend=False
    )])
    
    fig.update_layout(
        title_text='<b>Total Distribution of Male and Female Students</b>',
        font=dict(family='Inter'),
        title_x=0.5,
        margin=dict(t=60, b=80),
        title_font=dict(size=17)
    )
    return fig


def schools_zero_enrolles(df):
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

    df['Enrollment Total'] = df[enrollment_columns].sum(axis=1)
    zero_enrollment_df = df[df['Enrollment Total'] == 0]

    return len(zero_enrollment_df)


def high_enrollment_table(df):
    # Calculate the sum of enrollees
    df['Enrollees'] = df.loc[:, 'K Male':'G12 ARTS Female'].sum(axis=1)

    # Delete the original columns
    columns_to_delete = list(df.loc[:, 'K Male':'G12 ARTS Female'].columns)
    columns_to_delete.extend(['Region', 'District', 'Municipality', 'Legislative District', 'Barangay', 'Sector', 'School Subclassification', 'School Type',  'BEIS School ID', 'Province', 'Modified COC'])
    df = df.drop(columns=columns_to_delete) 

    # Group by school name and division, sum enrollees, and sort
    top_schools = df.groupby(['School Name', 'Division'])['Enrollees'].sum().reset_index()
    top_schools = top_schools.sort_values('Enrollees', ascending=False).head(10)
    
    top_schools['Enrollees'] = top_schools['Enrollees'].apply(lambda x: f"{x:,}")

    # Create the interactive table
    fig = go.Figure(data=[go.Table(
        header=dict(values=['<b><i>School Name</i></b>', '<b><i>Division</i></b>', '<b><i>Enrollees</i></b>'],
                    align='center',
                    font=dict(size=15, color='white'),
                    fill_color = '#054a91'
                    ),
        cells=dict(values=[top_schools['School Name'], top_schools['Division'], top_schools['Enrollees']],
                align='center',
                font=dict(size=15),
                fill_color = '#dbe4ee'
                ))
    ])

    fig.update_layout(
        title_text="<b>Schools with the Highest Number of Enrollees</b>",
        font=dict(family='Inter'),
        title_x=0.5,
        title_font=dict(size=17),
        width = 615,
        margin=dict(t=60, b=20, l=10, r=10),
    )

    return fig