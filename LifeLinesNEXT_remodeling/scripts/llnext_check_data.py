import pandas as pd
import argparse
import re
import numpy as np


parser=argparse.ArgumentParser(description="command line args")
parser.add_argument("-c", type=str, dest='codebook', required=True,\
                    help="Source file containing mapping of LL NEXT and "\
                    "TGO codebook")
parser.add_argument("-dtgo", type=str, dest='data_tgo', required=True,\
                    help="Source file containing LL NEXT data in TGO data model")
parser.add_argument("-dll", type=str, dest='data_ll', required=True,\
                    help="Source file containing LL NEXT data in LL data model")
##parser.add_argument("-out", type=str, dest='output', required=True,\
##                    help="Define filename without extension to save output")

args=parser.parse_args()


def main():
    #read codebook
    template = pd.ExcelFile(args.codebook)
    codebook = template.parse()
    #adjust ll_names
    codebook = short_ll_names(codebook)
  
    #read data in tgo model
    template = pd.ExcelFile(args.data_tgo)
    tgo_data = template.parse()

    #read data in ll model
##    template = pd.ExcelFile(args.data_ll)
##    ll_data = template.parse()
    ll_data = pd.read_csv(args.data_ll, sep=";")
    ll_data = ll_data.replace(' ', np.NaN)

    #transform data to values
    tgo_data_values = get_values(tgo_data, "tgo", codebook)
    print(tgo_data_values)
    tgo_data_values.to_excel("tgo_values.xlsx", index=None)
    ll_data_values = get_values(ll_data, "ll", codebook)
    ll_data_values.to_excel("ll_values.xlsx", index=None)
    print(ll_data_values)
    
    compare_values(tgo_data_values, ll_data_values)

    compare_codebook_to_data(ll_data, codebook)


def short_ll_names(codebook):
    
    codebook['ll_name_short'] = codebook.ll_name.apply(cut_ll_name)

    return codebook


def cut_ll_name(x):

    end_prefix = x.find('_') + 1
    short_name = x[end_prefix:]
    
    return short_name


def get_values(df, datamodel, codebook):
    df_values = pd.DataFrame()

    #define variables for different datasets 
    for col_name, col_data in df.iteritems():
        if datamodel == "tgo":
            col_name = short_col_name(col_name)
            codes = "tgo_coding"
        elif datamodel == "ll":
            codes = "ll_coding"

        
        if col_name in codebook.ll_name_short.to_list():
            idx = codebook.ll_name_short[codebook.ll_name_short == col_name].index[0]
            if not pd.isna(codebook.ll_coding[idx]):
                #get coding
##                print(codes, codebook.ll_name[idx])
                s = codebook[codes][idx]
                print(idx)
                coding = [int(num) for num in re.findall(r'\d+', s)]
                coding = codes_to_dict(coding, s)
                #transform codes to values
                col_data = col_data.apply(decode, args=(coding,))
                df_values[codebook.ll_name[idx]] = col_data
            else:
                df_values[codebook.ll_name[idx]] = col_data

    return df_values


def short_col_name(s):
    begin = s.find("_") + 1
    end = s.find(",")
    s = s[begin:end]

    return s

                
def codes_to_dict(codes, s):
    """ (list, str) -> dict
    """
    
    #get coding from string s using list of numerical codes that
    #were extracted from s (s has format '['1 = ja', '2 = nee']')
    values = []

    for c in codes:
        i = s.find(str(c))
        start = s.find('=', i) + 2
        end = s.find("'", i)
        value = s[start:end]
        values.append(value)

    coding = dict(zip(codes, values))

    return coding


def decode(x, coding):
    """ (pandas.Series, dict) -> pandas.Series

    Decode col_data according to coding dict.
    """
    if not pd.isna(x) and not x == ' ':
        x = int(x)
        x = coding[x]

    return x


def compare_values(tgo_data_values, ll_data_values):
    
    for col_name, tgo_col_data in tgo_data_values.iteritems():
        if col_name in ll_data_values.columns.to_list():
            ll_col_data = ll_data_values[col_name]
##            print(tgo_col_data.value_counts(), ll_col_data.value_counts())

##            same_values = tgo_col_data.value_counts() == ll_col_data.value_counts()
##            if not same_values.all():
##                print(col_name, same_values)
        

def compare_codebook_to_data(ll_data, codebook):

    for colname in codebook['ll_name_short']:
        if colname not in ll_data.columns.tolist():
            print(colname)


if __name__ == '__main__':
    main()
