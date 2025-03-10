import textwrap

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from filewriter import writefile
from utils import test_cuda

# MODEL_ID = "openai/whisper-large-v3"
MODEL_ID = "openai/whisper-large-v3-turbo"


def speech_to_text(mp3_file, path, output, fine_grained=True):
    test_cuda()
    device = "cuda"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        MODEL_ID, torch_dtype=torch_dtype, low_cpu_mem_usage=True  # , use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(MODEL_ID)

    rts = "word" if fine_grained else True
    chunk_length_s = 5 if fine_grained else 20
    batch_size = 2 if fine_grained else 16
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=chunk_length_s,
        batch_size=batch_size,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=rts,
        # generate_kwargs={"use_flash_attention_2": True},
    )

    result = pipe(mp3_file)
    # sometimes tokenization_whisper.py throws error: TypeError: '<=' not supported between instances of 'NoneType' and 'float'
    # update the file locally according to this pr: https://github.com/huggingface/transformers/pull/33625/files
    # then install it from local repo using `pip install /path/to/transformers`
    text = textwrap.fill(result["text"], width=120)
    writefile(text, path, f"{output}_original_transcription", "txt")

    return result
