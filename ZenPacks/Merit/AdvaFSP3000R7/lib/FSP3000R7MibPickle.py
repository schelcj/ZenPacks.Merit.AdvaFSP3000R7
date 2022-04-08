import cPickle
import time
from pprint import pformat

def getCache (deviceId, modelerName, log):
    cache = {}
    cache_file_name = '/tmp/%s.Adva_inventory_SNMP.pickle' % deviceId
    cache_file_time = 0

    try:
        cache_file = open(cache_file_name, 'r')
        cache = cPickle.load(cache_file)
        cache_file.close()
    except IOError,cPickle.PickleError:
        log.error('Could not open or read %s', cache_file_name)
        return False

    if not cache or cache.get('time', 0) < time.time() - 900:
        log.warn("Cached SNMP doesn't exist or is older than 15 minutes. You must include the modeler plugin FSP3000R7Device")
        return False

    required_tables = ['inventoryTable', 'entityTable']
    for table_name in required_tables:
        if not cache.get(table_name):
            log.error('No SNMP %s response from %s for the %s plugin', table_name, deviceId, modelerName)
            return False

    log.debug('SNMP entityTable and inventoryTable responses received')

    # not all modules will respond to opticalIfDiagTable so don't return False
    optional_tables = ['opticalIfDiagTable', 'facilityPhysInstValueTable']
    for table_name in optional_tables:
        if not cache.get(table_name):
            log.warn('No SNMP %s response from %s for the %s plugin', table_name, deviceId, modelerName)
        else:
            log.debug('SNMP %s response received', table_name)

    # dictionary of lists of what modules or submodules contain
    # submodules that respond to OPR
    if cache['opticalIfDiagTable']:
        containsOPRModules = _build_opr_tree(cache['entityTable'], cache['opticalIfDiagTable'], log)

    if cache['facilityPhysInstValueTable']:
        vchOPRModules = _build_opr_tree(
            cache['facilityTable'],
            cache['facilityPhysInstValueTable'],
            log,
            aid_field='entityFacilityAidString',
            power_field='facilityPhysInstValueInputPower',
            parent_field=None,
        )
        containsOPRModules.update(vchOPRModules)

    cache['containsOPRModules'] = containsOPRModules

    return cache


def _build_opr_tree(
    entity_table,
    power_table,
    log,
    aid_field='entityIndexAid',
    power_field='opticalIfDiagInputPower',
    parent_field='entityContainedIn'
):
    """
    Return a flattened dict of component aid strings with a list of their
    childrens' indexes, if any of the children have values for the power_field.
    Also includes keys for each child with a 1-item list containing its own index.

    SHELF-1 (index 1111)
      MOD-1-1 (index 2222)
        OM-1-1 (index 3333)
          CH-1-1-N (index 4444)
          VCH-1-1-1 (index 5555)

    {
      'SHELF-1': [2222],
      'MOD-1-1': [3333],
      'OM-1-1': [4444, 5555],
      'CH-1-1-N': [4444],
      'VCH-1-1-1': [5555],
    }
    """
    results = {}

    for entity_index, entity_attrs in entity_table.items():
        if entity_index not in power_table:
            continue

        if power_field not in power_table[entity_index]:
            continue

        # MIB says value of -65535 means not available or invalid
        if power_table[entity_index][power_field] == -65535:
            continue

        if not entity_attrs.get(aid_field, None):
            log.debug("Component at %s responds to OPR but has no aid string, skipping...")
            continue

        # create entry for the OPR responding module itself
        results[entity_table[entity_index][aid_field]] = [entity_index]

        # create entry for the immediate parent or append
        if parent_field:
            parent_index = entity_table[entity_index].get(parent_field, None)

            parent_index = str(parent_index)

            if not parent_index:
                break

            parent_index_aid = entity_table[parent_index].get(aid_field, None)

            if parent_index_aid is None:
                continue
            elif parent_index_aid not in results:
                results[parent_index_aid] = [entity_index]
            else:
                results[parent_index_aid].append(entity_index)

            # create entry for all parents above immediate parent
            while(parent_index):
                parent_index = __get_parent(log, parent_index, entity_table, parent_field)

                if not parent_index:
                    break

                parent_index_aid = entity_table[parent_index].get(aid_field, None)

                if parent_index_aid is None:
                    continue
                elif parent_index_aid not in results:
                    results[parent_index_aid] = [entity_index]
                else:
                    results[parent_index_aid].append(entity_index)

    return results


def __get_parent(log, child_index, entity_table, parent_field):
    if child_index not in entity_table:
        return False
    if parent_field not in entity_table[child_index]:
        return False
    if entity_table[child_index][parent_field] == 0:
        return False
    return str(entity_table[child_index][parent_field])
