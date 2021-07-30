import time
from filtres.filtre import Filtre
import settings
import re
from soa.service import SOAService

import logging
logger = logging.getLogger(__name__)


class FiltreNou(Filtre):

    solicitant = None
    ticket_id = None
    enviar_missatge_creacio = 'S'

    def es_aplicable(self):
        logger.info("Filtre de Nou")
        logger.info("Tinc un mail de %s" % self.msg.get_from())
        self.solicitant = self.get_uid()

        logger.info("UID del solicitant: %s" % self.solicitant)
        return self.solicitant is not None

    def obtenir_parametres_addicionals(self):
        defaults = {
            "equipResolutor": settings.get("equip_resolutor_nous"),
            "enviarMissatgeCreacio": self.enviar_missatge_creacio
        }
        if settings.get("valors_defecte") is None:
            return defaults
        for item in settings.get("valors_defecte"):
            regex = re.compile(item['match'], re.IGNORECASE)
            for header_name in item['order']:
                if self.msg.get_header(header_name):
                    header_values = self.msg.get_header(header_name).split(",")
                    for header_value in header_values:
                        if header_value and regex.match(header_value):
                            logger.info("Tinc parametres adicionals via %s"
                                        % header_name)
                            defaults.update(item['defaults'])

        logger.info("Parametres addicionals: %s" % str(defaults))
        return defaults

    def netejar_html(self, html):
        funcio_netejar_mail_nou = settings.get("netejar_mail_nou")
        if funcio_netejar_mail_nou:
            return funcio_netejar_mail_nou(html)
        else:
            return html

    def cal_enviar_cc(self):
        if len(self.msg.get_cc()) == 0:
            return False
        if settings.get("afegir_solicitants_addicionals_en_cc"):
            return True
        patro = settings.get("afegir_solicitants_addicionals_en_cc_nomes_via")
        if not patro:
            return False
        return (re.compile(patro).match(self.msg.get_to()))

    def filtrar(self):
        logger.info("Aplico filtre...")
        body = self.msg.get_body()

        subject = self.msg.get_subject()
        if len(subject) == 0:
            subject = "Ticket de %s" % self.solicitant

        if self.msg.get_reply_to() is not None:
            from_or_reply_to = self.msg.get_reply_to()
        else:
            from_or_reply_to = self.msg.get_from()

        parametres_addicionals = self.obtenir_parametres_addicionals()
        logger.info("A veure si puc crear el ticket de %s" % self.solicitant)
        descripcio = (
            "[Tiquet creat des del correu de %s a %s del %s a les %s]" % (
                self.msg.get_from(),
                self.msg.get_to(),
                self.msg.get_date().strftime("%d/%m/%Y"),
                self.msg.get_date().strftime("%H:%M")
            )
        ) + "<br><br>" + body

        parametres = {
            'assumpte': subject,
            'solicitant': self.solicitant,
            'emailSolicitant': from_or_reply_to,
            'descripcio': self.netejar_html(descripcio)
        }
        parametres.update(parametres_addicionals)
        resultat = self.tickets.alta_tiquet(**parametres)

        if SOAService.resultat_erroni(resultat):
            logger.info("Error: %s - %s" % (
                resultat['codiRetorn'],
                resultat['descripcioError']
            ))
            return False

        logger.info("Ticket creat")

        ticket_id = resultat['codiTiquet']
        descripcio = self.afegir_attachments_canviant_body(
            ticket_id,
            self.solicitant,
            descripcio
        )

        logger.info("Attachments (si n'hi ha) afegits")

        if settings.get("assignar_data_resolucio_amb_data_creacio"):
            data_resolucio = time.strftime("%d-%m-%Y")
        else:
            data_resolucio = ''

        resultat = self.tickets.modificar_tiquet(
            codiTiquet=ticket_id,
            descripcio=self.netejar_html(descripcio),
            dataResol=data_resolucio
        )

        if SOAService.resultat_erroni(resultat):
            logger.info("Error: %s - %s" % (
                resultat['codiRetorn'],
                resultat['descripcioError']
            ))
        else:
            logger.info("Mail modificat a %s" % self.msg.get_from())

        if self.cal_enviar_cc():
            for uid in self.get_uid_addicionals():
                resultat = self.tickets.afegir_solicitant_tiquet(
                    codiTiquet=ticket_id,
                    solicitant=uid
                )

                if SOAService.resultat_erroni(resultat):
                    logger.info("Error: %s - %s" % (
                        resultat['codiRetorn'],
                        resultat['descripcioError']
                    ))
                else:
                    logger.info("Afegit %s" % uid)

        return True
