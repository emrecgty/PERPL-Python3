# Import standard libraries
import time

# Import third-party libraries
import numpy as np

def getdistances(xyz_values,
                 filterdist,
                 sort_and_halve=True):
    """Store all vectors between points within a chosen distance of each other
    in all three dimensions in a numpy array. Also works for 2D.

    Args:
        xyz (numpy array):
            Numpy array of localisations with shape (N, 2 or 3),
            where N is the number of localisations.
        filterdist (float):
            Distance (in all three dimensions) between points within
            which relative positions are calculated. This can be chosen by
            user input as the function runs, or by specifying when calling
            the function from a script.
        verbose (Boolean):
            Choice whether to print updates to screen. Defaults to False.
        sort_and_halve (Boolean):
            Choice whether to perform sorting and duplicate removal.
            Defaults to True.

    Returns:
        d (numpy array):
            A numpy array of vectors of neighbours within the filter distance
            for every localisation.
    """
    start_time = time.time()  # Start timing it.

    xyz_filter_values = np.array([filterdist, filterdist, filterdist])

    if True:
        print('\nFinding vectors to nearby localisations:\n')

    # Add 3rd column to 2D localisations
    if xyz_values.shape[1] == 2:
        xyz_values = np.column_stack((xyz_values, np.zeros(xyz_values.shape[0])))

    # Initialise d (array of relative positions)
    separation_values = []

    # Find relative positions of near neighbours to first point.
    # Keep going through the list of points until at least one near neighbour
    # is found.
    xyz_index = 0

    # finding all the separtions in x, y (and z) for the first locatisation
    while len(separation_values) == 0:
        if xyz_index > len(xyz_values) -1:
            break

        one_xyz_value = xyz_values[xyz_index]  # Reference localisation


        # A filter to find localisation coordinates within filterdist of loc
        # Gives np.array of True / False
        boolean_test_results = np.logical_and(
            xyz_values > one_xyz_value - xyz_filter_values,
            xyz_values < one_xyz_value + xyz_filter_values)


        # Find indices of localisations within filterdist
        # in all three dimensions (all True) and select these
        test_results_indices = np.all(boolean_test_results, axis=1)
        subxyz = xyz_values[test_results_indices]

        # Populate d with any near neighbours.
        # len(subxyz) == 1 would mean only the reference localisation was
        # within filterdist.
        # Remove [0,0,0], these are duplicates and can overwhelm the result.
        # Store the vectors from reference loc to the filtered subset
        # of all locs.
        if len(subxyz) != 1:
            separation_values = subxyz - one_xyz_value
            selectnonzeros = np.any(separation_values != 0, axis=1)
            separation_values = np.compress(selectnonzeros, separation_values, axis=0)


        # Increment reference localisation
        # in search of next localisation with near neighbours.
        xyz_index = xyz_index + 1


    # Continue appending to the array d
    # with vectors to the near-enough neighbours of other localisations.
    for xyz_index in range(xyz_index, len(xyz_values)):
        one_xyz_value = xyz_values[xyz_index]
        boolean_test_results = np.logical_and(xyz_values > one_xyz_value - xyz_filter_values,
                                              xyz_values < one_xyz_value + xyz_filter_values)
        test_results_indices = np.all(boolean_test_results, axis=1)
        subxyz = xyz_values[test_results_indices]
        if len(subxyz) != 1:
            subd = subxyz - one_xyz_value  #  Array of vectors to near-enough neighbours
            selectnonzeros = np.any(subd != 0, axis=1)
            subd = np.compress(selectnonzeros, subd, axis=0)
            separation_values = np.append(separation_values, subd, axis=0)

        # Progress message
        if True and xyz_index % 5000 == 0:
            print('Found neighbours for localisation', xyz_index, 'of', repr(len(xyz_values)) +'.')
            print('%i seconds so far.' % (time.time() - start_time))

    if True:
        print('Found %i vectors between all localisations' % len(separation_values))
        print('in %i seconds.' % (time.time() - start_time))

    if sort_and_halve is True:
        separation_values = separation_values[separation_values[:, 2].argsort()]

        separation_values = separation_values[separation_values[:, 1].argsort(kind='mergesort')]

        separation_values = separation_values[separation_values[:, 0].argsort(kind='mergesort')]

        #size, cols = separation_values.shape

        separation_values = np.array_split(separation_values, 2)

        return separation_values[1]

    else:
        return separation_values


def getdistances_two_colours(
    xyz_values_start, filterdist, xyz_values_end,
    verbose=False
    ):
    """Store all vectors (relative positions) between points within a chosen
    distance of each other in 3D from a list of points in one numpy array
    to another.
    Also works for 2D.

    Args:
        xyz_values_start (numpy array):
            Numpy array of localisations with one row per localisation and
            spatial coordinates in 2 or 3 columns,
            to calculate relative positions 'from'.
        filterdist (float):
            Distance (in all three dimensions) between points within
            which relative positions are calculated. This can be chosen by
            user input as the function runs, or by specifying when calling
            the function from a script.
        xyz_values_end (float):
            A second, optional set of points to calculate relative positions
            'to', from the xyz_values_start values.
            Defaults to None.
        verbose (Boolean):
            Choice whether to print updates to screen. Defaults to False.

    Returns:
        d (numpy array):
            A numpy array of vectors of neighbours within the filter distance
            for every localisation.
    """
    start_time = time.time()  # Start timing it.

    # If two set of points are in use:
    # REMOVE THIS AND PUT IN MAIN AS WILL SLOW DOWN FITTING LATER
    if xyz_values_end is not None:
        # Check they have the same dimensionality. Exit if not.
        if xyz_values_start.shape[1] != xyz_values_end.shape[1]:
            sys.exit(
                '\nYour start and end sets of posistions must have '
                'the same dimensionality.\n'
                'They currently have ' +repr(xyz_values_start.shape[1])+
                ' and ' +repr(xyz_values_end.shape[1])+ 'dimensions, '
                'respectively.\n')
        # Add 3rd column to 2D localisations
        if xyz_values_end.shape[1] == 2:
            xyz_values_end = np.column_stack((xyz_values_end, np.zeros(xyz_values_end.shape[0])))

    # Set up distance filter
    xyz_filter_values = np.array([filterdist, filterdist, filterdist])

    if True:
        print('\nFinding vectors to nearby localisations:\n')

    # Add 3rd column to 2D 'from' localisations
    if xyz_values_start.shape[1] == 2:
        xyz_values_start = np.column_stack((xyz_values_start, np.zeros(xyz_values_start.shape[0])))

    # Initialise d (array of relative positions)
    separation_values = []

    # Find relative positions of near neighbours in 'from' to the first point
    # in the 'from' set. Keep going through the list of points until at least
    # one near neighbour is found.
    xyz_index = 0

    # Find all the separtions in x, y (and z) from the first 'from'
    # localisation to the 'to' localisations.
    while len(separation_values) == 0:
        if xyz_index > len(xyz_values_start) -1:
            break

        one_xyz_value = xyz_values_start[xyz_index]  # Reference 'from' loc

        # A filter to find 'to' localisation coordinates within filterdist of
        # 'from' loc. Gives np.array of True / False
        boolean_test_results = np.logical_and(
            xyz_values_end > one_xyz_value - xyz_filter_values,
            xyz_values_end < one_xyz_value + xyz_filter_values
            )

        # Find indices of 'to' locs within filterdist of 'from'
        # loc in all three dimensions (all True) and select these.
        test_results_indices = np.all(boolean_test_results, axis=1)
        subxyz_end = xyz_values_end[test_results_indices]

        # Populate separation_values with any near neighbours.
        # len(subxyz) == 1 would mean the reference 'from' loc was
        # duplicated in the 'to' set and was the only locs within
        # filterdist of itself.
        # Remove [0,0,0], these are duplicates and can overwhelm the result
        # when there is not a second 'to' dataset.
        # Very unlikely that [0,0,0] occurs at all when there are different
        # from and two datasets.
        # Store the vectors from the reference 'from' loc to the filtered subset
        # of all 'from' locs.
        if len(subxyz_end) != 1:
            separation_values = subxyz_end - one_xyz_value
            selectnonzeros = np.any(separation_values != 0, axis=1)
            separation_values = np.compress(selectnonzeros, separation_values, axis=0)

        # Increment reference 'from' localisation
        # in search of next 'from' localisation with near neighbours.
        xyz_index = xyz_index + 1

    # Continue appending to the array separation_values
    # with vectors to the near-enough neighbours of other localisations.
    for xyz_index in range(xyz_index, len(xyz_values_start)):
        one_xyz_value = xyz_values_start[xyz_index]
        boolean_test_results = np.logical_and(
            xyz_values_end > one_xyz_value - xyz_filter_values,
            xyz_values_end < one_xyz_value + xyz_filter_values)
        test_results_indices = np.all(boolean_test_results, axis=1)
        subxyz_end = xyz_values_end[test_results_indices]
        if len(subxyz_end) != 1:
            subd = subxyz_end - one_xyz_value  #  Array of vectors to near-enough neighbours
            selectnonzeros = np.any(subd != 0, axis=1)
            subd = np.compress(selectnonzeros, subd, axis=0)
            separation_values = np.append(separation_values, subd, axis=0)

        # Progress message
        if True and xyz_index % 5000 == 0:
            print('Found neighbours for localisation', xyz_index, 'of',
                repr(len(xyz_values_start)) +'.')
            print('%i seconds so far.' % (time.time() - start_time))

    if True:
        print('Found %i vectors between all localisations' % len(separation_values))
        print('in %i seconds.' % (time.time() - start_time))

    return separation_values