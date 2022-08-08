# Example 2 - Sequence Labeling

This example highlights named entity recognition of drugs and adverse drug events (ADE). Occurrences of drugs and ADEs are identified and labelled.
##Model Set Up

### Model Initializing

The `sentence_classification\resources` folder contains model weights from a fine-tuned model, saved as `model-fine-tuned.hdf5`(not tracked by GitHub). This file only contains the weights, not the model architecture. Therefore, the `model` class, is initialized by loading the base model from the Hugging Face model hub. Next, the models' weights are loaded from the `sentence_classification\resources`. In the last step, the model is wrapped in a transformers `pipeline`, which conveniently wraps pre-processing, prediction and post-processing in a single object. embeddings of the model.

### Pre-processing of inputs

The `pipeline` object pre-processes the model inputs according to the model' requirements. 

### Prediction of inputs
 
The `predict` method is a simple wrapper for the Hugging Face `pipeline` object. 

### Post-processing of model outputs

While the `pipeline` object converts to numerical outputs in a readable format, the annotations are on a token-level in the [IOB format][IOB]. 

For example, the drug aspirin would be annotated as to separate entities:
```
annotation_1 = {
                "begin": 0,
                'end': 5,
                "value": aspir,
                'label': 'B-drug',
                'confidence': 0.98,
                'componentId': 'ADE_Sentence_SequenceLabeling-service:0.1.0'
            }
```

```
annotation_2 = {
                "begin": 5,
                'end': 7,
                "value": in,
                'label': 'I-ade-sequence-labeling',
                'confidence': 0.96,
                'componentId': 'ADE_Sentence_SequenceLabeling-service:0.1.0'
            }
```

The `post-processing` model iterates over all annotations, and merges annotations belonging to the same entities. 


## Sequence labeling annotations

The `Annotator` iterates over each sentence and creates drug and ADE annotations in the following format:

```
annotation = {
                "begin": 0,
                'end': 7,
                "value": "aspirin",
                'label': "drug',
                'confidence': 0.97,
                'componentId': 'ADE_Sentence_SequenceLabeling-service:0.1.0'
            }
```

[IOB]: https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)