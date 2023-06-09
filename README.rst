Ising model 2D
==============

In the present repository, we study the two-dimensional classical Ising
model by numerical simulation. In particular, we analyze the behaviour of the
system around the phase transition, verifying the effect of finite-size scaling
and deriving the critical exponents.

The scheme of the repository is the following:

- ising_lattice_class.h contains the lattice class from which the ising lattice
is instantiated. This class also contains a Metropolis update method.

- ising_run_simulation.h contains the simulation parameters and the subroutine
that generates the simulation data in the Data_simulations folder. Here we can
find for every beta a file with the measures of energy and magnetization.

- main_ising.cpp and main_parallel.cpp call the above mentioned subroutine for
all the given values of beta and side.

- data_analysis.cpp contains the errors analysis parameters and generates the
files in the Data_analysis folder. Here we can find the physical quantities in
function of beta, the cumulant data in function of L and the analysis of the
associated errors in the .txt files.

- plot_and_cumulant.py uses the data in the Data_analysis folder to plot all of
the studied physical quantities and the associated errors.

- critical_exp.py uses the data in the Data_analysis folder to compute the
critical point and exponents. It also produces plots of the performed fits.
The output is reported in the critical_analysis.txt file.
