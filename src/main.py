import itertools
import random

import matplotlib.pyplot as plt
from numpy.random import choice

ROUNDS = 1000


def show_histogram(data, title):
    plt.figure()
    plt.hist(data)
    plt.title(title)
    plt.xlabel("Pulls")
    plt.ylabel("Frequency")


def pull_valk(amount_wanted=1):
    item_wanted = "valk"
    items = [item_wanted, "not"]
    probabilities = [0.015, 1 - 0.015]

    pull_success_results = []

    for x in range(ROUNDS):
        pull_count = 0
        item_got = ""
        amount_got = 0
        pity_100 = 0
        while amount_got < amount_wanted:
            item_got = choice(items, p=probabilities)
            pity_100 += 1
            pull_count += 1
            if pity_100 == 100:
                amount_got += 1
                pity_100 = 0
            elif item_got == item_wanted:
                amount_got += 1

        print(f"Got {item_wanted} {amount_wanted}x in {str(pull_count).ljust(3)} pulls")

        pull_success_results.append(pull_count)

    valk_avg = sum(pull_success_results) / ROUNDS
    return pull_success_results, valk_avg


def pull_gears():
    def find_num_missing_stigs(stigs_dict):
        count = 0
        for x in stigs_dict.values():
            if x == 0:
                count += 1
        return count

    def get_owned_stigs_count(stigs_dict):
        count = 0
        for x in stigs_dict.values():
            count += x
        return count

    items = ["wep", "stig1", "stig2", "stig3", "not"]

    items_wanted = items[:-1]

    probabilities = [0.02479, 0.01240, 0.01240, 0.01240, 0.93801]

    pull_success_results = []

    for x in range(ROUNDS):
        item_counts = dict.fromkeys(items, 0)
        pull_count = 0
        pity_count = 0
        item_got = ""
        items_got = []
        wishing_well_msg = ""
        while len(items_got) < len(items_wanted):
            item_got = choice(items, p=probabilities)
            if pity_count == 50:
                rand = random.choice([x for x in items_wanted if x not in items_got])
                items_got.append(rand)
                item_counts[rand] += 1
                pity_count = 0
            elif item_got in items_wanted:  # it's the item you want
                if item_got not in items_got:  # you don't have it yet
                    items_got.append(item_got)
                    pity_count = 0
                item_counts[item_got] += 1
            else:
                pity_count += 1
            pull_count += 1

            just_stigs = dict(itertools.islice(item_counts.items(), 1, 4))
            if (
                item_counts["wep"] > 0
                and find_num_missing_stigs(just_stigs) == 1
                and get_owned_stigs_count(just_stigs) >= 4
            ):
                wishing_well_msg = "(Wishing well-able)"
                break

        item_counts = dict(
            itertools.islice(item_counts.items(), 0, 4)
        )  # removes the "not" key
        print(item_counts, f"{str(pull_count).ljust(3)} pulls", wishing_well_msg)
        # print(f"Got all gear {items_got} in {pull_count} pulls", end='\r')
        pull_success_results.append(pull_count)

    gear_avg = sum(pull_success_results) / ROUNDS

    return pull_success_results, gear_avg


valk_res, valk_avg = pull_valk()
gear_res, gear_avg = pull_gears()

valk_xtals = valk_avg * 280
gear_xtals = gear_avg * 280

print(f"Average pulls to get valk: {valk_avg} ({valk_xtals} crystals)")
print(f"Average pulls to get all gear: {gear_avg} ({gear_xtals} crystals)")
print(f"Total crystals to 4/4 on average: {valk_xtals + gear_xtals}")
show_histogram(valk_res, "Valk pull successes")
show_histogram(gear_res, "Stig pull successes")
plt.show()
