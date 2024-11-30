import requests
import json
def send_request():
    url = 'http://127.0.0.1:5000/task'
    data = {
        'task_name':'Task1',
        'task_description':'Task1 Description',
        'task_status':'Pending'
    }
    response = requests.post(url, json=data)
    print(response.json())
    print(response.status_code)


send_request()
