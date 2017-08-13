# Copyright (C) 2017  Jan Wollschläger <jmw.tau@gmail.com>
# This file is part of ORCAunleashed.
#
# ORCAunleashed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

# Given an ORCAReporter, this function returns the total runtime of
# the orca job in minutes.
def run_time(reporter):
    # e.g.
    # TOTAL RUN TIME: 0 days 0 hours 0 minutes 34 seconds 857 msec
    for lne in reporter.output_lines():
        if lne.strip().startswith("TOTAL RUN TIME:"):
            lne = lne.split(':')[1]
            lne = re.sub(r'[a-zA-Z]','',lne)
            d,h,m,s,ms = re.compile('\s+').split(lne.strip())
            d,h,m,s,ms = float(d),float(h),float(m),float(s),float(ms)
            return d*60*24 + h*60 + m + s/60.0 + ms/60.0 * 1/1000.0
    assert(False)


# Given an ORCAReporter, this function returns the NMR chemical shifts
# in the form of a dictionary, i.e. {'atom-with-label': chemical-shift}.
# Two different labelling schemes are available:
# *) the natural numbering 1H, 2H, 3H, ..., 1C, 2C, 3C, ...
# *) the orca numbering 0H, 1H, 2H, 3C, 4C, 5O, 6C, ...
def chemical_shifts(reporter, label_type='natural'):
    dct = { }
    key,val = None,None
    #lne_count = 0
    for lne in reporter.output_lines():
        #lne_count += 1
        lne = lne.strip()
        #print(lne_count)
        if (lne.startswith('Nucleus') and lne.endswith(':')
            and not lne.startswith('Nucleus:')):
            key = None
            try:
                _,key,_ = re.compile('\s+').split(lne)
            except ValueError:
                _,key = re.compile('\s+').split(lne)
            assert(key is not None)
            key = key.replace(':','')
        if lne.startswith('Total') and 'iso=' in lne:
            _,val = lne.split('iso=')
            val = val.strip()
            assert(key is not None and key != '')
            assert(val is not None and val != '')
            dct[key] = float(val)
            key,val=None,None
    if label_type.lower() == 'orca':
        return dct
    else:
        assert(label_type.lower() == 'natural')
        # Iterate over orca numbered dict and apply natural labelling scheme:
        # 0H, 1H, 2H, 3C, 4C, 50, 6C -> 1H, 2H, 3H, 1C, 2C, 1O, 3C
        relab_dct = { }
        # tricky key function is necessary to prevent trouble in cases of
        # two-digit numbers, e.g. 10C comes before 2C otherwise.
        for key in sorted(dct,key=lambda itm: int(re.sub(r'[a-zA-Z]','',itm))):
            atom_type = re.sub(r'[0-9]', '', key)
            atom_numb = len([k for k in relab_dct if atom_type in k]) + 1
            relab_dct[str(atom_numb)+atom_type] = dct[key]
        return relab_dct




















    #
