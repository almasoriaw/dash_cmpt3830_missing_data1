import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from flask_basicauth import BasicAuth
import dash.dcc as dcc

# Load missing_df (Before Cleaning)
missing_df = pd.read_csv('missing_values_summary.csv')

# Load missing_df_after (After Cleaning)
missing_df_after = pd.read_csv('missing_values_summary_after.csv')

# Initialize Dash App
app = dash.Dash(__name__)
server = app.server
# Set up basic authentication
app.server.config['BASIC_AUTH_USERNAME'] = 'group1'
app.server.config['BASIC_AUTH_PASSWORD'] = 'norquestca'

basic_auth = BasicAuth(app.server)

# Protect the app with basic authentication
@app.server.before_request
def before_request():
    if not basic_auth.authenticate():
        return basic_auth.challenge()  # Challenge for authentication

app.layout = html.Div([
    html.H1(
        "Data Cleaning, EDA & Feature Engineering: The process",
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
            {'label': 'Missing Values Before Cleaning', 'value': 'before'},            
            {'label': 'First Columns Created', 'value': 'columns_created'},
            {'label': 'Columns Dropped', 'value': 'columns_dropped'},
            {'label': 'Missing Values After Cleaning', 'value': 'after'}
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

    # Content Component
    html.Div(id='content-display')
], style={'fontFamily': 'Tahoma'})

# Callback to Update Content Based on Dropdown
@app.callback(
    Output('content-display', 'children'),
    [Input('data-selector', 'value')]
)
def update_content(selected_data):
    if selected_data == 'before':
        df = missing_df  # Ensure this DataFrame is defined in your code
        title = "Missing Data Before Cleaning"
        color_scale = 'Reds'
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
        return dcc.Graph(figure=fig)

    elif selected_data == 'after':
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
        return dcc.Graph(figure=fig)

    elif selected_data == 'columns_created':
        text = dcc.Markdown("""
Splitting **Meter Description** in 2 columns --> **Meter Location** and **Product Description**. Dropped original column.

Splitting **Tank Description** in 2 columns --> **Tank Location** and **Tank Product**. Dropped original column.

From the **PDF Minesite flows info**. We mapped each row with their respective product description match to create the columns **LOW FLOW**, **MED FLOW** and **HI FLOW**.
""")
        
    
        return html.Div([
            html.H2("Columns Created", style={'fontFamily': 'Tahoma', 'fontSize': '20px'}),
            html.Pre(text, style={'fontFamily': 'Tahoma', 'fontSize': '16px'})
        ])
    
    elif selected_data == 'columns_dropped':
        text = dcc.Markdown("""
**Dropped Columns:**  
                            
**SCU ID**, **Meter ID**, **Tank ID**, **Equipment ID**, **Equipment Field ID**, **Department**, **Category** (1 unique value), **"Metered Volume"** (high correlation with Volume)

Dropping ID columns in EDA removes non-predictive, unique identifiers that lack statistical relevance, reduce visualization clarity, and risk model overfitting.

If left in, they can confuse models into “memorizing” these codes instead of learning real patterns, leading to poor predictions on new data. This allows the analysis to focus on meaningful data patterns and relationships.
""")

        return html.Div([
            html.H2("Columns Dropped", style={'fontFamily': 'Tahoma', 'fontSize': '20px'}),
            html.Div(text, style={'fontFamily': 'Tahoma', 'fontSize': '16px'})
        ])  # Make sure this closing bracket matches the opening one above

    else:
        return html.P("Select an option from the dropdown.", style={'fontFamily': 'Tahoma', 'fontSize': '16px'})


# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
