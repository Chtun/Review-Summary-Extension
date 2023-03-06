# api, scraper, data imports
from flask import Flask, request, jsonify, session
import selectorlib
import requests
import os
from dateutil import parser as dateparser
import json

# system
import sys, subprocess
# adding cwd to the system path to access variables
sys.path.insert(0, os.getcwd())
import variables

# Flask and Extractor variables
app = Flask(__name__)
extractor = selectorlib.Extractor.from_yaml_file(os.getcwd() + variables.get_selectors_amazon_path())

# For number of pages to retrieve
retrieve_pages = variables.get_num_pages_retrieve()

# Scrape page to find product review page
def scrape_product_review_url(url):

    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    data = extractor.extract(r.text,base_url=url)
    if not("/dp/" in url):
        return None
    if (data['product_review_link'] != None):
        return data['product_review_link']
    print("No product review link found")
    return None



# Scrape product review page for information
def scrape(url):    
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    data = extractor.extract(r.text,base_url=url)
    if(data['other_country'] != None):
        return
    if(data['reviews'] == None):
        return
    reviews = []
    for r in data['reviews']:
        r["product"] = data["product_title"]
        r['url'] = url
        if 'verified_purchase' in r:
            if r['verified_purchase'] == None:
                r['verified_purchase'] = False
            elif 'Verified Purchase' in r['verified_purchase']:
                r['verified_purchase'] = True
            else:
                r['verified_purchase'] = False
        r['rating'] = r['rating'].split(' out of')[0]
        date_posted = r['date'].split('on ')[-1]
        if r['images']:
            r['images'] = "\n".join(r['images'])
        r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
        reviews.append(r)
    histogram = {}
    for h in data['histogram']:
        histogram[h['key']] = h['value']
    data['histogram'] = histogram
    data['average_rating'] = float(data['average_rating'].split(' out')[0])
    data['reviews'] = reviews
    data['number_of_reviews'] = int(str((str(data['number_of_reviews'].split('ratings, ')[1]).replace(',','')).split(' with ')[0]).replace(',',''))
    return data 

# Append reviews to data from data_to_add, if the reviews exist
def append_reviews(data_to_add, data):
    if data_to_add['reviews']:
        for r in data_to_add['reviews']:
            data['reviews'].append(r)

# Only processes the top 20 reviews for each of the 5 star categories - up to 100 trust reviews in English processed in total
def quick_retrieve(data):
    data['reviews'] = []

    # If five star reviews exist, add its reviews to data
    if (data['five_star_link'] != None):
        next_data = scrape(data['five_star_link'])
        count = 0
        while(next_data != None and count < retrieve_pages):
            # If another page exists, add its reviews to data
            append_reviews(next_data, data)
            if (next_data['next_page'] != None):
                next_data = scrape(next_data['next_page'])
            else:
                next_data = None
            count += 1
    
    # If four star reviews exist, add its reviews to data
    if (data['four_star_link'] != None):
        next_data = scrape(data['four_star_link'])
        count = 0
        while(next_data != None and count < retrieve_pages):
            append_reviews(next_data, data)
            # If another page exists, add its reviews to data
            if (next_data['next_page'] != None):
                next_data = scrape(next_data['next_page'])
            else:
                next_data = None
            count += 1

    # If three star reviews exist, add its reviews to data
    if (data['three_star_link'] != None):
        next_data = scrape(data['three_star_link'])
        count = 0
        while(next_data != None and count < retrieve_pages):
            append_reviews(next_data, data)
            # If another page exists, add its reviews to data
            if (next_data['next_page'] != None):
                next_data = scrape(next_data['next_page'])
            else:
                next_data = None
            count += 1

    # If two star reviews exist, add its reviews to data
    if (data['two_star_link'] != None):
        next_data = scrape(data['two_star_link'])
        count = 0
        while(next_data != None and count < retrieve_pages):
            append_reviews(next_data, data)
            # If another page exists, add its reviews to data
            if (next_data['next_page'] != None):
                next_data = scrape(next_data['next_page'])
            else:
                next_data = None
            count += 1

    # If one star reviews exist, add them to data
    if (data['one_star_link'] != None):
        next_data = scrape(data['one_star_link'])
        count = 0
        while(next_data != None and count < retrieve_pages):
            append_reviews(next_data, data)
            # If another page exists, add its reviews to data
            if (next_data['next_page'] != None):
                next_data = scrape(next_data['next_page'])
            else:
                next_data = None
            count += 1

# Processes all trust reviews in English under a product
def deep_retrieve(data):
    next_page = data['next_page']
    count = 1
    while (next_page != None and count < 50):
        count += 1
        next_data = scrape(next_page)
        if next_data != None:
            for r in next_data['reviews']:
                data['reviews'].append(r)
            next_page = next_data['next_page']
        else:
            next_page = None
            break

# deletes empty or null data values
def format_data(data):
    for key, value in list(data.items()):
        if value is None:
            del data[key]
        elif isinstance(value, dict):
            format_data(value)
    return data


# Runs api requests when user changes link
@app.route('/')
def api():
    url = request.args.get('url',None)
    product_review_url = None
    
    if url:
        product_review_url = url
        if not('product-reviews' in url):
            print("Has to find product review page")
            product_review_url = scrape_product_review_url(url)
        else:
            print("already on product review page")
    
    if product_review_url:

        data = scrape(product_review_url)

        if data and data['number_of_reviews'] < 100:
            print("Deep retrieve")
            deep_retrieve(data)
        else:
            print("Quick retrieve")
            quick_retrieve(data)
        
        print("Finished retrieval")
        
        format_data(data)

        json_object = json.dumps(data, indent = 4)
        with open("review_contents.json", "w") as outfile:
            json.dump(data, outfile)


        subprocess.call([sys.executable, os.getcwd() + variables.get_gpt_analysis_path()])
        
        
        return jsonify(data)
    return jsonify({'error':'URL to scrape is not valid or provided'}),400

if __name__ == "__main__":
    app.run(debug=True)
