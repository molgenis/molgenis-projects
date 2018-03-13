import csv, zipfile, os

class BbmriEricCountryModelMaker():
    def __init__(self, country_codes, cwd):
        self.cwd = cwd
        self.retrieve_model()
        self.country_codes = country_codes

    def retrieve_model(self):
        self.packages = self.get_packages()
        self.attributes = self.get_attributes()
        self.entities = self.get_entities()

    def create_country_directories(self):
        os.chdir(self.cwd+'/data_model/countries')
        for code in self.country_codes:
            if not os.path.exists(code):
                os.makedirs(code)

    def create_meta_data_for_countries(self):
        for code in self.country_codes:
            self.create_meta_data_for_country(code)

    def create_meta_data_for_country(self, country_code):
        country_specific_attributes = self.make_country_attributes(country_code)
        country_specific_entities = self.make_country_entities(country_code)
        country_specific_packages = self.make_country_packages(country_code)
        self.write_to_file(country_code, country_specific_attributes, country_specific_entities, country_specific_packages)


    def make_country_attributes(self, country_code):
        entities = self.rename_entities(self.attributes['entity'], country_code)
        ref_entities = self.rename_entities(self.attributes['refEntity'], country_code)
        return {"refEntity": ref_entities, "entity": entities}

    def make_country_entities(self, country_code):
        package_column = []
        label_column = []
        for i, entity in enumerate(self.entities['name']):
            if entity == "biobanks" or entity == "collections" or entity == "networks" or entity == "persons":
                package_column.append("eu_bbmri_eric_" + country_code)
                label_column.append(country_code+": "+entity)
            else:
                package_column.append(self.entities['package'][i])
                label_column.append(self.entities['label'][i])

        return {"package": package_column, "label":label_column}

    def make_country_packages(self, country_code):
        return {"name": ["eu_bbmri_eric_" + country_code, "eu_bbmri_eric"], "description":["bbmri_eric", "bbmri_eric"],
                "label":["", ""], "parent":["", ""], 'tags':["", ""]}

    def rename_entities(self, entities, country_code):
        entityNames = []
        for entity in entities:
            if entity.endswith('biobanks') or entity.endswith('collections') or entity.endswith(
                    'persons') or entity.endswith('networks'):
                splitted = entity.split("_")
                countryEntity = "_".join(splitted[0:3]) + "_" + country_code + "_" + "_".join(splitted[3:len(splitted)])
                entityNames.append(countryEntity)
            else:
                entityNames.append(entity)
        return entityNames

    def rename_labels(self, labels, country_code):
        countryLabels = []
        for label in labels:
            if label.endswith('biobanks') or label.endswith('collections') or label.endswith(
                    'persons') or label.endswith('networks'):
                splitted = label.split("_")
                countryEntity = "_".join(splitted[0:3]) + "_" + country_code + "_" + "_".join(splitted[3:len(splitted)])
                countryLabels.append(countryEntity)
            else:
                countryLabels.append(label)
        return countryLabels

    def get_model_sheet(self, filename):
        model_sheet = {}
        headers = []
        with open(self.cwd+'/data_model/{}.csv'.format(filename)) as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            for i, line in enumerate(reader):
                if i == 0:
                    for header_num, value in enumerate(line):
                        value = value.strip('\n')
                        headers.append(value)
                        model_sheet[value] = []
                else:
                    for num, value in enumerate(line):
                        model_sheet[headers[num]].append(value)
        return model_sheet

    def get_packages(self):
        packages = self.get_model_sheet("packages")
        return packages

    def get_entities(self):
        entities = self.get_model_sheet("entities")
        return entities

    def get_attributes(self):
        attributes = self.get_model_sheet("attributes")
        return attributes

    def write_to_file(self, country, country_specific_attributes, country_specific_entities, country_specific_packages):
        self.write_meta_data_sheet(country_specific_packages, self.packages, country, 'packages')
        self.write_meta_data_sheet(country_specific_entities, self.entities, country, 'entities')
        self.write_meta_data_sheet(country_specific_attributes, self.attributes, country, 'attributes')
        meta_data = zipfile.ZipFile('{}/{}.zip'.format(country, country), 'w')
        meta_data.write(country+'/packages.csv')
        meta_data.write(country+'/entities.csv')
        meta_data.write(country+'/attributes.csv')
        meta_data.close()

    def write_meta_data_sheet(self, specific, generic, country, filename):
        items = self.convert_format(specific, generic)
        output = open(country+'/'+filename+'.csv', 'w')
        for line in items:
            output.write('"'+'","'.join(line)+'"\n')
        output.close()

    def convert_format(self, specific, generic):
        # for each attribute, entity and package:
        #   check if in specific
        #   if so:
        #       take specific
        #   else:
        #       take not specific
        # convert: d = {'x':['a','b','c'], 'y':['d','e','f'], 'z':['g', 'h', 'i']}
        # to: [['x', 'y', 'z'], ('a', 'g', 'd'), ('b', 'h', 'e'), ('c', 'i', 'f')]
        country = generic.copy()
        content = [list(country.keys())]
        # replace country specific part
        for key in specific:
            country[key] = specific[key]
        # put the values in the right format
        for i, value in enumerate(zip(*list(country.values()))):
            content.append(value)
        return content



def main():
    model_maker = BbmriEricCountryModelMaker(["AT", "BE", "CZ", "DE", "EE", "FI", "FR", "GR", "IT", "MT", "NL", "NO",
                                              "PL", "SE", "UK", "LV"])
    model_maker.create_country_directories()
    model_maker.create_meta_data_for_countries()


if __name__ == "__main__":
    main()
