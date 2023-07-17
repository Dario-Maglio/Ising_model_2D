"""*****************************************************************************
*
* Plot and fit program for the critical exponents
*
*****************************************************************************"""

import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat, unumpy

# import data, fit functions and plot subroutines
from critical_plots_subr import *

#*******************************************************************************
# PARAMETERS OF THE SIMULATION
#
# interval = data interval to fit for chi and cal.
#
#*******************************************************************************

interval_chi = {20:(10,45), 30:(19,57), 40:(32,58),
                50:(38,62), 60:(43,62), 70:(45,62)}
interval_cal = {20:(24,58), 30:(38,64), 40:(45,69),
                50:(48,66), 60:(51,70), 70:(53,71)}

#--- Parabolic fit subroutines -------------------------------------------------

def par_max_fit(fit_x, fit_y, fit_e):
    """ Get y_max values and correspinding x_max with parabolic fit """

    # fit the parabola
    parameters, covariance = curve_fit(fit_par, fit_x, fit_y, sigma=fit_e, bounds=((-np.inf, 0, 0), (0, 0.5, np.inf)))
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
    print("Max x coordinate:")
    x_max = par_b
    print(x_max)
    print("Max y coordinate:")
    y_max = par_c
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

#--- Mag interpolation ---------------------------------------------------------

def critical_mag(data, beta):
    """ Subroutine for selecting mag max """

    mag_cri = []
    mag_err = []

    for side in sides:
        # select mag data
        x, _, _, y, y_err, _, _, _, _ = data[side]
        x, y, y_err = zip(*sorted(zip(x, y, y_err)))
        # select nearest point to beta
        index_nearest = min(range(len(x)), key=lambda i: abs(x[i] - beta))
        mag_cri.append(y[index_nearest])
        mag_err.append(y_err[index_nearest])

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
    nu_exp = par_b
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
    par_c = ufloat(parameters[1], std_deviation[1])
    print(par_c)
    # compute reduced chi squared
    fitted_y = fit_lin(logsides, *parameters)
    chisq = np.sum(np.power(((logy - fitted_y)/ loge), 2))
    chisqrd = chisq / (len(sides) - 3)
    print(f"Reduced chi squared: \n{chisqrd}")
    # compute results
    ratio = par_a
    return (ratio, parameters)

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
    ratio_gamma_nu, parameters = critical_ratio(logy, loge)
    # compute exponent
    print("\nCritical exponent gamma:")
    gamma_exp = nu_exp * ratio_gamma_nu
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
    ratio_beta_nu, parameters = critical_ratio(logy, loge)
    # compute exponent
    print("\nCritical exponent beta:")
    beta_exp = - nu_exp * ratio_beta_nu
    print(beta_exp)
    # plot results
    print("\nPlot mag_cri as a function of L\n")
    plot_critical_mag(logy, loge, parameters)

    #---Critical alpha
    print("Study cal_max")
    ratio, parameters = critical_ratio(cal_max, cal_err)
    print("\nPlot chi_max as a function of L\n")
    plot_critical_cal(cal_max, cal_err, parameters)

    #------ Finite size-scaling
    print("--- Study the finite size scaling -----------\n")
    plot_chi_scaling(data, 0.44068, 7/4, 1)
    plot_mag_scaling(data, 0.44068, 1/8, 1)
    plot_cal_scaling(data, 0.44068, parameters, 1)
