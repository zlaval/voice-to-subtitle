import torch
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

from utils import test_cuda


def translate_fbm2m100(ts_text,src_lang,tgt_lang):
    test_cuda()
    device = "cuda"

    model_name = "facebook/m2m100_1.2B"

    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name).to(device)

    tokenizer.src_lang = src_lang

    result = []


    for item in ts_text:
        # if a sentence is too long and not separated with comma, then lines should be joined
        # till the sentence is complete, but this is not important yet
        text = item["line"]
        inputs = tokenizer(text, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        result.append({
            "line": translated_text,
            "start_time": item["start_time"],
            "end_time": item["end_time"]
        })

    return result