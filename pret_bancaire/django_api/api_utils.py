# connexion à l'API et demande de pret
import requests
from dotenv import load_dotenv
import os
import json


load_dotenv(dotenv_path="../../.env")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")



class API_Requests() : 
    pass


def account_activation(email : str, new_password : str, confirm_password : str) : 
    url = f"http://localhost:8080/auth/activation/{email}"
    
    headers = {
        'accept' : 'application/json', 
        'Content-Type' : 'application/json'
    }
    
    data = {
        "new_password": new_password,
        "confirm_password": confirm_password
    }
    requete = requests.post(url = url, headers = headers, data = data)
    
    return requete.content["message"]


# def get_token(self, user_name, password) :
def get_token(email = EMAIL, password = PASSWORD) :
    url = 'http://localhost:8080/auth/login'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'password',
        'username': email,
        'password': password,
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string'
    }
    
    response = requests.post(url = url, headers = headers, data = data)
    if response.status_code == 200 :
        response_dict = json.loads(response.content.decode("utf-8"))
        return response_dict["access_token"]
    # return response


def loan_request_to_api(donnees : dict) : 
    
    token = get_token()
        
    url = "http://127.0.0.1:8080/loans/request"
    
    headers = {
        'accept': 'application/json',
        "Authorization": f"Bearer {token}",
        'Content-Type' : 'application/json'
    }
    json_data = json.dumps(donnees)
    response = requests.post(url = url, headers = headers, data = json_data)
    
    if response.status_code == 200 :
        reponse_dict = json.loads(response.content.decode("utf-8"))
        return reponse_dict["resultat"]
    return type(response)




# def api_errors(self, response):
#     if response.status_code == 401:
#         # Token expiré ou invalide
#         return "Session_expirée reconnectez-vous"


if __name__ == "__main__" :
    # token = get_token(email, password)
    
    data = {
    "ApprovalFY": 2008,
    "Bank": "BBCN BANK",
    "BankState": "CA",
    "City": "SPRINGFIELD",
    "CreateJob": 2,
    "DisbursementGross": 20000,
    "FranchiseCode": 1,
    "GrAppv": 20000,
    "LowDoc": 0,
    "NAICS": 453110,
    "NewExist": 1,
    "NoEmp": 4,
    "RetainedJob": 250,
    "RevLineCr": 0,
    "State": "TN",
    "Term": 6,
    "UrbanRural": 1,
    "Zip": 37172
    }
    
    print(loan_request_to_api(donnees = data))
