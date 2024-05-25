import argparse
from src.factory.source_factory import SourceFactory



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch records from an API endpoint.')
    parser.add_argument('--source', type=str, default="api")
    parser.add_argument('--stage', type=str, default = None)

    args = parser.parse_args()

    source_factory = SourceFactory()

    handler = source_factory.select_handler(args.source)

    page = 1
    page_size = 1000
    handler.create_tables()

    while True:
        response = handler.extract_data("2021-07-17", "2024-04-23", str(page_size), str(page))
        total_count = handler.get_total_data_count(response)
        extracted_datas = handler.get_data_from_response(response)

        if extracted_datas:
            print(f"Inserting {len(extracted_datas)} into raw tables")
            handler.insert_into_raw_tables(raw_data_set = extracted_datas)

        if total_count <= page_size * page:
            break
        page += 1

    print("Processing Data for Standard tables")
    handler.insert_into_std_tables()
    print("Processing Data for final tables")
    handler.insert_into_final_tables()
    print("Creating  Data for final tables")
    handler.create_procedures()
        


