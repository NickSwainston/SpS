FROM continuumio/miniconda3

COPY conda.yml .
RUN \
   conda env update -n root -f conda.yml \
&& conda clean -a

RUN pip install Cython matplotlib

RUN apt-get update && \
    apt-get -y install gcc \
    procps

WORKDIR /home/soft
COPY . /home/soft
RUN cythonize -i /opt/conda/lib/python3.7/site-packages/sps/src/C_Funct.pyx && \
    pip install .