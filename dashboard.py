import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)
app.title = "861 Beers"

NICKNAMES = {
    os.getenv("USER_1_NUMBER"): os.getenv("USER_1"),
    os.getenv("USER_2_NUMBER"): os.getenv("USER_2"),
    os.getenv("USER_3_NUMBER"): os.getenv("USER_3")
}

app.layout = html.Div([
    html.H1("861 Beers"),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),
    dcc.Graph(id='beer-graph'),
])

@app.callback(
    Output('beer-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    try:
        df = pd.read_csv("beer_log.csv", header=None, names=["timestamp", "number", "text"])
    except Exception:
        df = pd.DataFrame(columns=["timestamp", "number", "text"])

    df = df[df["text"].str.contains("beer", case=False, na=False)]

    count = df["number"].value_counts().reset_index()
    count.columns = ["Phone Number", "Beers"]
    # print("Raw phone numbers in count:")
    # print(count["Phone Number"].tolist())
    count["Phone Number"] = count["Phone Number"].map(NICKNAMES).fillna("Unknown")

    fig = px.bar(count, x="Phone Number", y="Beers", title="Total Beers Drank by Number", color="Phone Number")
    fig.update_layout(xaxis_title="Roommate", yaxis_title="Beers", template="plotly_white")
    return fig

if __name__ == "__main__":
    app.run()