FROM continuumio/miniconda:4.7.12

COPY conda.yml .
RUN \
   conda env update -n root -f conda.yml \
&& conda clean -a

RUN pip install Cython matplotlib

RUN apt-get update && \
    apt-get -y install gcc

WORKDIR /home/soft
COPY . /home/soft
RUN pip install . && \
    cythonize -i sps/src/C_Funct.pyx && \
    chmod +x sps/sps.py
    
ENV PATH="/home/soft/sps:${PATH}"
