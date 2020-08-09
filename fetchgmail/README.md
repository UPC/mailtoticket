## Fetchgmail

Codi basat en el que hi ha aqui

https://github.com/google/gmail-oauth2-tools

i seguint aquestes explicacions

https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough

# Preparació

Primer de tot hem de donar d'alta la nostra aplicació tal i com explica aqui

https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough

Necessitarem un client_id i un client_secret que ens generarà Google. Amb aquests valors obtindrem un refresh token. Per fer aixo, executarem via docker el següent:

```
python oauth2.py --user=nom.usuari@upc.edu --client_id=xxxxxx.apps.googleusercontent.com --client_secret=yyyyy --generate_oauth2_token
```

Del resultat d'aquesta ordre, nomes necessitem el refresh token, que ens apuntarem al fitxer settings_fetchgmail.py, substituint els valors de user, client_id i refresh_token pels correctes.

```
user="nom.usuari@upc.edu"
client_id="xxxxxx"
client_secret="yyyyyy"
# El refresh token s'obté executant oauth2.sh
refresh_token="zzzzzzzz"
mailtoticket=["python","/mailtoticket/mailtoticket.py"]
```

# Proves

Ara ja tenim un settings.py amb tot el necessari per poder accedir al compte. Llavors simplement executem

```
python3 fetchgmail
```

I aixo es connectarà al compte i executarà el mailtoticket.sh passant cada mail no llegit per l'entrada estàndard