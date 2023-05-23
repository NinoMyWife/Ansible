import smtplib
import sys
from email.message import EmailMessage

class Class_Mail(Exception):

    """A class which will send report mail :

    - SendReportMail

    """

    def __init__(self, MyObjLog):
        self._MyObjLog = MyObjLog
        self._file_conf_path = "/var/log"
        self._namelogpy = "LogAutoDiscoveryAnsible.txt"
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        
    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    
    # ?  setter method
    def set_MyObjLog(self, value):
        if (type(value) == type(self._MonWinRM)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MyObjLog = value
        else :
            raise "Property Error"


    def SendReportMail(self, FullLog, NbrNOTOK) :

        """This function will send a report mail

        Args:
            FullLog (Str): Log we need to send in email
            NbrNOTOK (int): The number of error in file

        Raises:
            Exception: SMTP Error/Invalide certificate
            
        Return:
            Mail
        """

        try :
            # set your email and password
            # please use App Password
            email_address = "XXXXXX"
            email_password = "XXXXXX"
            if NbrNOTOK == 0 :
                # create email
                msg = EmailMessage()
                msg["Subject"] = "Rapport du Cron de changement de mot de passe, Etat : Successfull"
                msg["From"] = "XXXXXX"
                msg["To"] = "XXXXXX"
                # msg["To"] = "monitoring@dinao.com"
                msg.set_content(f"{FullLog}")
                # send email
                with smtplib.SMTP_SSL("XXXXXX", port=XXXXXX) as smtp:
                    smtp.login(email_address, email_password)
                    smtp.send_message(msg)
            else : 
                # create email
                msg = EmailMessage()
                msg["Subject"] = f"Rapport du Cron de changement de mot de passe, Etat : {NbrNOTOK} Erreur"
                msg["From"] = "XXXXXX"
                msg["To"] = "XXXXXX"
                # msg["To"] = "monitoring@dinao.com"
                msg.set_content(f"{FullLog}")
                # send email
                with smtplib.SMTP_SSL("XXXXXX", port=XXXXXX) as smtp:
                    smtp.login(email_address, email_password)
                    smtp.send_message(msg)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

