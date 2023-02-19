import sched, time
from app import db
from kavenegar import *
from config import Config
from models import User, Audite


def send_notif(audite, users_phone):
    msg = f''''
        {audite.CompanyName} {audite.Symbol} \n
        {audite.Title} \n
        {audite.Url} \n\n

        [کدالر]
    '''
    try:
        params = {
            'receptor': users_phone,
            'message': msg
        } 
        response = api.sms_send(params)
        return True
    except Exception as e:
        print(str(e))
        return False


def periodic_alert(scheduler): 
    scheduler.enter(60, 1, periodic_alert, (scheduler,))
    with db.session() as session:
        users = session.query(User).all()
        audites = session.query(Audite).filter(Audite.send.is_(None)).offset(50).all()
        for audite in audites:
            users_phone = ''
            for user in users:
                if audite.Symbol in user.symbols:
                    users_phone += f'0{user.phone},'
            
            if len(users_phone) > 0:
                status = send_notif(audite, users_phone=users_phone)
                if status:
                    audite.send = True
                    session.commit()


if __name__ == '__main__':
    api = KavenegarAPI(Config.SMS_TOKEN)
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(60, 1, periodic_alert, (scheduler,))
    scheduler.run()
