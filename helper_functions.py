from bisect import bisect_left
import numpy as np


# Returns whether element is in sorted array
def binary_in(array, value):
    i = bisect_left(array, value)
    if i != len(array) and array[i] == value:
        return True
    else:
        return False


# Return distance between two vectors in the form of map. Returns squared value to save on unnecessary computations.
# It takes average to avoid problems with more tags being disadvantaged
def euclidian_distance_squared_per_component(rating, tags):
    # 2 is maximal possible rating person could rate a problem,
    # so if the person totally liked the problem, distance would be zero
    # distance between components squared
    rating_tags = np.array([
        ((rating.get(tag, [0, 0])[0] / rating.get(tag, [0, 1])[1]) ** 2 - 4) ** 2 for tag in tags if tag in rating
    ])
    try:
        distance_squared = np.sum(rating_tags) / len(tags)
    except ZeroDivisionError:
        return float("inf")
    return distance_squared


def k_smallest_elements(data, k):
    data_array = np.array(data)
    # Get the indices that would partition the array into k smallest elements
    partition_indices = np.argpartition(data_array[:, 1], k)[:k]
    # Get the k smallest elements using the partition indices
    k_smallest_elements = data_array[partition_indices]
    # Sort the k smallest elements based on the values
    sorted_indices = np.argsort(k_smallest_elements[:, 1])  # Sort in ascending order
    return k_smallest_elements[sorted_indices]
