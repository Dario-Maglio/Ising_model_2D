import os

import numpy as np
import matplotlib.pyplot as plt

side = 70
beta = 0.440000
DIM = 200000

#-------------------------------------------------------------------------------

def plot_metropolis():

    fig, axes = plt.subplots(1, 2, num="energy and magnet", figsize=(12, 12))

    axes[0].set_title("Energy density")
    axes[0].set_ylabel(r'$\epsilon$')
    axes[0].set_xlabel('$step$')

    axes[1].set_title("Magnetization density")
    axes[1].set_ylabel(r'$ M $')
    axes[1].set_xlabel(r'$step$')

    directory = f"../Data_simulations/Side_{side}"
    filename = "side_{0}_beta_{1:.6f}.dat".format(side, beta)
    file = os.path.join(directory, filename)
    print("Loading file " + file)

    x = [ i for i in range(DIM)]

    if os.path.isfile(file):
        ene, mag = np.loadtxt(file, unpack='True')
        axes[0].plot(x, ene[:DIM])
        axes[1].plot(x, abs(mag[:DIM]))

    print("\nPlots of energy and magnetization: \n")
    plt.show()


#-------------------------------------------------------------------------------

if __name__ == '__main__':

    plot_metropolis()
