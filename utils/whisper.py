from transformers import pipeline
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch
import numpy as np

MODEL_ID = 'arielcerdap/largev3-turbo-stutter'


device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32


processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    MODEL_ID,
    torch_dtype=torch_dtype,
)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch.dtype,
    device=device
)

def test_file(input_file):
    response = pipe(input_file)
    return response

def test_buffer(buffer):
    print(buffer)
    response = pipe({ 'raw': np.array(buffer['audio']['array']), 'sampling_rate': buffer['audio']['sampling_rate']})
    return response
