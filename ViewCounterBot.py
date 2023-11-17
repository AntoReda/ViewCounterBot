from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromService
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import random
from datetime import date
import datetime
import matplotlib.pyplot as plt
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import requests
import math

# List of questions you need to provide:_______________________________________________________________________

# Approximately how many hours would you like me to run for?
runTime=5

# What is your username and password for Facebook?
username = ""
password = ""

# Depending on which listing you want to record, find the CSS class elements of the text that displays '0 clicks on listing' you can find this by using inspect mode. 
# This class should locate the first listing regardless. Yes you can change the way this bot selects the listing but I did it manually. You can find it on line 139.
NumberOfViewsText = '[class="x78zum5 x1q0g3np xg7h5cd"]'

# To avoid detection use a consistent user agent. Paste the contents here. You can find your user agent by browsing to: https://www.whatismybrowser.com/detect/what-is-my-user-agent/
# I added a starting sample. However you must keep the --user-agent=
userAgent = '--user-agent=Mozilla/5.0 (Windows...)...'

# The file path in which this repo is located on your comp and add /GraphPic.png at the end.
GraphFilePath = ""

# The file path in which this repo is located on your comp and add /listing.png at the end.
ListingFilePath =""

# Needed for sending a message to Discord. Insert your webhooks URL link here.
discURL=''

# Needed for sending a message to Discord. To find the right headers for you, follow these instructions carefully: 
# Open Discord on your browser (you will not find this info if you use the app but it will work on the app once it is setup) Open the channel in which you configured your Discord webhook
# Right click the message field (where you enter text)
# Select inspect and open the Network tab now write a message in the text field and send it to the channel>>you will see the network traffic show up in your inspect mode. Look for the field named "message"
# Click "message" in the Network block>> select the headers tab>>scroll down until you find Authorization and paste the contents here. Should look like some gibberish, example: cyNzY2OTk3vsihvjxbYHHhojc
headers ={
    "Authorization": ""
}
# Sending the discord message (you can edit it how you like).
discMessage1= "Hello, here is the graph showing the listing and its view counter throughout the day: "
discMessage2 ="Here is the listing I evaluated: "

# Add the message to your payload.
payload1 = {
    "content": discMessage1
}
payload2 = {
    "content": discMessage2
}
#_____________________________________________________________________________________________________________






# Instantiate the chrome options.
chrome_options = Options()

# Add your Chrome options (makes screen bigger, disables automation flag and adds consistent user agent to avoid bot detection also disables notifications that would otherwise prompt bot for input).
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument(userAgent)
chrome_options.add_argument("--disable-notifications")

# Create a DesiredCapabilities instance
capabilities = DesiredCapabilities.CHROME.copy()

# Set the dictionary of capabilities
capabilities['goog:chromeOptions'] = {'args': [], 'extensions': []}
capabilities['goog:chromeOptions']['args'].extend(chrome_options.arguments)

# Instantiate the WebDriver with the options above.
driver = webdriver.Chrome(chrome_options)
driver.maximize_window()
driver.get("https://facebook.com")
time.sleep(random.randrange(6,20))

# Find the email and password input fields and enter your login credentials
email_input = driver.find_element("id", "email").send_keys(username)
time.sleep(random.randrange(6,20))
passw_input = driver.find_element("id", "pass").send_keys(password)

driver.find_element("name", "login").click()

time.sleep(random.randrange(6,20))


marketplacelinkID= "x1lliihq x6ikm8r x10wlt62 x1n2onr6"
#finds the marketplace button
driver.find_element("xpath","//span[contains(text(), 'Marketplace')]").click()
time.sleep(random.randrange(5,10))
driver.find_element("xpath","//span[contains(text(), 'Selling')]").click()
time.sleep(random.randrange(5,12))

# initializes an array of fixed size = 24
timeContainer=[0]*24



#retrieves the number of views and assigns it to the variable called viewCounter. Keep in mind, viewcounter is a web element so we must retrieve the text using .text
try:
    # Create or overwrite a file and add some initial text.
    with open('DetailedViews.txt', 'w') as wFile:
            wFile.write("Below you will find the detailed view count for this listing:\n")
    # Do some math so that the program loops properly.
    runTime = (runTime*60)/3
    loopTime = int(math.ceil(runTime))
    # Loop for recording time.
    for i in range (loopTime):

        #saves only the hour (not military time)
        militaryHour = datetime.datetime.now().hour
        if militaryHour>12:
            hour = militaryHour-12
        else:
            hour=militaryHour

        decimal = -1

        # Saves the text of the listing number inside a variable. Keep in mind, this is not a string but an obj so you must use viewCounter.text if you wish to treat it like a string.
        viewCounter = driver.find_element(By.CSS_SELECTOR, NumberOfViewsText)

        # Checks how many digits the viewCounter has and turns that substring into a number
        for j in range(4):
            if viewCounter.text[j]!=" ":
                decimal=decimal+1

        # Extracts the number from facebook string
        intCounter = int(viewCounter.text[0:decimal])
        
        # Prints info on txt doc.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"At {timestamp}, This post has: {intCounter} views.\n"
        with open('DetailedViews.txt', 'a') as wFile:
            wFile.write(message)
            
        # Assigns the view value to an array to later graph.
        timeContainer[militaryHour-1]=intCounter
        time.sleep(random.randrange(150,190))
        driver.refresh()
        time.sleep(random.randrange(2,5))
    
except Exception as errorName: 
    print("Error Something went wrong see below: \n",errorName)
    driver.quit()
    exit()

# Now that the data is scraped, click on the listing and take a screenshot.
driver.find_element(By.CSS_SELECTOR, '[class="xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3"]').click()
time.sleep(random.randrange(5,10))
driver.save_screenshot(r''+ListingFilePath)

# Saves date
format= '%Y-%m-%d'
yearMonthDay=date.today().strftime(format)

# x-coordinates of left sides of bars  
left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] 

# heights of bars 
height = [timeContainer[0], timeContainer[1], timeContainer[2], timeContainer[3], timeContainer[4],timeContainer[5], timeContainer[6], timeContainer[7], timeContainer[8],timeContainer[9],timeContainer[10],timeContainer[11],timeContainer[12],timeContainer[13],timeContainer[14],timeContainer[15],timeContainer[16],timeContainer[17],timeContainer[18],timeContainer[19],timeContainer[20],timeContainer[21],timeContainer[22],timeContainer[23]] 

# labels for bars 
tick_label = ['1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am','11am', '12pm', '1pm', '2pm', '3pm','4pm', '5pm', '6pm', '7pm', '8pm','9pm', '10pm', '11pm', '12am'] 

# Enlarges the graph.
plt.figure(figsize=(20, 9))

# Plotting a bar chart and adding colors.
plt.bar(left, height, tick_label = tick_label, 
        width = 0.6, color = ['royalblue', 'khaki', 'cornflowerblue']) 
  
# Naming the x-axis 
plt.xlabel('Time') 

# Naming the y-axis 
plt.ylabel('Number of Views') 

# Plot title 
title = "Facebook Marketplace View Counter! Date: "+ yearMonthDay
plt.title(title) 

# Save the image of the plot.
plt.savefig('GraphPic.png', dpi='figure', format='png')


# Save the file path
file_path1 = r''+GraphFilePath
file_path2 = r''+ListingFilePath

# Open the image file
with open(file_path1, 'rb') as file1:
    file_content1 = file1.read()
    files1 = {'file': ('GraphPic.png', file_content1)}

with open(file_path2, 'rb') as file2:
    file_content2 = file2.read()
    files2 = {'file': ('listing.png', file_content2)}
  
# Sends message to discord channel.
sendMessage=requests.post(discURL, payload1, headers=headers, files=files1)
sendMessage=requests.post(discURL, payload2, headers=headers, files=files2)

#closes the session
time.sleep(5)
driver.quit()
exit()
