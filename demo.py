"""
demo.py
Spring 2023 PJW

Demonstrate an inner join and a few other features of Pandas.
"""

import pandas as pd

#
#  Read the files of state names and populations. Read all variables as
#  strings to avoid clobbering FIPS codes, and then convert the population
#  to a float. Also set up the name of the output file.
#

name_data = pd.read_csv('state_name.csv',dtype=str)

pop_data = pd.read_csv('state_pop.csv',dtype=str)
pop_data['pop'] = pop_data['pop'].astype(float)

outfile = 'demo-merged.csv'

#%%
#
#  Do an inner join of the population data onto the name data. Will keep only
#  the rows for states and DC since the population file doesn't have populations
#  for Census regions. Also drops Puerto Rico, which is in the population data
#  but isn't in the state name file.
#

merged = name_data.merge(pop_data,left_on="State",right_on="STATEFP",how='inner')

#%%
#
#  Set the index to the state's Division. The index in Pandas doesn't need
#  to be unique except in certain circumstances.
#

indexed = merged.set_index('Division')

#  Use the .head() method to print out the first few rows

print( '\n', indexed.head() )

#  Use the .loc[] operation to print out the data for Division 8

print( '\n', indexed.loc["8"] )

#%%
#
#  Aggregate the population by Census division
#

group_by_div = indexed.groupby('Division')
div_pop = group_by_div['pop'].sum()

print(div_pop)

#%%
#
#  Compute each state's percentage of its division population. Pandas
#  automatically lines up the data by Division using the indexes of
#  merged and div_pop.
#

indexed['percent'] = 100*indexed['pop']/div_pop

#%%
#
#  Do a spot check on division 3
#

div3 = indexed.loc["3"]
print( div3 )
print( '\nCheck:', div3['percent'].sum() )

#%%
#
#  Print out the 4 states that have the smallest population shares of their
#  divisions.
#

sort_percent = indexed.sort_values("percent")
small4 = sort_percent[:4]
print( small4 )

#%%
#
#  Sort the output file by STATEFP and then write it out
#

indexed = indexed.sort_values('STATEFP')
indexed.to_csv(outfile)
