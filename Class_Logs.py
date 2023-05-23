##########################################################################
# * Importation des bibliotheques
##########################################################################

import winrm
import sys
import inspect
import Class_Colors

##########################################################################
# * Début du script
##########################################################################


TopDefaultPrintLog = True
TopDontRaise = False
TopDontExit = False

class Class_Logs(Exception):
    def __init__(self):
        try:
            self.directory=""
            self.filename=""
            self.writemode='a'
            self.content=""
            self.file=""
            self.TopExit = False
            self.TopRaise = False
            self.TopPrintLog = True
        except Exception as e:
            print ("ERROR in Class_logs.__init__(self) : error %s" % (e))                    

    def __del__(self):

        try:
            self.directory=""
            self.filename=""
            self.writemode=""
            self.content=""
        except Exception as err:
            raise Exception("Class_logs.CreateLogFile - impossible de créer le fichier de log -> %s" % err)
        

    def CreateLogFile(self, mytext):

        """This function will create the log file
        Args:
            mytext (str): Text to write in log file
            
        Raises:
            Exception: FileError or Permission denied
        """
        try:
            # Création du chemin du fichier de log
            myfullname = "%s/%s" % (self.directory, self.filename)
            # Création du fichier de log
            self.file = open(myfullname, self.writemode)
            self.file.write("\n" + mytext)
        except Exception as err :
            raise Exception("Class_logs.CreateLogFile - impossible de créer le fichier de log -> %s" % err)
    
    def AjouteLog(self, mytext, TopSysExit=TopDontExit, TopPrint=TopDefaultPrintLog, ExitCode=None, CouleurTexte=Class_Colors.Color_Off):

        """This function will add log in log file and can show the log in prompt
        
        Args:
            mytext (str): Text to write in log file
            TopSysExit (bool): For exit code
            TopPrint (bool): For print in prompt
            ExitCode (int/None): The exit code
            CouleurTexte (str): The color we want to color the line in prompt
            
        Raises:
            TypeError: FileError or Permission denied
        """

        try:
            myoriginaltext = mytext
            # Coloration du texte pour mieux voir les erreurs dans le prompt
            mytext = mytext + Class_Colors.Color_Off 
            # Si il y a des NOT OK le texte sera affiché en rouge dans le prompt
            if "NOT OK" in mytext:
                if CouleurTexte==Class_Colors.Color_Off:
                    mytext = Class_Colors.BIRed + mytext
                else:
                    mytext = CouleurTexte + mytext
            if "ERREUR - " in mytext:
                if CouleurTexte==Class_Colors.Color_Off:
                    mytext = Class_Colors.BIRed + mytext
                else:
                    mytext = CouleurTexte + mytext
            # Si il y a des NOTICE le texte sera affiché en bleu dans le prompt
            elif "NOTICE -" in mytext:
                if CouleurTexte==Class_Colors.Color_Off:
                    mytext = Class_Colors.IBlue + mytext
                else:
                    mytext = CouleurTexte + mytext
            # Si tout se passe bien le texte sera affiché en bleu dans le prompt
            else:
                if CouleurTexte==Class_Colors.Color_Off:
                    mytext = Class_Colors.Green + mytext
                else:
                    mytext = CouleurTexte + mytext
            # Vérification si le fichier de log est bien présent
            if (self.directory !=""):
                self.writemode='a'
                myfullname = "%s/%s" % (self.directory, self.filename)
                # Ouverture du fichier de log
                self.file = open(myfullname, self.writemode)
                # Ecriture dans le fichier de log
                self.file.write("\n" + myoriginaltext)
            else: 
                # On force le print si on peut pas loger dans le fichier
                TopPrint=True
            # Si le TopPrint == True cela affiche les log en couleur dans le prompt
            if (TopPrint==True):
                print(CouleurTexte + mytext )
            # Si le TopSysExit == True cela stop le code a l'endroit du TopSysExit
            if (TopSysExit==True):
                if ExitCode!=None:
                    sys.exit(CouleurTexte + mytext)
                else:
                    sys.exit(ExitCode) 
        except Exception as err:
            raise (CouleurTexte + mytext + err)
    
    def DefineLogFileFor_Create(self): # ?  PAS UTILISE
        try:
            #! attention cette méthode n'est pas ok pour travaile sur pluseurs serveurs a revoir
            self.directory="/var/www/www.dinao.com/WebDev_Automation/DINAO-WEBDEV26/W26TESTD"
            self.filename="Create.log"
        except Exception as err :
            raise Exception("Class_logs.AjouteLog -> erreur %s" % err)    