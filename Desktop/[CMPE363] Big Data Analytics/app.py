import pandas as pd
from dash import Dash, html, dash_table, dcc
import plotly.express as px



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

#For Graph 1
# Combine "School Subclassification" and "Modified COC" into a new dataframe (School Type Combined)
df['School Type Combined'] = df['School Subclassification'] + ' ' + df['Modified COC']

# Using groupby to count the number of school type by sector.
school_type_counts = df.groupby(['School Type Combined', 'Sector']).size().reset_index(name='Number of Schools')

# Selecting only the top10 school typress across all sectors
top_10_types = school_type_counts.groupby('School Type Combined')['Number of Schools'].sum().nlargest(10).index.tolist()
top_10 = school_type_counts[school_type_counts['School Type Combined'].isin(top_10_types)]

fig = px.bar(top_10,
             x='School Type Combined',
             y='Number of Schools',
             color='Sector',
             hover_data={'School Type Combined': False, 'Sector': False, 'Number of Schools': True})
fig.update_layout(xaxis_title='School Type',
                  yaxis_title='Number of Schools',
                  xaxis_tickangle = -90)


#Website
app = Dash(__name__, external_stylesheets=["/static/main.css"])

app.layout = [
  #Sidebar
  html.Div([
     html.P([
        html.Img(src='assets/Seal_of_the_Department_of_Education_of_the_Philippines.png'),
        html.Br(),'Republic of the Philippines', 
        html.Br(), 
        html.Span('Department of Education', className='deped'), 
        html.Br(), 'Education Management Information System Division'], className='header-1'),
        html.Hr(), 

  #About the Data Dashboard
      html.P([
         html.H2(['About the Data Dashboard'], className='header-text'), 
         html.P([' The Learner Information System Dashboard provides a comprehensive view of student enrollment across all schools in the Philippines, from Pre-Elementary to Grade 12. Designed for educators, policymakers, and administrators, this dashboard offers data-driven insights to support educational planning and resource allocation.'], className='body-text'),
         ]),
  ], className='sidebar'),

  #Content
    html.Div([
       #Plotly Chart 1
       html.Div([
          html.P('Top 10 School Types with Highest Number of Schools (Grouped by Sector)', className='header-text'), 
          #Chart 1
          dcc.Graph(figure = fig)
          ],className='container')
    ],className='main')
   

]

if __name__ == '__main__':
    app.run(debug=True)

