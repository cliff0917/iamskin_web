import plotly.graph_objects as go

def pie(col_name, col_val):
    fig = go.Figure(go.Pie(
        name='',
        labels = col_name,
        values = col_val,
        text = col_name,
        hovertemplate = "%{label} <br>預測機率: %{percent}",
    ))
    return fig