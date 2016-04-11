# backup-db-vm
Backing up a database VM can be easily done using a scheduled job executed by a Jenkins server.
<br>
<br>
Two different actions seem necessary:
* Taking a snapshot of the VM itself
* Saving a dump of the DB on a cloud storage (Google Cloud Storage or Amazon S3)

Storing SQL dumps from Prod on a 3rd party platform can also be very helpful for developers: they can import the production data in their local devtest environment easily & safely.

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
<br><img src="https://github.com/craimbert/backup-db-vm/blob/master/list_backup_snapshots_vcenter.png" width="600" >


# Backup the data from a PSQL database into Google Cloud Storage
## Get a compressed dump of a PSQL database
PostgreSQL doc [here](http://www.postgresql.org/docs/9.1/static/backup-dump.html).<br>
A timestamp can be used in the gz file name, for example I used: `sql-dump_040716_1234.gz`
````
$ pg_dump dbname | gzip > sql-dump_040716_1234.gz
````
## Upload the archive to a Google Cloud Storage bucket

### Get GCP Service credentials
Authentication is obivously required for using the GCP API/library: refer to the `Service account credentials` section of the [GCP doc](https://cloud.google.com/storage/docs/authentication?hl=en#service_accounts) => the private key (service account key) is part of the the service account credentials JSON returned from service account credentials creation.
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
04/07/16 16:23 - The object named 'sql-dump_040516_1234.gz' has been uploaded to the bucket 'my-bucket'!
````
# Common Issue on MAC OSX
## GCP Python library & pip
Undefined error: 'Module_six_moves_urllib_parse' object has no attribute 'urlencode' -> [Github issue](https://github.com/google/google-api-python-client/issues/100)
````
$ export PYTHONPATH=/Library/Python/2.7/site-packages
````
