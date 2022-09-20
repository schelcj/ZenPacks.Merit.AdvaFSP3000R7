######################################################################
#
# FSP3000R7Optical100GigMib modeler plugin
#
######################################################################

__doc__="""Check the FSP3000R7 SNMP cache for optical lane (OTL) entities"""

from Products.DataCollector.plugins.CollectorPlugin import GetMap
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import EntityClass

class FSP3000R7Optical100GigMib(SnmpPlugin):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Optical100Gig"
    relname = "FSP3000R7Optical100G"

    allowed_entity_classes = [
        EntityClass.OPT_CHANNEL_TRANSPORT_LANE,
    ]

    # Not actually used; just have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})

    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # tabledata is not actually used (instead, use cached SNMP data file created in FSP3000R7Device modeler)
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
            facility_class = attrs.get('entityFacilityClass', '')
            unit_name = attrs.get('inventoryUnitName', '')

            if facility_class not in self.allowed_entity_classes:
                log.debug('Skipping non-optical transport component %s' % aid_string)
                continue

            om = self.objectMap()
            om.title = aid_string
            om.id = self.prepId(aid_string)
            om.inventoryUnitName = unit_name
            om.snmpindex = index

            log.info("Found optical transport lane %s", aid_string)
            rm.append(om)

        return rm
