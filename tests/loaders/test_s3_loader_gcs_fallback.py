from mock import patch
from os.path import abspath, join, dirname

from unittest import TestCase
from preggy import expect

import thumbor
import thumbor_cloud_storage
import tc_aws

from thumbor.context import Context
from thumbor.config import Config
from thumbor.loaders import LoaderResult

import thumbor_cloud_storage.loaders.s3_loader_gcs_fallback as loader


result = LoaderResult()
result.successful = True


def dummy_gcs_load(context, url, callback):
    result.buffer = 'gcs'
    callback(result)

def dummy_s3_load(context, url, callback):
    result.buffer = 's3'
    callback(result)

def dummy_s3_load_failed(context, url, callback):
    result = LoaderResult()

    result.buffer = 's3'
    result.successful = False
    callback(result)


class GCSLoaderS3FallbackTestCase(TestCase):
    def setUp(self):
        config = Config()
        self.ctx = Context(config=config)

    @patch.object(tc_aws.loaders.s3_loader, 'load', dummy_s3_load)
    def test_should_load_s3_first(self):
        path = "bucket/image.png"

        result = loader.load(self.ctx, path, lambda x: x).result()

        expect(result).to_be_instance_of(LoaderResult)
        expect(result.buffer).to_equal('s3')

    @patch.object(tc_aws.loaders.s3_loader, 'load', dummy_s3_load_failed)
    @patch.object(thumbor_cloud_storage.loaders.cloud_storage_loader, 'load', dummy_gcs_load)
    def test_should_load_gcs_when_s3_fail(self):
        path = "bucket/image.png"

        result = loader.load(self.ctx, path, lambda x: x).result()

        expect(result).to_be_instance_of(LoaderResult)
        expect(result.buffer).to_equal('gcs')
