import soccerdata as sd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi



# Format %
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{v} ({p:.0f}%)'.format(v=val, p=pct)
    return my_format

# Format season
def season_format(year):
    if '/' in year:
        parts = year.split('/')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():  # If the format is A/W
            if len(parts[0]) == 4 and len(parts[1]) == 4:  # If format is ABCD/WXYZ
                if parts[0] == str(int(parts[1]) - 1):  # If ABCD is 1 year less than WXYZ
                    return parts[0]  # Return format as ABCD
            elif len(parts[0]) == 4 and len(parts[1]) == 2:  # If format is ABCD/YZ
                if parts[0][2:] == str(int(parts[1]) - 1):  # If CD is 1 year less than YZ
                    return parts[0] # Return format as ABCD
            elif len(parts[0]) == 2 and len(parts[1]) == 2: # If format is 18/19
                if parts[0] == str(int(parts[1]) - 1):  # If 18 is 1 year less than 19
                    if (0 <= int(parts[0]) <= 79):
                        return int("20" + parts[0])
                    else:
                        return int("19" + parts[0])
            
    elif year.isdigit() and len(year) == 4:
        if str(year[:2]) == str(int(year[2:]) - 1): # If 1819, 8081
            if (0 <= int(year[:2]) <= 79): 
                return int("20" + year[:2]) # Return 2018
            else:
                return int("19" + year[:2]) # Return 1980
        else:
            return year

    else:
        return False
    

# Display proper season
def season_display(year):
    first_part = year[:2]
    second_part = year[2:]
    return f"{first_part}/{second_part}"  

# Format league
def league_format(league):
    if (league == "ENG" or league == "England" or league == "1" or league == "Premier League"): return "ENG-Premier League"
    elif (league == "ESP" or league == "Spain" or league == "2" or league == "La Liga"): return "ESP-La Liga"
    elif (league == "ITA" or league == "Italy" or league == "3" or league == "Serie A"): return "ITA-Serie A"
    elif (league == "GER" or league == "Germany" or league == "4" or league == "Bundesliga"): return "GER-Bundesliga"
    elif (league == "FRA" or league == "France" or league == "5" or league == "Ligue 1"): return "FRA-Ligue 1"

    else:
        return False

# Fetch player stats
def read_player_stats(fbref, stat_type, player_name):
    player_season_stats = fbref.read_player_season_stats(stat_type=stat_type)
    return player_season_stats[player_season_stats.index.get_level_values("player").str.contains(player_name, case=False, na=False)]

# Get player
def get_player(p_name, p_league, p_year):
    try:
        fbref = sd.FBref(leagues=p_league, seasons=p_year)
        player = read_player_stats(fbref, "standard", p_name)

        try:
            player_name = player.index.get_level_values("player")[0]
        except (IndexError, AttributeError):
            player_name = None

    except IndexError:
        player_name = None

    return player_name

# Compare Stats
def compare_statistics(statistic, p1_name, p1_year, p1_league, p2_name, p2_year, p2_league):
    stat_functions = {
        "standard": standard,                               # 1 Standard
        "shooting": shooting,                               # 2 Shooting
        "final_ball": final_ball,                           # 3 Final Ball
        "goal_shot_creation": goal_and_shot,                # 4 Goal and Shot Creation
        "playmaking": playmaking,                           # 5 Playmaking
        "possession": possession,                           # 6 Possession
        "pass_types": pass_types,                           # 7 Pass Types
        "passing_distance": passing_distance,               # 8 Passing Distance
    }

    if statistic in stat_functions:
        stat_function = stat_functions[statistic]
        fbref1 = sd.FBref(leagues = p1_league, seasons = p1_year)
        fbref2 = sd.FBref(leagues = p2_league, seasons = p2_year)
        stat_function(fbref1, p1_name, fbref2, p2_name)
    else:
        print("Invalid statistic: ", statistic)



# 1 Standard
def standard(fbref1, p1_name, fbref2, p2_name):
    player1_season_stats = read_player_stats(fbref1, "standard", p1_name)
    player2_season_stats = read_player_stats(fbref2, "standard", p2_name)

    player1_name = player1_season_stats.index.get_level_values("player")[0]
    player1_team = player1_season_stats.index.get_level_values("team")[0]
    player1_season = player1_season_stats.index.get_level_values("season")[0]

    player2_name = player2_season_stats.index.get_level_values("player")[0]
    player2_team = player2_season_stats.index.get_level_values("team")[0]
    player2_season = player2_season_stats.index.get_level_values("season")[0]

    p1_90s = player1_season_stats["Playing Time"]["90s"].values[0]
    p2_90s = player2_season_stats["Playing Time"]["90s"].values[0]

    p1_color = 'red'
    p2_color = 'blue'

    # Standard stat categories
    standard_categories = ['Goals', 'xG', 'Assists', 'xAG', 'Progressive Carries', 'Progressive Passes', '']

    # Number of categories
    num_categories = len(standard_categories)

    p1_standard_stats = [
        round(player1_season_stats["Performance"]["Gls"].values[0] / p1_90s, 2),
        round(player1_season_stats["Expected"]["xG"].values[0] / p1_90s, 2),
        round(player1_season_stats["Performance"]["Ast"].values[0] / p1_90s, 2),
        round(player1_season_stats["Expected"]["xAG"].values[0] / p1_90s, 2),
        round(player1_season_stats["Progression"]["PrgC"].values[0] / p1_90s, 2),
        round(player1_season_stats["Progression"]["PrgP"].values[0] / p1_90s, 2),
        round(player1_season_stats["Performance"]["Gls"].values[0] / p1_90s, 2),
    ]

    p2_standard_stats = [
        round(player2_season_stats["Performance"]["Gls"].values[0] / p2_90s, 2),
        round(player2_season_stats["Expected"]["xG"].values[0] / p2_90s, 2),
        round(player2_season_stats["Performance"]["Ast"].values[0] / p2_90s, 2),
        round(player2_season_stats["Expected"]["xAG"].values[0] / p2_90s, 2),
        round(player2_season_stats["Progression"]["PrgC"].values[0] / p2_90s, 2),
        round(player2_season_stats["Progression"]["PrgP"].values[0] / p2_90s, 2),
        round(player2_season_stats["Performance"]["Gls"].values[0] / p2_90s, 2),
    ]

    p1_normalized = []
    p2_normalized = []

    for p1_stat, p2_stat in zip(p1_standard_stats, p2_standard_stats):
        max_value = max(p1_stat, p2_stat)
        p1_normalized.append(round(p1_stat/max_value/1.1, 2))
        p2_normalized.append(round(p2_stat/max_value/1.1, 2))

    # Create a list of angles for the radar chart
    angles = np.flip(np.linspace(0, 2 * np.pi, num_categories, endpoint=True))

    # Make the plot circular
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, polar=True)

    # Plot the data for Player 1
    line1, = ax.plot(angles, p1_normalized, marker='o', label=player1_name, color=p1_color)
    ax.fill(angles, p1_normalized, alpha=0.25, color=p1_color)

    # Plot the data for Player 2
    line2, = ax.plot(angles, p2_normalized, marker='o', label=player2_name, color=p2_color)
    ax.fill(angles, p2_normalized, alpha=0.25, color=p2_color)

    # Set the angle labels
    ax.set_xticks(angles)
    ax.set_xticklabels(standard_categories)

    # Set y-axis labels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10)
    plt.ylim(0, 1)
    
    # Add numeric labels for Player 1
    for angle, norm_stat, stat in zip(angles, p1_normalized, p1_standard_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line1.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Add numeric labels for Player 2
    for angle, norm_stat, stat in zip(angles, p2_normalized, p2_standard_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line2.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    custom_legend = [
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_name} ({season_display(player1_season)})", markerfacecolor=p1_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p1_90s}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_name} ({season_display(player2_season)})", markerfacecolor=p2_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p2_90s}"),
    ]

    plt.legend(handles=custom_legend, loc='upper right', bbox_to_anchor=(1.55, 1.05))
    ax.set_title(player1_name + " (" + season_display(player1_season) + ") vs " + player2_name + " (" + season_display(player2_season) + "): Standard Stats (Per 90)", y=1.075)

    plt.show()

# 2 Shooting
def shooting(fbref1, p1_name, fbref2, p2_name):
    player1_season_stats = read_player_stats(fbref1, "shooting", p1_name)
    player2_season_stats = read_player_stats(fbref2, "shooting", p2_name)

    player1_name = player1_season_stats.index.get_level_values("player")[0]
    player1_team = player1_season_stats.index.get_level_values("team")[0]
    player1_season = player1_season_stats.index.get_level_values("season")[0]

    player2_name = player2_season_stats.index.get_level_values("player")[0]
    player2_team = player2_season_stats.index.get_level_values("team")[0]
    player2_season = player2_season_stats.index.get_level_values("season")[0]

    p1_90s = player1_season_stats["90s"].values[0]
    p2_90s = player2_season_stats["90s"].values[0]

    p1_color = 'red'
    p2_color = 'blue'

    # Playmaking stat categories
    shooting_categories = ['Goals (p90)', 'xG (p90)', 'Shots (p90)', 'Shots on Target (p90)', 'Goals per Shot', '']

    # Number of categories
    num_categories = len(shooting_categories)

    p1_shooting_stats = [
        round(player1_season_stats["Standard"]["Gls"].values[0] / p1_90s, 2),
        round(player1_season_stats["Expected"]["xG"].values[0] / p1_90s, 2),
        round(player1_season_stats["Standard"]["Sh"].values[0] / p1_90s, 2),
        round(player1_season_stats["Standard"]["SoT"].values[0] / p1_90s, 2),
        round(player1_season_stats["Standard"]["G/Sh"].values[0], 2),
        round(player1_season_stats["Standard"]["Gls"].values[0] / p1_90s, 2),
    ]

    p2_shooting_stats = [
        round(player2_season_stats["Standard"]["Gls"].values[0] / p2_90s, 2),
        round(player2_season_stats["Expected"]["xG"].values[0] / p2_90s, 2),
        round(player2_season_stats["Standard"]["Sh"].values[0] / p2_90s, 2),
        round(player2_season_stats["Standard"]["SoT"].values[0] / p2_90s, 2),
        round(player2_season_stats["Standard"]["G/Sh"].values[0], 2),
        round(player2_season_stats["Standard"]["Gls"].values[0] / p2_90s, 2),
    ]

    p1_normalized = []
    p2_normalized = []

    for p1_stat, p2_stat in zip(p1_shooting_stats, p2_shooting_stats):
        if (p1_stat == p1_shooting_stats[len(p1_shooting_stats)-1]):
                max_value = max(p1_stat, p2_stat)
        max_value = max(p1_stat, p2_stat)
        p1_normalized.append(round(p1_stat/max_value/1.1, 2))
        p2_normalized.append(round(p2_stat/max_value/1.1, 2))

    # Create a list of angles for the radar chart
    angles = np.flip(np.linspace(0, 2 * np.pi, num_categories, endpoint=True))

    # Make the plot circular
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, polar=True)

    # Plot the data for Player 1
    line1, = ax.plot(angles, p1_normalized, marker='o', label=player1_name, color=p1_color)
    ax.fill(angles, p1_normalized, alpha=0.25, color=p1_color)

    # Plot the data for Player 2
    line2, = ax.plot(angles, p2_normalized, marker='o', label=player2_name, color=p2_color)
    ax.fill(angles, p2_normalized, alpha=0.25, color=p2_color)

    # Set the angle labels
    ax.set_xticks(angles)
    ax.set_xticklabels(shooting_categories)

    # Set y-axis labels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10)
    plt.ylim(0, 1)
    
    # Add numeric labels for Player 1
    for angle, norm_stat, stat in zip(angles, p1_normalized, p1_shooting_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line1.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Add numeric labels for Player 2
    for angle, norm_stat, stat in zip(angles, p2_normalized, p2_shooting_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line2.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    custom_legend = [
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_name} ({season_display(player1_season)})", markerfacecolor=p1_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p1_90s}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_name} ({season_display(player2_season)})", markerfacecolor=p2_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p2_90s}"),
    ]

    plt.legend(handles=custom_legend, loc='upper right', bbox_to_anchor=(1.5, 1.05))
    ax.set_title(player1_name + " (" + season_display(player1_season) + ") vs " + player2_name + " (" + season_display(player2_season) + "): Shooting Comparision", y=1.075)

    plt.show()

# 3 Final Ball
def final_ball(fbref1, p1_name, fbref2, p2_name):
    player1_season_stats = read_player_stats(fbref1, "passing", p1_name)
    player2_season_stats = read_player_stats(fbref2, "passing", p2_name)

    player1_name = player1_season_stats.index.get_level_values("player")[0]
    player1_team = player1_season_stats.index.get_level_values("team")[0]
    player1_season = player1_season_stats.index.get_level_values("season")[0]

    player2_name = player2_season_stats.index.get_level_values("player")[0]
    player2_team = player2_season_stats.index.get_level_values("team")[0]
    player2_season = player2_season_stats.index.get_level_values("season")[0]

    p1_90s = player1_season_stats["90s"].values[0]
    p2_90s = player2_season_stats["90s"].values[0]

    p1_color = 'red'
    p2_color = 'blue'

    # Final Ball stat categories
    final_ball_categories = ['Assists', 'xAG', 'xA', 'Key Passes', 'Passes into Penalty Area', 'Crosses in Penalty Area', '']

    # Number of categories
    num_categories = len(final_ball_categories)

    p1_playmaking_stats = [
        round(player1_season_stats["Ast"].values[0] / p1_90s, 2),
        round(player1_season_stats["xAG"].values[0] / p1_90s, 2),
        round(player1_season_stats["xA"].values[0] / p1_90s, 2),
        round(player1_season_stats["KP"].values[0] / p1_90s, 2),
        round(player1_season_stats["PPA"].values[0] / p1_90s, 2),
        round(player1_season_stats["CrsPA"].values[0] / p1_90s, 2),
        round(player1_season_stats["Ast"].values[0] / p1_90s, 2),
    ]

    p2_playmaking_stats = [
        round(player2_season_stats["Ast"].values[0] / p2_90s, 2),
        round(player2_season_stats["xAG"].values[0] / p2_90s, 2),
        round(player2_season_stats["xA"].values[0] / p2_90s, 2),
        round(player2_season_stats["KP"].values[0] / p2_90s, 2),
        round(player2_season_stats["PPA"].values[0] / p2_90s, 2),
        round(player2_season_stats["CrsPA"].values[0] / p2_90s, 2),
        round(player2_season_stats["Ast"].values[0] / p2_90s, 2),
    ]

    p1_normalized = []
    p2_normalized = []
    
    for p1_stat, p2_stat in zip(p1_playmaking_stats, p2_playmaking_stats):
        max_value = max(p1_stat, p2_stat)
        p1_normalized.append(round(p1_stat/max_value/1.1, 2))
        p2_normalized.append(round(p2_stat/max_value/1.1, 2))

    
    # Create a list of angles for the radar chart
    angles = np.flip(np.linspace(0, 2 * np.pi, num_categories, endpoint=True))

    # Make the plot circular
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, polar=True)

    # Plot the data for Player 1
    line1, = ax.plot(angles, p1_normalized, marker='o', label=player1_name, color=p1_color)
    ax.fill(angles, p1_normalized, alpha=0.25, color=p1_color)

    # Plot the data for Player 2
    line2, = ax.plot(angles, p2_normalized, marker='o', label=player2_name, color=p2_color)
    ax.fill(angles, p2_normalized, alpha=0.25, color=p2_color)

    # Set the angle labels
    ax.set_xticks(angles)
    ax.set_xticklabels(final_ball_categories)

    # Set y-axis labels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10)
    plt.ylim(0, 1)

    # Add numeric labels for Player 1
    for angle, norm_stat, stat in zip(angles, p1_normalized, p1_playmaking_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line1.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Add numeric labels for Player 2
    for angle, norm_stat, stat in zip(angles, p2_normalized, p2_playmaking_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line2.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Create a custom legend
    custom_legend = [
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_name} ({season_display(player1_season)})", markerfacecolor=p1_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p1_90s}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_name} ({season_display(player2_season)})", markerfacecolor=p2_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p2_90s}"),
    ]

    plt.legend(handles=custom_legend, loc='upper right', bbox_to_anchor=(1.5, 1.05))
    ax.set_title(player1_name + " (" + season_display(player1_season) + ") vs " + player2_name + " (" + season_display(player2_season) + "): Final Ball Comparison (Per 90)", y=1.075)

    plt.show()

# 4 Goal and Shot Creation
def goal_and_shot(fbref1, p1_name, fbref2, p2_name):
    player1_season_stats = read_player_stats(fbref1, "goal_shot_creation", p1_name)
    player2_season_stats = read_player_stats(fbref2, "goal_shot_creation", p2_name)

    player1_name = player1_season_stats.index.get_level_values("player")[0]
    player1_team = player1_season_stats.index.get_level_values("team")[0]
    player1_season = player1_season_stats.index.get_level_values("season")[0]

    player2_name = player2_season_stats.index.get_level_values("player")[0]
    player2_team = player2_season_stats.index.get_level_values("team")[0] 
    player2_season = player2_season_stats.index.get_level_values("season")[0]

    p1_90s = player1_season_stats["90s"].values[0]
    p2_90s = player2_season_stats["90s"].values[0]

    p1_color = 'red'
    p2_color = 'blue'

    # Goal and Shot stat categories
    goalshot_categories = ['SCA (Live)', 'SCA (Dead)', 'SCA (Take-Ons)', 'GCA (Live)', 'GCA (Dead)', 'GCA (Take-Ons)', '']

    # Number of categories
    num_categories = len(goalshot_categories)

    p1_goalshot_stats = [
        round(player1_season_stats["SCA Types"]["PassLive"].values[0] / p1_90s, 2),
        round(player1_season_stats["SCA Types"]["PassDead"].values[0] / p1_90s, 2),
        round(player1_season_stats["SCA Types"]["TO"].values[0] / p1_90s, 2),
        round(player1_season_stats["GCA Types"]["PassLive"].values[0] / p1_90s, 2),
        round(player1_season_stats["GCA Types"]["PassDead"].values[0] / p1_90s, 2),
        round(player1_season_stats["GCA Types"]["TO"].values[0] / p1_90s, 2),
        round(player1_season_stats["SCA Types"]["PassLive"].values[0] / p1_90s, 2),
    ]

    p2_goalshot_stats = [
        round(player2_season_stats["SCA Types"]["PassLive"].values[0] / p1_90s, 2),
        round(player2_season_stats["SCA Types"]["PassDead"].values[0] / p1_90s, 2),
        round(player2_season_stats["SCA Types"]["TO"].values[0] / p1_90s, 2),
        round(player2_season_stats["GCA Types"]["PassLive"].values[0] / p1_90s, 2),
        round(player2_season_stats["GCA Types"]["PassDead"].values[0] / p1_90s, 2),
        round(player2_season_stats["GCA Types"]["TO"].values[0] / p1_90s, 2),
        round(player2_season_stats["SCA Types"]["PassLive"].values[0] / p1_90s, 2),
    ]

    p1_normalized = []
    p2_normalized = []
    
    for p1_stat, p2_stat in zip(p1_goalshot_stats, p2_goalshot_stats):
        max_value = max(p1_stat, p2_stat)
        p1_normalized.append(round(p1_stat/max_value/1.1, 2))
        p2_normalized.append(round(p2_stat/max_value/1.1, 2))
    
    # Create a list of angles for the radar chart
    angles = np.flip(np.linspace(0, 2 * pi, num_categories, endpoint=True))

    # Make the plot circular
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, polar=True)

    # Plot the data for Player 1
    line1, = ax.plot(angles, p1_normalized, marker='o', label=player1_name, color=p1_color)
    ax.fill(angles, p1_normalized, alpha=0.25, color=p1_color)

    # Plot the data for Player 2
    line2, = ax.plot(angles, p2_normalized, marker='o', label=player2_name, color=p2_color)
    ax.fill(angles, p2_normalized, alpha=0.25, color=p2_color)

    # Set the angle labels
    ax.set_xticks(angles)
    ax.set_xticklabels(goalshot_categories)

    # Set y-axis labels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10)
    plt.ylim(0, 1)

    # Add numeric labels for Player 1
    for angle, norm_stat, stat in zip(angles, p1_normalized, p1_goalshot_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line1.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Add numeric labels for Player 2
    for angle, norm_stat, stat in zip(angles, p2_normalized, p2_goalshot_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line2.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Create a custom legend
    custom_legend = [
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_name} ({season_display(player1_season)})", markerfacecolor=p1_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p1_90s}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_name} ({season_display(player2_season)})", markerfacecolor=p2_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p2_90s}"),
    ]

    plt.legend(handles=custom_legend, loc='upper right', bbox_to_anchor=(1.5, 1.05))
    ax.set_title(player1_name + " (" + season_display(player1_season) + ") vs " + player2_name + " (" + season_display(player2_season) + "): SCA and GCA Comparison (Per 90)", y=1.075)

    plt.show()

# 5 Playmaking
def playmaking(fbref1, p1_name, fbref2, p2_name):  
    player1_season_stats_pass = read_player_stats(fbref1, "passing", p1_name)
    player2_season_stats_pass = read_player_stats(fbref2, "passing", p2_name)

    player1_season_stats_poss = read_player_stats(fbref1, "possession", p1_name)
    player2_season_stats_poss = read_player_stats(fbref2, "possession", p2_name)

    player1_name = player1_season_stats_pass.index.get_level_values("player")[0]
    player1_team = player1_season_stats_pass.index.get_level_values("team")[0]
    player1_season = player1_season_stats_pass.index.get_level_values("season")[0]

    player2_name = player2_season_stats_pass.index.get_level_values("player")[0]
    player2_team = player2_season_stats_pass.index.get_level_values("team")[0]
    player2_season = player2_season_stats_pass.index.get_level_values("season")[0]

    p1_90s = player1_season_stats_pass["90s"].values[0]
    p2_90s = player2_season_stats_pass["90s"].values[0]

    p1_color = 'red'
    p2_color = 'blue'

    # Playmaking stat categories
    playmaking_categories = ['Total Passes', 'Pass Accuracy (%)', 'Key Passes', 'Progressive Passes', 'Passes into Final Third', 'Passes into Penalty Area', 'Progressive Carries', 'Carries into Final Third', 'Carries into Penalty Area', 'Take Ons', 'Take Ons %', '']

    # Number of categories
    num_categories = len(playmaking_categories)

    p1_playmaking_stats = [
        round(player1_season_stats_pass["Total"]["Cmp"].values[0] / p1_90s, 2),
        round(player1_season_stats_pass["Total"]["Cmp%"].values[0], 2),
        round(player1_season_stats_pass["KP"].values[0] / p1_90s, 2),
        round(player1_season_stats_pass["PrgP"].values[0] / p1_90s, 2),
        round(player1_season_stats_pass["1/3"].values[0] / p1_90s, 2),
        round(player1_season_stats_pass["PPA"].values[0] / p1_90s, 2),
        round(player1_season_stats_poss["Carries"]["PrgC"].values[0] / p1_90s, 2),
        round(player1_season_stats_poss["Carries"]["1/3"].values[0] / p1_90s, 2),
        round(player1_season_stats_poss["Carries"]["CPA"].values[0] / p1_90s, 2),
        round(player1_season_stats_poss["Take-Ons"]["Succ"].values[0] / p1_90s, 2),
        round(player1_season_stats_poss["Take-Ons"]["Succ%"].values[0], 2),
        round(player1_season_stats_pass["Total"]["Cmp"].values[0] / p1_90s, 2),
    ]

    p2_playmaking_stats = [
        round(player2_season_stats_pass["Total"]["Cmp"].values[0] / p2_90s, 2),
        round(player2_season_stats_pass["Total"]["Cmp%"].values[0], 2),
        round(player2_season_stats_pass["KP"].values[0] / p2_90s, 2),
        round(player2_season_stats_pass["PrgP"].values[0] / p2_90s, 2),
        round(player2_season_stats_pass["1/3"].values[0] / p2_90s, 2),
        round(player2_season_stats_pass["PPA"].values[0] / p2_90s, 2),
        round(player2_season_stats_poss["Carries"]["PrgC"].values[0] / p2_90s, 2),
        round(player2_season_stats_poss["Carries"]["1/3"].values[0] / p2_90s, 2),
        round(player2_season_stats_poss["Carries"]["CPA"].values[0] / p2_90s, 2),
        round(player2_season_stats_poss["Take-Ons"]["Succ"].values[0] / p2_90s, 2),
        round(player2_season_stats_poss["Take-Ons"]["Succ%"].values[0], 2),
        round(player2_season_stats_pass["Total"]["Cmp"].values[0] / p2_90s, 2),
    ]

    p1_normalized = []
    p2_normalized = []
    
    for p1_stat, p2_stat in zip(p1_playmaking_stats, p2_playmaking_stats):
        max_value = max(p1_stat, p2_stat)
        p1_normalized.append(round(p1_stat/max_value/1.1, 2))
        p2_normalized.append(round(p2_stat/max_value/1.1, 2))
    
    # Create a list of angles for the radar chart
    angles = np.flip(np.linspace(0, 2 * np.pi, num_categories, endpoint=True))

    # Make the plot circular
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, polar=True)

    # Plot the data for Player 1
    line1, = ax.plot(angles, p1_normalized, marker='o', label=player1_name, color=p1_color)
    ax.fill(angles, p1_normalized, alpha=0.25, color=p1_color)

    # Plot the data for Player 2
    line2, = ax.plot(angles, p2_normalized, marker='o', label=player2_name, color=p2_color)
    ax.fill(angles, p2_normalized, alpha=0.25, color=p2_color)

    # Set the angle labels
    ax.set_xticks(angles)
    ax.set_xticklabels(playmaking_categories)

    # Set y-axis labels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10)
    plt.ylim(0, 1)

    # Add numeric labels for Player 1
    for angle, norm_stat, stat in zip(angles, p1_normalized, p1_playmaking_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line1.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Add numeric labels for Player 2
    for angle, norm_stat, stat in zip(angles, p2_normalized, p2_playmaking_stats):
        x = angle
        y = norm_stat + 0.075
        ax.annotate(
            str(stat),
            xy=(x, y),
            xytext=(0, 0),
            textcoords='offset points',
            color=line2.get_color(),
            fontsize=10,
            fontweight='bold',
            ha="center",
            va="center",
            bbox=dict(boxstyle='round,pad=0.3', facecolor=(1, 1, 1, 0.5), edgecolor='none')
        )

    # Create a custom legend
    custom_legend = [
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_name} ({season_display(player1_season)})", markerfacecolor=p1_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p1_90s}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_name} ({season_display(player2_season)})", markerfacecolor=p2_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p2_90s}"),
    ]

    plt.legend(handles=custom_legend, loc='upper right', bbox_to_anchor=(1.5, 1.05))
    ax.set_title(player1_name + " (" + season_display(player1_season) + ") vs " + player2_name + " (" + season_display(player2_season) + "): Playmaking Comparison (Per 90)", y=1.075)

    plt.show()

# 6 Possession
def possession(fbref1, p1_name, fbref2, p2_name):
    player1_season_stats = read_player_stats(fbref1, "possession", p1_name)
    player2_season_stats = read_player_stats(fbref2, "possession", p2_name)

    player1_name = player1_season_stats.index.get_level_values("player")[0]
    player1_team = player1_season_stats.index.get_level_values("team")[0]
    player1_season = player1_season_stats.index.get_level_values("season")[0]

    player2_name = player2_season_stats.index.get_level_values("player")[0]
    player2_team = player2_season_stats.index.get_level_values("team")[0] 
    player2_season = player2_season_stats.index.get_level_values("season")[0]

    # Possession stat categories
    possession_categories = ["Def Pen", "Def 3rd", "Mid 3rd", "Att 3rd", "Att Pen"]

    player1_possession_stats = player1_season_stats["Touches"][possession_categories].values.tolist()[0]
    player2_possession_stats = player2_season_stats["Touches"][possession_categories].values.tolist()[0]

    # Create the side-by-side pie charts
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))

    # Player 1 Pie Chart
    wedges1, texts1, autotexts1 = ax[0].pie(player1_possession_stats, labels=possession_categories, autopct=autopct_format(player1_possession_stats), startangle=140)
    for i, wedge in enumerate(wedges1):
        wedge.set_facecolor("red")
        wedge.set_alpha((i+1)/5)

    ax[0].set_title(player1_name + " (" + season_display(player1_season) + "): Total Touches")
    ax[0].axis('equal')
    legend_labels1 = [f'{label}: {autotext.get_text()}' for label, autotext in zip(possession_categories, autotexts1)]
    ax[0].legend(wedges1, legend_labels1,title=player1_name + "'s Touches\n (" + player1_team + ")",  loc="center left", bbox_to_anchor=(1.05, 0.5))

    # Player 2 Pie Chart
    wedges2, texts2, autotexts2 = ax[1].pie(player2_possession_stats, labels=possession_categories, autopct=autopct_format(player2_possession_stats), startangle=140)
    for i, wedge in enumerate(wedges2):
        wedge.set_facecolor("blue")
        wedge.set_alpha((i+1)/5)

    ax[1].set_title(player2_name + " (" + season_display(player2_season) + "): Total Touches")
    ax[1].axis('equal')
    legend_labels2 = [f'{label}: {autotext.get_text()}' for label, autotext in zip(possession_categories, autotexts2)]
    ax[1].legend(wedges2, legend_labels2, title=player2_name + "'s Touches\n (" + player2_team + ")", loc="center left", bbox_to_anchor=(-0.45, 0.5))

    plt.tight_layout()
    plt.show()

# 7 Pass Types
def pass_types(fbref1, p1_name, fbref2, p2_name):
    player1_season_stats = read_player_stats(fbref1, "passing_types", p1_name)
    player2_season_stats = read_player_stats(fbref2, "passing_types", p2_name)

    player1_name = player1_season_stats.index.get_level_values("player")[0]
    player1_team = player1_season_stats.index.get_level_values("team")[0]
    player1_season = player1_season_stats.index.get_level_values("season")[0]

    player2_name = player2_season_stats.index.get_level_values("player")[0]
    player2_team = player2_season_stats.index.get_level_values("team")[0] 
    player2_season = player2_season_stats.index.get_level_values("season")[0]

    # Passing Type stat categories
    passing_types_categories = ["Live", "Through Balls", "Crosses", "Switches"]
    passing_types_categories_input = ["TB", "Crs", "Sw"]

    player1_threestats = player1_season_stats["Pass Types"][passing_types_categories_input].values.tolist()[0]
    player2_threestats = player2_season_stats["Pass Types"][passing_types_categories_input].values.tolist()[0]

    player1_passing_types_stats = [(int(player1_season_stats["Pass Types"]["Live"].values[0] - sum(player1_threestats)))]
    player2_passing_types_stats = [(int(player2_season_stats["Pass Types"]["Live"].values[0] - sum(player2_threestats)))]

    player1_passing_types_stats.extend(player1_threestats)
    player2_passing_types_stats.extend(player2_threestats)

    # Create the side-by-side pie charts
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))

    # Player 1 Pie Chart
    p1_colors = ["darkred", "red", "darkorange", "orange"]
    wedges1, texts1, autotexts1 = ax[0].pie(player1_passing_types_stats, labels=passing_types_categories, autopct=autopct_format(player1_passing_types_stats), startangle=140)
    for i, wedge in enumerate(wedges1):
        wedge.set_facecolor(p1_colors[i])
        wedge.set_alpha(0.8)

    ax[0].set_title(player1_name + " (" + season_display(player1_season) + "): Pass Types", y=1.075)
    ax[0].axis('equal')
    legend_labels1 = [f'{label}: {autotext.get_text()}' for label, autotext in zip(passing_types_categories, autotexts1)]
    ax[0].legend(wedges1, legend_labels1,title=player1_name + "'s Pass Types\n (" + player1_team + ")",  loc="center left", bbox_to_anchor=(1.05, 0.5))

    # Player 2 Pie Chart
    p2_colors = ["darkblue", "blue", "lightskyblue", "cornflowerblue"]
    wedges2, texts2, autotexts2 = ax[1].pie(player2_passing_types_stats, labels=passing_types_categories, autopct=autopct_format(player2_passing_types_stats), startangle=140)
    for i, wedge in enumerate(wedges2):
        wedge.set_facecolor(p2_colors[i])
        wedge.set_alpha(0.8)

    ax[1].set_title(player2_name + " (" + season_display(player2_season) + "): Pass Types", y=1.075)
    ax[1].axis('equal')
    legend_labels2 = [f'{label}: {autotext.get_text()}' for label, autotext in zip(passing_types_categories, autotexts2)]
    ax[1].legend(wedges2, legend_labels2, title=player2_name + "'s Pass Types\n (" + player2_team + ")", loc="center left", bbox_to_anchor=(-0.45, 0.5))

    plt.tight_layout()
    plt.show()

# 8 Passing Distance
def passing_distance(fbref1, p1_name, fbref2, p2_name):
    player1_season_stats = read_player_stats(fbref1, "passing", p1_name)
    player2_season_stats = read_player_stats(fbref2, "passing", p2_name)

    player1_name = player1_season_stats.index.get_level_values("player")[0]
    player1_team = player1_season_stats.index.get_level_values("team")[0]
    player1_season = player1_season_stats.index.get_level_values("season")[0]

    player2_name = player2_season_stats.index.get_level_values("player")[0]
    player2_team = player2_season_stats.index.get_level_values("team")[0] 
    player2_season = player2_season_stats.index.get_level_values("season")[0]

    p1_90s = player1_season_stats["90s"].values[0]
    p2_90s = player2_season_stats["90s"].values[0]

    # Creating a bar chart
    fig, ax = plt.subplots(figsize=(12, 6))

    # Loop through pass types
    pass_types = ["Short", "Medium", "Long"]
    p1_color = 'red'
    p2_color = 'blue'

    p1_prog_p90 = round((player1_season_stats["PrgP"].values[0])/p1_90s)
    p1_cmp_p90 = round((player1_season_stats["Total"]["Cmp"].values[0])/p1_90s)
    p1_att_p90 = round((player1_season_stats["Total"]["Att"].values[0])/p1_90s)

    p2_prog_p90 = round((player2_season_stats["PrgP"].values[0])/p2_90s)
    p2_cmp_p90 = round((player2_season_stats["Total"]["Cmp"].values[0])/p2_90s)
    p2_att_p90 = round((player2_season_stats["Total"]["Att"].values[0])/p2_90s)

    ax.bar(0 - 0.15, p1_prog_p90, width=0.3, color=p1_color)
    ax.bar(0 - 0.15, p1_cmp_p90, width=0.3, alpha=0.125, color=p1_color)
    ax.bar(0 - 0.15, p1_att_p90, width=0.3, alpha=0.250, color=p1_color)

    ax.bar(0 + 0.15, p2_prog_p90, width=0.3, color=p2_color)
    ax.bar(0 + 0.15, p2_cmp_p90, width=0.3, alpha=0.125, color=p2_color)
    ax.bar(0 + 0.15, p2_att_p90, width=0.3, alpha=0.250, color=p2_color)

    # Calculating and formatting the completion percentage
    p1_prog_percentage = round((p1_prog_p90 / p1_att_p90) * 100)
    p2_prog_percentage = round((p2_prog_p90 / p2_att_p90) * 100)

    # Adding labels for the ratios directly above the bars
    ax.text(- 0.15, p1_att_p90 + 0.5, f"{p1_prog_p90}/{p1_att_p90} ($\\mathbf{{{p1_prog_percentage}\\%}}$)", ha='center', fontsize=8, color='black')
    ax.text(0.15, p2_att_p90 + 0.5, f"{p2_prog_p90}/{p2_att_p90} ($\\mathbf{{{p2_prog_percentage}\\%}}$)", ha='center', fontsize=8, color='black')

    for i, pass_type in enumerate(pass_types, start = 1):

        p1_cmp_value = round((player1_season_stats[pass_type]["Cmp"].values[0])/p1_90s)
        p1_att_value = round((player1_season_stats[pass_type]["Att"].values[0])/p1_90s)
        p2_cmp_value = round((player2_season_stats[pass_type]["Cmp"].values[0])/p2_90s)
        p2_att_value = round((player2_season_stats[pass_type]["Att"].values[0])/p2_90s)

        # Player 1's Values
        ax.bar(i - 0.15, p1_att_value, width=0.3, alpha=0.250, color=p1_color)
        ax.bar(i - 0.15, p1_cmp_value, width=0.3, color=p1_color)

        # Player 2's Values
        ax.bar(i + 0.15, p2_att_value, width=0.3, alpha=0.250, color=p2_color)
        ax.bar(i + 0.15, p2_cmp_value, width=0.3, color=p2_color)

        # Calculating and formatting the completion percentage
        p1_cmp_percentage = round((p1_cmp_value / p1_att_value) * 100)
        p2_cmp_percentage = round((p2_cmp_value / p2_att_value) * 100)

        # Adding labels for the ratios directly above the bars
        ax.text(i - 0.15, p1_att_value + 0.5, f"{p1_cmp_value}/{p1_att_value} ($\\mathbf{{{p1_cmp_percentage}\\%}}$)", ha='center', fontsize=8, color='black')
        ax.text(i + 0.15, p2_att_value + 0.5, f"{p2_cmp_value}/{p2_att_value} ($\\mathbf{{{p2_cmp_percentage}\\%}}$)", ha='center', fontsize=8, color='black')


    # Adding labels and title
    ax.set_ylabel("Amount of Passes (Per 90)")
    pass_types = ["Progressive" , "Short (5-15yds)", "Medium (15-30yds)", "Long (>30yds)"]
    ax.set_title(player1_name + " (" + season_display(player1_season) + ") vs " + player2_name + " (" + season_display(player2_season) + "): Pass Distance Comparison", y=1.075)
    ax.set_xticks(range(len(pass_types)))
    ax.set_xticklabels(pass_types)

    # Create a custom legend
    custom_legend = [
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_name} ({season_display(player1_season)})", markerfacecolor=p1_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player1_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p1_90s}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_name} ({season_display(player2_season)})", markerfacecolor=p2_color, markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label=f"{player2_team}"),
        plt.Line2D([0], [0], marker='s', color='w', label=f"Full 90s: {p2_90s}"),
    ]

    ax.legend(handles=custom_legend, loc='upper right')

    # Display the bar chart
    plt.tight_layout()
    plt.show()


def main():
    print('================================================================')
    # Select First Player
    firstPlayer = False
    while not firstPlayer:
        print("Chippy: Enter your first player!")
        p1_name = input("P1 - Name: ")
        if (p1_name == ""):
            p1_name = "Mesut"
            p1_league = "ENG"
            p1_year = "2017/18"
        else:
            print("\t [1] Premier League")
            print("\t [2] La Liga")
            print("\t [3] Serie A")
            print("\t [4] Bundesliga")
            print("\t [5] Ligue 1")
            p1_league = input("P1 - League: ")
            p1_year = input("P1 - Season: ")
        
        print("Chippy: Checking if player exists...")
        
        if (league_format(p1_league) and season_format(p1_year)):
            player1Name = get_player(p1_name, league_format(p1_league), season_format(p1_year))
            if (player1Name):
                print("Chippy: Found '" + player1Name + "'!")
                firstPlayer = True
            else:
                print("Chippy: '" + str(p1_name) + "' who played in '" + str(p1_league) + "' during '" + str(p1_year) + "' does not exist, try again.")
        else:
            print("Chippy: '" + str(p1_name) + "' who played in '" + str(p1_league) + "' during '" + str(p1_year) + "' does not exist, try again.")

        print('================================================================')


    # Select Second Player       
    secondPlayer = False
    while not secondPlayer:
        print("Chippy: Enter your second player!")
        p2_name = input("P2 - Name: ")
        if (p2_name == ""):
            p2_name = "De Bruyne"
            p2_league = "ENG"
            p2_year = "2022/2023"
        else:
            print("\t [1] Premier League")
            print("\t [2] La Liga")
            print("\t [3] Serie A")
            print("\t [4] Bundesliga")
            print("\t [5] Ligue 1")
            p2_league = input("P2 - League: ")
            p2_year = input("P2 - Season: ")
        
        print("Chippy: Checking if player exists...")
        
        if (league_format(p2_league) and season_format(p2_year)):
            player2Name = get_player(p2_name, league_format(p2_league), season_format(p2_year))
            if (player2Name):
                print("Chippy: Found '" + player2Name + "'!")
                secondPlayer = True
            else:
                print("Chippy: '" + str(p2_name) + "' who played in '" + str(p2_league) + "' during '" + str(p2_year) + "' does not exist, try again.")
        else:
            print("Chippy: '" + str(p2_name) + "' who played in '" + str(p2_league) + "' during '" + str(p2_year) + "' does not exist, try again.")
        
        
        print('================================================================')

    # Run while you want
    while True:
        # Which statistic?
        print("Chippy: The following stat types are available:")

        stats = {
            0: 'EXIT',
            1: 'standard',
            2: 'shooting',
            3: 'final_ball',
            4: 'goal_shot_creation',
            5: 'playmaking',
            6: 'possession',
            7: 'pass_types',
            8: 'passing_distance',
        }

        # Loop through all possible stats
        for key, value in stats.items():
            formatted_value = value.replace('_', ' ').title()
            print(f"[{key}] {formatted_value}")

        # What they choose
        stat = input("Chippy: Please select a stat type by entering a number (1-8): \n").lower()

        if stat == 'EXIT':
            break
        elif stat == '0':
            print("Chippy: I hope you enjoyed!")
            print('================================================================')
            break

        if stat.isdigit():
            stat_index = int(stat)
            if stat_index in stats:
                statistic = stats[stat_index]
                print("Chippy: Loading '" + statistic.replace('_', ' ').title() + "' for " + player1Name + " and " + player2Name + ".")
                compare_statistics(statistic, p1_name, season_format(p1_year), league_format(p1_league), p2_name, season_format(p2_year), league_format(p2_league))
                print(f"Chippy: Statistic has been assigned the value: '{statistic}'")
            else:
                print("Chippy: Invalid index, try again")

        print('================================================================')

if __name__ == '__main__':
    main()