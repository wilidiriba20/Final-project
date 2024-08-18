import requests

API_KEY = "0450b5cf0fbc459c9b131e76f89580b1"  # Replace with your actual API key
def image(diet,intolerances,query="pasta"):
    url = " https://api.spoonacular.com/recipes/complexSearch"


    params = {
        "apiKey": API_KEY,
        "number":5,
        "diet" : diet,
        "intolerances":intolerances,    
        "query":query
    }

    response = requests.get(url, params=params)
    data= response.json()



    id_list = [item["id"] for item in data["results"]]
    url_list=[]

    for recipe_id in id_list:
        url1 = f"https://api.spoonacular.com/recipes/{recipe_id}/card" 
        params = {
            "apiKey": API_KEY,
            "mask":"ellipseMask",
            "backgroundColor":"ffffff",
            "fontColor":"333333",
            "instructionsRequired":"true"  # Include instructions
        }

        response = requests.get(url1, params=params)
        response = response.json()
        url_list.append(response)

    return url_list
# Assuming a function to check if image is saved
def check_if_image_saved(user_id, image_url):
    # Replace with your database query to check if image exists for the user
    result = db.execute("SELECT * FROM saved_images WHERE user_id = :user_id AND image_url = :image_url", user_id=user_id, image_url=image_url)
    return len(result) > 0


   