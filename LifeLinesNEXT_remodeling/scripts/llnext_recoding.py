##import xlrd
##import os
import pandas as pd
import argparse
##from fuzzywuzzy import process
import re
import numpy as np


parser=argparse.ArgumentParser(description="command line args")
parser.add_argument("-c", type=str, dest='codebook', required=True,\
                    help="Source file containing mapping of LL NEXT and "\
                    "TGO codebook")
parser.add_argument("-d", type=str, dest='data', required=True,\
                    help="Source file containing LL NEXT data")
parser.add_argument("-out", type=str, dest='output', required=True,\
                    help="Define filename without extension to save output")

args=parser.parse_args()


def main():
    #read codebook
    template = pd.ExcelFile(args.codebook)
    codebook = template.parse()

    #adjust ll_names
    codebook = short_ll_names(codebook)

    #read data from LL NEXT questionnaires
##    template = pd.ExcelFile(args.data)
##    ll_data = template.parse()  
    ll_data = pd.read_csv(args.data, sep=';')
    ll_data = ll_data.replace(' ', np.NaN)
    
    #change data according to codebook
    tgo_data = remodel(ll_data, codebook)

    #save to excel
    tgo_data.to_excel(args.output + '.xlsx', index=None)


def short_ll_names(codebook):
    
    codebook['ll_name_short'] = codebook.ll_name.apply(cut_ll_name)

    return codebook


def cut_ll_name(x):

    if not pd.isna(x):

        end_prefix = x.find('_') + 1
        short_name = x[end_prefix:]
        
        return short_name

    return x
   

def remodel(ll_data, codebook):
    #make new df for tgo_modeled data
    tgo_data = pd.DataFrame()

    #make lists for 'not_present'
    not_in_ll = []
    not_in_tgo = []
    
    for col_name, col_data in ll_data.iteritems():
        if col_name in codebook.ll_name_short.to_list():
            idx = codebook.ll_name_short[codebook.ll_name_short == col_name].index[0]

            #if tgo_name is not_present, save ll_name in list
            if codebook.tgo_name[idx] == 'not_present':
                not_in_tgo.append(codebook.ll_name[idx])
            
            #if ll and tgo data are of type str data can be copied
            elif codebook.ll_type[idx] in ['int', 'varchar', 'tinyint', 'smallint', 'datetime'] and \
               codebook.tgo_type[idx] in ['varchar', 'blob']:
                    tgo_data = copy_data(col_data, codebook, idx, tgo_data)

            #if ll data is of type tinyint and tgo data of type int
            elif codebook.ll_type[idx] == 'tinyint' and \
               codebook.tgo_type[idx] == 'int':
                tgo_data = coding(col_name, col_data, codebook, idx, tgo_data)

            else:
                print("Variable not recoded: " + str(idx) + " " + col_name)

        else:
            print("Variable not in LL/combined codebook:" + col_name)

    print("Variable not found in TGO: " + str(not_in_tgo))
       
    return tgo_data    
    

def coding(col_name, col_data, codebook, idx, tgo_data):
        
    #if ll and tgo coding are the same data can be copied
    if codebook.ll_coding[idx] == codebook.tgo_coding[idx]:
        tgo_data = copy_data(col_data, codebook, idx, tgo_data)

    else:
##        print(idx) # to check whether values are consistent        
        tgo_data = check_coding(col_name, col_data, codebook, idx, tgo_data)
        
    return tgo_data
        

def copy_data(col_data, codebook, idx, tgo_data):
    
    tgo_data[codebook.ll_name[idx] + ', ' + codebook.tgo_name[idx]] = col_data

    return tgo_data


def check_coding(col_name, col_data, codebook, idx, tgo_data):

    #extract codes from ll_codes in dict
    s = codebook.ll_coding[idx]
    ll_coding = [int(num) for num in re.findall(r'\d+', s)]
##    print(ll_coding)
    ll_coding = codes_to_dict(ll_coding, s)

    #extract codes from tgo_codes in dict
    s = codebook.tgo_coding[idx]
    tgo_coding = [int(num) for num in re.findall(r'\d+', s)]
    tgo_coding = codes_to_dict(tgo_coding, s)

##    print(ll_coding, tgo_coding)

    #decode data according to ll_coding
    col_data = col_data.apply(decode, args=(ll_coding,))
    
    #recode data according to tgo_coding
    col_data = col_data.apply(recode, args=(tgo_coding,))

    tgo_data[codebook.ll_name[idx] + ', ' + codebook.tgo_name[idx]] = col_data

    return tgo_data


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


def decode(x, ll_coding):
    """ (pandas.Series, dict) -> pandas.Series

    Decode col_data according to ll_coding.
    """
    if not pd.isna(x):
        x = int(x)
        x = ll_coding[x]

    return x


def recode(x, tgo_coding):
    """ (pandas.Series, dict) -> pandas.Series

    Recode col_data according to tgo_coding.
    """
    if not pd.isna(x) and not x == ' ':
        x = list(tgo_coding.keys())[list(tgo_coding.values()).index(x)]

    return x


if __name__ == '__main__':
    main()
