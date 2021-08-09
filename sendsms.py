# -*- coding: utf-8 -*-
def sendsms(number):
    import http.client
    
    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = '''{
      "sender": "PUNRTO",
      "route": "4",
      "country": "91",
      "sms": [
        {
          "message": "You have been fined with 200 RS for parking your vehicle in no parking area.Visit nearest traffic police station to avoid any inconvenience.",
          "to": [
          "%s" 
          ]
        }
      ]
    }'''%number
    headers = {
        'authkey': "auth-key",
        'content-type': "application/json"
        }
    
    conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    
    print(data.decode("utf-8"))
