from dash import Dash, html, dash_table, dcc, Output, Input, callback
import plotly.express as px
import plotly.graph_objects as go
from chart1 import total_student_chart, top_enrollees, total_enrollees_and_schools, school_types, schools_top, pie_chart, schools_zero_enrolles, high_enrollment_table
from cleaned_data import cleaned_data

df = cleaned_data()

#For Region Dropdown
region_dropdown = [{'label': region, 'value': region} for region in df['Region'].unique()]
province_dropdown = dcc.Dropdown(
    id='province-dropdown',
    options=[],
    style={'display': 'none'}
)
district_dropdown_component = dcc.Dropdown(
    id='district-dropdown',
    options=[],
    style={'display': 'none'}
)

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
      html.H2(['Filters'], className='header-text'),
      #Dropdown
      html.H3(['Select your Region'], className='header-text'),
      dcc.Dropdown(id = 'region-dropdown', options = region_dropdown, className= 'body-text'),
      html.Div(id='region-output', className='body-text'),

      html.H3(['Select your Province'], className='header-text'),
      html.Div(province_dropdown, className='body-text'),
      html.Div(id='province-output', className='body-text'),

      html.H3(['Select your District'], className='header-text'),
      html.Div(district_dropdown_component, className='body-text'),
      html.Div(id='district-output', className='body-text')


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
           html.Div([html.H1([largest['Total Enrollees'], " Learners"])], className='numerals'), html.P(['Most Populous School: ',largest['School Name']],className='body-text-caption')
            ], className='container'),

         #Region with least number of enrolees
         html.Div([
           html.Div([html.H1(schools_zero_enrolles(df))], className='numerals'), html.P(['Schools with Zero Enrollees'],className='body-text-caption')
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

        html.Div([
           #Pie Chart
           dcc.Graph(figure=pie_chart(df), style={'width': '610px', 'height': '450px', 'margin-top': '0px'})
        ], className='container'),

        html.Div([
           #Pie Chart
           dcc.Graph(figure=high_enrollment_table(df), style={'width': '610px', 'height': '450px', 'margin-top': '0px'})
        ], className='container')

    ],className='main'),

]

# Callbacks
@callback(
    Output('province-dropdown', 'options'),
    Output('province-dropdown', 'style'),
    Input('region-dropdown', 'value')
)
def update_province_dropdown(selected_region):
    if selected_region:
        filtered_df = df[df['Region'] == selected_region]
        province_options = [{'label': province, 'value': province} for province in filtered_df['Province'].unique()]
        return province_options, {'display': 'block'}
    else:
        return [], {'display': 'none'}

@callback(
    Output('district-dropdown', 'options'),
    Output('district-dropdown', 'style'),
    Input('province-dropdown', 'value')
)
def update_district_dropdown(selected_province):
    if selected_province:
        filtered_df = df[df['Province'] == selected_province]
        district_options = [{'label': district, 'value': district} for district in filtered_df['District'].unique()]
        return district_options, {'display': 'block'}
    else:
        return [], {'display': 'none'}

@callback(
   Output('region-output', 'children'),
   Input('region-dropdown', 'value')
)

@callback(
    Output('province-output', 'children'),
    Input('province-dropdown', 'value')
)
def update_province_output(value):
    return f'You have selected {value}'

@callback(
    Output('district-output', 'children'),
    Input('district-dropdown', 'value')
)
def update_district_output(value):
    return f'You have selected {value}'



def update_output(value):
   return f'You have selected {value}'





if __name__ == '__main__':
    app.run(debug=True)

