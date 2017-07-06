from ORCAunleashed import orcaunleashed


if __name__ == '__main__':
    print('Testing features of ORCAunleashed')
    print('-- Testing run_orca_opt_freq')
    print('-- .. running job with methane.xyz')
    reporter = orcaunleashed.run_orca_opt_freq(xyzfile='methane.xyz',method='AM1')
    print('-- .. job runs without errors')
    print('-- .. retrieving final gibbs energy')
    fge = reporter.final_gibbs_energy()
    print('-- .. final gibbs energy:',fge)
