from setuptools import setup
from setuptools import find_packages

REQUIREMENTS = [
  "thumbor",
  "google-cloud-storage",
  "timeout_decorator",
  "tc_aws" #https://github.com/KMK-ONLINE/aws/archive/master.zip
]

TEST_REQUIREMENTS = [
  "mock",
  "preggy"
]

setup(
  name="thumbor_cloud_storage",
  version="1.0.0",
  author="Pedro Gimenez",
  author_email="me@pedro.bz",
  description="Thumbor's Google Cloud Storage loader",
  url="https://github.com/pedrogimenez/thumbor-cloud-storage",
  license="MIT",
  include_package_data=True,
  packages=find_packages(),
  install_requires=REQUIREMENTS,
  tests_require=TEST_REQUIREMENTS,
  zip_safe=False
)
