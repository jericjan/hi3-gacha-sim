import itertools
import logging
import random

from numpy.random import choice
from tqdm import tqdm

BAR_FORMAT = '{desc}: {percentage:3.0f}% [{elapsed}<{remaining}]'


def pull_valk(rounds, amount_wanted=1, pity=100):
    logging.info("Pulling valks")
    item_wanted = "valk"
    items = [item_wanted, "not"]
    probabilities = [0.015, 1 - 0.015]

    pull_success_results = []

    for x in tqdm(range(rounds), desc="Valkyrie", mininterval=5, position=0,
                  bar_format=BAR_FORMAT):
        pull_count = 0
        item_got = ""
        amount_got = 0
        pity_100 = 0
        while amount_got < amount_wanted:
            item_got = choice(items, p=probabilities)
            pity_100 += 1
            pull_count += 1
            if pity_100 == pity:
                amount_got += 1
                pity_100 = 0
            elif item_got == item_wanted:
                amount_got += 1

        logging.debug(
            f"Got {item_wanted} {amount_wanted}x in {str(pull_count).ljust(3)} pulls"
        )

        pull_success_results.append(pull_count)
    # logging.info("Pulling valks finished.")
    return pull_success_results


def pull_gears(rounds, wishing_well=True, gear_pity=50):
    if wishing_well:
        logging.info("Pulling gears w/ wishing well")
    else:
        logging.info("Pulling gears w/o wishing well")

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

    gear_pity = gear_pity - 1  # it just has to be this way, trust me

    items = ["wep", "stig1", "stig2", "stig3", "not"]

    items_wanted = items[:-1]

    probabilities = [0.02479, 0.01240, 0.01240, 0.01240, 0.93801]

    pull_success_results = []

    for idx, x in tqdm(
        enumerate(range(rounds)),
        desc=f"Gear (Well: {wishing_well})",
        mininterval=5,
        position=1 if wishing_well else 2,
        bar_format=BAR_FORMAT,
        total=rounds
    ):
        item_counts = dict.fromkeys(items, 0)
        pull_count = 0
        pity_count = 0
        item_got = ""
        items_got = []
        wishing_well_msg = ""
        last_round_logs = []
        while len(items_got) < len(items_wanted):
            last_round_logs.append(
                f"=====ROUND {str(idx+1).ljust(len(str(rounds)))}; "
                f"PULL {str(pull_count).ljust(3)}; PITY {str(pity_count).ljust(3)}; "
                f"START!!!======= {item_counts}"
            )
            if pull_count > 200:
                with open("log.txt", "w") as f:
                    f.write("\n".join(last_round_logs))
                    print("stig pull exceeded 200. exiting")
                    exit()

            item_got = choice(items, p=probabilities)
            if pity_count == gear_pity:
                rand = random.choice([x for x in items_wanted if x not in items_got])
                items_got.append(rand)
                item_counts[rand] += 1
                pity_count = 0
            elif item_got in items_wanted:  # it's one of the items you want
                if item_got not in items_got:  # you don't have it yet
                    items_got.append(item_got)
                    pity_count = 0
                else:  # you alr have it
                    pity_count += 1
                item_counts[item_got] += 1
            else:
                pity_count += 1
            pull_count += 1

            if wishing_well:
                just_stigs = dict(itertools.islice(item_counts.items(), 1, 4))
                if (
                    item_counts["wep"] > 0
                    and find_num_missing_stigs(just_stigs) == 1
                    and get_owned_stigs_count(just_stigs) >= 4
                ):
                    wishing_well_msg = "(Wishing well-able)"
                    break
            last_round_logs.append(
                f"=====ROUND {str(idx+1).ljust(len(str(rounds)))}; "
                f"PULL {str(pull_count).ljust(3)}; PITY {str(pity_count).ljust(3)}; "
                f"END!!!======= {item_counts}"
            )

        item_counts = dict(
            itertools.islice(item_counts.items(), 0, 4)
        )  # removes the "not" key
        logging.debug(
            item_counts, f"{str(pull_count).ljust(3)} pulls", wishing_well_msg
        )
        # print(f"Got all gear {items_got} in {pull_count} pulls", end='\r')
        pull_success_results.append(pull_count)

    # if wishing_well:
    #     logging.info("Pulling gears w/ wishing well finished.")
    # else:
    #     logging.info("Pulling gears w/o wishing well finished.")
    return pull_success_results
