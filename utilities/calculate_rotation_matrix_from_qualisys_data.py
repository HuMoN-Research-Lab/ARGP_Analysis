from numpy import ndarray

from pupil_labs_stuff.rotation_matrix_calculator_qualisys import RotationMatrixCalculator


def calculate_rotation_matrix_from_qualisys_data(skelly_dict: dict) -> ndarray:

    print('About to calculate head rotation matrix, make sure you are importing the qualisys version!!!')

    rotation_matrix_calculator = RotationMatrixCalculator(skelly_dict=skelly_dict)

    return rotation_matrix_calculator.calculate_head_rotation_matricies(debug=False)
