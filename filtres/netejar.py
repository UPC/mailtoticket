import time
from filtres.filtre import Filtre
import settings
import re

class FiltreNou(Filtre):

    def netejar_html(self, html):
        funcio_netejar_mail_nou = settings.get("netejar_mail_nou")
        if funcio_netejar_mail_nou:
            return funcio_netejar_mail_nou(html)
        else:
            return html

    def filtrar(self):
        body = self.msg.get_body()

        subject = self.msg.get_subject()
        if len(subject) == 0:
            subject = "Ticket de %s" % self.solicitant

        if self.msg.get_reply_to() is not None:
            from_or_reply_to = self.msg.get_reply_to()
        else:
            from_or_reply_to = self.msg.get_from()

        descripcio = (
            "[Tiquet creat des del correu de %s del %s a les %s]<br><br>" % (
                self.msg.get_from(),
                self.msg.get_date().strftime("%d/%m/%Y"),
                self.msg.get_date().strftime("%H:%M")
            )
        ) + body

        return self.netejar_html(descripcio)
