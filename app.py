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

        html.H2('Import Data', className='header-text'),
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Button('Upload CSV', className='upload-button'),
                    multiple=False  # Allow only one file to be uploaded at a time
                ),
                html.Button('Clear CSV', id='clear-button', n_clicks=0, className='upload-button'),
                html.Div(id='output-data-upload')
            ],className='button-div')
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
                    placeholder='Select Region'),

        dcc.Dropdown(id='province-dropdown', 
                     options=[], className='filter-container', placeholder='Select Province', 
                     style={'display':'block'}),
        html.Div(id='province-output'),

        dcc.Dropdown(id='district-dropdown', 
                     options=[], className='filter-container', placeholder='Select Municipality', 
                     style={'display':'block'}),
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
            dcc.Graph(id='schools-and-enrollees-chart', style={'width': '1229px', 'height': '600px'})
        ], className='container'), # Added this placeholder



    ], className='main'),
]


@callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    Input('clear-button', 'n_clicks')
)
def update_output(contents, filename, clear_clicks):
    # If the clear button is clicked, reset the output
    if clear_clicks > 0:
        return html.Div(['Data cleared.'])

    if contents is not None:
        # Decode the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Use pandas to read the CSV file
            if 'csv' in filename:
                # Decode the CSV content to a string
                csv_string = decoded.decode('utf-8')
                
                # Pass the CSV content to the cleaned_data function
                df_cleaned =cleaned_data(csv_string)
                
                return html.Div([
                    html.H5(filename),
                    html.H6('File successfully uploaded and processed.'),
                    # Display the first few rows of the cleaned dataframe
                    html.Pre(df_cleaned.head().to_string())
                ])
            else:
                return html.Div(['Please upload a CSV file.'])
        except Exception as e:
            return html.Div([
                'There was an error processing this file.',
                html.Pre(str(e))
            ])
    return html.Div(['No file uploaded yet.'])

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
    return [], {'display': 'block'}


@callback(
    Output('district-dropdown', 'options'),
    Output('district-dropdown', 'style'),
    Input('province-dropdown', 'value')
)
def update_district_dropdown(selected_province):
    if selected_province:
        districts = df[df['Province'] == selected_province]['District'].unique()
        return [{'label': d, 'value': d} for d in districts], {'display': 'block'}
    return [], {'display': 'block'}

# Callback for Reset Button
@callback(
    Output('region-dropdown', 'value'),
    Output('province-dropdown', 'value'),
    Output('district-dropdown', 'value'),
    Input('reset-button', 'n_clicks')
)
def reset_filters(n_clicks):
    # Reset all dropdowns to None or initial state
    return None, None, None

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
    Output('school-percentage-chart', 'figure'),
    Output('low-enrollment-chart', 'figure'),
    Output('gender-pie-chart', 'figure'),
    Output('high-enrollment-chart', 'figure'),
    Output('schools-and-enrollees-chart', 'figure'), # Added this line
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
        schools_and_enrollees_chart(filtered)
    )


if __name__ == '__main__':
    app.run(debug=True)