import pandas as pd
import re
import yagmail
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

######################################################################################################
# Using Send email function for if new dogs are found, using Yagmail
# To run this program yourself change the sender/receiver_email and password below!
######################################################################################################
def send_email(df):
    sender_email = 'lukefeilbergp@gmail.com'
    receiver_email = '19495255075@tmomail.net'
    subject = 'New dogs alert!'
    password = 'Enter_Password_Here'
    contents = []
    
    yag = yagmail.SMTP(user=sender_email, password=password)
    
    # Displaying at most 5
    for i in range(min(len(df), 5)):
        contents.append('')
        contents.append(df.iloc[i]['name']
                        + ', '
                        + df.iloc[i]['breed']
                        + ', '
                        + df.iloc[i]['age'])
    
    contents.extend(['', 'https://labsandmore.org/dogs/'])

    yag.send(receiver_email, subject, contents);


######################################################################################################
# Using Selenium to scrape website
# 
######################################################################################################
# Setting path to Selenium Firefox browser
path = r'C:\Users\lukef\AppData\Local\BrowserDriver\geckodriver.exe'

# Setting headless
options = webdriver.FirefoxOptions()
options.headless = True

# Initializing browser
driver = webdriver.Firefox(executable_path = path, options = options)

# Navigating to website
driver.get('https://labsandmore.org/dogs/')
time.sleep(20)


######################################################################################################
# Scraping the breed, details, and name
######################################################################################################
i = 0
breed = []
details = []
name = []

# First looping through breed and details elements
for li in driver.find_elements_by_xpath("//div[@class='property-stats']//ul//li"):
       
    # Alternates between breed and details in the li (list) elements
    if i % 2 == 0:
        breed.append(li.text)
    else:
        details.append(li.text)
    
    i += 1
    
# Now looping through the name elements
for li in driver.find_elements_by_xpath("//div[@class='tile-footer']/div[@class='price']/a"):
       
    name.append(li.text)

# Closing the browswer
driver.close()


######################################################################################################
# Creating Pandas DataFrame
######################################################################################################
df = pd.DataFrame(dict(name=name,breed=breed,details=details))


######################################################################################################
# Extracting info from the details column
######################################################################################################
df[['gender','age','weight','id']] = df['details'].str.extract(pat = r'(.*?),\s(.*?),\s(.*?)\.\sID\s(\d*)')

df.drop(columns = 'details', inplace = True)

df['id'] = df['id'].astype('int32')


######################################################################################################
# Checking if dog is unavailable
######################################################################################################
df['unavailable'] = df['name'].str.lower().str.contains('adopted') \
                  | df['name'].str.lower().str.contains('list full')


######################################################################################################
# Reading in saved (old) dataframe
######################################################################################################
try:
    old = pd.read_csv('dogs.csv')
except:
    old = pd.DataFrame(columns = df.columns)


######################################################################################################
# Checking for new dogs, sending email if so!
######################################################################################################
# If an id is not in the old list of id's
if sum(~df['id'].isin(old['id'])) > 0:

    print('New dogs found! :-)')
    
    new_dogs = df[~df['id'].isin(old['id'])]
    
    send_email(new_dogs)

else:

    print('No new dogs yet!')

######################################################################################################
# Concatenating and dropping duplicates, then saving for next time
######################################################################################################
old_and_new = pd.concat([df, old])  

old_and_new.drop_duplicates(subset='id',keep='first',inplace=True)

old_and_new.to_csv('dogs.csv', index = False)
