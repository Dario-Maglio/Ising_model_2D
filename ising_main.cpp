/*******************************************************************************
*
* Main program for the Ising simulations
*
*******************************************************************************/

// g++ class_lattice.h ising_main.cpp -o main.out

//--- Preprocessor directives --------------------------------------------------

#include <iostream>
#include <fstream>
#include <string>

#include <chrono>
#include <vector>

// Import the Class lattice
#include "class_lattice.h"

using namespace std;

/*******************************************************************************
* PARAMETERS OF THE SIMULATION
*
* SIDE_SEP = separation between the sides of different simulations.
*
* BETA_SEP = separation between the betas of different simulations.
*
* MEASURES = desired number of measures for each value of beta.
*
* I_DECORREL = MC-updates of the lattice between different measurements.
*
* I_FLAG = lattice's initial configuration flag:
*          0 for cold initialization.
*          1 for hot (random) initialization.
*          2 for loading the previous configuration and append data.
*
* G_FLAG = lattice's geometry flag:
*          0 and others not implemented yet.
*          1 for 1D periodic chain.
*          2 for 2D square with PBC.
*
* EXTFIELD = adimensional intensity of the external magnetic field.
*
*******************************************************************************/

// sides to simulate
#define SIDE_SEP 10
#define SIDE_MIN 150
#define SIDE_MAX 150
// betas to simulate
#define BETA_SEP 0.0050
#define BETA_INI 0.4800
#define BETA_FIN 0.4800
// number of measures to save
#define MEASURES 100000
// decorrelation between measures
#define I_DECORREL 10 // * V
// initialization flags
#define I_FLAG 2
#define G_FLAG 2
// external field
#define EXTFIELD 0.

using namespace std;



//--- Contents -----------------------------------------------------------------

void run_simulation(int side, float beta){
    /* MC-simulation for a given side and beta */

    ofstream file;
    string directory, name_file, name_file_data, name_file_state, message;
    lattice ising(side, G_FLAG, I_FLAG);

    // Define path data directory
    directory = "Data_simulations/Side_" + to_string(side) + "/";
    // Define name file last configuration of the lattice
    name_file_state = "side_" + to_string(side) + "_beta_" + to_string(beta);
    // Define name file simulation for a given side and beta
    name_file_data =  name_file_state + ".dat";

    // Prepare the lattice for the simulation
    if(I_FLAG == 2){
        // Load last configuration of the lattice
        ising.load_configuration(directory + name_file_state);
    } else {
        // Thermalization phase
        for(int i = 0; i < (1000*I_DECORREL); i++) ising.update(beta, EXTFIELD);
    }

    // Print initial energy and magnetization
    message = "File: " + name_file_data +
              "\n -> starting energy = " + to_string(ising.energy(EXTFIELD)) +
              "\n -> starting magnet = " + to_string(ising.magnetization());
    cout << message << endl << endl;

    // Open the data file
    if(I_FLAG == 2){
        file.open(directory + name_file_data, ios_base::app);
    } else {
        file.open(directory + name_file_data);
    }

    // Update ising and take measures
    for(int n = 0; n < MEASURES; n++){
        for(int i = 0; i < I_DECORREL; i++) ising.update(beta, EXTFIELD);
        file << ising.energy(EXTFIELD) << " " << ising.magnetization() << endl;
    }
    file.close();

    // We can stop the simulation when a file is completed
    ising.save_configuration(directory + name_file_state);
    cout << "Creation of " << name_file_data << " completed." << endl << endl;
}

//--- Main ---------------------------------------------------------------------

int main(){
    /* Main program iterates the timed Ising simulation over sides and betas */

    auto start = chrono::steady_clock::now();
    for(int side = SIDE_MIN; side <= SIDE_MAX; side += SIDE_SEP){
        for(float beta = BETA_INI; beta <= BETA_FIN; beta += BETA_SEP){
            run_simulation(side, beta);
        }
    }
    auto end = chrono::steady_clock::now();

    chrono::duration<double> elapsed_seconds = end - start;
    cout << "Elapsed time: " << elapsed_seconds.count() << "s " << endl << endl;

    cout << "The work is done." << endl << endl;
    return 0;
}
