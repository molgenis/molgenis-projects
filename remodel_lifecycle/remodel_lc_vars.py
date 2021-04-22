import pandas as pd
import os
import shutil

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

    #add keywords to keywords table
    keywords = generate_keywords(topics)

    #read formats
    formats = pd.read_csv('./target/Formats.csv')

    #write to file
    remodeled_variables.to_csv('./output/Variables.csv', index=False)
    variable_values.to_csv('./output/VariableValues.csv', index=False)
    keywords.to_csv('./output/Keywords.csv', index=False)
    formats.to_csv('./output/Formats.csv', index=False)

    #zip output
    shutil.make_archive('output', 'zip', './output/')
    shutil.move('output.zip', './output')
    
    
def remodel_variables(variables):
    #read target model
    remodeled_variables = pd.read_csv('./target/Variables.csv', index_col=0, nrows=0)

    #remodel existing information
    remodeled_variables['name'] = variables['name']
    remodeled_variables['label'] = variables['label']
    remodeled_variables['format'] = variables['format']
    remodeled_variables['keywords'] = variables['topic']
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

def generate_keywords(topics):
    keywords = topics.rename(columns={"label": "definition", "parentTopic": "parent"})
    keywords["comments"] = ""
    keywords["ontologyTermURI"] = ""

    return keywords
                    
    

if __name__ == '__main__':
    main()


    
