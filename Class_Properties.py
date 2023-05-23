##########################################################################
# * Importation des bibliotheques
##########################################################################

import sys
import paramiko
from Class_Security import Class_Security
from Class_Servers import Class_Servers

##########################################################################
# * Début du script
##########################################################################

class Class_Properties(Exception):

    """This class will do ....
    
    """
    def __init__(self, ObjLog, MonWinRM):
        self._MyObjLog = ObjLog
        self.MonWinRM = MonWinRM
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        self._useransible = Class_Security().UserAnsible
        self._passansible = Class_Security().PassAnsible

    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    def get_MonWinRM(self):
        return self._MonWinRM
    def get_useransible(self):
        return self._useransible
    def get_passansible(self):
        return self._passansible
    
    # ? setter method
    def set_MyObjLog(self, value):
        if (type(value) == type(self._MonWinRM)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MyObjLog = value
        else :
            raise "Property Error"
    def set_MonWinRM(self, value):
        if (type(value) == type(self._MonWinRM)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MonWinRM = value
        else :
            raise "Property Error"
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
    
    
    def ServiceLinux(self, NameOfService, IPServer, state):
        
        """This function will start a linux service

        Args:
            IPServer (str): IP of server
            nameofservice (str): name of service
            state (str): State of service

        Raises:
            connection error or permission denied
        """

        try :
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, self._useransible, self._passansible)
            stdin, stdout, stderr = ssh.exec_command(f"systemctl {state} {NameOfService}")
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors du {state} du service {NameOfService} sur Linux", self.TopExit, True, self.TopPrintLog)
                raise 
            else :
                self._MyObjLog.AjouteLog(f"OK - {state} du service {NameOfService} sur Linux", self.TopExit, True, self.TopPrintLog)
                raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err

    def ServiceWindows(self, NameOfService, IPServer, state):

        """This function will start a windows service

        Args:
            IPServer (str): IP of server
            nameofservice (str): name of service
            state (str): State of service

        Raises:
            connection error or permission denied
        """

        try :
            self._MonWinRM.IP = IPServer
            mycmd = f"net start {NameOfService}"
            self._MonWinRM.Run_WinRM_CMD_Session(mycmd)
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - {state} du service {NameOfService} sur Windows", self.TopExit, self.TopRaise, self.TopPrintLog)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors du {state} du service {NameOfService} sur Windows", self.TopExit, True, self.TopPrintLog)
                raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err

    def FireWallWindows(self, IPServer, state):

        """This function will start a windows fire wall

        Args:
            IPServer (str): IP of server
            state (str): State of service

        Raises:
            connection error or permission denied
        """

        try :
            self._MonWinRM.IP = IPServer
            mycmd = "netsh advfirewall set allprofiles state on"
            self._MonWinRM.Run_WinRM_CMD_Session(mycmd)
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - {state} du pare-feu sur Windows", self.TopExit, self.TopRaise, self.TopPrintLog)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors du {state} du pare-feu sur Windows", self.TopExit, True, self.TopPrintLog)
                raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err

    def FireWallLinux(self, IPServer, state):
        
        """This function will start a linux fire wall

        Args:
            IPServer (str): IP of server
            state (str): State of service

        Raises:
            connection error or permission denied
        """
        
        try :
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, self._useransible, self._passansible)
            stdin, stdout, stderr = ssh.exec_command("service ufw start")
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors du {state} du pare-feu sur Linux", self.TopExit, True, self.TopPrintLog)
                raise
            else :
                self._MyObjLog.AjouteLog(f"OK - {state} du pare-feu sur Linux", self.TopExit, True, self.TopPrintLog)
                raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err

    def Check_Exist_Service_For_Windows(self, NameOfService, IPServer):

        """This function will check if the service exist on the windows machine

        Args:
            NameOfService (str): name of service
            IPServer (str): IP of server

        Raises:
            connection error or permission denied
        """

        try :
            self._MonWinRM.IP = IPServer
            mycmd = "Get-Service | Where Status -eq 'Running' | Select Name"
            self._MonWinRM.Run_WinRM_PS_Session(mycmd, False)
            if NameOfService in self._MonWinRM.std_out:
                self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est présent sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                return True
            else :
                self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} n'est pas présent sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                return False
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err

    def Check_Exist_Service_For_Linux(self, NameOfService, IPServer):

        """This function will check if the service exist on the linux machine

        Args:
            NameOfService (str): name of service
            IPServer (str): IP of server

        Raises:
            connection error or permission denied
        """

        try :
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, self._useransible, self._passansible)
            stdin, stdout, stderr = ssh.exec_command("service ufw start")
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors du lancement du pare-feu sur Linux", self.TopExit, True, self.TopPrintLog)
                raise 
            else :
                serviceslist = stdout.readlines()
                separator = ""
                services = separator.join(serviceslist)
                if NameOfService in services:
                    self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est présent sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                    return True
                else :
                    self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} n'est pas présent sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                    return False
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err

    def Check_State_Service_Windows(self, NameOfService, IPServer):

        """This function will check if the state of service on windows machine

        Args:
            NameOfService (str): name of service
            IPServer (str): IP of server

        Raises:
            connection error or permission denied or service doesn't exist
        """

        try :
            self._MonWinRM.IP = IPServer
            mycmd = f'Get-Service {NameOfService} | Select status'
            self._MonWinRM.Run_WinRM_PS_Session(mycmd, False)
            if "Running" in self._MonWinRM.std_out:
                self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est en cours d'éxecution sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                return "Running"
            elif "Paused" in self._MonWinRM.std_out: #! VOIR SI C4EST LE BON STATUS
                self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est en pause sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                return "Paused"
            elif "Stopped" in self._MonWinRM.std_out:
                self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est arreté sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                return "Stopped"
            else :
                self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} n'est pas présent sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                return False
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err

    def Check_State_Service_Linux(self, NameOfService, IPServer):

        """This function will check if the state of service on linux machine

        Args:
            NameOfService (str): name of service
            IPServer (str): IP of server

        Raises:
            connection error or permission denied or service doesn't exist
        """

        try :
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, self._useransible, self._passansible)
            stdin, stdout, stderr = ssh.exec_command(f"service {NameOfService} status | grep Active:")
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors du lancement du pare-feu sur Linux", self.TopExit, True, self.TopPrintLog)
            else :
                serviceslist = stdout.readlines()
                separator = ""
                services = separator.join(serviceslist)
                if "running" in services:
                    self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est en cours d'éxecution sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                    return ("Running")
                elif "Paused" in self._MonWinRM.std_out: #! VOIR SI C4EST LE BON STATUS
                    self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est en pause sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                    return "Paused"
                elif "dead" in services:
                    self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} est arreté sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                    return ("Running")
                else :
                    self._MyObjLog.AjouteLog(f"OK - Le service {NameOfService} n'est pas présent sur la machine", self.TopExit, self.TopRaise, self.TopPrintLog)
                    return False
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise err
