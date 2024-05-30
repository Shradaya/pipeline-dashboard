import boto3


s3 = boto3.client("s3")

def get_file_content(bucket: str, key: str) -> str:
    data = s3.get_object(Bucket=bucket, Key=key)
    msg = data['Body'].read()
    try:
        msg_final = msg.decode("UTF-8")
    except:
        msg_final = msg.decode("ISO-8859-1")
    return msg_final.replace('\n', '\r')