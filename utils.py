from dash import html
from dash import dcc
import pandas as pd
import time
from dateutil.relativedelta import relativedelta

def get_timeAxis():
    return {"autorange"    : True,
           "rangeselector": {"buttons": [
                            {   "count": 1,
                                "label": "1m",
                                "step": "month",
                                "stepmode": "backward",
                            },
                            {   "count": 6,
                                "label": "6m",
                                "step": "month",
                                "stepmode": "backward",
                            },
                            {   "count": 1,
                                "label": "YTD",
                                "step": "year",
                                "stepmode":"todate"
                            },
                            {   "count": 1,
                                "label": "1Y",
                                "step": "year",
                                "stepmode": "backward",
                            },
                            {   "label": "All",
                                "step": "all",
                            },]
                            },
            "showline": True,
            "type"    : "date",
            "linecolor" : "black",
            "nticks"    : 5,
            }



def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("a&g logo.png"),
                            className="logo",
                        ),
                        href="https://plotly.com/dash",
                    ),
                   
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Oceania Performance Tracking")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/ml-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/ml-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "Portfolio Performance",
                href="/ml-report/portfolio-performance",
                className="tab",
            ),
            dcc.Link(
                "Risk & Management",
                href="/ml-report/risk-management",
                className="tab",
            ),
            dcc.Link(
                "Model Tracking", href="/ml-report/model-tracking", className="tab"
            ),
            dcc.Link(
                "Appendix & Glossary",
                href="/ml-report/appendix-glossary",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s')

def get_marks_from_start_end(start, end):
    ''' Returns dict with one item per week
    {seconds: '2015-08',
    '''
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += relativedelta(weeks=4)
    return {unixTimeMillis(m): str(m.strftime('%Y-%m-%d')) for m in result}