"""
Code translations for defined types in ADVA-MIB
"""

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
