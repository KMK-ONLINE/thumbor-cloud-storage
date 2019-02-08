from . import cloud_storage_loader
from tc_aws.loaders import s3_loader
from tornado.concurrent import return_future


@return_future
def load(context, path, callback):
    def callback_wrapper(result):
        # result data type from s3 loader when succesfull is str type,
        # it is diffrent with gcs loader that always return LoaderResult
        # with successful attribute set
        if hasattr(result, "successful") and not result.successful:
            cloud_storage_loader.load(context, path, callback)
        else:
            callback(result)

    s3_loader.load(context, path, callback_wrapper)
