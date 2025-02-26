# Voice to subtitle
This project is a simple hobby voice to subtitle converter. 
It uses the OpenAI Whisper model to convert the audio to text.



## Dependencies
Dependencies are listed in `requirements.txt`. Install them using pip.
```bash
pip install -r requirements.txt
```

## Required programs
* Python 3.6 or higher
* Pip
* FFmpeg

## Usage

### Run the application
Multiple outputs will be saved. Extension is not required.
```bash
python main.py -f test.mkv -p ./testdata -o subtitle
```
### Translate the subtitle:
```bash
python main.py -f test.mkv -p ./testdata -o subtitle -s hu -t en
```


## Troubleshooting

#### 'CUDA not available' error
If your GPU supports cuda but still getting this error, 
try installing the correct version of torch.
Check the compatibility of your GPU with the version of torch 
from [here](https://pytorch.org/get-started/previous-versions/).

```
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

