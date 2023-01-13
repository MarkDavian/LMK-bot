from ..csv_parser import CSVParser

FILE_TO_PARSE = 'output.csv'

def main():
    parser = CSVParser(FILE_TO_PARSE)
    parser.process()

    print('Dictionary: ')
    print(parser.dict())

    parser.json('output.json')

if __name__ == "__main__":
    main()