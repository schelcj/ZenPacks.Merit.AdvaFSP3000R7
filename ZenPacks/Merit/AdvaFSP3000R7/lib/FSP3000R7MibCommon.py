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

        cache = getCache(device.id, self.name(), log)
        if not cache:
            log.debug('Could not get cache for %s' % self.name())
            return

        # relationship mapping
        rm = self.relMap()

        for entityIndex, inventoryUnitName in cache['inventoryTable'].items():
            entityIndex_str = str(entityIndex)
            invName = inventoryUnitName['inventoryUnitName']
            modName = cache['entityTable'][entityIndex]['entityIndexAid']
            # if model name matches, assigned and equiped:
            if self._model_match(invName, self.componentModels) \
              and entityIndex in cache['entityTable'] \
              and 'entityAssignmentState' in cache['entityTable'][entityIndex] \
              and 'entityEquipmentState' in cache['entityTable'][entityIndex] \
              and cache['entityTable'][entityIndex]['entityAssignmentState'] == AssignmentState.ASSIGNED \
              and cache['entityTable'][entityIndex]['entityEquipmentState'] == EquipmentState.EQUIPPED:
                # only add MOD name if power supply, fan or NCU
                if self.__class__.__name__ in ['FSP3000R7PowerSupplyMib',
                                               'FSP3000R7FanMib',
                                               'FSP3000R7NCUMib']:
                  om = self.objectMap()
                  om.EntityIndex = int(entityIndex)
                  om.inventoryUnitName = invName
                  # Add comment (e.g. 'RAMAN from Niles') if one exists
                  if 'interfaceConfigIdentifier' in cache['entityTable'][entityIndex]:
                      om.interfaceConfigId = \
                          cache['entityTable'][entityIndex]['interfaceConfigIdentifier']
                  om.entityIndexAid = modName
                  om.sortKey = self._make_sort_key(modName)
                  om.entityAssignmentState = \
                      cache['entityTable'][entityIndex]['entityAssignmentState']
                  om.id = self.prepId(modName)
                  om.title = modName 
                  om.snmpindex = int(entityIndex)
                  log.info('Found component at: %s inventoryUnitName: %s',
                           modName, invName)

                  rm.append(om)

                # Now find sub-organizers that respond to OPR
                if modName not in cache['containsOPRModules']:
                    continue
                for entityIndex in cache['containsOPRModules'][modName]:
                    # skip non-production components
                    entity_assigned = (
                        entityIndex in cache['entityTable']
                        and cache['entityTable'][entityIndex].get('entityAssignmentState') == AssignmentState.ASSIGNED
                    )

                    # Sub-organizers with EquipmentState.UNDEFINED or no equipment state should be considered valid
                    entity_equipped = (
                        entityIndex in cache['entityTable']
                        and cache['entityTable'][entityIndex].get('entityEquipmentState') in (
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
                    if 'interfaceConfigIdentifier' in cache['entityTable'][entityIndex]:
                        om.interfaceConfigId = \
                           cache['entityTable'][entityIndex]['interfaceConfigIdentifier']
                    om.entityIndexAid = cache['entityTable'][entityIndex]['entityIndexAid']
                    om.sortKey = self._make_sort_key(om.entityIndexAid)
                    om.entityAssignmentState = \
                        cache['entityTable'][entityIndex]['entityAssignmentState']
                    om.id = self.prepId(om.entityIndexAid)
                    om.title = om.entityIndexAid
                    om.snmpindex = int(entityIndex)
                    log.info('Found component at: %s inventoryUnitName: %s',
                             om.entityIndexAid, invName)

                    rm.append(om)

        return rm

    def _model_match(self,inventoryUnitName,componentModels):
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

    def _make_sort_key(self,entityIndexAid):
        """
        Return a string to sort on. We generally want the first element placed last to
        prioritize the shelf and slot numbers (the second two fields) rather than the
        component type.

        Examples:
          'MOD-1-7'         -> '001007MOD'
          'VCH-1-7-C1'      -> '001007C1VCH'
          'VCH-1-7-N-19200' -> '001007N-19200VCH'
        """
        parts = entityIndexAid.split('-', 3)

        if len(parts) < 3:
            return ''

        type = parts[0]
        shelf_slot = parts[1].zfill(3) + parts[2].zfill(3)
        remainder = ''.join(parts[3:])

        return shelf_slot + remainder + type
