import pickle
from django.shortcuts import render,redirect
from firebase import firebase
import requests  # Import requests to catch HTTPError
from .utils.utils import createPostslug,get_categories

from django.http import HttpRequest,JsonResponse
config = {
    "apiKey": "AIzaSyAjimJxm2UZHP7L5rHIpAdBIWlDr2_NFKs",
    "authDomain": "news-in-briefs-db.firebaseapp.com",
    "databaseURL": "https://news-in-briefs-db-default-rtdb.firebaseio.com",
    "storageBucket": "news-in-briefs-db.appspot.com"
}

def updateshorts(request):
    
    def add_news(title, headline, summary, image_url, news_url, category):
        firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)

        # Retrieve existing news to determine the next ID
        result = firebaseconn.get('/News', None)
        total_count = len(result) if isinstance(result, dict) else 0  # Count total existing entries

        # Create a new ID with a prefix of '-'
        new_id = str(-total_count - 1)  # Decrement the count to get the new ID

        # Create a dictionary to hold news data
        news_data = {
            "title": title,
            "headline": headline,
            "summary": summary,
            "image_url": image_url,
            "news_url": news_url,
            "post_slug":createPostslug(title),
            "category": category  # Add category to news data
        }
        
        # Save the news data with the determined ID
        firebaseconn.put('/News', new_id, news_data)

        return True  # Indicate successful addition

    def add_ads(banner_ad_image_1, banner_ad_image_2, banner_ad_image_3):
        firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)

        # Create a dictionary to hold ad data
        ad_data = {
            "banner_ad_image_1": banner_ad_image_1,
            "banner_ad_image_2": banner_ad_image_2,
            "banner_ad_image_3": banner_ad_image_3
        }
        
        # Save the ad data with the determined ID
        firebaseconn.put('/Ads', "BannerAdsURLs", ad_data)

        return True  # Indicate successful addition

    def add_category(category_name):
        firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)
        
        # Retrieve existing categories
        categories = firebaseconn.get('NewsCategories', None)

        # Ensure that categories is a dictionary
        if not isinstance(categories, dict):
            categories = {}

        # Check if the category already exists
        if category_name in categories.values():
            return False  # Indicate that the category already exists

        # Retrieve the last used category ID from Firebase
        last_id = firebaseconn.get('LastCategoryId', None)
        last_id = int(last_id) if last_id else 0  # Convert to integer if it exists

        # Increment the last ID by 1 to get the new category ID
        new_id = str(last_id + 1)

        # Add the new category with the new ID
        categories[new_id] = category_name

        # Save the new category to Firebase
        firebaseconn.put('NewsCategories', new_id, category_name)

        # Update the last used category ID in Firebase
        firebaseconn.put('/', 'LastCategoryId', new_id)  # Update LastCategoryId node

        return True  # Indicate that the category was added successfully

    
    def get_news():
        firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)
        try:
            news = firebaseconn.get('/News', None)
            return news if isinstance(news, dict) else {}  # Return news as a dict
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return {}  # Return an empty dictionary on error

    # Initialize context variables
    context = {}

    if request.method == "POST":
        if 'add_category' in request.POST:
            new_category = request.POST.get("new_category")
            if new_category:
                category_added = add_category(new_category)
                context['category_added'] = category_added  # Store category added status

        Title = request.POST.get("title")
        Headline = request.POST.get("headline")
        Summary = request.POST.get("summary")
        ImageUrl = request.POST.get("imageurl")
        NewsUrl = request.POST.get("newsurl")

        if 'post_news' in request.POST:
            category = request.POST.get("category")  # Retrieve selected category
            news_added = add_news(Title, Headline, Summary, ImageUrl, NewsUrl, category)
            context['news_added'] = news_added  # Store news added status

        # Handle posting ads
        AdTitle = request.POST.get("ad_title")
        AdDescription = request.POST.get("ad_description")
        AdImage = request.POST.get("ad_image")

        if 'post_ads' in request.POST:
            BannerAdImage1 = request.POST.get("banner_ad_image_1")
            BannerAdImage2 = request.POST.get("banner_ad_image_2")
            BannerAdImage3 = request.POST.get("banner_ad_image_3")
            
            print(f"Banner Ad Images: {BannerAdImage1}, {BannerAdImage2}, {BannerAdImage3}")  # Debug output
            
            ads_added = add_ads(BannerAdImage1, BannerAdImage2, BannerAdImage3)
            context['ads_added'] = ads_added  # Store ads added status

    # Fetch updated categories, ads, and news after handling POST requests
    context['categories'] = get_categories()
    context['news'] = get_news()  # Retrieve news for the context
    context['categories_message'] = "No categories found." if not context['categories'] else ""
    context['news_message'] = "No news found." if not context['news'] else ""  # Message if no news found

    return render(request=request, template_name='updateshorts.html', context=context)


def ShoweditPost(request:HttpRequest):

    post_id = request.POST.get("post_id")
    firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)
    data = firebaseconn.get("/News",post_id)

    print(data)
    context = {}
    context["news"] = data
    context['categories'] = get_categories()
    context["post_id"] = post_id
    return render(request=request,template_name="editPosts.html",context=context)

def editPost(request:HttpRequest):
    Title = request.POST.get("title")
    Headline = request.POST.get("headline")
    Summary = request.POST.get("summary")
    ImageUrl = request.POST.get("imageurl")
    NewsUrl = request.POST.get("newsurl")
    post_id = request.POST.get("post_id")
    Category = request.POST.get("category")
    print(request.POST)
    
    firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)
    news_data = {
            "title": Title,
            "headline": Headline,
            "summary": Summary,
            "image_url": ImageUrl,
            "news_url": NewsUrl,
            "post_slug":createPostslug(Title),
            "category": Category  # Add category to news data
    }
    firebaseconn.put(f"/News",post_id,news_data)
    return redirect("/")
    
