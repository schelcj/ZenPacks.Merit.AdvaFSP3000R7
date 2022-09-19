######################################################################
#
# FSP3000R7DeviceMib modeler plugin
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7DeviceMib

FSP3000R7DeviceMib gets System name from the NCU-II.  It creates a pickle
file with information needed by component modelers so the same information
does not have to be queried from the shelf over and over.  The Adva shelves
can respond very slowly and without this strategy zenoss can time out before
all the SNMP information is returned."""


from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
import cPickle
import time
import subprocess
from pprint import pformat
from ZenPacks.Merit.AdvaFSP3000R7.lib.AdvaMibTypes import EntityClass


class FSP3000R7DeviceMib(PythonPlugin):
    """Use a PythonPlugin instead of SnmpPlugin since they run first in
       def collectDevice in /opt/zenoss/Products/DataCollector/zenmodeler.py
       Need that order so the pickle file will be created first."""

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device"


    def copyDataToProxy(self, device, proxy):
        """add zSnmpCommunity to device proxy"""
        result = PythonPlugin.copyDataToProxy(self, device, proxy)
        proxy.zSnmpCommunity = device.zSnmpCommunity


    def collect(self, device, log):
        log.info('Starting to collect SNMP data using snmpget and snmpbulkwalk')
        # from the FspR7-MIB mib, neSystemId has the name of the system
        # and neSwVersion is the software version
        neSystemId = '.1.3.6.1.4.1.2544.1.11.2.2.1.1.0'
        neSwVersion = '.1.3.6.1.4.1.2544.1.11.2.2.1.5.0'

        inventoryUnitNameOID = '1.3.6.1.4.1.2544.2.5.5.1.1.1'
        entityContainedInOID = '1.3.6.1.4.1.2544.2.5.5.2.1.2'
        entityIndexAidOID = '1.3.6.1.4.1.2544.2.5.5.2.1.5'
        interfaceConfigIdentifierOID = '1.3.6.1.4.1.2544.1.11.2.4.3.1.1.1'
        entityAssignmentStateOID = '1.3.6.1.4.1.2544.2.5.5.2.1.7'
        entityEquipmentStateOID = '1.3.6.1.4.1.2544.2.5.5.2.1.8'
        opticalIfDiagInputPowerOID = '1.3.6.1.4.1.2544.1.11.2.4.3.5.1.3'

        # 9ROADM Virtual Channels are in a separate SNMP location with alternate indexes
        facilityPhysInstValueInputPowerOID = '1.3.6.1.4.1.2544.1.11.11.7.2.1.1.1.2'
        virtualPortAliasOID = '1.3.6.1.4.1.2544.1.11.7.3.4.2.1.4'
        virtualPortAdminOID = '1.3.6.1.4.1.2544.1.11.7.3.4.2.1.9'

        # Build/flatten a parent tree to filter entities (i.e., VCHs for '9ROADM-RS')
        entity_tables = {
            'entityFacility': {
                'base_oids': {
                    'AidString': '1.3.6.1.4.1.2544.1.11.7.2.7.1.6',
                    'Class': '1.3.6.1.4.1.2544.1.11.7.2.7.1.10',
                    'ParentId': '1.3.6.1.4.1.2544.1.11.7.2.7.1.9',
                },
                'table_data': {},
            },
            'entityOpticalMux': {
                'base_oids': {
                    'AidString': '1.3.6.1.4.1.2544.1.11.7.2.17.1.6',
                    'Class': '1.3.6.1.4.1.2544.1.11.7.2.17.1.10',
                    'ParentId': '1.3.6.1.4.1.2544.1.11.7.2.17.1.9',
                },
                'table_data': {},
            },
            'entityEqpt': {
                'base_oids': {
                    'AidString': '1.3.6.1.4.1.2544.1.11.7.2.2.1.6',
                    'Class': '1.3.6.1.4.1.2544.1.11.7.2.2.1.10',
                    'ParentId': '1.3.6.1.4.1.2544.1.11.7.2.2.1.9',
                 },
                'table_data': {},
            },
            'advaInventory': {
                'base_oids': {
                    'AidString': '1.3.6.1.4.1.2544.1.11.7.10.1.1.6',
                    'Class': '1.3.6.1.4.1.2544.1.11.7.10.1.1.19',
                    'UnitName': '1.3.6.1.4.1.2544.1.11.7.10.1.1.7',
                 },
                'table_data': {},
            },
        }

        for key, info in entity_tables.items():
            for base_oid_name, base_oid in info['base_oids'].items():
                raw_data = self.__snmpgettable(device, base_oid)
                self.__make_cacheable(
                    base_oid,
                    key + base_oid_name,
                    raw_data,
                    info['table_data'],
                )

        # Attach the containing module's UnitName directly to lower-level entities
        for facility_index, facility_info in entity_tables['entityFacility']['table_data'].items():
            unit_name = self.__get_unit_name(facility_info['entityFacilityParentId'], entity_tables, log)
            facility_info['inventoryUnitName'] = unit_name

        getdata = {}
        
        self.__snmpget(device,neSystemId,'setHWTag',getdata)
        log.info('Got system name %s' % getdata['setHWTag'])
        self.__snmpget(device,neSwVersion,'setOSProductKey',getdata)
        log.info('Got software version %s' % getdata['setOSProductKey'])

        inventoryTable = {}
        raw_inventory = {}
        raw_inventory = self.__snmpgettable(device,inventoryUnitNameOID)
        self.__make_cacheable(inventoryUnitNameOID, 'inventoryUnitName', raw_inventory, inventoryTable)

        entityTable = {}
        raw_entityContainedIn = {}
        raw_entityContainedIn = self.__snmpgettable(device,entityContainedInOID)
        self.__make_cacheable(entityContainedInOID,
                              'entityContainedIn',
                              raw_entityContainedIn,
                              entityTable)

        raw_entityIndexAid = {}
        raw_entityIndexAid = self.__snmpgettable(device,entityIndexAidOID)
        self.__make_cacheable(entityIndexAidOID,
                              'entityIndexAid',
                              raw_entityIndexAid,
                              entityTable)

        raw_interfaceConfigIdentifier = {}
        raw_interfaceConfigIdentifier = \
          self.__snmpgettable(device,interfaceConfigIdentifierOID)
        self.__make_cacheable(interfaceConfigIdentifierOID,
                              'interfaceConfigIdentifier',
                              raw_interfaceConfigIdentifier,
                              entityTable)

        raw_entityAssignmentState = {}
        raw_entityAssignmentState = self.__snmpgettable(device,
                                                       entityAssignmentStateOID)
        self.__make_cacheable(entityAssignmentStateOID,
                              'entityAssignmentState',
                              raw_entityAssignmentState,
                              entityTable)

        raw_entityEquipmentState = {}
        raw_entityEquipmentState = self.__snmpgettable(device,
                                                       entityEquipmentStateOID)
        self.__make_cacheable(entityEquipmentStateOID,
                              'entityEquipmentState',
                              raw_entityEquipmentState,
                              entityTable)

        raw_virtualPortAlias = self.__snmpgettable(device, virtualPortAliasOID)
        self.__make_cacheable(virtualPortAliasOID,
                              'virtualPortAlias',
                              raw_virtualPortAlias,
                              entity_tables['entityFacility']['table_data'])

        raw_virtualPortAdmin = self.__snmpgettable(device, virtualPortAdminOID)
        self.__make_cacheable(virtualPortAdminOID,
                              'virtualPortAdmin',
                              raw_virtualPortAdmin,
                              entity_tables['entityFacility']['table_data'])

        opticalIfDiagTable = {}
        raw_opticalIfDiagInputPower = {}
        raw_opticalIfDiagInputPower= self.__snmpgettable(device,
                                                     opticalIfDiagInputPowerOID)
        self.__make_cacheable(opticalIfDiagInputPowerOID,
                              'opticalIfDiagInputPower',
                              raw_opticalIfDiagInputPower,
                              opticalIfDiagTable)

        facilityPhysInstValueTable = {}
        raw_facilityPhysInstValueInputPower = {}
        raw_facilityPhysInstValueInputPower = self.__snmpgettable(device,
                                                     facilityPhysInstValueInputPowerOID)
        self.__make_cacheable(facilityPhysInstValueInputPowerOID,
                              'facilityPhysInstValueInputPower',
                              raw_facilityPhysInstValueInputPower,
                              facilityPhysInstValueTable)

        # sometimes Avda shelves give bogus -65535 input power readings for
        # components that really do have input power readings when you do a
        # specific snmpget on them.
        for index, opr_dict in opticalIfDiagTable.items():
            try:
                if opr_dict['opticalIfDiagInputPower'] == -65535:
                    oid = opticalIfDiagInputPowerOID + '.' + index
                    w = {}
                    self.__snmpget(device,oid,'opr',w)
                    opticalIfDiagTable[index] = \
                            { 'opticalIfDiagInputPower' : int(w['opr']) }
            except (KeyError, ValueError):
                pass

        cache_file_name = '/tmp/%s.Adva_inventory_SNMP.pickle' % device.id
        cache_data = {
            'inventoryTable': inventoryTable,
            'entityTable': entityTable,
            'opticalIfDiagTable': opticalIfDiagTable,
            'facilityTable': entity_tables['entityFacility']['table_data'],
            'facilityPhysInstValueTable': facilityPhysInstValueTable,
            'time': time.time(),
        }
        try:
            cache_file = open(cache_file_name,'w')
            cPickle.dump(cache_data, cache_file)
            cache_file.close()
        except IOError,cPickle.PickleError:
            log.warn("Couldn't cache SNMP data in", cache_file_name)

        return getdata


    def __get_unit_name(self, start_oid, entity_tables, log, current_oid=None, chain=None):
        """
        Traverse the ParentId data, returning the inventoryUnitName associated with
        the first module-level entity in the entityEqpt table.

        For troubleshooting purposes, build a chain (list) of the OIDs from child->parent.
        """
        unit_name = None

        if current_oid is None:
            current_oid = start_oid

        if chain is None:
            chain = []

        current_oid = current_oid.lstrip('.')

        chain.append(current_oid)

        for table_prefix, table_attrs in entity_tables.items():
            for entity_index, entity_attrs in table_attrs['table_data'].items():
                full_aid_oid = ".".join([table_attrs['base_oids']['AidString'], entity_index])
                if full_aid_oid != current_oid:
                    continue

                if entity_attrs.get('entityEqptClass') == EntityClass.MODULE:
                    try:
                        unit_name = entity_tables['advaInventory']['table_data'][entity_index]['advaInventoryUnitName']
                        return unit_name
                    except KeyError as err:
                        log.warning('%s: %s, unable to find UnitName for entity with chain %s' % (err.__class__.__name__, err, chain))

                try:
                    next_parent = entity_attrs[table_prefix + 'ParentId']
                    return self.__get_unit_name(
                        start_oid=start_oid,
                        entity_tables=entity_tables,
                        log=log,
                        current_oid=next_parent,
                        chain=chain,
                   )
                except KeyError as err:
                    log.warning('%s: %s, no further ParentIds to follow with chain %s' % (err.__class__.__name__, err, chain))
                    continue

        log.warning("Unable to find UnitName for entity with chain %s" % chain)
        return None


    def process(self, device, results, log):
        """Set the system name and software version"""

        log.debug('in process, got results:',results)
        rm = self.relMap()
        om = self.objectMap(results)
        return om


    def __snmpget(self,device,oid,oid_name,results):
        cmd = ['snmpget','-v2c','-t','3',
               '-c',device.zSnmpCommunity, '-Onq', device.manageIp,oid]
        try:
            results[oid_name] = \
                subprocess.check_output(cmd).split(' ')[1].strip('\n"')
        except subprocess.CalledProcessError, IndexError:
            results[oid_name] = ''


    def __snmpgettable(self, device, oid, not_found_prefix='no such instance'):
        """
        Use snmpbulkwalk to get data.  Use timeout of 5 seconds since
        shelves can be very slow to respond.

        If the value of the first result starts with not_found_prefix,
        return an empty dict.
        """
        cmd = ['snmpbulkwalk','-v2c','-t','5',
               '-c',device.zSnmpCommunity, '-Onq', device.manageIp,oid]

        results = {}

        try:
            walk_output = subprocess.check_output(cmd).split('\n')

            for line in walk_output:
                try:
                    oid,val = line.split(' ',1)
                    oid = oid.lstrip('.')
                    val = val.strip('"')

                    if not len(results) and val.lower().startswith(not_found_prefix):
                        return results

                except ValueError:
                    continue

                try:
                    val = int(val)
                except ValueError:
                    pass

                results[oid] = val
        except subprocess.CalledProcessError, IndexError:
            pass

        return results

    def __make_cacheable(self, base_oid, name, raw, results):
        """
        Compile SNMP results by index
        May use single- or dotted-value indexes. For base OID 1.2.3.4.5, the component indexes would be:
          - 1.2.3.4.5.12345   -> 12345
          - 1.2.3.4.5.1.234.5 -> 1.234.5
        """
        for oid, val in raw.items():
            index = oid.replace(base_oid + '.', '')
            if index not in results:
                results[index] = {}
            results[index][name] = val
