
import hashlib
import pandas as pd
import logging


class Helper():
    #Diese Klasse bietet diverse Funktionen an

    def Create_Checksum(self,str_toHash : str) -> str:
        """Diese Funktion gibt eine 16-stellige Checksum für einen String zurück
        
        Input:
        String mit nur ASCII Zeichen
        
        Output:
        16-stellige Checksum"""
        return hashlib.md5(str_toHash.encode('ascii')).hexdigest()

    def Check_Checksums(self,to_Check, path):
        """Diese Funktion kontrolliert ob eine gegebene Checksum in der ebenfalls übergebenen liste enthalten ist
        Input:
        to_Check = Variable die die Checksum enthält die kontrolliert werden soll
        li_toCheckAgainst = Liste mit vorhandenen Checksums
        
        Output:
        "True" wenn die Checksum bereits vorhanden ist
        "False" wenn es die Checksum noch nicht gibt"""

        df_temp = pd.read_csv(path,sep = ";")
        li_toCheckAgainst = list(df_temp["Checksum"])

        if to_Check in li_toCheckAgainst:
            return True
        else:
            return False

  

file_handler = logging.FileHandler("logfile.log")

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.critical("Something critical")
logger.error("An error")
logger.warning("A warning")
logger.info("My info is that you are here")
logger.debug("I'm debugging")

global obj_helper
obj_helper = Helper()
