######################################################################
#
# FSP3000R7MibCommon modeler plugin
#
######################################################################

__doc__="""FSP3000R7MibCommon

FSP3000R7MibCommon is a modeler base class to find components on an
Adva FSP3000R7 system. It uses stored SNMP data from an Adva system in a
file in /tmp so if there is more than one component to be modeled, the
subsequent components will not have to get the same information over and over.
Without this, a system may respond so slowly that modeling times out in
Zenoss.  The stored SNMP data is created by the Adva device modeler which
must be run first."""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7Channels import Channels
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import AdminState
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import AssignmentState
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import EquipmentState


# Use SNMP data from Device Modeler in a cache file.  Can't be a PythonPlugin
# since those run before any SnmpPlugin; device modeler is an PythonPlugin so
# the cache file will be created before this is run.
class FSP3000R7MibCommon(SnmpPlugin):

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

        inventoryTable = entityTable = opticalIfDiagTable = False
        containsOPRModules = {}
        gotCache, inventoryTable, entityTable, opticalIfDiagTable, adminStateTable, \
            containsOPRModules = getCache(device.id, self.name(), log)
        if not gotCache:
            log.debug('Could not get cache for %s' % self.name())
            return

        # relationship mapping
        rm = self.relMap()

        for entityIndex, inventoryUnitName in inventoryTable.items():
            entityIndex_str = str(entityIndex)
            invName = inventoryUnitName['inventoryUnitName']
            modName = entityTable[entityIndex]['entityIndexAid']
            # if model name matches, assigned and equiped:
            if self.__model_match(invName, self.componentModels) \
              and entityIndex in entityTable \
              and 'entityAssignmentState' in entityTable[entityIndex] \
              and 'entityEquipmentState' in entityTable[entityIndex] \
              and entityTable[entityIndex]['entityAssignmentState'] == AssignmentState.ASSIGNED \
              and entityTable[entityIndex]['entityEquipmentState'] == EquipmentState.EQUIPPED:
                # only add MOD name if power supply, fan or NCU
                if self.__class__.__name__ in ['FSP3000R7PowerSupplyMib',
                                               'FSP3000R7FanMib',
                                               'FSP3000R7NCUMib']:
                  om = self.objectMap()
                  om.EntityIndex = int(entityIndex)
                  om.inventoryUnitName = invName
                  # Add comment (e.g. 'RAMAN from Niles') if one exists
                  if 'interfaceConfigIdentifier' in entityTable[entityIndex]:
                      om.interfaceConfigId = \
                          entityTable[entityIndex]['interfaceConfigIdentifier']
                  om.entityIndexAid = modName
                  om.sortKey = self.__make_sort_key(modName)
                  om.entityAssignmentState = \
                      entityTable[entityIndex]['entityAssignmentState']
                  om.id = self.prepId(modName)
                  om.title = modName 
                  om.snmpindex = int(entityIndex)
                  log.info('Found component at: %s inventoryUnitName: %s',
                           modName, invName)

                  rm.append(om)

                # Now find sub-organizers that respond to OPR
                if modName not in containsOPRModules:
                    continue

                # Skip modules that are out of service
                if not self._entity_is_in_service(modName, adminStateTable):
                    continue

                for entityIndex in containsOPRModules[modName]:
                    # skip non-production components
                    entity_assigned = (
                        entityIndex in entityTable
                        and entityTable[entityIndex].get('entityAssignmentState') == AssignmentState.ASSIGNED
                    )

                    # Sub-organizers with EquipmentState.UNDEFINED or no equipment state should be considered valid
                    entity_equipped = (
                        entityIndex in entityTable
                        and entityTable[entityIndex].get('entityEquipmentState') in (
                            None,
                            EquipmentState.UNDEFINED,
                            EquipmentState.EQUIPPED,
                        )
                    )

                    if not (entity_assigned and entity_equipped):
                        continue;

                    om = self.objectMap()
                    om.EntityIndex = int(entityIndex)
                    om.inventoryUnitName = invName
                    if 'interfaceConfigIdentifier' in entityTable[entityIndex]:
                        om.interfaceConfigId = \
                           entityTable[entityIndex]['interfaceConfigIdentifier']
                    om.entityIndexAid=entityTable[entityIndex]['entityIndexAid']
                    om.sortKey = self.__make_sort_key(om.entityIndexAid)
                    om.entityAssignmentState = \
                        entityTable[entityIndex]['entityAssignmentState']
                    om.id = self.prepId(om.entityIndexAid)
                    om.title = om.entityIndexAid
                    om.snmpindex = int(entityIndex)
                    log.info('Found component at: %s inventoryUnitName: %s',
                             om.entityIndexAid, invName)

                    rm.append(om)

        return rm

    def _entity_is_in_service(self, entityIndexAid, adminStateTable):
        """
        To be considered "in service", adminState must either be undefined,
        non-existent, in service, or automatically in service. This seems to
        only exist for module-level components like "MOD-2-2", "MOD-1-PSU10".
        """
        return self._get_admin_state(entityIndexAid, adminStateTable) in (
            AdminState.UNDEFINED,
            AdminState.AUTO_IN_SERVICE,
            AdminState.IN_SERVICE,
        )

    def _get_admin_state(self, entityIndexAid, adminStateTable):
        """
        Since the table containing adminStatus uses a different indexing system,
        use the entityEqptAidString to match the alternate index and return the
        adminState if available.
        """
        for index, attributes in adminStateTable.items():
            if entityIndexAid == attributes.get('entityEqptAidString'):
                return attributes.get('moduleDefAdmin', AdminState.UNDEFINED)

        return AdminState.UNDEFINED

    def __model_match(self,inventoryUnitName,componentModels):
        for model in componentModels:
            # Test different channel variations if there's a # on end
            if model.endswith('#'):
                all_ch = Channels.dwdm_old_channels+Channels.cwdm_channels
                for ch in all_ch:
                    model_var = model + ch
                    if inventoryUnitName == model_var:
                        return True
            if inventoryUnitName == model:
                return True
        return False

    def __make_sort_key(self,entityIndexAid):
        """Return a string to sort on, e.g. 'MOD-1-3' -> '001003000000'
and 'VCH-1-7-N1' -> ' 1 7VCH N1'"""
        a = entityIndexAid.split('-',4)
        if len(a) < 3:
            return '000000000'
        if entityIndexAid.startswith('MOD-') or entityIndexAid.startswith('FAN-') or entityIndexAid.startswith('MODC-') or entityIndexAid.startswith('FANC-'):
            return "%03s%03s%03s000" % (a[1],a[2],a[0])
        return "%03s%03s%03s%03s" % (a[1],a[2],a[0],a[3])
