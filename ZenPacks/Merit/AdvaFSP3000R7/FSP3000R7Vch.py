######################################################################
#
# FSP3000R7Vch object class
#
# Copyright (C) 2021 Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7Vch

FSP3000R7Vch is a component of a FSP3000R7Device Device
"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7Component import *

import logging
log = logging.getLogger('FSP3000R7Vch')

class FSP3000R7Vch(FSP3000R7Component):
    """FSP3000R7Vch object"""

    portal_type = meta_type = 'FSP3000R7Vch'

    _relations = (("FSP3000R7Dev",
                  ToOne(ToManyCont,
                        "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device",
                        "FSP3000R7VchRel")),
        )

InitializeClass(FSP3000R7Vch)
