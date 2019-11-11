FROM python:2.7

WORKDIR /usr/src/app
RUN echo "PATH=$PWD/local/bin:\$PATH" >> ~/.bashrc
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "mailtoticket.py" ]
