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

from src import config
from src.Model import Model


class Annotator:
    """
    Carries out processing of incoming annotation requests.
    """

    def __init__(self):
        """
        Definition of Models and all necessary preprocessing steps.
        """

        self.model: Model = Model()

    def predict(self,
                cas: cassis.Cas):

        """
        Method for resources prediction and creation of annotation.

        Args:
            cas: cassis.Cas - Incoming Document in Cas format
        """

        # set annotation type to be carried out
        averbis_annotation_type = cas.typesystem.get_type(config.PREDICTED_TYPE)

        # set text input type (typically Document or Sentence)
        annotation_input: str = config.ANNOTATION_INPUT_DICT[config.ANNOTATION_INPUT]

        # iterate over each text piece of annotate
        for cas_element in cas.select(annotation_input):

            text_input = cas_element.get_covered_text()

            label, confidence = self.model.predict(text_input)

            annotation = {
                "begin": cas_element.begin,
                "end": cas_element.end,
                "label": 'classfication',
                "componentId": 'averbis-nlp-template:0.1.0',
                'value': label,
                'confidence': confidence}

            cas.add_annotation(averbis_annotation_type(**annotation))


















