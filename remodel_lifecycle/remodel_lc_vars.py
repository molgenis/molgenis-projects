import pandas as pd
import os

def main():
    #read source files, 'old' lifecycle variables
    variables = pd.read_csv('./src/Variable.csv')
    values = pd.read_csv('./src/Code.csv')
    topics = pd.read_csv('./src/Topic.csv')

    #remodel to emx2 Cohort Catalogue model
    remodeled_variables = remodel_variables(variables)
    variable_values = get_variables_values(remodeled_variables, values)

    #delete temporary codelist column
    remodeled_variables = remodeled_variables.drop('temp_code_list', axis=1)

    #get keywords/topics
    remodeled_variables = get_topics(remodeled_variables, topics)

    #add keywords to keywords table
    keywords = add_keywords(remodeled_variables)

    #write to file
    remodeled_variables.to_csv('./output/Variables.csv', index=False)
    variable_values.to_csv('./output/VariableValues.csv', index=False)
    keywords.to_csv('./output/Keywords.csv', index=False)
    
    
def remodel_variables(variables):
    #read target model
    remodeled_variables = pd.read_csv('./target/Variables.csv', index_col=0, nrows=0)

    #remodel existing information
    remodeled_variables['name'] = variables['name']
    remodeled_variables['label'] = variables['label']
    remodeled_variables['format'] = variables['format']
    remodeled_variables['temp_keywords'] = variables['topic']
    remodeled_variables['temp_code_list'] = variables['codeList']
    

    #write new information
    remodeled_variables['release.resource'] = 'LifeCycle'
    remodeled_variables['release.version'] = '1.0.0'
    remodeled_variables['table'] = 'core'

    return remodeled_variables


def get_variables_values(remodeled_variables, values):
    #create new df
    var_values = pd.read_csv('./target/VariableValues.csv', index_col=0, nrows=0)

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


def get_topics(remodeled_variables, topics):
    #iterate over temp_keywords and get topic labels instead of names
    remodeled_variables = remodeled_variables.assign(keywords = '')

    i = 0
    for keyword in remodeled_variables['temp_keywords']:
        j = 0
        for name in topics['name']:
            if keyword == name:
                remodeled_variables.loc[i, 'keywords'] = topics['label'][j]
            j+=1
        i+=1

    #drop temporary column
    remodeled_variables = remodeled_variables.drop('temp_keywords', axis=1)

    return remodeled_variables

def add_keywords(remodeled_variables):
    keywords = pd.read_csv('./target/Keywords.csv')

    i = 0
    for keyword in remodeled_variables['keywords']:
        keywords.loc[i, 'name'] = keyword
        i+=1

    #delete duplicate rows 
    keywords = keywords.drop_duplicates().dropna(subset=['name'])
    
    return keywords           
                    
    

if __name__ == '__main__':
    main()


    
