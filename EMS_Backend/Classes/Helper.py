
import hashlib
  



class Helper():
    #Diese Klasse bietet diverse Funktionen an

    def Create_Checksum(self,str_toHash : str) -> str:
        """Diese Funktion gibt eine 16-stellige Checksum für einen String zurück
        
        Input:
        String mit nur ASCII Zeichen
        
        Output:
        16-stellige Checksum"""
        return hashlib.md5(str_toHash.encode('ascii')).hexdigest()

    def Check_Checksums(self,to_Check, li_toCheckAgainst):
        """Diese Funktion kontrolliert ob eine gegebene Checksum in der ebenfalls übergebenen liste enthalten ist
        Input:
        to_Check = Variable die die Checksum enthält die kontrolliert werden soll
        li_toCheckAgainst = Liste mit vorhandenen Checksums
        
        Output:
        "True" wenn die Checksum bereits vorhanden ist
        "False" wenn es die Checksum noch nicht gibt"""
        if to_Check in li_toCheckAgainst:
            return True
        else:
            return False

global obj_helper
obj_helper = Helper()



print(obj_helper.Check_Checksums("5", ["4","8","4","45","8","1","4","7","5"]))