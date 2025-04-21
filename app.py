from dash import Dash, html, dcc, Output, Input, callback
import plotly.express as px
import plotly.graph_objects as go
from chart1 import (
    total_student_chart, top_enrollees, total_enrollees_and_schools,
    school_types, schools_top, pie_chart, schools_zero_enrolles, high_enrollment_table
)
from cleaned_data import cleaned_data

df = cleaned_data()

# For Region Dropdown
region_dropdown = [{'label': region, 'value': region} for region in df['Region'].unique()]

# App Setup
app = Dash(__name__, external_stylesheets=["/static/main.css"])

app.layout = [
    # Sidebar
    html.Div([
        html.P([
            html.Img(src='assets/Seal_of_the_Department_of_Education_of_the_Philippines.png'),
            html.Br(), 'Republic of the Philippines',
            html.Br(),
            html.Span('Department of Education', className='deped'),
            html.Br(), 'Education Management Information System Division'
        ], className='header-1'),
        html.Hr(),

        html.P([
            html.H2('About the Data Dashboard', className='header-text'),
            html.P([
                'The Learner Information System Dashboard provides a comprehensive view of student enrollment across all schools in the Philippines, from Pre-Elementary to Grade 12. Designed for educators, policymakers, and administrators, this dashboard offers data-driven insights to support educational planning and resource allocation.'
            ], className='body-text'),
        ]),

        html.Hr(),
        html.H2('Filters', className='header-text'),

        html.H3('Select your Region', className='header-text'),
        dcc.Dropdown(id='region-dropdown', options=region_dropdown, className='body-text'),
        html.Div(id='region-output', className='body-text'),

        html.H3('Select your Province', className='header-text'),
        dcc.Dropdown(id='province-dropdown', options=[], style={'display': 'none'}, className='body-text'),
        html.Div(id='province-output', className='body-text'),

        html.H3('Select your District', className='header-text'),
        dcc.Dropdown(id='district-dropdown', options=[], style={'display': 'none'}, className='body-text'),
        html.Div(id='district-output', className='body-text')
    ], className='sidebar'),

    # Main Content
    html.Div([
        html.H2('Data Dashboard', className='header-text'),
        html.Hr(),

        html.Div(id='summary-cards', className='summary-container', style={'display': 'flex', 'flexWrap': 'wrap'}),

        html.Div([
            dcc.Graph(id='total-student-chart', style={'width': '610px', 'height': '450px'})
        ], className='container'),

        html.Div([
            dcc.Graph(id='school-types-chart', style={'width': '610px', 'height': '450px'})
        ], className='container'),

        html.Div([
            dcc.Graph(id='gender-pie-chart', style={'width': '610px', 'height': '450px'})
        ], className='container'),

        html.Div([
            dcc.Graph(id='high-enrollment-chart', style={'width': '610px', 'height': '450px'})
        ], className='container'),
    ], className='main'),
]


# Callbacks for dependent dropdowns
@callback(
    Output('province-dropdown', 'options'),
    Output('province-dropdown', 'style'),
    Input('region-dropdown', 'value')
)
def update_province_dropdown(selected_region):
    if selected_region:
        provinces = df[df['Region'] == selected_region]['Province'].unique()
        return [{'label': p, 'value': p} for p in provinces], {'display': 'block'}
    return [], {'display': 'none'}


@callback(
    Output('district-dropdown', 'options'),
    Output('district-dropdown', 'style'),
    Input('province-dropdown', 'value')
)
def update_district_dropdown(selected_province):
    if selected_province:
        districts = df[df['Province'] == selected_province]['District'].unique()
        return [{'label': d, 'value': d} for d in districts], {'display': 'block'}
    return [], {'display': 'none'}



# Function to filter data based on dropdowns
def filter_df(region, province, district):
    filtered_df = df.copy()
    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if province:
        filtered_df = filtered_df[filtered_df['Province'] == province]
    if district:
        filtered_df = filtered_df[filtered_df['District'] == district]
    return filtered_df


# Callback to update summary cards and charts
@callback(
    Output('summary-cards', 'children'),
    Output('total-student-chart', 'figure'),
    Output('school-types-chart', 'figure'),
    Output('gender-pie-chart', 'figure'),
    Output('high-enrollment-chart', 'figure'),
    Input('region-dropdown', 'value'),
    Input('province-dropdown', 'value'),
    Input('district-dropdown', 'value')
)
def update_dashboard(region, province, district):
    filtered = filter_df(region, province, district)

    overall_total, school_count = total_enrollees_and_schools(filtered)
    largest, smallest = schools_top(filtered)

    summary_cards = [
        html.Div([
            html.Div([html.H1(overall_total)], className='numerals'),
            html.P("Number of Enrollees in AY 2023-2024", className='body-text-caption')
        ], className='container'),

        html.Div([
            html.Div([html.H1(school_count)], className='numerals'),
            html.P("Number of Schools in AY 2023-2024", className='body-text-caption')
        ], className='container'),

        html.Div([
            html.Div([html.H1([f"{int(largest['Total Enrollees']):,}", " Learners"])], className='numerals'), html.P(f"Most Populous School: {largest['School Name']}", className='body-text-caption')
        ], className='container', style={'max-width': '425px', 'width': '100%',}),

        html.Div([
            html.Div([html.H1(schools_zero_enrolles(filtered))], className='numerals'),
            html.P("Schools with Zero Enrollees", className='body-text-caption')
        ], className='container'),
    ]

    return (
        summary_cards,
        total_student_chart(filtered),
        school_types(filtered),
        pie_chart(filtered),
        high_enrollment_table(filtered)
    )


if __name__ == '__main__':
    app.run(debug=True)
