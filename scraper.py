from time import sleep
from requests import get


def get_last_audites():
    try:
        res = get(
            'https://search.codal.ir/api/search/v2/q?=&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=false',
            timeout=10)
        res_json = res.json()
    except Exception as e:
        print(e)
        return False
    return res_json


def check_update():
    global last_number
    last_audites = get_last_audites()
    if last_audites:
        if last_audites['Total'] > last_number:
            last_number = last_audites['Total']
            return last_audites['Letters']
    return False


if __name__ == '__main__':
    last_number = 0
    while True:
        last_audite = check_update()
        if last_audite:
            print(last_audite)
        sleep(60)
