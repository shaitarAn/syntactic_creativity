import torch
import os
import csv
from nltk import Alignment
import argparse
import numpy as np
# from utils import normalize_punct
from transformers import AutoModel, AutoTokenizer
from calculate_xwr import *

