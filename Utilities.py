
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




def store_value_from_client(cls, id_str, data):

    try:
        cls.__dict_values[id_str]
    except KeyError:            #if there is no key id_string, create a new queue and the key-value pair <id_str,n_qu>
        n_qu = Queue(maxsize=10)
        cls.__dict_values[id_str] = n_qu

    window = cls.__dict_values[id_str]

    window.put_nowait(data)

    print("Client: ",id_str," - window: ",list(window.queue))


    if window.full():

        l_window = list(window.queue)

        AVG = Utilities.mean(l_window)[1] #per il momento skippo il check se è un numero o no, prendo direttament eil valore

        print("Client: ", id_str, " - AVG ",AVG)
        cls.__dict_values[id_str].queue.clear()

        return AVG

    cls.__dict_values[id_str] = window

    return -1