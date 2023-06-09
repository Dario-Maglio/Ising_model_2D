"""*****************************************************************************
*
* Plot and fit program for the critical exponents
*
*****************************************************************************"""

import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import make_interp_spline
from uncertainties import ufloat, unumpy

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

interval_chi = {20:(11,40), 30:(11,60), 40:(21,64),
                50:(38,58), 60:(40,63), 70:(46,64)}
interval_cal = {20:(21,56), 30:(35,64), 40:(46,66),
                50:(43,66), 60:(50,66), 70:(50,66)}
interval_mag = {20:(5,70), 30:(5,70), 40:(5,70),
                50:(5,70), 60:(5,70), 70:(5,70)}

#--- Contents ------------------------------------------------------------------

def fit_lin(x, a, b):
    y = a * np.power(x, 1) + b
    return y

def fit_par(x, a, b, c):
    y = a * np.power(x, 2) + b * np.power(x, 1) + c
    return y

def fit_beta(x, a, b, c):
    y = a / np.power(x, b) + c
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

#--- Parabolic fit subroutines -------------------------------------------------

def par_max_fit(fit_x, fit_y, fit_e):
    """ Get y_max values and correspinding x_max with parabolic fit """

    # fit the parabola
    parameters, covariance = curve_fit(fit_par, fit_x, fit_y, sigma=fit_e)
    std_deviation = np.sqrt(np.diag(covariance))
    # print values and uncertainties
    print("Fit parameters:")
    par_a = ufloat(parameters[0], std_deviation[0])
    print(par_a)
    par_b = ufloat(parameters[1], std_deviation[1])
    print(par_b)
    par_c = ufloat(parameters[2], std_deviation[2])
    print(par_c)
    # compute y_max and x_max
    print("Max point:")
    x_max = - par_b / (2 * par_a)
    print(x_max)
    y_max = (par_b * par_b)/(4 * par_a)
    y_max = y_max - (par_b * par_b)/(2 * par_a) + par_c
    print(y_max)
    # compute reduced chi squared
    fitted_y = fit_par(fit_x, *parameters)
    chisq = np.sum(np.power(((fit_y - fitted_y)/ fit_e), 2))
    chisqrd = chisq / (len(fit_x) - 4)
    print(f"Reduced chi squared: \n{chisqrd}\n")
    return (x_max, y_max, parameters)

def parabolic_fit_chi(data):
    """ Subroutine for parabolic fit of chi max """

    beta_pc = []
    beta_er = []
    chi_max = []
    chi_err = []

    for side in sides:
        # select chi data to fit
        x, _, _, _, _, _, _, y, y_err = data[side]
        x, y, y_err = zip(*sorted(zip(x, y, y_err)))
        a = interval_chi[side][0]
        b = interval_chi[side][1]
        # fit and append
        print(f"Susceptibility side {side}")
        x_max, y_max, parameters = par_max_fit(x[a:b], y[a:b], y_err[a:b])
        beta_pc.append(x_max.n)
        beta_er.append(x_max.std_dev)
        chi_max.append(y_max.n)
        chi_err.append(y_max.std_dev)
        # plot data and fit
        title = f"Fit max susceptibility side: {side} "
        print(title + "\n")
        plot_par_chi(x, y, y_err, a, b, parameters, title)

    return beta_pc, beta_er, chi_max, chi_err

def parabolic_fit_cal(data):
    """ Subroutine for parabolic fit of cal max"""

    cal_max = []
    cal_err = []

    for side in sides:
        # select cal data to fit
        x, _, _, _, _, y, y_err, _, _ = data[side]
        x, y, y_err = zip(*sorted(zip(x, y, y_err)))
        a = interval_cal[side][0]
        b = interval_cal[side][1]
        # fit and append
        print(f"Specific heat side {side}")
        x_max, y_max, parameters = par_max_fit(x[a:b], y[a:b], y_err[a:b])
        cal_max.append(y_max.n)
        cal_err.append(y_max.std_dev)
        # plot data and fit
        title = f"Fit max specific heat side: {side} "
        print(title + "\n")
        plot_par_cal(x, y, y_err, a, b, parameters, title)

    return cal_max, cal_err

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
    plt.show()

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
    plt.show()

#--- Mag interpolation ---------------------------------------------------------

def critical_mag(data, beta):
    """ Subroutine for parabolic fit of mag max """

    mag_cri = []
    mag_err = []

    for side in sides:
        # select mag data
        x, _, _, y, y_err, _, _, _, _ = data[side]
        x, y, y_err = zip(*sorted(zip(x, y, y_err)))

        # interpolation of critical mag
        # x = x[63:69]
        # y = y[63:69]
        # # interpolate the critical magnetization
        # mag_fun_2 = make_interp_spline(x, y, k=2)
        # mag_fun_3 = make_interp_spline(x, y, k=3)
        # # compute mag_cri with error systematic + nearest
        # print("Critical magnetization:")
        # mag_c_val = (mag_fun_3(beta.n) + mag_fun_2(beta.n)) / 2
        # mag_c_err = abs(mag_fun_3(beta.n) - mag_fun_2(beta.n))
        # mag_c_err = mag_c_err + y_err[66]
        # print(f"{mag_c_val} pm {mag_c_err}")
        # mag_cri.append(mag_c_val)
        # mag_err.append(mag_c_err)

        mag_cri.append(y[66])
        mag_err.append(y_err[66])

    return mag_cri, mag_err

#--- Critical ratios and Beta --------------------------------------------------

def critical_point(beta_pc, beta_er):
    """ Get critical point and nu from beta pseudo critical """

    # exponential fit
    parameters, covariance = curve_fit(fit_beta, sides, beta_pc, sigma=beta_er)
    std_deviation = np.sqrt(np.diag(covariance))
    # print values and uncertainties
    print("Fit parameters:")
    par_a = ufloat(parameters[0], std_deviation[0])
    print(par_a)
    par_b = ufloat(parameters[1], std_deviation[1])
    print(par_b)
    par_c = ufloat(parameters[2], std_deviation[2])
    print(par_c)
    # compute reduced chi squared
    fitted_y = fit_beta(sides, *parameters)
    chisq = np.sum(np.power(((beta_pc - fitted_y)/ beta_er), 2))
    chisqrd = chisq / (len(sides) - 4)
    print(f"Reduced chi squared: \n{chisqrd}")
    # compute results
    beta_cr = par_c
    nu_exp = 1 / par_b
    return (beta_cr, nu_exp, parameters)

def critical_ratio(logy, loge):
    """ Get critical exponent ratio fitting a linear function """

    # fit
    parameters, covariance = curve_fit(fit_lin, logsides, logy, sigma=loge)
    std_deviation = np.sqrt(np.diag(covariance))
    # print values and uncertainties
    print("Fit parameters:")
    par_a = ufloat(parameters[0], std_deviation[0])
    print(par_a)
    par_b = ufloat(parameters[1], std_deviation[1])
    print(par_b)
    # compute reduced chi squared
    fitted_y = fit_lin(logsides, *parameters)
    chisq = np.sum(np.power(((logy - fitted_y)/ loge), 2))
    chisqrd = chisq / (len(sides) - 3)
    print(f"Reduced chi squared: \n{chisqrd}")
    # compute results
    ratio = par_a
    return (ratio, parameters)

#--- Plot subroutines ----------------------------------------------------------

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
    fit_label = r'fit y = c + a / x^b'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    plt.errorbar(sides, beta_pc, yerr=beta_er, fmt='.', label=f'simulation')
    # legend, save and show
    plt.legend(loc='lower right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    plt.show()

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
    fit_label = f'fit logy = ratio * logL + b'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    sim_label = f'simulation data'
    plt.errorbar(logsides, y_max, yerr=y_err, fmt='<',label=sim_label)
    # legend, save and show
    plt.legend(loc='lower right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    plt.show()

def plot_critical_mag(y_max, y_err, parameters):
    """ Plot magnetization as a function of L"""

    title = "Fit magnetization as a function of L"
    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \log \langle | M | \rangle $')
    plt.xlabel(r'$ \log L $')
    # plot data and fit in function of beta
    fit_x = np.linspace(logsides[0], logsides[-1], 100)
    fit_y = fit_lin(fit_x, *parameters)
    fit_label = f'fit logy = ratio * logL + b'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    sim_label = f'simulation data'
    plt.errorbar(logsides, y_max, yerr=y_err, fmt='<',label=sim_label)
    # legend, save and show
    plt.legend(loc='upper right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    plt.show()

def plot_critical_cal(y_max, y_err, parameters):
    """ Plot cal_max as a function of L"""

    title = "Fit cal_max as a function of L"
    fig = plt.figure(title)
    # axis and style
    plt.style.use('seaborn-whitegrid')
    plt.title(title)
    plt.ylabel(r'$ \log C_V $')
    plt.xlabel(r'$ \log L $')
    # plot data and fit in function of beta
    fit_x = np.linspace(logsides[0], logsides[-1], 100)
    fit_y = fit_lin(fit_x, *parameters)
    fit_label = f'fit logy = ratio * logL + b'
    plt.plot(fit_x, fit_y, '-', label=fit_label)
    sim_label = f'simulation data'
    plt.errorbar(logsides, y_max, yerr=y_err, fmt='<',label=sim_label)
    # legend, save and show
    plt.legend(loc='lower right')
    plt.savefig(os.path.join("Plots_and_fit", title + ".png"))
    plt.show()

#--- Main ----------------------------------------------------------------------

if __name__ == '__main__':

    data = load_data()
    print("Loading complete! \n")

    #--- Parabolic fit
    print("--- Start parabolic fit for chi and cal -----\n")

    beta_pc, beta_er, chi_max, chi_err = parabolic_fit_chi(data)
    cal_max, cal_err = parabolic_fit_cal(data)

    #--- Critical point
    print("--- Study the critical point ----------------\n")

    print("Study pseudo critical beta")
    beta_cr, nu_exp, parameters = critical_point(beta_pc, beta_er)

    print("\nCritical beta:")
    print(beta_cr)
    print("Critical exponent nu:")
    print(nu_exp)

    print("\nPlot beta_pc as a function of L\n")
    plot_beta_critical(beta_pc, beta_er, parameters)

    #------ Critical ratios
    print("--- Study the critical ratios ---------------\n")

    #--- Critical ratio gamma
    print("Study chi_max")
    # format data in log scale
    uy = [ ufloat(val, err) for val, err in zip(chi_max, chi_err)]
    loguy = unumpy.log(uy)
    logy = [val.n for val in loguy]
    loge = [val.std_dev for val in loguy]
    # fit the data
    ratio, parameters = critical_ratio(logy, loge)
    # compute exponent
    print("\nCritical exponent gamma:")
    gamma_exp = nu_exp * ratio
    print(gamma_exp)
    # plot results
    print("\nPlot chi_max as a function of L\n")
    plot_critical_chi(logy, loge, parameters)

    #--- Critical ratio beta
    print("Study magnetization")
    # get magnetization data
    mag_cri, mag_err = critical_mag(data, beta_cr)
    # format data in log scale
    uy = [ ufloat(val, err) for val, err in zip(mag_cri, mag_err)]
    loguy = unumpy.log(uy)
    logy = [logval.n for logval in loguy]
    loge = [logval.std_dev for logval in loguy]
    # fit the data
    ratio, parameters = critical_ratio(logy, loge)
    # compute exponent
    print("\nCritical exponent beta:")
    beta_exp = - nu_exp * ratio
    print(beta_exp)
    # plot results
    print("\nPlot mag_cri as a function of L\n")
    plot_critical_mag(logy, loge, parameters)

    #---Critical ratio alpha
    print("Study cal_max")
    # format data in log scale
    uy = [ ufloat(val, err) for val, err in zip(cal_max, cal_err)]
    loguy = unumpy.log(uy)
    logy = [logval.n for logval in loguy]
    loge = [logval.std_dev for logval in loguy]
    # fit the data
    ratio, parameters = critical_ratio(logy, loge)
    # compute exponent
    print("\nCritical exponent alpha:")
    alpha_exp = - nu_exp * ratio
    print(alpha_exp)
    # plot results
    print("\nPlot chi_max as a function of L\n")
    plot_critical_cal(logy, loge, parameters)
