# necessary imports
import pandas as pd

# read as many previously scraped csv's as needed
df = pd.read_csv('csv') # df needs to be the original master dataframe that you are adding to
df2 = pd.read_csv('csv')
df3 = pd.read_csv('csv')
df4 = pd.read_csv('csv')

# sepcify the market for each df - these are examples, will change with new data
df2['MARKET (agency/dept/client)'] = 'USAF'
df3['MARKET (agency/dept/client)'] = 'ARMY'
df4['MARKET (agency/dept/client)'] = 'NAVY'

# split first and last name for all df
df2[['First Name', 'Last Name']] = df2['Name'].str.split(' ', expand=True, n=1)
df2.drop('Name', axis=1, inplace=True)
df2['Last Name'] = df2['Last Name'].str.split(',').str[0]
df2['Last Name'] = df2['Last Name'].str.split(' ').str[0]

df3[['First Name', 'Last Name']] = df3['Name'].str.split(' ', expand=True, n=1)
df3.drop('Name', axis=1, inplace=True)
df3['Last Name'] = df3['Last Name'].str.split(',').str[0]
df3['Last Name'] = df3['Last Name'].str.split(' ').str[0]

df4[['First Name', 'Last Name']] = df4['Name'].str.split(' ', expand=True, n=1)
df4.drop('Name', axis=1, inplace=True)
df4['Last Name'] = df4['Last Name'].str.split(',').str[0]
df4['Last Name'] = df4['Last Name'].str.split(' ').str[0]

# merge into one, drop duplicates, and sort 
df_new = pd.concat([df, df2, df3, df4]).drop_duplicates(['First Name','Last Name', 'Experience', 'Description/Bio'],keep='last').sort_values('First Name')
df_new = pd.concat([df, df2, df3, df4]).sort_values('First Name')

# save to temporary csv, later must convert to .xlsx
df_new.to_csv('temp_master.csv')
