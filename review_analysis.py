import json
import os

api_script_path = "AmazonReviewAPI\\app.py"

def make_review_array():
    rc_json = open("review_contents.json")
    review_content = json.load(rc_json)
    print("hello")
    print(review_content['product_title'])




if __name__ == "__main__":
    os.system('python ' + api_script_path)
    
    make_review_array()

