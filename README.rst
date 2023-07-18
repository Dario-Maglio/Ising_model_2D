==============
Ising Model 2D
==============

In this repository, we present the study of the two-dimensional classical Ising model through numerical simulation. By implementing the Monte Carlo method, we obtain the characteristic quantities of the system and analyze their behaviour around the ferromagnetic phase transition. We determine critical exponents and examine the effect of finite-size scaling.

Repository Structure
====================

The structure of the repository is as follows:

- ``class_lattice.h``: \.
  This header contains the lattice class from which the Ising lattice is instantiated. The class includes a Metropolis update method and an incorporated Pseudo Random Number Generator.

- ``main_*.cpp``: \
  These programs call the simulation subroutine for all betas and sides, collecting average energy and magnetization measures in the ``Data_simulations`` folder.

- ``data_analysis.cpp``: \
  This program, located in the ``Data_processing`` directory, computes the quantities of interest and their errors. The computation and error analysis results are stored in the ``Data_analysis`` folder.

- ``plot_and_cumulant.py`` and ``critical_exponents.py``: \
  These programs, also located in the ``Data_processing`` directory, utilize the data in the ``Data_analysis`` folder to plot the physical quantities and fit the cumulant and critical exponents. The fit parameters and their errors are stored in the ``cumulant_results.txt`` and ``critical_exponents.txt`` files.

- ``Tests``: \
  This directory contains easy-to-use examples for testing the lattice class and verifying that the Monte Carlo algorithm has thermalized.

- ``Plots_and_fit``: \
  All produced plots are stored in this folder.

Analysis Results
================

Here are some of the plots generated from the analysis:

- Plot of the main physical quantities:

  .. image:: https://github.com/Dario-Maglio/Ising_model_2D/blob/068471897db23d22a6fe0203f327ce824c5c2503/Plots_and_fit/Plots%20from%20analysis.png
     :align: center
     :width: 70%

- Susceptibility scaling plot:

  .. image:: https://github.com/Dario-Maglio/Ising_model_2D/blob/068471897db23d22a6fe0203f327ce824c5c2503/Plots_and_fit/Plot%20scaling%20susceptibility.png
     :align: center

- Fit to find the critical point:

  .. image:: https://github.com/Dario-Maglio/Ising_model_2D/blob/068471897db23d22a6fe0203f327ce824c5c2503/Plots_and_fit/Fit%20beta_pc%20as%20a%20function%20of%20L.png
     :align: center

- Binder cumulant:

  .. image:: https://github.com/Dario-Maglio/Ising_model_2D/blob/16209762f5964f89316ee703e5d1a4e786d7f414/Plots_and_fit/Binder%20cumulant%20beta%20%3D%200.360000.png
     :align: center

Feel free to explore the repository and use the provided programs for further analysis and investigation.

License
=======

This repository is licensed under the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for more information.
