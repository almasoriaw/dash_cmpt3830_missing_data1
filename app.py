import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from flask_basicauth import BasicAuth

# Load missing_df (Before Cleaning)
missing_df = pd.read_csv('missing_values_summary.csv')

# Load missing_df_after (After Cleaning)
missing_df_after = pd.read_csv('missing_values_summary_after.csv')

# Initialize Dash App
app = dash.Dash(__name__)
server = app.server
# Set up basic authentication
app.server.config['BASIC_AUTH_USERNAME'] = 'my_add'
app.server.config['BASIC_AUTH_PASSWORD'] = '12asasdas'

basic_auth = BasicAuth(app.server)

# Protect the app with basic authentication
@app.server.before_request
def before_request():
    if not basic_auth.authenticate():
        return basic_auth.challenge()  # Challenge for authentication

app.layout = html.Div([
    html.H1(
        "Missing Data Comparison: Before vs After Cleaning",
        style={
            'textAlign': 'center',
            'fontFamily': 'Tahoma',
            'color': '#333',
            'backgroundColor': '#89cad3',
        }
    ),

    # Styled Dropdown
    dcc.Dropdown(
        id='data-selector',
        options=[
            {'label': 'Before Cleaning', 'value': 'before'},
            {'label': 'After Cleaning', 'value': 'after'}
        ],
        value='before',
        style={
            'fontFamily': 'Tahoma',
            'fontSize': '16px',
            'backgroundColor': '#09f0bf',  # Light blue background
            'color': '#33',               # Dark gray text
            'border': '1px solid #999',    # Subtle border
            'borderRadius': '5px',         # Rounded corners
            'padding': '5px'
        }
    ),

    # Graph Component
    dcc.Graph(id='missing-data-graph')
], style={'fontFamily': 'Tahoma'})

# Callback to Update Graph Based on Dropdown
@app.callback(
    Output('missing-data-graph', 'figure'),
    [Input('data-selector', 'value')]
)
def update_graph(selected_data):
    if selected_data == 'before':
        df = missing_df  # Ensure this DataFrame is defined in your code
        title = "Missing Data Before Cleaning"
        color_scale = 'Reds'
    else:
        df = missing_df_after  # Ensure this DataFrame is defined in your code
        title = "Missing Data After Cleaning"
        color_scale = 'Greens'

    # Create Bar Chart
    fig = px.bar(
        df,
        x='Column Name',
        y='Missing Data Percentage',
        color='Missing Data Percentage',
        color_continuous_scale=color_scale,
        title=title,
        labels={'Missing Data Percentage': '% Missing'}
    )

    # Apply Font Styling to Plot
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="% Missing Data",
        xaxis_title="Column Name",
        font=dict(family='Tahoma', size=14, color='#333')
    )

    return fig

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)