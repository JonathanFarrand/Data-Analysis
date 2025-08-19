import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    """
    A class for plotting various types of data visualizations.
    It provides methods to plot histograms and scatter plots from dictionaries.

    Author: Jonathan Farrand
    
    """
    @staticmethod
    def plot_histogram_dict(data: dict, title='Histogram', x_label='X-Axis', y_label='Y-Axis'):
        """
        Plots a histogram of given data.
        """
        x = list(data.keys())
        y = list(data.values())
        plt.hist(x, weights=y)

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    @staticmethod
    def plot_scatter_dict(data: dict, title='Scatter Plot', x_label='X-Axis', y_label='Y-Axis'):
        """
        Plots a scatter plot of given data.
        """
        x = list(data.keys())
        y = list(data.values())
        plt.scatter(x, y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()