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

from ORCAunleashed import orca
orca_input = "!AM1 opt freq\n\n*xyz 0 1\nN 0 0 0\nN 1 1 1\nend"
reporter = orca.run_orca(orca_input=orca_input)
print(reporter.output_lines()[-5:-1])
assert("TERMINATED NORMALLY" in "".join(reporter.output_lines()[-5:-1]))
