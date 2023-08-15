import pandas as pd
import sys
import os


# min games played/started filter
min_gp = 20
min_gs = 10
covid_min_gp = 14
covid_min_gs = 6 

# helper function to quantify ATOI
def atoi_convert(x):
    time = x.split(":")
    minutes = int(time[0]) * 60
    seconds = int(time[1])
    return minutes + seconds


def main(input_s, input_g, output):
    
    # load data
    s = pd.read_csv(input_s, skiprows=1)
    g = pd.read_csv(input_g, skiprows=1)

    s['ATOI'] = s['ATOI'].map(atoi_convert)

    # cleaning skater data
    if ("2021" in input_s):
        s = s[ s['GP'] > covid_min_gp].copy()
    else:
        s = s[ s['GP'] > min_gp].copy()

    s.set_index("Player", inplace=True)
    s["FO%"].fillna(0, inplace=True) # filling in NaN faceoff values to 0%
    s = s.drop(columns = ['Tm', '-9999'])


    # cleaning goalie data
    if ("2021" in input_g):
        g = g[ g['GS'] > covid_min_gs].copy()
    else:
        g = g[ g['GS'] > min_gs].copy()

    g.set_index("Player", inplace=True)
    g = g.drop(columns = ['Tm', 'G','A','PTS','PIM', '-9999'])
    
        
    # output
    if ("1819" in input_s):
        s_out = os.path.join(output, "1819_hr_s.csv")
        g_out = os.path.join(output, "1819_hr_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)

    elif ("1920" in input_s):
        s_out = os.path.join(output, "1920_hr_s.csv")
        g_out = os.path.join(output, "1920_hr_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)

    elif ("2021" in input_s):
        s_out = os.path.join(output, "2021_hr_s.csv")
        g_out = os.path.join(output, "2021_hr_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)

    elif ("2122" in input_s): 
        s_out = os.path.join(output, "2122_hr_s.csv")
        g_out = os.path.join(output, "2122_hr_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)

    else:
        s_out = os.path.join(output, "2223_hr_s.csv")
        g_out = os.path.join(output, "2223_hr_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)



# run script for each hockey season 

# python3 01-cleaning_hr.py raw/2018-2019/hockeyref1819.csv raw/2018-2019/hockeyref_goalie1819.csv cleaned/2018-2019
# python3 01-cleaning_hr.py raw/2019-2020/hockeyref1920.csv raw/2019-2020/hockeyref_goalie1920.csv cleaned/2019-2020
# python3 01-cleaning_hr.py raw/2020-2021/hockeyref2021.csv raw/2020-2021/hockeyref_goalie2021.csv cleaned/2020-2021
# python3 01-cleaning_hr.py raw/2021-2022/hockeyref2122.csv raw/2021-2022/hockeyref_goalie2122.csv cleaned/2021-2022
# python3 01-cleaning_hr.py raw/2022-2023/hockeyref2223.csv raw/2022-2023/hockeyref_goalie2223.csv cleaned/2022-2023

if __name__ == '__main__':
    input_s = sys.argv[1]
    input_g = sys.argv[2]
    output = sys.argv[3] 
    main(input_s, input_g, output)
