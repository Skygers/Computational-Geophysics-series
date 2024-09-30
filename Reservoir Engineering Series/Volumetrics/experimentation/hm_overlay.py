import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from scipy.interpolate import griddata

def plot_contour_with_heatmap(data, save_path=None):
    x, y, z = data['x'], data['y'], data['DEPTH']
    
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')

    plt.figure(figsize=(20, 10))
    contour_filled = plt.contourf(xi, yi, zi, levels=15, cmap='terrain', alpha=0.6)

    plt.scatter(x, y, c='black', marker='o', s=5)

    triang = tri.Triangulation(x, y)
    contour_lines = plt.tricontour(triang, z, levels=15, colors='black', linewidths=0.5)

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Contour Map with Heatmap Overlay')
    plt.colorbar(contour_filled,label='Depth')

    if save_path:
        plt.savefig(save_path, format='png', dpi=300)
        print(f"Heatmap overlay saved to {save_path}")
    
    plt.show()
