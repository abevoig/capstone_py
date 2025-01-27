from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")


#find your right key here
table = soup.find('table', attrs={'class':'history-rates-data'})
row = table.find_all('span', attrs={'class': 'nowrap'})
table.find_all('span', attrs={'class': 'nowrap'})
row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length, 6):
#insert the scrapping process here
    # Scraping process
    # Date
    date = table.find_all('span', attrs={'class': 'nowrap'})[i].text
    date = date.strip()
    # Exchange Rate
    exchange = table.find_all('span', attrs={'class': 'nowrap'})[i+4].text
    exchange = exchange.strip().replace(' IDR', '')

    temp.append((date, exchange))
temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns=['Date', 'Exchange Rate'])

#insert data wrangling here
data['Date'] = pd.to_datetime(data['Date'])
data['Exchange Rate'] = data['Exchange Rate'].str.replace(',', '')
data['Exchange Rate'] = data['Exchange Rate'].astype(float)
data.dtypes

#end of data wranggling 
data = data.set_index('Date')

@app.route("/")
def index(): 
	
	card_data = f'{data["Exchange Rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
    
	ax = data.plot(figsize = (10,9)) 
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)