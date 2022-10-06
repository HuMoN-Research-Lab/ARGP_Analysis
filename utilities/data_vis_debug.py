from numpy import ndarray

from utilities.skelly_plotter import skelly_plotter


def data_vis_debug(generic_skelly_dict: dict,
                   select_frame: ndarray):

    skelly_plotter(generic_skelly_dict, select_frame)  # update backend to plot figures in a floating window