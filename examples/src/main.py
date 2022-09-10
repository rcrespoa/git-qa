import sys
import os


# compute the sum of the first n natural numbers function
def sum_n(n):
    if n == 0:
        return 0
    else:
        return n + sum_n(n - 1)
