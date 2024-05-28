from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt

class bamboo:

    def __init__(self,link):
        self.link = link

    def bamboo_price(url = 'https://bamboohousing.ca/homepage'): #returns a list of prices of all the listings on the current page
        l=[]
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        houses = soup.find_all('p', class_ = 'mobiletitle')
        for house in houses:
            price = house.find('b').text
            price=(((price.split('$'))[1]).split(' '))[0]
            l.append(int(price))
        #print(l)
        return l

    def pages_bamboo(): #returns the total number of pages
        html_text = requests.get('https://bamboohousing.ca/homepage').text
        soup = BeautifulSoup(html_text,'lxml')
        paginate = soup.find('div',class_="ui center aligned container paginate").text
        paginate = ((paginate.split('of')[-1]).split(' '))[1]
        #print(paginate)
        return (int(paginate))
    
    def url_changer(): #returns a list of urls for the different page numbers
        l=[]
        pages = bamboo.pages_bamboo()
        link = "https://bamboohousing.ca/homepage?StartTerm=&RoomsAvailable=&Coed=&Ensuite=&LeaseType=&Price=&Sort=Recent"
        #https://bamboohousing.ca/homepage?page=2&RoomsAvailable=&Coed=&StartTerm=&Ensuite=&LeaseType=&Price=&Sort=Recent
        for i in range(2,pages+1):
            url_elements = link.split('StartTerm=',1)
            url = url_elements[0]+f'page={i}'+url_elements[1]
            print(url)
            l.extend(bamboo.bamboo_price(url))
        return l






class kjiji:
    def __init__(self,link):
        self.link=link
    
    def kjiji_price(url = 'https://www.kijiji.ca/b-short-term-rental/kitchener-waterloo/c42l1700212' ):  #returns a list of prices of all the listings on the current page
        l=[]
        headers = {
            'Referer': 'https://www.example.com',  # Replace with the actual referer URL
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        html_text=requests.get(url, headers = headers).text
        soup = BeautifulSoup(html_text, 'lxml')
        houses = soup.find_all('div', class_ = "sc-4cd8c886-0 fkzIce")
        #print(houses)
        for house in houses:
            price = house.find('p').text
            #print(price)
            price = price.split('$')
            try:
                price = (price[1]).split('.')
                        #print(price)
            except IndexError:
                    price='NA'
                    #print(price)
                    continue
            try:
                price = price[0].split(',')
                price = price[0]+price[1]
                l.append(int(price))
                #print(price)
            except IndexError:
                l.append(int(price[0]))
                #print(price[0])
        #print(l)
        #print(len(l))
        return l
    
    def pages_kjiji():  #returns the total number of pages
        headers = {
            'Referer': 'https://www.example.com',  # Replace with the actual referer URL
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        html_text=requests.get('https://www.kijiji.ca/b-short-term-rental/kitchener-waterloo/c42l1700212', headers = headers).text
        soup=BeautifulSoup(html_text, 'lxml')
        try:
            pages=(soup.find('div', 'sc-fa75c125-0 YhqUg').text).split('Next')[0][-1]
        except AttributeError:
            pages=1
        #print(pages)
        return(int(pages))

    def total_listings_kjiji():
        html_text=requests.get('https://www.kijiji.ca/b-short-term-rental/kitchener-waterloo/c42l1700212').text
        soup=BeautifulSoup(html_text, 'lxml')
        listings=(soup.find('h2').text).split('of ')[-1]
        print(listings)
        return int(listings)
    
    def url_changer(): #calls price function with different urls corresponding to the different page numbers and returns a list of all the prices
        l=[]
        pages=kjiji.pages_kjiji()
        link='https://www.kijiji.ca/b-short-term-rental/kitchener-waterloo/c42l1700212'
        for i in range(2,pages+1):
            url_elements=link.split('waterloo',1)
            url=url_elements[0]+f'waterloo/page-{i}'+url_elements[1]
            print(url)
            l.extend(kjiji.kjiji_price(url))
        return l
    


def bar(bamboo,kjiji):
    x=["bamboo","kjiji"]
    y=[bamboo,kjiji]
    return plt.bar(x,y)

def hist(website):
    return plt.hist(website)

bamboo_price_list = bamboo.bamboo_price() + bamboo.url_changer()
kjiji_price_list = kjiji.kjiji_price() + kjiji.url_changer()


bamboo_price_avg = np.mean(bamboo_price_list)
kjiji_price_avg = np.mean(kjiji_price_list)
avg_prices = [bamboo_price_avg,kjiji_price_avg]

num_listings = [len(bamboo_price_list), len(kjiji_price_list)]

platforms = ["Bamboo", "Kjiji"]

fig, axs = plt.subplots(2, 3, figsize=(18, 10))

# Avg Price
axs[0,0].bar(platforms, avg_prices, color=['green', 'purple'])
axs[0,0].set_title('Avg Price Comparison')
axs[0,0].set_xlabel('Platforms')
axs[0,0].set_ylabel('Avg Price')

# Total listings
axs[1,0].bar(platforms, num_listings, color=['green', 'purple'])
axs[1,0].set_title('Total Listings')
axs[1,0].set_xlabel('Platforms')
axs[1,0].set_ylabel('Number of Listings')

# Bamboo Histogram
axs[0,1].hist(bamboo_price_list, bins=30, color='green', alpha=0.7)
axs[0,1].set_title('Bamboo Price Variation')
axs[0,1].set_xlabel('Value')
axs[0,1].set_ylabel('Frequency')

# Kjiji Histogram
axs[1,1].hist(kjiji_price_list, bins=30, color='purple', alpha=0.7)
axs[1,1].set_title('Kjiji Price Variation')
axs[1,1].set_xlabel('Value')
axs[1,1].set_ylabel('Frequency')

# Bamboo Boxplot
axs[0,2].boxplot(bamboo_price_list)
axs[0,2].set_title('bamboo price variance')
axs[0,2].set_ylabel('prices')

# Kjiji Boxplot
axs[1,2].boxplot(kjiji_price_list)
axs[1,2].set_title('kjiji price variance')
axs[1,2].set_ylabel('prices')

plt.show()