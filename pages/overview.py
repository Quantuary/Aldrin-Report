from Data_Handler.preparedData import data, _AFN_NAME, _color, _font
from dash import html
from dash import dcc
import plotly.graph_objs as go
from utils import Header, unixTimeMillis, get_marks_from_start_end, unixToDatetime, make_dash_table
import pandas as pd
from dash.dependencies import Input, Output
from app import app
from plotly.subplots import make_subplots

# =============================================================================
# html component    
# =============================================================================

Report_Purpose = html.Div(
                    [html.Div(
                        [html.H5("Purpose"),
                         html.Br([]),
                         html.P(
                             '''
Project Aldrin aims to improve the competitiveness of A&G products offered on the aggregator website, namely, Compare the Market.
A new product, Oceania, is presented at a discount to Budget Direct in the uncompetitive segments.

This report tracks the performance across this channel(CTM) to provide a vis-a-vis comparison of the comprehensive product only (GOLD COMPREHENSIVE).
A set of indicators such as the conversion rate, average margin and quote ranking are used to gauge the performance of Budget Direct are not negatively impacted by the new product.
                             ''',
                             style={"color": "#ffffff"},
                             className="row",
                            ),
                        ], className="product")   
                    ],className="row")


report_cycle = html.Div(
                [
                html.H6(
                    ["Report Cycle"], className="subtitle padded"),
                html.Table(id="meta"),
                ], className="six columns")

margin_bar = html.Div(
                [
                html.H6("Average Margin on Sold Policy",
                        className="subtitle padded"),
                dcc.Graph(id="margin-bar",
                          config={"displayModeBar": False})
                ], className="six columns")

ranking_bar = html.Div(
                [
                html.H6("Quote Ranking Proportion",
                        className="subtitle padded"),
                dcc.Graph(id="ranking-bar",
                          config={"displayModeBar": False}),
                html.Li( '''Oceania Ranking available 7 MAR2022 onwards'''
                        )
                ], className="six columns")

channel = dcc.Checklist(id="channel",
            options = [{'label':'CTM', 'value':'CTM'},
                       {'label':'Direct','value':'Others'}],
            value=['CTM'],
            labelStyle={'display': 'inline-block',
                        "padding-right" : "0.5rem",
                        },
            persistence=True, persistence_type='memory'
        )

premium_chart = html.Div(
                [
                html.H6("Sales",
                        className="subtitle padded"),
                channel,
                dcc.Graph(id="premium-chart",
                          config={"displayModeBar": False}),                
                ], className="six columns")

time_axis = data.data.sales['GOLD'].index.droplevel(level='CHANNEL')
date_range = html.Div(
                [
                html.Label(id='date-label',
                           style={'font-weight': 'bold'}),
                dcc.RangeSlider(
                    id='date-rage',
                    min= unixTimeMillis(time_axis.min())+3600*24,
                    max= unixTimeMillis(time_axis.max())+3600*24*7,
                    step=1*60*60*24*7,
                    pushable=2, 
                    allowCross=False,
                    updatemode='drag',
                    value=[unixTimeMillis(time_axis.min())+3600*24,
                           unixTimeMillis(time_axis.max())+3600*24],
                    marks=get_marks_from_start_end(time_axis.min(),
                                                   time_axis.max()),
                    dots=True,
                    included=True,
                    #tooltip={"placement": "bottom", "always_visible": True}
            
                    )
                ])



# =============================================================================
# callbacks
# =============================================================================
@app.callback([Output('premium-chart','figure'),
               Output('ranking-bar','figure'),
               Output('date-label','children'),
               Output('margin-bar','figure'),
               Output('meta','children')
               ],
              [Input('date-rage','value'),
               Input('channel','value')])    
def update_graph(date_range, channel):
    
    '''
    start end format as 'YYYY-MM-DD'
    '''
    start = str( unixToDatetime( min(date_range) ).date() )
    end =   str( unixToDatetime( max(date_range) ).date() )
 
    ############################
    # premium chart
    ############################
    keys = list(_AFN_NAME.keys())
    portfolio = data.data.sales[keys[0]] + data.data.sales[keys[1]].fillna(0) 
    portfolio = portfolio.query("CHANNEL==%s" %channel).droplevel(level='CHANNEL')
    
    # premium Line chart
    premium_fig = make_subplots(specs=[[{"secondary_y": True}]])
    for i in keys:
        df = data.data.sales[i].query("CHANNEL==%s" %channel).droplevel(level='CHANNEL')
        df = df.resample("D").sum()[start:end].fillna(0)
        premium_fig.add_trace(
        go.Scatter(
                x = df.index,
                y = df['VEHICLE_PREMIUM'].cumsum(),
                mode= "lines",
                name= _AFN_NAME[i],
                line={'color': _color[i]},
                hovertemplate='<br>' +
                              'Premium :  $%{y:,.0f}' + 
                              '<br>' +
                              'Sold : %{text}' +
                              '<br>',
                text=['{0:,.0f}'.format(i) for i in df['SALES_COUNT'].cumsum()],                              
                ),
        secondary_y=False,)
        
        # sales volume bar chart
        premium_fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['SALES_COUNT'],
            opacity=0.2,
            marker={'color': _color[i],
                    },
            name = _AFN_NAME[i],
            #showlegend=False,
            hoverinfo='skip'
            ),
        secondary_y=True
        )
    # Portfolio    
    premium_fig.add_trace(
        go.Scatter(
            x= df.index,
            y= portfolio.resample("D").sum()[start:end].fillna(0).cumsum()['VEHICLE_PREMIUM'],
            mode="lines",
            name="Portfolio",
            line={'color': _color["PORTFOLIO"]},
            #showlegend=False,
            ),
        secondary_y=False,)
    
    premium_fig.update_layout(
        hovermode="x unified",
        barmode="stack",
        bargap =0,
        autosize=True,
        title="",
        font={"family": "Raleway", "size": 10},
        height=240,
        width=330,
        legend={
            "x": -0.0277108433735,
            "y": -0.142606516291,
            "orientation": "h",
            },
        margin={"r": 0,"t": 0,"b": 0,"l": 0},
        showlegend=True,
        #    paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={
            "autorange"    : True,
            "linecolor"    : "black",
            "linewidth"    : 1,
            "title"        : "",
            "type"         : "date", #"linear"
            "showline"     : True,
            "linecolor"    : "black",
            "showgrid"     : False,
            "gridcolor"    : "#F0F0F0"
            },
               
        yaxis={
            #"autorange": False,
            "tickprefix" :'$',
            "gridcolor" : "#F0F0F0",
            "showline": True,
            "linecolor" : "black",
            "showgrid": True,
            "gridcolor" : "#F0F0F0" ,
            "mirror": False,
            "nticks": 4,
            "ticklen": 10,
            "ticks": "outside",
            "title": "Cumulative Premium",
            "type": "linear",
            "zeroline": False,
            "zerolinewidth": 4,
            },
            )
    premium_fig.update_yaxes(title_text="Sales Volume",
                             secondary_y=True)
    
    ############################
    # ranking bar chart
    ############################
    d = data.data.ranking
    
    #calculated cummulative quote as denominator
    cum_quote = d["GOLD"][start:end
                          ].groupby('RANKING'
                          ).sum()["QUOTE_COUNT"].sum()
    
    ranking_fig = go.Figure()
    for i in _AFN_NAME:
        r = d[i][start:end].groupby('RANKING').sum()
        proportion = r["QUOTE_COUNT"][0:8]/cum_quote # top8 only
        
        ranking_fig.add_trace(
                go.Bar(
                    x= proportion,
                    y= r.index,
                    marker={'color': _color[i],
                            'line' : {"color": "rgb(255,255,255)",
                                      "width": 0}
                            },
                    orientation='h',
                    texttemplate = ["{0:.2f}%".format(x*100) for x in proportion[0:5]],
                    name = _AFN_NAME[i]
                    )    
            )
        
    ranking_fig.update_layout(
        barmode="stack",
        plot_bgcolor='rgba(0,0,0,0)',
        height=260,
        width=330,
        showlegend=True,
        font= _font,
        legend={
                "x": -0.0228945952895,
                "y": -0.189563896463,
                "orientation": "h",
                "yanchor": "top",
            },
        margin={
                "r": 0,
                "l": 0,
                "t": 35,
                "b": 0,
                },
        
        xaxis={
            "autorange" : False,
            "range": [0.0, 0.5,],
            "type": "linear",
            "showgrid"  : True,
            "gridcolor" : "#F0F0F0",
            "linecolor" : "black",
            "tickformat": ".0%",
            },
    
        
        yaxis={
            "autorange"      :"reversed",
            "linecolor"      : "black",
            "showticklabels" : True,
            "range": [1, 9],
            "title" :"Rank",
            "type": "category",
            "ticklen": 3,
            "ticks": "outside",
            }
        ) 
    label = 'Cummulative Period from %s to %s' %(start, end)
    
    

    def _margin_bar():
        s = pd.concat(data.data.sales_dict, axis=1).T.droplevel(0)
        m = pd.concat(data.data.margin_dict, axis=1).T.droplevel(0)
        avg_margin = m/s
        
        fig = go.Figure()
        for i in _AFN_NAME:
            fig.add_trace(
                go.Bar(
                    x= avg_margin.index,
                    y= avg_margin[i],
                    marker={'color': _color[i],
                            'line' : {"color": "rgb(255,255,255)",
                                      "width": 2}
                            },
                    name = _AFN_NAME[i]
                    ))
                    
        fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                autosize=False,
                bargap=0.35,
                font= _font,
                height=240,
                width=330,
                hovermode="closest",
                showlegend=True,
                legend={
                    "x": -0.0228945952895,
                    "y": -0.189563896463,
                    "orientation": "h",
                    "yanchor": "top",
                },
                margin={
                    "r": 0,
                    "l": 0,
                    "t": 0,
                    "b": 0,
                    
                },
                title="",
                xaxis={
                    "autorange": True,
                    "showline": True,
                    "title": "",
                    "type": "category",
                    "linecolor" : "black",
                },
                yaxis={
                    "autorange": True,
                    "showgrid": True,
                    "showline": True,
                    "title": "",
                    "type": "linear",
                    "zeroline": False,
                    "tickprefix" :'$',
                    "tickformat": ",.0f",
                    "linecolor" : "black",
                    "gridcolor" : "#F0F0F0" 
                },
            )            
        return fig

    def _meta(): 
        df = pd.DataFrame({0: ['Report Last Updated', 'CTM Data as at', 'Sales Data as at', 'Earnix Log as at'],
                           1: [data.data.last_updated.strftime('%Y-%m-%d %H:%M:%S'),
                               data.data.ctm_data_date,
                               data.data.sales_data_date,
                               data.data.Earnix_log_date]
                           })
        return make_dash_table(df)
        
    
    
    return (premium_fig, ranking_fig, label, _margin_bar(), _meta() )
        
        
# =============================================================================
# layout
# =============================================================================

def create_layout(app):
    # Page layouts
    return html.Div(
                [
                html.Div([Header(app)]),
                # page 1
                html.Div(
                        [
                        # Row 1
                        Report_Purpose,
                        
                        # Row 2
                        html.Div(
                            [
                             report_cycle,
                             margin_bar,
                            ],
                            className="row ",
                            style={"margin-bottom": "35px"},
                            ),
                        
                        # Row 3
                        date_range, 
                        html.Div(
                            [
                            ranking_bar,
                            premium_chart,
                            ],className="row "),
                           
                        ], className="sub_page")
                ],className="page"
             )
