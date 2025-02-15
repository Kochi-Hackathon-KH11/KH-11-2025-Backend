from transformers import pipeline
import torch
from datasets import load_dataset
MODEL_ID = 'microsoft/speecht5_tts'
synthesizer = pipeline('text-to-speech', MODEL_ID)

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)


def text_to_speech(text):
    speech = synthesizer(text, forward_params={"speaker_embeddings": speaker_embedding})
    return speech


