#
# Copyright (c) 2022 Averbis GmbH.
#
# This file is part of Averbis Python NLP Template.
# See https://www.averbis.com for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

import cassis
import logging

from src.PredictionRequest import PredictionRequest


def setup_logging():
    """
    Configures Logging of Container
    """
    logging_formatting = "%(process)d-%(thread)d %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG,
                        format=logging_formatting)


def process_annotation_request(annotation_request: PredictionRequest) -> cassis.Cas:
    """
    Parses incoming prediction request.

    Args:
        annotation_request: Incoming Prediction Request

    Returns:
        cas: Document to be annotated in cas format
    """

    return cassis.load_cas_from_xmi(source=annotation_request.document['xmi'],
                                    typesystem=cassis.load_typesystem(annotation_request.typeSystem))
