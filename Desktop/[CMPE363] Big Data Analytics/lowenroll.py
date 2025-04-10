import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Dropping null, duplicates, and unnecessary column
df = pd.read_csv(r'C:\Users\codil.RALPH\Downloads\DataCamp\DepEdBigData\Desktop\[CMPE363] Big Data Analytics\data\SY 2023-2024 School Level Data on Official Enrollment 13.csv', encoding='latin-1', skiprows=4)
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

# Calculate the sum of enrollees
df['Enrollees'] = df.loc[:, 'K Male':'G12 ARTS Female'].sum(axis=1)

# Delete the original columns
columns_to_delete = list(df.loc[:, 'K Male':'G12 ARTS Female'].columns)
columns_to_delete.extend(['Region', 'District', 'Municipality', 'Legislative District', 'Barangay', 'Sector', 'School Subclassification', 'School Type',  'BEIS School ID', 'Province', 'Modified COC'])
print(df.columns)
df = df.drop(columns=columns_to_delete) 

# Group by school name and division, sum enrollees, and sort
top_schools = df.groupby(['School Name', 'Division'])['Enrollees'].sum().reset_index()
top_schools = top_schools.sort_values('Enrollees', ascending=True).head(10)

# Create the interactive table
fig = go.Figure(data=[go.Table(
    header=dict(values=['<b><i>School Name</i></b>', '<b><i>Division</i></b>', '<b><i>Enrollees</i></b>'],
                fill_color='white',
                align='center',
                font=dict(size=12),
                line_color='darkslategray',
                line_width=[0, 0, 0, 0]),
    cells=dict(values=[top_schools['School Name'], top_schools['Division'], top_schools['Enrollees']],
               fill_color='white',
               align='center',
               font=dict(size=10),
               line_color=['darkslategray', 'white', 'white', 'white'], # Top, Vertical 1, Vertical 2, Right
               line_width=[0, 0, 0, 0]))
])

fig.update_layout(
    title_text="<b>Schools with the Lowest Number of Enrollees</b>",
    title_x=0.5,
    title_font=dict(size=17),
    margin=dict(l=50, r=50, b=50, t=70),
    width=800,
    height=600
)

fig.show()