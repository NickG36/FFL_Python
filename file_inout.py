import common_types

def parseFixtures():
    """
    parseFixtures will read through all the fixtures in the csv file and
    return a list of all the fixtures found there
    """

    result = []
    f = open("Fixtures1718.csv", "rU")

    curr_line = f.readline()

    while(curr_line != ""):
        if(curr_line[0:2] == ",,"):
            date_str = curr_line[2:-1]
            #print("Date:'%s'." % date_str)            
        else:
            string_list = curr_line.split(",")

            home_team = string_list[0]
            full_away_team = string_list[1]

            # Remove newline:
            away_team = full_away_team[0:-1]
            #print("Home:'%s', away:'%s'." % (home_team, away_team) )            

            curr_fix = common_types.Fixture(home_team, away_team)
            result.append(curr_fix)

        curr_line = f.readline()

    f.close()
    return result

def parseResults():
    """
    parseResults will look in the results csv file and return a list of
    all the fixtures found there
    """

    result =[]
    f = open("Results1718.csv", "rU")
    
    curr_line = f.readline()

    while(curr_line != ""):
        if(curr_line[0:2] == ",,"):
            date_str = curr_line[2:-1]
        else:
            string_list = curr_line.split(",")

            home_team = string_list[0]
            home_gls = int(string_list[1])
            away_gls = int(string_list[2])
            away_team = string_list[3]

            curr_fix = common_types.Match(home_team, away_team,
                                          home_gls, away_gls)
            result.append(curr_fix)

        curr_line = f.readline()
        
    f.close()

    return result
