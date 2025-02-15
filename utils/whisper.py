from transformers import pipeline
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch
import re

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

def clean_text(input_text):
    text = re.sub(r'\s+a\s+(?=\w+)', ' ', input_text)  # "a" between words
    
    for _ in range(2):
        text = re.sub(r'\b(\w+\s\w+\s\w+)( \1)+\b', r'\1', text)
        text = re.sub(r'\b(\w+\s\w+)( \1)+\b', r'\1', text)
        text = re.sub(r'\b(\w+)( \1)+\b', r'\1', text)
    
    interjections = ["damn it", "uh", "um"]
    for expr in interjections:
        text = re.sub(fr'\s*{expr}\s*', ' ', text)
    
    text = re.sub(r'\s+', ' ', text).strip()
    return text  

def speech_to_text_from_file(input_file):
    try:
        response = pipe(input_file)
        cleaned_text = clean_text(response['text'])
        return cleaned_text
    except:
        return None


# def speech_to_text_from_stream(input_stream):
#     try:
#         response = pipe({
#             "array": 
#         })
    
