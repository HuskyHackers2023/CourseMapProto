# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from nltk.corpus import stopwords
import gensim.downloader as api
import networkx as nx
import plotly.graph_objects as go
import re as rg
word_vectors = api.load("glove-wiki-gigaword-300")
l = stopwords.words('english')
l.append('used')
l.append('focuses')
l.append('often')
l.append('accumulo')
l.append('blockchain')
l.append('Blockchain')
l.append('untraceability')
l.append('cryptocurrency')
l.append('cryptocurrencies')
l.append('wireframes')
l.append('pmbok')
df = pd.read_csv('data/CourseDetails.csv')
ed = pd.read_csv('data/Book1.csv')
po = pd.read_csv('data/Position.csv')
po = po.set_index('index')

def pr(s):
    re =''
    s = s.replace("-", " ")
    s = s.replace("/", " ")
    s = s.replace(".", " ")
    s = s.replace(",", " ")
    s = rg.sub(rg.compile("[^A-Za-z]"), " ", s.lower())
    for s_ in s.split():
        if s_ not in l:
            re+=' '+s_
    return re.split()

df['keyword_'] = df['Course_Name'].apply(lambda x: pr(x))
df['keywords'] = df['Description'].apply(lambda x: pr(x))

def scoring(st):
    c_l =[]
    sc = []
    for c in df.Course_Name:
        s = []
        for w in df[df.Course_Name==c]['keywords']:
            for w_ in w:
                te = glove_vectors.similarity(st, w_)
                s.append(te)
        for w in df[df.Course_Name==c]['keyword_']:
            for w_ in w:
                te = word_vectors.similarity(st, w_)
                s.append(te)
        c_ = 0
        for s_ in s:
            if s_>0.38:
                c_+=1
        if c_>1:
            c_l.append(c)
        
    return c_l

G = nx.DiGraph()
for cn in df.CourseID:
    G.add_node(cn, pos = [po.loc[cn,:][0],po.loc[cn,:][1]])
for i in range(len(ed)):
    G.add_edge(ed.n1[i], ed.n2[i])
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=5, color='#888'),
    hoverinfo='none',
    mode="lines")
node_x = []
node_y = []
ll = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)
    ll.append(node)
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=25,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))
node_trace.text = ll
                          
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='test',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('data\CourseDetails.csv')
ed = pd.read_csv('data\Book1.csv')
po = pd.read_csv('data\Position.csv')



app.layout = html.Div(children=[
    html.H1(children='Course Advisor'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
