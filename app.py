import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas.core.indexes.base import Index
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})

df=pd.read_csv("country_indicators.csv")

fig = px.scatter(df, x="Year", y="Value", color="Country Name", 
custom_data=["Country Name","Indicator Name","Year","Value"])

fig.update_layout(clickmode='event+select')

fig.update_traces(marker_size=20)

df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),
    


    html.Div(className='row', children=[
        html.Div([html.Button("comenzar a capturar seleccion", id="btn_txt"), dcc.Download(id="download-text-index")]),

        html.Div([
            dcc.Markdown(id='table_show',)
        ], className='three columns'),
                 
        
    ])
])
@app.callback(
    Output('table_show', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_table_show(table_show):

    if table_show is None:
        raise dash.exceptions.PreventUpdate
    else:     
        #print(table_show["points"])
        dfs=pd.DataFrame(table_show["points"])
        #print(dfs)
        return dfs[["x","y","customdata"]].to_markdown()



@app.callback(Output("download-text-index", "data"), Input("btn_txt", "n_clicks"),Input('basic-interactions', 'selectedData'))
def func(n_clicks,table_show):
    if n_clicks is None  :
        raise dash.exceptions.PreventUpdate
    else:        
        print("ejecutando no")
        dfs=pd.DataFrame(table_show["points"])
        return dict(content=dfs.to_html(), filename="hello.xls")
            




if __name__ == '__main__':
    app.run_server(debug=True)

