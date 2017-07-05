from google.cloud import storage
from thumbor.loaders import LoaderResult
from tornado.concurrent import return_future


@return_future
def load(context, path, callback):
    bucket_id  = context.config.get("CLOUD_STORAGE_BUCKET_ID")
    project_id = context.config.get("CLOUD_STORAGE_PROJECT_ID")

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_id)
    blob = bucket.blob(path)

    result = LoaderResult()

    if blob is None:
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False
        return callback(result)

    result.buffer = blob.download_as_string()
    result.successful = True
    callback(result)
