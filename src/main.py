from numpy.random import choice
import random
import matplotlib.pyplot as plt

LINE_CLEAR = '\x1b[2K'   
rounds = 10000
def pull_valk(amount_wanted=1):    
    global rounds
    item_wanted = "valk"
    items = [item_wanted,"not"]
    probabilities = [0.015, 1-0.015]

    pull_success_results = []

    for x in range(rounds):
        pull_count = 0
        item_got = ""
        amount_got = 0
        while amount_got < amount_wanted:
            item_got = choice(items,p=probabilities)
            if item_got == item_wanted:
                amount_got += 1
            pull_count += 1
        pull_count = pull_count if pull_count < 100 else 100
        print(f"Got {item_wanted} {amount_wanted}x in {pull_count} pulls", end='\r') 
        print(end=LINE_CLEAR)    
        
        pull_success_results.append(pull_count)

    print(f"Average pulls to get {item_wanted}: {sum(pull_success_results) / rounds}") 
    plt.hist(pull_success_results)
    plt.title("Valk pull successes")
    plt.xlabel("Pulls")
    plt.ylabel("Frequency")
    plt.show()

def pull_gears(): 
    global rounds
    items = ["wep","stig1","stig2","stig3","not"]
    items_wanted = items[:-1]
    probabilities = [.02479, .01240, .01240, .01240, 0.93801]
    
    pull_success_results = []

    for x in range(rounds):
        pull_count = 0
        pity_count = 0
        item_got = ""
        items_got = []
        amount_got = 0
        while len(items_got) < len(items_wanted):
            item_got = choice(items,p=probabilities)
            if pity_count == 50:
                items_got.append(random.choice([x for x in items_wanted if x not in items_got]))
                pity_count = 0
            elif item_got in items_wanted: #it's the item you want
                if item_got not in items_got: #you don't have it yet
                    items_got.append(item_got)
                    pity_count = 0
            else:
                pity_count += 1
            pull_count += 1
        print(f"Got all gear {items_got} in {pull_count} pulls", end='\r')    
        print(end=LINE_CLEAR)    
        pull_success_results.append(pull_count)

    print(f"Average pulls to get all gear: {sum(pull_success_results) / rounds}") 
    plt.hist(pull_success_results)
    plt.title("Stig pull successes")
    plt.xlabel("Pulls")
    plt.ylabel("Frequency")
    plt.show()

pull_valk()    
pull_gears()
