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

import pathlib

### Path Seetings

RESOURCES_FOLDER = pathlib.Path(__file__).resolve().parents[1] / "resources"
MODEL_FILE_NAME = 'model-fine-tuned.hdf5'

if MODEL_FILE_NAME:
    MODEL_PATH = RESOURCES_FOLDER / MODEL_FILE_NAME

### Model Settings

MAX_TOKENS = 512

NER_TAGS = {
    'B-ade': 0,
    'B-drug': 1,
    'I-ade': 2,
    'I-drug': 3,
    'O': 4}

# Annotation Settings
ANNOTATION_INPUT = 'Sentence'

# Averbis Types

DOCUMENT_TYPE = 'uima.tcas.DocumentAnnotation'
SENTENCE_TYPE = 'de.averbis.extraction.types.Sentence'
TOKEN_TYPE = 'de.averbis.extraction.types.Token'
PREDICTED_TYPE = "de.averbis.extraction.types.Entity"

ANNOTATION_INPUT_DICT: dict = {
    'Document': DOCUMENT_TYPE,
    'Sentence': SENTENCE_TYPE
}
