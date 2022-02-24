######################################################################
#
# FSP3000R7RoadmMib modeler pluginn
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R70RoadmVchMib

FSP3000R7VchMib maps Virtual Channels on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon
from Products.DataCollector.plugins.CollectorPlugin import GetMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache


class FSP3000R7VchMib(FSP3000R7MibCommon):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Vch"
    relname = "FSP3000R7VchRel"

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0.  Not used;
    # Have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})

    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # tabledata is not used (get tables from cache pickle file created
        # in FSP3000R7Device modeler)
        getdata = {}
        getdata['setHWTag'] = False
        getdata, tabledata = results
        if not getdata['setHWTag']:
            log.info("Couldn't get system name from Adva shelf.")

        gotCache, inventoryTable, entityTable, opticalIfDiagTable, \
            facilityTable, facilityPhysInstValueTable, containsOPRModules = getCache(device.id, self.name(), log)
        if not gotCache:
            log.debug('Could not get cache for %s' % self.name())
            return

        # relationship mapping
        rm = self.relMap()

        for index, attrs in facilityTable.items():
            aid_string = attrs.get('entityFacilityAidString', '')

            om = self.objectMap()
            om.EntityIndex = index
            om.interfaceConfigId = attrs.get('virtualPortAlias', '')
            om.entityIndexAid = aid_string
            sort_key = self._make_sort_key(aid_string)
            om.sortKey = sort_key
            om.id = self.prepId(aid_string)
            om.title = aid_string
            om.snmpindex = index

            log.info("Found virtual channel %s", aid_string)
            rm.append(om)

        return rm
