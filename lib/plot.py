import plotly.graph_objects as go

def pie(likelihood, output_path):
    class_name, class_prob = [], []

    for k, v in likelihood.items():
        class_name.append(k)
        class_prob.append(v)

    fig = go.Figure(go.Pie(
        name='',
        labels=class_name,
        values=class_prob,
        text=class_name
    ))
    fig.write_image(output_path) # save
    return fig