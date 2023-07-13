from gacha import pull_gears, pull_valk
from thread_utils import CustomThread, ThreadStarter

DEFAULT_ROUNDS = 10000
DEFAULT_VALK_PITY = 100
DEFAULT_GEAR_PITY = 50


def setup_info():
    print("Leave blank to use the default value.")
    name = input("Give this simulation a name: ") or "Unnamed"

    def get_integer_input(prompt, default):
        while True:
            try:
                user_input = input(f"{prompt} (default: {default})? ")
                return int(user_input) if user_input else default
            except ValueError:
                print("Invalid input. Please enter an integer.")

    rounds = get_integer_input("How many rounds", DEFAULT_ROUNDS)
    valk_pity = get_integer_input("What's the valkyrie pity", DEFAULT_VALK_PITY)
    gear_pity = get_integer_input("What's the gear pity", DEFAULT_GEAR_PITY)

    return name, rounds, valk_pity, gear_pity


class Simulation:
    def __init__(self, db):
        self.db = db

    def new_sim(self):
        name, rounds, valk_pity, gear_pity = setup_info()

        t_starter = ThreadStarter(
            [
                CustomThread(
                    target=pull_valk, kwargs={"rounds": rounds, "pity": valk_pity}
                ),
                CustomThread(
                    target=pull_gears,
                    kwargs={
                        "rounds": rounds,
                        "wishing_well": True,
                        "gear_pity": gear_pity,
                    },
                ),
                CustomThread(
                    target=pull_gears,
                    kwargs={
                        "rounds": rounds,
                        "wishing_well": False,
                        "gear_pity": gear_pity,
                    },
                ),
            ]
        )

        t_starter.start()

        valk_res, gear_res, no_well_gear_res = t_starter.results
        dic = {"valks": valk_res, "gears": gear_res, "no_well_gears": no_well_gear_res}
        self.db.add(name, rounds, valk_pity, gear_pity, dic)
        return name, valk_res, gear_res, no_well_gear_res
