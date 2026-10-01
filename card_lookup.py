import httpx

def card_find(code):
    BASE_URL = "https://api.gcgapi.com/v1/cards/"

    request = httpx.get(BASE_URL + code.upper())

    if request.status_code == 200:

        card = request.json()

        card_data = {"Name": card["data"]["name"],
                    "Code": card["data"]["card_number"],
                    "Effect": card["data"]["effect"],
                    "Image_Url": card["data"]["image_url"]}

        return card_data
    else:
        return None