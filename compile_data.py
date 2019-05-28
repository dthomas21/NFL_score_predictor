import pandas as pd
import numpy as np
import math
import sys

nflplays = sys.argv[1]
spreads = sys.argv[2]
fullgame = bool(sys.argv[3])
print(fullgame)

nfl = pd.read_csv(nflplays, low_memory=False)
spread = pd.read_csv(spreads)

print('csvs read')

teams = {"ARI": "Arizona Cardinals", "ATL": "Atlanta Falcons",
         "BAL": "Baltimore Ravens", "BUF": "Buffalo Bills",
         "CAR": "Carolina Panthers", "CHI": "Chicago Bears",
         "CIN": "Cincinnati Bengals", "CLE": "Cleveland Browns",
         "DAL": "Dallas Cowboys", "DEN": "Denver Broncos",
         "DET": "Detroit Lions", "GB": "Green Bay Packers",
         "HOU": "Houston Texans", "IND": "Indianapolis Colts",
         "JAX": "Jacksonville Jaguars", "JAC": "Jacksonville Jaguars",
         "KC": "Kansas City Chiefs", "LA": "Los Angeles Rams",
         "LAC": "Los Angeles Chargers", "MIA": "Miami Dolphins",
         "MIN": "Minnesota Vikings", "NE": "New England Patriots",
         "NO": "New Orleans Saints", "NYG": "New York Giants",
         "NYJ": "New York Jets", "OAK": "Oakland Raiders",
         "PHI": "Philadelphia Eagles", "PIT": "Pittsburgh Steelers",
         "SD": "San Diego Chargers", "SEA": "Seattle Seahawks",
         "SF": "San Francisco 49ers", "STL": "St. Louis Rams",
         "TB": "Tampa Bay Buccaneers", "TEN": "Tennessee Titans",
         "WAS": "Washington Redskins"}

"""Get desired features to include"""
nfl_teams = nfl[["Date", "GameID", "HomeTeam", "AwayTeam"]]
spread_games = list()
for game in range(len(spread["spread_favorite"])):
    if not math.isnan(spread["spread_favorite"][game]):
        if int(spread["schedule_date"][game][6:10]) >= 2009:
            spread_games.append(spread.iloc[game])
    else:
        pass
spread_games = pd.DataFrame(spread_games)

"""Clean up data to prepare for merging"""
spread_dates_list = list()
for date in spread_games["schedule_date"]:
    spread_dates_list.append(date)
for date in range(len(spread_dates_list)):
    spread_dates_list[date] = spread_dates_list[date][6:10] + "/" + \
                              spread_dates_list[date][0:2] + "/" + \
                              spread_dates_list[date][3:5]
spread_games["schedule_date"] = spread_dates_list
nfl_dates_list = list()
for date in nfl_teams["Date"]:
    nfl_dates_list.append(date.replace("-", "/"))
nfl_teams.loc[:]['Date'] = nfl_dates_list
nfl_dates_set = set()
for date in nfl_dates_list:
    nfl_dates_set.add(date)
spread_dates = set(spread_dates_list)

"""Merge data sets"""
accounted_dates = nfl_dates_set.intersection(spread_dates)
nfl_df = pd.DataFrame(list(accounted_dates), columns=["Date"])
nfl_teams = np.array(nfl_teams)
unique_games = set()
for game in nfl_teams:
    unique_games.add(tuple(game))
matched_games = set()
for game in unique_games:
    if game[0] in accounted_dates:
        matched_games.add(game)
accounted_spread_games = spread_games[["schedule_date", "team_home",
                                       "team_away", "score_home",
                                       "score_away", "team_favorite_id",
                                       "spread_favorite", "over_under_line"]]
accounted_spread_array = np.array(accounted_spread_games)
matched_scores = list()
for game in accounted_spread_array:
    for g in matched_games:
        if game[0] == g[0] and game[1] == teams[g[2]] \
                and game[2] == teams[g[3]]:
            game = tuple(game) + (g[1],)
            matched_scores.append(tuple(game))
new_df = pd.DataFrame(matched_scores, columns=["Date", "Home Team",
                                               "Away Team",
                                               "Home Score",
                                               "Away Score",
                                               "Favorite Team ID",
                                               "Spread Favorite",
                                               "Over Under",
                                               "gameid"])
new_df = new_df.set_index('gameid')


nfl = nfl.sort_values(['Date', 'GameID', 'TimeSecs'], ascending=False)
nfl = nfl[0 <= nfl.TimeSecs]
nfl.index = range(nfl.shape[0])
df = nfl

gameid = []
hometm = []
awaytm = []
homesc = []
awaysc = []
hmhalfsc = []
awhalfsc = []
ot = []
hpassgm = []
apassgm = []
hpassd = []
apassd = []
hrushgm = []
arushgm = []
hrushsd = []
arushsd = []
hairyds = [0]
hyac = [0]
hpatts = [0]
hcomp = [0]
hcpct = []
hints = [0]
hrushyds = [0]
hratts = [0]
hsacks = [0]
hsackyds = [0]
hfums = [0]
hfumlost = [0]
aairyds = [0]
ayac = [0]
apatts = [0]
acomp = [0]
acpct = []
aints = [0]
arushyds = [0]
aratts = [0]
asacks = [0]
asackyds = [0]
afums = [0]
afumlost = [0]
hmadj = 0
awadj = 0
for i in range(df.shape[0]):
    if df.qtr[i] == 4 and not df.qtr[i + 1] == 4:
        if df.qtr[i + 1] == 1:
            ot.extend([0])
        else:
            ot.extend([1])
        offscore = df.PosTeamScore[i - 1]  # score after 4 quarters
        defscore = df.DefTeamScore[i - 1]
        fgpts = 0
        if math.isnan(offscore):
            offscore = df.PosTeamScore[i]
            defscore = df.DefTeamScore[i]
            if df.FieldGoalResult[i] == 'Good':
                fgpts += 3
        if df.posteam[i] == df.HomeTeam[i]:
            if df.Touchdown[i] == 1 and not df.sp[i] == 1:
                hmadj += 6
                if df.ExPointResult[i] == 'Good':
                    hmadj += 1
                elif df.TwoPointConv[i] == 'Success':
                    hmadj += 2
            elif df.Touchdown[i] == 1 and df.sp[i] == 1:
                awadj += 6
                if df.ExPointResult[i] == 'Good':
                    awadj += 1
                elif df.TwoPointConv[i] == 'Success':
                    awadj += 2
            homesc.extend([offscore + hmadj + fgpts])
            awaysc.extend([defscore + awadj])
        else:
            if df.Touchdown[i] == 1 and not df.sp[i] == 1:
                awadj += 6
                if df.ExPointResult[i] == 'Good':
                    awadj += 1
                elif df.TwoPointConv[i] == 'Success':
                    awadj += 2
            elif df.Touchdown[i] == 1 and df.sp[i] == 1:
                hmadj += 6
                if df.ExPointResult[i] == 'Good':
                    hmadj += 1
                elif df.TwoPointConv[i] == 'Success':
                    hmadj += 2
            homesc.extend([defscore + hmadj])
            awaysc.extend([offscore + awadj + fgpts])
        hmadj = 0
        awadj = 0
    qtr = 2
    if fullgame:
        qtr = 4
    if df.qtr[i] == qtr and not df.qtr[i + 1] == qtr:
        gameid.extend([df.GameID[i]])
        hometm.extend([df.HomeTeam[i]])
        awaytm.extend([df.AwayTeam[i]])
        hcpct.extend([hcomp[-1] / hpatts[-1]])
        hpatts.append(0)
        hcomp.append(0)
        hints.append(0)
        hrushyds.append(0)
        hratts.append(0)
        hsacks.append(0)
        hsackyds.append(0)
        hfums.append(0)
        hfumlost.append(0)
        acpct.extend([acomp[-1] / apatts[-1]])
        apatts.append(0)
        acomp.append(0)
        aints.append(0)
        arushyds.append(0)
        aratts.append(0)
        asacks.append(0)
        asackyds.append(0)
        afums.append(0)
        afumlost.append(0)

        hairyds.append(0)
        aairyds.append(0)
        hyac.append(0)
        ayac.append(0)

        hpassd.append(np.std(hpassgm))
        if len(apassgm) == 0:
            apassd.append(0)
        else:
            apassd.append(np.std(apassgm))
        hpassgm = []
        apassgm = []

        hrushsd.append(np.std(hrushgm))
        arushsd.append(np.std(arushgm))
        hrushgm = []
        arushgm = []

        offscore = df.PosTeamScore[i + 1]  # halftime score
        defscore = df.DefTeamScore[i + 1]
        if df.posteam[i + 1] == df.HomeTeam[i]:
            hmhalfsc.extend([offscore + hmadj])
            awhalfsc.extend([defscore + awadj])
        else:
            hmhalfsc.extend([defscore + hmadj])
            awhalfsc.extend([offscore + awadj])
        # hmadj=0; awadj=0 #should be commented out
    if df.qtr[i] in [1, 2, 3, 4]:  # need all 4 quarters for full time score
        if df.Touchdown[i] == 1:
            j = 1
            while not isinstance(df.posteam[i + j], str):
                j += 1
            if not isinstance(df.ExPointResult[i + j], str) \
                    and not isinstance(df.TwoPointConv[i + j], str) and \
                    df['Challenge.Replay'][i] == 0:
                if df.HomeTeam[i] == df.DefensiveTeam[i]:
                    hmadj += 1
                    if df.ScoreDiff[i] == df.ScoreDiff[i + j]:
                        hmadj += 6
                else:
                    awadj += 1
                    if df.ScoreDiff[i] == df.ScoreDiff[i + j]:
                        awadj += 6
    qtrs = [1, 2]
    if fullgame:
        qtrs = [1, 2, 3, 4]
    if df.qtr[i] in qtrs:  # to be changed to [1,2]
        if df.PassAttempt[i] == 1 and not df.PlayType[i] == 'No Play' \
                and not isinstance(df.TwoPointConv[i], str):
            if df.posteam[i] == df.HomeTeam[i]:
                hpatts[-1] += 1
                if df.InterceptionThrown[i] == 1:
                    hints[-1] += 1
                elif df.PassOutcome[i] == 'Complete':
                    hairyds[-1] += df.AirYards[i]
                    hyac[-1] += df.YardsAfterCatch[i]
                    hpassgm.append(df.AirYards[i] + df.YardsAfterCatch[i])
                    hcomp[-1] += 1
            elif df.posteam[i] == df.AwayTeam[i]:
                apatts[-1] += 1
                if df.InterceptionThrown[i] == 1:
                    aints[-1] += 1
                elif df.PassOutcome[i] == 'Complete':
                    aairyds[-1] += df.AirYards[i]
                    ayac[-1] += df.YardsAfterCatch[i]
                    apassgm.append(df.AirYards[i] + df.YardsAfterCatch[i])
                    acomp[-1] += 1
        elif df.RushAttempt[i] == 1 and not df.PlayType[i] == 'No Play' \
                and not isinstance(df.TwoPointConv[i], str):
            if df.posteam[i] == df.HomeTeam[i]:
                hratts[-1] += 1
                if df['Challenge.Replay'][i] == 1:
                    hrushyds[-1] += (df.yrdline100[i] - df.yrdline100[i + 1])
                    hrushgm.append(df.yrdline100[i] - df.yrdline100[i + 1])
                else:
                    hrushyds[-1] += df['Yards.Gained'][i]
                    hrushgm.append(df['Yards.Gained'][i])
            elif df.posteam[i] == df.AwayTeam[i]:
                aratts[-1] += 1
                if df['Challenge.Replay'][i] == 1:
                    arushyds[-1] += (df.yrdline100[i] - df.yrdline100[i + 1])
                    arushgm.append(df.yrdline100[i] - df.yrdline100[i + 1])
                else:
                    arushyds[-1] += df['Yards.Gained'][i]
                    arushgm.append(df['Yards.Gained'][i])
        elif df.Sack[i] == 1:
            if df.posteam[i] == df.HomeTeam[i]:
                hsacks[-1] += 1
                hsackyds[-1] += df['Yards.Gained'][i]
            elif df.posteam[i] == df.AwayTeam[i]:
                asacks[-1] += 1
                asackyds[-1] += df['Yards.Gained'][i]
        if df.Fumble[i] == 1:
            if df.posteam[i] == df.HomeTeam[i]:
                hfums[-1] += 1
                if df.RecFumbTeam[i] == df.AwayTeam[i]:
                    hfumlost[-1] += 1
            elif df.posteam[i] == df.AwayTeam[i]:
                afums[-1] += 1
                if df.RecFumbTeam[i] == df.HomeTeam[i]:
                    afumlost[-1] += 1

hairyds = hairyds[:-1]
hyac = hyac[:-1]
aairyds = aairyds[:-1]
ayac = ayac[:-1]
hpatts = hpatts[:-1]
hcomp = hcomp[:-1]
hints = hints[:-1]
hrushyds = hrushyds[:-1]
hratts = hratts[:-1]
hsacks = hsacks[:-1]
hsackyds = hsackyds[:-1]
hfums = hfums[:-1]
hfumlost = hfumlost[:-1]
apatts = apatts[:-1]
acomp = acomp[:-1]
aints = aints[:-1]
arushyds = arushyds[:-1]
aratts = aratts[:-1]
asacks = asacks[:-1]
asackyds = asackyds[:-1]
afums = afums[:-1]
afumlost = afumlost[:-1]

wrangled = pd.DataFrame({'gameid': gameid, 'home': hometm,
                         'away': awaytm, 'homesc': homesc,
                         'awaysc': awaysc, 'hmhalfsc': hmhalfsc,
                         'awhalfsc': awhalfsc, 'ot': ot,
                         'hairyd': hairyds, 'hyac': hyac,
                         'hpassd': hpassd, 'hpatt': hpatts,
                         'hcomp': hcomp, 'hcomppct': hcpct,
                         'hint': hints, 'hryd': hrushyds,
                         'hrushsd': hrushsd, 'hratt': hratts,
                         'hsacks': hsacks, 'hsackyds': hsackyds,
                         'hfum': hfums, 'hfuml': hfumlost,
                         'aairyd': aairyds, 'ayac': ayac,
                         'apassd': apassd, 'apatt': apatts,
                         'acomp': acomp, 'acomppct': acpct,
                         'aint': aints, 'aryd': arushyds,
                         'arushsd': arushsd, 'aratt': aratts,
                         'asacks': asacks, 'asackyds': asackyds,
                         'afum': afums, 'afuml': afumlost})

if fullgame:
    htotyds = wrangled[['hairyd', 'hyac',
                        'hryd', 'hsackyds']].transpose().sum()
    atotyds = wrangled[['aairyd', 'ayac',
                        'aryd', 'asackyds']].transpose().sum()
    htos = wrangled[['hint', 'hfuml']].transpose().sum()
    atos = wrangled[['aint', 'afuml']].transpose().sum()
    wrangled['htotyds'] = htotyds
    wrangled['atotyds'] = atotyds
    wrangled['htos'] = htos
    wrangled['atos'] = atos

wrangled = wrangled.set_index('gameid')
merged = new_df.merge(wrangled, how='outer', on='gameid')

if fullgame:
    merged.to_csv('nfl_cleaned_full.csv')
else:
    valid_gameids = sys.argv[4]
    valid_gameids = pd.read_csv(valid_gameids)
    valid_gameids = valid_gameids.set_index('valid_gameids')
    merged = merged.loc[valid_gameids.index]
    # merged['Favorite Team ID'][merged['Favorite Team ID'] == 'LAR'] = 'LA'
    # merged.home[merged.home == 'JAC'] = 'JAX'
    # merged['homespread'] = merged['Spread Favorite']
    # merged.homespread[merged['Favorite Team ID']
    # != merged.home] = -merged.homespread[
    # merged['Favorite Team ID'] != merged.home]
    merged['homewin'] = merged['Home Score'] > merged['Away Score']
    merged.homewin = merged.homewin.astype(int)

    merged.to_csv('nfl_cleaned.csv')
