#!/bin/bash

env=iamskin

conda create -y -n $env python=3.7
conda activate $env
pip install -r requirements.txt