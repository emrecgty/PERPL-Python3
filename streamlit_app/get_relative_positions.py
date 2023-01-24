# Import standard libraries
from typing import Optional

# Import third-party libraries
import numpy as np

# Import local libraries
from get_distances import getdistances, getdistances_two_colours

def get_relative_positions(
                            xyzcolour_values: np.ndarray,
                            filter_dist: float,
                            dims: int,
                            start_channel: int,
                            end_channel: int,
                            color_count: Optional[int] = None,
                            ):
    """Get relative positions of cells in a channel or between two channels.

    Parameters
    ----------
    xyzcolour_values : numpy.ndarray
        Array of xyz coordinates and colour values.
    filter_dist : float
        Distance (in all three dimensions) between points within
        which relative positions are calculated. This can be chosen by
        user input as the function runs, or by specifying when calling
        the function from a script.
    dims : int
        Number of dimensions in the data.
    start_channel : int
        Colour channel to measure from.
    end_channel : int
        Colour channel to measure to.
    color_count : int, optional
        Number of colours in the file, by default None

    Returns
    -------
    d_values : numpy.ndarray
        Array of relative positions.
    """
    if color_count is None:
        xyz_values_start = xyzcolour_values[:, 0:dims]
        d_values = getdistances(
            xyz_values_start, filter_dist
            )

    if color_count == 1:
        xyz_values_start = \
            xyzcolour_values[:, 0:dims][xyzcolour_values[:, -1] == start_channel]
        d_values = getdistances(
            xyz_values_start, filter_dist
            )

    if color_count == 2:
        xyz_values_start = \
            xyzcolour_values[:, 0:dims][xyzcolour_values[:, -1] == start_channel]
        xyz_values_end = \
            xyzcolour_values[:, 0:dims][xyzcolour_values[:, -1] == end_channel]
        d_values = getdistances_two_colours(
            xyz_values_start, filter_dist, xyz_values_end
            )
    
    return d_values