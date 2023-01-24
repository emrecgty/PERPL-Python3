# Import third-party libraries
import numpy as np

def get_vectors(d_values, dims):
    """Calculates the vector components of relative positions. This
    function saves both 2D and 3D data.

    Args:
        d_values: numpy array of localisations with distances between the
                  localisations.
        dim: The dimensions of the data ie 2D or 3D.

    Returns:
        d_values (numpy array): Array of vector components.
    """
    #for i in range(0, 10):
    #    print(d_values[i])
    x_square_values = np.square(d_values[:, 0])
    y_square_values = np.square(d_values[:, 1])

    if dims == 3:
        z_square_values = np.square(d_values[:, 2])

    # Calculate distances across planes and 3D space
    xy_distance_values = np.sqrt(x_square_values + y_square_values)

    if dims == 3:
        xz_distance_values = np.sqrt(x_square_values + z_square_values)
        yz_distance_values = np.sqrt(y_square_values + z_square_values)
        xyz_distance_values = np.sqrt(x_square_values + y_square_values + z_square_values)

    # Include these distances in the output table
    d_values = np.column_stack((d_values, xy_distance_values))

    if dims == 3:
        d_values = np.column_stack((d_values, xz_distance_values))
        d_values = np.column_stack((d_values, yz_distance_values))
        d_values = np.column_stack((d_values, xyz_distance_values))

    if dims == 2:
        d_values.view('f8,f8,f8,f8').sort(order=['f3'], axis=0)

    if dims == 3:
        d_values.view('f8,f8,f8,f8,f8,f8,f8').sort(order=['f6'], axis=0)

    return d_values