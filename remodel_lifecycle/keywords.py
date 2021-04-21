import pandas as pd 
import numpy as np

topics = pd.read_csv('./src/Topic.csv')

keywords = topics.rename(columns={"label": "new_name", "parentTopic": "parent"})
keywords["definition"] = ""
keywords["comments"] = ""
keywords["ontologyTermURI"] = ""

# voor elke keyword rij
for index, row in keywords.iterrows():
  parentId = row['parent']
  # als er sprake is van een parent
  if not parentId == "":
    parentIndex = ""
    # zoek de rij index van de parent
    for lookUpIndex, lookUpRow in keywords.iterrows():
      if(parentId == lookUpRow['name']):
        parentIndex = lookUpIndex
  # als de parent gevonden is 
  if not parentIndex == "":
    # set de name naam de parent als parent cell
    keywords.loc[index, 'parent'] = keywords.loc[parentIndex, 'new_name']

keywords = keywords.drop(columns=['name'])
keywords = keywords.rename(columns={"new_name": "name"})

keywords.to_csv('./output/temp/Keywords.csv', index=False)
keywords