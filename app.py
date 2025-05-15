from dash import Dash, html, dcc, Output, Input, callback, State
import plotly.express as px
import plotly.graph_objects as go
from chart1 import total_student_chart, top_enrollees, total_enrollees_and_schools, school_types, schools_top, pie_chart, schools_zero_enrolles, high_enrollment_table, low_enrollment_table, school_level_percentage_chart, schools_and_enrollees_chart
from cleaned_data import cleaned_data
import io
import base64

df =cleaned_data()

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
        html.P([
            html.H2('Interpreting the Visuals', className='header-text'),
            html.P([html.B('1. Overview Cards'),  html.P('These give you a quick snapshot of the current total number of enrolled students, the total number of schools being tracked, the school with the largest student population, and the number of schools with zero enrollees.'), html.B('2. Enrollment by Grade levels and the Distibution of the Education Cluster'), html.P('This chart shows you how student enrollment is distributed across each grade. It helps you identify which grade levels have the most or fewest students. Meanwhile, the donut chart divides enrollment into categories like Elementary, Junior High, and Senior High.'), html.B('3. Gender Balance'), html.P('This gives you a visual sense of gender parity in enrollment.'),  html.B('4. Schools with the Highest and Lowest Enrollment'),html.P('The left table highlights schools with very few or no students enrolled. The right table lists schools managing the largest student bodies.'), html.B('5. Filters'), html.P('When you select a filter, all figures and charts update so you can drill down from the national view to specific locales.')
            ], className='body-text'),
        ]),


], className='sidebar'),

    # Main Content
    html.Div([
        #Filters
        html.Div([
        html.Span('Filters', className='filters-text'),
        dcc.Dropdown(id='region-dropdown', 
                     options=region_dropdown,
                     className='filter-container',
                    style={'display':'block'},
                    placeholder='Select Region',
                    multi=True),

        dcc.Dropdown(id='province-dropdown', 
                     options=[], className='filter-container', placeholder='Select Province', 
                     style={'display':'block'},
                     multi = True),
        html.Div(id='province-output'),

        dcc.Dropdown(id='district-dropdown', 
                     options=[], className='filter-container', placeholder='Select Municipality', 
                     style={'display':'block'},
                     multi = True),
        html.Div(id='district-output'),
        html.Button('Reset Filters', id='reset-button', n_clicks=0, className='reset-button'),
        ], className='main-filter-container'),
        html.Hr(),


        #First Four Figures
        html.Div(id='summary-cards', className='summary-cards', style={'display': 'flex', 'flexWrap': 'wrap'}),

        #Middle Section
        #Bar and Pie Chart
        html.Div([
            #Percentage of Enrollees per Grade clusters
            html.Div([
                dcc.Graph(id='school-percentage-chart', style={'width': '200px', 'height': '450px'})
            ], className='container'),
            html.Div([
                dcc.Graph(id='total-student-chart', style={'width': '610px', 'height': '450px'})
            ], className='container'),
            #Gender Pie Chart
            html.Div([
                dcc.Graph(id='gender-pie-chart', style={'width': '400px', 'height': '450px'})
            ], className='container'),
        ], className='middle-container'),

        #Bottom Section
        #Types of School
        html.Div([
            dcc.Graph(id='low-enrollment-chart', style={'width': '611px', 'height': '450px'})
        ], className='container'),
        #Schools with Highest Number of Enrollees
        html.Div([
            dcc.Graph(id='high-enrollment-chart', style={'width': '611px', 'height': '450px'})
        ], className='container'),


        html.Div([
            dcc.Graph(id='schools-and-enrollees-chart', style={'width': '1226px', 'height': '600px'})
        ], className='container'), # Added this placeholder

    ], className='main'),
]



# Callbacks for dependent dropdowns
@callback(
    Output('province-dropdown', 'options'),
    Output('province-dropdown', 'style'),
    Input('region-dropdown', 'value')
)
def update_province_dropdown(selected_regions):
    if selected_regions:
        provinces = df[df['Region'].isin(selected_regions)]['Province'].unique()
        return [{'label': p, 'value': p} for p in sorted(provinces)], {'display': 'block'}
    return [], {'display': 'block'}


@callback(
    Output('district-dropdown', 'options'),
    Output('district-dropdown', 'style'),
    Input('province-dropdown', 'value')
)
def update_district_dropdown(selected_provinces):
    if selected_provinces:
        districts = df[df['Province'].isin(selected_provinces)]['District'].unique()
        return [{'label': d, 'value': d} for d in sorted(districts)], {'display': 'block'}
    return [], {'display': 'block'}

# Callback for Reset Button
@callback(
    Output('region-dropdown', 'value'),
    Output('province-dropdown', 'value'),
    Output('district-dropdown', 'value'),
    Input('reset-button', 'n_clicks')
)
def reset_filters(n_clicks):
    return [], None, None

def filter_df(regions, province, district):
    filtered_df = df.copy()
    if regions:
        # regions is a list now!
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    if province:
        filtered_df = filtered_df[filtered_df['Province'].isin(province)]
    if district:
        filtered_df = filtered_df[filtered_df['District'].isin(district)]
    return filtered_df


# Callback to update summary cards and charts
@callback(
    Output('summary-cards', 'children'),
    Output('total-student-chart', 'figure'),
    Output('school-percentage-chart', 'figure'),
    Output('low-enrollment-chart', 'figure'),
    Output('gender-pie-chart', 'figure'),
    Output('high-enrollment-chart', 'figure'),
    Output('schools-and-enrollees-chart', 'figure'),
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
            html.Div([html.Span(overall_total)], className='numerals'),
            html.P("Number of Enrollees in AY 2023-2024", className='body-text-caption')
        ], className='container'),

        html.Div([
            html.Div([html.Span(school_count)], className='numerals'),
            html.P("Number of Schools in AY 2023-2024", className='body-text-caption')
        ], className='container'),

        html.Div([
            html.Div([html.Span([f"{int(largest['Total Enrollees']):,}"])], className='numerals'), html.P(f"Largest School Based on Student Population: {largest['School Name']}", className='body-text-caption')
        ], className='container', style={'max-width': '423px', 'width': '100%',}),

        html.Div([
            html.Div([html.Span(schools_zero_enrolles(filtered))], className='numerals'),
            html.P("Schools with Zero Enrollees", className='body-text-caption')
        ], className='container'),
    ]

    return (
        summary_cards,
        total_student_chart(filtered),
        school_level_percentage_chart(df, region, province, district),
        low_enrollment_table(filtered),
        pie_chart(filtered),
        high_enrollment_table(filtered),
        schools_and_enrollees_chart(df)
    )


if __name__ == '__main__':
    app.run(debug=True)