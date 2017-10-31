
# coding: utf-8

# ## Module 4
# 
# This week we will be looking at Enterococcus levels in the Hudson River, using data from the
# organization Riverkeeper ( http://www.riverkeeper.org/).
# 
# Background: Enterococcus is a fecal indicating bacteria that lives in the intestines of humans
# and other warm-blooded animals. Enterococcus (“ Entero”) counts are useful as a water
# quality indicator due to their abundance in human sewage, correlation with many human
# pathogens and low abundance in sewage free environments. The United States
# Environmental Protection Agency (EPA) reports Entero counts as colonies (or cells) per 100
# ml of water.
# 
# Riverkeeper has based its assessment of acceptable water quality on the 2012 Federal
# Recreational Water Quality Criteria from the US EPA. Unacceptable water is based on an
# illness rate of 32 per 1000 swimmers.
# 
# The federal standard for unacceptable water quality is a single sample value of greater than
# 110 Enterococcus/100 mL, or five or more samples with a geometric mean (a weighted
# average) greater than 30 Enterococcus/100 mL.
# 
# Data: I have provided the data on our github page, in the folder
# https://github.com/charleyferrari/CUNY_DATA608/tree/master/lecture4/Data. I have not
# cleaned it – you need to do so.
# 
# This assignment must be done in python. It must be done using the ‘bokeh’, 'seaborn', or
# 'pandas' package. You may turn in either a . py file or an ipython notebook file.
# 
# Questions:
# - Create lists & graphs of the best and worst places to swim in the dataset.
# - The testing of water quality can be sporadic. Which sites have been tested most regularly?
# Which ones have long gaps between tests? Pick out 5-10 sites and visually compare how
# regularly their water quality is tested.
# - Is there a relationship between the amount of rain and water quality? Show this
# relationship graphically. If you can, estimate the effect of rain on quality at different sites and
# create a visualization to compare them.

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
print (__version__)
init_notebook_mode(connected=True)

import cufflinks as cf

import seaborn as sns


# In[2]:

from ipywidgets import interact


# In[3]:

hudson = pd.read_csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture4/Data/riverkeeper_data_2013.csv")


# In[4]:

hudson.head(20)


# In[5]:

hudson.describe(include = 'all')


# In[6]:

hudson = hudson.dropna(axis=0)


# In[7]:

hudson['Date'] = pd.to_datetime(hudson['Date'])


# In[8]:

import string 
hudson['stange']=hudson['EnteroCount'].str.contains('[{}]'.format(string.punctuation)).astype(int)


# In[9]:

stange=hudson.loc[hudson['stange']==1,]
stange['EnteroCount'].unique()


# In[10]:

hudson['EnteroCount']=hudson['EnteroCount'].str.replace('[{}]'.format(string.punctuation), '')


# In[11]:

hudson['EnteroCount']=pd.to_numeric(hudson['EnteroCount'])


# ### 1. Create lists & graphs of the best and worst places to swim in the dataset.

# Check whehter there are sites have less than 5 samples

# In[12]:

c = hudson.groupby(['Site'])['Site'].count()
c=c.to_frame()
c.columns=['samples']
c[c.samples < 5].index.values


# All sites have more than 5 samples. Go ahead to calculate geometric mean of enteroccocus count. 

# In[13]:

from scipy.stats.mstats import gmean


# In[14]:

hudson['geomean']=hudson.groupby('Site').EnteroCount.apply(gmean,axis=0)
hudson['geomean'].unique()


# Geometric mean returned null so there must be 0 or null in the dataset.
# Then I will check if there is missing data or o in EnteroCount

# In[15]:

hudson['EnteroCount'].isnull().values.any()


# In[16]:

any(n == 0 for n in hudson['EnteroCount'])


# In[17]:

hudson.loc[hudson['EnteroCount']==0,'EnteroCount']


# There is only one 0 record. So I remove row 522 in order to calculate geometric mean for EnteroCount. 
# 

# In[18]:

hudson.drop(hudson.index[[522]],inplace=True)


# In[19]:

any(n == 0 for n in hudson['EnteroCount'])


# In[20]:

hudson['EnteroCount'].isnull().values.any()


# In[21]:

a=hudson.groupby(['Site'])['EnteroCount'].apply(gmean,axis=0)
a.to_dict() 
hudson['geomean'] = hudson['Site'].map(a)


# **Find the sites where a single sample value of greater than 110 Enterococcus/100 mL**

# In[22]:

single = hudson.loc[hudson.EnteroCount >=110,'Site'].unique()
len(single)
single


# **Find the sites where five or more samples with a geometric mean (a weighted average) greater than 30 Enterococcus/100 mL.**

# In[23]:

many =  hudson.loc[hudson.geomean >=30,'Site'].unique()
len(many)
many


# In[24]:

len(hudson.Site.unique())


# **So we know that 98% of the sites have unacceptable water quality for swimming.**

# In[25]:

hudson['swim'] = np.where(((hudson['Site'].isin(single)) |(hudson['Site'].isin(many))), 'unacceptable', 'acceptable')


# In[26]:

hudson['swim_num']=np.where((hudson['swim']=='acceptable'),1,-1)


# In[27]:

hudson['ecount'] = hudson['swim_num']*hudson['EnteroCount']
q1 = hudson.loc[:,('Site','geomean','swim','swim_num')]
q1 = q1.drop_duplicates()


# **Plot the site with either good or bad water qualities in bar chart.**

# In[28]:

y = q1['swim_num'] 
x = q1['Site']
x_pos = [i for i, _ in enumerate(x)] 
plt.barh(x_pos, y, color='green')
plt.yticks(x_pos, x)
plt.title('The sites for swim')
 
plt.show()


# There are too many sites so the name could not be seen clearly. font size should be adjusted.

# In[29]:

import plotly.plotly as py
import cufflinks as cf

cf.go_offline()


# **Find the sites with the highest geomean in unacceptable group and lowest geomean in accetable group**

# In[30]:

high = q1.loc[q1.swim == 'unacceptable','geomean'].max()
low = q1.loc[q1.swim == 'acceptable','geomean'].min()


# In[31]:

q1.loc[q1.geomean == low,'swim']='acceptable/best'
q1.loc[q1.geomean == high,'swim']='unacceptable/worst'


# In[32]:

q1.loc[q1.geomean == high,'swim']


# **Plot the geomean vs sites in bubble chart.**

# In[33]:

q1.iplot(kind='bubble', x='Site', y='geomean', size='geomean', text='Site',categories='swim',
             xTitle='hudson river site', yTitle='Enteroccocus Count',
             filename='cufflinks/q1-bubble-chart',logy=True)


# **Conclusion:**
#     
#     There are two sites in Hudson river where the water quality is acceptable for swimming: Poughkeepsie Drinking Water Intake and Poughkeepsie Launch Ramp and the former is the best site which has very low Enteroccocus count. About 98% of the sites along Hudson river is not appropreate for swimming and the worst site is Upper Sparkill Creek.

# #### 2: The testing of water quality can be sporadic. Which sites have been tested most regularly? Which ones have long gaps between tests? Pick out 5-10 sites and visually compare how regularly their water quality is tested.

# change the formate of date and time

# In[34]:

hudson['Date'] = pd.to_datetime(hudson['Date'])


# In[35]:

demin = lambda df: df - df.min()
gap = hudson.groupby(['Site'])['Date'].transform(demin)
hudson['gap'] = gap
hudson['gap_num'] = hudson['gap'] / np.timedelta64(1, 'D') # extract the integer value of days by divide it with a timedelta of one day


# In[36]:

hudson.head(3)


# In[37]:

hudson.sort_values(['Site','gap_num'],ascending=True)


# In[39]:

grp = hudson.sort_values(['Site','gap_num'],ascending=True).groupby(['Site'])
g = grp.apply(lambda g: g['gap_num'].diff().replace(np.nan,0))
tm = pd.DataFrame(g)
tm=tm.reset_index()
tm.set_index('level_1',inplace=True)


# In[46]:

hudson['day_diff']=tm.gap_num
hudson.head(3)


# **View the distribution of gap between tests for each site**

# In[47]:

g = sns.FacetGrid(hudson, col="Site", col_wrap=5, size=3)
g = g.map(sns.swarmplot,"day_diff", "Site", data=hudson)


# **Find the average gap between tests **

# In[48]:

hudson['ave_diff'] = hudson.groupby(['Site'])['day_diff'].transform(np.mean)
hudson.head(3)


# In[49]:

test_freq = hudson.loc[:,['Site','swim','ave_diff']].drop_duplicates()
test_freq


# In[50]:

sns.barplot(x="ave_diff", y="Site", hue="swim", data=test_freq)


# In[52]:

test_freq.iplot(kind='bar', x="ave_diff", y="Site", orientation = 'h',text='Site',
             xTitle='Test Time Gap',
             filename='cufflinks/q2-bar-chart')


# **Conlusion-1: Upper Sparkill Creek and Piermont Pier have been tested most regularly. Gowanus Canal and Tarryto Marina have long gaps between tests. Then Pick out 5-10 sites and visually compare how regularly their water quality is tested.**

# In[54]:

timesub = hudson.loc[(hudson.Site == 'Poughkeepsie Drinking Water Intake')| 
                    (hudson.Site == 'Poughkeepsie Launch Ramp')| 
                    (hudson.Site == 'Pier 96 Kayak Launch')|
                    (hudson.Site == 'East River mid-channel at Roosevelt Is.')|
                    (hudson.Site == 'The Battery mid-channel')|
                    (hudson.Site == 'Tarrytown Marina')|
                    (hudson.Site == 'Upper Sparkill Creek')|
                    (hudson.Site == 'West Point STP Outfall')|
                    (hudson.Site == 'Cold Spring Harbor')]
timesub.Site.unique()


# In[56]:

sns.violinplot(x="day_diff", y="Site", hue="swim", data=timesub,
               bw=.1, scale="count", scale_hue=False)


# **Conclusion-2: The two best swim sites, the worst swim site and some other sites were chosen to compare the gap between tests. There is no difference on the frequency of test between different sites.**

# #### 3. Is there a relationship between the amount of rain and water quality? Show this relationship graphically. If you can, estimate the effect of rain on quality at different sites and create a visualization to compare them.

# In[57]:

sns.set(style="ticks", color_codes=True)


# In[58]:

rain = hudson.loc[:,['Site','EnteroCount','FourDayRainTotal']]


# In[59]:

g = sns.FacetGrid(rain, col="Site", col_wrap=5, size=3)
g = g.map(sns.regplot, "FourDayRainTotal", "EnteroCount", marker=".")


# In[60]:

rainsub = rain.loc[(rain.Site == 'Poughkeepsie Drinking Water Intake')| 
                    (rain.Site == 'Poughkeepsie Launch Ramp')| 
                    (rain.Site == 'Pier 96 Kayak Launch')|
                    (rain.Site == 'East River mid-channel at Roosevelt Is.')|
                    (rain.Site == 'The Battery mid-channel')|
                    (rain.Site == 'Tarrytown Marina')|
                    (rain.Site == 'Upper Sparkill Creek')|
                    (rain.Site == 'West Point STP Outfall')|
                    (rain.Site == 'Cold Spring Harbor')]
rainsub.Site.unique()


# In[61]:

g = sns.lmplot(x="FourDayRainTotal", y="EnteroCount", col="Site", hue="Site", data=rainsub, col_wrap=3, size=3)

# Additional line to adjust some appearance issue
plt.subplots_adjust(top=0.9)

# Set the Title of the graph 
g.fig.suptitle('Effects of Rain on Water Quality', fontsize=34,color="r",alpha=0.5)


# **According to the linear regression plots, we can see there is no correlations between rain and the water quality. We can confirm this conclusion by the linear regression model for each sites as shown as follows.**

# In[62]:

from statsmodels.formula.api import ols

for location in rain.Site.unique():
    tempdf = rain[rain.Site == location]
    x = tempdf['EnteroCount']
    y = tempdf['FourDayRainTotal']
    model = ols("y ~ x",tempdf)
    results = model.fit()
    print (results.summary())


# **R-square values are all very small, suggesting that there is no correlation between rain and the water quality.**
