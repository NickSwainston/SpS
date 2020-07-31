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
RUN pip install . && \
    cythonize -i sps/src/C_Funct.pyx && \
    cp sps/src/C_Funct* /opt/conda/lib/python3.7/site-packages/sps/src/