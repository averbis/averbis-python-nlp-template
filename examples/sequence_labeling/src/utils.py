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
import logging

from src.PredictionRequest import PredictionRequest


def setup_logging():
    """
    Configures Logging of Container
    """
    logging_formatting = "%(process)d-%(thread)d %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG,
                        format=logging_formatting)


def process_annotation_request(annotation_request: PredictionRequest):
    """
    Parses incoming prediction request

    Args:
        annotation_request: Incoming Prediction Request

    Returns:
        cas: Document to be annotated in cas format
        layer: Annotation type carried out by annotator - "de.averbis.extraction.types.Entity"
        feature: field name of annotation carried out - "label"
    """

    return cassis.load_cas_from_xmi(source=annotation_request.document['xmi'],
                                    typesystem=cassis.load_typesystem(annotation_request.typeSystem))


def postprocess_predictions(prediction_list: list):
    """

    Args:
        prediction_list:

    Returns:

    """

    separated_entities = separate_entities_from_bio(prediction_list)
    merged_entities = merge_entities_from_bio(separated_entities)

    return merged_entities


def separate_entities_from_bio(ner_annotations) -> list:
    """
    Takes in predictions of HuFa NER Model, and
    creates a list of individual entity lists.

    Arguments:
        ner_annotations: Annotation output from HuFa Token Classification Model

    Returns:
        entity_list: list of lists containing all annotations of given entity
    """
    entity_list = list()
    entity_current = list()

    for idx, cur_anno in enumerate(ner_annotations):

        if not entity_current:
            last_entity = cur_anno['entity'][2:]
            last_end = cur_anno['end']
            entity_current.append(cur_anno)

        else:

            if cur_anno['entity'][2:] == last_entity and cur_anno['start'] - last_end in [0, 1]:

                entity_current.append(cur_anno)
                last_end = cur_anno['end']

            else:
                entity_list.append(entity_current)
                entity_current = list()
                entity_current.append(cur_anno)
                last_entity = cur_anno['entity'][2:]
                last_end = cur_anno['end']

    entity_list.append(entity_current)

    return entity_list


def merge_entities_from_bio(entity_list) -> list:
    """
    Takes in list of lists containing all token annotations for
    an individual entity and merges them to list of entity annotation
    Arguments:
     entity_list: List of lists with token annotations for each entity

    Returns:
        merged_entities: list of merged annotations
    """
    merged_entities = list()

    for entity in entity_list:

        cur_entity_begin = entity[0]['start']
        cur_entity_end = entity[-1]['end']
        cur_entity = entity[0]['entity'][2:]
        cur_conf = 0
        cur_cov_text = ''

        for token_annotation in entity:
            cur_conf += token_annotation['score']
            cur_cov_text += token_annotation['word']

        if 'Ġ' in cur_cov_text:
            if cur_cov_text.startswith('Ġ'):
                cur_cov_text = cur_cov_text[1:]

            cur_cov_text = cur_cov_text.replace('Ġ', ' ')

        merged_entities.append({
            'tag': cur_entity,
            'begin': cur_entity_begin,
            'end': cur_entity_end,
            'confidence': cur_conf / len(entity),
            'value': cur_cov_text
        }
        )

    return merged_entities
