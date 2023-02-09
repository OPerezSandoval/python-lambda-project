# import modules
import boto3
from datetime import datetime

# variables for current date and to format date
today = datetime.today()
todays_date = today.strftime("%Y%m%d")

# lambda handler
def lambda_handler(event, context):

    # variable to connect to s3 through boto3
    s3_client = boto3.client("s3")

    # connect to the correct bucket in AWS and list all objects in the bucket
    bucket_name = "orginize-s3-objects-python-project"
    list_objects_response = s3_client.list_objects_v2(Bucket=bucket_name)

    # get only the contents from list_object_response and create a list
    get_contents = list_objects_response.get("Contents")
    get_objects_and_folder_names = []

    # iterate through get_contents to get Key value, which has the files name.
    # add objects to the list get_object_and_folder_names
    for item in get_contents:
        s3_object_name = item.get("Key")
        get_objects_and_folder_names.append(s3_object_name)

    # create variable for directories with correct date format
    directory_name = todays_date + "/"

    # create directory if it doesn't exist within the bucket
    if directory_name not in get_objects_and_folder_names:
        s3_client.put_object(Bucket=bucket_name, Key=(directory_name))

    # copies files with correct date into the correct directory with the same date.
    # deletes the files from the main bucket and keeps only the files inside the directories.
    for item in get_contents:
        object_creation_date = item.get("LastModified").strftime("%Y%m%d") + "/"
        object_name = item.get("Key")

        if object_creation_date == directory_name and "/" not in object_name:
            s3_client.copy_object(Bucket=bucket_name, CopySource=bucket_name+"/"+object_name, Key=directory_name+object_name)
            s3_client.delete_object(Bucket=bucket_name, Key=object_name)

