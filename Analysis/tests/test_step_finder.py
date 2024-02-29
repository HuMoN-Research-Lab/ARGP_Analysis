# test_step_finder.py
import numpy as np
import pytest

from step_finder_stuff.step_finder import find_heel_strikes


def test_find_heel_strikes():
    # Generate a sine wave for velocity data
    time = np.linspace(0, 2 * np.pi, 100)  # Generate 100 time points
    velocity_data = np.sin(time)

    # Calculate position and acceleration from velocity
    # For simplicity, we'll assume position is the integral of velocity and acceleration is the derivative
    position_data = -np.cos(time)  # Integral of sine is -cosine
    acceleration_data = -np.sin(time)  # Derivative of sine is -sine

    # Define our thresholds
    velocity_threshold = -0.5  # Looking for local minima in negative sine wave
    position_threshold = 0.1  # Arbitrary threshold for position
    acceleration_threshold = 0.5  # Arbitrary threshold for acceleration

    # Call the function with the generated data
    result = find_heel_strikes(velocity_data, position_data, acceleration_data, velocity_threshold, position_threshold,
                               acceleration_threshold)

    # Expected result is the indices of local minima in the velocity data that meet the threshold criteria
    # For a full sine wave, this would be at pi (180 degrees), which corresponds to index 50 in our generated data
    expected_result = [50]

    # Assert that the result from the function matches our expected result
    assert result == expected_result, "The find_heel_strikes function did not return the expected heel strike indices."
