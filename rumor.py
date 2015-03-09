#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# INFO-F106 : Projet d'année
# Carlos Requena López

"""rumor.py - main module of the network simulator"""

# --- Import libraries --- #

import argparse
import rumorFunctions as rF


# --- Main --- #


def main():
    """Simulates the propagation of a rumor in a social network, given a
    network file containing all names and friends and simulation
    options (variables).

    """

    # -- Defining parser object and arguments --- #
    parser = argparse.ArgumentParser()

    parser.add_argument("network_file", type=argparse.FileType('r'),
                        help="Network file. Friends and friendships")

    parser.add_argument("-s", "--starter", action="store", dest="rumor_starter",
                        type=str, default=None,
                        help="Name of the person starting the rumor")
    parser.add_argument("-r", "--rumor", action="store", dest="rumor",
                        type=rF.rumor_type, default=rF.randint(0, rF.RUMOR_MAX_VALUE),
                        help="Initial rumor value")
    parser.add_argument("-t", "--time", action="store", dest="stages_number",
                        type=int, default=False,
                        help="Number of times the simulation should run")
    parser.add_argument("-d", "--dont", action="store_true",
                        dest="dont_tell", default=False, help="People won't tell again if \
                        they already know. Defaults to False")
    parser.add_argument("-m", "--modif", action="store",
                        dest="modif_type", default="none",
                        choices=['incremental', 'bitflip', 'none'],
                        help="Rumor modification type. Will change the rumor accordingly \
                        (also watching probability)")
    parser.add_argument("-p", "--prob", action="store", dest="probability",
                        type=rF.probability, default=rF.MODIF_PROB,
                        help="Probability of the rumor being modified while transmission. \
                        Float in range 0 : 1")
    parser.add_argument("-u", "--update", action="store", dest="update_rule",
                        type=str, default="stable",
                        choices=['rewrite', 'mixture', 'stable'],
                        help="Rumor update rule. How will a rumor change someone's \
                        own version")

    args = parser.parse_args()

    
    # --- Expanding the information --- #
    modif_funcs = {"none": rF.none,
                   "incremental": rF.incremental,
                   "bitflip": rF.bitflip}

    update_funcs = {"stable": rF.stable,
                    "rewrite": rF.rewrite,
                    "mixture": rF.mixture}

    filename = args.network_file.name

    # load functions
    people = rF.load_people(filename)
    names, friends = rF.load_names_friends(filename)
    network = rF.load_network(people)

    if not args.rumor_starter:
        args.rumor_starter = people[rF.randint(0, len(people) - 1)]
    elif args.rumor_starter not in names:
        print("\nThe person starting the rumor is not in the network\n")
        exit()

    args.rumor_starter.rumor = args.rumor

    modif_function = modif_funcs[args.modif_type]
    update_function = update_funcs[args.update_rule]
    flags = (args.dont_tell,
             modif_function,
             args.probability,
             update_function)


    # --- Show intro messages --- #
    rF.print_network(names, friends)
    print("\nRumor starter:", args.rumor_starter.name)
    print("Initial rumor:", args.rumor)
    print("Initial State:")
    rF.print_state(names, people)

    
    # --- Start of the simulation --- #
    stage = 1
    total_rumor_spread = 0
    keep_propagating = True
    while keep_propagating:
        print("\nSimulation round", stage, ":")
        rumor_spread = rF.update(network, people, flags)
        total_rumor_spread += rumor_spread
        print("{number} {ppl} just learnt the rumor."\
              .format(number=rumor_spread,
                      ppl="person" if rumor_spread == 1 else "people"))
        rF.print_state(names, people)

        # Adjust condition
        if args.stages_number:  # Finite, determined number of rounds
            keep_propagating = stage < args.stages_number
        else:              # Keep going until everyone knows the rumor
            keep_propagating = total_rumor_spread != len(people) - 1
        stage += 1
    print("\n# --- End of simulation --- #\n")

if __name__ == "__main__":
    main()
