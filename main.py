from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client

account_sid = 'AC775909a127625162b0051b94c68502c2'
auth_token = 'b0201902f143ce8cc3fa5695a99a7510'
client = Client(account_sid, auth_token)


app = Flask(__name__)


@app.route('/', methods=['POST'])
def bot():
    # response = MessagingResponse()
    number = request.form['From']

    incoming_msg = request.values.get('Body', '')
    if "hi" in incoming_msg.lower() or "hello" in incoming_msg.lower():
        message = client.messages.create(
            body="-----------------------------------\nCONTINEO CHATBOT\n-----------------------------------\n\nEnter details in format : \nUSN\nDOB(dd mm yyyy\n\nExample\n1nt19ec005\n20 03 2002",
            from_='whatsapp:+14155238886',
            to=number
        )
    else:
        l = incoming_msg.split()
        usn = l[0]
        d = l[1]
        m = l[2]
        yy = l[3]

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-software-rasterizer')
        driver = webdriver.Chrome(chrome_options=options)

        url = 'https://www.nmit.ac.in/'

        driver = webdriver.Chrome()

        driver.get('https://www.nmit.ac.in/')

        driver.find_element(By.XPATH, '//button[text()="Parent Portal"]').click()

        dd = Select(driver.find_element(By.ID, 'dd'))
        mm = Select(driver.find_element(By.ID, 'mm'))
        yyyy = Select(driver.find_element(By.ID, 'yyyy'))

        username = driver.find_element(By.ID, 'username')

        username.send_keys(usn)
        dd.select_by_value(d + ' ')
        mm.select_by_value(m)
        yyyy.select_by_value(yy)

        driver.find_element(By.CLASS_NAME, "uk-button").click()

        input = driver.find_element(By.XPATH,
                                    "//div[@id='barPadding']//*[name()='svg']//*[name()='g' and contains(@transform,'translate(')]//*[name()='g' and contains(@class,'bb-chart')]//*[name()='g' and contains(@class,'bb-event-r')]//*[name()='rect' and contains(@class,'bb-event-r')]")
        achains = ActionChains(driver)
        achains.move_to_element(input).perform()

        num_rows = len(driver.find_elements(By.XPATH,
                                            "//body[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr")) - 1

        sub_code = list()
        sub_marks = list()
        for i in range(2, num_rows + 2):
            xpath = "//body[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/" + "tr[{}]".format(
                i) + "/td[1]"
            sub_code.append(driver.find_element(By.XPATH, xpath).text)
            xpath = "//body[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/" + "tr[{}]".format(
                i) + "/td[2]"
            sub_marks.append(driver.find_element(By.XPATH, xpath).text)
        j = 0

        msggg = " "
        for result in sub_code:
            msggg = msggg + result + "-" + sub_marks[j] + "\n"
            j = j + 1
        print(msggg)
        # #response.message(msgd)
        # response = MessagingResponse()
        # msg = response.message(msggg)
        # # msg.body(msggg)

        message = client.messages.create(
                body=msggg,
                from_='whatsapp:+14155238886',
                to=number
            )

    # return str(response)


if __name__ == "__main__":
    app.run()
