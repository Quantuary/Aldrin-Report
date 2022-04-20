from Data_Handler.preparedData import data, _AFN_NAME, _color, _font
from dash import html
from dash import dcc
import plotly.graph_objs as go
from utils import Header, make_dash_table, get_timeAxis
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from app import app
from plotly.subplots import make_subplots

 

# =============================================================================
# html component    
# =============================================================================
conversion_graph = dcc.Graph(id="conv_graph",
                    config={"displayModeBar": False})
                    
frequency_select = dcc.Dropdown(id='freq',
                    options=[{'label':'daily'     , 'value':'D'},
                             {'label':'weekly'    , 'value':'W'},
                             {'label':'bi-weekly' , 'value':'2W'},
                             {'label':'monthly'   , 'value':'M'},
                             {'label':'quarterly' , 'value':'Q'},
                             ],
                    value='W', multi=False,
                    persistence=True, persistence_type='memory')
                                    
conversion_table = html.Div([
                        html.Table(make_dash_table(data.data.conversion_summary),
                                   className="tiny-header",
                                   )
                            ],style={"overflow-x": "auto"})
                            
brand_select = dcc.Dropdown(id='brand',
                            options=[{'label':'Budget Direct' , 'value':'GOLD'},
                                     {'label':'Oceania'       , 'value':'OCEA'},
                                     {'label':'Portfolio'     , 'value':'PORTFOLIO'},
                                     ],
                            value='PORTFOLIO', multi=False,
                            persistence=True, persistence_type='memory')
                            
conversion_delta = dcc.Graph(id='period_o_period', 
                    config={"displayModeBar": False})
                    
# =============================================================================
# callbacks
# =============================================================================
@app.callback([Output('period_o_period','figure')
               ],
              [Input('brand','value')])
def _delta(brand):
    c = data.data.conversion_dict
    #############################
    # Calculate period-over-period 
    #############################
    def _last_period(N):
        df = data.data.ts[-N*2:-N].sum()
        c_ = {}   # conversion rate of Ndays one period ago
        for i in _AFN_NAME:    
            s = df[i]['SALES_COUNT']
            q = df[i]['QUOTE_COUNT']
            c_[i] = np.divide(s, q, out=np.zeros_like(s), where=q!=0)
    
        # calculate portfolio total           
        s = df["GOLD"]['SALES_COUNT'] + df["OCEA"]['SALES_COUNT'] 
        q = df["GOLD"]['QUOTE_COUNT']
        c_['PORTFOLIO'] = np.divide(s, q, out=np.zeros_like(s), where=q!=0)
        
        # make dict into dataframe
        df_last_period = pd.DataFrame(c_.items())
        df_last_period.set_index([0], inplace=True)
        
        # rename column name
        df_last_period.rename(columns={1: '%sd_LP'%N }, inplace=True)
     
        return df_last_period
    
    c_LP = _last_period(7)
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
                 mode = "number+delta",
                 value = float(c['7d'].loc[brand] *100),
                 number = {'suffix': " %",
                           "font":{"color":"#b5b5b5",
                                   "size" : 30}},
                 title = {"text": "<br><span style='font-size:2em;color:gray'> Conversion 7D </span>" },
                 delta = {'position': "bottom",
                          'reference': float(c_LP.loc[brand]*100) ,
                          'relative': False},
                 domain = {'row': 0, 'column': 0}))

    fig.update_layout(
            grid = {'rows': 1, 'columns': 1, 'pattern': "independent"},
            height=120, width=150,
            margin=dict(l=0, r=0, t=0, b=0),
            

            )
    return (fig,)


@app.callback([Output('conv_graph','figure')
               ],
              [Input('freq','value')])
def update_graph(freq):
    
    def generate_data(freq):
        df = data.data.ts.resample(freq).sum()
        quote_cnt = df['GOLD']['QUOTE_COUNT']
                
        y={}
        for i in _AFN_NAME:
            y[i]=df[i]["SALES_COUNT"].div(df[i]["QUOTE_COUNT"])
        conv_rate = pd.concat(y,axis=1).fillna(0)
        conv_rate["PORTFOLIO"] = conv_rate[conv_rate.columns[0]] + conv_rate[conv_rate.columns[1]]
        return conv_rate, quote_cnt

    
    conv_rate, quote_cnt = generate_data(freq)
    
    def xperiod(freq):
        if freq=="M" :
            return "M1"
        elif freq=="Q":
            return "M2"
        else:
            return None
        
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for i in _AFN_NAME:
        fig.add_trace(
        go.Scatter(
            x=conv_rate.index,
            y=conv_rate[i],
            mode="lines",
            name=_AFN_NAME[i],
            line={"color": _color[i]},
            xperiod =xperiod(freq),
            xperiodalignment="start",
            ),
        secondary_y=False,
        )
    
    #portfolio view
    fig.add_trace(
    go.Scatter(
        x=conv_rate.index,
        y=conv_rate["PORTFOLIO"],
        mode="lines",
        name="Portfolio",
        line={"color": _color["PORTFOLIO"]},
        xperiod =xperiod(freq),
        xperiodalignment="start",
        ),
    secondary_y=False,
    )
    
    # barchart
    fig.add_trace(
    go.Bar(
        x=conv_rate.index,
        y=quote_cnt,
        opacity=0.4,
        marker={'color': "#b5b5b5",
                #'line' : {"color": "rgb(255,255,255)",
                #"width": 2
                },
        name = "Quote Volume",
        xperiod =xperiod(freq),
        xperiodalignment="start",
        ),
    secondary_y=True
    )
    
    
    fig.update_layout(
               hovermode="x unified",       
               autosize=True,
               width  =700,
               height =200,
               bargap =0,
               font   =_font,
               margin={"r": 30,
                       "t": 30,
                       "b": 30,
                       "l": 30,},
               showlegend=True,
               titlefont= _font,
               #    paper_bgcolor='rgba(0,0,0,0)',
               plot_bgcolor='rgba(0,0,0,0)',
               xaxis=get_timeAxis(),
               
               yaxis={"autorange": True,
                      "type"      : "linear",
                      "zeroline"  : True,
                      "nticks"    : 4,
                      "tickformat": ".2%",
                      "linecolor" : "black",
                      "gridcolor" : "#F0F0F0"
                                },
               )
    
    #fig.update_yaxes(title_text="Conversion Rate", secondary_y=False)
    fig.update_yaxes(title_text="Quote Volume", secondary_y=True)
    
    return (fig,)

# =============================================================================
# layout
# =============================================================================
def create_layout(app):
    return html.Div(
                [
                Header(app),
                
                # page 2
                html.Div(
                    [ 
                    # Row 1
                    html.Div(
                        [
                        html.Div(
                            [
                            html.H6("Conversion Rate", className="subtitle padded"),
                            frequency_select,
                            conversion_graph,
                            ],className="twelve columns")
                        ],className="row "),
                    
                    # Row 2
                    html.Div(
                        [
                        html.Div(
                            [
                            html.H6("Rolling Conversion Rate", className="subtitle padded"),
                            conversion_table,
                            ],className="nine columns"),
                        html.Div(
                            [
                            html.H6("Delta", className="subtitle padded"),
                            brand_select,
                            conversion_delta,
                            ],className="three columns")
                        ],className="row "),
                    
                    # Row 3
                    html.Div(
                        [
                         html.Div(
                            [
                            html.H6("Financial Result", className="subtitle padded"),
                            #financial performance,
                            ],className="twelve columns"),    
                        ],className="row ")
    
                    ], className="sub_page"),
                ],className="page")