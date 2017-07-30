from ORCAunleashed import orca
orca_input = "!AM1 opt freq\n\n*xyz 0 1\nN 0 0 0\nN 1 1 1\nend"
reporter = orca.run_orca(orca_input=orca_input)
print(reporter.output_lines()[-5:-1])
assert("TERMINATED NORMALLY" in "".join(reporter.output_lines()[-5:-1]))
