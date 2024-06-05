import numpy as np
import math
def gen_base_traj(pointsList, x, y):
    std = 0.1
    if (not pointsList[0]) and (x >= -0.08) :
        x_values = np.random.normal(-0.1, std, 1)
        y_values = np.random.normal( 0.0, std, 1)
        if x_values >= 0: x_values = -0.01
        return x_values, y_values, pointsList
    elif (not pointsList[1]) and (y >=-0.04):
        pointsList[0] = True
        x_values = np.random.normal( 0.0, std, 1)
        y_values = np.random.normal(-0.1, std, 1)
        if y_values >= 0: y_values = -0.01
        return x_values, y_values, pointsList
    elif (not pointsList[2]) and (x <=0.08):
        pointsList[1] = True
        x_values = np.random.normal(0.1, std, 1)
        y_values = np.random.normal(0.0, std, 1)
        if x_values <= 0: x_values = 0.01
        return x_values, y_values, pointsList
    elif (not pointsList[3]) and  (y >=-0.08):
        pointsList[2] = True
        x_values = np.random.normal( 0.0, std, 1)
        y_values = np.random.normal(-0.1, std, 1)
        if y_values >= 0: y_values = -0.01
        return x_values, y_values, pointsList
    elif (not pointsList[4]) and (x >=-0.08):
        pointsList[3] = True
        x_values = np.random.normal(-0.1, std, 1)
        y_values = np.random.normal( 0.0, std, 1)
        if x_values >= 0: x_values = -0.01
        return x_values, y_values, pointsList
    else:
        pointsList[4] = True
        x_values = 0
        y_values = 0
        return x_values, y_values, pointsList
    
def distance_error(pointsList, xb, yb, xt, yt):
    if (not pointsList[0]) and (xb >= -0.08) :
        error_b = math.sqrt((yb-0)**2)
        error_t = math.sqrt((yt-0)**2)
        return error_b, error_t
    elif (not pointsList[1]) and (yb >=-0.04):
        error_b = math.sqrt((xb+0.08)**2)
        error_t = math.sqrt((xt+0.08)**2)
        return error_b, error_t
    elif (not pointsList[2]) and (xb <=0.08):
        error_b = math.sqrt((yb+0.04)**2)
        error_t = math.sqrt((yt+0.04)**2)
        return error_b, error_t
    elif (not pointsList[3]) and  (yb >=-0.08):
        error_b = math.sqrt((xb-0.08)**2)
        error_t = math.sqrt((xt-0.08)**2)
        return error_b, error_t
    elif (not pointsList[4]) and (xb >=-0.08):
        error_b = math.sqrt((yb+0.08)**2)
        error_t = math.sqrt((yt+0.08)**2)
        return error_b, error_t
    else:
        error_b = 0
        error_t = 0
        return error_b, error_t