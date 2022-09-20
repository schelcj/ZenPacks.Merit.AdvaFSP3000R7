################################################################################
#
# File used to display information in GUI for Adva FSP3000R7 components
# Gets information from ZODB to be displayed to the user.
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of FSP3000R7 components.

"""

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.Merit.AdvaFSP3000R7 import interfaces


class ModuleInfo(ComponentInfo):
    implements(interfaces.IModuleInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    snmpindex = ProxyProperty("snmpindex")

class OSCInfo(ComponentInfo):
    implements(interfaces.IOSCInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class PowerSupplyInfo(ComponentInfo):
    implements(interfaces.IPowerSupplyInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    snmpindex = ProxyProperty("snmpindex")

class AmplifierInfo(ComponentInfo):
    implements(interfaces.IAmplifierInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class RamanNPortInfo(ComponentInfo):
    implements(interfaces.IRamanNPortInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class RamanUPortInfo(ComponentInfo):
    implements(interfaces.IRamanUPortInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class RoadmInfo(ComponentInfo):
    implements(interfaces.IRoadmInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class TransponderInfo(ComponentInfo):
    implements(interfaces.ITransponderInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class TransponderVCHInfo(ComponentInfo):
    implements(interfaces.ITransponderVCHInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class OTU100GInfo(ComponentInfo):
    implements(interfaces.IOTU100GInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class Optical100GInfo(ComponentInfo):
    implements(interfaces.IOptical100GInfo)
    snmpindex = ProxyProperty("snmpindex")

class NCUInfo(ComponentInfo):
    implements(interfaces.INCUInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class VCHInfo(ComponentInfo):
    implements(interfaces.IVCHInfo)
    inventoryUnitName = ProxyProperty("inventoryUnitName")
    interfaceConfigId = ProxyProperty("interfaceConfigId")
    snmpindex = ProxyProperty("snmpindex")

class FanInfo(ComponentInfo):
    implements(interfaces.IFanInfo)
    snmpindex = ProxyProperty("snmpindex")
