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

    #oauth/authorize?client_id=d2463025f42ca58f&redirect_uri=http://localhost:3005&response_type=code&state=approved
    #Code: bd511468979f630bb3f3f1701a58c297

    def get_code(self):
        url = config.sandbox_url + config.auth_url
        print(url)
        r = requests.get(url)
        redirect = str(r.url)
        print(url)
        # code = redirect.split("?code=")[1].split("&")[0]
        #
        # with open("config.py", "r") as configFile:
        #     data = configFile.read()
        # configFile.close()
        #
        # data = data.split("\n")
        # newData = ""
        #
        # for item in data:
        #     if (item.split("=")[0] == "code"):
        #         newData = newData + "code=\"" + str(access_token) + "\"\n"
        #     else:
        #         newData = newData + item + "\n"
        #
        # with open("config.py", "w") as configFile:
        #     configFile.write(newData)
        # configFile.close()
        #
        # return code


    def get_authorization(self):
        url = "http://apm.sandboxpresales.fidorfzco.com/oauth/token"

        querystring = {"grant_type": "authorization_code",
                       "client_id": "d2463025f42ca58f",
                       "client_secret": "9d1adff976b667eb946f2248d170cc95",
                       "code": config.code,
                       "redirect_uri": "http://localhost:3005"}

        headers = {}

        response = requests.request("POST", url, headers=headers, params=querystring)
        access_token = str(response.text).split("\"")[3]

        with open("config.py", "r") as configFile:
            data = configFile.read()
        configFile.close()

        data = data.split("\n")
        newData = ""

        for item in data:
            if (item.split("=")[0] == "access_token"):
                newData = newData + "access_token=\"" + str(access_token) + "\"\n"
            else:
                newData = newData + item + "\n"

        with open("config.py", "w") as configFile:
            configFile.write(newData)
        configFile.close()

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

    def get_accounts(self, auth):
        url = config.api_url + "/fidor_banking/accounts"

        headers = {
            'Authorization': "Bearer " + str(auth),
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

    def post_internal_transfer(self):
        url = config.api_url + "/fidor_banking/internal_transfers"

        payload = "{\n  \"account_id\": \"19394998\",\n  \"receiver\": \"67152831\",\n  \"external_uid\": \"9ur64fgdg355iu8\",\n  \"amount\": \"1000\",\n  \"subject\": \"my share of yesterday evening\"\n}"
        headers = {
            'Authorization': "Bearer " + config.access_token,
            'Content-Type': "application/json",
            'Accept': "application/vnd.fidor.de; version=1,text/json"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.text

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

    def post_external_transfer(self):
        url = config.api_url + "/fidor_banking/sepa_credit_transfers"

        payload = "{\n  \"account_id\" : \"19394998\",\n  \"external_uid\" : \"666ifgftdfffrsdtsfgjuh\",\n  \"remote_iban\": \"GB33BUKB20201555555555\",\n  \"remote_bic\": \"FDDODEMMXXX\",\n  \"remote_name\" : \"test test\",\n  \"amount\" : 100,\n  \"subject\" : \"Here is your dirty money\"\n}"
        headers = {
            'Authorization': "Bearer " + config.access_token,
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

api = SandboxApi()
#print(api.get_code())
#print(api.get_authorization())
#print(api.get_accounts())