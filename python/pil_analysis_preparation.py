# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 17:51:42 2024

@author: edobo
"""

import PyPDF2
import pandas as pd
import numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import math
import sys
import json
sys.path.append(r"C:\Users\edobo\OneDrive\Desktop\Python\modules")
from data_structures import list_to_dict
from data_structures import merge_dict
from statistical_calculations import frequencies
from text_analysis import find_similarity
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import random
from text_analysis import find_similarity, compare_dict
from plotly.subplots import make_subplots

#parth
path = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\duration\guilds_number2_region.xlsx"
path_pil = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_veneto.xlsx"
path_toscana = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_toscana.xlsx"
path_emilia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_emilia.xlsx"
path_lazio = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_lazio.xlsx"
path_liguria = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_liguria.xlsx"
path_lombardia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_lombardia.xlsx"
pil_piemonte = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_piemonte.xlsx"
pil_campania = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_campania.xlsx"
pil_sicilia = r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\RAW_db\PIL\pil_sicilia.xlsx"

#regions
merged = pd.read_excel(path)
pil_veneto = pd.read_excel(path_pil)
pil_toscana = pd.read_excel(path_toscana)
pil_emilia = pd.read_excel(path_emilia)
pil_lazio = pd.read_excel(path_lazio)
pil_liguria = pd.read_excel(path_liguria)
pil_lombardia = pd.read_excel(path_lombardia)
pil_piemonte = pd.read_excel(pil_piemonte)
pil_campania = pd.read_excel(pil_campania)
pil_sicilia = pd.read_excel(pil_sicilia)

def approximate(year):
    return round(year/25) * 25

def closest_year_value(group):
    closest_year = group['year'].sub(group.name - 1).abs().idxmin()
    return group.loc[closest_year, 'GDP']

def rolling_window_average(pil_region):
    pil_region.set_index('year', inplace=True)
    
    # Calculate rolling window average (window size: 11 years - 5 years before, the year itself, 5 years after)
    pil_region['rolling_avg_GDP'] = pil_region['GDP'].rolling(window=5, min_periods=1, center=True).mean()
    pil_region.reset_index(inplace=True)
    return pil_region


def data_extraction(dataset,  pil_region,regione = None,):
    veneto = merged[merged.region == regione]
    veneto = veneto[['group', 'region_new_guilds', 'guilds_nr_region', 'region_perc_new']]
    veneto = veneto[veneto['group'] < 1800]
    veneto = veneto.groupby('group').agg({'region_new_guilds' : 'mean', 'guilds_nr_region' : 'max', 
                                          'region_perc_new' : 'min'})
    
    pil_region = rolling_window_average(pil_region)
    return veneto, pil_region




veneto, pil_veneto = data_extraction(merged, pil_veneto, 'Veneto')
emilia, pil_emilia= data_extraction(merged,pil_emilia, 'Emilia-Romagna')
toscana, pil_toscana = data_extraction(merged,pil_toscana, 'Toscana')
lazio, pil_lazio = data_extraction(merged,pil_lazio,  'Lazio')
liguria, pil_liguria = data_extraction(merged, pil_liguria, 'Liguria')
lombardia, pil_lombardia = data_extraction(merged, pil_lombardia, 'Lombardia')
piemonte, pil_piemonte = data_extraction(merged, pil_piemonte, 'Piemonte')
campania, pil_campania = data_extraction(merged, pil_campania, 'Campania')
sicilia, pil_sicilia = data_extraction(merged, pil_sicilia, 'Sicilia')

pil_toscana['compunded'] = (pil_toscana['rolling_avg_GDP'] / pil_toscana['rolling_avg_GDP'].shift(25))**(1/25) - 1
pil_veneto['compunded'] = (pil_veneto['rolling_avg_GDP'] / pil_veneto['rolling_avg_GDP'].shift(25))**(1/25) - 1

def merging_function(region, pil):
    region = region.reset_index()
    all_years = pd.DataFrame({'group': range(1000, 1901, 10)})
    merged_df = pd.merge(all_years,region, on='group', how='left')
    #merged_df['region_new_guilds'] = merged_df['region_new_guilds'].fillna(0)
    merging = pd.merge(merged_df, pil, left_on = 'group', right_on = 'year', how = 'inner')
    merging = pd.merge(merged_df, merging, on = ['group', 'region_new_guilds', 'guilds_nr_region',
                                                              'region_perc_new'], how = 'outer')
    
    merging['agg_change'] = merging['rolling_avg_GDP'].pct_change()*100
    merging['log_return'] = np.log(merging['rolling_avg_GDP'] / merging['rolling_avg_GDP'].shift(1)) * 100
    merging['SMA'] = merging['agg_change'].rolling(window=3).mean()
    merging = merging.drop(merging.index[0])
    merging = merging[merging['group'] <= 1800]
    return merging

def merging_graph(region,pil):
    region = region.reset_index()
    merging = pd.merge(region, pil, left_on = 'group', right_on = 'year', how = 'left')
    merging['agg_change'] = merging['rolling_avg_GDP'].pct_change()*100
    merging = merging[merging['group']<= 1800]
    merging = merging[merging['group'] >= 1300]
    return merging

merging_veneto = merging_function(veneto, pil_veneto)
merging_toscana = merging_function(toscana, pil_toscana)
merging_lazio = merging_function(lazio, pil_lazio)
merging_liguria = merging_function(liguria, pil_liguria)
merging_lombardia = merging_function(lombardia, pil_lombardia)
merging_piemonte = merging_function(piemonte, pil_piemonte)
merging_campania = merging_function(campania, pil_campania)
merging_emilia = merging_function(emilia, pil_emilia)
merging_sicilia = merging_function(sicilia, pil_sicilia)


# Calculate the logarithmic return

merging_veneto['region'] = 'VENETO'
merging_toscana['region'] = 'TOSCANA'
merging_emilia['region'] = 'EMILIA'
merging_lazio['region'] = 'LAZIO'
merging_liguria['region'] = 'LIGURIA'
merging_lombardia['region'] = 'LOMBARDIA'
merging_piemonte['region'] = 'PIEMONTE'
merging_campania['region'] = 'CAMPANIA'

#add all to a list
merged_df = [merging_veneto, merging_toscana, merging_lazio, merging_liguria, merging_lombardia, merging_piemonte, merging_campania, merging_emilia,
                merging_sicilia]
             

#calculate correlation
correlation_toscana = merging_toscana[['region_new_guilds', 'agg_change']].corr()
correlation = merging_veneto[['region_new_guilds', 'agg_change']].corr()
correlation_emilia =  merging_emilia[['region_new_guilds', 'agg_change']].corr()
correlation_lazio =  merging_lazio[['region_new_guilds', 'agg_change']].corr()
correlation_liguria =  merging_liguria[['region_new_guilds', 'agg_change']].corr()
correlation_lombardia = merging_lombardia[['region_new_guilds', 'agg_change']].corr()
correlation_piemonte = merging_piemonte[['region_new_guilds', 'agg_change']].corr()
correlation_campania = merging_campania[['region_new_guilds', 'agg_change']].corr()
correlation_sicilia = merging_sicilia[['region_new_guilds', 'agg_change']].corr()

#perc correlation
correlation_perc_veneto = merging_veneto[['region_perc_new', 'agg_change']].corr()

graph_veneto = merging_graph(veneto, pil_veneto)
graph_toscana = merging_graph(toscana, pil_toscana)
graph_emilia = merging_graph(emilia, pil_emilia)
graph_lazio = merging_graph(lazio, pil_lazio)
graph_liguria = merging_graph(liguria, pil_liguria)
graph_lombardia = merging_graph(lombardia, pil_lombardia)
graph_piemonte = merging_graph(piemonte, pil_piemonte)
graph_campania = merging_graph(campania, pil_campania)
graph_sicilia = merging_graph(sicilia, pil_sicilia)

#add region column
graph_veneto['region'] = 'VENETO'
graph_toscana['region'] = 'TOSCANA'
graph_emilia['region'] = 'EMILIA'
graph_lazio['region'] = 'LAZIO'
graph_liguria['region'] = 'LIGURIA'
graph_lombardia['region'] = 'LOMBARDIA'
graph_piemonte['region'] = 'PIEMONTE'
graph_campania['region'] = 'CAMPANIA'
graph_sicilia['region'] = 'SICILIA'


#add all to a list
graph_df = [graph_veneto, graph_toscana, graph_lazio, graph_liguria, graph_lombardia, graph_piemonte, graph_campania, graph_sicilia]
def graph_creation(dataset, region):
    fig1 = go.Figure()
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(
        x = list(dataset['group']),
        y = list(dataset['agg_change']),
        line_color='orange',
        name = 'GDPgrowth'),
        secondary_y = False,
        )
    fig1.add_trace(go.Scatter(
        x = list(dataset['group']),
        y = list(dataset['region_new_guilds']),
        line_color='blue',
        name = 'net new guilds'),
        secondary_y = True
        )   
    
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        title={
        'text': "GDP growth and guilds creation in Veneto, 1300-1800",  # Set the title text here
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },
        xaxis = dict(
            showgrid = False,
            title = 'year',
            tickmode = 'linear',
            tick0 = 1300,
            dtick = 25
        ),
        yaxis = dict(
            range = (-10, 10),
            title = 'GDPgrwoth(% change)',
            showgrid = False,
            zeroline = True,
            zerolinecolor = 'grey',
            gridcolor = 'grey',
            griddash = 'dash'
        ),
        yaxis2 = dict(
            showgrid = False,
            title = 'guilds number',
            range= (-60, 60),
            zeroline = True,
            zerolinecolor = 'grey',
            gridcolor = 'grey',
            griddash = 'dash'
        ),
    )
    
    fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\pil_'+ region + '.html')

for region in graph_df:
    graph_creation(region, region['region'].iloc[0])   

subplots = ['Veneto', 'Campania', 'Lazio', 'Toscana', 'Emilia', 'Liguria', 'Lombardia', 'Piemonte', 'Sicilia']
fig1 = make_subplots(rows=3, cols=3,
                    specs=[[{"secondary_y": True}, {"secondary_y": True},{"secondary_y": True} ],
                           [{"secondary_y": True}, {"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}, {"secondary_y": True}]],
                    subplot_titles= subplots)


fig1.add_trace(
    go.Scatter(x=graph_veneto['group'], y=graph_veneto['agg_change'], line_color = 'orange'),
    row=1, col=1, secondary_y=False)

fig1.add_trace(
    go.Scatter(x=graph_veneto['group'], y=graph_veneto['region_new_guilds'], line_color = 'blue'),
    row=1, col=1, secondary_y=True)

fig1.add_trace(
    go.Scatter(x=graph_campania['group'], y = graph_campania['agg_change'], line_color = 'orange'),
    row=1, col=2, secondary_y=False)

fig1.add_trace(
    go.Scatter(x=graph_campania['group'], y = graph_campania['region_new_guilds'], line_color = 'blue'),
    row=1, col=2, secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=graph_lazio['group'], y = graph_lazio['agg_change'], line_color = 'orange'),
    row=1, col=3, secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=graph_lazio['group'], y = graph_lazio['region_new_guilds'], line_color = 'blue'),
    row=1, col=3, secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=graph_toscana['group'], y = graph_toscana['agg_change'], line_color = 'orange'),
    row=2, col=1, secondary_y=False,
)   

fig1.add_trace(
    go.Scatter(x=graph_toscana['group'], y = graph_toscana['region_new_guilds'], line_color = 'blue'),
    row=2, col=1, secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=graph_emilia['group'], y = graph_emilia['agg_change'], line_color = 'orange'),
    row=2, col=2, secondary_y=False,    
)

fig1.add_trace(
    go.Scatter(x=graph_emilia['group'], y = graph_emilia['region_new_guilds'], line_color = 'blue'),
    row=2, col=2, secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=graph_liguria['group'], y = graph_liguria['agg_change'], line_color = 'orange'),
    row=2, col=3, secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=graph_liguria['group'], y = graph_liguria['region_new_guilds'], line_color = 'blue'),
    row=2, col=3, secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=graph_lombardia['group'], y = graph_lombardia['agg_change'], line_color = 'orange'),
    row=3, col=1, secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=graph_lombardia['group'], y = graph_lombardia['region_new_guilds'], line_color = 'blue'),
    row=3, col=1, secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=graph_piemonte['group'], y = graph_piemonte['agg_change'], line_color = 'blue', name="yaxis15 data"),
    row=3, col=2, secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=graph_piemonte['group'], y = graph_piemonte['region_new_guilds'], line_color = 'orange'),
    row=3, col=2, secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=graph_sicilia['group'], y = graph_sicilia['agg_change'], line_color = 'blue', name="yaxis17 data"),
    row=3, col=3, secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=graph_sicilia['group'], y = graph_sicilia['region_new_guilds'], line_color = 'orange'),
    row=3, col=3, secondary_y=True,
)



fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis1 = dict(
        showgrid = True,
    ),
    yaxis1 = dict(
        range = [-10, +10],
        showgrid = False,
        zeroline = False,
        zerolinecolor = 'grey',
        gridcolor = 'grey',
        griddash = 'dash'
    ),
    yaxis2 = dict(
        showgrid = False,
        #range= [0, 150],
        zeroline = False,
        zerolinecolor = 'grey',
        gridcolor = 'grey',
        griddash = 'dash'
    ),
)


for i in range(1, 10):
    fig1.update_xaxes(
        title_text= 'year',
        row=(i-1)//3 + 1, col=(i-1)%3 + 1
    )
    fig1.update_yaxes(
        title_text='GDP growth(% values)',
        row=(i-1)//3 + 1, col=(i-1)%3 + 1
    )


fig1.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\pil_bho.html')



# Export to an HTML file
#fig.write_html(r'C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\some_graph_attempts\pil_all_region.html')

total = pd.concat([merging_veneto, merging_toscana, merging_emilia, merging_campania, merging_liguria,
                   merging_lombardia, merging_piemonte, merging_sicilia, merging_lazio])
#total_correlation = total[['guilds_nr_region', 'GDP']].corr()

merging_veneto.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_veneto.xlsx")
merging_toscana.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_toscana.xlsx")
merging_emilia.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_emilia.xlsx")
total.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_total.xlsx")
merging_lazio.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_lazio.xlsx")
merging_liguria.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_liguria.xlsx")
merging_lombardia.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_lombardia.xlsx")
merging_piemonte.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_piemonte.xlsx")
merging_campania.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_campania.xlsx")
merging_sicilia.to_excel(r"C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_sicilia.xlsx")
