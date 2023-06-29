Ising model 2D
==============

In the present repository, we study the two-dimensional classical Ising
model via Monte Carlo simulation. In particular, we analyze the behaviour of the
system around the phase transition, verifying the effect of finite-size scaling
and deriving the critical exponents.

The scheme of the repository is the following:

- ising_lattice_class.h contains the lattice class from which the ising lattice is instantiated. The class has a Metropolis update method and an incorporated Pseudo Random Number Generator.

- ising_run_simulation.h contains the subroutine that generates the data in the Data_simulations folder. In particular, for every given side and beta, it generates a file with the measures of <e> and <m>.

- main_*.cpp calls the simulation subroutine in ising_run_simulation.h for all betas and sides.

- data_analysis.cpp produces the error analysis and save the results in the Data_analysis folder.

- plot_and_cumulant.py uses the data in the Data_analysis folder to plot all of the physical quantities.

- critical_exp.py uses the data in the Data_analysis folder to compute the critical point and exponents. It also produces plots of the performed fits. The last output is shown in the critical_analysis.txt file.

Easy to use examples are given in the test folder.
