##########################################################################
# * Importation des bibliotheques
##########################################################################

import mysql.connector
from mysql.connector import errorcode
import sys

##########################################################################
# * Début du script
##########################################################################

class Class_MySQL(Exception):

    def __init__(self, MyObjLog):
        self._MyObjLog = MyObjLog
        self.UserBDD = "XXXXXX"
        self.PasswdBDD = "XXXXXX"
        self.HostBDD = "XXXXXX"
        self.NameBDD = "XXXXXX"
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False

    def mysqlconnector(self):

        """This function will etablish a connection with DB

        Raises:
            Exception: Connection error

        Return:
            Obj: db is the object of connection
        """
        
        try:
            connection_params = {
            'host': self.HostBDD,
            'user': self.UserBDD,
            'password': self.PasswdBDD,
            'database': self.NameBDD,
            }

            db = mysql.connector.connect(**connection_params)
            return db
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def SelectRow(self, db, query, column=False):

        """This function will select a row in DB

        Args:
            db (obj): The object of connection
            query (str): DB query
            column (bool): If we want to have the name of column

        Raises:
            Exception: Select error
        """

        try: 
            c = db.cursor()
            c.execute(query)
            if column == False : 
                myresult = c.fetchall()
            else : 
                myresult = c.fetchall(), c.column_names
            return myresult
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def InsertRow(self, db, query):

        """This function will insert a row in DB

        Args:
            db (obj): The object of connection
            query (str): DB query

        Raises:
            Exception: INSERT error
        """

        try: 
            db.cursor().execute(query)
            db.commit()
            db.close() 
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise

    def UpdateRow(self, db, query):
        
        """This function will Update a row in DB

        Args:
            db (obj): The object of connection
            query (str): DB query

        Raises:
            Exception: Update error
        """

        try: 
            db.cursor().execute(query)
            db.commit()
            db.close() 
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise

    def DeleteRow(self, db, query):
        
        """This function will Delete a row in DB

        Args:
            db (obj): The object of connection
            query (str): DB query

        Raises:
            Exception: Delete error
        """

        try: 
            db.cursor().execute(query)
            db.commit()
            db.close() 
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True, self.TopPrintLog)
            raise
