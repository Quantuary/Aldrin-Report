from dash import html
from utils import Header


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Notes", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                '''
                                                Please note that some data are a few days in arrears,
                                                e.g. The actual ranking from CTM is uploaded 2-3 days behind the reporting cycle.
                                                '''
                                            ),
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                    
                                    html.H6("Updates & Changes", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li( '''01/04/2022 - Model Refreshed'''),
                                            html.Li( '''01/03/2022 - Oceania going live'''),
                                            html.Li( '''07/03/2022 - Oceania ranking is made available but incorrect'''),
                                        ],
                                        id="reviews-bullet-pts",
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="row",
                            ),
                            html.Div(
                                [
                                    html.H6("Definition", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                        html.P(
                                            '''
                                            Page : Overview
                                            '''
                                        ),
                                        html.Li(
                                            "Margin = Vehicle Premium - [Actuarial Cost + Direct Cost]"
                                        ),
                                        html.Li(
                                            '''
                                            Sales count are order by sales date and inclusive of subsequent cancelled policies.
                                            '''
                                        ),
                                        html.Li(
                                            '''
                                            The sales figure consider sales count from channel ['2','4','6'] and media type ["CM",'19','41','OA'] only.
                                            '''
                                        ),
                                        html.Li(
                                            '''
                                            The tick box CTM filter for media type = "CM" only, and Direct is other media type listed above.
                                            
                                            '''
                                        ),
                                        html.P(
                                            '''
                                            Page : Model Tracking
                                            '''
                                        ),                                        
                                        ],
                                        id="reviews-bullet-pts",
                                    ),
                                    html.Div(
                                        [

                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="row ",
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
