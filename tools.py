# Copyright (C) 2017-2018  Jan Wollschläger <jmw.tau@gmail.com>
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

import re,os

try:
    import numpy as np
except:
    print('failed loading numpy (which could be needed for some functionality)')
try:
    from matplotlib import pyplot as plt
except:
    print('failed loading matplotlib (which could be needed for some functionality)')

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



def orca_trj_to_xyz(trj_file):
    pardir = os.path.dirname(trj_file)+os.path.sep
    os.chdir(pardir)
    with open(os.path.join(pardir,trj_file),'r') as fin:
        xyz_str,count = "",0
        for lne in fin:
            if re.match('[0-9]+',lne.strip()):
                if xyz_str:
                    with open(os.path.join(pardir,'xyzs/xyz_{}.xyz'.format(count)),'w') as fout:
                        fout.write(xyz_str)
                count += 1
                xyz_str = lne
            else:
                xyz_str += lne



def uvvis_peaks_str(rep):
    peaks_str = ""
    parsing = False
    sep_count = 0
    for lne in rep.output().split('\n'):
        lne = lne.strip()
        if lne.startswith("ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"):
            parsing = True
        if parsing and lne:
            if lne.startswith("----"):
                sep_count += 1
                if sep_count > 2:
                    return peaks_str
                continue
            if sep_count == 2:
                peaks_str += lne+"\n"

    return None


def uvvis_peaks(rep):
    pxs,pys=[],[]
    for lne in uvvis_peaks_str(rep).split('\n'):
        lne = lne.replace('\t',' ').replace('  ',' ').replace('  ',' ')
        lne = lne.split(' ')
        if len(lne) != 8: continue
        pxs.append(float(lne[2]))
        pys.append(float(lne[3]))
    return pxs,pys

def uvvis_spec(rep,peak_width=None,show_plot=True):
    if peak_width is None:
        peak_width = 10 ## sensible guess for peak-width?
    def gauss(x,a,b,c):
        return a * np.e ** (- ((x - b)**2) / (2 * c**2))
    pxs,pys = uvvis_peaks(rep)
    cxs,cys = np.linspace(min(pxs)-50,max(pxs)+50,200),np.zeros(200)
    for px,py in zip(pxs,pys):
        a = py; b = px; c = peak_width
        cys += np.array([gauss(cx,a,b,c) for cx in cxs])
    if show_plot:
        plt.plot(cxs,cys)
    return cxs,cys















#
