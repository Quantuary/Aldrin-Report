from Data_Handler.preparedData import data, _font, _color
from utils import Header, get_timeAxis
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from datetime import date
from app import app
from dash.dependencies import Input, Output


date_range = html.Div(
                [
               dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed = date(2022, 3, 1),
                    max_date_allowed = date(2029, 9, 9),
                    start_date = date(2022, 3, 1),
                    end_date = data.data.ctm_data_date,
                    display_format = 'DD MMM Y',
                    initial_visible_month=date(2022, 3, 1),
                    end_date_placeholder_text="End Period",
                    ),
                ], 
                )
AnnualKM_Banding = dcc.RadioItems(id="annualKM",
            options = [{'label':'Exclude LowKM', 'value':'EXLowKM'},
                       {'label':'Include LowKM','value':'all'}],
            value='all',
            labelStyle={'display': 'inline-block',
                        "padding-right" : "0.5rem",
                        },
            persistence=True, persistence_type='memory'
        ) 
sale_status = dcc.RadioItems(id="sale_status",
            options = [{'label':'Policies', 'value':'SOLD'},
                       {'label':'Quotes','value':'all'}],
            value='all',
            labelStyle={'display': 'inline-block',
                        "padding-right" : "0.5rem",
                        },
            persistence=True, persistence_type='memory'
        ) 

   
confusion_matrix = dcc.Graph(
                    id='confusion_matrix',
                    config={"displayModeBar": False}
                    )
comparison_matrix = dcc.Graph(id='comparison_matrix',
                    config={"displayModeBar": False}
                    )
false_positive_rate = dcc.Graph(id="false_positive_rate",
                          config={"displayModeBar": False})
discounted_portion = dcc.Graph(id="discount_portion",
                          config={"displayModeBar": False})


# =============================================================================
# callbacks
# =============================================================================
@app.callback([Output('comparison_matrix','figure'),
               Output('confusion_matrix','figure'),
               Output('false_positive_rate','figure'),
               Output('discount_portion','figure')],
              [Input('date-picker','start_date'),
               Input('date-picker','end_date'),
               Input('annualKM','value'),
               Input('sale_status','value')])
def update(start, end, km, sale_status):
   
    def heatmap(start=start, end=end, AnnualKM_Banding=km, sale_status=sale_status):
        df = data.data.heatmap[start:end]
        
        if AnnualKM_Banding=="EXLowKM":
            df = df[df['AnnualKM_Banding']!='LowKM']
        if sale_status=="SOLD":
            df = df[df['SALE_STATUS']==sale_status]            
        
        df = df.groupby(['GOLD_RANKING','OCEA_RANKING'], as_index=False).sum()
            
        z = np.zeros((8,8))
        
        for x in range(1,9):
            for y in range(1,9):
                try:
                    z[x-1][y-1] = df[(df['GOLD_RANKING']==x) & (df['OCEA_RANKING']==y) ]['QUOTE_COUNT'].values
                except:
                    continue
    
        #inverse the order for plot
        z = z[::-1,...]
        total = df['QUOTE_COUNT'].sum()
        x=['`1','`2','`3','`4','`5','`6','`7','`8']
        y=['`8','`7','`6','`5','`4','`3','`2','`1']
        texttemplate = pd.DataFrame(z/total).applymap(lambda i: '{:.1%}'.format(i)).values
        
        
        hover=[]
        for i in z:
            hover.append(['{0:,.0f}'.format(j) + '  / <br>' + '{0:,.0f}'.format(total) for j in i])
            
        fig = ff.create_annotated_heatmap(z,x=x,y=y,
                                          annotation_text=texttemplate,
                                          text=hover,
                                          hoverinfo='text',
                                          colorscale='Reds') #RdBu
        fig.update_layout(
                   width  =400,
                   height =350,
                   font   =_font,
                   margin={"r": 0,
                           "t": 0,
                           "b": 0,
                           "l": 0,},
                   
                  yaxis={"title" :"Budget Gold Ranking",
                         },
                  xaxis={"title" :"Oceania Ranking",
                         }
                  )
        return fig
    
    def false_positive(start=start, end=end, AnnualKM_Banding=km):
        df = data.data.ave[start:end].reset_index()
        if AnnualKM_Banding=="EXLowKM":
            df = df[df['AnnualKM_Banding']!='LowKM']        
        top = df[df['RANKING']=='1. Rank Top']
        total_top = top.resample('D',  on='DATE').sum().sort_values(by='DATE')

        top_dis = top[top['PREDICTED']=='2.Discounted'
                      ].resample('D',  on='DATE').sum().sort_values(by='DATE')
        
        FPR = top_dis.div(total_top)
        
        fig = go.Figure()
        fig.add_trace(
        go.Scatter(
            x=FPR.index,
            y=FPR["QUOTE_COUNT"],
            mode="lines",
            name="False Positive Rate",
            line={"color": _color["GOLD"]},
            #xperiod =xperiod(freq),
            #xperiodalignment="start",
            ),
        )
        fig.update_layout(
            #hovermode="x unified",  
            #barmode="stack",
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=True,
            width  =400,
            height =250,
            font= _font,
            
            margin={
                    "r": 0,
                    "l": 0,
                    "t": 0,
                    "b": 0,
                    },
            xaxis= {"autorange" : True,
                    "showgrid"  : True,
                    "showline"  : True,
                    "type"      : "date",
                    "linecolor" : "black",
                    "nticks"    : 5,
                    #"title"     : "Rate Effective Date",
                    "gridcolor" : "#F0F0F0"
                    },
            yaxis={
                    "autorange" : True,   
                    #"range": [.05, 0.18],
                    "showgrid": True,
                    "type"      : "linear",
                    "zeroline"  : True,
                    "nticks"    : 4,
                    "tickformat": ".2%",
                    "linecolor" : "black",
                    "gridcolor" : "#F0F0F0"
                              },
            )
        
        
        return fig
        

    def confusion_matrix(start=start, end=end, AnnualKM_Banding=km):
        df = data.data.ave[start:end]
        if AnnualKM_Banding=="EXLowKM":
            df = df[df['AnnualKM_Banding']!='LowKM']
        # get rid of all time index
        df = df.groupby(['RANKING','PREDICTED'], as_index=False).sum()
        z = df.pivot_table(index="RANKING", columns="PREDICTED", 
                           fill_value=0, values='QUOTE_COUNT').values
    
        x1=['Loaded','Discounted',]
        y1=['Bottom','Top']
        z = z[::-1,...]
        texttemplate = pd.DataFrame(z).applymap(lambda i: '{:,.0f}'.format(i)).values
    
        fig = ff.create_annotated_heatmap(z, x=x1, y=y1,
                                          annotation_text=texttemplate,
                                          hoverinfo='none', colorscale='Reds') #RdBu
        fig.update_layout(
                   width  =230,
                   height =140,
                   font   =_font,
                   
                   margin={"r": 0,
                           "t": 0,
                           "b": 0,
                           "l": 0,
                           }
                  )
        
        return fig
    
    def discount_portion(start=start, end=end, AnnualKM_Banding=km):
        df = data.data.percentageDiscount[start:end].reset_index()
        if AnnualKM_Banding=="EXLowKM":
            df = df[df['AnnualKM_Banding']!='LowKM']  
        ############################
        # percentage discount bar chart
        ############################
        df = df.groupby('REASON').resample('D',  on='DATE').sum().reset_index().sort_values(by='DATE')
        total = df.resample('D',  on='DATE').sum().reset_index().sort_values(by='DATE')
        total.set_index('DATE', inplace=True)
        df.set_index('DATE', inplace=True)
        
    
        discounted = df.loc[df['REASON']=='Discounted']['QUOTE_COUNT']/total['QUOTE_COUNT']
        prvins_BD = df.loc[df['REASON']=='Previous Insurer BD']['QUOTE_COUNT']/total['QUOTE_COUNT']
        margin_fail = df.loc[df['REASON']=='Margin not Allowed']['QUOTE_COUNT']/total['QUOTE_COUNT']
        fig = go.Figure()
        fig.add_trace(
                    go.Bar(
                        x= discounted.index,
                        y= discounted,
                        marker={"color": "#97151c"},
                        name = 'Discounted',
                        ))
        fig.add_trace(
                    go.Bar(
                        x= prvins_BD.index,
                        y= prvins_BD,
                        marker={"color": "#4d4d4d"},
                        name = 'Previous Insurer BD',
                        ))
        fig.add_trace(
                    go.Bar(
                        x= margin_fail.index,
                        y= margin_fail,
                        marker={"color": "#e0e0e0"},
                        name = 'Margin Not Allowed',
                        ))
        fig.update_layout(
            hovermode="x unified",  
            barmode="stack",
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=True,
            width  =400,
            height =250,
            font= _font,
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
            xaxis=get_timeAxis(),
            yaxis={
                   "range": [0, 0.5],
                    "type"      : "linear",
                    "zeroline"  : True,
                    "nticks"    : 4,
                    "tickformat": ".2%",
                    "linecolor" : "black",
                    "gridcolor" : "#F0F0F0"
                              },
            )
        return fig
    
    
    return (heatmap(), confusion_matrix(), false_positive(), discount_portion())



# =============================================================================
# layout
# =============================================================================
def create_layout(app):
    return html.Div(
                [
                Header(app),
                
                # page 3
                html.Div(
                    [ 
                    # Row 1 selection
                    html.Div(
                        [
                        html.Div(
                            [
                            date_range,
                            ],className="five columns"),   
                        html.Div(
                            [
                            AnnualKM_Banding,    
                            ],className="seven columns"),                        
                        ],className="row "),

                    # Row 2
                    html.Div(
                        [
                        html.Div(
                            [
                            html.H6("Confusion Matrix", className="subtitle padded"),
                            confusion_matrix,
                            ],className="five columns"),   
                        html.Div(
                            [
                            html.H6("Rank Comparison Matrix", className="subtitle padded"),
                            sale_status,
                            comparison_matrix,
                            ],className="seven columns"),                        
                        ],className="row "),
                    
                    # Row 3
                    html.Div(
                        [
                        html.Div(
                            [
                       
                            
                            ],className="four columns"),                            
                        html.Div(
                            [
                            html.H6("False Positive Rate", className="subtitle padded"),
                            #frequency_select,
                            false_positive_rate,
                            ],className="eight columns")
                        ],className="row "),                    
                    # Row 4
                    html.Div(
                        [
                        html.Div(
                            [
                            html.H6("Percentage Discounted", className="subtitle padded"),
                            discounted_portion,
                            ],className="nine columns"),                       
                        ],className="row ")
    
                    ], className="sub_page"),
                ],className="page")