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


class EntityClass:
    """
    https://www.circitor.fr/Mibs/Html/A/ADVA-MIB.php#EntityClass
    """
    UNDEFINED = 0
    OTHER = 1
    UNKNOWN = 2
    CHASSIS = 3
    BACKPLANE = 4
    CONTAINER = 5
    POWER_SUPPLY = 6
    FAN = 7
    SENSOR = 8
    MODULE = 9
    PLUG = 10
    STACK = 11
    GROUP = 12
    CLIENT_PORT = 13
    NETWORK_PORT = 14
    VIRTUAL_CHANNEL = 15
    CONNECTION = 16
    VC4_CONTAINER = 17
    VC3STS1_CONTAINER = 18
    VC12VT15_CONTAINER = 19
    DCN_CHANNEL = 20
    ROUTER_CONFIG = 21
    ENVIRONMENT_PORT = 22
    INTERNAL_PORT = 23
    UPGRADE_PORT = 24
    MIDSTAGE_PORT = 25
    SERIAL_PORT = 26
    PPP_IP_INTERFACE = 27
    LAN_IP = 28
    VS1_CONTAINER = 29
    STS3C_CONTAINER = 30
    PAYLOAD_CHANNEL = 31
    PASSIVE_SHELF = 32
    STS24C_CONTAINER = 33
    STS48C_CONTAINER = 34
    VS2C_CONTAINER = 35
    VS4C_CONTAINER = 36
    TIF_INPUT_PORT = 37
    TIF_OUTPUT_PORT = 38
    OPTICAL_LINK = 39
    VIRTUAL_OPTICAL_CHANNEL = 40
    LOGICAL_INTERFACE = 41
    PHYSICAL_TERMINATION_POINT = 42
    ETH_CLIENT = 43
    ETH_NETWORK = 44
    VETH = 45
    FLOW = 47
    CTRANS = 48
    POLICER_ON_FLOW = 50
    QUEUE_ON_PORT = 51
    QUEUE_ON_FLOW = 52
    FAR_END_PLUG = 53
    FAR_END_CHANNEL = 54
    VC4C8_CONTAINER = 55
    VC4C16_CONTAINER = 56
    VS0_CONTAINER = 57
    VIRTUAL_SUB_CHANNEL = 58
    BRIDGE = 59
    QUEUE_ON_BRIDGE = 60
    BACKWARD_VIRTUAL_OPT_MUX = 61
    FORWARD_VIRTUAL_OPT_MUX = 62
    OPT_CHANNEL_TRANSPORT_LANE = 63
    VIRTUAL_CHANNEL_N = 64
    EXTERNAL_CHANNEL = 65
    VIRTUAL_TERMINATION_POINT = 66
    VIRTUAL_CONNECTION = 67
