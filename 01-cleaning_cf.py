import pandas as pd
import sys
import os


# salary caps for different years
s18_19 = 79500000 
s20_to_22 = 81500000
s22_23 = 82500000

# helper functions to quantify attributes
def signing_convert(x):
    if x =="RFA":
        return 0
    elif x == "UFA":
        return 1
    return None

def hand_convert(x):
    if x=='Left':
        return 0
    elif x=='Right':
        return 1
    
def main(input, output):

    # load raw data
    cf = pd.read_csv(input, encoding='latin-1')

    # formatting & reset index
    cf['PLAYER'] = cf['PLAYER'].str.replace(r'^\d+\. ', '', regex=True)
    cf.set_index("PLAYER", inplace=True)

    # quantify attributes
    cf['SIGNING'] = cf['SIGNING'].map(signing_convert)
    cf['HANDED'] = cf['HANDED'].map(hand_convert)

    # quantify draft position, if undrafted -> NaN we then replace with 300 
    # https://en.wikipedia.org/wiki/NHL_Entry_Draft, most amount of players ever drafted in one year is 293
    cf['DRAFTED'] = cf['DRAFTED'].str.extract(r'(\d+)')
    cf['DRAFTED'].fillna(300, inplace= True)

    # fix cap hit % + drop clauses
    cf = cf.drop(columns = ['CAP HIT %', 'CLAUSE'])


    if ("1819" in input):
        cf['CAP_HIT_%'] = cf['CAP HIT'] / s18_19

    elif ("1920" in input or "2021" in input or "2122" in input):
        cf['CAP_HIT_%'] = cf['CAP HIT'] / s20_to_22

    elif ("2223" in input):
        cf['CAP_HIT_%'] = cf['CAP HIT'] / s22_23
    
    else: 
        print("invalid input file ...")
        return

    # split dataframe into 2: skaters & goalies
    s = cf[ cf['ixG'] != '-' ]
    s = s.drop(columns = ['GA60','xGA60','GSAx60'])

    g = cf[ cf['ixG'] == '-' ]
    g = g.drop(columns = ['ixG','iSh','iCF','iFF','ixG60','iSh60','iCF60','iFF60','SF','SA','SF%','CF','CA','CF%','FF','FA','FF%','xGF','xGA','xGF%'])

    # combine data & output
    if ("1819" in input):
        s_out = os.path.join(output, "1819_cf_s.csv")
        g_out = os.path.join(output, "1819_cf_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)
    elif ("1920" in input):
        s_out = os.path.join(output, "1920_cf_s.csv")
        g_out = os.path.join(output, "1920_cf_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)
    elif ("2021" in input):
        s_out = os.path.join(output, "2021_cf_s.csv")
        g_out = os.path.join(output, "2021_cf_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)
    elif ("2122" in input):
        s_out = os.path.join(output, "2122_cf_s.csv")
        g_out = os.path.join(output, "2122_cf_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)
    else:
        s_out = os.path.join(output, "2223_cf_s.csv")
        g_out = os.path.join(output, "2223_cf_g.csv")
        s.to_csv(s_out)
        g.to_csv(g_out)       



# run script for each hockey season 

# python3 01-cleaning_cf.py raw/2018-2019/capfriendly1819.csv cleaned/2018-2019
# python3 01-cleaning_cf.py raw/2019-2020/capfriendly1920.csv cleaned/2019-2020
# python3 01-cleaning_cf.py raw/2020-2021/capfriendly2021.csv cleaned/2020-2021
# python3 01-cleaning_cf.py raw/2021-2022/capfriendly2122.csv cleaned/2021-2022
# python3 01-cleaning_cf.py raw/2022-2023/capfriendly2223.csv cleaned/2022-2023

if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]
    main(input, output)
