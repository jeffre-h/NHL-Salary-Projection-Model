import pandas as pd
import sys
import os

def main(cf, hr, output):

    df1 = pd.read_csv(cf)
    df2 = pd.read_csv(hr)
    df1.rename(columns={"PLAYER": "player"}, inplace=True)
    df2.rename(columns={"Player": "player"}, inplace=True)

    combined = pd.merge(df2, df1, on="player", how="inner")


    # output
    if ("1819_" in cf):
        if ("cf_g" in cf):
            g = os.path.join(output, "g1819.csv")
            combined.to_csv(g, index=False)
        else:
            s = os.path.join(output, "s1819.csv")
            combined.to_csv(s, index=False)

    elif ("1920_" in cf):
        if ("cf_g" in cf):
            g = os.path.join(output, "g1920.csv")
            combined.to_csv(g, index=False)
        else:
            s = os.path.join(output, "s1920.csv")
            combined.to_csv(s, index=False)
            
    elif ("2021_" in cf):
        if ("cf_g" in cf):
            g = os.path.join(output, "g2021.csv")
            combined.to_csv(g, index=False)
        else:
            s = os.path.join(output, "s2021.csv")
            combined.to_csv(s, index=False)
            
    elif ("2122_" in cf):
        if ("cf_g" in cf):
            g = os.path.join(output, "g2122.csv")
            combined.to_csv(g, index=False)
        else:
            s = os.path.join(output, "s2122.csv")
            combined.to_csv(s, index=False)
            
    elif ("2223_" in cf):
        if ("cf_g" in cf):
            g = os.path.join(output, "g2223.csv")
            combined.to_csv(g, index=False)
        else:
            s = os.path.join(output, "s2223.csv")
            combined.to_csv(s, index=False)
            
    else:
        print("invalid input ...")
        return




# GOALIES

# python3 02-combine_data.py cleaned/2018-2019/1819_cf_g.csv cleaned/2018-2019/1819_hr_g.csv combined
# python3 02-combine_data.py cleaned/2019-2020/1920_cf_g.csv cleaned/2019-2020/1920_hr_g.csv combined
# python3 02-combine_data.py cleaned/2020-2021/2021_cf_g.csv cleaned/2020-2021/2021_hr_g.csv combined
# python3 02-combine_data.py cleaned/2021-2022/2122_cf_g.csv cleaned/2021-2022/2122_hr_g.csv combined
# python3 02-combine_data.py cleaned/2022-2023/2223_cf_g.csv cleaned/2022-2023/2223_hr_g.csv combined

# SKATERS

# python3 02-combine_data.py cleaned/2018-2019/1819_cf_s.csv cleaned/2018-2019/1819_hr_s.csv combined
# python3 02-combine_data.py cleaned/2019-2020/1920_cf_s.csv cleaned/2019-2020/1920_hr_s.csv combined
# python3 02-combine_data.py cleaned/2020-2021/2021_cf_s.csv cleaned/2020-2021/2021_hr_s.csv combined
# python3 02-combine_data.py cleaned/2021-2022/2122_cf_s.csv cleaned/2021-2022/2122_hr_s.csv combined
# python3 02-combine_data.py cleaned/2022-2023/2223_cf_s.csv cleaned/2022-2023/2223_hr_s.csv combined


if __name__ == '__main__':
    cf = sys.argv[1]
    hr = sys.argv[2]
    output = sys.argv[3]
    main(cf, hr, output)