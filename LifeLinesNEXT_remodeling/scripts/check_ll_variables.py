import pandas as pd
import argparse
import re
import numpy as np


parser=argparse.ArgumentParser(description="command line args")
parser.add_argument("-c", type=str, dest='codebook', required=True,\
                    help="Source file containing mapping of LL NEXT and "\
                    "TGO codebook")
parser.add_argument("-dll", type=str, dest='data_ll', required=True,\
                    help="Source file containing LL NEXT data in LL data model")

args=parser.parse_args()


def main():
    #read codebook
    template = pd.ExcelFile(args.codebook)
    codebook = template.parse()
    #adjust ll_names
    codebook = short_ll_names(codebook)
  
    ll_data = pd.read_csv(args.data_ll, sep=";")
##    ll_data = ll_data.replace(' ', np.NaN)


    compare_codebook_to_data(ll_data, codebook)


def short_ll_names(codebook):
    
    codebook['ll_name_short'] = codebook.ll_name.apply(cut_ll_name)

    return codebook


def cut_ll_name(x):
    if not pd.isna(x):
        end_prefix = x.find('_') + 1
        short_name = x[end_prefix:]
        
        return short_name
    else:
        return x


def compare_codebook_to_data(ll_data, codebook):

    for colname in codebook['ll_name_short']:
        if colname not in ll_data.columns.tolist():
            print(colname)


if __name__ == '__main__':
    main()
