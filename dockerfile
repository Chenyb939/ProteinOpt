# tested
FROM ubuntu:18.04
MAINTAINER Zilin Ren "zilin.ren@outlook.com"

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list  

RUN apt-get clean && \
apt-get update --fix-missing && \
apt-get clean

RUN apt-get install build-essential -y
RUN apt-get install libboost-dev -y 
RUN apt-get install python -y
RUN apt-get install zlib1g zlib1g-dev lib32z1-dev -y
RUN apt-get install clang libicu-dev -y
RUN apt-get install libopenmpi-dev openmpi-bin -y
RUN apt-get install vim ssh -y
RUN apt-get install openmpi-bin openmpi-doc libopenmpi-dev -y 

RUN wget -c --http-user=<account> --http-passwd=<password> https://www.rosettacommons.org/downloads/academic/2022/wk11/rosetta.source.release-314.tar.bz2

RUN tar -xjf rosetta.source.release-314.tar.bz2 


WORKDIR rosetta.source.release-314/main/source/
RUN python ./scons.py -j 20 mode=release bin 
RUN python ./scons.py -j 20 mode=release bin extras=mpi
RUN echo export PATH=$PATH:`pwd`/bin >> ~/.bashrc


WORKDIR / 
RUN rm rosetta.source.release-314.tar.bz2