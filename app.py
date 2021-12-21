import dash
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd

corrMatrix = pd.read_pickle(r"corrMatrix.pkl")


df = pd.read_csv(r'steam-200k.csv',header=None,names=['userId','game','purchaseOrPlay','hoursPlayed','rating'])

# Remove the lines with the purchase attribute
df = df.drop(df.loc[df['purchaseOrPlay']=="purchase"].index)
df = df.drop(columns=['purchaseOrPlay'])
games = df['game'].unique()
games.sort()
allGames = [{'label':i,'value':i} for i in games]

popularGames = pd.DataFrame(df['game'].value_counts()).reset_index()
popularGames.rename({'index': 'game', 'game': 'count'}, axis=1, inplace=True)


app = dash.Dash()
colors = {
    'background': 'white',
    'text': 'black'
}

app.layout = html.Div(style={'backgroundColor': colors['background'],'padding-left':'200px','padding-right':'200px'}, children=[
    html.H1(
        children='Steam Video-games recommendation',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    html.Div(children='Made with Dash', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Br(),
    html.Br(),
    html.Br(),


    html.H2(
            children='Select games you like :',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
    ),

html.Div(style={'width':'60%','margin':'auto'}, children=[
    dcc.Dropdown(
    id='selectedGames',
    options=[{'label':i,'value':i} for i in games],
    multi=True
),
]),

    html.Br(),
    html.Br(),
    html.Br(),

    html.H2(
            children='Your recommendations :',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
    ),

    html.Div(style={'width':'50%','margin':'auto'}, children=[
    dash_table.DataTable(
                id='recommendedGames',
                columns=[{"name": i, "id": i} for i in ['game','score']],
                data=None,
            ),
    ]),

    html.Br(),
    html.Br(),
    html.Br(),

    html.H2(
            children='Most popular games in the dataset :',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
    ),
html.Div(style={'width':'30%','margin':'auto'}, children=[
    dash_table.DataTable(
                id='popularGames',
                columns=[{"name": i, "id": i} for i in ['game','count']],
                data=popularGames.to_dict('records'),
                page_size=15
            ),
])

])


@app.callback(
    dash.dependencies.Output('recommendedGames', 'data'),
    dash.dependencies.Input('selectedGames', 'value'),
     )

def update_recommendedGames(value):
    if value != None:
        recommendedGames = recommend_games(value)
        print(recommendedGames)
        res = pd.DataFrame(recommendedGames,columns=['game','score'])
        return res.to_dict('records')



def recommend_games(list):
    myRatings = pd.DataFrame(columns=['game', 'rating'])
    for game in list:
        myRatings = myRatings.append({'game':game, 'rating':5}, ignore_index=True)
    myRatings = myRatings.set_index('game')
    similarGames = pd.Series(dtype='float64')
    for i in range(0, len(myRatings.index)):
        similar_temp = corrMatrix[myRatings.index[i]].dropna()
        similar_temp = similar_temp.map(lambda x: x * myRatings.iloc[i]['rating'])
        similarGames = similarGames.append(similar_temp)
        
    similarGames = similarGames.groupby(similarGames.index).sum()
    similarGames = similarGames.drop(similarGames.loc[similarGames.index.isin(myRatings.index)].index)

    similarGames.sort_values(inplace = True, ascending = False)
    similarGames = similarGames[0:10]
    similarGames = similarGames.reset_index()
    similarGames.rename({'index': 'game', 0: 'score'}, axis=1, inplace=True)
    return similarGames
    
if __name__ == '__main__':
    app.run_server(debug=True)