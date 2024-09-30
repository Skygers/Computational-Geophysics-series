import matplotlib.tri as tri
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_contour(data, save_path=None):
    x, y, z = data['x'], data['y'], data['DEPTH']
    
    # Create the triangulation
    triang = tri.Triangulation(x, y)

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot a 3D trisurface
    ax.plot_trisurf(triang, z, cmap=cm.terrain, edgecolor='none')

    # Label axes
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Depth')
    ax.set_title('3D Structure Map using Triangulation')

    if save_path:
        plt.savefig(save_path, format='png', dpi=300)
        print(f"3D plot saved to {save_path}")

    plt.show()
