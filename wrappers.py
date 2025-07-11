"""
Pridey.wrappers
Plotting wrapper functions and fitting utilities.
"""
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit

# --- Fitting functions and labels ---
linear_fit = lambda x, a, b: a*x + b
linear_label = lambda a, b: f"$y = {a:.2f}x+ {b:.2f}$"
quad_fit = lambda x, a, b, c: a*x**2 + b*x +c
quad_label = lambda a, b, c: f"$y = {a:.2f}x^2 + {b:.2f}x+c$"
exp_fit = lambda x, a, b: a* np.exp( b * x)
exp_label = lambda a, b: f"$y = {a:.2f} e^{{{b:.2f} x}}$"

def plot_fit(ax, x, y, fit_func, label=None, **kwargs):
    """
    Fits a curve to the data and plots the fit on the given axes.
    Returns fit parameters, covariance matrix, and R^2 value.
    """
    popt, popc = curve_fit(fit_func, x, y)
    if callable(label):
        label = label(*popt)
    spread = max(x) - min(x)
    xfit = np.linspace(min(x) - spread, max(x) + spread, 1000)
    y_fit = fit_func(xfit, *popt)
    label = f'{label}' if label else None
    sns.lineplot(ax=ax, x=xfit, y=y_fit, label=label, **kwargs)
    ss_res = np.sum((y - fit_func(x, *popt)) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    R2 = 1 - (ss_res / ss_tot)
    return popt, popc, R2
