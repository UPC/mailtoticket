import re
from filtres.filtre import Filtre
import settings
from soa.service import SOAService

import logging
logger = logging.getLogger(__name__)


class FiltreReply(Filtre):

    def __init__(self, msg=None, tickets=None, identitat=None):
        Filtre.__init__(self, msg, tickets, identitat)
        self.solicitant = None
        self.ticket_id = None
        self.privat = False
        self.ticket = None
        self.regex_message_id = settings.get(
            "regex_message_id") or "^<[-a-f0-9]+-tiquet-id-([0-9]+)@gn6>$"

    def buscar_ticket_id(self, string, regex):
        try:
            logger.info("Buscant numero a  %s" % string)
            p = re.compile(regex, re.UNICODE)
            m = p.match(string)
            ticket_id = m.group(1)
            logger.info("Trobat ticket %s" % ticket_id)
            return ticket_id
        except Exception as e:
            logger.info(e)
            logger.info("Error found")
            return None

    def obtenir_ticket_id(self):
        ticket_id = self.buscar_ticket_id(
            self.msg.get_header("In-Reply-To"),
            self.regex_message_id
        )
        if ticket_id is not None:
            return ticket_id
        ticket_id = self.buscar_ticket_id(
            self.msg.get_subject(),
            settings.get("regex_reply")
        )
        return ticket_id

    def es_aplicable(self):
        logger.info("Filtre de reply")

        try:
            # Ara anem a veure que podem fer amb aquest missatge
            self.ticket_id = self.obtenir_ticket_id()
            if self.ticket_id is None:
                return False

            regex_privat = settings.get("regex_privat")
            comentari_intern = re.compile(regex_privat)
            if comentari_intern.match(self.msg.get_subject()):
                logger.info("El comentari es privat")
                self.privat = True

            # Obtenim el tiquet amb les dades de solicitant i emailSolicitant
            self.ticket = self.tickets.consulta_tiquet_dades(self.ticket_id)

            # Mirem qui ha creat el ticket
            self.solicitant_segons_ticket = self.ticket['solicitant']
            logger.info("Ticket de %s" % self.solicitant)
            logger.info("Mail de %s" % self.msg.get_from())

            self.solicitant_segons_mail = self.get_uid()
            logger.info("Solicitant segons Mail %s"
                        % self.solicitant_segons_mail)

            # Si no trobem el mail, sera de l'usuari generic
            if self.solicitant_segons_mail is not None:
                self.solicitant = self.solicitant_segons_mail
            elif self.ticket['emailSolicitant'] == self.msg.get_from():
                self.solicitant = self.solicitant_segons_ticket
            else:
                self.solicitant = settings.get("usuari_extern")

            logger.info("Crearem comentari a nom de %s" % self.solicitant)
            return True

        except Exception as e:
            logger.info("Peta el filtre... %s" % str(e))
            return False

    def filtrar(self):
        body = self.msg.get_body()
        if self.solicitant == self.solicitant_segons_ticket:
            notificat = 'N'
        else:
            notificar_comentaris = settings.get("notificar_comentaris_afegits")
            if notificar_comentaris is None:
                notificar_comentaris = True
            notificat = 'S' if notificar_comentaris else 'N'
        body = self.afegir_attachments_canviant_body(
            self.ticket_id,
            self.solicitant,
            body
        )
        funcio_netejar_mail_reply = settings.get("netejar_mail_reply")
        if funcio_netejar_mail_reply:
            body = funcio_netejar_mail_reply(body)
        resultat = self.tickets.afegir_comentari_tiquet(
            codiTiquet=self.ticket_id,
            usuari=self.solicitant,
            descripcio=(
                "[Comentari afegit des del correu de %s" % self.msg.get_from()
            ) + (
                " del %s" % self.msg.get_date().strftime("%d/%m/%Y")
            ) + (
                " a les %s]<br><br>" % self.msg.get_date().strftime("%H:%M")
            ) + body,
            tipusComentari='COMENT_TIQUET_PRIVAT'
            if self.privat else 'COMENT_TIQUET_PUBLIC',
            esNotificat=notificat if not self.privat else 'N'
        )

        if SOAService.resultat_erroni(resultat):
            logger.info("Error: %s - %s" % (
                resultat['codiRetorn'],
                resultat['descripcioError']
            ))
            return False

        logger.info("Comentari afegit")
        return True
