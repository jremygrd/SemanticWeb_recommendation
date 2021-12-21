import pandas as pd
import numpy as np

#Code to create the correlation matrix

df = pd.read_csv(r'steam-200k.csv',header=None,names=['userId','game','purchaseOrPlay','hoursPlayed','rating'])

#Remove the lines with the purchase attribute (because we don't care about it)
df = df.drop(df.loc[df['purchaseOrPlay']=="purchase"].index)
df = df.drop(columns=['purchaseOrPlay'])

#This is purely experimental, but we need to give a rating to each game. We can think of doing it another way
#For example for each user, mapping a rate between 1 and 5 depending on how long he spent on the games he played could be a solution
df.loc[(df['hoursPlayed']>50),'rating'] = 5
df.loc[(df['hoursPlayed']>10) & (df['hoursPlayed']<=50),'rating'] = 4
df.loc[(df['hoursPlayed']>5) & (df['hoursPlayed']<=10),'rating'] = 3
df.loc[(df['hoursPlayed']>1) & (df['hoursPlayed']<=5),'rating'] = 2
df.loc[(df['hoursPlayed']<=1),'rating'] = 1

#Create the pivot table
#Now the games are columns. Which is why we will see a lot of NaN values. Because users didn't rate all the 3600 games.
userRatings = df.pivot_table(index=['userId'],columns=['game'],values='rating')

#correlation matrix, needed to find the related games
#takes a while to compute so we will need to save it into a pickle file and load it
corrMatrix = userRatings.corr(method='pearson', min_periods=20)
corrMatrix.head()

# compression_opts = dict(method='zip', archive_name='outCorr.csv')  
# corrMatrix.to_csv('out.zip', index=True, compression=compression_opts)  

corrMatrix.to_pickle("./corrMatrix.pkl")