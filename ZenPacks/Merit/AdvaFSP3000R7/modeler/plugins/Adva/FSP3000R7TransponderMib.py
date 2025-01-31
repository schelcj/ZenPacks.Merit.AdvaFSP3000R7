######################################################################
#
# FSP3000R7TransponderMib modeler pluginn
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7TransponderMib

FSP3000R7TransponderMib maps Transponder amplifiers on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon

class FSP3000R7TransponderMib(FSP3000R7MibCommon):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Transponder"
    relname = "FSP3000R7Trans"

    componentModels = [ # Core Type channel modules
                        'WCC-TN-40G-L#DC',
                        '4TCC-PCTN-10G+40G-L#DC',
                        'WCC-PCTN-100GB',
                        'WCC-PCTN-100GA',
                        '10TCC-PCTN-10G+100GB',
                        '10TCC-PCTN-10G+100GC',
                        'WCC-PCTN-10G-LN#DC',
                        'WCC-PCTN-10G-V#DC',
                        'WCC-PCTN-10G-V#DL',
                        'WCC-PCTN-10G-V#D01-32',
                        '4TCC-PCTN-2G7+10G-LN#DC',
                        '4TCC-PCTN-2G7+10G-V#DC',
                        '4TCC-PCTN-2G7+10G-V#DL',
                        '4TCC-PCTN-2G7+10G-V#D01-32',
                        '10TCC-PCTN-4GU+10G-LN#DC',
                        '10TCC-PCTN-4GU+10G-V#DC',
                        '10TCC-PCTN-4GU+10G-V#DL',
                        '10TCC-PCTN-4GU+10G-V#D01-32',
                        '10TCC-PCTN-4GUS+10G-LN#DC',
                        '10TCC-PCTN-4GUS+10G-V#DC',
                        '10TCC-PCTN-4GUS+10G-V#DL',
                        '10TCC-PCN-2G7US+10G',
                        '10WXC-PCN-10G',
                        '2WCC-PCN-10G',
                        '2TWCC-PCN-2G7U',
                        'WCC-PC1N-2G7U',
                        '4TCC-PCN-2G1U+2G5',
                        'WCC-PCN-100G',
                        'WCC-PCN-100GA',
                        'WCC-PCN-100GB',
                        # Access Type Channel modules
                        '2PCA-PCN-10G',
                        '10PCA-PCN-1G3-10G',
                        '10PCA-PCN-1G3+10G',
                        '2WCA-PCN-10G',
                        'WCA-PC-10G-V#',
                        '8TCA-PC-2G1U+10G-V#',
                        '4TCA-PCN-4GU+4G',
                        '4TCA-PCN-4GUS+4G',
                        'WCA-PCN-2G5U',
                        '2TCA-PCN-1G3+2G5',
                        '2TCA-PCN-622M+2G5',
                        '4TCA-LS+1G3-V#',
                        # Enterprise Type Channel modules
                        'WCE-PCN-100G',
                        '4WCE-PCN-16GFC',
                        '5TCE-PCTN-10GU+10G-LN#DC',
                        '5TCE-PCTN-10GU+10G-V#DC',
                        '5TCE-PCTN-10GU+10G-V#DL',
                        '5TCE-PCTN-10GU+AES10G-LN#DC',
                        '5TCE-PCTN-10GU+AES10G-V#DC',
                        '5TCE-PCTN-10GU+AES10G-V#DL',
                        '5TCE-PCTN-8GU+10GS-LN#DC',
                        '5TCE-PCTN-8GU+10GS-V#DC',
                        '10TCE-PCN-10G+100G-GF',
                        '10TCE-PCN-10G+100G',
                        '10TCE-PCN-16GU+100G',
                        '8TCE-ESCON+2G5-V#',
                        '8TCE-GLINK+2G5-V#',
                        'MP-2B4CT',
                        'MA-B5LT',
                        ]
