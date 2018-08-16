class MolgenisConfigParser:
    def __init__(self, file):
        self.config = {"url": "http://localhost:8080/api/",
                       "account":"user",
                       "password":"password",
                       "labs":"lab1,lab2,lab3"}