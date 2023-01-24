# Import standard libraries
import sys

def choose_channels(info):
    """Choose 'from' and 'to' colour channels for between colour relative
    positions.

    Args:
        info (dict): A python dictionary containing a collection of useful parameters
            such as the filenames and paths.
            This dictionary is modified to contain information about the data read
            during the function.

    Returns:
        start_channel (float):
            The value of the colour channel for 'from' locs.
        end_channel (float):
            The value of the colour channel for 'to' locs.
            'None' if analysis is of a single specific channel.
    """
    # User input for the number of channels.
    if len(info['unique_colour_values']) == 1:
        start_channel = info['unique_colour_values'][0]
        end_channel = None
        print('Using the only colour channel: ' +repr(start_channel))
        return start_channel, end_channel

    # If > 1 channel - won't get this far if only 1.
    try:
        print('\nHow many colour channels would you like to use in the analysis?')
        colour_number = int(input('You can currently choose 1 or 2: ' ))
    except ValueError:
        sys.exit('\nThe number of colour channels to use must be an integer.\n')
    if colour_number == 0 or colour_number > 2:
        sys.exit('\nSorry, only 1 or 2.\n')
    else:
        print('\n'+str(colour_number)+' colour channels were selected.\n')
        info['colours_analysed'] = colour_number

    # Get the colour channel values.
    if info['colours_analysed'] == 1:
        start_channel = float(input('Which colour channel do you want to analyse? '))
        end_channel = None

    if info['colours_analysed'] == 2:
        start_channel = float(input('Which colour channel do you want to measure FROM? '))
        end_channel = float(input('Which colour channel do you want to measure TO? '))

    # Check the input values match channel values in the data
    # For 'from' channel
    valid_colour = False
    for colour in info['unique_colour_values']:
        if start_channel == colour:
            valid_colour = True
    if valid_colour is False:
        print(repr(start_channel)+ ' is not one of your colour channel values.')
        retry = input('Do you want to select a different colour channel value (yes/no)?')
        if retry.lower()[0] == 'y':
            # info['start_channel'] == 'Incorrect input' # Debug option
            start_channel, end_channel = choose_channels(info)
        else:
            sys.exit('Exiting.')

    # For 'to' channel
    if end_channel is not None:
        valid_colour = False
        for colour in info['unique_colour_values']:
            if end_channel == colour:
                valid_colour = True
        if valid_colour is False:
            print(repr(end_channel)+ ' is not one of your colour channel values.')
            retry = input('Do you want to select a different colour channel value (yes/no)?')
            if retry.lower()[0] == 'y':
                # info['end_channel'] == 'Incorrect input' # Debug option
                start_channel, end_channel = choose_channels(info)
            else:
                sys.exit('Exiting.')

    return start_channel, end_channel