from step_finder_stuff.debug_plot_heel_strikes import debug_plot_heel_strikes


# find frames where heel strikes occur
def find_heel_strikes(velocity_data, position_data, acceleration_data, velocity_threshold, position_threshold,
                      acceleration_threshold):
    heel_strike_indices = []
    data_length = len(velocity_data)

    for i in range(1, data_length - 1):  # Adjust the range to avoid index errors
        # Check for local minima below the threshold
        if (velocity_data[i] < velocity_threshold and
                velocity_data[i] < velocity_data[i - 1] and
                velocity_data[i] < velocity_data[i + 1]):
            # Look in the next 75 frames
            for j in range(i + 1, min(i + 76, data_length)):
                if position_data[j] < position_threshold and acceleration_data[j] > acceleration_threshold:
                    heel_strike_indices.append(j)
                    break  # Exit inner loop once the heel strike is found

    return heel_strike_indices


if __name__ == "__main__":
    print("henolso?!")

    debug_plot_heel_strikes()
