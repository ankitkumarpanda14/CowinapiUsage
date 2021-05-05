import requests
from datetime import date, datetime
from time import time, ctime, sleep
from win10toast import ToastNotifier

minutes = 5

today = date.today()

__district = "8"  # visakhapatnam

d1 = today.strftime("%d/%m/%Y")

__date = str(d1).replace("/", "-")

above_45 = True


def parse_json(result):
    output = []
    centers = result['centers']
    for center in centers:
        sessions = center['sessions']
        for session in sessions:
            if session['available_capacity'] > 0:
                res = {'name': center['name'], 'block_name': center['block_name'],
                       'age_limit': session['min_age_limit'], 'vaccine_type': session['vaccine'],
                       'date': session['date'], 'available_capacity': session['available_capacity']}
                output.append(res)
    return output


def call_api():
    global count
    count = 1
    notification = ToastNotifier()
    print(ctime(time()))
    api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + __district + "&date=" + __date
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(api, headers=headers)

    if response.status_code == 200:
        print("API call success")
        result = response.json()
        output = parse_json(result)
        if len(output) > 0:
            # print("Vaccines available")
            print('\007')
            result_str = ""
            if above_45:
                for center in output:
                    notification.show_toast(title="CoWinAPI", msg="Vaccines are available", duration=5)
                    print(center['name'])
                    print("block:" + center['block_name'])
                    print("vaccine count:" + str(center['available_capacity']))
                    print("vaccines type:" + center['vaccine_type'])
                    print(center['date'])
                    print("age_limit:" + str(center['age_limit']))
                    print("---------------------------------------------------------")

            elif ~above_45:
                if len(output) > 0:
                    for center in output:
                        if center['age_limit'] < 45:
                            if count == 1:
                                count = count + 1
                                notification.show_toast(title="CoWinAPI", msg="Vaccines are available", duration=5)
                            print(center['name'])
                            print("block:" + center['block_name'])
                            print("vaccine count:" + str(center['available_capacity']))
                            print("vaccines type:" + center['vaccine_type'])
                            print(center['date'])
                            print("age_limit:" + str(center['age_limit']))
                            print("---------------------------------------------------------")

                        elif count == 1:
                            count = count + 1
                            print("Vaccines Unavailable at the moment")


t = datetime.now()

if __name__ == '__main__':
    call_api()
    while True:
        delta = datetime.now() - t
        if delta.seconds >= minutes * 24:
            call_api()
            t = datetime.now()
