# backup-db-vm

# Take a backup snapshot of a VM managed by a vCenter
````
$ python take_vm_backup_snapshot.py \
    --vcenter-host my-vc.com \
    --vcenter-user my-vc-user \
    --vcenter-pwd my-vc-pwd \
    --vm-name my-vm-name
    
04/06/16 21:27 - Connection succesful with vCenter my-vc.com
04/06/16 21:27 - Taking backup snaphost for VM 'my-vm-name'
04/06/16 21:29 - Backup snaphost for VM 'my-vm-name' succesfully taken!
````

# Backup the data from a SQL database into Google Cloud Storage
## Extract the data from the DB

## Upload the compressed data to a GCS bucket
````
$ python upload_file_to_gcs.py \
    --gcs-bucket my-bucket \
    --gcs-cred-json mycred.json \
    --file my-sql-dump_040716_1234.gz  \
    --file-gcs-type application/x-gzip
    
04/07/16 16:23 - File named 'my-sql-dump_040516_1234.gz' exists
04/07/16 16:23 - URL being requested: POST https://www.googleapis.com/upload/storage/v1/b/prestodbbackup/o?uploadType=multipart&alt=json
04/07/16 16:23 - Attempting refresh to obtain initial access_token
04/07/16 16:23 - Refreshing access_token
04/07/16 16:23 - URL being requested: GET https://www.googleapis.com/storage/v1/b/prestodbbackup/o?fields=items%28name%2Csize%2CcontentType%29&alt=json
04/07/16 16:23 - Attempting refresh to obtain initial access_token
04/07/16 16:23 - Refreshing access_token
04/07/16 16:23 - The object of name 'my-sql-dump_040516_1234.gz' is present on the bucket 'my-bucket'!
````
