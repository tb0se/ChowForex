# Standard library imports
import random
import sys


def generate_username(fname,lname):

    num = '{:03d}'.format(random.randrange(1, 999))
    return (fname+lname+num)
