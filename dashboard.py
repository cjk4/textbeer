import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

app = dash.Dash(__name__)
app.title = "861 Beers"

numbers = [int(os.getenv("USER_1_NUMBER")), int(os.getenv("USER_2_NUMBER")), int(os.getenv("USER_3_NUMBER"))]
names = [os.getenv("USER_1"), os.getenv("USER_2"), os.getenv("USER_3")]

NICKNAMES = dict(zip(numbers, names))

beer_background = {
    'background-image': 'url("https://em-content.zobj.net/source/microsoft-teams/363/beer-mug_1f37a.png")',
    'background-repeat': 'repeat',
    'background-size': '100px',
    'height': '100vh',
    'padding': '20px',
}

app.layout = html.Div([
    html.H1("Live Beer Dashboard", style={'color': 'red', 'text-shadow': '2px 2px black'}),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),
    dcc.Graph(id='beer-graph'),
], style=beer_background)

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
    count.columns = ["Roommate", "Beers"]
    print("Raw phone numbers in count:")
    print(count["Roommate"].tolist())
    count["Roommate"] = count["Roommate"].map(NICKNAMES).fillna("Unknown")
    print(NICKNAMES)
    fig = px.bar(count, x="Roommate", y="Beers", title="Dashboard", color="Roommate")
    fig.update_layout(xaxis_title="Roommate", yaxis_title="Beers", template="plotly_white")
    return fig

beer_background = {
    'background-image': 'url("https://em-content.zobj.net/source/microsoft-teams/363/beer-mug_1f37a.png")',
    'background-repeat': 'repeat',
    'background-size': '100px',
    'height': '100vh',
    'padding': '20px',
}


if __name__ == "__main__":
    app.run()