from transformers import pipeline
from transformers import logging

logging.set_verbosity_error()

# โหลด FinBERT
classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")

