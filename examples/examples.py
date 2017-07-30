from ORCAunleashed import orcaunleashed
import time

if __name__ == '__main__':
    print('Testing features of ORCAunleashed')
    print('-- Testing run_orca_opt_freq')
    print('-- .. running job with methane.xyz')
    reporter = orcaunleashed.run_orca_opt_freq(xyzfile='methane.xyz',method='AM1')
    print('-- .. job runs without errors')
    print('-- .. retrieving final gibbs energy')
    fge = reporter.final_gibbs_energy()
    print('-- .. final gibbs energy:',fge)
    assert(len(fge) == 1)

    print('-- Testing run_orca_md')
    print('-- .. running job with methane.xyz')
    reporter = orcaunleashed.run_orca_md(xyzfile='pentane.xyz',method='AM1', dt=2)
    print('-- .. job runs without errors')
    print('-- .. retrieving final gibbs energy')
    fge = reporter.final_gibbs_energy()
    print('-- .. final gibbs energy:',fge)
    assert(len(fge) == 0)
    xyzgeoms,energies = reporter.report_md()
    for i,xyzgeom in enumerate(xyzgeoms):
        with open('geom_{}.xyz'.format(i),'w') as fout:
            fout.write(xyzgeom)
