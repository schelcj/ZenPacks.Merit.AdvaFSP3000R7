######################################################################
#
# FSP3000R7VchMib modeler pluginn
#
# Copyright (C) 2022 Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7VchMib

FSP3000R7VchMib maps Virtual Channels on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon
from Products.DataCollector.plugins.CollectorPlugin import GetMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import AdminState
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import EntityClass


class FSP3000R7VchMib(FSP3000R7MibCommon):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Vch"
    relname = "FSP3000R7VchRel"

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0.  Not used;
    # Have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})

    # Since Virtual Channels on older cards might already by detected by other
    # plugins (like FSP3000R7Transponder, FSP3000R7Roadm), only allow this plugin
    # to detect channels on specific (newer) models.
    allowed_unit_names = [
        '9ROADM-RS',
        'MA-B5LT',
    ]

    allowed_entity_classes = [
        EntityClass.VIRTUAL_CHANNEL,
        EntityClass.VIRTUAL_CHANNEL_N,
    ]

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
            log.error('Could not get cache for %s' % self.name())
            return

        # relationship mapping
        rm = self.relMap()

        for index, attrs in cache['facilityTable'].items():
            aid_string = attrs.get('entityFacilityAidString', '')
            unit_name = attrs.get('inventoryUnitName', '')
            facility_class = attrs.get('entityFacilityClass', '')
            virtual_port_alias = attrs.get('virtualPortAlias', '')

            if facility_class not in self.allowed_entity_classes:
                log.info('Skipping non-virtual component %s' % aid_string)
                continue

            if not self._is_admin_in_service(attrs.get('virtualPortAdmin')):
                log.info('Skipping out-of-service component %s ' % aid_string)
                continue

            if unit_name not in self.allowed_unit_names:
                log.info(
                    'Skipping component %s from model %s since it is not contained in any of: %s, full attrs are %s' % (
                        aid_string,
                        unit_name,
                        self.allowed_unit_names,
                        attrs,
                    )
                )
                continue

            om = self.objectMap()
            om.EntityIndex = index
            om.interfaceConfigId = virtual_port_alias
            om.entityIndexAid = aid_string
            om.inventoryUnitName = unit_name
            sort_key = self._make_sort_key(aid_string)
            om.sortKey = sort_key
            om.id = self.prepId(aid_string)
            om.title = aid_string
            om.snmpindex = index

            log.info("Found virtual channel %s", aid_string)
            rm.append(om)

        return rm

    def _is_admin_in_service(self, adminState=None):
        """Compare status code with AdminState mappings"""
        if adminState in [AdminState.IN_SERVICE, AdminState.AUTO_IN_SERVICE]:
            return True

        return False
