import pandas as pd
import os

file = "files/chess_results.csv"


def create_file():
    if not os.path.exists(file):
        df = pd.DataFrame({"Player": [],
                           "Winner": [],
                           "TimeTaken": []})
        df.to_csv(file, index=False)


def write_results(white_player, white_is_winner, white_time_taken, black_player, black_is_winner, black_time_taken):
    if os.path.exists(file):
        df = pd.DataFrame({"Player": [white_player, black_player],
                           "Winner": [white_is_winner, black_is_winner],
                           "TimeTaken": [white_time_taken, black_time_taken]})
        df.to_csv("files/chess_results.csv", mode="a", index=False, header=False)


def fastest_wins():
    df = pd.read_csv(file)
    filter_winners = df["Winner"] == "Yes"
    df = df[filter_winners]
    df1 = df[["Player", "TimeTaken"]].nsmallest(5, "TimeTaken")
    return df1.values.tolist()


def most_wins():
    df = pd.read_csv(file)
    player_group = df.groupby("Player")
    num_winners = player_group["Winner"].apply(lambda x: x.str.contains("Yes").sum()).values.tolist()
    player_details = player_group.groups  # Gets all players
    player_list = list(player_details.keys())  # Finds all player names in the aggregate
    return list(zip(player_list, num_winners))  # Returns list of tuples of player and no of wins


def personal_stats(player):
    df = pd.read_csv(file)
    filter_player = df["Player"] == player
    df = df[filter_player]
    player_group = df.groupby("Player")
    num_wins = player_group["Winner"].apply(lambda x: x.str.contains("Yes").sum()).values.tolist()
    num_losses = player_group["Winner"].apply(lambda x: x.str.contains("No").sum()).values.tolist()
    num_draws = player_group["Winner"].apply(lambda x: x.str.contains("Draw").sum()).values.tolist()
    df_winner = df[df["Winner"] == "Yes"]
    fastest_win = df_winner[["Player", "TimeTaken"]].nsmallest(1, "TimeTaken").values.tolist()
    return num_wins, num_losses, num_draws, fastest_win
