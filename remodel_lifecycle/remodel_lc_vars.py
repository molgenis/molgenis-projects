import pandas as pd
import os
import shutil

def main():
    #read source files, 'old' lifecycle variables
    variables = pd.read_csv('./src/Variable.csv')
    values = pd.read_csv('./src/Code.csv')
    topics = pd.read_csv('./src/Topic.csv')

    #add keywords to keywords table
    keywords = generate_keywords(topics)

    #remodel to emx2 Cohort Catalogue model
    remodeled_variables = remodel_variables(variables, keywords)
    variable_values = get_variables_values(remodeled_variables, values) 

    #add repeated variables
    repeated_variables = add_repeats(remodeled_variables)

    #delete temporary codelist and repeats columns
    remodeled_variables = remodeled_variables.drop(['temp_code_list',
                                                    'temp_repeats'], axis=1)

    #copy tables in catalogue_emx2 to output folder
    source_dir = './catalogue_emx2/'
    target_dir = './output/'
    file_names = os.listdir(source_dir)

    for file in file_names:
        shutil.copy(os.path.join(source_dir, file), target_dir)

    #write to file
    remodeled_variables.to_csv('./output/Variables.csv', index=False)
    variable_values.to_csv('./output/VariableValues.csv', index=False)
    keywords.to_csv('./output/Keywords.csv', index=False)
    repeated_variables.to_csv('./output/RepeatedVariables.csv', index=False)

    #if output.zip already exists in ./output, delete it
    if os.path.exists('./output/output.zip'):
        os.remove('./output/output.zip')
    #zip output
    shutil.make_archive('output', 'zip', './output/')    
    #move output.zip to folder ouptut
    shutil.move('output.zip', './output')
    
    
def remodel_variables(variables, keywords):
    #read target model
    remodeled_variables = pd.read_csv('./target/Variables.csv', nrows=0)

    #remodel existing information
    remodeled_variables['name'] = variables['name']
    remodeled_variables['label'] = variables['label']
    remodeled_variables['format'] = variables['format']
    remodeled_variables['keywords_id'] = variables['topic']
    remodeled_variables['description'] = variables['description']
    remodeled_variables['unit'] = variables['unit']
    remodeled_variables['temp_code_list'] = variables['codeList']
    remodeled_variables['temp_repeats'] = variables['collectionEvent']

    #add '_0' to names of repeated variables
    remodeled_variables.loc[:, 'name'] = remodeled_variables.apply(lambda x: add_appendix(x['name'], x['temp_repeats']), axis=1)
    
    #write new information
    remodeled_variables['release.resource'] = 'LifeCycle'
    remodeled_variables['release.version'] = '1.0.0'
    remodeled_variables['table'] = 'core'

    #get keyword labels instead of ids
    remodeled_variables = get_keyword_labels(remodeled_variables, keywords)

    return remodeled_variables


def add_appendix(name, repeat):
    #define irregular repeats
    irregular_repeats = ['famsize_child', 'famsize_adult', 'edu_f1_fath', 'edu_f2_fath',
                         'fam_splitup', 'occup_f1_fath', 'occup_f2_fath', 'occupcode_f1_fath',
                         'occupcode_f2_fath', 'mental_exp','smk_exp', 'height_age', 'weight_age']
    
    #add "_0" to variable name for repeated variables
    if repeat in ['year', 'month', 'week'] and name not in irregular_repeats:
        name_0 = name + "_0"
        return name_0
    elif name in irregular_repeats:
        name0 = name + "0"
        return name0
    elif repeat == 'trimester':
        name_t1 = name + "1"
        return name_t1
    else:
        return name


def get_variables_values(remodeled_variables, values):
    #create new df
    var_values = pd.read_csv('./target/VariableValues.csv', nrows=0)

    #for categorical variables get values from values df and write to new df
    i = 0
    for data_type in remodeled_variables['format']:
        if data_type == 'categorical':
            j = 0
            for code_list in values['codeList']:
                if code_list == remodeled_variables.loc[i, 'temp_code_list']:
                    var_values.loc[j, 'variable.name'] = remodeled_variables['name'][i]
                    var_values.loc[j, 'value'] = values['value'][j]
                    var_values.loc[j, 'label'] = values['label'][j]
                    var_values.loc[j, 'order'] = values['order'][j]
                j+=1
        i+=1
    
    var_values['release.resource'] = 'LifeCycle'
    var_values['release.version'] = '1.0.0'
    var_values['variable.table'] = 'core'
    
    return var_values


def generate_keywords(topics):
    keywords = topics.rename(columns={"label": "name",
                                      "name": "definition",
                                      "parentTopicLabel": "parent"})

    return keywords


def get_keyword_labels(remodeled_variables, keywords):
    #rename and drop columns to be able to merge
    keywords = keywords.rename(columns={"definition": "keywords_id",
                                       "name": "keywords_label"})

    keywords = keywords.drop(['parent', 'order'], axis=1)
    
    #merge remodeled_variables and keywords dfs on 'keywords' (id/name)
    merged = pd.merge(remodeled_variables, keywords, on='keywords_id', how='left')

    #drop and rename columns
    merged = merged.drop(['keywords_id', 'keywords'], axis=1)
    merged = merged.rename(columns={'keywords_label': 'keywords'})
    
    return merged


def add_repeats(remodeled_variables):
    repeated_variables = pd.read_csv('./target/RepeatedVariables.csv', nrows=0)
    
    i = 0 #iterate over variables in remodeled_variables
    row = 0 #iterator to count at which index to add repeated variable
    for repeat in remodeled_variables['temp_repeats']:

        #when yearly repeated add 17 repeats
        if repeat == 'year':
            for j in range(1, 18):
                repeated_variables.loc[row, 'table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'name'] = remodeled_variables['name'][i][:-1] + str(j)
                repeated_variables.loc[row, 'isRepeatOf.table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'isRepeatOf.name'] = remodeled_variables['name'][i]
                row+=1
        #when monthly repeated add 215 repeats
        elif repeat == 'month':
            for j in range(1, 216):
                repeated_variables.loc[row, 'table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'name'] = remodeled_variables['name'][i][:-1] + str(j)
                repeated_variables.loc[row, 'isRepeatOf.table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'isRepeatOf.name'] = remodeled_variables['name'][i]
                row+=1
        #when weekly repeated add 42 repeats #NEEDS CHECK
        elif repeat == 'week':
            for j in range(1, 43):
                repeated_variables.loc[row, 'table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'name'] = remodeled_variables['name'][i][:-1] + str(j)
                repeated_variables.loc[row, 'isRepeatOf.table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'isRepeatOf.name'] = remodeled_variables['name'][i]
                row+=1
        #when trimesterly repeated add 2 repeats
        elif repeat == 'trimester':
            for j in range(2, 4):
                repeated_variables.loc[row, 'table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'name'] = remodeled_variables['name'][i][:-1] + str(j)
                repeated_variables.loc[row, 'isRepeatOf.table'] = remodeled_variables['table'][i]
                repeated_variables.loc[row, 'isRepeatOf.name'] = remodeled_variables['name'][i]
                row+=1
        i+=1

    repeated_variables['release.resource'] = 'LifeCycle'
    repeated_variables['release.version'] = '1.0.0'
    
    return repeated_variables

    

if __name__ == '__main__':
    main()


    
