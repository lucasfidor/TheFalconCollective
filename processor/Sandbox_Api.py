import requests
import json
import random, string
global access_token
global accountID
global externalUID
global permission
global internalTransferID
global externalTransferID
from processor import config

class SandboxApi:

    ###########################
    ##### API STARTS HERE #####
    ###########################

    _authorization_code = ""


    def get_authorization(self, id, secret, code):
        url = "http://apm.sandboxpresales.fidorfzco.com/oauth/token"

        querystring = {"grant_type": "authorization_code",
                       "client_id": id,
                       "client_secret": secret,
                       "code": code,
                       "redirect_uri": "http://localhost:3005"}

        headers = {}

        response = requests.request("POST", url, headers=headers, params=querystring)
        access_token = str(response.text).split("\"")[3]
        return access_token

    def get_customers(self):
        url = config.api_url + "/fidor_banking/customers"

        payload = ""
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + config.access_token,
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }
        print(headers)
        response = requests.request("GET", url, data=payload, headers=headers)

        return response.text

    def get_accounts(self, token):
        url = config.api_url + "/fidor_banking/accounts"

        headers = {
            'Authorization': "Bearer " + str(token),
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

    def get_current_user(self):
        url = config.api_url + "/fidor_banking/users/current"

        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Accept': "application/vnd.fidor.de; version=1,text/json",
            'Content-Type': "application/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

    def post_internal_transfer(self, token, origin, receiver, external, amount, subject):
        url = config.api_url + "/fidor_banking/internal_transfers"

        payload = {"account_id": origin, "receiver": receiver, "external_uid": external, "amount": amount, "subject": subject}
        payloadRaw = json.dumps(payload)
        headers = {
            'Authorization': "Bearer " + token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("POST", url, data=payloadRaw, headers=headers)
        return response

    def get_internal_transfer(self):
        url = config.api_url + "/fidor_banking/internal_transfers"

        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Accept': "application/vnd.fidor.de; version=1,text/json",
            'Content-Type': "application/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

    def get_internal_transfer_by_id(self):
        url = config.api_url + "/fidor_banking/internal_transfers/8"

        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

    def post_external_transfer(self, token):
        url = config.api_url + "/fidor_banking/sepa_credit_transfers"

        payload = "{\n  \"account_id\" : \"19394998\",\n  \"external_uid\" : \"666ifgftdfffrsdtsfgjuh\",\n  \"remote_iban\": \"GB33BUKB20201555555555\",\n  \"remote_bic\": \"FDDODEMMXXX\",\n  \"remote_name\" : \"test test\",\n  \"amount\" : 100,\n  \"subject\" : \"Here is your dirty money\"\n}"
        headers = {
            'Authorization': "Bearer " + token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.text

    def get_external_transfer(self):
        url = config.api_url + "/fidor_banking/sepa_credit_transfers"

        payload = ""
        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("GET", url, data=payload, headers=headers)

        return response.text

    def get_external_transfer_by_id(self):
        url = config.api_url + "/fidor_banking/sepa_credit_transfers/1"

        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text
    def get_pre_auths(self):
        url = config.api_url + "/fidor_banking/preauths"

        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

    def get_transactions(self):
        url = config.api_url + "/fidor_banking/transactions"

        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

    def get_transactions_by_id(self):
        url = config.api_url + "/fidor_banking/transactions/11"

        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

#api = SandboxApi()
#print(api.post_internal_transfer("1uEWCen5oSC3ZGRdI5VMfL:3cSJtMTziW6LQn9a7wmM6t", "90923694", "54012762", "883151gdg883183", 10, ""))
#print(api.get_code())
#print(api.get_authorization())
#print(api.get_accounts())