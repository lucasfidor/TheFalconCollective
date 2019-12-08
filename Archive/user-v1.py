from processor.webdriverfactory import WebDriverFactory
from processor import config
from processor.basepage import BasePage
from processor.Sandbox_Api import SandboxApi
import time
import json

class User(BasePage):
    def __init__(self, teleId):
        self.banking = SandboxApi()
        self.wdf = WebDriverFactory(config.browser)
        self.driver = ""
        super().__init__(self.driver)

        self.telegramID = str(teleId)
        self.username = ""
        self.email = ""
        self.password = "asdASD123!"
        self.first = ""
        self.last = ""

        self.id = ""
        self.secret = ""
        self.callback = ""
        self.code = ""
        self.token = ""

        self.cust_id = ""
        self.balance = ""
        self.avail_balance = ""

        self.tokenExpiry = ""

    def set_username(self, username):
        self.username = username.lower()

    def load(self):
        try:
            with open(config.cdat, 'r') as cdat:
                database = json.load(cdat)
            cdat.close()

            self.username = database[self.telegramID]["username"]
            self.email = database[self.telegramID]["email"]
            self.password = database[self.telegramID]["password"]
            self.first = database[self.telegramID]["first"]
            self.last = database[self.telegramID]["last"]

            self.id = database[self.telegramID]["id"]
            self.secret = database[self.telegramID]["secret"]
            self.callback = database[self.telegramID]["callback"]
            self.code = database[self.telegramID]["code"]
            self.token = database[self.telegramID]["token"]

            self.tokenExpiry = database[self.telegramID]["token_expiry"]
            if self.tokenExpiry < time.time():
                self.getCode()
                self.getToken()
            self.getAccount()
            self.store()
            return True

        except:
            return False

    def store(self):
        try:
            with open(config.cdat, 'r') as cdat:
                database = json.load(cdat)
            cdat.close()

            user_data = {}
            user_data["username"] = self.username
            user_data["email"] = self.email
            user_data["password"] = self.password
            user_data["first"] = self.first
            user_data["last"] = self.last

            user_data["id"] = self.id
            user_data["secret"] = self.secret
            user_data["callback"] = self.callback
            user_data["code"] = self.code
            user_data["token"] = self.token

            user_data["cust_id"] = self.cust_id
            user_data["balance"] = self.balance
            user_data["balance_available"] = self.avail_balance

            user_data["token_expiry"] = self.tokenExpiry

            database[self.telegramID] = user_data

            with open(config.cdat, 'w') as cdat:
                json.dump(database, cdat)
            cdat.close()
            return True
        except:
            return False


    def register(self, first, last, email):
        try:
            self.first = first
            self.last = last
            self.email = email
            self.driver = self.wdf.getWebDriverInstance(config.apm_url)
            self.elementClick("//a[text()='Register']", locatorType="XPATH")
            self.elementClick("//option[text()='{}']".format("Mr."), locatorType="XPATH")
            self.sendKeys(self.first, "//input[contains(@id, '_signup_first_name')]", locatorType="XPATH")
            self.sendKeys(self.last, "//input[contains(@id, '_signup_last_name')]", locatorType="XPATH")
            self.sendKeys(self.email, "//input[contains(@id, '_signup_email')]", locatorType="XPATH")
            self.sendKeys(self.password, "//input[contains(@id, '_signup_password')]", locatorType="XPATH")
            self.sendKeys(self.password, "//input[contains(@id, '_signup_password_confirmation')]", locatorType="XPATH")
            self.elementClick("//input[@type='submit']", locatorType="XPATH")
            time.sleep(3)
            self.driver.get(config.mailcatcher_url)
            self.elementClick("//tr[1]//td[1]",locatorType="XPATH")
            self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
            time.sleep(1)
            self.elementClick("//a[contains(@href, 'confirmation')]", locatorType="XPATH")
            time.sleep(1)

            self.driver.quit()
            self.driver = self.wdf.getWebDriverInstance(config.apm_url)
            self.sendKeys(self.email, "//input[contains(@id, 'session_email')]", locatorType="XPATH")
            self.sendKeys(self.password, "//input[contains(@id, 'session_password')]", locatorType="XPATH")
            self.elementClick("//input[@type='submit']", locatorType="XPATH")
            self.elementClick("//a[text()='New App']", locatorType="XPATH")
            self.sendKeys("MrSir"+str(time.time())+self.email,"//input[@id='app_name']", locatorType="XPATH")
            self.sendKeys("MrSir","//input[@id='app_provider']", locatorType="XPATH")
            self.sendKeys("MrSir","//textarea[@id='app_description']", locatorType="XPATH")
            self.sendKeys("http://localhost:3005","//input[@id='app_url']", locatorType="XPATH")
            self.sendKeys("http://localhost:3005","//input[@id='app_callback_urls']", locatorType="XPATH")
            self.sendKeys("support@mrsir.com","//input[@id='app_support_email']", locatorType="XPATH")
            self.sendKeys("http://localhost:3005","//input[@id='app_support_url']", locatorType="XPATH")
            self.sendKeys("http://localhost:3005","//input[@id='app_tos_url']", locatorType="XPATH")
            self.sendKeys("http://localhost:3005","//input[@id='app_privacy_policy_url']", locatorType="XPATH")
            self.elementClick("//input[@id='banking-scope']", locatorType="XPATH")
            self.elementClick("//*[text()='Basic, read-write']", locatorType="XPATH")
            self.elementClick("//input[@type='submit']", locatorType="XPATH")

            self.id = self.driver.find_element_by_xpath("//tr[.//th[text()='Client ID']]//td//code").text
            self.secret = self.driver.find_element_by_xpath("//tr[.//th[text()='Client Secret']]//td//code").text
            self.callback = self.driver.find_element_by_xpath("//tr[.//th[text()='Callback URLs']]//td//code").text
            self.driver.get(config.apm_url+config.auth_url.format(self.id))
            self.elementClick("//a[contains(text(), 'Next')]", locatorType="XPATH")
            self.elementClick("//a[contains(text(), 'Allow')]", locatorType="XPATH")
            self.elementClick("//input[@type='submit']", locatorType="XPATH")
            self.code = str(self.driver.current_url).split("?code=")[1].split("&state")[0]
            self.driver.quit()
            return True
        except:
            return False

    def getCode(self):
        try:
            self.driver = self.wdf.getWebDriverInstance(config.apm_url)
            self.sendKeys(self.email, "//input[contains(@id, 'session_email')]", locatorType="XPATH")
            self.sendKeys(self.password, "//input[contains(@id, 'session_password')]", locatorType="XPATH")
            self.elementClick("//input[@type='submit']", locatorType="XPATH")
            self.driver.get(config.apm_url + config.auth_url.format(self.id))
            time.sleep(1)
            self.code = str(self.driver.current_url).split("?code=")[1].split("&state")[0]
            self.driver.quit()
            return True
        except:
            return False


    def getToken(self):
        try:
            self.token = self.banking.get_authorization(self.id, self.secret, self.code)
            self.logTime()
            return True
        except:
            return False

    def getAccount(self):
        rawData = self.banking.get_accounts(self.token)
        data = json.loads(rawData)['data'][0]
        self.cust_id = data['id']
        self.balance = data['balance']
        self.avail_balance = data['balance_available']


    def transfer(self, receiver, amount, note=""):
        with open(config.cdat, 'r') as cdat:
            database = json.load(cdat)
        cdat.close()

        receiverID = ""
        for user in database:
            if receiver == database[user]['username']:
                receiverID = database[user]['cust_id']

        if receiverID == "":
            return "NOT FOUND"
        else:
            external = str(time.time()).split(".")[1]+"gdg"+str(time.time()).split(".")[1]
            response = self.banking.post_internal_transfer(self.token, self.cust_id, receiverID, external, amount, note)

            if response.status_code == 201:
                return str(receiverID)
            else:
                return "FAILED"

    def logTime(self):
        self.tokenExpiry = time.time()+3600





# us = User("239618248")
# us.load()
# us.getAccount()

# us.register("user", "user", "user@6.com")
# us.getCode()
# us.getToken()
# print(us.token)
# us.store()
