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

import numpy as np
import pathlib

from tensorflow.python.keras.models import load_model
from typing import Any

from src import config
from src.classification.util.parameters import CNNConfigManager
from src.neuralcore.utils.alphabet import DatasetAlphabet, LabelAlphabet
from src.neuralcore.utils.embedding import Embedding as AverbisEmbedding


class Model:

    def __init__(self):

        self._asset_path: pathlib.Path = config.RESOURCES_FOLDER / 'assets'
        self._hdf5_path: pathlib.Path = config.RESOURCES_FOLDER / 'model.hdf5'

        self._configs: CNNConfigManager = CNNConfigManager(self._asset_path)

        self._dataset_alphabet: DatasetAlphabet = DatasetAlphabet(self._asset_path / "dataset.alphabet")
        self._embedding: AverbisEmbedding = AverbisEmbedding.from_config(self._configs)
        self._embedding.set_dataset_alphabet(self._dataset_alphabet)
        self._embedding.pad_token = self._embedding.unk_token

        self._inv_label_alphabet = LabelAlphabet(self._asset_path / "dataset.labelalphabet").get_reverse_mapping()

        if self._hdf5_path.exists():
            self._model = load_model(self._hdf5_path)
        else:
            self._model = load_model(config.RESOURCES_FOLDER)

        self._model.compile()

    def preprocess_model_input(self, text_input: str):
        """
        Calculates word embeddings for model.

        Returns:
            Text embeddings of text to annotate

        """

        return self._embedding.encode([text_input],
                                      max_length=config.MAX_TOKENS)

    def postprocess_model_output(self, model_output: Any) -> tuple:
        """
        Extracts label and confidence from model output.

        Args:
            model_output: Output from model.

        Returns:
            tuple(label, confidence)
        """

        label = config.ANNOTATION_OUTPUT_DICT[np.argmax(model_output, axis=-1)[0]]
        confidence = np.max(model_output, axis=-1)[0]

        return label, confidence

    def predict(self, text_input: str) -> tuple:

        model_input = self.preprocess_model_input(text_input)

        prediction = self._model.predict(x=model_input.astype(float),
                                         batch_size=self._configs.BATCH_SIZE.value)

        return self.postprocess_model_output(prediction)

