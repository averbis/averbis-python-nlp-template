# Example 1 - Sentence Classification - ADE Detection

This example highlight the detections of adverse drug events (ADE). Each sentence is classified for the absence (not relevant) or the presence (relevant) ADE.

## Model Set Up

### Model Initializing

The `sentence_classification\resources` folder contains several files required for the model (not tracked by GitHub). 

In the `__init__` method of the `model` class, the model is loaded using tensorflow. Additionally, proprietary classes load the model configuration and the embeddings of the model.

### Pre-processing of inputs

In the `preprocess_model_input` method, the input text is converted into a numerical representation using word embeddings.

### Prediction of inputs
 
The `predict` method is a simple wrapper for the `predict` method of the tensorflow method of the model. 

### Post-processing of model outputs

The output of the model is a numpy array representing the label and the confidence numerically. Numpy is used to extract the label and the confidence, which are returned to the `Annotator` class.

## Sentence classification annotations

Exemplary annotation for an input sentence: 

```
annotation = {
                "begin": 0,
                'end': 25,
                "value": relevant,
                'label': 'ade-sentence-classification',
                'confidence': 0.68,
                'componentId': 'ade-sentence-classifier:0.1.0'
            }

