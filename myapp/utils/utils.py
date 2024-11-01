import re
from firebase import firebase
config = {
    "apiKey": "AIzaSyAjimJxm2UZHP7L5rHIpAdBIWlDr2_NFKs",
    "authDomain": "news-in-briefs-db.firebaseapp.com",
    "databaseURL": "https://news-in-briefs-db-default-rtdb.firebaseio.com",
    "storageBucket": "news-in-briefs-db.appspot.com"
}

def createPostslug(text):
    # Replace any non-alphanumeric character (symbols, spaces, etc.) with a hyphen
    return re.sub(r'[^a-zA-Z0-9]', '-', text)

def get_categories():
        firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)
        try:
            categories = firebaseconn.get('NewsCategories', None)

            # If categories are in list format, filter out None values
            if isinstance(categories, list):
                categories = [category for category in categories if category is not None]
                return {str(index): category for index, category in enumerate(categories)}
            elif isinstance(categories, dict):
                return {str(key): value for key, value in categories.items() if value is not None}
            
            return {}  # Return an empty dictionary if categories is None or not a dict
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return {}  # Return an empty dictionary on error
