import molgenis

class Bbmri_eric_data_retriever():
    def __init__(self, url):
        self.url = url
        session = molgenis.Session(url)
        session.login("admin", "admin")
        # session.upload_with_meta_data("/Users/mslofstra/Desktop/demo/borrel.xlsx")


def main():
    data_retriever = Bbmri_eric_data_retriever("http://localhost:8080/api/")

if __name__ == "__main__":
    main()