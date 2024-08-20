#!/usr/bin/env python
# coding: utf-8

# ## Fedaral Election Commission Data Exploration

# This project focuses on the exploration and analysis of Federal Election Commission (FEC) data using Python and the Pandas library. The dataset contains information on individual contributions to various candidates during a specific election cycle. Through this analysis, we aim to gain insights into the data, such as identifying top contributors, understanding the distribution of contributions by party, and analyzing patterns based on occupation and employer.

# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
print(pd.__version__)


# In[4]:


import os
cwd = os.getcwd()
print("Current working directory:", cwd)


# # Initial exploration and clean-up

# In[6]:


import pandas as pd 
df= pd.read_csv("fecdata.csv",low_memory=False)


# In[7]:


df.head()


# In[13]:


df.iloc[:,5].dtype


# In[14]:


df.iloc[:,5].unique()


# In[15]:


df.info()


# Get a random sample:

# In[16]:


df.sample(5)


# summarize numerical data

# In[17]:


df.describe()


# Get a list of the unique candidates(unique_candidates):

# In[19]:


unique_candidates = df['cand_nm'].unique()
unique_candidates


# Assign party affiliations(they are al republicans except for barack obama):

# In[20]:


party_affiliations ={name:'D' if name== 'Obama, Barack' else'R' for name in unique_candidates}
party_affiliations


# In[21]:


aff = {name:'D' if name=="Obama, Barack" else "R" for name in unique_candidates}
aff


# In[23]:


candidate_sample =df['cand_nm'].sample(5)
candidate_sample


# In[24]:


candidate_sample.map(party_affiliations)


# In[25]:


df['party']=df['cand_nm'].map(party_affiliations)


# In[26]:


df.sample(5)


# ## Total contributions by party and candidate

# What was the total amount of contributions(in millions of dollars)?

# In[27]:


df['contb_receipt_amt'].sum()*1e-6 # millions of dollars 


# Which party got more individual donations(transactions,not total dollars)?

# In[28]:


df['party'].value_counts()


# Which party got more total dollars?

# In[30]:


df.groupby('party')['contb_receipt_amt'].sum()*1e-6


# Filter aall the data to include only the two main candidates, romney and obama.

# In[36]:


keep_candidates={'Obama, Barack','Romney, Mitt'}


# In[37]:


matches =df['cand_nm'].apply(lambda x:x in keep_candidates)
df[matches].shape


# In[42]:


fecmain =df[df['cand_nm'].isin(keep_candidates)].copy()
print(fecmain['cand_nm'].unique())
display(fecmain.sample(5))
display(fecmain.groupby('cand_nm')['contb_receipt_amt'].sum()*1e-6)


# ## WHo contributes?

# Get a list of top occupations:

# In[43]:


len(fecmain['contbr_occupation'].unique())


# In[44]:


fecmain['contbr_occupation'].value_counts()


# Replace synonyms:(also:dict.get())

# In[45]:


occ_mapping ={'INFORMATION REQUESTED ': 'NOT PROVIDED',
             'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED',
               'C.E.O.': 'CEO'}


# In[46]:


fecmain['contbr_occupation'].map(occ_mapping)


# In[47]:


# .get()!
print(occ_mapping.get('PROFESSOR'))
print(occ_mapping.get('PROFESSOR', 'PROFESSOR'))


# In[48]:


fecmain['contbr_occupation'] = fecmain['contbr_occupation'].map(lambda x: occ_mapping.get(x, x))


# In[49]:


fecmain['contbr_occupation']


# Synonymous employer mappings:

# In[50]:


emp_mapping = occ_mapping.copy()
emp_mapping['SELF']='SELF-EMPLOYED'
emp_mapping['SELF EMPLOYED']='SELF-EMPLOYED'
emp_mapping


# In[51]:


fecmain['contbr_employer']= fecmain['contbr_employer'].map(lambda x: emp_mapping.get(x,x))


# In[52]:


emp_mapping.get('prof','pro')


# Create a "pivot table" taht shows occupations as rows and party affiliation as columns, summing the individual contributions.

# In[53]:


by_occ = fecmain.pivot_table('contb_receipt_amt',index ='contbr_occupation',columns='party',aggfunc='sum')
by_occ


# Determine wich occupations account for $1 million or more in contributions.Compare the amounts between the two party affiliations.(Bonus : Make a plot to compare these visually.)

# In[54]:


over_1mil = by_occ[by_occ.sum(axis=1) > 1e6]*1e-6
len(over_1mil)


# In[55]:


over_1mil


# In[57]:


sorted_occ = over_1mil.sum(axis=1).sort_values()
sorted_occ


# In[58]:


over_1mil_sorted =over_1mil.loc[sorted_occ.index]
over_1mil_sorted.plot(kind='barh',stacked=True, figsize=(10,6));


# ## Simple ranking 

# Determine largest donors:

# In[60]:


largest_donors = fecmain['contb_receipt_amt'].nlargest(7)
largest_donors


# In[61]:


fecmain.loc[largest_donors.index]


# Display donors , grouped by candidate:

# In[62]:


grouped = fecmain.groupby('cand_nm')
grouped['contb_receipt_amt'].nlargest(3)


# In[63]:


type(grouped)


# .apply() for groups:

# In[64]:


grouped.apply(lambda x: type(x))


# Use .apply() to get DataFrame objects showing the largest donors,grouped by candidate and occupation: 

# In[65]:


def top_amounts_by_occupation(df,n=5):
    # Fill me in!
    totals =df.groupby('contbr_occupation')['contb_receipt_amt'].sum()
    return totals.nlargest(n)
top_amounts_by_occupation(fecmain)


# In[66]:


grouped.apply(top_amounts_by_occupation,n=10)


# ## Big vs. small donations

# For each of the leading two candidates, did most of their money come from large or small donations?

# In[67]:


bins =[0]+ [10**k for k in range(0,8)]
bins


# In[68]:


labels = pd.cut(fecmain['contb_receipt_amt'], bins, right=False)
labels[:5]


# In[69]:


grouped = fecmain.groupby(['cand_nm',labels])
grouped.size()


# Fin!

# In[ ]:




