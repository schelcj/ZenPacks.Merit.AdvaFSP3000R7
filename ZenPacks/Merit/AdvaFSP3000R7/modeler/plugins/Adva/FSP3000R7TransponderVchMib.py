######################################################################
#
# FSP3000R7TransponderVchMib modeler pluginn
#
# Copyright (C) 2022 Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7TransponderVchMib

FSP3000R7TransponderVchMib maps Virtual Channels on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7VchCommon import FSP3000R7VchCommon


class FSP3000R7TransponderVchMib(FSP3000R7VchCommon):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7TransponderVch"
    relname = "FSP3000R7TransponderVchRel"

    # Since Virtual Channels on older cards might already by detected by other
    # plugins (like FSP3000R7Transponder), only allow this plugin
    # to detect channels on specific (newer) models.
    allowed_unit_names = [
        '4TCA-PCN-4GU+4G',
    ]
