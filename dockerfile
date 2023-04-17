FROM python:2.7
RUN git clone --single-branch --branch feature_api_rest_identitat https://github.com/UPC/mailtoticket.git

WORKDIR /mailtoticket

COPY settings_default.py .
COPY entrypoint.sh .
COPY .fetchmailrc /root/

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y fetchmail
RUN apt-get install -y cron
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 755 entrypoint.sh
RUN chmod 600 /root/.fetchmailrc


ENTRYPOINT /mailtoticket/entrypoint.sh