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

from pathlib import Path
from cassis import Cas
from src.Annotator import Annotator

from tests.test_utils import prepare_cas_for_test


def test_predict():
    """
    """
    annotator = Annotator()

    text = """Human cleavage-stage embryos frequently acquire chromosomal aneuploidies during mitosis due to unknown mechanisms. Here, we show that S phase at the 1-cell stage shows replication fork stalling, low fork speed, and DNA synthesis extending into G2 phase. DNA damage foci consistent with collapsed replication forks, DSBs, and incomplete replication form in G2 in an ATR- and MRE11-dependent manner, followed by spontaneous chromosome breakage and segmental aneuploidies. Entry into mitosis with incomplete replication results in chromosome breakage, whole and segmental chromosome errors, micronucleation, chromosome fragmentation, and poor embryo quality. Sites of spontaneous chromosome breakage are concordant with sites of DNA synthesis in G2 phase, locating to gene-poor regions with long neural genes, which are transcriptionally silent at this stage of development. Thus, DNA replication stress in preimplantation embryos predisposes gene-poor regions to fragility, and in particular in the human embryo, to the formation of aneuploidies, impairing developmental potential. """

    cas = prepare_cas_for_test(text)

    annotator.predict(cas=cas)

    predictions = cas.select(config.PREDICTED_TYPE)

    expected = {
        "summary": "DNA Synthesis in cleavage-stage embryos leads to chromosome breakage and segmental aneuploidies during mitosis, impairing the embryo's developmental potential and ability to acquire long neural genes, which are transcriptionally silent at this stage of development."
    }

    assert len(predictions) > 0
    for prediction in predictions:
        assert expected['summary'] == prediction.value
