import xlrd
import os
import pandas as pd
import argparse
from fuzzywuzzy import process
import re


parser=argparse.ArgumentParser(description="command line args")
parser.add_argument("-ll_in", type=str, dest='ll_input', required=True,\
                    help="Source file containing LL NEXT codebook")
parser.add_argument("-tgo_in", type=str, dest='tgo_input', required=True,\
                    help="Source file containing TGO NEXT codebook")
parser.add_argument("-out", type=str, dest='output', required=True,\
                    help="Define filename without extension to save output")
##parser.add_argument("--overwrite", dest='overwrite', action="store_true",\
##                    required=False, help="Output folder will be cleaned first")

args=parser.parse_args()


def main():
    #read ll_next codebook
    ll_sh = read_sheet(args.ll_input, 'LifeLines NEXT ')

    #read variable name, data type and question and store in df
    matching_df = extract_ll_data(ll_sh)
    
    #read tgo_next codebook
    tgo_sh = read_sheet(args.tgo_input, 'TGO NEXT')

    #extract all possible tgo questions and
    #extract possible variable names associated with strings in tgo_df
    tgo_df = extract_tgo_data(tgo_sh)
    
    #match questions
    matching_df = match_questions(matching_df, tgo_df)

    #get names and types for matched tgo questions
    matching_df = get_tgo_names_types(matching_df, tgo_df)

    #save in Excel
    matching_df.to_excel(args.output + '.xlsx', index=None)

    
def read_sheet(excel_file, name_codebook):
    #open workbook by name and sheet by index
    wb = xlrd.open_workbook(excel_file)
    sheet = wb.sheet_by_index(0)
    print('Read ' + name_codebook + 'codebook.')

    return sheet


def extract_ll_data(ll_sh):
    #create empty df
    df = pd.DataFrame(columns=['ll_name', 'll_type', 'll_question', \
                               'll_coding'])

    #find index of first variable name ('PID')
    for i in range(25):
        if ll_sh.cell_value(i, 0) == 'PID':
            idx_1st_var = i

    idx = 0
    for i in range(idx_1st_var, ll_sh.nrows):
        #variable description starts with var_name in sheet column index 0
        if not ll_sh.cell_value(i, 0) == '':
            
            #store variables saved in previous iterations in df
            #except for first round of iterations           
            if not i == idx_1st_var:
                if ll_coding == ['']:
                    ll_coding = ''
                df.loc[idx] = [ll_name, ll_type, ll_question, ll_coding]
                idx += 1

            #read variable name, data type and question
            ll_name = ll_sh.cell_value(i, 0)
            ll_type = ll_sh.cell_value(i, 1)
            ll_question = ll_sh.cell_value(i, 5)

            #clean question
            ll_question = clean_ll_question(ll_question)

            #get first code and value and save in list
            ll_coding = []
            if ll_type == 'tinyint' and not ll_sh.cell_value(i, 6) == '':
                coding = clean_label(ll_sh.cell_value(i, 6))
                ll_coding.append(coding)
            else:
                ll_coding = ''

        #get remaining codes and values and save in list
        if ll_sh.cell_value(i, 0) == '' and ll_type == 'tinyint'\
           and not ll_sh.cell_value(i, 6) == '':
            coding = clean_label(ll_sh.cell_value(i, 6))
            ll_coding.append(coding)        

    return df


def clean_ll_question(question):
    #remove html coding
    question = question.replace('<em>', '')
    question = question.replace('</em>', '')
    question = question.replace('<strong>', '')
    question = question.replace('</strong>', '')
    question = question.replace('<u>', '')
    question = question.replace('</u>', '')
    question = question.replace('<br>', ' ')
    question = question.replace('<sup>', ' ')
    question = question.replace('</sup>', ' ')

    #remove non-breaking spaces
    question = question.replace(u"\u00A0", " ")
    #lower case
    question = question.lower()
    
    #remove text between brackets and brackets themselves
    if '(' in question:
        question = question[:question.find('(')] + question[question.find(')')+1:]
    #again
    if '(' in question:
        question = question[:question.find('(')] + question[question.find(')')+1:]
    
    #remove trailing white space
    question = question.rstrip()
        
    return question


def extract_tgo_data(tgo_sh):
    #extract data from 
    df = pd.DataFrame(columns=['tgo_name', 'tgo_type', 'tgo_question', \
                               'tgo_coding'])

    idx = 0
    df, idx = extract_1st_col(df, tgo_sh, idx)
    df.to_excel("tgo_data_1stcol.xlsx")
    df = extract_4th_col(df, tgo_sh, idx)
    df.to_excel("tgo_data_4thcol.xlsx")
    
    return df


def extract_1st_col(df, tgo_sh, idx):
    #extract all possible questions and associated variables
    #from first column of tgo sheet and return in df
    for i in range(tgo_sh.nrows - 1):
        tgo_question = clean_tgo_question_1(tgo_sh.cell_value(i, 0))
        if not tgo_question == '':
            tgo_name = tgo_sh.cell_value(i+1, 1)
            tgo_type = tgo_sh.cell_value(i+1, 2)
            tgo_coding = ''

            if tgo_type == 'int':
                tgo_coding = []
                for j in range(1, 30):
                    if not tgo_sh.cell_value(i+1+j, 2) in ['', 'varchar',\
                                                           'blob', 'int']:
                        label = clean_label(tgo_sh.cell_value(i+1+j, 2))
                        value = tgo_sh.cell_value(i+1+j, 3)
                        code = label + ' = ' + value                               
                        tgo_coding.append(code)
                    else:
                        break

            #store in df
            df.loc[idx] = [tgo_name, tgo_type, tgo_question, tgo_coding]
            idx += 1

    return df, idx


def extract_4th_col(df, tgo_sh, idx):

    #extract all possible questions and associated variables
    #from fourth column and store in df
    for i in range(tgo_sh.nrows - 1):
        tgo_question = clean_tgo_question_2(tgo_sh.cell_value(i, 3))
        tgo_type = tgo_sh.cell_value(i, 2)
        if possible_question(tgo_question, tgo_type):
            tgo_name = tgo_sh.cell_value(i, 1)
            tgo_coding = ''

            if tgo_type == 'int':
                tgo_coding = []
                for j in range(1, 30):
                    if not tgo_sh.cell_value(i+j, 2) in ['', 'varchar',\
                                                           'blob', 'int']:
                        label = clean_label(tgo_sh.cell_value(i+j, 2))
                        value = tgo_sh.cell_value(i+j, 3)
                        code = label + ' = ' + value                               
                        tgo_coding.append(code)
                    else:
                        break

            #store in df
            df.loc[idx] = [tgo_name, tgo_type, tgo_question, tgo_coding]
            idx += 1


    return df


def clean_tgo_question_1(question):
    #remove non-breaking spaces
    question = question.replace(u"\u00A0", " ")
    #lower case
    question = question.lower()

    #remove text between brackets and brackets themselves
    if '(' in question:
        question = question[:question.find('(')] + question[question.find(')')+1:]

    if '(' in question:
        question = question[:question.find('(')] + question[question.find(')')+1:]

    return question


def clean_tgo_question_2(question):
    #remove non-breaking spaces
    question = question.replace(u"\u00A0", " ")
    #lower case
    question = question.lower()
    #delete numbers at end of string
    question = re.sub(r'\d+$', '', question)

    return question


def possible_question(question, var_type):
    #list of answers, not questions
    answers = ['Ja', 'Nee', 'ja', 'nee', 'quoted', 'not quoted']

    #questions are not empty strings, numeric or in answers list and
    #are associated with a valid var type
    if not question == '' and not question.isnumeric()\
       and not question in answers and valid_type(var_type):
        return True
    else:
        return False


def valid_type(var_type):
    #return whether var_type is a valid type
    valid_type = ['int', 'blob', 'varchar']

    return var_type in valid_type


def clean_label(label):
    #return cleaned label
    label = label.replace(u"\u00A0", " ")
    label = label.replace("<br>", " ")

    return label


def match_questions(matching_df, tgo_df):
    #add new columns for tgo_data
    matching_df['tgo_question'] = ''
    matching_df['matching_score'] = '' 

    tgo_strings = tgo_df['tgo_question'].to_list()
    
    for i in range(len(matching_df)):
        ll_question = matching_df['ll_question'][i]

        #find best match using fuzzywuzzy and store in df
        match = process.extractOne(ll_question, tgo_strings)
        if match[1] >= 90:
            matching_df['tgo_question'][i] = match[0]
            matching_df['matching_score'][i] = match[1]
                
    return matching_df


def get_tgo_names_types(matching_df, tgo_df):
    #add new columns for tgo_data
    matching_df['tgo_name'] = ''
    matching_df['tgo_type'] = ''
    matching_df['tgo_coding'] = ''

    #iterate over matched tgo questions in matching_df
    for i in range(len(matching_df)):
        if not pd.isna(matching_df['tgo_question'][i]):
            matched_tgo_question = matching_df['tgo_question'][i]
            #find tgo question in tgo_df and get associated var type and name
            for j in range(len(tgo_df)):
                if tgo_df['tgo_question'][j] == matched_tgo_question:
                    matching_df['tgo_name'][i] = tgo_df['tgo_name'][j]
                    matching_df['tgo_type'][i] = tgo_df['tgo_type'][j]
                    matching_df['tgo_coding'][i] = tgo_df['tgo_coding'][j]
           
    return matching_df 



if __name__ == '__main__':
    main()
