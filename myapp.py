#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:45:37 2020

@author: alexbaverstock
"""
import streamlit

import pandas as pd
#df = pd.read_csv('/content/SundfixturelistA.csv')
#dffix = pd.read_csv('/content/Sundstats3.csv')

df = pd.read_csv('https://raw.githubusercontent.com/alex85301/safcdata/master/SundfixturelistA.csv')
dffix = pd.read_csv('https://raw.githubusercontent.com/alex85301/safcdata/master/Sundstats3.csv')
dfcat = pd.read_csv('https://raw.githubusercontent.com/alex85301/safcdata/master/PlayerCatStats.csv')

#Idea is that dfcat can be added to with player specific categorical data, dffix = fixture specifc caterical data

#Merge Data sheets
dfB = pd.merge(df,dffix, how='right', on=['event_id'])

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 40)
pd.set_option('display.max_rows', 50)

#Merge, column renames etc..
dfB.drop('Opponent_y',axis=1, inplace=True)
dfB.drop(['player_name_x','Unnamed: 0'],axis=1, inplace=True)
dfB.rename(columns= {'player_name_y':'player_name'}, inplace=True)
dfB.rename(columns={'Opponent_x':'Opponent'}, inplace=True)
dfB['Game'] = dfB["Opponent"]  + (' ') + dfB["Date"]
dfB['player_name'] = dfB['player_name'].replace(to_replace ='Alim √ñzt√ºrk', value ='Alim Öztürk')

#NEW Seaborn plotting attempts

#add split=True to split Managers

dfB1 = dfB[['Manager','minutes_played', 'shotstotal', 'shotson', 'gconceded',
       'gassists', 'gtotal', 'ptotal', 'pkey', 'paccuracy', 'ttotal']]

M3 = (dfB.groupby(by='Manager')[['rating','shotstotal', 'shotson', 'offsides', 'gconceded',
       'gassists', 'gtotal', 'pkey', 'ttotal',
       'tblocks', 'tinterc', 'dtotal', 'dwon', 'dattempts', 'dsuccess',
       'dpast', 'fdrawn', 'fcommit', 'red', 'yellow', 'penaltysuccess']].aggregate('mean'))
M3 = M3.reset_index()

#dfB2 = M2[['Manager', 'shotstotal', 'shotson', 'gconceded',
       #'gassists', 'gtotal', 'pkey', 'ttotal']]
#print(dfB1.head(20))

melted_df = pd.melt(dfB1, 
                    id_vars=["Manager"], # Variables to keep
                    var_name="Stat") # Name of melted variable

melted_df1 = pd.melt(M3, 
                    id_vars=["Manager"], # Variables to keep
                    var_name="Stat") # Name of melted variable

#print(melted_df)

#print(melted_df.head())
#melted_df["value"] = melted_df.value.astype(np.object)
plt.figure(figsize=(15,10))
sns.swarmplot(x='Stat', y='value',data=melted_df, hue='Manager',split=True)
plt.show()

plt.figure(figsize=(15,10))
A = sns.barplot(x="Stat", y="value", hue="Manager", data=melted_df1)
plt.setp(A.get_xticklabels(), rotation=90)
plt.show()
