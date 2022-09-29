################################################################################
#
# Used for 'Display' drop-down in 'Components' section of GUI.
# Has nothing to do with interfaces on a device.
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field on the user interface.

"""

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IFSP3000R7ComponentInfo(IComponentInfo):
    """Base class for FSP3000R7 info adpators"""
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')
    snmpindex = schema.Text(title    = u"SNMP Index",
                            readonly = True,
                            group    = 'Details')

class IModuleInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Module (container) component """
    pass

class IOSCInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Optical Service Channel component """
    pass

class IPowerSupplyInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Power Supply component """
    pass

class IAmplifierInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Amplifier component """
    pass

class IRamanNPortInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Raman Amplifier Network Port component """
    pass

class IRamanUPortInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Raman Amplifier Upgrade Port component """
    pass

class IRoadmInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for ROADM component """
    pass

class ITransponderInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Transponder component """
    pass

class ITransponderVCHInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Transponder VCH component """
    pass

class IOTU100GInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for 100G Transponder OTU component."""
    pass

class IOptical100GInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for 100G Transponder Optical component """
    pass

class INCUInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for NCU component """
    pass

class IVCHInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for VCH component """
    pass

class IFanInfo(IFSP3000R7ComponentInfo):
    """ Info adapter for Fan NCU component """
    pass
