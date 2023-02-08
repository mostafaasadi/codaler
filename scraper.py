import logging
import sqlalchemy
from time import sleep
from requests import get
from models import Audite
from sys import stdout, exit
from fake_headers import Headers
from sqlalchemy.orm import sessionmaker


try:
    db_engine = sqlalchemy.create_engine('sqlite:///audites.db')
    Session = sessionmaker(bind=db_engine)
    Audite.metadata.create_all(db_engine)
except Exception as e:
    logging.error(e)
    exit(1)


def get_last_audites():
    try:
        header = Headers().generate()
        res = get(
            'https://search.codal.ir/api/search/v2/q?=&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=false',
            headers=header,
            timeout=10)
        res_json = res.json()
    except Exception as e:
        logging.error(e)
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


def create_audite_object(request_audites):
    audites = []
    for request_audite in request_audites:
        audite_object = Audite(
            TrackingNo=request_audite.get('TracingNo'),
            Url='https://codal.ir' + request_audite.get('Url', ''),
            Title=request_audite.get('Title'),
            Symbol=request_audite.get('Symbol'),
            PdfUrl='https://codal.ir/' + request_audite.get('PdfUrl', ''),
            SentDateTime=request_audite.get('SentDateTime'),
            AttachmentUrl='https://codal.ir' + request_audite.get('AttachmentUrl'),
            PublishDateTime=request_audite.get('PublishDateTime'),
        )
        audites.append(audite_object)
    return audites


def save_audites(audites):
    with Session() as session:
        for audite in audites:
            session.merge(audite)

        try:
            session.commit()
            return True
        except Exception as e:
            logging.error(e)
            session.rollback()
            return False


def run():
    global last_number
    format = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log = logging.FileHandler('scraper.log', mode='w')

    log.setFormatter(format)
    logger.addHandler(log)
    logger.addHandler(logging.StreamHandler(stdout))

    last_number = 0
    new_number = 1

    while True:
        last_audite = check_update()
        if last_audite:
            logging.info('new audites scraped')
            new_number = int(last_audite[-1].get('TracingNo'))
            if new_number == last_number:
                continue

            logging.info(f'new audite number: {new_number}')
            last_number = new_number
            audites = create_audite_object(last_audite)
            save_status = save_audites(audites)
            if save_status:
                logging.info('audites saved')

        sleep(60)


if __name__ == '__main__':
    run()
