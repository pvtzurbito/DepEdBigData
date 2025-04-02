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

#Question: Do certain school subclassification tend to have higher enrollment in particular grade levels?

# Defining grade-level groups to be used in enrollee count
preschool_cols = df.filter(like="K ").columns
elementary_cols = df.filter(regex="G[1-6] ").columns
jhs_cols= df.filter(regex="G(7|8|9|10) ").columns
SNEd_cols= df.filter(regex="JHS NG ").columns
shs_cols= df.filter(regex="G(11|12) ").columns

# Creating summarized enrollment count
df["Preschool"] = df[preschool_cols].sum(axis=1)
df["Elementary"] = df[elementary_cols].sum(axis=1)
df["JHS"] = df[jhs_cols].sum(axis=1)
df["SNEd"] = df[SNEd_cols].sum(axis=1)
df["SHS"] = df[shs_cols].sum(axis=1)

# Selecting only the relevant columns to be used in data visualization
df_summarized = df[['School Subclassification', 'Preschool', 'Elementary', 'JHS', 'SNEd', 'SHS']]

#Aggregating enrollment by school subclassification
enrollment_summary = df_summarized.groupby('School Subclassification').sum()

#Converting the dataframe for plotly
enrollment_summary = enrollment_summary.reset_index()
enrollment_melted = enrollment_summary.melt(id_vars='School Subclassification', var_name='Educational Level', value_name='Enrollment Count')

#Stacked bar chart - plotly
fig1 = px.bar(enrollment_melted,
             x='School Subclassification',
             y='Enrollment Count',
             color='Educational Level',
             barmode='group',
             hover_data={'School Subclassification': False, 'Educational Level': True, 'Enrollment Count': True },
             color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(xaxis_title='School Subclassification',
                  yaxis_title='Enrollment Count',
                  xaxis_tickangle=-90)



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
       html.H2(['Data Dashboard'], className='header-text'),
       html.Hr(),
       #Plotly Chart 1
        html.Div([
          html.P('Top 10 School Types with Highest Number of Schools (Grouped by Sector)', className='header-text'), 
          #Chart 1
          dcc.Graph(figure = fig)
          ],className='container'),

        html.Div([
           html.P('Enrollment in Different School Types', className = 'header-text'),
           #Chart 2
           dcc.Graph(figure = fig1, style={'width': '580px', 'height': '450px'})
        ], className='container')
    ],className='main')
   

]

if __name__ == '__main__':
    app.run(debug=True)

