FROM continuumio/miniconda:4.7.12

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
    chmod +x sps/sps.py
    
#ENV PATH="${PATH}:/home/soft/sps:/home/soft/sps/src/waterfaller"
#ENV PYTHONPATH="/home/soft/sps:/home/soft/sps/src/waterfaller"
