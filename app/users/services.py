import requests

API_KEY = "kz8a589b926934809614fba58b659b15e63c954dc17088f6dc9e529e80f1d648fe074a"
URL = "https://api.mobizon.kz/service/Message/SendSmsMessage?output=json&api=v1&apiKey=" + API_KEY

def send_otp_via_sms(phone_number, otp):
    #
    # api.mobizon.kz
    #
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "cache-control": "no-cache"
    }
    message = {
        "recipient": phone_number,
        "text": "Your activation code: " + otp
    }

    r = requests.post(url=URL, data=message, headers=headers)

    data = r.json()

    print("Request", data)

    return data
