import pandas as pd
from dash import Dash, html, dash_table, dcc, Output, Input, callback
import plotly.express as px
import plotly.graph_objects as go
from chart1 import total_student_chart, top_enrollees, total_enrollees_and_schools, school_types, schools_top

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
#Options for dropdown menus
region_dropdown = [{'label': region, 'value': region} for region in df['Region'].unique()]
 
#Website
app = Dash(__name__, external_stylesheets=["/static/main.css"])
top_region, bot_region = top_enrollees(df)
overall_total, school_count = total_enrollees_and_schools(df)
largest, smallest = schools_top(df)
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

  #Dropdown Menu
      html.Hr(),
      html.H2(['Select your Region'], className='header-text'),
      #Dropdown
      dcc.Dropdown(id = 'region-dropdown', options = region_dropdown, className= 'body-text'),
      html.Div(id='region-output', className='body-text')


  ], className='sidebar'),

  #Content
    html.Div([
       html.H2(['Data Dashboard'], className='header-text'),
       html.Hr(),

       #Number of Enrolled Students
         html.Div([
           html.Div([html.H1(overall_total)], className='numerals'), html.P(['Number of Enrolees in AY 2023-2024'],className='body-text-caption')
            ], className='container'),

         #School Count
         html.Div([
           html.Div([html.H1(school_count)], className='numerals'), html.P(['Number of Schools in AY 2023-2024'],className='body-text-caption')
            ], className='container'),


         #Region with most number of enrolees
         html.Div([
           html.Div([html.H1(largest['Total Enrollees'])], className='numerals'), html.P(['Most Populous: ',largest['School Name']],className='body-text-caption')
            ], className='container'),

         #Region with least number of enrolees
         html.Div([
           html.Div([html.H1(smallest['Total Enrollees'])], className='numerals'), html.P(['Least Populous: ',smallest['School Name']],className='body-text-caption')
            ], className='container'),


         
       #Plotly Chart 1
        html.Div([
          #Chart 1
          dcc.Graph(figure = total_student_chart(df), style={'width': '610px', 'height': '450px', 'margin-top': '0px'})
          ],className='container'),

        html.Div([
           #Table 1
           dcc.Graph(figure = school_types(df), style={'width': '610px', 'height': '450px'})
        ], className='container'),

        html.Div([])

    ],className='main'),

]

@callback(
   Output('region-output', 'children'),
   Input('region-dropdown', 'value')
)
def update_output(value):
   return f'You have selected {value}'




if __name__ == '__main__':
    app.run(debug=True)

