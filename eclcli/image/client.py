#   Copyright 2012-2013 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import logging

from eclcli.common import utils


LOG = logging.getLogger(__name__)

DEFAULT_API_VERSION = '1'
API_VERSION_OPTION = 'os_image_api_version'
API_NAME = "image"
API_VERSIONS = {
    "1": "glanceclient.v1.client.Client",
    "2": "glanceclient.v2.client.Client",
}

IMAGE_API_TYPE = 'image'
IMAGE_API_VERSIONS = {
    '1': 'eclcli.api.image_v1.APIv1',
    '2': 'eclcli.api.image_v2.APIv2',
}


def make_client(instance):
    """Returns an image service client"""
    image_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('Instantiating image client: %s', image_client)

    endpoint = instance.get_endpoint_for_service_type(
        API_NAME,
        region_name=instance._region_name,
        interface=instance._interface,
    )

    client = image_client(
        endpoint,
        token=instance.auth.get_token(instance.session),
        cacert=instance._cacert,
        insecure=instance._insecure,
    )

    # Create the low-level API

    image_api = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        IMAGE_API_VERSIONS)
    LOG.debug('Instantiating image api: %s', image_api)

    client.api = image_api(
        session=instance.session,
        endpoint=instance.get_endpoint_for_service_type(
            IMAGE_API_TYPE,
            region_name=instance._region_name,
            interface=instance._interface,
        )
    )

    return client


def build_option_parser(parser):
    """Hook to add global options"""
    # parser.add_argument(
    #     '--os-image-api-version',
    #     metavar='<image-api-version>',
    #     default=utils.env('OS_IMAGE_API_VERSION'),
    #     help='Image API version, default=' +
    #          DEFAULT_API_VERSION +
    #          ' (Env: OS_IMAGE_API_VERSION)')
    return parser
