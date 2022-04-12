#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset - [No Show Appointment]
# 
# ● In this project we will analyze 110.527 medical appointments with its 14 associated variables.<br>
#   From this dataset we want to analyze the patient behavior of showing or not showing to their appointments.<br>
#   
#   Some of the features are not answering our questions and some are let's descover some of these features:-<br> 
# 
# ## Describing the features 
# 
# ● ‘ScheduledDay’ indicates the day our patient called or registered the appointment.<br>
# ● ‘Neighborhood’ indicates where the appointment takes place.<br>
# ● ‘Scholarship’ indicates whether or not the patient is enrolled in Brasilian welfare program Bolsa Família.<br>
# ● ‘No_show’ it says ‘No’ if the patient showed up to their appointment, and ‘Yes’ if they did not show up.<br>
# 
# ## Questions to be answered:
# 1- What is the distribution of the appointment for showing or not ?<br>
# 2- How each factor ("Age", "Gender", "Scholarship", "Alchoholi", "Having as SMS") affects the appointements rates ?

# In[1]:


# importing the libraries
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# # Data Wrangling
# >Check for cleanliness, and then trim and clean the dataset before analysis

# ## Generel Properties 

# In[4]:


# Load the data. 
df = pd.read_csv('noshowappointments-kagglev2-may-2016.csv')
df.head()


# In[48]:


df.info()


# In[49]:


#summary of the data 
df.describe()


# In[50]:


# No Null Values 
df.isna().sum()


# ## Looking for Data that need to be cleaned
# >Looking for the duplicated Patient IDs with the same status of No_show.

# In[51]:


df[df['Gender'] ==  37.08887421173107]


# > Check for the Age feature as we found value of "-1" in df.describe() 

# In[52]:


df[df["Age"] <= 0]


# 
# ### Data Cleaning
# > Fixing Typos in the column names
#  

# In[53]:


df.rename(columns = {'Hipertension': 'Hypertension', 'Handcap': 'Handicap','No-show':'No_show'}, inplace = True)


# > Converting the Schedule Day and Appointment Day into Date time 

# In[54]:


df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])


# >fixing the ages that are less then 0 by taking the mean of all ages and put those values into it

# In[55]:


mean_age = df['Age'].mean()
df[df['Age'] <= 0] = mean_age


# > For making the data more representative and plotable, we will convert the No_show values from No, Yes into 0,1

# In[56]:


df.drop(df[df['Age'] == 37.08887421173107].index, inplace = True)


# In[57]:


df.No_show[df['No_show'] == 'Yes'] = '1'
df.No_show[df['No_show'] == 'No'] = '0'
df['No_show'] = pd.to_numeric(df['No_show'])


# In[58]:


showed = df['No_show'] == 0
not_showed = df['No_show'] == 1
df['showed'] = showed
df['not_showed'] = not_showed
print(type(showed), type(df['Age']))


# <a id='eda'></a>
# ## Exploratory Data Analysis
# ### Research Question 1 (What is the distribution of the appointment for showing or not ?)

# In[59]:


total_attend = df['showed'].value_counts()
print(total_attend[1] / total_attend.sum() * 100)
pieChart = total_attend.plot.pie(figsize=(10,10), autopct='%1.1f%%', fontsize = 12);
pieChart.set_title("Status" + ' (%) (Per appointment)\n', fontsize = 15);
plt.legend();


# ## Summary :
# ### Answering question 1 : 
# > We can see that 79.7 % of the appointments is made. So we need to study what the features affecting the appointment rate

# ### Research Question 2  (How each factor ["Age", "Gender", "Scholarship", "Alchoholic", "Receiving SMS"] affects the appointements rates ?)

# ### The average age of people who show up and people who didn't
# 

# In[60]:


df.Age[showed].mean() , df.Age[not_showed].mean()


# In[61]:


def committment_hist (df, col_name, showed, not_showed):
    ''' This function is for plotting the effect of a specific feature "col_name" on the showing and not showing results.
        
        Paramaters :
            df (pd.DataFrame): the DataFrame we need to study.
            col_name (pd.Series): the specific coulmn we need to study its effect.
            showed (pd.Series): the mask for the showed dataset.
            not_showed (pd.Series): the mask for the not showed dataset.
            
        Returns :
            NA
        
        Outputs :
            1- Printing the Summary of the feature effect on the dataset. 
            2- Plotting the histogram of the desired feature in the showed and not showed groups. 
    '''
    try :
        print('Showed Appointment Rate affected by {} = {}'.format(col_name,df[col_name][showed].mean()))
        print('Not Showed Appointment Rate affected by {} = {}'.format(col_name,df[col_name][not_showed].mean()))
    except:
        print('The categories percentage in the showed group in ',  df.groupby(col_name)['showed'].mean())
    plt.figure(figsize= (15,5))
    df[col_name][showed].hist(alpha= 0.5, bins= 10, color= 'green', label= 'Show')
    df[col_name][not_showed].hist(alpha= 0.5, bins= 10, color= 'blue', label= 'No show')
    plt.legend();
    plt.title('Comparing by {}'.format(col_name))
    plt.xlabel('{}'.format(col_name))
    plt.ylabel('Number of Patients')

committment_hist(df, 'Age', showed, not_showed);


# ### Age Effect on Appointment Rate:
# >The average of the age for people who will be most likely to show up is 39.0 and the average age for people who are not likely to show up is 35.3. 

# In[62]:


committment_hist(df, 'Gender', showed, not_showed);


# In[63]:


committment_hist(df, 'Scholarship', showed, not_showed);


# In[64]:


committment_hist(df, 'SMS_received', showed, not_showed);


# In[65]:


committment_hist(df, 'Alcoholism', showed, not_showed);


# <a id='conclusions'></a>
# ## Conclusions
# 
# >- We can conclude that thew Age has the most effect on the appointment showing.
# >- We can also conclude that SMS Receive unlogically has no effect on the appointment showing which mean it's better to review >the SMS campaign, the content, or the sending time ,...etc.
# >- We can see that people with Scholarship tend to miss their appointment as 0.76% of showing VS 0.80% of patients with no scholarship showed.
# >- Gender also is not affecting the results as 0.796 F Vs 0.799 M showing percentage found.
# 
# ## Limitations
# >It could be helpful if the data set contains the working status as a feature which will be representive with the existed features.
# > Also the working hours with the neighbourhood feature will give a good representation as well.
# 
# 
# ## Summary
# 
# > For most of the features the Age has the most effect on showing status as the average of the age for people who will be most likely to show up is 39.0 and the average age for people who are not likely to show up is 35.3. 
# 
# 
# 

# In[66]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




