import boto3
import os
import json

from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers

# Read environment variables
HOST = os.environ.get('ES_HOST')
INDEX = os.environ.get('ES_INDEX')

s3client = boto3.client('s3')

def get_es():
    session = boto3.Session()
    region = session.region_name or 'eu-north-1'
    credentials = session.get_credentials().get_frozen_credentials()

    awsauth = AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=HOST,
        aws_region=region,
        aws_service='es'
    )

    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    es.transport._verified_elasticsearch = True

    return es
       

def push_batch(actions):
    es = get_es()
    if not es.ping():
        print('Unable to connect to Elasticsearch.')
        

    print(f'Pushing batch of {len(actions)} records to Elasticsearch...')
    success, failed = helpers.bulk(es, actions, stats_only=True)
    print(f'Successfully pushed: {success}, Failed: {failed}')

def lambda_handler(event, context):
    
    print("Received event:")
    print(json.dumps(event))

    records = event.get('Records', [])
    actions = []
    ignored_record_count = 0

    for record in records:
        try:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            print(f"Processing file: s3://{bucket}/{key}")

            obj = s3client.get_object(Bucket=bucket, Key=key)
            body = obj['Body'].read()
            body_json = json.loads(body.decode('utf-8'))
            data = body_json.get('data', [])

            for item in data:
                actions.append({
                    '_index': INDEX,
                    '_id': item.get('id'),
                    '_source': item,
                    '_op_type': 'index'
                })

                if len(actions) == 50:
                    push_batch(actions)
                    actions = []

        except Exception as e:
            ignored_record_count += 1
            print(f"Error processing record: {record}")
            print(str(e))

    if actions:
        push_batch(actions)

    print(f'Total ignored records: {ignored_record_count}')
