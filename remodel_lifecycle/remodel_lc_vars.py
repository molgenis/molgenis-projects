import pandas as pd
import os

def main():
    #read source files, 'old' lifecycle variables
    variables = pd.read_csv('./src/Variable.csv')
    values = pd.read_csv('./src/Code.csv')

    

    #remodel to emx2 Cohort Catalogue model
    remodeled_variables = remodel_variables(variables)
    variable_values = get_variables_values(remodeled_variables, values)

    #write to file
    remodeled_variables.to_csv('./output/Variables.csv', index=False)
    variable_values.to_csv('./output/VariableValues.csv', index=False)

    

def remodel_variables(variables):
    #read target model
    remodeled_variables = pd.read_csv('./target/Variables.csv', index_col=0, nrows=0)

    #remodel existing information
    remodeled_variables['name'] = variables['name']
    remodeled_variables['label'] = variables['label']
    remodeled_variables['format'] = variables['format']
    remodeled_variables['temp_code_list'] = variables['codeList']

    #write new information
    remodeled_variables['release.resource'] = 'LifeCycle'
    remodeled_variables['release.version'] = '1.0.0'
    remodeled_variables['table'] = 'core'

    return remodeled_variables


def get_variables_values(remodeled_variables, values):
    #create new df
    var_values = pd.DataFrame(columns=['release', 'variable', 'value',
                                       'label', 'order', 'isMissing',
                                       'ontologyTermIRI'])

    

    #for categorical variables get values from values df and write to new df
    i = 0
    for data_type in remodeled_variables['format']:
        if data_type == 'categorical':
            j = 0
            for code_list in values['codeList']:
                if code_list == remodeled_variables.loc[i, 'temp_code_list']:
                    var_values.loc[j, 'variable'] = 'core.' + remodeled_variables['name'][i]
                    var_values.loc[j, 'value'] = values['value'][j]
                    var_values.loc[j, 'label'] = values['label'][j]
                    var_values.loc[j, 'order'] = values['order'][j]
                j+=1
        i+=1

    var_values['release'] = 'LifeCycle.1.0.0'
    
                    
    return var_values
            
    

if __name__ == '__main__':
    main()


    
