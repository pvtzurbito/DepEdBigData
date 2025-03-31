import pandas as pd
import numpy as np
from dash import Dash, html, dash_table

# Dropping null, duplicates, and unnecessary column
df = pd.read_csv('SY 2023-2024 School Level Data on Official Enrollment 13.csv', encoding='latin-1', skiprows=4)
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

df.head(50)


app = Dash(__name__, external_stylesheets=["/static/main.css"])


app.layout = [
    html.P([html.Img(src='assets/Seal_of_the_Department_of_Education_of_the_Philippines.png'),html.Br(),'Republic of the Philippines', html.Br(), html.Span('Department of Education', className='deped')], className='header-1'),
    html.Hr(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
]

if __name__ == '__main__':
    app.run(debug=True)

