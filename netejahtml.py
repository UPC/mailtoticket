# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import bleach
import re


def neteja_nou(html):
    html = sanitize(html)
    html = treure_signatura(html)
    html = treure_pgp(html)
    html = treure_imatges_trencades(html)
    html = compacta_br(html)
    html = treure_body(html)
    return html


def neteja_reply(html):
    html = sanitize(html)
    html = treure_reply(html)
    html = treure_signatura(html)
    html = treure_pgp(html)
    html = treure_imatges_trencades(html)
    html = compacta_br(html)
    html = treure_body(html)
    return html


def assegura_contingut(funcio_neteja):
    def funcio_assegura_contingut(html):
        html_net = funcio_neteja(html)
        soup = BeautifulSoup(html_net, "html.parser")
        # Truquillo pythonic per treure espais al text
        text_sense_espais = "".join(soup.text.strip())
        if len(text_sense_espais) > 0:
            return html_net
        else:
            return html

    return funcio_assegura_contingut


@assegura_contingut
def sanitize(html):
    # Mails del tipus <mail@fib.upc.edu> no son tags!
    html = re.sub(r"<(a-zA-Z0-9_\.+-]+@a-zA-Z0-9_\.+-]+)>", r"[\1]", html)
    html = re.sub(r"&lt;([a-zA-Z0-9_\.+-]+@[a-zA-Z0-9_\.+-]+)&gt;", r"[\1]",
                  html)
    # Trec tags i el seu contingut
    html = treure_tag_complet(html, 'style')
    html = treure_tag_complet(html, 'script')
    # Netejo propiament
    net = bleach.clean(
        html,
        tags=[
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
            'li', 'ol', 'strong', 'ul', 'pre', 'table', 'tr', 'td', 'th',
            'tbody', 'thead', 'tfoot', 'div', 'br', 'hr', 'img', 'p'
        ],
        attributes={
            '*': ['class'],
            'img': ['src'],
            'a': ['href'],
            'td': ['colspan', 'rowspan'],
            'blockquote': ['type']
        },
        strip=True
    )
    # Aixo es perque els BR siguin autocontinguts i no interfereixin a l'arbre
    net = re.sub(r'<br\s*/?>', '<br/>', net, flags=re.I)
    net = re.sub(r'</br\s*>', '', net, flags=re.I)
    return "<body>%s</body>" % net


@assegura_contingut
def compacta_br(html):
    html = re.sub(r'<br\s*/?>(?:\s*<br\s*/?>)+', '<br/><br/>', html,
                  flags=re.I)
    return html


@assegura_contingut
def treure_body(html):
    html = re.sub(r'</?body\s*>', '', html, flags=re.I)
    return html


def treure_reply(html):
    html = treure_blockquote(html)
    html = treure_reply_text(html)
    return html


def _es_prefix_reply_valid(tag):
    # Comprovem que no contingui mes dels 2 tags que posa per defecte
    # (un <a> i un <br>) o voldrà dir que té contingut que no hem d'esborrar
    return len(tag.find_all(True)) <= 2


def treure_tag_complet(html, tag):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.select(tag)
    for t in tags:
        t.decompose()
    return unicode(soup)


@assegura_contingut
def treure_blockquote(html):
    soup = BeautifulSoup(html, "html.parser")

    # Thunderbird, webmail
    tags = soup.select('body > blockquote[type=cite]')
    if len(tags) == 1:
        tags[0].decompose()

    # gmail
    tags = soup.select('body > div.gmail_extra')
    if len(tags) == 1:
        tags[0].decompose()

    # Client mail android
    tags = soup.select('body > div.quote')
    if len(tags) == 1:
        tags[0].decompose()

    # Prefix de signatura de Thunderbird
    tags = soup.select('body > div.moz-cite-prefix')
    if len(tags) == 1 and _es_prefix_reply_valid(tags[0]):
        tags[0].decompose()

    return unicode(soup)


@assegura_contingut
def treure_reply_text(text):
    blocs = 0
    anterior = False
    linies = text.split("<br/>\n")
    sensequotes = []
    for linia in linies:
        if linia.startswith("&gt;"):
            dintre = True
            if anterior != dintre:
                blocs += 1

        else:
            dintre = False
            sensequotes.append(linia)

        anterior = dintre

    if blocs == 1:
        return "<br/>\n".join(sensequotes)
    else:
        return text


def treure_signatura(html):
    html = treure_signatura_text(html)
    html = treure_signatura_html(html)
    return html


@assegura_contingut
def treure_signatura_text(text):
    blocs = 0
    signatura = False
    cos = []
    linies = text.split(r"<br\s*/?>\n")
    for linia in linies:
        if re.match(r"^--\s*$", linia):
            signatura = True
            blocs += 1

        if not signatura:
            cos.append(linia)

    if blocs == 1:
        return "<br>\n".join(cos)
    else:
        return text


@assegura_contingut
def treure_signatura_html(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.select('.moz-signature')
    if len(tags) >= 1:
        tags[len(tags) - 1].decompose()

    return unicode(soup)


@assegura_contingut
def treure_imatges_trencades(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.select('img[src^="cid:"]')
    for tag in tags:
        tag.decompose()

    return unicode(soup)


@assegura_contingut
def treure_pgp(text):
    text = treure_bloc(text,
                       "^-----BEGIN PGP PUBLIC KEY BLOCK-----",
                       "^-----END PGP PUBLIC KEY BLOCK-----")
    text = treure_bloc(text,
                       "^-----BEGIN PGP SIGNATURE-----",
                       "^-----END PGP SIGNATURE-----")
    return text


def treure_bloc(text, regex_inici, regex_fi):
    pgp = False
    cos = []
    linies = text.split("\n")
    for linia in linies:
        if re.match(regex_inici, linia):
            pgp = True

        if not pgp:
            cos.append(linia)

        if re.match(regex_fi, linia):
            pgp = False

    return "\n".join(cos)
