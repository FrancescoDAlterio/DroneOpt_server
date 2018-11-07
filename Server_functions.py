from DataStructuresManagement import DataStructuresManagement
from queue import *
import Utilities


def store_value_from_client(id_str, data):
    dict_values = DataStructuresManagement.get_dict_values()

    try:
        dict_values[id_str]

    except KeyError:  # if there is no key id_string, create a new queue and the key-value pair <id_str,n_qu>
        n_qu = Queue(maxsize=10)
        dict_values[id_str] = n_qu

    window = dict_values[id_str]

    window.put_nowait(data)

    print("Client: ", id_str, " - window: ", list(window.queue))

    if window.full():
        l_window = list(window.queue)

        AVG = Utilities.mean(l_window)[
            1]  # per il momento skippo il check se è un numero o no, prendo direttament eil valore

        print("Client: ", id_str, " - AVG ", AVG)
        dict_values[id_str].queue.clear()

        DataStructuresManagement.set_dict_values(dict_values)

        return AVG

    dict_values[id_str] = window

    DataStructuresManagement.set_dict_values(dict_values)

    return -1


def cmp_avg_and_decide(id_str, AVG):
    # now I start from the simple case to compare the new AVG with the old one
    # avg_window is a variable, but it could be generalized to a queue

    dict_AVGs = DataStructuresManagement.get_dict_AVGs()
    do_movement = 5  # stand still

    try:
        dict_AVGs[id_str]

    except KeyError:
        dict_AVGs[id_str] = False

    avg_window = dict_AVGs[id_str]

    dict_AVGs[id_str] = AVG

    DataStructuresManagement.set_dict_AVGs(dict_AVGs)

    if not avg_window:
        do_movement = "left"  # move left

    elif avg_window < AVG:
        do_movement = "forward"  # move forward

    elif avg_window > AVG:
        do_movement = "right"  # move right

    elif avg_window == AVG and not avg_window == 10:
        do_movement = "backward"  # move backward

    return do_movement
