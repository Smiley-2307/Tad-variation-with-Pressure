#include "cantera/thermo.h"
#include <iostream>

using namespace Cantera;
using namespace std;

// The actual code is put into a function that
// can be called from the main program.
void simple_demo()
{
    // Create a new phase
    auto sol = newSolution("JP10.yaml");
    auto gas = sol->thermo();
 
    // create some arrays to hold the results value
    size_t nsp = gas->nSpecies();
    vector_fp x(nsp, 0.0);
    double Tad[50];

    double P[4] = { 0.1, 1, 10, 100 };

    // gaseous fuel species
    string fuelSpecies = "C10H16";

    // assign values to array phi
    double phi[50];
    for (int i = 0; i < 50; i++) {
        phi[i] = 0.3 + (0.0653*i);
    }
    for (int j = 0; j < 4; ++j) {
        for (int i = 0; i < 50; i++) {
            // set gas state 
            gas->setState_TP(1000, P[j]);

            // set the equivalnce ratio of gas
            gas->setEquivalenceRatio(phi[i], fuelSpecies, "O2:1.0, N2:3.76");

            // equilibrate the mixture adiabatically at constant P
            gas->equilibrate("HP", "gibbs");

            // storing the resulting value of adiabatic temp and molefractions
            Tad[i] = gas->temperature();
            gas->getMoleFractions(x.data());

            // print the results
            cout << "phi = " << phi[i] << "\t Tad = " << Tad[i] << endl;
        }
    }
 }



// the main program just calls function simple_demo within
// a 'try' block, and catches CanteraError exceptions that
// might be thrown
int main()
{
    try {
        simple_demo();
    }
    catch (CanteraError& err) {
        std::cout << err.what() << std::endl;
    }
}


