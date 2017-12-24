import common_types
import team_list
import utils

def parseResults(curr_team_res, team, attack_sum, def_sum):
    """
    Filters a team's current results to create an attacking and a defensive
    summary for the given team
    """
    num_matches = len(curr_team_res)

    for idx, val in enumerate(curr_team_res):
        curr_gls_for = 0
        curr_gls_against = 0
        curr_cln_sheets = 0

        if(val.home == team):
            curr_gls_for = int(val.home_gls)
            curr_gls_against = int(val.away_gls)

            if(val.away_gls == 0):
                curr_cln_sheets = 1

            attack_sum.goals_scored.all += curr_gls_for
            def_sum.goals_conceded.all += curr_gls_against
            def_sum.clean_sheets.all += curr_cln_sheets

            if(idx > (num_matches - 6 - 1)):
                attack_sum.goals_scored.last6m += curr_gls_for
                def_sum.goals_conceded.last6m += curr_gls_against
                def_sum.clean_sheets.last6m += curr_cln_sheets
            
            if(idx > (num_matches - 10 - 1)):
                attack_sum.goals_scored.last10m += curr_gls_for
                def_sum.goals_conceded.last10m += curr_gls_against
                def_sum.clean_sheets.last10m += curr_cln_sheets

def getOrderedAttDefSummary(results, ordered_att_summary, ordered_def_summary):
    """
    Sorts all results into separate lists for each team, ordered by ability
    """
    t1 = team_list.Team_List

    all_attacking_summaries = []
    all_defensive_summaries = []

    for team in t1.teams:
        curr_team_res = utils.filterResByTeam(results, team)

        attack_sum = common_types.AttackingSummary(team)
        def_sum = common_types.DefensiveSummary(team)
        
        utils.parseResults(curr_team_res, team, attack_sum, def_sum)

        all_attacking_summaries.append(attack_sum)
        all_defensive_summaries.append(def_sum)


    temp_ordered_att_summary = utils.orderAttSummary(all_attacking_summaries)
    temp_ordered_def_summary = utils.orderDefSummary(all_defensive_summaries)

    for att_sum in temp_ordered_att_summary:
        ordered_att_summary.append(att_sum)

    for def_sum in temp_ordered_def_summary:
        ordered_def_summary.append(def_sum)

def findDefSummary(team, ordered_def_summary):
    for def_sum in ordered_def_summary:
        if(def_sum.team == team):
            return def_sum
        
def findAttSummary(team, ordered_att_summary):
    for att_sum in ordered_att_summary:
        if(att_sum.team == team):
            return att_sum
    
def filterResByTeam(all_res, team_name):
    results = []
    for curr_res in all_res:
        if(curr_res.home == team_name):
            results.append(curr_res)

        if(curr_res.away == team_name):
            results.append(curr_res)
            
    return results


def orderAttSummary(all_att_summaries):
    changed = True

    while(changed):
        changed = False
        for idx, val in enumerate(all_att_summaries):
            if(idx < len(all_att_summaries) - 1):
               curr = all_att_summaries[idx]
               next = all_att_summaries[idx + 1]

               if(curr < next):
                   # Swap
                   all_att_summaries[idx + 1] = curr
                   all_att_summaries[idx] = next
                   changed = True
    return all_att_summaries

def orderDefSummary(all_def_summaries):
    changed = True

    while(changed):
        changed = False

        for idx, val in enumerate(all_def_summaries):
            if(idx < len(all_def_summaries) - 1):
               curr = all_def_summaries[idx]
               next = all_def_summaries[idx + 1]

               if(curr < next):
                   # Swap
                   all_def_summaries[idx + 1] = curr
                   all_def_summaries[idx] = next
                   changed = True

    return all_def_summaries
