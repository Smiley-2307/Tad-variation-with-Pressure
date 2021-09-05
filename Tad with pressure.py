#2. Variation of T_ad with phi for different combustor pressures (P_c).

import matplotlib.pyplot as plt
import cantera as ct
import numpy as np
import sys
import csv


# Edit these parameters to change the initial temperature, the pressure, and
# the phases in the mixture.

T = 1000

# phases
gas = ct.Solution('JP10.yaml')
carbon = ct.Solution('graphite.yaml')

gas();

# the phases that will be included in the calculation, and their initial moles
mix_phases = [(gas, 1.0), (carbon, 0.0)]

# gaseous fuel species
fuel_species = 'C10H16'

mix = ct.Mixture(mix_phases)

# equivalence ratio range
npoints = 50
phi = np.linspace(0.5, 3, npoints)

P = [0.1,1,10,100]

# create some arrays to hold the data
tad = np.zeros(npoints)
xeq = np.zeros((mix.n_species, npoints))

for j in range(len(P)):
    for i in range(npoints):
        # set the gas state
        gas.set_equivalence_ratio(phi[i], fuel_species, 'O2:1.0, N2:3.76')

        # create a mixture of 1 mole of gas, and 0 moles of solid carbon.
        mix = ct.Mixture(mix_phases)
        mix.T = T
        mix.P = P[j]

        # equilibrate the mixture adiabatically 
        mix.equilibrate('HP', solver='gibbs', max_steps=1000)
        
        tad[i] = mix.T
        xeq[:, i] = mix.species_moles

        print('At phi = {0:12.4g}, Tad = {1:12.4g}'.format(phi[i], tad[i]))
   
    plt.plot(phi, tad,label =   P[j])


if '--plot' in sys.argv:
    plt.xlabel('Equivalence ratio')
    plt.ylabel('Adiabatic flame temperature [K]')
    plt.legend(['0.1','1','10','100'])
    plt.show()
    

#write output CSV file for importing into Excel
csv_file = 'Adiabatic_varPre.csv'
with open(csv_file, 'w', newline='') as outfile:
   writer = csv.writer(outfile)
   writer.writerow(['phi', 'T (K)'] + mix.species_names)
   for i in range(npoints):
       writer.writerow([phi[i], tad[i]] + list(xeq[:, i]))
print('Output written to {0}'.format(csv_file))


   


