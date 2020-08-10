"""
Code translations for defined types in ADVA MIBs
"""

class AdminState:
    """
    http://www.circitor.fr/Mibs/Html/A/ADVA-FSPR7-TC-MIB.php#FspR7AdminState
    Translations assisted by browsing the Adva FSP Network Manager client.
    """
    UNDEFINED = 0
    UNASSIGNED = 1
    IN_SERVICE = 2
    AUTO_IN_SERVICE = 3
    OUT_OF_SERVICE_MANAGEMENT = 4
    OUT_OF_SERVICE_MAINTENANCE = 5
    DISABLED = 6
    PRE_POST_SERVICE = 7


class AssignmentState:
    """
    http://www.circitor.fr/Mibs/Html/A/ADVA-MIB.php#AssignmentState
    """
    UNDEFINED = 0
    ASSIGNED = 1
    UNASSIGNED = 2
    NOT_ASSIGNABLE = 3


class EquipmentState:
    """
    http://www.circitor.fr/Mibs/Html/A/ADVA-MIB.php#EquipmentState
    """
    UNDEFINED = 0
    EQUIPPED = 1
    UNEQUIPPED = 2
