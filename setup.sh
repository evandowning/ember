#!/bin/bash

# Download Anaconda3
wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh

# Run Anaconda setup
bash ./Anaconda3-2020.07-Linux-x86_64.sh -b -p /root/anaconda3/
source /root/anaconda3/bin/activate
conda init
source ~/.bashrc

# Update Anaconda
conda update conda -y

# Setup Ember
conda create -n ember python=3.6 anaconda -y
conda activate ember
conda config --add channels conda-forge
conda install --file requirements_conda.txt -y
python setup.py install

conda deactivate
