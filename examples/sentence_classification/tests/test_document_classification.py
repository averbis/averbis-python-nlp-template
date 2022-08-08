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

from src import config
from src.Annotator import Annotator

from tests.test_utils import prepare_cas_for_test


def test_predict():
    """
    """
    annotator = Annotator()

    text = "Cisplatin causes headaches. "
    cas = prepare_cas_for_test(text)

    annotator.predict(cas=cas)

    predictions = cas.select(config.PREDICTED_TYPE)
    expected = {
        "value": "relevant",
        "confidence": 0.7975344
    }

    assert len(predictions) > 0
    for prediction in predictions:
        assert prediction.value == expected['value']
        assert prediction.confidence == expected['confidence']
