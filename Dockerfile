FROM python:2.7

WORKDIR /usr/src/app
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -yy libsasl2-dev libldap2-dev
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "mailtoticket.py" ]
