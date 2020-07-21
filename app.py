import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, request
from flask_cors import cross_origin

# The app is deployed on both heroku & pivotal, and following are the respective urls:
# https://web-scrapper-nse-stock-price.herokuapp.com/
# http://livestockprice-hilarious-fox-xq.cfapps.io/

# Since the project involves fetching lve data, the creation on MongoDB database seemed futile and hence I 
# avoided it. I confirmed the same with iNeuron support team.


# Since NSE search bar requires either company symbol or the registered name of the company, I am going ahead
# with asking for company symbol as user Input, as there are less chances of error. What I mean is that even if
# you use the mapping of  company name with company symbols then also user will be required to enter the
# exact name with which company is registered with NSE and hence there would be bigger chance of giving the
# wrong input than if the user enters just the company symbol [lesser the words, lesser the chance of mistake]

app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/StockInfo', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")  # To deal with leading/lagging spaces
            stock_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' \
                        + searchString  # Takes to the NSE page with live/latest stock price for the company
            # print(stock_url)
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/79.0.3945.117 Safari/537.36'}  # User Agent String
            response = requests.get(stock_url, headers=headers)  # Requesting access to web page
            soup = bs(response.text, 'html.parser') #
            data_array = soup.find(id='responseDiv').getText().strip().split(":")
            # Extracting the relevant portion of html and converting it in list format [I am more adept at
            # working with lists than dictionaries]. Now the erstwhile key value pairs have turned into adjacent
            # elements in the list

            Stock_Info = {'Company Symbol': searchString, 'Latest Price': 'No Latest Price', 'Change': 'No Change',
                          'Percent Change': 'Percent Change',
                          'Highest Price Today': 'No Highest Price of Today',
                          'Lowest Price Today': 'No Lowest Price of Today',
                          'Opening Price': 'No Opening Price', 'Pr. Closing Price': 'No Pr. Closing Price'}
            # Creating a dictionary with default values. If the info for relevant fields(here keys) are present
            # for the given company then they would be updated in the below code block (for loop block),
            # otherwise the keys would retain their default values.

            for item in data_array:

                if 'dayLow' in item:
                    index = data_array.index(item) + 1
                    Lowest_Price_Today = data_array[index].split('"')[1]
                    Stock_Info['Lowest Price Today'] = Lowest_Price_Today

                if 'dayHigh' in item:
                    index = data_array.index(item) + 1
                    Highest_Price_Today = data_array[index].split('"')[1]
                    Stock_Info['Highest Price Today'] = Highest_Price_Today

                if 'pChange' in item:
                    index = data_array.index(item) + 1
                    Percent_Change = data_array[index].split('"')[1]
                    Stock_Info['Percent Change'] = Percent_Change + ' %'

                if 'change' in item:
                    index = data_array.index(item) + 1
                    Change = data_array[index].split('"')[1]
                    Stock_Info['Change'] = Change

                if 'previousClose' in item:
                    index = data_array.index(item) + 1
                    Yesterdays_Closing_Price = data_array[index].split('"')[1]
                    Stock_Info['Pr. Closing Price'] = Yesterdays_Closing_Price
                    # Closing price is only available once the market closes for the day. Hence previous day's
                    # closing price is used

                if 'open' in item:
                    index = data_array.index(item) + 1
                    Opening_Price = data_array[index].split('"')[1]
                    Stock_Info['Opening Price'] = Opening_Price

                if 'lastPrice' in item:
                    index = data_array.index(item) + 1
                    Latest_Price = data_array[index].split('"')[1]
                    Stock_Info['Latest Price'] = Latest_Price

            return render_template('results.html', Stock_Info=Stock_Info)
        except Exception as e:
            print('The Exception message is: ', e) # To identify what went wrong in try block
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)
