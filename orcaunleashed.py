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
            xyzstring = xyzfile.read()
    xyzinputfile = output_dir + "{}_input.xyz".format(jobname)
    log("creating xyz geometry input file")
    with open(xyzinputfile, 'w') as fout:
        fout.write(xyzstring)
    jobinputfile = output_dir + "{}.in".format(jobname)
    log("creating job file")
    with open(jobinputfile, 'w') as fout:
        fout.write(orca_input)
    joboutputfile = output_dir + "{}.out".format(jobname)
    log("running job")
    #os.system("{} {} > {}&".format(orca_path, jobinputfile, joboutputfile))



def run_orca_opt_freq(xyzfile=None, xyzstring=None, jobname="job"):
    orca_input = """
!AM1 opt freq

*xyzfile 1 0 {}
    """.format("{}_input.xyz".format(jobname)).strip()
    return run_orca(xyzfile=xyzfile,xyzstring=xyzstring,jobname=jobname,orca_input=orca_input)
