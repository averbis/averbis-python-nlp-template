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
        Definition of Models and all required components.
        """

        self._model: Model = Model()

    def predict(self,
                cas: cassis.Cas):

        """
        Wrapper for Model Prediction

        Args:
            cas: cassis.Cas - Incoming Document in Cas format
        """

        # set annotation type to be carried out
        averbis_annotation_type = cas.typesystem.get_type(config.PREDICTED_TYPE)

        # set text input type (in this example Sentence)
        annotation_input: str = config.ANNOTATION_INPUT_DICT[config.ANNOTATION_INPUT]

        # Iterate over all sentences in Document
        for cas_sentence in cas.select(annotation_input):

            # text input is converted to word embeddings
            label, confidence = self._model.predict(cas_sentence.get_covered_text())

            annotation = {
                "begin": cas_sentence.begin,
                'end': cas_sentence.end,
                "value": label,
                'label': 'ade-sentence-classification',
                'confidence': confidence,
                'componentId': 'ade-sentence-classifier:0.1.0'
            }

            cas.add_annotation(averbis_annotation_type(**annotation))
