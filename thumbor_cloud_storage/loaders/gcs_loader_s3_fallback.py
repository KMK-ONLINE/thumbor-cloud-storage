from . import cloud_storage_loader
from tc_aws.loaders import s3_loader
from tornado.concurrent import return_future


@return_future
def load(context, path, callback):
    def callback_wrapper(result):
        if result.successful:
            callback(result)
        else:
            s3_loader.load(context, path, callback)

    cloud_storage_loader.load(context, path, callback_wrapper)
