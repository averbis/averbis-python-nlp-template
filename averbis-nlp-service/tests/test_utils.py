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

import re

from cassis import Cas

from src import config


def prepare_cas_for_test(text_input: str) -> Cas:

    cas = Cas()
    cas.sofa_string = text_input
    predicted_type = cas.typesystem.create_type(config.PREDICTED_TYPE)
    cas.typesystem.add_feature(predicted_type, "label", "uima.cas.String")
    cas.typesystem.add_feature(predicted_type, "componentId", "uima.cas.String")
    cas.typesystem.add_feature(predicted_type, "confidence", "uima.cas.Double")
    cas.typesystem.add_feature(predicted_type, "value", "uima.cas.String")

    token_type = cas.typesystem.create_type(config.TOKEN_TYPE)
    token_list = [token_type(begin=word.start(), end=word.end()) for word in re.finditer(r"\S+", text_input)]
    cas.add_annotations(token_list)

    sentence_type = cas.typesystem.create_type(config.SENTENCE_TYPE)
    sentence_annotation = sentence_type(begin=0, end=len(text_input))
    cas.add_annotation(sentence_annotation)

    # add document type
    document_type = cas.typesystem.get_type(config.DOCUMENT_TYPE)
    document_annotation = document_type(begin=0, end=len(text_input))
    cas.add_annotation(document_annotation)

    return cas
