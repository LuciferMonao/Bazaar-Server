from get_data import get_item_price
import pickle
import minion_list

def get_leaderboard(MINION_AMOUNT = 1, MINION_LEVEL = 1, MINION_FUEL = 0.0, SECONDS = 3600, ROUND=True, diamondspreading=True, afk=1):
    minion_data = minion_list.get()

    minion_profits = {}

    for minion in minion_data[1]:
        data = minion_data[1][minion]
        profit = 0


        for element in data["Products"]:
            if not element["Name"] == False:
                pure_items = pure_item_profit = ((SECONDS / minion_data[1][minion]["Speed"][MINION_LEVEL - 1] / 2 * (1 + MINION_FUEL)) * element["Amount"] * MINION_AMOUNT)
                pure_item_profit = get_item_price(element["Name"]) * pure_items
                if afk > 0.0 and "Afk" in element:
                    profit += pure_item_profit * (1 + afk)
                else:
                    profit += ((SECONDS / minion_data[1][minion]["Speed"][MINION_LEVEL - 1] / 2 * (1 + MINION_FUEL)) * get_item_price(element["Name"]) * element["Amount"] * MINION_AMOUNT)
                    if diamondspreading: profit += (pure_items / 10) * get_item_price("DIAMOND")
        minion_profits[minion] = profit if ROUND == False else int(profit)

    leaderboard = []

    for key, value in sorted(minion_profits.items(), key=lambda item: item[1]):
        leaderboard.append([key, value])
    leaderboard.reverse()
    return(leaderboard)

def get_minion_ranking(minion, MINION_AMOUNT=16, MINION_LEVEL=5, SECONDS=86400, MINION_FUEL=0.25):
    leaderboard = get_leaderboard(MINION_AMOUNT=MINION_AMOUNT, MINION_LEVEL=MINION_LEVEL, SECONDS=SECONDS, MINION_FUEL=MINION_FUEL)
    position = False
    for element in range(0, len(leaderboard)):
        if leaderboard[element][0] == minion:
            position = element
            break
    return([len(leaderboard) - position, leaderboard[element][1]])




if __name__ == "__main__":
    while True:
        try:
            MINION_AMOUNT = int(input("How many Minions do you want to use?\n"))
            if MINION_AMOUNT == 0: break
            MINION_FUEL = float(int(input("What minion Fuel do you use? (Percent of 100)\n")) / 100)
            MINION_LEVEL = int(input("What Level will your minions have?\n"))
            AFK = float(input("How often will you be (normal and afk) on your island (Percent of 100)?\n")) / 100
            diamondspreading = True if str(input("Do you use Diamond spreadings? yes / no\n")) == "no" else False
            show = int(input("Do you want to see everything or just the top ones. If you want to see everything enter 0 else the number of the minions you want to see\n"))
            #print(get_minion_ranking("rabbit"))
        except ValueError:
            print("Please enter a valid number.")
            pass
        except TypeError:
            print("Please enter a valid number.")
            pass

        leaderboard = get_leaderboard(MINION_AMOUNT=MINION_AMOUNT, MINION_LEVEL=MINION_LEVEL, MINION_FUEL=MINION_FUEL, SECONDS=86400, afk=AFK, diamondspreading=diamondspreading)
        for element in leaderboard:
            if leaderboard.index(element) + 1 > show and not show == 0: break
            print("{}. is {} with {} coins a day.".format(leaderboard.index(element) + 1, element[0], element[1]))
        print("This is the minion leaderboard for {} minions, all Level {} with fuel for {}% more speed.\nAlso a Diamondspreading is {} used and the time of somebody on the island is {}% of the day.".format(MINION_AMOUNT, MINION_LEVEL, MINION_FUEL * 100, "not" if diamondspreading == False else "", AFK * 100))