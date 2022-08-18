import dash
from dash import dcc
from dash import dash_table
from dash import html
import pandas as pd
#import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
from nltk.probability import FreqDist
from ast import literal_eval

def get_words(df):    
    words = []
    for wordList in df.tokens:
        words += wordList

    common_wds = pd.DataFrame(FreqDist(words).most_common(50), columns = ['word','count'])
    return common_wds



fn = 'all_predictions2.csv'
data = pd.read_csv(fn)
fn = 'pb_budak_v3.csv'
data_pb = pd.read_csv(fn)
data_pb = data_pb.sample(5000)

data_pb['tokens'] = data_pb['tokens'].apply(literal_eval)
all_wrds = get_words(data_pb)
dem_wrds = get_words(data_pb[data_pb['type'] < 1.5 ])
rep_wrds = get_words(data_pb[data_pb['type'] > 2.5 ])
neu_wrds = get_words(data_pb[data_pb['type'].between(1.5,2.5)])

data['text_sh'] = [x[:200] for x in data.text]

data = data.rename(columns={'Unnamed: 0':'id'})



data['bias'] = data['bias'].astype('float64')
data["cluster"] = data["cluster"].astype(str)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Fake News Dashboard"



table_cols = ['Article ID', 'Political Bias', 'Misinfo Probability']


app.layout = html.Div([
    ##Header
    html.Div(
            children=[
                html.H1(children="Misinformation Dashboard",
                        className = "header-title"),
                html.P(
                    children="Explore characteristics related to misinformation"
                    " within a corpus of news articles.",
                    className = "header-description"
                ),
            ],
            className="header",
        ),
    ##Top section
    html.Div([
        html.Div([
            html.Div([
                html.H2(children="Data Exploration: Political Bias"),
                html.H3(children="Political Bias vs. Sentiment Rating"),
                ],style={'margin-left':'25px'}),
            dcc.Dropdown(['Aggregate Bias', 'Democrat Slant', 'Republican Slant'], 'Aggregate Bias', id='dropdown_strip'),
            dcc.Graph(id='top_graph1'),
            html.H3(children="Word Usage", style={'margin-left':'25px'}),
            dcc.Dropdown(['All Articles', 'Left-Leaning', 'Neutral', 'Right-Leaning'], 'All Articles', id='dropdown_hist'),
            dcc.Graph(id='bottom_graph1')
            ], style={'width': '49%', 'display': 'inline-block', 'float':'left'}
            ),
        html.Div([
            dash_table.DataTable(id='table_1',
                                  #data[['id','title']].to_dict('records'),
                                  page_size=30,
                                  style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',},
                                  style_cell={'textAlign': 'left'},
                                  style_header={
                                    'backgroundColor': 'black',
                                    'fontWeight': 'bold',
                                    'color':'white',
                                    },
                                ),
            ], style={'margin-top':'100px','width': '49%', 'display': 'inline-block', 'float':'right'},
            ),
        ], style={'display':'block'}),
    ##Bottom Section
    html.Div([
        html.Div([
            html.H2(children="Modeling: Misinformation"),
            html.H3(children="Political Bias vs. Misinformation Rating"),
            ],style={'margin-left':'25px'}),
        html.Div([
            dcc.Dropdown(['Aggregate Probability', 'Probability of Being True Information', 'Probability of Being a Mix of True and False Information',
                          'Probability of Being Misinformation'], 'Aggregate Probability', id='dropdown_scatter'),
            dcc.Graph(id='top_graph2'),
            html.H3(children="Misinformation and Political Bias Ratings vs. Clusters", style={'margin-left':'25px'}),
            dcc.Dropdown(['Misinformation vs. Clusters', 'Political Bias vs. Clussters'], 'Misinformation vs. Clusters', id='dropdown_strip_2'),
            dcc.Graph(id='bottom_graph2')
            ], style={'width': '49%', 'display': 'inline-block', 'float':'left'}
            ),
        html.Div([
            dash_table.DataTable(id='table_2',
                                  #data[['id','title']].to_dict('records'),
                                  page_size=26,
                                  style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',},
                                  style_cell={'textAlign': 'left'},
                                  style_header={
                                    'backgroundColor': 'black',
                                    'fontWeight': 'bold',
                                    'color':'white',
                                    },
                                ),
            ], style={'width': '49%', 'display': 'inline-block', 'float':'right'},
            )
        ], style={'margin-top':'100px','display':'inline-block'})         
    ])

@app.callback(
    Output('table_2','data'),
    Input('top_graph2','selectedData'),
    Input('bottom_graph2','selectedData')
    )  

def update_table_bottom(selection_top,selection_bottom):
    if selection_top == None and selection_bottom == None:
        table_data = data[['id','text_sh']].to_dict('records')
    elif selection_top == None:
        ids = []
        for point in selection_bottom['points']:
            ids.append(point['customdata'][0])
        tmp_df = data[data['id'].isin(ids)]
        table_data = tmp_df[['id','text_sh']].to_dict('records')
    elif selection_bottom == None:
        ids = []
        for point in selection_top['points']:
            ids.append(point['customdata'][0])
        tmp_df = data[data['id'].isin(ids)]
        table_data = tmp_df[['id','text_sh']].to_dict('records')
    else:
        ids = []
        for point in selection_top['points']:
            ids.append(point['customdata'][0])
        for point in selection_top['points']:
            ids.append(point['customdata'][0])
        tmp_df = data[data['id'].isin(ids)]
        table_data = tmp_df[['id','text_sh']].to_dict('records')
        
        
    return table_data

@app.callback(
    Output('table_1','data'),
    Input('top_graph1','selectedData'),
    )  

def update_table_top(selection_top):
    if selection_top == None:
        table_data = data_pb[['id','title']].to_dict('records')

    else:
        ids = []
        for point in selection_top['points']:
            ids.append(point['customdata'][0])
        tmp_df = data_pb[data_pb['id'].isin(ids)]
        table_data = tmp_df[['id','title']].to_dict('records')
        
    print(table_data)    
    return table_data

@app.callback(
    Output('top_graph1', 'figure'),
    Input('dropdown_strip', 'value')
)

def update_fig1(dropdown):
    'Aggregate Bias', 'Democrat Slant', 'Republican Slant'
    if dropdown == 'Democrat Slant':
        x = 'democrat'
        tix = ['Pro-Democrat', 'Neutral', 'Anti-Democrat']
    elif dropdown == 'Republican Slant':
        x = 'republican'
        tix = ['Anti-Republican', 'Neutral', 'Pro-Republican']
    else:
        x = 'type'
        tix = ["Favors Democrats", "Neutral", "Favors Republicans"]
    fig1 = px.strip(data_pb, x=x, y="sentiment",
                      custom_data=['id'],
                      labels={'type':'Political Bias',
                              'sentiment':'Sentiment Score'},
                      #title='Political Bias vs. Sentiment Rating',
                      hover_data={"id":True,
                                  'title':True,
                                  "type":False,
                                  'sentiment':False})

    fig1.update_xaxes(
        ticktext=tix,
        tickvals=[0,2,4],
    )
    return fig1

@app.callback(
    Output('bottom_graph1', 'figure'),
    Input('dropdown_hist', 'value')
)

def update_fig2(dropdown):
    
    if dropdown == 'Left-Leaning':
        common_wds = dem_wrds 
    elif dropdown == 'Neutral':
        common_wds = neu_wrds
    elif dropdown == 'Right-Leaning':
        common_wds = rep_wrds
    else:
        common_wds = all_wrds
        
    
    fig2 = px.histogram(common_wds, x="word", y='count',
                        labels={'sum of count': 'Count',
                                'word': 'Word'})
    
    fig2.update_layout(
        yaxis_title_text='Count', # yaxis label
    )
    
    return fig2

@app.callback(
    Output('top_graph2', 'figure'),
    Input('dropdown_scatter', 'value')
)

def update_fig3(dropdown):
    
    if dropdown == 'Probability of Being True Information':
        y = 'Prob_True'
        labels = {'bias':'Political Bias',
                'Prob_True':'Probability of being True',
                'cluster':'Cluster'}
    elif dropdown == 'Probability of Being a Mix of True and False Information':
        y = 'Prob_Mix'
        labels = {'bias':'Political Bias',
                'Prob_Mix':'Probability of being a Mix',
                'cluster':'Cluster'}
    elif dropdown == 'Probability of Being Misinformation':
        y = 'Prob_Fake'
        labels = {'bias':'Political Bias',
                'Prob_Fake':'Probability of being Misinformation',
                'cluster':'Cluster'}
    else:
        y = 'fn_prob'
        labels = {'bias':'Political Bias',
                'fn_prob':'Weighted Probability of being Misinformation',
                'cluster':'Cluster'}
                  
    
    
    fig3 = px.scatter(data, x="bias", y=y, color='cluster',
                      custom_data=['id'],
                      labels=labels,
                      category_orders={'cluster':['0','1','2','3']},
                      hover_data={"id":True,
                                  'text_sh':True,
                                  "text":False,
                                  'bias':False,
                                  'fn_prob':False,
                                  'cluster':False})
    
    return fig3

@app.callback(
    Output('bottom_graph2', 'figure'),
    Input('dropdown_strip_2', 'value')
)

def update_fig4(dropdown):
    
    if dropdown == 'Political Bias vs. Clussters':
        y='bias'
        labels={'bias':'Political Bias (Lower leans Democratic)',
              'cluster':'Cluster'}
    else:
        y='fn_prob'
        labels={'bias':'Political Bias',
              'fn_prob':'Probability of being Misinformation',
              'cluster':'Cluster'}
    
    fig4 = px.strip(data, x="cluster", y=y,
                  custom_data=['id'],

                  #title='Probability of Misinformation vs. Predicted Cluster',
                  category_orders={'cluster':['0','1','2','3']},
                  #color_continuous_scale='Bluered',
                  labels = labels,
                  hover_data={"id":True,
                              'text_sh':True,
                              "text":False,
                              'bias':False,
                              'fn_prob':False,
                              'cluster':False})
    fig4.update_xaxes(type='category')
    return fig4

 
        
if __name__ == "__main__":
    app.run_server(debug=True)