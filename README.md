# backup-db-vm

# Take a backup snapshot of the VM managed by a vCenter
Taking a snapshot of a VM can be triggered through VMware vSphere API, using [pyVmomi](https://github.com/vmware/pyvmomi) for example.
<br>
<br>
Usage of the python wrapper around the vSphere API written in Python:
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
Result:
![snapshots list](https://github.com/craimbert/backup-db-vm/list_backup_snapshots_vcenter.png =250px)

# Backup the data from a PSQL database into Google Cloud Storage
## Get a compressed dump of a PSQL database
PostgreSQL doc [here](http://www.postgresql.org/docs/9.1/static/backup-dump.html).<br>
You can use a timestamp in the gz file name, for example I used: `sql-dump_040716_1234.gz`
````
$ pg_dump dbname | gzip > sql-dump_040716_1234.gz
````
## Upload the archive to a Google Cloud Storage bucket

### Get GCP Service credentials
Authentication is obivously required for using the GCP API/library: refer to the `Service account credentials` section of the [GCP doc](https://cloud.google.com/storage/docs/authentication?hl=en#service_accounts)=> The private key (service account key) is part of the the service account credentials JSON returned as a result of service account credentials creation.
<br>
<br>
FYI: An env var `GOOGLE_APPLICATION_CREDENTIALS` needs to point to that credentials JSON, but this is handled in the python script.

### Upload the file to GCS
The python script will upload the archive to the specified GCS bucket:
````
$ python upload_file_to_gcs.py \
    --gcs-bucket my-bucket \
    --gcs-cred-json mycred.json \
    --file sql-dump_040716_1234.gz  \
    --file-gcs-type application/x-gzip
    
04/07/16 16:23 - File named 'sql-dump_040516_1234.gz' exists
04/07/16 16:23 - URL being requested: POST https://www.googleapis.com/upload/storage/v1/b/prestodbbackup/o?uploadType=multipart&alt=json
04/07/16 16:23 - Attempting refresh to obtain initial access_token
04/07/16 16:23 - Refreshing access_token
04/07/16 16:23 - URL being requested: GET https://www.googleapis.com/storage/v1/b/prestodbbackup/o?fields=items%28name%2Csize%2CcontentType%29&alt=json
04/07/16 16:23 - Attempting refresh to obtain initial access_token
04/07/16 16:23 - Refreshing access_token
04/07/16 16:23 - The object of name 'sql-dump_040516_1234.gz' is present on the bucket 'my-bucket'!
````
# Common Issue on MAC OSX
## GCP Python library & pip
Undefined error: 'Module_six_moves_urllib_parse' object has no attribute 'urlencode' -> [Github issue](https://github.com/google/google-api-python-client/issues/100)
````
$ export PYTHONPATH=/Library/Python/2.7/site-packages
````
