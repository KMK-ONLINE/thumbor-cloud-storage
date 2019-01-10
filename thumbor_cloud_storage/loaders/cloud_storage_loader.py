# coding: utf-8

import urllib2
from google.cloud import storage
from thumbor.loaders import LoaderResult
from tornado.concurrent import return_future
import requests
from requests.adapters import TimeoutSauce

class ThumborRetrievalTimeout(TimeoutSauce):
    def __init__(self, *args, **kwargs):
        super(MyTimeout, self).__init__(connect=31, read=31)

requests.adapters.TimeoutSauce = ThumborRetrievalTimeout


@return_future
def load(context, path, callback):
    project_id = context.config.get("CLOUD_STORAGE_PROJECT_ID")

    result = LoaderResult()

    bucket_id = _get_bucket(path)
    if bucket_id == '' or bucket_id is None:
        result.successful = False
        result.error = LoaderResult.ERROR_NOT_FOUND
        callback(result)
        return

    prefix = len(bucket_id) + 1

    path = _clean_path(path)
    file_path = path[prefix:]

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_id)
    blob = bucket.blob(file_path)

    try:
        result.buffer = blob.download_as_string()
        result.successful = True
    except Exception, e:
        if '404' in str(e):
            result.successful = False
            result.error = LoaderResult.ERROR_NOT_FOUND
        else:
            result.successful = False
            result.error = LoaderResult.ERROR_UPSTREAM

    callback(result)


def _get_bucket(url):
    url = urllib2.unquote(url)

    if '/' not in url:
        return None

    url_by_piece = url.lstrip('/').split('/')
    return url_by_piece[0]


def _clean_path(path):
    path = urllib2.unquote(path)
    path = path.decode('utf-8')

    while '//' in path:
        path = path.replace('//', '/')

    if '/' == path[0]:
        path = path[1:]

    return path
