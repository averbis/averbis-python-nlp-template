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

from transformers import AutoTokenizer, TFAutoModelForTokenClassification, pipeline
from typing import Any
from src import config, utils


class Model:

    def __init__(self):
        self.pretrained = 'roberta-base'
        self.max_tokens = config.MAX_TOKENS
        self.model = TFAutoModelForTokenClassification.from_pretrained(self.pretrained,
                                                                       id2label={v: k for k, v in
                                                                                 config.NER_TAGS.items()},
                                                                       label2id=config.NER_TAGS,
                                                                       from_pt=True)

        self.model.load_weights(config.MODEL_PATH)

        self.ner_pipeline = pipeline(task="ner",
                                     model=self.model,
                                     tokenizer=AutoTokenizer.from_pretrained(self.pretrained,
                                                                             model_max_length=config.MAX_TOKENS))

    def preprocess_model_input(self):
        """
        Not necessary in this example.
        Hugging Face Pipeline does pre-processing
        """
        pass

    def postprocess_model_output(self, model_input: Any,
                                 cas_sentence) -> list():
        """
        Output of the model are annotations per (sub-)token. Post-processing
        merges token annotations to entity annotations.
        eg: Asp[Drug] irin[Drug] will be merged to Aspirin[Drug]
        """

        merged_entities = utils.postprocess_predictions(model_input)
        entity_list = list()

        for entity in merged_entities:
            annotation_offset = cas_sentence.begin

            cur_annotation = {
                "begin": entity['begin'] + annotation_offset,
                "end": entity['end'] + annotation_offset,
                "value": entity['value'],
                'label': entity['tag'],
                'componentId': 'ADE_Sentence_SequenceLabeling-service:0.1.0',
                "confidence": entity['confidence']
            }
            entity_list.append(cur_annotation)

        return entity_list

    def predict(self,
                text_input: str,
                cas_sentence):
        """
        Wrapper for model prediction
        """
        model_output = self.ner_pipeline(text_input)

        return self.postprocess_model_output(model_output,
                                             cas_sentence=cas_sentence)



