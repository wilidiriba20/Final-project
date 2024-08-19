import requests

API_KEY = "7ef29e09b940480fb1ea5069f13ccb7a"  # Replace with your actual API key
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

   