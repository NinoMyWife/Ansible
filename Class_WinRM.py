##########################################################################
# * Importation des biblioteque
##########################################################################

import winrm
import inspect
import sys
import Class_Colors
import re
import traceback

##########################################################################
# * Importation des classes
##########################################################################


class Class_WinRM(Exception):
    def __init__(self, ObjLog, TopPrintStdErr_param=True, TopPrintStdOut_param=True, TopPrintCommand_param=True,TopPrintStatusCode_param=True):
        try:
            self._MyObjLog = ObjLog
            self.status_code=None
            self.std_err=None
            self.std_out=None
            self.ExecutionCommandSucess= False
            self.IP = None
            self.TopPrintStdErr = TopPrintStdErr_param
            self.TopPrintStdOut = TopPrintStdOut_param
            self.TopPrintCommand = TopPrintCommand_param
            self.TopPrintStatusCode = TopPrintStatusCode_param
            self._useransible = None
            self._passansible = None
            self.TopExit = False
            self.TopRaise = False
            self.TopPrintLog = False
        except Exception as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, False)

    # ? getter method
    def get_useransible(self):
        return self._useransible
    def get_passansible(self):
        return self._passansible

    # ?  setter method
    def set_useransible(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._useransible = value
        else :
            raise "Property Error"
    def set_passansible(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._passansible = value
        else :
            raise "Property Error"

    def _clear_del__(self):
        try:
            self._MyObjLog = None
            self.status_code=None
            self.std_err=None
            self.std_out=None
            self.ExecutionCommandSucess= False
            self.IP = None
            self.TopPrintStdErr = False
            self.TopPrintStdOut = False
            self.TopPrintCommand = False
            self.TopPrintStatusCode = False
        except Exception as err:                 
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, False)
            raise

    def Run_WinRM_CMD_Session(self, command):

        """This function will execute WinRM CMD Session and run our command
        
        Args:
            command (str): Command we need to execute
        """

        try :
            # if self.TopPrintCommand:
            #     print("Class_WinRM.%s / commande = %s " % (inspect.stack()[0][3],command)) 
            winrm_session = self.WinRM_Get_Session()
            ResultWinrmCommand = winrm_session.run_cmd("%s" % command)
            self.status_code=ResultWinrmCommand.status_code
            # if self.TopPrintStatusCode:
            #     print("self.status_code=[%s]" % self.status_code)
            if ResultWinrmCommand.status_code != 0 : 
                self.ExecutionCommandSucess= False
                self.std_err=ResultWinrmCommand.std_err.decode("cp850")
                # if self.TopPrintStdErr:
                #     print("self.std_err=[%s]" % self.std_err)
                # if self.TopPrintStdOut:   
                #     print("self.std_out=[%s]" % self.std_out)
            else :
                self.ExecutionCommandSucess= True
                # if self.TopPrintStdErr:
                #     print("self.std_err=[%s]" % self.std_err)                
                rx = re.compile('[^a-zA-Z0-9_.?-]')
                self.std_out  = rx.sub(' ', ResultWinrmCommand.std_out.decode("cp850")).strip()
                # self.std_out = ResultWinrmCommand.std_out.decode("cp850")
                # if self.TopPrintStdOut:   
                #     print("self.std_out=[%s]" % self.std_out)
            #print("sortie de Run_WinRM_CMD_Session")
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, False)
            raise

    def Run_WinRM_PS_Session(self, command, Clean=True):

        """This function will execute WinRM PS Session and run our command
        
        Args:
            command (str): Command we need to execute
        """

        try :
            # if self.TopPrintCommand:
            #     print("Class_WinRM - %s / commande = %s " % (inspect.stack()[0][3],command)) 
            winrm_session = self.WinRM_Get_Session()
            ResultWinrmCommand = winrm_session.run_ps("%s" % command)
            self.status_code=ResultWinrmCommand.status_code
            self.std_err=ResultWinrmCommand.std_err.decode("cp850")
            if Clean==True : 
                rx = re.compile('[^a-zA-Z0-9_.?-]')
                self.std_out = rx.sub(' ', ResultWinrmCommand.std_out.decode("cp850")).strip()
            else :
                self.std_out = ResultWinrmCommand.std_out.decode("cp850")
            # if self.TopPrintStdErr:
            #     print("self.std_err=[%s]" % self.std_err)
            # if self.TopPrintStatusCode:   
            #     print("self.status_code=%s" % self.status_code)
            # if self.TopPrintStdOut:   
            #     print("self.std_out = %s" % self.std_out)                                            
                
            if ResultWinrmCommand.status_code != 0 : 
                self.ExecutionCommandSucess= False
                # if self.TopPrintStdErr:
                #     print("self.std_err = %s" % self.std_err)
            else :
                self.ExecutionCommandSucess= True
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, False)
            raise

    def WinRM_Get_Session(self) :

        """This function will create WinRM Session
        """

        try : 
            #print("entrée dans WinRM_Get_Session")
            winrm_session = winrm.Session('http://' + self.IP + ':5985+/wsman' , auth=(self._useransible, self._passansible))
            p = self.WinRM_GetProtocol()
            return (winrm_session)
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, False)
            raise

    def WinRM_GetProtocol(self) :

        """This function will get the protocol
        """

        try :
            #print("entrée dans WinRM_GetProtocol")
            p = winrm.Protocol(endpoint='http://' + self.IP + ':5985/wsman',
                        transport='credssp',
                        username=self._useransible,
                        password=self._passansible,
                        server_cert_validation='ignore',
                        message_encryption='auto')
            return (p)
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, False)
            raise
