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

from fastapi import FastAPI

from src import utils
from src.PredictionRequest import PredictionRequest
from src.Annotator import Annotator

annotator = Annotator()

app = FastAPI()


@app.post("/annotate")
async def annotate(annotation_request: PredictionRequest):

    cas = utils.process_annotation_request(annotation_request)

    annotator.predict(cas=cas)

    return {"document": cas.to_xmi()}

