# Copyright (C) 2017  Jan Wollschläger <jmw.tau@gmail.com>
# This file is part of ORCAunleashed.
#
# Tau is free software: you can redistribute it and/or modify
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

import os

_log_output = True
def log(msg):
    global _log_output
    if _log_output:
        print(msg)

orca_path = "orca"
output_dir = os.path.dirname(os.path.realpath(__file__))+os.sep+"output"+os.sep
def run_orca(xyzfile=None, xyzstring=None, jobname=None, orca_input=None):
    if jobname is None:
        jobname = "job"
    assert(orca_input is not None)
    assert(xyzfile is not None or xyzstring is not None)
    global orca_path
    global output_dir
    log("orca executable path is {}".format(orca_path))
    if orca_path == "orca":
        log("assuming orca is on your path")
    log("output directory is {}".format(output_dir))
    if not os.path.exists(output_dir):
        log("creating output directory")
        os.makedirs(output_dir)
    if xyzfile:
        with open(xyzfile, 'r') as fin:
            xyzstring = fin.read()
    xyzstring += '\n\n'
    xyzinputfile = output_dir + "{}_input.xyz".format(jobname)
    log("creating xyz geometry input file")
    with open(xyzinputfile, 'w') as fout:
        fout.write(xyzstring)
    orca_input += '\n\n'
    jobinputfile = output_dir + "{}.in".format(jobname)
    log("creating job file")
    with open(jobinputfile, 'w') as fout:
        fout.write(orca_input)
    joboutputfile = output_dir + "{}.out".format(jobname)
    log("running job (this could take a while)")
    previous_wd = os.getcwd()
    os.chdir(output_dir)
    os.system("{} {} > {}".format(orca_path, jobinputfile, joboutputfile))
    log("running of job finished")
    log("changing back current working directory")
    os.chdir(previous_wd)
    return ORCAReporter(joboutputfile)



def run_orca_opt_freq(xyzfile=None, xyzstring=None, jobname="job", method=None, basis_set=None):
    assert(method is not None)
    if basis_set is None:
        if method not in ['AM1', 'PM3', 'MNDO', 'INDO']:
            log('warning: no basis set specified!')
        basis_set = ''
    orca_input = """
!{} {} opt freq

*xyzfile 0 1 {}
    """.format(basis_set, method, "{}_input.xyz".format(jobname)).strip()
    return run_orca(xyzfile=xyzfile,xyzstring=xyzstring,jobname=jobname,orca_input=orca_input)





class ORCAReporter(object):
    def __init__(self, joboutputfile):
        self.joboutputfile = joboutputfile
        self._output = None

    def output_lines(self):
        lst = []
        for lne in self.output().split('\n'):
            lst.append(lne)
        return lst

    def output(self):
        if self._output is not None:
            return self._output
        else:
            self._output = None
            with open(self.joboutputfile, 'r') as fin:
                self._output = fin.read()
        assert self._output is not None, 'error reading in file {}'.format(self.joboutputfile)
        return self._output

    def final_gibbs_energy(self):
            for lne in self.output_lines():
                lne = lne.strip()
                if lne.startswith("Final Gibbs free enthalpy"):
                    return lne.split(' ')[-2]
            print(self.joboutputfile)















#
