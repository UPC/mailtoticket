Per fer servir mailtoticket + fetchmail a Docker caldrà
 
####0.- Crear una carpeta "conf" buida
Necessitarem posar les configuracions a passar al docker en una única carpeta

####1.- Tenir un fitxer docker/.fetchmailrc correcte 
Tenim una plantilla per generar-lo, bàsicament es canviar el username i password del compte a llegir.
El deixarem a la carpeta "conf" que acabem de crear

####2.- Fer el settings_default.py 
Es pot partir copiar del settings_sample.py. El copiarem també a "conf"

####3.- Fer el build

```
docker build -t mailtoticket .
```

####4.- Executar, passant on ha d'escriure els logs i on tenim la carpeta conf 

Poso un example amb windows. La idea es mapejar un path local amb el "/log" i el "conf"

```
docker run -it -v "d:\usuaris\jaumem\workspace-mailtoticket\mailtoticket\log":/log -v "d:\usuaris\jaumem\workspace-mailtoticket\mailtoticket\conf":/conf mailtoticket
```