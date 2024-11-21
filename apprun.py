# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 11:17:55 2022

@author: mleong
"""
from datetime import datetime
from Data_Handler.preparedData import retrieve, data
from app import app
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from pages import (
    overview,
    portfolioPerformance,
    riskManagement,
    modelTracking,
    appendix
)

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    #### This step is to trigger a refresh at 6am without restarting the app ##
    today=datetime.now().replace(hour=6,minute=0,second=0,microsecond=0)   
    
    if data.data.last_updated < today:
        data.data=retrieve()
    ##########################################################################
    
    
    
    if pathname == "/ml-report/portfolio-performance":
        return portfolioPerformance.create_layout(app)
    elif pathname == "/ml-report/risk-management":
        return riskManagement.create_layout(app)
    elif pathname == "/ml-report/model-tracking":
        return modelTracking.create_layout(app)  
    elif pathname == "/ml-report/appendix-glossary":
        return appendix.create_layout(app)
        
    elif pathname == "/ml-report/full-view":
        return (overview.create_layout(app),
                portfolioPerformance.create_layout(app),
                #riskManagement.create_layout(app),
                modelTracking.create_layout(app),
                #pricePerformance.create_layout(app)
                )
    else:
       return overview.create_layout(app)
      
if __name__ == "__main__":
    app.run_server(host='0.0.0.0',debug=False, port=8080)