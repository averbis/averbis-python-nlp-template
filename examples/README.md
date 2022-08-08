# Averbis Deep Learning Template - Examples

# [Use Case 1 - Sentence Classification][EXAMPLE1]

In this [example][EXAMPLE1] a self-trained CNN model is used to detect adverse drug events (ADEs) on the sentence level. The Annotator creates annotations (relevant or not relevant) for each sentence.

# [Use Case 2 - Sequence Labeling][EXAMPLE2]

In this [example][EXAMPLE2], all drug and adverse events Entities are annotated. The initial model is loaded using the Hugging Face, and the weights are loaded locally.

Entities on the token level are merged to entity-level in the post-processing. 

# [Use Case 3 - Text Summarizer][EXAMPLE3]

This [example][EXAMPLE3] displays the usage of summarizer model taken from the Hugging Face Model Hub without any pre- or postprocessing.


[CONFIG_FILE]: ../main/averbis-nlp-service/src/config.py
[EXAMPLE]: ../main/examples
[EXAMPLE1]: ../main/examples/sentence_classification
[EXAMPLE2]: ../main/examples/sequence_labeling
[EXAMPLE3]: ../main/examples/text_summarizer
[HuFaHUB]: https://huggingface.co/models
[MODEL_FILE]: ../main/averbis-nlp-service/src/Model.py
[UIMA]: https://uima.apache.org/