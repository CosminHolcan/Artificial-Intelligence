# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""

t_values = dict()
t_values['NVB'] = [None, -40, - 25]
t_values['NB'] = [-40, -25, -10]
t_values['N'] = [-20, -10, 0]
t_values['ZO'] = [-5, 0, 5]
t_values['P'] = [0, 10, 20]
t_values['PB'] = [10, 25, 40]
t_values['PVB'] = [25, 40, None]

w_values = dict()
w_values['NB'] = [None, -8, -3]
w_values['N'] = [-6, -3, 0]
w_values['ZO'] = [-1, 0, 1]
w_values['P'] = [0, 3, 6]
w_values['PB'] = [3, 8, None]

f_values = dict()
f_values['NVVB'] = [None, -32, -24]
f_values['NVB'] = [-32, -24, -16]
f_values['NB'] = [-24, -16, -8]
f_values['N'] = [-16, -8, 0]
f_values['Z'] = [-4, 0, 4]
f_values['P'] = [0, 8, 16]
f_values['PB'] = [8, 16, 24]
f_values['PVB'] = [16, 24, 32]
f_values['PVVB'] = [24, 32, None]

b_values = dict()
b_values['NVVB'] = -32
b_values['NVB'] = -24
b_values['NB'] = -16
b_values['N'] = -8
b_values['Z'] = 0
b_values['P'] = 8
b_values['PB'] = 16
b_values['PVB'] = 24
b_values['PVVB'] = 32

rules = dict()
rules['PVB'] = dict()
rules['PVB']['PB'] = 'PVVB'
rules['PVB']['P'] = 'PVVB'
rules['PVB']['ZO'] = 'PVB'
rules['PVB']['N'] = 'PB'
rules['PVB']['NB'] = 'P'
rules['PB'] = dict()
rules['PB']['PB'] = 'PVVB'
rules['PB']['P'] = 'PVB'
rules['PB']['ZO'] = 'PB'
rules['PB']['N'] = 'P'
rules['PB']['NB'] = 'Z'
rules['P'] = dict()
rules['P']['PB'] = 'PVB'
rules['P']['P'] = 'PB'
rules['P']['ZO'] = 'P'
rules['P']['N'] = 'Z'
rules['P']['NB'] = 'N'
rules['ZO'] = dict()
rules['ZO']['PB'] = 'PB'
rules['ZO']['P'] = 'P'
rules['ZO']['ZO'] = 'Z'
rules['ZO']['N'] = 'N'
rules['ZO']['NB'] = 'NB'
rules['N'] = dict()
rules['N']['PB'] = 'P'
rules['N']['P'] = 'Z'
rules['N']['ZO'] = 'N'
rules['N']['N'] = 'NB'
rules['N']['NB'] = 'NVB'
rules['NB'] = dict()
rules['NB']['PB'] = 'Z'
rules['NB']['P'] = 'N'
rules['NB']['ZO'] = 'NB'
rules['NB']['N'] = 'NVB'
rules['NB']['NB'] = 'NVVB'
rules['NVB'] = dict()
rules['NVB']['PB'] = 'N'
rules['NVB']['P'] = 'NB'
rules['NVB']['ZO'] = 'NVB'
rules['NVB']['N'] = 'NVVB'
rules['NVB']['NB'] = 'NVVB'

def compute_degree(x, x0, x1, x2):
    # first equation : y = (x-x0) / (x1 - x0)
    # second equation : y = (x-x2) / (x1 - x2)
    if x0 == None:
        if x1 <= x <= x2:
            y = (x - x2) / (x1 - x2)
            return y
        elif x < x1:
            return 1
        else:
            return 0
    elif x2 == None:
        if x0 <= x <= x1:
            y = (x - x0) / (x1 - x0)
            return y
        elif x > x1:
            return 1
        else:
            return 0
    else:
        if x0 <= x <= x1:
            y = (x - x0) / (x1 - x0)
            return y
        elif x1 < x <= x2:
            y = (x - x2) / (x1 - x2)
            return y
        else:
            return 0

def t_membership_degrees(x):
    result = dict()
    for key in t_values.keys() :
        values = t_values[key]
        x0 = values[0]
        x1 = values[1]
        x2 = values[2]
        y = compute_degree(x, x0, x1, x2)
        result[key] = y
    return result

def w_membership_degrees(x) :
    result = dict()
    for key in w_values.keys():
        values = w_values[key]
        x0 = values[0]
        x1 = values[1]
        x2 = values[2]
        y = compute_degree(x, x0, x1, x2)
        result[key]= y
    return result

def solver(t, w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or

    None :if we have a division by zero

    """
    t_degrees = t_membership_degrees(t)
    w_degrees = w_membership_degrees(w)
    f_degrees = dict()
    for key in f_values.keys():
        f_degrees[key] = None
    for t_class in rules.keys() :
        for w_class in rules[t_class].keys():
            f_class = rules[t_class][w_class]
            f_degree = min(t_degrees[t_class], w_degrees[w_class])
            if f_degrees[f_class] == None :
                f_degrees[f_class] = f_degree
            else :
                current_degree = f_degrees[f_class]
                f_degrees[f_class] = max(current_degree, f_degree)
    degrees_sum = 0
    weighted_sum = 0
    for f_class in f_degrees.keys():
        degrees_sum += f_degrees[f_class]
        print(f_class, f_degrees[f_class])
        weighted_sum += f_degrees[f_class]*b_values[f_class]
    if degrees_sum == 0 :
        return None
    return weighted_sum / degrees_sum



