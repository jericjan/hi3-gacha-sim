import json
import logging
import statistics
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from chart_helpers import make_bar, make_histogram
from db import Database
from simulation_setup import Simulation

logging.basicConfig(level=logging.INFO)
SHOW_EFFICIENCY = False

CURRENT_DIR = Path(sys.executable).parent if hasattr(sys, "frozen") else Path.cwd()

db = Database(CURRENT_DIR / "saved_pulls.db")
sim = Simulation(db)


def main():
    running = True
    while running:
        if db.count_items() != 0:
            while True:
                db.show_all()
                print(
                    "Type the ID to view a simulation,\n"
                    "'n' to run a new one,\n"
                    "'d' to delete one,\n"
                    "'q' to quit."
                )
                start_choice = input(">> ")
                if start_choice.lower() == "q":
                    running = False
                    break
                elif start_choice.lower() == "n":
                    name, valk_res, gear_res, no_well_gear_res = sim.new_sim()
                    break
                elif start_choice.lower() == "d":
                    while True:
                        id = input("Type the ID of the simulation you want to delete: ")
                        row = db.get_row(id)
                        if row:
                            db.delete_row(id)
                            print(f"ID {id} deleted.")
                            break
                        else:
                            print("ID doesn't exist.")

                else:
                    row = db.get_row(start_choice)

                    if row:
                        name = row[1]
                        row = json.loads(row[0])
                        valk_res = row["valks"]
                        gear_res = row["gears"]
                        no_well_gear_res = row["no_well_gears"]
                        break
                    else:
                        print("ID doesn't exist.")
        else:
            print("No saved pulls yet.")
            name, valk_res, gear_res, no_well_gear_res = sim.new_sim()

        if running is False:
            break

        valk_res = np.array(valk_res)
        gear_res = np.array(gear_res)
        no_well_gear_res = np.array(no_well_gear_res)

        combined_res = valk_res + gear_res
        no_well_combined_res = valk_res + no_well_gear_res

        valk_xtals = statistics.mean(valk_res) * 280
        gear_xtals = statistics.mean(gear_res) * 280

        def calc_mean_median_mode(data):
            mean = statistics.mean(data)
            print(f"- Mean: {mean:.2f} ({(mean*280):.2f} xtals)")

            median = statistics.median(data)
            print(f"- Median: {median:.2f} ({(median*280):.2f} xtals)")

            mode = statistics.multimode(data)
            print(
                f"- Mode: {', '.join(str(x) for x in mode)} "
                f"({', '.join([str(x*280) for x in mode])} xtals)"
            )

            print(f"- Min: {min(data):.2f} Max: {max(data):.2f}")

        print(
            f"Average pulls to get valk: "
            f"{statistics.mean(valk_res)} ({valk_xtals} crystals)"
        )
        print(
            f"Average pulls to get all gear: "
            f"{statistics.mean(gear_res)} ({gear_xtals} crystals)"
        )
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

        make_histogram(valk_res, "Valk pull successes", 10)
        make_histogram(gear_res, "Gear pull successes w/ wishing well")

        class Xcalculator:
            def __init__(self, values, bins, labels=None, title=""):
                if not isinstance(values[0], np.ndarray):
                    self.values = np.array([values])  # contains y values
                else:
                    self.values = values  # contains y values

                self.bins = bins  # contains x values
                self.labels = labels
                self.dic = {x: [] for x in self.labels}
                self.title = title

            def calculate_x_value(self, y_value):
                for label, x in zip(self.labels, self.values):
                    try:
                        index = np.where(x >= y_value)[0][0]
                        x_value = self.bins[index]
                        self.dic[label].append(
                            f"{x_value:.2f} pulls has a {y_value*100}% chance"
                        )
                    except IndexError:
                        self.dic[label].append(
                            f"[Out Of Bounds] pulls has a {y_value*100}% chance"
                        )

            def calculate_y_value(self, x_value):
                for label, x in zip(self.labels, self.values):
                    try:
                        index = np.where(self.bins >= x_value)[0][0]
                        y_value = x[index]
                        self.dic[label].append(
                            f"{x_value:.2f} pulls has a {(y_value*100):.2f}% chance"
                        )
                    except IndexError:
                        self.dic[label].append(f"{x_value:.2f} pulls: Out Of Bounds")

            def show_all(self):
                print(self.title)
                for key, values in self.dic.items():
                    print(key)
                    for value in values:
                        print(f"- {value}")
                self.dic = {x: [] for x in self.labels}  # clears items
                print("")

        xcal_list = []

        values, bins, labels = make_histogram(
            valk_res, "Valk pull successes (cumulative)", cumulative=True
        )

        xcal = Xcalculator(values, bins, ["Valk pulls"], "VALK ONLY:")
        xcal.calculate_x_value(0.25)
        xcal.calculate_x_value(0.5)
        xcal.calculate_x_value(0.75)
        xcal.calculate_x_value(0.90)
        xcal.calculate_x_value(0.95)
        xcal.show_all()
        xcal_list.append(xcal)

        if SHOW_EFFICIENCY:
            make_bar(bins, values, "Valk efficiency")

        values, bins, labels = make_histogram(
            [gear_res, no_well_gear_res],
            "Gear pull successes (cumulative)",
            cumulative=True,
            alpha=0.5,
            label=["With wishing well:", "Without wishing well:"],
        )
        xcal = Xcalculator(values, bins, labels, "GEARS ONLY:")
        xcal.calculate_x_value(0.25)
        xcal.calculate_x_value(0.5)
        xcal.calculate_x_value(0.75)
        xcal.calculate_x_value(0.90)
        xcal.calculate_x_value(0.95)
        xcal.show_all()
        xcal_list.append(xcal)

        if SHOW_EFFICIENCY:
            make_bar(
                bins,
                values,
                "Gear efficiency",
                ["With wishing well:", "Without wishing well:"],
            )

        values, bins, labels = make_histogram(
            [combined_res, no_well_combined_res],
            "Combined pull successes (cumulative)",
            cumulative=True,
            alpha=0.5,
            label=["With wishing well:", "Without wishing well:"],
        )
        xcal = Xcalculator(values, bins, labels, "COMBINED:")
        xcal.calculate_x_value(0.25)
        xcal.calculate_x_value(0.5)
        xcal.calculate_x_value(0.75)
        xcal.calculate_x_value(0.90)
        xcal.calculate_x_value(0.95)
        xcal.show_all()
        xcal_list.append(xcal)

        if SHOW_EFFICIENCY:
            make_bar(
                bins,
                values,
                "Combined efficiency",
                ["With wishing well:", "Without wishing well:"],
            )

        print("Close all graph windows to continue...")

        plt.show()

        while True:
            print(
                f"Selected: [{name}]\n"
                "Type a number of pulls or a percentage from 1%-100% to calculate "
                "the probability or number of pulls needed, respectively.\n"
                "'q' to quit to main menu."
            )
            user_input = input(">> ")
            print("")
            if user_input.lower() == "q":
                break
            elif user_input.isdigit():  # pulls input
                user_input = int(user_input)
                for xcal in xcal_list:
                    xcal.calculate_y_value(user_input)
                    xcal.show_all()
            elif user_input.endswith("%"):
                number_without_percent = user_input.rstrip("%")
                if number_without_percent.isdigit():
                    percentage = int(number_without_percent) / 100
                    for xcal in xcal_list:
                        xcal.calculate_x_value(percentage)
                        xcal.show_all()
                else:
                    print(
                        "Invalid format: "
                        "The number part of the percentage is not a number."
                    )
            else:
                print("Invalid input.")


try:
    main()
finally:
    print("Closing database...")
    db.close()
