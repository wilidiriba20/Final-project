import requests

API_KEY = "0450b5cf0fbc459c9b131e76f89580b1"  # Replace with your actual API key

url = " https://api.spoonacular.com/recipes/complexSearch"


params = {
    "apiKey": API_KEY,
    "number":10,
    "diet" : "vegan",
    "excludeCuisine" : "greek",
    "intolerances":"gluten",
    
    "query":"pasta"
}

response = requests.get(url, params=params)
data= response.json()



# Assuming the dictionary is loaded into a variable named `data`

# Access the "results" list where the IDs are located
id_list = [item["id"] for item in data["results"]]
url_list=[]

for recipe_id in id_list:
  url = f"https://api.spoonacular.com/recipes/{recipe_id}/card"  # Use f-string for URL formatting

  params = {
      "apiKey": API_KEY,
      "mask":"ellipseMask",
      "backgroundColor":"ffffff",
      "fontColor":"333333",
      "instructionsRequired":"true"  # Include instructions
  }

  response = requests.get(url, params=params)
  response = response.json()
  url_list.append(response)
