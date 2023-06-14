"""*****************************************************************************
*
* Plot subroutines for the critical exponents
*
*****************************************************************************"""

import os

import numpy as np
import matplotlib.pyplot as plt

#*******************************************************************************
# PARAMETERS OF THE SIMULATION
#
# SIDE_SEP = separation between the sides of different simulations.
#
#*******************************************************************************

SIDE_MIN = 20
SIDE_MAX = 70
SIDE_SEP = 10

sides = np.arange(SIDE_MIN, SIDE_MAX + 1, SIDE_SEP, dtype='int')
logsides = np.log(sides)

#--- Contents ------------------------------------------------------------------

def fit_lin(x, a, c):
    y = c + a * np.power(x, 1)
    return y

def fit_par(x, a, b, c):
    y = c + a * np.power((x - b), 2)
    return y

def fit_beta(x, a, b, c):
    y = c + a / np.power(x, (1/b))
    return y

def load_data():
    """ Load data produced by analysis """

    data = {}
    for side in sides:
        # define data file path
        filename = f"side_{side}_data.dat"
        file_path = os.path.join("Data_analysis", filename)
        print("Loading " + file_path)
        # load data from each side file
        if os.path.isfile(file_path):
            data[side] = np.loadtxt(file_path, unpack='True')

    return data

#--- Parabolic plot subroutines ------------------------------------------------

def plot_par_chi(x, y, y_err, a, b, parameters, title):
    """ Plot parabolic fit for chi """

    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \chi $')
    plt.xlabel(r'$ \beta $')
    plt.xlim([0.40, 0.45])
    # plot data and fit in function of beta
    fit_x = np.linspace(x[a], x[b], 100)
    fit_y = fit_par(fit_x, *parameters)
    fit_label = f'fit [{round(x[a], 4)}, {round(x[b], 4)}]'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    plt.errorbar(x, y, yerr=y_err, fmt='.', label=f'simulation')
    # legend, save and show
    plt.legend(loc='lower right')
    path = os.path.join("Plots_and_fit", "Max_Sus")
    plt.savefig(os.path.join(path, title + ".png"))
    #plt.show()

def plot_par_cal(x, y, y_err, a, b, parameters, title):
    """ Plot parabolic fit for cal """

    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ C_V $')
    plt.xlabel(r'$ \beta $')
    plt.xlim([0.40, 0.45])
    # plot data and fit in function of beta
    fit_x = np.linspace(x[a], x[b], 100)
    fit_y = fit_par(fit_x, *parameters)
    fit_label = f'fit [{round(x[a], 4)}, {round(x[b], 4)}]'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    plt.errorbar(x, y, yerr=y_err, fmt='.', label=f'simulation')
    # legend, save and show
    plt.legend(loc='lower right')
    path = os.path.join("Plots_and_fit", "Max_Cal")
    plt.savefig(os.path.join(path, title + ".png"))
    #plt.show()

#--- Critical plot subroutines -------------------------------------------------

def plot_beta_critical(beta_pc, beta_er, parameters):
    """ Plot beta_pc as a function of L """

    title = "Fit beta_pc as a function of L"
    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \beta_{pc} $')
    plt.xlabel(r'$ L $')
    # plot data and fit in function of beta
    fit_x = np.linspace(10, 80, 100)
    fit_y = fit_beta(fit_x, *parameters)
    fit_label = r'fit y = c + a / x^(1/b)'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    plt.errorbar(sides, beta_pc, yerr=beta_er, fmt='.', label=f'simulation')
    # legend, save and show
    plt.legend(loc='lower right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    #plt.show()

def plot_critical_chi(y_max, y_err, parameters):
    """ Plot chi_max as a function of L"""

    title = "Fit chi_max as a function of L"
    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \log \chi_{max} $')
    plt.xlabel(r'$ \log L $')
    # plot data and fit in function of beta
    fit_x = np.linspace(logsides[0], logsides[-1], 100)
    fit_y = fit_lin(fit_x, *parameters)
    fit_label = f'fit logy = ratio * logL + c'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    sim_label = f'simulation data'
    plt.errorbar(logsides, y_max, yerr=y_err, fmt='<',label=sim_label)
    # legend, save and show
    plt.legend(loc='lower right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    #plt.show()

def plot_critical_mag(y_max, y_err, parameters):
    """ Plot magnetization as a function of L"""

    title = "Fit magneti as a function of L"
    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \log \langle | M | \rangle $')
    plt.xlabel(r'$ \log L $')
    # plot data and fit in function of beta
    fit_x = np.linspace(logsides[0], logsides[-1], 100)
    fit_y = fit_lin(fit_x, *parameters)
    fit_label = f'fit logy = ratio * logL + c'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    sim_label = f'simulation data'
    plt.errorbar(logsides, y_max, yerr=y_err, fmt='<',label=sim_label)
    # legend, save and show
    plt.legend(loc='upper right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    #plt.show()

def plot_critical_cal(y_max, y_err, parameters):
    """ Plot cal_max as a function of L"""

    title = "Fit cal_max as a function of L"
    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ C_V $')
    plt.xlabel(r'$ \log L $')
    # plot data and fit in function of beta
    fit_x = np.linspace(logsides[0], logsides[-1], 100)
    fit_y = fit_lin(fit_x, *parameters)
    fit_label = f'fit y = c + a * logL'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    sim_label = f'simulation data'
    plt.errorbar(logsides, y_max, yerr=y_err, fmt='<',label=sim_label)
    # legend, save and show
    plt.legend(loc='lower right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    #plt.show()

#--- Size-scaling subroutines --------------------------------------------------

def plot_chi_scaling(data, beta_c, ratio, nu):
    """ Plot susceptibility scaling """

    title = "Plot scaling susceptibility"
    print(title + "\n")
    # axis and style
    fig = plt.figure(title)
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \chi / L^{\gamma / \nu}$')
    plt.xlabel(r'$(\beta - \beta_c) L^{1 / \nu} $')
    # load and plot susceptibility in function of beta
    for side in sides:
        x, _, _, _, _, _, _, y, y_err = data[side]
        y = y / np.power(side, ratio)
        y_err = y_err / np.power(side, ratio)
        x = (x - beta_c) * np.power(side, (1/nu))
        plt.errorbar(x, y, yerr=y_err, fmt='.', label=f'side = {side}')
    # save and show
    plt.legend(loc='upper right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    #plt.show()

def plot_mag_scaling(data, beta_c, ratio, nu):
    """ Plot magnetization scaling """

    title = "Plot scaling magnetization"
    print(title + "\n")
    # axis and style
    fig = plt.figure(title)
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \langle |M| \rangle / L^{-\beta / \nu}$')
    plt.xlabel(r'$(\beta - \beta_c) L^{1 / \nu} $')
    # load and plot susceptibility in function of beta
    for side in sides:
        x, _, _, y, y_err, _, _, _, _ = data[side]
        y = y / np.power(side, - ratio)
        y_err = y_err / np.power(side, - ratio)
        x = (x - beta_c) * np.power(side, (1/nu))
        plt.errorbar(x, y, yerr=y_err, fmt='.', label=f'side = {side}')
    # save and show
    plt.legend(loc='upper right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    #plt.show()

def plot_cal_scaling(data, beta_c, param, nu):
    """ Plot specific heat scaling """

    title = "Plot scaling specific heat"
    print(title + "\n")
    # axis and style
    fig = plt.figure(title)
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ C_V / log(L) + c $')
    plt.xlabel(r'$(\beta - \beta_c) L^{1 / \nu} $')
    # load and plot susceptibility in function of beta
    for side in sides:
        x, _, _, _, _, y, y_err, _, _ = data[side]
        y = y / (param*np.log(side))
        y_err = y_err / (param*np.log(side))
        x = (x - beta_c) * np.power(side, (1/nu))
        plt.errorbar(x, y, yerr=y_err, fmt='.', label=f'side = {side}')
    # save and show
    plt.legend(loc='upper right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    #plt.show()
