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

class Model:
    def __init__(self):

        self._model = None

    def preprocess_model_input(self, text_input: str):
        """
        Method for all pre-processing steps required transforming
        the text input to the model input
        """
        return text_input

    def postprocess_model_output(self, predictions):
        """
        Method for all post-processing steps required for
        formatting model output to label and confidence.
        """

        return predictions

    def predict(self, text_input: str):

        model_input = self.preprocess_model_input(text_input)

        predictions = self._model.predict(model_input)

        return self.postprocess_model_output(predictions)
