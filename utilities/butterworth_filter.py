from scipy.signal import butter, filtfilt


# filter the data to clean the spikes in derived data
def butterworth_filter(data, cutoff, frame_rate, order=4, filter_type='low'):
    nyq = 0.5 * frame_rate
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)

    # Adjust the padlen based on the length of the data
    padlen = min(order * 3, len(data) - 1)

    y = filtfilt(b, a, data, padlen=padlen)
    return y