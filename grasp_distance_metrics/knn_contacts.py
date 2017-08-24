# coding: utf-8

__all__ = ['contact_distance']

import argparse
import numpy as np
from sklearn.neighbors import NearestNeighbors

import curvox.np_conversions


def contact_distance(c1_filename, c2_filename, verbose=False):

    c1 = curvox.np_conversions.pcd_to_np(c1_filename)
    c2 = curvox.np_conversions.pcd_to_np(c2_filename)

    nbrs = NearestNeighbors(n_neighbors=1).fit(c1)
    nbrs.kneighbors(c2)
    c2_distances, indices = nbrs.kneighbors(c2)

    nbrs = NearestNeighbors(n_neighbors=1).fit(c2)
    c1_distances, indices = nbrs.kneighbors(c1)

    c1_mean_distance = np.mean(c1_distances)
    c2_mean_distance = np.mean(c2_distances)
    total_distance = c1_mean_distance + c2_mean_distance

    if verbose:
        print "c1_filename: " + str(c1_filename)
        print "c2_filename: " + str(c2_filename)
        print "c1.shape: " + str(c1.shape)
        print "c2.shape: " + str(c2.shape)
        print "c1_mean_distance: " + str(c1_mean_distance)
        print "c2_mean_distance: " + str(c2_mean_distance)
        print "total_distance: " + str(total_distance)

    return total_distance


def main():
    parser = argparse.ArgumentParser(
        description=
        """This script takes as input, two pcd filepaths representing contact
        locations from the same grasp on two different objects.  The script
        does a bi-directional KNN lookup to find the closest contact from the
        other grasp  the sum of the mean distances is returned.  Smaller
        distances mean the contact locations from the two grasps are closer
        to each other in Cartesian Space""")

    parser.add_argument(
        'c1',
        type=str,
        help="first .pcd pointcloud file to be compared")

    parser.add_argument(
        'c2',
        type=str,
        help="second .pcd pointcloud file to be compared")

    parser.add_argument(
        '--verbose', help="run in verbose mode", action="store_true")

    args = parser.parse_args()

    print contact_distance(args.c1, args.c2, args.verbose)


if __name__ == "__main__":
    main()
