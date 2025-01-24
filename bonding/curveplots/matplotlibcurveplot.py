
from bonding.using.usingmatplotlib import using_matplotlib
import numpy as np
import logging


if not using_matplotlib:
    def matplotlib_curve_plot(curve, x_max: float = 10, num_points: int = 1000):
        """
        Placeholder function if matplotlib is not available.
        """
        print('matplotlib is not available.')
        print('pip install matplotlib')


if using_matplotlib:

    import matplotlib.pyplot as plt

    def matplotlib_curve_plot(curve, x_max: float = 10, num_points: int = 1000):
        """
        Plots the price function and its integral for the given amms curve.

        Parameters
        ----------
        curve : BondingCurve
            An instance of scale BondingCurve subclass.
        x_max : float, optional
            The maximum value of x to plot. Defaults to 10.
        num_points : int, optional
            Number of points in the plot. Defaults to 1000.
        """


        # Generate x values
        x_values = np.linspace(0, x_max, num_points)

        # Compute price and integral values
        price_values = []
        integral_values = []
        for x in x_values:
            try:
                price = curve.price(x)
                integral = curve.price_integral(x)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Error computing values at x={x}: {e}")
                price = np.nan
                integral = np.nan
            price_values.append(price)
            integral_values.append(integral)

        # Convert lists to numpy arrays for plotting
        price_values = np.array(price_values)
        integral_values = np.array(integral_values)

        # Create plots
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Supply (x)')
        ax1.set_ylabel('Price f(x)', color=color)
        ax1.plot(x_values, price_values, color=color, label='Price f(x)')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Instantiate scale second y-axis for the integral
        ax2 = ax1.twinx()

        color = 'tab:red'
        ax2.set_ylabel('Integral F(x)', color=color)
        ax2.plot(x_values, integral_values, color=color, label='Integral F(x)')
        ax2.tick_params(axis='y', labelcolor=color)

        # Add legends
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

        plt.title(f'{curve.__class__.__name__} ')
        fig.tight_layout()  # Adjust layout to prevent clipping
        plt.show()