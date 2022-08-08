# Example 3 - Text summarization

##Model Set Up

### Model Initializing

The `sentence_classification\resources` folder contains model weights from a fine-tuned model, saved as `model-fine-tuned.hdf5`(not tracked by GitHub). This file only contains the weights, not the model architecture. Therefore, the `model` class, is initialized by loading the base model from the Hugging Face model hub. Next, the models' weights are loaded from the `sentence_classification\resources`. In the last step, the model is wrapped in a transformers `pipeline`, which conveniently wraps pre-processing, prediction and post-processing in a single object. embeddings of the model.

### Pre-processing of inputs

The `pipeline` object pre-processes the model inputs according to the model' requirements. 

### Prediction of inputs
 
The `predict` method is a simple wrapper for the Hugging Face `pipeline` object. 

### Post-processing of model outputs

While the `pipeline` object converts to numerical outputs in a readable format, the annotations are on a token-level. 

## Sequence labeling annotations

An exemplary annotation for an input sentence: 

```
annotation = {
                "begin": 0,
                'end': 25,
                "value": "DNA Synthesis in cleavage-stage embryos leads to chromosome breakage and segmental aneuploidies during mitosis, impairing the embryo's developmental potential and ability to acquire long neural genes, which are transcriptionally silent at this stage of development.",
                'label': 'summary',
                'confidence': 0.68,
                'componentId': 'TextSummarizer:0.1.0'
            }
```