import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import xlrd
import plotly.express as px
app = dash.Dash(__name__)

server = app.server

excel = 'https://raw.githubusercontent.com/hludgate/cs6440-unit2project/master/plotly.csv'
state_code = 'https://raw.githubusercontent.com/hludgate/cs6440-unit2project/master/state_codes.csv'
dt = pd.read_csv(state_code)
dt = dt.set_index('State').T.to_dict('list')
df = pd.read_csv(excel)

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
                                       'Heart Failure','Cancer','COPD','Diabetes','Ischemic Heart Disease','Arthritis','Stroke','Most Common Illness'])
chronics = ['Alzheimers','Osteoporosis','Chronic Kidney Disease',
                                       'Heart Failure','Cancer','COPD','Diabetes','Ischemic Heart Disease','Arthritis','Stroke']
i = 0
for state in dt:
    df_state = df[df['SP_STATE_CODE']==dt[state][0]]
    df_state['chronic_sum'] = df_state['SP_ALZHDMTA'] + df_state['SP_OSTEOPRS'] + df_state['SP_CHRNKIDN'] +df_state['SP_CHF'] + \
    df_state['SP_CNCR'] + df_state['SP_COPD'] + df_state['SP_DIABETES']+ df_state['SP_ISCHMCHT']+ df_state['SP_RA_OA'] + \
    df_state['SP_STRKETIA']
    chronic_tots = [df_state['SP_ALZHDMTA'].sum(),df_state['SP_OSTEOPRS'].sum(),df_state['SP_CHRNKIDN'].sum(),
                       df_state['SP_CHF'].sum(),df_state['SP_CNCR'].sum(),df_state['SP_COPD'].sum(), df_state['SP_DIABETES'].sum(),
                       df_state['SP_ISCHMCHT'].sum(),df_state['SP_RA_OA'].sum(),df_state['SP_STRKETIA'].sum()]
    
    df_states_info.loc[i]=[state,df_state['chronic_sum'].mean(),df_state['SP_ALZHDMTA'].sum(),df_state['SP_OSTEOPRS'].sum(),df_state['SP_CHRNKIDN'].sum(),
                       df_state['SP_CHF'].sum(),df_state['SP_CNCR'].sum(),df_state['SP_COPD'].sum(), df_state['SP_DIABETES'].sum(),
                       df_state['SP_ISCHMCHT'].sum(),df_state['SP_RA_OA'].sum(),df_state['SP_STRKETIA'].sum(),chronics[chronic_tots.index(max(chronic_tots))]]
    i += 1
df_sex = []
df_sex_info = pd.DataFrame(columns=['Sex','Average_Chronic','Alzheimers','Osteoporosis','Chronic Kidney Disease',
                                       'Heart Failure','Cancer','COPD','Diabetes','Ischemic Heart Disease','Arthritis','Stroke'])
chronics = ['Alzheimers','Osteoporosis','Chronic Kidney Disease',
                                       'Heart Failure','Cancer','COPD','Diabetes','Ischemic Heart Disease','Arthritis','Stroke']
sex = ['Male','Female']
sex_totals = []
for i in range(2):
    df_sex = df[df['BENE_SEX_IDENT_CD']==i+1]
    num = len(df_sex.index)
    df_sex['chronic_sum'] = df_sex['SP_ALZHDMTA'] + df_sex['SP_OSTEOPRS'] + df_sex['SP_CHRNKIDN'] +df_sex['SP_CHF'] + \
    df_sex['SP_CNCR'] + df_sex['SP_COPD'] + df_sex['SP_DIABETES']+ df_sex['SP_ISCHMCHT']+ df_sex['SP_RA_OA'] + \
    df_sex['SP_STRKETIA']
    df_sex_info.loc[i]=[i,df_sex['chronic_sum'].mean(),df_sex['SP_ALZHDMTA'].sum(),df_sex['SP_OSTEOPRS'].sum(),df_sex['SP_CHRNKIDN'].sum(),
                       df_sex['SP_CHF'].sum(),df_sex['SP_CNCR'].sum(),df_sex['SP_COPD'].sum(), df_sex['SP_DIABETES'].sum(),
                       df_sex['SP_ISCHMCHT'].sum(),df_sex['SP_RA_OA'].sum(),df_sex['SP_STRKETIA'].sum()]
    temp_tots = [df_sex['SP_ALZHDMTA'].sum()/num,df_sex['SP_OSTEOPRS'].sum()/num,df_sex['SP_CHRNKIDN'].sum()/num,
                   df_sex['SP_CHF'].sum()/num,df_sex['SP_CNCR'].sum()/num,df_sex['SP_COPD'].sum()/num, df_sex['SP_DIABETES'].sum()/num,
                   df_sex['SP_ISCHMCHT'].sum()/num,df_sex['SP_RA_OA'].sum()/num,df_sex['SP_STRKETIA'].sum()/num]
    sex_totals.append(temp_tots)
    
df_eth = []
df_eth_info = pd.DataFrame(columns=['Ethnicity','Average_Chronic','Alzheimers','Osteoporosis','Chronic Kidney Disease',
                                       'Heart Failure','Cancer','COPD','Diabetes','Ischemic Heart Disease','Arthritis','Stroke'])
chronics = ['Alzheimers','Osteoporosis','Chronic Kidney Disease',
                                       'Heart Failure','Cancer','COPD','Diabetes','Ischemic Heart Disease','Arthritis','Stroke']
ethns = ['White','Black','Other','NA','Hispanic']
eth_totals = []
for i in range(5):
    df_eth = df[df['BENE_RACE_CD']==i+1]
    num = len(df_eth.index)
    df_eth['chronic_sum'] = df_eth['SP_ALZHDMTA'] + df_eth['SP_OSTEOPRS'] + df_eth['SP_CHRNKIDN'] +df_eth['SP_CHF'] + \
    df_eth['SP_CNCR'] + df_eth['SP_COPD'] + df_eth['SP_DIABETES']+ df_eth['SP_ISCHMCHT']+ df_eth['SP_RA_OA'] + \
    df_eth['SP_STRKETIA']
    df_eth_info.loc[i]=[i,df_eth['chronic_sum'].mean(),df_eth['SP_ALZHDMTA'].sum(),df_eth['SP_OSTEOPRS'].sum(),df_eth['SP_CHRNKIDN'].sum(),
                       df_eth['SP_CHF'].sum(),df_eth['SP_CNCR'].sum(),df_eth['SP_COPD'].sum(), df_eth['SP_DIABETES'].sum(),
                       df_eth['SP_ISCHMCHT'].sum(),df_eth['SP_RA_OA'].sum(),df_eth['SP_STRKETIA'].sum()]
    temp_tots = [df_eth['SP_ALZHDMTA'].sum()/num,df_eth['SP_OSTEOPRS'].sum()/num,df_eth['SP_CHRNKIDN'].sum()/num,
                       df_eth['SP_CHF'].sum()/num,df_eth['SP_CNCR'].sum()/num,df_eth['SP_COPD'].sum()/num, df_eth['SP_DIABETES'].sum()/num,
                       df_eth['SP_ISCHMCHT'].sum()/num,df_eth['SP_RA_OA'].sum()/num,df_eth['SP_STRKETIA'].sum()/num]
    eth_totals.append(temp_tots)   
    
df_states_info['text'] = df_states_info['State'] + '<br>' + \
    'Most Common Illness ' + df_states_info['Most Common Illness'] 
fig = go.Figure(data=go.Choropleth(
    locations=df_states_info['State'], # Spatial coordinates
    z = df_states_info['Average_Chronic'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    text=df_states_info['text'], # hover text
    colorbar_title = "Average Chronic Illnesses",
))

fig.update_layout(
    title_text = '2008 US Average # of Chronic Illnesses of patients with Depression',
    geo_scope='usa', # limite map scope to USA
)
    
fig2 = go.Figure(data=[
    go.Bar(name=ethns[0], x=chronics, y=eth_totals[0]),
    go.Bar(name=ethns[1], x=chronics, y=eth_totals[1]),
    go.Bar(name=ethns[2], x=chronics, y=eth_totals[2]),
    go.Bar(name=ethns[4], x=chronics, y=eth_totals[4])    
])
# Change the bar mode
fig2.update_layout(barmode='group')
fig3 = go.Figure(data=[
    go.Bar(name=sex[0], x=chronics, y=sex_totals[0]),
    go.Bar(name=sex[1], x=chronics, y=sex_totals[1])   
])
# Change the bar mode
fig3.update_layout(barmode='group')
app.layout = html.Div([
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3)
])

#@app.callback(dash.dependencies.Output('display-value', 'children'),
#              [dash.dependencies.Input('dropdown', 'value')])
#def display_value(value):
#    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)