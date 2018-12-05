
def str_to_i(val):

    try:
        val_int=int(val)
    except ValueError:
        return False,0

    return True,val_int


def mean(numbers):

    try:
        AVG= float(sum(numbers)) / max(len(numbers), 1)
    except TypeError:
        return False,0

    return True,AVG


