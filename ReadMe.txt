# Ths project can be broken down into 3 segments (1) Getting live stock prices from NSE India's website (2) Displaying the results in a UI (3) Deployment in cloud

# Following are the few discretions I took
# Since NSE search bar requires either company symbol or the registered name of the company, I went ahead with asking for company symbol as user Input, as there are less chances
# of   error. What I mean is that even if you use the mapping of  company name with company symbols then also user will be required to enter the exact name with which company is
# registered with NSE and hence there would be bigger chance of giving the wrong input than if the user enters just the company symbol [lesser the words, lesser the chance of 
# mistake]
# Since the project involves fetching lve data, the creation on MongoDB database seemed futile and hence I avoided it. I confirmed the same with iNeuron support team


# The app is deployed on both heroku & pivotal, and following are the respective urls:
# (1) https://web-scrapper-nse-stock-price.herokuapp.com/
# (2) http://livestockprice-hilarious-fox-xq.cfapps.io/

# However, I've uploaded the files corresponding to Heroku deployment only to avoid duplcity and hence the unnecessary confusion
