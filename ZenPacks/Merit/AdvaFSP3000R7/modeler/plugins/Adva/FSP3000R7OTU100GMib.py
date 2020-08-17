######################################################################
#
# FSP3000R7OTU100GMib modeler plugin
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7OTU100GMib

FSP3000R7OTU100GMib maps 100G Muxsponder OTU ports on a FSP3000R7 system

"""

from re import match
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import AssignmentState
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import EquipmentState


# Use SNMP data from Device Modeler in a cache file.  Can't be a PythonPlugin
# since those run before any SnmpPlugin; device modeler is an PythonPlugin so
# the cache file will be created before this is run.
# Need to override FSP3000R7MibCommon.process() since some Muxsponder OTU ports
# don't respond to OPR.
class FSP3000R7OTU100GMib(FSP3000R7MibCommon):

    modname = 'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7OTU100Gig'
    relname = 'FSP3000R7OTU100G'

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0.  Not used;
    # Have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})

    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # These models contain OTU100G amplifiers to look for network ports on
        componentModels = ['10TCC-PCTN-10G+100GB',
                           '10TCC-PCTN-10G+100GC',
                           '10TCE-PCN-10G+100G',
                           '10TCE-PCN-10G+100G-GF',
                           '10TCE-PCN-16GU+100G',
                           'WCC-PCTN-100GA',
                           'WCC-PCTN-100GB',
                           'MP-2B4CT']

        # SNMP table
        getdata, tabledata = results

        # cached data from device modeler
        inventoryTable = entityTable = opticalIfDiagTable = False
        containsOPRModules = {}
        gotCache, inventoryTable, entityTable, opticalIfDiagTable, \
            containsOPRModules = getCache(device.id, self.name(), log)
        if not gotCache:
            log.debug('Could not get cache for %s' % self.name())
            return

        # relationship mapping
        rm = self.relMap()

        # look for blades containing 100G Muxponder in inventory table
        for bladeEntityIndex in inventoryTable:
            bladeInv = inventoryTable[bladeEntityIndex]['inventoryUnitName']
            bladeIndexAid = entityTable[bladeEntityIndex]['entityIndexAid']
            if not bladeInv in componentModels:
                continue

            # Skip blade if out of service
            if not self._entity_is_in_service(bladeIndexAid, adminStateTable):
                continue

            log.info('found 100G Muxponder OTU matching model %s in module %s', bladeInv, bladeIndexAid)
    
            # find ports from entityContainedIn for 100G OTU entityIndex
            ports = self.__findPorts(log,bladeEntityIndex,entityTable)

            if not ports:
                continue

            for portEntityIndex, portEntityIndexAid in ports:
                om = self.objectMap()
                om.EntityIndex = int(portEntityIndex)
                om.inventoryUnitName = bladeInv
                if 'interfaceConfigIdentifier' in entityTable[portEntityIndex]:
                    om.interfaceConfigId = entityTable[portEntityIndex]['interfaceConfigIdentifier']
                om.entityIndexAid=entityTable[portEntityIndex]['entityIndexAid']
                om.entityAssignmentState = entityTable[portEntityIndex]['entityAssignmentState']
                om.id = self.prepId(om.entityIndexAid)
                om.title = om.entityIndexAid
                om.snmpindex = int(portEntityIndex)
                log.info('Found 100Gig Muxponder OTU port at: %s inventoryUnitName: %s',
                         om.entityIndexAid, om.inventoryUnitName)

                rm.append(om)

        return rm


    def __findPorts(self, log, parentEntityIndex, entityTable):
        """
        Follow the entityContainedIn chain and collect components with
        entityIndexAid like "CH-1-1-N*". If we see an entity that is either not
        assigned or unequipped, don't go any deeper into that component chain.
        """
        ports = []
        parentEntityIndex = str(parentEntityIndex)
        for entityIndex, entityAttrs in entityTable.items():
            entityContainedIn = str(entityAttrs['entityContainedIn'])
            if entityContainedIn == parentEntityIndex:
                entity_is_not_assigned = entityAttrs['entityAssignmentState'] != AssignmentState.ASSIGNED
                entity_is_unequipped = entityAttrs['entityEquipmentState'] == EquipmentState.UNEQUIPPED

                if entity_is_unequipped or entity_is_not_assigned:
                    continue

                if (match(r'CH\-\d+\-\d+\-N', entityAttrs['entityIndexAid'])):
                    ports.append((entityIndex, entityAttrs['entityIndexAid']))
                else:
                    ports.extend(self.__findPorts(log, entityIndex, entityTable))

        return ports
