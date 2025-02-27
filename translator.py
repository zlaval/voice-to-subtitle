import torch
import openai
from openai import AsyncOpenAI, OpenAI
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

from utils import test_cuda


def translate_fbm2m100(ts_text, src_lang, tgt_lang):
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


def translate_gpt(ts_text, src_lang, tgt_lang):
    with open("apikey.conf", "r") as file:
        api_key = file.readline().strip()

    client = OpenAI(
        api_key=api_key
    )

    result = []

    ## TODO batching should be added to avoid rate limiting
    for item in ts_text:
        text = item["line"]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Translate the following text from {src_lang} to {tgt_lang}."},
                {"role": "user", "content": text}
            ]
        )
        translated_text = response.choices[0].message.content

        result.append({
            "line": translated_text,
            "start_time": item["start_time"],
            "end_time": item["end_time"]
        })

    return result
