import itertools
import json
import random
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import choice

ROUNDS = 100000


def show_histogram(data, title, bin_count=1000, cumulative=False, fig_num = None, alpha=1, label=None):    
    if fig_num is None:
        plt.figure()
    else:
        plt.figure(fig_num)
    n, bins, patches = plt.hist(data, histtype='stepfilled', bins=bin_count,cumulative=cumulative, density=True if cumulative else False, alpha=alpha, label=label)
    plt.title(title)
    plt.xlabel("Pulls")
    plt.ylabel("Probablity" if cumulative else "Frequency")
    if label:
        ax = plt.gcf().axes[0]
        legend = ax.legend(prop={'size': 10})

    return n, bins, label

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

    return pull_success_results


def pull_gears(wishing_well=True):
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
    
    for idx, x in enumerate(range(ROUNDS)):
        item_counts = dict.fromkeys(items, 0)
        pull_count = 0
        pity_count = 0
        item_got = ""
        items_got = []
        wishing_well_msg = ""
        last_round_logs = []
        while len(items_got) < len(items_wanted):
            last_round_logs.append(f"=====ROUND {str(idx+1).ljust(len(str(ROUNDS)))}; PULL {str(pull_count).ljust(3)}; PITY {str(pity_count).ljust(3)}; START!!!======= {item_counts}")            
            if pull_count > 200:
                with open("log.txt", "w") as f:
                    f.write('\n'.join(last_round_logs))
                    print("stig pull exceeded 200. exiting")
                    exit()

            item_got = choice(items, p=probabilities)
            if pity_count == 49: # it just has to be this way, trust me
                rand = random.choice([x for x in items_wanted if x not in items_got])
                items_got.append(rand)
                item_counts[rand] += 1
                pity_count = 0
            elif item_got in items_wanted:  # it's one of the items you want
                if item_got not in items_got:  # you don't have it yet
                    items_got.append(item_got)
                    pity_count = 0
                else:                  # you alr have it
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
            last_round_logs.append(f"=====ROUND {str(idx+1).ljust(len(str(ROUNDS)))}; PULL {str(pull_count).ljust(3)}; PITY {str(pity_count).ljust(3)}; END!!!======= {item_counts}")

        item_counts = dict(
            itertools.islice(item_counts.items(), 0, 4)
        )  # removes the "not" key
        print(item_counts, f"{str(pull_count).ljust(3)} pulls", wishing_well_msg)
        # print(f"Got all gear {items_got} in {pull_count} pulls", end='\r')
        pull_success_results.append(pull_count)

    return pull_success_results

save_file = Path("pull_data.json")

if save_file.exists():
    with Path("pull_data.json").open() as f:        
        dic = json.load(f)
        valk_res = dic['valks']
        gear_res = dic['gears']
        no_well_gear_res = dic['no_well_gears']
else:

    valk_res = pull_valk()
    gear_res = pull_gears(wishing_well=True)
    
    no_well_gear_res = pull_gears(wishing_well=False)

    with Path("pull_data.json").open("w") as f:
        dic = {"valks":valk_res, "gears":gear_res, "no_well_gears":no_well_gear_res}        
        json.dump(dic,f)

combined_res = [x+y for x, y in zip(valk_res, gear_res)]
no_well_combined_res = [x+y for x, y in zip(valk_res, no_well_gear_res)]

valk_xtals = statistics.mean(valk_res) * 280
gear_xtals = statistics.mean(gear_res) * 280

def calc_mean_median_mode(data):
    mean = statistics.mean(data)
    print(f"Mean: {mean:.2f} ({(mean*280):.2f} xtals)")

    median = statistics.median(data)
    print(f"Median: {median:.2f} ({(median*280):.2f} xtals)")

    mode = statistics.multimode(data)
    print(f"Mode: {', '.join(str(x) for x in mode)} ({', '.join([str(x*280) for x in mode])} xtals)")

    print(f"Min: {min(data):.2f} Max: {max(data):.2f}")

print(f"Average pulls to get valk: {statistics.mean(valk_res)} ({valk_xtals} crystals)")
print(f"Average pulls to get all gear: {statistics.mean(gear_res)} ({gear_xtals} crystals)")
print(f"Total crystals to 4/4 on average: {valk_xtals + gear_xtals}")
print("\n")
print("Valk statistics:")
calc_mean_median_mode(valk_res)

print("\nGear statistics:")
print("With wishing well:")
calc_mean_median_mode(gear_res)
print("Without wishing well:")
calc_mean_median_mode(no_well_gear_res)

print("\nCombined statistics")
print("With wishing well:")
calc_mean_median_mode(combined_res)
print("Without wishing well:")
calc_mean_median_mode(no_well_combined_res)

show_histogram(valk_res, "Valk pull successes", 10)
show_histogram(gear_res, "Gear pull successes w/ wishing well")








class Xcalculator:
    def __init__(self, values, bins, labels=None):
        self.values = values
        self.bins = bins
        self.labels = labels
        self.dic = {x: [] for x in self.labels}
    def calculate_x_value(self, y_value):
        # cumulative_sum = np.cumsum(self.values) #no need cuz alr cumsum'd
        # cumulative_sum /= cumulative_sum[-1]         
        #if len(self.values) > 1:
        if isinstance(self.values, np.ndarray) and all(isinstance(x, np.ndarray) for x in self.values):
            #dic = self.dic
            for idx, x in enumerate(self.values):
                index = np.where(x >= y_value)[0][0]
                x_value = self.bins[index]
                label = self.labels[idx]                
                self.dic[label].append(f"{x_value:.2f} pulls has a {y_value*100}% chance")                
            #self.dic = dic
        else:
            index = np.where(self.values >= y_value)[0][0]
            x_value = self.bins[index]
            self.dic[self.labels[0]].append(f"{x_value:.2f} pulls has a {y_value*100}% chance")                            
    def show_all(self):    
        for key, values in self.dic.items():
            print(key)
            for value in values:    
                print(f"- {value}")

values, bins, labels = show_histogram(valk_res, "Valk pull successes (cumulative)", cumulative=True)
print("VALK ONLY:")
xcal = Xcalculator(values, bins, ["Valk pulls"])
xcal.calculate_x_value(0.25)
xcal.calculate_x_value(0.5)
xcal.calculate_x_value(0.75)
xcal.calculate_x_value(0.90)
xcal.calculate_x_value(0.95)
xcal.show_all()

values, bins, labels = show_histogram([gear_res, no_well_gear_res], "Gear pull successes (cumulative)", cumulative=True, alpha=0.5, label=["w/ wishing well", "w/o wishing well"])
print("GEARS ONLY:")
xcal = Xcalculator(values, bins, labels)
xcal.calculate_x_value(0.25)
xcal.calculate_x_value(0.5)
xcal.calculate_x_value(0.75)
xcal.calculate_x_value(0.90)
xcal.calculate_x_value(0.95)
xcal.show_all()

values, bins, labels = show_histogram([combined_res, no_well_combined_res], "Combined pull successes (cumulative)", cumulative=True, alpha=0.5, label=["w/ wishing well", "w/o wishing well"])
print("COMBINED:")
xcal = Xcalculator(values, bins, labels)
xcal.calculate_x_value(0.25)
xcal.calculate_x_value(0.5)
xcal.calculate_x_value(0.75)
xcal.calculate_x_value(0.90)
xcal.calculate_x_value(0.95)
xcal.show_all()

plt.show()
