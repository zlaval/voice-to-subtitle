import torch

# Remove this and set device = "cpu" to run on CPU instead of GPU
# Set device to "cuda:index" (eg cuda:0 if you have multiple GPUs) to run on GPU
def test_cuda():
    if not torch.cuda.is_available():
        raise Exception("CUDA not available")