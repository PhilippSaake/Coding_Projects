# -*- coding: utf-8 -*-
"""
Created in Aug 2024 by Philipp

Python implementation of calculation and plotting routine to calculate the 
Inflation parameter predictions from a scale-invariant potential and its
spontaneous symmetry breaking.
"""

# Importing the necessary packages
## System packages for potentially storing data
import sys
import re
import os
## Numpy for calculations
import numpy as np
from scipy.optimize import fsolve
## Matplotlib for visualization of results
import matplotlib.pyplot as plt
import matplotlib.colors as col

# Defining global constants used in the calculation
## Cosmological reference parameters
kStar = 0.002
log_kStar = np.log(0.002 / 67.74 / 1000 * 299792458)
## Number of degrees of freedom during reheating phase
gRH = 117.25
## Reduced Planck mass in GeV
mPl_red = 1.220890*10**19  / np.sqrt(8 * np.pi)

# Defining the effective potential in terms of their tree level contributions
# and their field dependent masses
# ! Capital letters -> fields, lower-case -> dimensionless couplings !

## Tree-level classical scale invariant potential --> 1 scalar self interaction
def potential_tree_level(l):
    return(lambda S: 0.25 * l * S**4)
    
## Field dependent mass-squares from the contributions including all scale-invariant
## terms from the tree level Lagrangian curvature contractions (= m_i^2)
def field_mass_kappa(b,k):
    return(lambda S : b * S**2 / 4 / k)

def field_mass_plus(l,b,g):
    return(lambda S : S**2 *(3 / 2 * l + b * (1 + 6 * b) / 24 / g
                  + ( (36 * l * g + b + 6 * b)**2 - 144 * g * b * l)**(1/2)
                  / 24 / g)
           )

def field_mass_minus(l,b,g):
    return(lambda S: S**2 *(3 / 2 * l + b * (1 + 6 * b) / 24 / g
                  - ( (36 * l * g + b + 6 * b)**2 - 144 * g * b * l)**(1/2)
                  / 24 / g)
           )

## (Full) one-loop potential (in MS-bar renormalization procedure)
def potential_full_one_loop(l,b,g,k,mu):
    temp_m_plus = field_mass_plus(l, b, g)
    temp_m_minus = field_mass_minus(l, b, g)
    temp_m_kappa = field_mass_kappa(b,k)
    return(lambda S: potential_tree_level(l)(S) + 1 / 64 / (np.pi**2) * 
           (temp_m_plus(S)**2 * (np.log(temp_m_plus(S) / mu**2) - 3 / 2)
            + temp_m_minus(S)**2 * (np.log(temp_m_minus(S) / mu**2) - 3 / 2)
            + 5 * temp_m_kappa(S)**2 * (np.log(temp_m_kappa(S) / mu**2) - 1/10)
            )
          )

# Calculating the symmetry breaking of the one-loop potential and therefore the
# VEV, the zero-point energy and giving a to-zero normalized potential
def find_vev(l,b,g,k,mu):
    """Finds and returns the global minimum of the full one-loop potential"""
    # Here we "hardcode" the accuracy of the numerical min-finding in order to 
    # reduce the number of arguments of these functions --> could also be added
    x_start,x_stop,steps = 0.001, 5, 10**6
    # First coarse look for the minimum
    x1 = np.linspace(x_start, x_stop,10)
    temp_vev = x1[np.where(min(potential_full_one_loop(l, b, g, k, mu)(x1)) ==
        potential_full_one_loop(l, b, g, k, mu)(x1))[0]]
    # Now more specific searching for minimum in the area of the temp_min
    if temp_vev < 1:
        x2 = np.linspace(0.001, temp_vev + 1,steps)
    elif temp_vev >= 1:
        x2 = np.linspace(temp_vev * 0.01, temp_vev*2,steps)
    else:
        print("vev_error")
    return(x2[np.where(min(potential_full_one_loop(l, b, g, k, mu)(x2)) ==
        potential_full_one_loop(l, b, g, k, mu)(x2))][0])

def potential_norm_one_loop(l,b,g,k,mu,vev):
    """Returns the normalized potential to be zero at the vev, with fixed 
    dimensionless couplings and still depending on S.
    To calculate, use find_vev(). As we need the vev for multiple calculations
    I chose to parse it in this function.
    """
    return(lambda S: potential_full_one_loop(l, b, g, k, mu)(S)
           - potential_full_one_loop(l, b, g, k, mu)(vev))

# Some more calculations now for the potential after symmetry breaking and thus
# depending on the generated vev
## Planck mass
def mass_planck(b,vev):
    """Calculates the Planck masses value in dependence of the renormalization 
    scheme and therefore its scale.
    """
    return(np.sqrt(b) * vev)

## B, A as shorthand functions for the potential after conformal transformation
## to the Einstein frame, but dependent on the field S
def factor_B(b,mu,mpl):
    return(lambda S: mu**2 * b * S**2 / mpl**2)
    
def factor_A(l, b, g, k, mu, vev, mpl):
    return(lambda S: 4 * g * potential_norm_one_loop(l, b, g, k, mu, vev)(S)
           / factor_B(b, mu, mpl)(S)**2 / mpl**4)


# Defining the final form of the inflation potential
def potential_inflation(l, b, g, k, mu, vev, mpl):
    return(lambda S: potential_norm_one_loop(l, b, g, k, mu, vev)(S) / 
           (1 + 4 * factor_A(l, b, g, k, mu, vev, mpl)(S))
           / factor_B(b, mu, mpl)(S)**2)


