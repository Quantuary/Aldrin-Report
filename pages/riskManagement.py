
from Data_Handler.preparedData import _AFN_NAME, _color, _font
from dash import html
from app import app
from utils import Header



discounted_portion = []


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
                    # Row 1
                    html.Div(
                        [
                        html.Div(
                            [
                            html.H6("Severity", className="subtitle padded"),
                            #frequency_select,
                            discounted_portion,
                            ],className="six columns"),
                        html.Div(
                            [
                            html.H6("% Frequency", className="subtitle padded"),
                            # require CTM data actual vs expected
                            ],className="six columns")
                        ],className="row "),
                    
                    # Row 2
                    html.Div(
                        [
                        html.Div(
                            [
                            html.H6("Loss Ratio", className="subtitle padded"),
                            #conversion_table,
                            ],className="twelve columns"),

                        ],className="row "),
                    
                    # Row 3
                    html.Div(
                        [
                            
                        ],className="row ")
    
                    ], className="sub_page"),
                ],className="page")