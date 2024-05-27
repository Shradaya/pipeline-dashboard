import argparse
from src.constants import HANDLERS_AVAILABLE
from src.factory.source_factory import SourceFactory

def lambda_handler(event, context):
    source = "api"
    bucket, key = (None, None)
    if event.get('Records'):
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        if not bucket or not key:
            print("Bucket or Key not available")
            return
        file_extension = key.split(".")[-1]
        if file_extension in HANDLERS_AVAILABLE:
            source = file_extension

    source_factory = SourceFactory()
    handler = source_factory.select_handler(source)
    page = 1
    page_size = 1000
    handler.create_tables()
    while True:
        response = handler.extract_data(
            startDate = "2021-07-17",
            endDate = "2024-04-23",
            size = str(page_size),
            page = str(page),
            bucket = bucket,
            key = key)
        total_count = handler.get_total_data_count(response)
        extracted_datas = handler.get_data_from_response(response)

        if extracted_datas:
            print(f"Inserting {len(extracted_datas)} into raw tables")
            handler.insert_into_raw_tables(raw_data_set = extracted_datas)

        if total_count <= page_size * page or bucket or key:
            break
        page += 1

    print("Processing Data for Standard tables")
    handler.insert_into_std_tables()
    print("Processing Data for final tables")
    handler.insert_into_final_tables()
    print("Creating  Data for final tables")
    handler.create_procedures()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Run pipeline")
    parser.add_argument(
        "--path",
        dest = "path",
        help="Path name sample 'path/to/file.*'",
    )
    parser.add_argument(
        "--bucket",
        dest = "bucket",
        help="Bucket from where file is to be read'",
    )
    known_cmd, unknown_cmd = parser.parse_known_args()
    lambda_handler({
        'Records': [
            {
                's3': {
                    'bucket': { 
                        'name':  known_cmd.bucket
                    }, 
                    'object': {
                        'key': known_cmd.path
                    }
                }
            }
        ]
    } if known_cmd.bucket and known_cmd.path else { 'Records': [] }, None)