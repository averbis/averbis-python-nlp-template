# Averbis Python NLP template

This project serves as a template to integrate any Deep Learning or other model accessible in Python with Information Discovery.

Models are set up and hosted in a separate Docker container running within the same Docker compose context as the Information Discovery. A pipeline component in Information Discovery manages communication between Information Discovery and the container hosting the model via a REST API. In general, communication with Information Discovery is handled by the template. Template users only need to set up their model and define the annotations.  

This project provides 
* The `Dockerfile` defining the settings of the container hosting the Python model
* The  `averbis-nlp-service-0.1.0-docker-compose.yml` compose file, used to start the averbis-nlp-service Docker image in the same Docker compose context as the Information Discovery
* The folder `averbis-nlp-service` containing the required Python code and resources necessary for receiving and processing requests

# General Usage

To make use of the template, the following steps are necessary to make annotations using your model.

0. [Setting up the Python environment](#setting-up-the-python-environment)
1. [Model definition](#model-definition)
   1. [Model Loading](#model-loading)
   2. [Pre-processing of model inputs](#pre-processing-of-model-inputs) 
   3. [Post-processing of model outputs](#post-processing-of-model-outputs)
2. [Adding the Annotations](#adding-the-annotations)
3. [Test your implementation](#test-your-implementation)
4. [Adapting of Dockerfile and Docker compose file](#adaption-of-dockerfile-and-docker-compose-file)

Central settings are saved in the [config file][CONFIG_FILE] `src/config.py`.

## Setting up the Python environment

We recommend setting up a separate Python environment for each project. Copy the project template to a new folder, and set up the virtual environment. The `requirements_basic.txt` file contains libraries necessary for receiving requests from and sending annotations to Information Discovery. To install the basic requirements, activate the virtual environment and install the dependencies:

```
pip install -r requirements_basic.txt
```
All dependencies necessary for model prediction need to be installed on top of the base dependencies. Once all dependencies are installed, create a new `requirements.txt` file: 

```
pip freeze > requirements.txt
```

Move the file `requirements.txt` to the same level as the `requirements_basic.txt` file. When building the Docker image, the `requirements.txt` file will be copied to the image, and the Python libraries added to the `requirements.txt` will be installed.  

## Model definition

The Model is defined in the `src/Models` [class][MODEL_FILE]. All ML/DL models trained using Python libraries can be integrated. Depending on the model, pre- or post-processing of model inputs or outputs are required. The input of the models commonly are either full documents or sentences.

The first step in setting up the model is defining whether the model input is the full document, or individual sentences. In [example 1][EXAMPLE1], classifications are carried out for each sentence. Similarly, in [example 2][EXAMPLE2] drug and ADE entities are recognized on the sentence level. [Example 3][EXAMPLE3] demonstrates summarizing whole documents. 

The model input is dependent on the model and is set in `src/config.py`. In User Settings, you can set the `ANNOTATION_INPUT` either to "Sentence" or "Document". Please make sure the spelling and case is correct.

### Model loading

In this step, the model used for prediction is set up. The most common ways to load a model are:
* loading a local model
* loading a model from the Hugging Face Model Hub or any other API
* loading a model from a separate Docker model image

#### Loading a local model

To load a model locally, copy the model and all required resources in the `averbis-nlp-service/resources` folder. Access to the folder path is defined in [config file][CONFIG_FILE] `src/config.py`. You can enter the file name of the model file in the `averbis-nlp-service/resources` folder. From the `src/Models` [class][MODEL_FILE], the model path can be accessed with `config.MODEL_PATH`. See [example 1][EXAMPLE1] and [example 2][EXAMPLE2] for a detailed example on loading a local model.

#### Loading a model from a Python API

Many Python libraries offer downloading models ready-to-use using an api. To load these models, simply use the methods provided in the respective libraries.

 In [example 2][EXAMPLE2], a base model is downloaded from the HuggingFace Model Hub [HuFaHUB], and the models weights are updated from a local model file within the `averrbis-nlp-service/resources` folder. In [example 3][EXAMPLE3], a model is imported from the HuggingFace Model Hub [HuFaHUB] and is used as downloaded. 

#### Loading a model from a separate Docker model image

It is recommended to version not only the code in repository, but also the model used for classification. To this end, it can be beneficial to save the model in a separate versioned Docker image and copy the model from the model image during the build of the averbis-nlp-service container image. 

To do so, the [Dockerfile][DOCKERFILE] needs to be updated to copy the image in the `averbis-nlp-service/resources` folder. Fill in the values in the brackets, and add the line of code in the section *Copy essential files to container* .
```
COPY --from=[docker-image-path] [Model Path in Docker image] $HOME/resources
```

The *docker-image-path* points to the docker registry path of the model image and the *Model Path in Docker image* to the path of the model within the model docker image. 

### Pre-processing of model inputs

The pre-processing of model inputs includes all required steps for the model to interpret text inputs. The `src/Models` [class][MODEL_FILE] contains a method `preprocess_model_input`, in which pre-processing is performed. 

In [example 2][EXAMPLE2] and [example 3][EXAMPLE3] all pre-processing steps are carried out by the transformers `pipeline` object, simplifying pre- and post-processing massively. 

[Example 1][EXAMPLE1] displays how the text input is embedded using self-trained embeddings loaded from the `averbis-nlp-service/resources` folder.
 
### Post-processing of model outputs

Post-processing of model outputs encompasses all steps to format the model output into a format to use in the annotations. The `src/Models` [class][MODEL_FILE] contains a method `postprocess_model_input`, in which post-processing can be added. 

Post-processing can be simple, just extracting the required information from the model outputs (see [example 1][EXAMPLE1] and [example 3][EXAMPLE3]). Depending on the outputs of the model, the post-processing can be more complex (see [example 2][EXAMPLE2]).

## Adding annotations

The natural language processing capabilities of Averbis are powered by the [Apache UIMA][UIMA] framework. Within this framework, all documents are represented as `Cas` objects. During processing of the documents in Information Discovery, a `Cas` object is sent to the `averbis-nlp-service` container, which adds the annotations carried out by the model to the `Cas` object. 

The annotations added are of the type `de.averbis.extraction.types.Entity`, and contain the following information:
* begin: The start index of a given annotation.
* end: The end index of a given annotation.
* label: The name of the provided annotation (eg. ade-classification)
* value: The label or text of the annotation provided by the model (eg. relevant). 
* confidence: The confidence of the prediction provided by the model (eg. 0.89)
* componentId: The name of the container/the model doing the prediction (eg. ade-classifier:0.1.0).

The post-processing of the model outputs should provide the information necessary to fill the annotation fields. 


## Test your implementation

The template project contains the folder `averbis-nlp-service\tests`, which is used to verify whether the model set up was successful. The [pytest framework][pytest] is used for testing.

The `averbis-nlp-service\tests` folder contains two files, `test_utils.py` contains code for converting text input in to `Cas` files required for the annotation. `test_averbis-nlp-service.py` contains the `test_predict` test users need to adapt to their models outputs.  

Enter a text to predict at line 18, and define your expected annotations in line 27. Then, use `assert` statements to verify the annotations. To run tests, the `pytest` module needs to be installed. Navigate to `./averbis-nlp-service/tests` and enter:

```
pytest
```

Check the [examples][EXAMPLE] for more details.

## Adapting the Dockerfile and Docker compose file

Both files are required to start the Docker container hosting the Python model. The `Dockerfile` contains all commands used for setting up the Docker image of the averbis-nlp-service container. Commonly, changes in the Docker file are not required. 

The Docker compose file `averbis-nlp-service-0.1.0-docker-compose.yml` defines the network context for both, the averbis-nlp-service container and Information Discovery.

There are two parameters in the `averbis-nlp-service-0.1.0-docker-compose.yml` file, which might require updates by the user. 

The service name (line 3) is set to `nlp-service` by default. The name of the service name must be unique within the Docker compose context, therefore the service name has to be updated in case multiple containers hosting Python models are in use.

The image path (line 4) might be adapted pointing to the path and name of the image averbis-nlp-service image. If the Docker image was build locally, no path is necessary, only the name of the image. 

### Build the averbis-nlp-service Docker image

Prior to using the averbis-nlp-service, the Docker image needs to be build. To do this locally, navigate to the top level and enter:
```
docker build -t averbis-nlp-service:0.1.0  .

(generic) docker build -t [name of docker image]:[version] .
```

In this case the image name (line 4) in the Docker compose file is `averbis-nlp-service:0.1.0`.

### Start the averbis-nlp-service Docker image with Docker compose

To start the averbis-nlp-service container in the same Docker compose context as Information Discovery, both need to be started together. In case Information Discovery is running, it can be shut down by entering. Make sure to time the shutdown to not interfere with ongoing text analyses.

```
docker compose -f [Information Discovery Docker compose file name] down
```

To start both services in the same Docker context, enter:

```
docker compose -f [Information Discovery Docker compose file name] -f averbis-nlp-service-0.1.0-docker-compose.yml up -d
```

Make sure the image name in averbis-nlp-service-0.1.0-docker-compose.yml is the same used when building the image.

# Examples

An overview over examples can be found [here][EXAMPLE]


[CONFIG_FILE]: ../main/averbis-nlp-service/src/config.py
[DOCKERFILE]: ../main/Dockerfile
[EXAMPLE]: ../main/examples
[EXAMPLE1]: ../main/examples/sentence_classification
[EXAMPLE2]: ../main/examples/sequence_labeling
[EXAMPLE3]: ../main/examples/text_summarizer
[HuFaHUB]: https://huggingface.co/models
[pytest]: https://docs.pytest.org/en/7.1.x/
[MODEL_FILE]: ../main/averbis-nlp-service/src/Model.py
[UIMA]: https://uima.apache.org/