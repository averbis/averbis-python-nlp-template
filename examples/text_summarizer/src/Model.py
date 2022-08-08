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

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from src import config


class Model:

    def __init__(self):
        # Model und Pipeline initialization

        self._pretrained = 'lrakotoson/scitldr-catts-xsum-ao'
        self._model = AutoModelForSeq2SeqLM.from_pretrained(self._pretrained)
        self._tokenizer = AutoTokenizer.from_pretrained(self._pretrained)

        self._summarizer_pipeline = pipeline(task='summarization',
                                             model=self._model,
                                             tokenizer=self._tokenizer)

    def preprocess_model_input(self):
        """
        Not necessary in this example.
        Hugging Face Pipeline does pre-processing
        """
        pass

    def postprocess_model_output(self, model_output):
        """
        Extracts summary from model output
        """

        return model_output[0]['summary_text']

    def predict(self, text_input: str) -> dict:
        """
        Wrapper for model prediction
        """
        model_output = self._summarizer_pipeline(text_input,
                                                 min_length=50,
                                                 max_length=150)

        return self.postprocess_model_output(model_output)
