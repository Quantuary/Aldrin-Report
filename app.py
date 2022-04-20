# -*- coding: utf-8 -*-
import dash


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True)
app.title = "ML Report"
server = app.server


