import json

class Session():
    """This is the mocked version of the molgenis API"""
    def __init__(self, url="https://molgenis01.gcc.rug.nl:443/api/"):
        self.url = url

    def login(self, username, password):
        return 'token'

    def get_total(self, entity):
        return 8

    def get(self, entity, num, start):
        ##########################################################################################
        ### cases to test:
        ##### 1 more than 1 omim number + consensus		--> negative
        ##### 2 more than 1 omim number + no consenus	--> negative
        ##### 3 more than 1 omim number + 1 lab			--> negative
        ##### 4 1 omim number + consensus 				--> positive (write to file)
        ##### 5 1 omim number + no consensus 			--> negative
        ##### 6 1 omim number + 1 lab					--> negative
        ##########################################################################################
        ##### variant1: case 6
        ##### variant2: case 1
        ##### variant3: case 2
        ##### variant4: case 3
        ##### variant5: case 4
        ##### variant6: case 4
        ##### variant7: case 4
        ##### variant8: case 5
        mocked_response = json.loads(open("mock_response.json").read())
        return mocked_response

    def get_response(self, entity, id, chromosome, ref, alt, gene, classification):
        response = {"_meta": {"test": "test"},
                    "_href": "/api/v2/{}/{}".format(entity, id),
                    "id": id,
                    "chromosome": chromosome,
                    "POS": 123456,
                    "stop": 123456,
                    "REF": ref,
                    "ALT": alt,
                    "gene": gene,
                    "cDNA": "c.123{}>{}".format(ref, alt),
                    "transcript": "NM_123456.7",
                    "protein": "p.T123I",
                    "type": "snp",
                    "location": "exonic",
                    "exon": "4",
                    "effect": "synonymous",
                    "classification": classification,
                    "comments": {"test": "test"}
                    }
        return response

    def getById(self, enity, id):
        if id == "lab1_mocked_variant5":
            response = self.get_response(enity, id, "5", "A", "C", "GENE5", "Pathogenic")
            return response
        elif id == "lab2_mocked_variant5" or id == "lab3_mocked_variant5":
            response = self.get_response(enity, id, "5", "A", "C", "GENE5", "Likely pathogenic")
            return response
        elif id.endswith("mocked_variant6"):
            response = self.get_response(enity, id, "6", "A", "T", "GENE6", "Benign")
            return response
        elif id == "lab2_mocked_variant7":
            response = self.get_response(enity, id, "7", "T", "G", "GENE7", "Likely benign")
            return response
        elif id == "lab3_mocked_variant7":
            response = self.get_response(enity, id, "7", "T", "G", "GENE7", "Benign")
            return response
        else:
            raise TypeError("{} not supported".format(id))

    def logout(self):
        return "Invalid token"
