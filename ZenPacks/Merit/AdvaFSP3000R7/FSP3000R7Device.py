######################################################################
#
# FSP3000R7Device object class
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

from Globals import InitializeClass
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class FSP3000R7Device(Device,ZenPackPersistence):
    "A FSP3000R7 Device"

    meta_type = 'FSP3000R7Device'

    _relations = Device._relations + (
        ('FSP3000R7Mod',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Module',
                    'FSP3000R7Dev')),
        ('FSP3000R7Amp',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Amplifier',
                    'FSP3000R7Dev')),
        ('FSP3000R7RamanNPort',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7RamanNPort',
                    'FSP3000R7Dev')),
        ('FSP3000R7RamanUPort',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7RamanUPort',
                    'FSP3000R7Dev')),
        ('FSP3000R7Ncu',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7NCU',
                    'FSP3000R7Dev')),
        ('FSP3000R7Osc',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7OSC',
                    'FSP3000R7Dev')),
        ('FSP3000R7Trans',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Transponder',
                    'FSP3000R7Dev')),
        ('FSP3000R7TransponderVchRel',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7TransponderVch',
                    'FSP3000R7Dev')),
        ('FSP3000R7OTU100G',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7OTU100Gig',
                    'FSP3000R7Dev')),
        ('FSP3000R7Optical100G',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Optical100Gig',
                    'FSP3000R7Dev')),
        ('FSP3000R7Road',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Roadm',
                    'FSP3000R7Dev')),
        ('FSP3000R7VchRel',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Vch',
                    'FSP3000R7Dev')),
        ('FSP3000R7PwrSupply',
         ToManyCont(ToOne,
                    'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7PowerSupply',
                    'FSP3000R7Dev')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(FSP3000R7Device)
