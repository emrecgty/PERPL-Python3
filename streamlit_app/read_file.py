from io import StringIO

from streamlit.runtime.uploaded_file_manager import UploadedFile
import numpy as np

def read_file(file: UploadedFile, errors: list = []):
    if file.name.endswith('.npy'):
        try:
            return np.load(file.name)
        except (OSError, ValueError,):
            errors.append("Could not read file")

    elif file.name.endswith('.csv') or file.name.endswith('.txt'):
        try:
            skip = 0
            line = file.readline().decode('utf-8')
            for cell in line.split(','):
                try:
                    float(cell)
                except ValueError:
                    skip = 1
            return np.loadtxt(
                            StringIO(file.read().decode('utf-8')),
                            delimiter=',',
                            skiprows=skip
                            )
        except (EOFError, IOError, OSError) as exception:
            errors.append("Could not read file")
    else:
        errors.append('Sorry, wrong format!')