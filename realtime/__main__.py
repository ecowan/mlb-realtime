from parse import MlbParser
from url_builder import UrlBuilder
from time_converter import TimeConverter
from client import Client

def main():
    converted_time = TimeConverter().get_time()
    url = UrlBuilder(converted_time).build_url()
    mlb = MlbParser(url)
    c = Client(mlb)
    c.update()

if __name__ == "__main__":
    main()