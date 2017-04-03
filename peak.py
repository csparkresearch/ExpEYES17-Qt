# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
"""Peak detection algorithms."""

import numpy as np
from scipy import optimize
from scipy.integrate import simps

eps = np.finfo(float).eps

def indexes(y, thres=0.3, min_dist=1):
    """Peak detection routine.

    Finds the peaks in *y* by taking its first order difference. By using
    *thres* and *min_dist* parameters, it is possible to reduce the number of
    detected peaks. *y* must be signed.

    Parameters
    ----------
    y : ndarray (signed)
        1D amplitude data to search for peaks.
    thres : float between [0., 1.]
        Normalized threshold. Only the peaks with amplitude higher than the
        threshold will be detected.
    min_dist : int
        Minimum distance between each detected peak. The peak with the highest
        amplitude is preferred to satisfy this constraint.

    Returns
    -------
    ndarray
        Array containing the indexes of the peaks that were detected
    """
    if isinstance(y, np.ndarray) and np.issubdtype(y.dtype, np.unsignedinteger):
        raise ValueError("y must be signed")

    thres = thres * (np.max(y) - np.min(y)) + np.min(y)
    min_dist = int(min_dist)

    # compute first order difference
    dy = np.diff(y)

    # propagate left and right values successively to fill all plateau pixels (0-value)
    zeros,=np.where(dy == 0)
    
    while len(zeros):
        # add pixels 2 by 2 to propagate left and right value onto the zero-value pixel
        zerosr = np.hstack([dy[1:], 0.])
        zerosl = np.hstack([0., dy[:-1]])

        # replace 0 with right value if non zero
        dy[zeros]=zerosr[zeros]
        zeros,=np.where(dy == 0)

        # replace 0 with left value if non zero
        dy[zeros]=zerosl[zeros]
        zeros,=np.where(dy == 0)

    # find the peaks by using the first order difference
    peaks = np.where((np.hstack([dy, 0.]) < 0.)
                     & (np.hstack([0., dy]) > 0.)
                     & (y > thres))[0]

    if peaks.size > 1 and min_dist > 1:
        highest = peaks[np.argsort(y[peaks])][::-1]
        rem = np.ones(y.size, dtype=bool)
        rem[peaks] = False

        for peak in highest:
            if not rem[peak]:
                sl = slice(max(0, peak - min_dist), peak + min_dist + 1)
                rem[sl] = True
                rem[peak] = False

        peaks = np.arange(y.size)[~rem]

    return peaks



def gaussian_fit(x, y, center_only=True):
    """Performs a Gaussian fitting of the specified data.

    Parameters
    ----------
    x : ndarray
        Data on the x axis.
    y : ndarray
        Data on the y axis.
    center_only: bool
        If True, returns only the center of the Gaussian for `interpolate` compatibility

    Returns
    -------
    ndarray or float
        If center_only is `False`, returns the parameters of the Gaussian that fits the specified data
        If center_only is `True`, returns the center position of the Gaussian
    """
    initial = [np.max(y), x[0], (x[1] - x[0]) * 5]
    params, pcov = optimize.curve_fit(gaussian, x, y, initial)

    if center_only:
        return params[1]
    else:
        return params


