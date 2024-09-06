#Question 1. Build a Flask app that scrapes data from multiple websites and displays it on your site.
#You can try to scrap websites like youtube , amazon and show data on output pages and deploy it on cloud
#platform .

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_youtube(query):
    # Example URL - you will need to adjust to use the YouTube API or scraping techniques
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract video titles (this is a simplified example)
    videos = []
    for item in soup.find_all('h3', class_='title'):
        title = item.get_text()
        videos.append(title)
    return videos

def scrape_amazon(query):
    # Example URL - you will need to adjust to use the Amazon API or scraping techniques
    url = f"https://www.amazon.com/s?k={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract product titles (this is a simplified example)
    products = []
    for item in soup.find_all('span', class_='a-text-normal'):
        title = item.get_text()
        products.append(title)
    return products

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    youtube_results = scrape_youtube(query)
    amazon_results = scrape_amazon(query)
    return render_template('results.html', query=query, youtube_results=youtube_results, amazon_results=amazon_results)

if __name__ == '__main__':
    app.run(debug=True)