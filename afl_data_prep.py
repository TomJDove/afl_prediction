import pandas as pd

def processAFLData(source):

    # Read CSV and convert date to the correct format
    columns = ["Game", "Season", "Date", "Round", "Home_Team", "Home_Points", "Away_Team", "Away_Points"]
    afl_df = pd.read_csv(source, usecols = columns)
    afl_df["Date"] = pd.to_datetime(afl_df["Date"])

    # Add a column which says whether the home or away team won (or a draw)
    afl_df["Winner"] = "Home"
    afl_df.loc[afl_df["Home_Points"] < afl_df["Away_Points"], "Winner"] = "Away"
    afl_df.loc[afl_df["Home_Points"] == afl_df["Away_Points"], "Winner"] = "Draw"

    # Create new dataframe 'teams_df', containing the match data for individual teams.
    # Start by getting the home teams.
    homeCols = ["Game", "Season", "Date", "Round", "Home_Team", "Home_Points", "Away_Points"]
    colNames = {"Home_Team":"Team", "Home_Points":"PointsBy", "Away_Points":"PointsAgainst"}
    home_df = afl_df[homeCols].rename(columns = colNames)
    home_df["Home/Away"] = "Home"
    home_df["Winner"] = afl_df["Winner"]

    # Now get the away teams and add it to the dataframe
    awayCols = ["Game", "Season", "Date", "Round", "Away_Team", "Away_Points", "Home_Points"]
    colNames = {"Away_Team":"Team", "Away_Points":"PointsBy", "Home_Points":"PointsAgainst"}
    away_df = afl_df[awayCols].rename(columns = colNames)
    away_df["Home/Away"] = "Away"
    away_df["Winner"] = afl_df["Winner"]

    # Join home and away teams together and sort by date
    teams_df = pd.concat([home_df, away_df]).sort_values(by = "Date", ignore_index=True)

    # Add a column which gives the performance score for the team's game
    # Two points for a win, one for a draw, and none for a loss
    teams_df['Performance'] = 2*(teams_df['Home/Away'] == teams_df["Winner"]) + (teams_df['Home/Away'] == "Draw")

    # Calculate the statistics, starting with the ones that are based on the current season.
    seasons = teams_df.groupby(['Team', 'Season'])
    teams_df['SeasonPointsBy'] = seasons['PointsBy'].cumsum() - teams_df['PointsBy']
    teams_df['SeasonPointsAgainst'] = seasons['PointsAgainst'].cumsum() - teams_df['PointsAgainst']  
    teams_df['SeasonPerformance'] = seasons['Performance'].cumsum() - teams_df['Performance']

    # Relative ranking of team by performance in season (higher rank means better performance).
    roundGroups = teams_df.groupby(['Season', 'Round'])
    teams_df['Ranking'] = roundGroups['SeasonPerformance'].rank("dense")

    # Now the stats that only depend on the team
    teamGroups = teams_df.groupby(['Team'])

    # Average points by, points against, and performance for a team in the last n=1...5 games
    for n in range(1,6):
        teams_df[('PointsBy_Last_' + str(n))] = teamGroups['PointsBy'].transform(lambda x: x.rolling(n,1).mean().shift())
        teams_df[('PointsAgainst_Last_' + str(n))] = teamGroups['PointsAgainst'].transform(lambda x: x.rolling(n,1).mean().shift())
        teams_df[('Performance_Last_' + str(n))] = teamGroups['Performance'].transform(lambda x: x.rolling(n,1).mean().shift())

    # Put the data back together so that each row corresponds to a game with a home and away team
    teams_df = teams_df.drop(columns = ['PointsAgainst', 'Performance', 'PointsBy'])

    # Get the columns that we keep and the ones we'll take the differences of
    unchangedCols = ['Game', 'Season', 'Date', 'Round', 'Winner', 'Home/Away', 'Team']
    diffCols = [name for name in teams_df.columns if name not in unchangedCols]

    # Get the home teams
    matchStats = teams_df[teams_df['Home/Away'] == 'Home'].drop(columns = ['Home/Away'])
    matchStats = matchStats.rename(columns = {'Team':'HomeTeam'})

    # Get the away teams
    awayStats = teams_df[teams_df['Home/Away'] == 'Away'].drop(columns = ['Home/Away'])

    # Add the away team names
    matchStats.insert(5, "AwayTeam", awayStats['Team'].to_numpy())

    # Subtract the away team stats from the home team stats
    matchStats[diffCols] = matchStats[diffCols] - awayStats[diffCols].to_numpy()

    return matchStats

afl_stats = processAFLData('afl_matches.csv')
afl_stats.to_csv('afl_stats2.csv', index=False)


