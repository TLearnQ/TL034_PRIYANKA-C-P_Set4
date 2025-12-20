import requests

def check_user_id_numeric():
    url = "https://reqres.in/api/users"

    headers = {
        "Authorization": "Bearer reqres-token",
        "Content-Type": "application/json"
    }
    payload = {
        "name": "cypher",
        "job": "traitor"
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    print("API Response:", data)
    user_id = data.get("id")

    if user_id and str(user_id).isnumeric():
        return True
    else:
        return False

print(check_user_id_numeric())
