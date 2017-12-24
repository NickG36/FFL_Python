
import file_inout
import team_list
import common_types
#import sets
import utils

def outputAttackingInfo(fixtures, results, ordered_att_summary,
                        ordered_def_summary, ranked_def_gls):
    """
    Prints a nicely formatted summary of the attacking info for each team
    """

    # TO DO: Split this fn into bits - it's too big
    print("Attacking data:")
    print(",Goals Scored,,,, 6m opp ranking, next opponents (w att rank),,,,,,, #home matches, ave op rk 3")
    print(",    10m,      *6m*,     All, Prev opp gls A last 6,,,,,,,Next opp gls A  last 6, Fixture easing")

    for i in range(0, len(ordered_att_summary), 1):
        curr_att_sum = ordered_att_summary[i]
        curr_team = curr_att_sum.team

        # TO DO: Change __str__ def for AttackingSummary and use this?
        output_str = curr_team + ","
        output_str += str(curr_att_sum.goals_scored.last10m) + ","
        output_str += str(curr_att_sum.goals_scored.last6m) + ","
        output_str += str(curr_att_sum.goals_scored.all) + ","

        this_team_results = utils.filterResByTeam(results, curr_team)

        num_opp_gls_prev_matches = 0
        num_results = len(this_team_results)

        for res_idx in range(0, 6, 1):
            curr_res = this_team_results[num_results - res_idx - 1]
            
            opposing_team = ""

            if(curr_res.home == curr_team):
                opposing_team = curr_res.away
            elif(curr_res.away == curr_team):
                opposing_team = curr_res.home
                
            # Look at curr_team's last 6 opponents and add up goals scored
            # in each of their last 6 matches
            opp_def = utils.findDefSummary(opposing_team, ordered_def_summary)
            
            # Keep interpreter happy by showing it the type of opp_def
            if isinstance(opp_def, common_types.DefensiveSummary):
                num_opp_gls_prev_matches += opp_def.goals_conceded.last6m
                
        output_str += str(num_opp_gls_prev_matches) + ","
        
        next_opp_rank = 0
        num_opponents_found = 0
        num_home_fixtures = 0
        num_opp_future_goals = 0

        num_fixtures_found = 0
        for fix_idx in range(0, len(fixtures), 1):
            if num_fixtures_found > 5:
                break

            curr_fix = fixtures[fix_idx]
            opponent = ""
            match_found = False

            if(curr_fix.home == curr_team):
                output_str += " "  + curr_fix.away + " A "
                num_home_fixtures += 1
                opponent = curr_fix.away
                match_found = True
            elif(curr_fix.away == curr_team):
                output_str += " " + curr_fix.home + " H "
                opponent = curr_fix.home
                match_found = True

            if(match_found):
                curr_rank = ranked_def_gls[opponent]
                output_str += str(curr_rank) + ", "

                if(num_opponents_found < 3):
                    next_opp_rank += curr_rank

                num_opponents_found += 1
                opp_def = utils.findDefSummary(opponent, ordered_def_summary)
                if isinstance(opp_def, common_types.DefensiveSummary):
                    conceded_last_6 = opp_def.goals_conceded.last6m
                    num_opp_future_goals += conceded_last_6
                    num_fixtures_found += 1

        output_str += str(num_opp_future_goals)
        
        fixture_easing = num_opp_future_goals - num_opp_gls_prev_matches
        output_str += ", "

        if fixture_easing > 20:
            output_str += "E "
        elif fixture_easing < -20:
            output_str += "H "
                
        output_str += str(fixture_easing) + ", " + str(num_home_fixtures) + ", "

        int_next_opp_rank = (next_opp_rank / 3.0)
        output_str += str(int_next_opp_rank) + ", "

        if int_next_opp_rank < 8:
            output_str += "H"
        elif int_next_opp_rank > 14:
            output_str += "E"
        else:
            output_str + "  "

        if( (i+1) % 4 == 0):
            output_str += "\n"

        print(output_str)
        
            
def outputDefensiveInfo(fixtures, results, ordered_att_summary,
                       ordered_def_summary, ranked_att_gls):
    """
    Prints a nicely formatted summary of the defensive info for each team
    """
    # TO DO: Split this fn into bits - it's too big
    print("Defensive data:")
    print(",Goals Conceded,,,Clean Sheets,,,, next opponents (w att rank),,,,,,, #home matches,, ave op rk 3")
    print(",    10m,      6m,     All, 10m, *6m, All, Prev opp gls A last 6,,,,,,,Next opp gls A  last 6, Fixture easing")

    for i in range(0, len(ordered_def_summary), 1):
        curr_def_sum = ordered_def_summary[i]
        curr_team = curr_def_sum.team

        # TO DO: Change __str__ def for DefendingSummary and use this?
        output_str = curr_team + ","
        output_str += str(curr_def_sum.goals_conceded.last10m) + ","
        output_str += str(curr_def_sum.goals_conceded.last6m) + ","
        output_str += str(curr_def_sum.goals_conceded.all) + ","
        output_str += str(curr_def_sum.clean_sheets.last10m) + ","
        output_str += str(curr_def_sum.clean_sheets.last6m) + ","
        output_str += str(curr_def_sum.clean_sheets.all) + ","

        this_team_results = utils.filterResByTeam(results, curr_team)

        num_opp_gls_prev_matches = 0
        num_results = len(this_team_results)

        for res_idx in range(0, 6, 1):
            curr_res = this_team_results[num_results - res_idx - 1]

            opposing_team = ""

            if(curr_res.home == curr_team):
                opposing_team = curr_res.away
            elif(curr_res.away == curr_team):
                opposing_team = curr_res.home

            # Look at curr_team's last 6 opponents and add up goals scored
            # in each of their last 6 matches
            opp_att = utils.findAttSummary(opposing_team, ordered_att_summary)
            if isinstance(opp_att, common_types.AttackingSummary):
                num_opp_gls_prev_matches += opp_att.goals_scored.last6m

        output_str += str(num_opp_gls_prev_matches) + ","

        next_opp_rank = 0
        num_opponents_found = 0
        num_home_fixtures = 0
        num_opp_future_goals = 0

        num_fixtures_found = 0
        for fix_idx in range(0, len(fixtures), 1):
            if num_fixtures_found > 5:
                break

            curr_fix = fixtures[fix_idx]
            opponent = ""
            match_found = False

            if(curr_fix.home == curr_team):
                output_str += " "  + curr_fix.away + " A "
                num_home_fixtures += 1
                opponent = curr_fix.away
                match_found = True
            elif(curr_fix.away == curr_team):
                output_str += " " + curr_fix.home + " H "
                opponent = curr_fix.home
                match_found = True

            if(match_found):
                curr_rank = ranked_att_gls[opponent]
                output_str += str(curr_rank) + ", "

                if(num_opponents_found < 3):
                    next_opp_rank += curr_rank

                num_opponents_found += 1
                opp_def = utils.findAttSummary(opponent, ordered_att_summary)
                scored_last_6 = opp_def.goals_scored.last6m
                num_opp_future_goals += scored_last_6
                num_fixtures_found += 1

        output_str += str(num_opp_future_goals)

        fixture_easing = num_opp_gls_prev_matches - num_opp_future_goals
        output_str += ", "

        if fixture_easing > 20:
            output_str += "E "
        elif fixture_easing < -20:
            output_str += "H "
                
        output_str += ", " + str(fixture_easing) + ", " + str(num_home_fixtures) + ", "

        int_next_opp_rank = (next_opp_rank / 3.0)
        output_str += str(int_next_opp_rank) + ", "

        if int_next_opp_rank < 8:
            output_str += "H"
        elif int_next_opp_rank > 14:
            output_str += "E"
        else:
            output_str + "  "

        if( (i+1) % 4 == 0):
            output_str += "\n"

        print(output_str)
                

def main():
    tl = team_list.Team_List

    fixtures = file_inout.parseFixtures()
    results = file_inout.parseResults()

    ordered_att_summary = []
    ordered_def_summary = []

    utils.getOrderedAttDefSummary(results, ordered_att_summary, ordered_def_summary)
    print("Size of ordered def sum %d " % len(ordered_def_summary) )
    # Set up ranked attacks
    ranked_attacks = {}

    rank = 1
    for curr_team_score in ordered_att_summary:
        ranked_attacks[curr_team_score.team] = rank
        rank += 1

    ranked_defences = {}

    rank = 1
    for curr_team_score in ordered_def_summary:
        ranked_defences[curr_team_score.team] = rank
        rank += 1

    outputAttackingInfo(fixtures,
                        results,
                        ordered_att_summary,
                        ordered_def_summary,
                        ranked_defences)

    outputDefensiveInfo(fixtures,
                        results,
                        ordered_att_summary,
                        ordered_def_summary,
                        ranked_attacks)


if __name__ == "__main__":
    main()
    
