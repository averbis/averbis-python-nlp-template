# Base Image - Determines Tensorflow/Cuda Version
FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

### Environment settings
# User/Paths settings
ENV USER=averbis
ENV UID=1000 
ENV HOME=/home/$USER
ENV PYTHONPATH "${PYTHONPATH}:$HOME/src"
ENV PATH "$PATH:$HOME/.local/bin"

# Update Container and install curl
RUN apt-get update \
    && apt-get full-upgrade -y

# User Setup
USER root

RUN adduser --disabled-password --gecos "Default user" --uid $UID $USER \
    && chown -R $UID $HOME \
    && chmod u+rwX $HOME

USER $USER

# Copy essential files to container
COPY requirements.txt $HOME
COPY averbis-nlp-service $HOME

# Install Python dependencies
WORKDIR $HOME
RUN pip install  --force-reinstall -r requirements.txt

# Expose Port
EXPOSE 5000

# Start uvicorn server hosting the API
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]