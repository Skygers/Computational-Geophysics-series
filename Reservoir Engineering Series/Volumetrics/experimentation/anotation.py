import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.cm as cm
import numpy as np

def plot_contour_with_annotations(data, save_path=None):
    x, y, z = data['x'], data['y'], data['DEPTH']
    
    # Create the triangulation
    triang = tri.Triangulation(x, y)

    plt.figure(figsize=(20, 10))
    plt.gca().set_aspect('equal')
    plt.triplot(triang, lw=0.5, color='white')

    # Define contour levels
    levels = np.linspace(min(z) + 10, max(z) - 10, 10)

    # Use the colormap
    cmap = cm.get_cmap(name='terrain')

    # Plot filled contours and lines
    contour_filled = plt.tricontourf(triang, z, levels=levels, cmap=cmap)
    contour_lines = plt.tricontour(triang, z, levels=levels, colors='k', linewidths=0.5)

    # Plot well points
    plt.plot(x, y, 'ko', ms=3)

    # Add annotations to some well points
    for i in range(len(x)):
        plt.annotate(f'Well {i+1}', (x[i], y[i]), textcoords="offset points", xytext=(5,5), ha='center', fontsize=8)

    # Set title and labels
    plt.title("Structure Map with Well Annotations", pad=10, size=20)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    
    # Add colorbar
    plt.colorbar(contour_filled, label='Depth')

    if save_path:
        plt.savefig(save_path, format='png', dpi=300)
        print(f"Annotated plot saved to {save_path}")
    
    plt.show()

