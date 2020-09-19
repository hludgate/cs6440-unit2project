import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go


app = dash.Dash(__name__)

server = app.server

excel = 'cs6440-unit2project/plotly_small.xlsx'
state_code = 'cs6440-unit2project/state_codes.xlsx'
dt = pd.read_excel(state_code)
dt = dt.set_index('State').T.to_dict('list')
df = pd.read_excel(excel)

df = df[df['SP_DEPRESSN'] > 1]
df['SP_ALZHDMTA'] = df['SP_ALZHDMTA'] -1
df['SP_OSTEOPRS'] = df['SP_OSTEOPRS'] -1
df['SP_CHRNKIDN'] = df['SP_CHRNKIDN'] -1
df['SP_CHF'] = df['SP_CHF'] -1
df['SP_CNCR'] = df['SP_CNCR'] -1
df['SP_COPD'] = df['SP_COPD'] -1
df['SP_DIABETES'] = df['SP_DIABETES'] -1
df['SP_ISCHMCHT'] = df['SP_ISCHMCHT'] -1
df['SP_RA_OA'] = df['SP_RA_OA'] -1
df['SP_STRKETIA'] = df['SP_STRKETIA'] -1

df_states = []
df_states_info = pd.DataFrame(columns=['State','Average_Chronic','Alzheimers','Osteoporosis','Chronic Kidney Disease',
                                       'Heart Failure','Cancer','COPD','Diabetes','Ischemic Heart Disease','Arthritis','Stroke'])
i = 0
for state in dt:
    df_state = df[df['SP_STATE_CODE']==dt[state][0]]
    df_state['chronic_sum'] = df_state['SP_ALZHDMTA'] + df_state['SP_OSTEOPRS'] + df_state['SP_CHRNKIDN'] +df_state['SP_CHF'] + \
    df_state['SP_CNCR'] + df_state['SP_COPD'] + df_state['SP_DIABETES']+ df_state['SP_ISCHMCHT']+ df_state['SP_RA_OA'] + \
    df_state['SP_STRKETIA']
    df_states_info.loc[i]=[state,df_state['chronic_sum'].mean(),df_state['SP_ALZHDMTA'].sum(),df_state['SP_OSTEOPRS'].sum(),df_state['SP_CHRNKIDN'].sum(),
                       df_state['SP_CHF'].sum(),df_state['SP_CNCR'].sum(),df_state['SP_COPD'].sum(), df_state['SP_DIABETES'].sum(),
                       df_state['SP_ISCHMCHT'].sum(),df_state['SP_RA_OA'].sum(),df_state['SP_STRKETIA'].sum()]
    i += 1
     
fig = go.Figure(data=go.Choropleth(
    locations=df_states_info['State'], # Spatial coordinates
    z = df_states_info['Average_Chronic'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Average Chronic Illnesses",
))

fig.update_layout(
    title_text = '2008 US Average # of Chronic Illnesses of patients with Depression',
    geo_scope='usa', # limite map scope to USA
)
    

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

#@app.callback(dash.dependencies.Output('display-value', 'children'),
#              [dash.dependencies.Input('dropdown', 'value')])
#def display_value(value):
#    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)