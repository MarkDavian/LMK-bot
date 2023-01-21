from ..pdf_parser import PDFParser


FILE_TO_PARSE = 'file.pdf'

def main():
    parser = PDFParser(FILE_TO_PARSE)
    df = parser.extract_df()
    print(df)

    parser.extract_csv('output.csv')

    d = parser.extract_dict()
    print(d)

    parser.extract_json('output.json')


if __name__ == "__main__":
    main()