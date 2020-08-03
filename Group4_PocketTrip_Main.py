# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 13:53:48 2020

@authors:   Gong, Siyu siyugong@andrew.cmu.edu
            Li, Zihan zihanli@andrew.cmu.edu
            Sharma, Arun aruns2@andrew.cmu.edu
            Sutaria, Rutvi rsutaria@andrew.cmu.edu
            Wang, Yuxi yuxiwang@andrew.cmu.edu
"""
# Source Code for PocketTrip- A start up that provides budget-based travel solutions

#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver



#function expense takes city as the argument and returns cost of common expenses in that city,
## currently,operational for London only
def expense(city):
    if city == "london":
        page = "https://www.expatistan.com/cost-of-living/london"
        
        #reading and creating soup
        page_data = requests.get(page)
        soup = BeautifulSoup(page_data.content, "html.parser")
                      
        #finding all with class = data_wide_table
        items = soup.findAll("tr")
        item = items[1]
        list_expense =[]
        list_price =[]
         
        #finding all the expense headers
        expense_name = item.findAll("td", {"class":"item-name"})
        
        #looping over expense_names
        for expense  in expense_name:
            list_expense.append(expense.text.strip())
        
        #finding prices
        prices = item.findAll("td", {"class":"price city-1"})
        
        #looping over prices
        for price  in prices:
            list_price.append(price.text.strip())
            
        #creating a dictionary for items and their prices
        expense = dict(zip(list_expense,list_price))
        
        #creating dataframes for further analysis
        expense_df = pd.DataFrame(expense.items(), columns =['Item', 'Price'])
        expense_df['Prices in GBP'] = expense_df[expense_df.columns[1:]].replace('[\£,]', '', regex=True).astype(float)
        del expense_df['Price']
        return expense_df

#---------------------------------------------------------------------------------#

#function leisure_activities takes city as the argument and returns cost of popular tourists desstinations in that city,
## currently,operational for London

def leisure_activities(city):
    if city == "london":
        page = "https://www.globalprice.info/en/?p=britan/museums-prices-in-london"
        
        #reading page and creating soup
        page_data = requests.get(page)
        soup = BeautifulSoup(page_data.content, "html.parser")
        
        #initialise list
        prices =[]
        
        #finding all with class = data_wide_table
        items = soup.findAll("span",{"class":"yel"})
        item_text = soup.findAll("ul")
        item_text_new = item_text[5].text.replace(",", ".")
        item_text_new = item_text_new.replace("brochure in Russian, 6.4 USD ,  5 GBP"," ")
        item_text_new = item_text_new.replace("  ",", ")
        item_text_new = item_text_new.replace("=",", ")
        item_text_new = item_text_new.replace(",","\n")
        
        #item_text_new
        m = re.findall('\n.*',item_text_new )
        items=[]
        prices=[]
        i=0
        
        #looping to append items and their prices
        for line in m:
            if i%3 == 0:
                items.append(line.strip())
            if i%3 ==2:
                prices.append(line.strip())
            if i == 38:
                break
            i+=1
        #create dictionary
        museums = dict(zip(items, prices))
        
        #convert to Data Frame
        museums_df = pd.DataFrame(museums.items(), columns = ['Leisure_Activity', 'Price'])
        museums_df['Prices in GBP-M'] = museums_df[museums_df.columns[1:]].replace('[ GBP,]', '', regex=True).astype(float)
        del museums_df['Price']
        return museums_df
    
leisure_activities("london")

#function lconversion rate scrapes the web and gets the latest conversion rates to GBP 
def conversion_rates():
    page = "https://www.x-rates.com/"

    #changing headers as sometime default is crawler and sites halt it
    #headers = {'User-Agent':'Mozilla/5.0'}
    page_data = requests.get(page)
    soup = BeautifulSoup(page_data.content, "html.parser")
    
    
    #finding all with class = data_wide_table
    items = soup.findAll("tr")
    items[2].th.text
    conversion_rate =[]
    rates = items[2].findAll("td")
    
    
    for i in range(len(rates)):
        if i !=1:
            conversion_rate.append(rates[i].a.text)
    conversion_rate
    conversion_scale = ["GBP-USD","GBP-CAD","GBP-EUR","GBP-AUD"]
    
    #create Dictionary
    conversion = dict(zip(conversion_scale,conversion_rate))
    
    #convert the rates from string to floats
    for v,j in conversion.items():
        conversion[v] = float(j)
    
    return conversion

#storing the latest rates
conversion_GBP = conversion_rates()

 #********************************************************************************
 
#function convert takes the amount entered by user and the currency type 
#entered by user as the argument and returns the converted amount to GBP as per the latest conversion rate
def convert(amount, choice):
    
    #Type 1: For USD, Type 2: For CAD, Type 3: For EUR, Type 4: For AUD, Type 5: For GBP
    if choice == 5:
        s = "Hi! You have entered {:>7.2f} GBP".format(amount)
        return s
    if choice == 4:
        amount = amount/conversion_GBP['GBP-AUD']
        return amount
    if choice == 3:
        amount = amount/conversion_GBP['GBP-EUR']
        return amount
    if choice == 2:
        amount = amount/conversion_GBP['GBP-CAD']
        return amount
    if choice == 1:
        amount = amount/conversion_GBP['GBP-USD']
        return amount

#***********************************************************************

#User Input Module

m=1
while m ==1:
#Asking for the city
    city = input("Thank You for choosing Pocket Travel- Which part of the world you would Like to explore?" +"\n")
    city = city.strip()
    city = city.lower()
           
    if city == "london":
        m=2
        ppl_bad = True
        i=1
        nodays_bad = True
        j = 1
        budget_bad = True
        k =1
        currency_bad  = True
        l = 1
        # loop till information about number of people is collected in the required format
        while ppl_bad:    
            try:
                if i == 1:
                    no_of_ppl = input("Sure, we can help you! How many of you would be travelling?" + "\n")
                    no_of_ppl =  int(no_of_ppl)
                else:
                    no_of_ppl = input("Please try again!"+ "\n")
                    no_of_ppl =  int(no_of_ppl)
                    
            except:
                print("Bad Format: Number of people can only be a positive integer")
                i+=1
                continue
            if not 0 < no_of_ppl <50:
                print("Those are either too less or Too many people"+"\n")
                i+=1
            else:
                ppl_bad = False
        #Ask the user to input the trip start ad the end date and calculate number of days
        while nodays_bad:    
            try:
                if j == 1:
                    startDate = input("Awesome! Please enter the trip start date (yyyy-mm-dd): ") #check the formatting
                    endDate = input("Enter the trip end date (yyyy-mm-dd): ")
                    start = int(startDate[-2:]) 
                    end = int(endDate[-2:])
                    #calculate the number of days
                    no_of_days = int(end - start + 1)
            
                else:
                    no_of_days = input("Please try again!" + "\n")
                    no_of_days =  int(no_of_days)
                    
            except:
                print("Bad Format: Number of days can only be a positive integer" +"\n")
                j+=1
                continue
            nodays_bad = False
        # ask the user the type of their currency and store the information
        while currency_bad:    
            try:
                if l == 1:
                    currency = input("Cool! In what currency would you be paying: Please Type 1: For USD, Type 2: For CAD, Type 3: For EUR, Type 4: For AUD, Type 5: For GBP" + "\n")
                    currency = int(currency)
            
                else:
                    currency = input("Please try again!" + "\n")
                    currency = int(currency)
                    
            except:
                print("Bad Format: Choose the options provided" + "\n")
                l+=1
                continue
            if not 1 <= currency <=5:
                print("We do not support that currency, yet!" + "\n")
                l+=1
            else:
                currency_bad = False
        #ask the user what their daily budget is and store the information
        while budget_bad:    
            try:
                if k == 1:
                    amount = input("Great! What budget per day do you have in mind?" + "\n")
                    amount = float(amount)
            
                else:
                    amount = input("Please try again!"+ "\n")
                    amount =  float(amount)
                    
            except:
                print("Bad Format: amount can be positive" + "\n")
                k+=1
                continue
            if not 0 < amount <100000:
                print("That is an invalid amount" +"\n")
                k+=1
            else:
                amount = convert(amount,currency)
                budget_bad = False
                
        print("\n\nHi! The equivalent GBP amount for the value you have entered is ** {:>7.2f} GBP **".format(amount))      
    else:
       m = input("Sorry, we currently serve only London. If you wish to travel to London please press 1 else check back later. Thank You!" + "\n")
       m = int(m)   
      
#**********************************************************************************

#Webscraping hotel information

# example option: add 'incognito' command line arg to options
option = webdriver.ChromeOptions()
option.add_argument("--incognito")


#set up chrome driver path
chrome_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path = chrome_path, chrome_options=option)

#scarp the hotels for those particluar days from Expedia 
driver.get("https://www.expedia.com/Hotel-Search?GOTO=HOTSEARCH&SearchArea=City&SearchType=Place&adults=1&children=&destination=London%2C%60England%2C%20United%20Kingdom&endDate="+endDate+"&lang=1033&latLong=&needUTF8Decode=true&regionId=178279&rfrr=hotel.search&selected=&sort=RECOMMENDED&startDate="+startDate)

#get the resulting hotel information from the site
hotels = list(driver.find_elements_by_class_name("results"))
hotel = [x.text for x in hotels]
hotel = hotel[0].split('\n')

# Using regular expressions, get the hotel name and price
name_pat = r'Click for more information about'
price_pat = r'Price is'
price_in_nums = r'^[$]'
review_pat = r'^.*.reviews.*$'

# define lists to store hotel details
Hotel_names = []
Price = []
Rating = []

#store the hotel details (name, price and review) in a list
for line in hotel:
    if re.search(name_pat, line) != None:
        name_slice = line[33:] 
        final_name = name_slice[:-23]
        Hotel_names.append(final_name)
    if re.search(price_pat,line) != None:
        price_slice = line[-3:]
        if(price_slice[0] == '$'):
            final_price = price_slice[1:]
        else:
            final_price = price_slice
        Price.append(final_price)
    if re.search(review_pat, line) != None:
        Rating.append(line[:3])
 
#Handle missing values       
while (len(Hotel_names) < 20):
    Hotel_names.append("NA")
while (len(Price) < 20):
    Price.append("102")
while (len(Rating) < 20):
    Rating.append("3.4")
    
#only scrap the first 20 values as they are enough
Hotel_names = Hotel_names[:20]
Price = Price[:20]
Rating = Rating[:20]
    
#*********************************************************************************

#calling expense function to store the latest expense rate in the city
df_expenses = expense(city)

#callinf the leisure activities function to get the prices for the most popular activities in the city
df_leisure_activities = leisure_activities(city)
    

#hotel sample result (if the scraping fails, please comment the code from line 311 till 338 and uncomment code from 351 to 353)
    
#Rating = ['4.3', '4.5', '3.5', '4.3', '3.7', '3.2', '4.2', '4.2', '4.0', '4.4', '4.4', '3.8', '3.8', '3.5', '3.8', '3.9', '4.6', '4.6', '4.2', '4.0']
#Price = ['208', '199', '147', '149', '160', '107', '151', '273', '163', '241', '228', '86', '96', '94', '127', '107', '214', '316', '263', '148']
#Hotel_names = ['The Tower Hotel', 'Nhow London', 'Marlin Canary Wharf', 'StowAway Waterloo by Bridgestreet', 'Marlin Apartments London Bridge - Empire Square', 'Chelsea Cloisters', 'Phoenix Heights By Bridgestreet', 'Amba Hotel Grosvenor', 'Native Hyde Park', "130 Queen's Gate Apartments", 'Manson Place', 'Rainbow Studios Canary Wharf', 'Courtfield Studios', 'The Park Grand London Paddington', 'MStay39 Studios', 'Grand Plaza Serviced Apartments', 'Circus Apartments by BridgeStreet', 'Ashburn Court', 'Chilworth Court', 'The Strand Palace Hotel']

#creating dictionary and then data frame
hotels = {"Hotels":Hotel_names,"Ratings":Rating, "Price":Price}
hotels_df = pd.DataFrame(hotels, columns = ['Hotels', 'Ratings', 'Price'])

#sorting the prices to get the cheapest hotels
sort_price = hotels_df.sort_values(by='Price')
sort_price['Price'] = sort_price['Price'].astype(float)

#convert to GBP
sort_price['Price']/=conversion_GBP['GBP-USD']

#sorting the ratings to get the highest rating hotel
sort_rating = hotels_df.sort_values(by ='Ratings', ascending = False)
sort_rating['Ratings'] = sort_rating['Ratings'].astype(float)

# building arrays to store ratings and prices for later plots
arr1 = np.array(sort_rating['Ratings'])
arr2 = np.array(sort_price['Price'])

#calculating the mean ratings
sort_rating['Ratings'].mean()

#cnvert to float type
sort_rating['Price'] = sort_price['Price'].astype(float)
#convert to GBP
sort_rating['Price']/=conversion_GBP['GBP-USD']

sort_price['Price'] = sort_price['Price'].astype(float)

#calculate the mean hotel price dor the givent date range
sort_price['Price'].mean()
  

###### plotting for graphs
        
## plotting the Prices
print("\n\n*** The Graphical representation of Prices across Hotels ***\n\n")   
# x-coordinates of left sides of bars  
x = [i for i in range(20)] 
# y co-ordinates
y = sort_price['Price']
# labels for bars
tick_label = sort_price['Hotels'] 
# plotting a bar chart
plt.bar(x, y, tick_label = tick_label,
        width = 0.8, color = ['red', 'green']) 
# naming the x-axis
plt.xlabel('Hotels')
# naming the y-axis
plt.ylabel('Prices')
# plot title
plt.title('Hotel Prices')
#rotating the titles
plt.xticks(rotation = 90)
# function to show the plot
plt.show() 

#plotting the Ratings
print("\n\n*** The Graphical representation of Prices across Hotels ***\n\n")  
# x-coordinates of left sides of bars  
x = [i for i in range(20)] 
# y co-ordinates or the heights of bars
y = sort_rating['Ratings']
# labels for bars
tick_label = sort_price['Hotels'] 
# plotting a bar chart
plt.bar(x, y, tick_label = tick_label,
        width = 0.8, color = ['red', 'green']) 
# naming the x-axis
plt.xlabel('Hotels')
# naming the y-axis
plt.ylabel('Ratings')
# plot title
plt.title('Hotel Ratings')
#rotating the titles
plt.xticks(rotation = 90)
# function to show the plot
plt.show() 

#### Option1 Generating the Minimum Price Option for a person in London

#minimum price per day for the hotel
min_price = sort_price.iloc[0]['Price']

#hotel corresponding to that price
min_hotel = sort_price.iloc[0]['Hotels']

#cheapest hotels
sort_rating.iloc[0:3]

## calculating the bare minimum per day fixed cost for being in the City
perday_expense = df_expenses.loc[0]['Prices in GBP'] + df_expenses.loc[44]['Prices in GBP'] +df_expenses.loc[31]['Prices in GBP'] +df_expenses.loc[45]['Prices in GBP'] +df_expenses.loc[46]['Prices in GBP']
items_included = [df_expenses.loc[0]['Item'], df_expenses.loc[44]['Item'], df_expenses.loc[31]['Item'], df_expenses.loc[45]['Item'], df_expenses.loc[46]['Item']]

#sorting by prices for the leisure activities in the city
sort_activities = df_leisure_activities.sort_values(by ='Prices in GBP-M')

#calculating the sum of at least three activities in the city
leisure_sum = sort_activities.iloc[0:3]['Prices in GBP-M'].sum()

#corresponding activities
activities = sort_activities.iloc[0:3]['Leisure_Activity']
activities = activities.tolist()

#the minimum requries amount per day per person for the city
minimum_amount = min_price + perday_expense + leisure_sum

items_included.append(activities)

s0 = "\n\nThe mean Price of a room per person in hotels in London on the dates entered by you is ** {:>7.2f} GBP **".format(sort_price['Price'].mean())

s1 = "Thank you for choosing Pocket Travel,\n\n*** Option # 1 ***\n\nThe cheapest price per person per day for traveling in London is ** {:>7.2f} GBP **".format(minimum_amount)

s2 = "It includes the hotel ** {:s} ** in London".format(min_hotel)

s3 = "Plus, it covers the following activities in London:\n** {:s},\n** {:s},\n** {:s},\n** {:s},\n** and {:s}".format(*items_included[:5])

s4 = "Additionally, it includes visits to the following places:\n** {:s},\n** {:s},\n** and, {:s}".format(*items_included[5])

print(s0 + "\n\n" + s1 + "\n \n" + s2 + "\n\n" + s3 + "\n\n" +s4)    


#### Option 2 : the best possible option
best_rating = sort_rating.iloc[0]['Ratings']
best_hotel =  sort_rating.iloc[0]['Hotels']
best_price = sort_rating.iloc[0]['Price']

perday_expense_best = perday_expense + df_expenses.loc[43]['Prices in GBP'] + df_expenses.loc[42]['Prices in GBP']
best_activities = [df_expenses.loc[43]['Item'] , df_expenses.loc[42]['Item']]

leisure_sum_best = leisure_sum + sort_activities.iloc[3:8]['Prices in GBP-M'].sum()
leisure_best = sort_activities.iloc[3:8]['Leisure_Activity'].tolist()
best_amount = best_price + perday_expense_best + leisure_sum_best

s1 = "\n\n*** Option # 2 ***\n\nThe Best price per person per day for traveling in London is{:>7.2f} GBP".format(best_amount)

s2 = "It includes the hotel ** {:s} ** in London, which has the highest rating of {:>3.1f}".format(best_hotel,best_rating)

s3 = "Plus, In addition to the activities in Option #1 it covers the following activities in London:\n**{:s},\n**and, {:s}".format(*best_activities)

s4 = "Also, apart from the leisure activities covered in the Option#1 it includes visits to the following places:\n**{:s},\n**{:s},\n**{:s},\n**{:s}\n** and, {:s}".format(*leisure_best)

print( s1 + "\n \n" + s2 + "\n\n" + s3 + "\n\n" +s4)

#### Option 3:
# based on user's input suggest him the final option
print("\n\n*** Pocket Travel's Recommendation ***\n\n")
if amount < minimum_amount:
    print("Hi! Unfortunately, the minimum amount recommended per day needed to visit London is ** {:>7.2f} GBP **, while you have mentioned only ** {:>7.2f} GBP **".format(minimum_amount, amount))
elif amount >= best_amount:
    print("Hi Congratulations!! You can avail our best option available that is Option #2, and still would have ** {:>7.2f} GBP ** left to enjoy your trip. ".format(amount-best_amount))
else:
    print("Hi Congratulations!! You can avail our basic Option #1, and still would have ** {:>7.2f} GBP ** left to enjoy your trip. ".format(amount-minimum_amount))





