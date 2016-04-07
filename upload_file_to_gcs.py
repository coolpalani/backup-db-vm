#!/usr/bin/env python

"""
Upload a file on a Google Cloud Storage bucket
"""

import argparse
import logging
import os
from googleapiclient import discovery
from googleapiclient import http

from oauth2client.client import GoogleCredentials

# Set logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%m/%d/%y %H:%M')

def main(bucket, json_gcs_api_key, filepath, gcs_filetype):
    # Set the env var GOOGLE_APPLICATION_CREDENTIALS to the JSON credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_gcs_api_key

    # Validate file
    filename = validate_file(filepath)

    if filename:
        upload_file(bucket, filepath, filename, gcs_filetype)
        validate_upload_file(bucket, filename, gcs_filetype)


def validate_file(filepath):
    """Validate the file pointed by filepath exists and is a file, and get its filename"""
    if os.path.isfile(filepath):
        _, tail = os.path.split(filepath)
        logging.info("File named '%s' exists" % tail)
        return tail


def create_service():
    """Create Google Cloud Storage service"""
    # Get the credentials from the JSON file pointed by env var GOOGLE_APPLICATION_CREDENTIALS
    credentials = GoogleCredentials.get_application_default()

    # Construct the service object for interacting with the Cloud Storage API
    return discovery.build('storage', 'v1', credentials=credentials)


def upload_file(bucket, filepath, filename, gcs_filetype):
    """Upload a single file of name filename and path filepath on the GCS bucket named bucket"""
    # Request body
    body = {
        'name': filename,
    }
    # Create service
    service = create_service()
    # Upload media to GCS bucket
    with open(filepath, 'rb') as f:
        req = service.objects().insert(
            bucket=bucket,
            body=body,
            media_body=http.MediaIoBaseUpload(f, gcs_filetype))
        req.execute()
    return


def validate_upload_file(bucket, filename, gcs_filetype):
    """Validate the file got uploaded on the GCS bucket by listing the content of the bucket"""
    service = create_service()

    # Get all the objects of the bucket
    req = service.objects().list(
        bucket=bucket,
        fields='items(name,size,contentType)')
    all_objects = []
    while req:
        resp = req.execute()
        all_objects.extend(resp.get('items', []))
        req = service.objects().list_next(req, resp)

    # Validate an object of the right name and contentType exists on the bucket
    if any(obj['name'] == filename and obj['contentType'] == gcs_filetype and obj['size'] > 0 for obj in all_objects):
        logging.info("The object of name '%s' is present on the bucket '%s'!" % (filename, bucket))
    else:
        logging.error("ERROR: The object of name '%s' is not present on the bucket '%s' or is of size null" % (filename, bucket))
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload a file to a Google Cloud Storage bucket')
    parser.add_argument('--gcs-bucket', help='Google Cloud Storage bucket name', required=True)
    parser.add_argument('--gcs-cred-json', help='JSON file of GCS credentials', required=True)
    parser.add_argument('--file', help='File to upload', required=True)
    parser.add_argument('--file-gcs-type', help='Type of the file in GCS', required=True)
    args = vars(parser.parse_args())

    main(args['gcs_bucket'], args['gcs_cred_json'], args['file'], args['file_gcs_type'])
