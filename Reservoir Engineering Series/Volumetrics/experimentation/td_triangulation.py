import pandas as pd
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

def plot_contour(data, save_path=None):
    x, y, z = data['x'], data['y'], data['DEPTH']
    
    # Create the Triangulation
    triang = tri.Triangulation(x, y)

    # Refine the Triangulation
    refiner = tri.UniformTriRefiner(triang)
    tri_refined, z_refined = refiner.refine_field(z, subdiv=5)

    # Plot the triangulation and high-resolution contours
    plt.figure(figsize=(20, 10))
    plt.gca().set_aspect('equal')
    plt.triplot(triang, lw=0.5, color='white')

    # Define contour levels
    levels = np.linspace(min(z) + 10, max(z) - 10, 10)

    # Use the colormap
    cmap = cm.get_cmap(name='terrain')

    # Plot filled contours and lines for refined data
    contour_filled = plt.tricontourf(tri_refined, z_refined, levels=levels, cmap=cmap)
    contour_lines = plt.tricontour(tri_refined, z_refined, levels=levels, colors='k', linewidths=0.5)

    # Plot well points
    plt.plot(x, y, 'ko', ms=3)

    # Add labels to contours
    plt.clabel(contour_lines, contour_lines.levels[::2], inline=True, fontsize=10)

    # Set title
    plt.title("Structure Map using Triangulation Method", pad=10, size=20)

    # Add colorbar for better interpretation
    plt.colorbar(contour_filled)

    # Save the plot if a save path is provided
    if save_path:
        plt.savefig(save_path, format='png', dpi=300)
        print(f"Plot saved to {save_path}")
    
    # Show plot
    plt.show()
