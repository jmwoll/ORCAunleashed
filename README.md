ORCAunleashed provides a very minimalistic python interface to the ORCA quantum chemistry package. Essentially, a single method is provided:
```
from ORCAunleashed import orca

reporter = orca.run_orca(orca_input="!AM1 opt freq\n\n*xyz 0 1\nN 0 0 0\nN 1 1 1")
print("\n".join(reporter.output_lines()[-3:-1]))
# Outputs:
#     ****ORCA TERMINATED NORMALLY****
# TOTAL RUN TIME: 0 days 0 hours 0 minutes 15 seconds 0 msec
```
