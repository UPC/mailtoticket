import imaplib
import oauth2
import settings_fetchgmail as settings
import os
import subprocess
import pickle
import datetime

MAIL_TMP="/tmp/mail"

def escriure_mail(mail):
    with open(MAIL_TMP, "wb") as f:
        f.write(mail)
        f.flush()

def refresca_i_guarda_token():
    creds=oauth2.RefreshToken(settings.client_id, settings.client_secret,settings.refresh_token)
    creds["expiration_time"]=datetime.datetime.now()+datetime.timedelta(seconds=creds["expires_in"])
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    return creds

def llegir_token():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        if creds["expiration_time"]>datetime.datetime.now():
            return creds
    return refresca_i_guarda_token()

creds = llegir_token()
access_token=creds['access_token']
auth_string=oauth2.GenerateOAuth2String(settings.user, access_token,base64_encode=False)
imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
imap_conn.select('INBOX')

resp, items = imap_conn.uid('SEARCH',None, '(UNSEEN)')
items = items[0].split() # getting the mails id

for emailid in items:
    resp, data = imap_conn.uid('FETCH',emailid, "(RFC822)")    
    escriure_mail(data[0][1])
    with open(MAIL_TMP, "rb") as f:
        r=subprocess.run(settings.mailtoticket,stdin=f) 
        if r.returncode>0:
            imap_conn.uid('STORE', emailid, '-FLAGS', '(\Seen)')
