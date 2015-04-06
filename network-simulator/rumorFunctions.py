#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module embodies all the necessary side functions and some
libraries that the main module 'rumor' is using

"""


# --- Import libraries --- #
import pickle
from random import random
from random import choice
from random import randint
from copy import deepcopy
from Person import Person
from Link import Link

# --- Constants --- #

RUMOR_LENGTH_BIN = 24           # RGB value on 3 bytes
RUMOR_MAX_VALUE = (1 << RUMOR_LENGTH_BIN) - 1

NO_FRIENDS = -1

MODIF_PROB = 0.1                # Default rumour modification
                                # probability

MIX_PROB = 0.9                  # Probability of keeping own rumour
                                # bit when mixture

# --- Extending types --- #


def probability(str_value):
    """checks if probability is a valid float value, raises exception
    otherwise

    """
    value = float(str_value)
    if not 0 <= value <= 1:
        raise TypeError("Invalid probability value")
    return value


def rumor_type(str_value):
    value = int(str_value)
    if not 0 <= value <= RUMOR_MAX_VALUE:
        raise TypeError("Invalid rumor value")
    return value

# --- Load functions --- #


def save_file(data_to_save):
    """Saves the current network state (two attributes) in a pickled
    format, in the specified file

    """
    filename = data_to_save["network_file"]
    archivo = open(filename, "wb")          # Open file in binary
    pickle.dump(data_to_save["people"], archivo, 2)           # protocol 2
    archivo.close()


def load_pickled_file(filename):
    """Loads the saved network by decoding the file given and returning
    the data to the simu_data class attribute of GUI

    """
    archivo = open(filename, "rb")
    data_to_load = pickle.load(archivo)
    archivo.close()
    return data_to_load


def load_network(people):
    """Computes and updates the friendship network. Returns network of
    Links.

    """

    network = [[False for person in people] for person in people]
    for i in range(len(people)):
        print("Hi, my name is", people[i].name, "and my friends are",
              people[i].friends)
        for friend in people[i].friends:
            j = 0
            index_of_friend = NO_FRIENDS
            while j < len(people):
                if people[j].name == friend:
                    index_of_friend = j
                j += 1
            if index_of_friend != NO_FRIENDS:
                set_as_friends(network, people, i, index_of_friend)
    return network


def load_people(network_file):
    """Creates all the Person instances and appends them to the people
    list

    """
    names, friends = load_names_friends(network_file)
    people = []
    for i in range(len(names)):
        people.append(Person(names[i], friends[i]))
    return people


def load_names_friends(friends_file):
    """Loads the list of names of the people in the network"""

    facebook = open(friends_file, "r")
    # comp list: it cleans the file from whitespaces and takes
    # whatever remains at the left of ":"
    names = [line.split(":")[0].strip() for line in facebook]
    facebook.seek(0)
    friends = [line.split(":")[1].split(",") for line in facebook]
    friends = [list(map(lambda friend: friend.strip(), lineFriends))
               for lineFriends in friends]
    facebook.close()

    return names, friends


def are_friends(network, idx0, idx1): # Esta funcion es una mierda.
    """
    """
    res = False
    if idx0 > idx1:
        res = network[idx0][idx1]
    elif idx0 < idx1:
        res = network[idx1][idx0]
    return res


def set_as_friends(network, people, idx0, idx1):
    """This funciton sets persons with ids id0 and id1 as friends in the
    social network.  It is impossible to set a person as a friend with
    himself/herself.

    """
    if idx0 > idx1:
        network[idx0][idx1] = Link(people[idx0], people[idx1])

###DEBUG
def print_matrix(matrix):
    new_matrix = [["T" if elem else "F" for elem in row] for row in matrix]
    for elem in new_matrix:
        print(elem)

###


def get_random_friend_id(index, network, people, dont_tell):
    """Gets the index of a random, possible, friend"""
    friends = []
    for i in range(len(network)):
        if are_friends(network, index, i):
            if people[i].rumor is None or not dont_tell:
                friends.append(i)
    if friends:
        chosen_one = choice(friends)
    else:
        chosen_one = NO_FRIENDS
    return chosen_one


# --- Printing functions --- #


def print_network(names, friends):
    """Prints the network as it was loaded from the file"""

    print("\nNetwork loaded: ")
    for i in range(len(names)):
        print(names[i], ": ", end="")
        print(", ".join(friends[i]))


def print_state(names, people):
    """For each person in the network, prints the rumor he/she knows, or
    whether they know it at all (-- Does not know --).

    """

    longest_name = len(max(names, key=len))
    fool = "-- Does not know --"
    # --- Printing --- #
    print("{:{width}}\t{:>24} {:>6}".format("NAME", "BIN", "HEX",
                                            width=longest_name))
    for i in range(len(names)):
        print("{:{width}}".format(names[i], width=longest_name), end="")
        if people[i].rumor is not None:
            print("\t{0:>024b} {0:>06X}".format(people[i].rumor))
        else:
            print("\t{}".format(fool))


# --- Rumor processing while transmission --- #

def will_modify(probability):
    """Determines if the rumor is going to be modified. Generates a
    random float in the [0:1] range and checks if probability is
    bigger or not.

    """
    res = False
    if random() < probability:
        res = True
    return res


def predict_rumor(rumor, modif_function, probability):
    """Determines if the rumor is to be modified"""
    if will_modify(probability):
        rumor = modif_function(rumor)
    return rumor


def none(rumor):
    """Returns the rumor without modification"""
    return rumor


def incremental(rumor):
    """Increments or decrements rumor by 1, both being equally likely to
    occur.

    """
    if random() > 0.5:
        rumor += 1
    else:
        rumor -= 1
    return rumor % (RUMOR_MAX_VALUE + 1)


def bitflip(rumor):
    """Performs a bitwise XOR with rumor and a power of 2 (up to
    2**23). This leaves the matching bits with 0 untouched and the bit
    matching with 1 flipped

    """
    return rumor ^ (2**randint(0, RUMOR_LENGTH_BIN - 1))


# --- Different reactions may occur / update functions --- #

def stable(new_people, chosen_one, rumor):
    """Stable update rule, person receiving the rumor does not change
    his/her version

    """
    if not new_people[chosen_one].rumor:
        new_people[chosen_one].rumor = rumor


def rewrite(new_people, chosen_one, rumor):
    """Rewrite update rule, person receiving the rumor will forget his/her
    own version and will change it for the new one that is being told

    """

    new_people[chosen_one].rumor = rumor


def mixture(new_people, chosen_one, rumor):
    """The new rumor is a mixture of the person own rumor and the one
    being told

    """

    try:
        own_rumor = list("{:024b}".format(new_people[chosen_one].rumor))
    except (TypeError, ValueError):
        pass
    else:
        rumor = list("{:024b}".format(rumor))
        for i in range(len(rumor) - 1):
            if own_rumor[i] != rumor[i]:
                if random() > 0.1:
                    rumor[i] = own_rumor[i]
        rumor = int("".join(rumor), 2)

    new_people[chosen_one].rumor = rumor


# --- Transmission stage, choosing friends and telling the rumor --- #

def update(network, people, flags):
    """
    Updates the network by determining who are the candidates to be
    told and then telling them a certain rumor (might be a modified
    version of his/her friend or not).

    Two or more people may choose the same friend.

    Flags:
    [0] --> Dont tell again / dont_tell
    [1] --> Modification rule / modif_function
    [2] --> Probability / probability
    [3] --> Update rule / update_function

    Returns rumor_spread; the number of people that learnt the rumor
    during that unit of time.

    """

    dont_tell, modif_function, probability, update_function = flags
    rumor_spread = 0
    # deepcopy needed to copy class attributes
    new_people = deepcopy(people)
    for i in range(len(people)):
        if people[i].rumor is not None:
            chosen_one = get_random_friend_id(i, network, new_people, dont_tell)
            if chosen_one != NO_FRIENDS:
                new_rumor = predict_rumor(new_people[i].rumor, modif_function, probability)
                if new_people[chosen_one].rumor is None:
                    rumor_spread += 1
                update_function(new_people, chosen_one, new_rumor)

    people[:] = new_people
    return rumor_spread
