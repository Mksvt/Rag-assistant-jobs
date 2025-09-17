from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Sample data for the dashboard
data = {
    'Skills': ['Python', 'JavaScript', 'React', 'Docker', 'Machine Learning'],
    'Frequency': [50, 30, 40, 20, 25]
}

df = pd.DataFrame(data)

# Create a bar chart
fig = px.bar(df, x='Skills', y='Frequency', title='Skills Frequency in Job Vacancies')

app.layout = html.Div(children=[
    html.H1(children='Dashboard'),

    html.Div(children='''
        Analyzing the skills required in job vacancies.
    '''),

    dcc.Graph(
        id='skills-frequency',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)