import math

# PATHS
# src
api_script_path = "\\src\\app.py"
gpt_analysis_path = "\\src\\TextAnalysis.py"
selectors_amazon_path = "\\src\\PageSelectors\\selectors-Amazon.yml"
requirements_path = "\\requirements.txt"

# data
review_contents_json = '\\data\\review_contents.json'

# VARIABLES
# api key
api_key = "insert"

# review scraping
review_retrieve_count = 20
review_per_pages = 10
num_pages_retrieve = math.ceil(review_retrieve_count / review_per_pages)

# FUNCTIONS

def get_api_script_path():
    return api_script_path

def get_gpt_analysis_path():
    return gpt_analysis_path

def get_selectors_amazon_path():
    return selectors_amazon_path

def get_review_contents_path():
    return review_contents_json

def get_requirements_path():
    return requirements_path

def get_api_key():
    return api_key

def get_num_pages_retrieve():
    return num_pages_retrieve