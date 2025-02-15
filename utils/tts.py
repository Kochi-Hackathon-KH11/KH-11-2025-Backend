from transformers import pipeline
import torch
from datasets import load_dataset
MODEL_ID = 'microsoft/speecht5_tts'
synthesizer = pipeline('text-to-speech', MODEL_ID)

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)


def text_to_speech(text):
    """
    Converts input text to speech using the SpeechT5 model.

    Args:
        text (str): The text to be converted into speech.

    Returns:
        dict: A dictionary containing:
            - 'audio': The generated speech waveform.
            - 'sampling_rate': The sampling rate of the generated audio.
    """
    speech = synthesizer(text, forward_params={"speaker_embeddings": speaker_embedding})
    return speech


