# to be entered
import os

# import IPython
# import matplotlib
# import matplotlib.pyplot as plt
# import requests
import torch
import torchaudio

# matplotlib.rcParams["figure.figsize"] = [16.0, 4.8]

torch.random.manual_seed(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(torch.__version__)
print(torchaudio.__version__)
print(device)
print()

'''
SPEECH_URL = "https://pytorch-tutorial-assets.s3.amazonaws.com/VOiCES_devkit/source-16k/train/sp0307/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav"  # noqa: E501
SPEECH_FILE = "_assets/speech.wav"

if not os.path.exists(SPEECH_FILE):
    os.makedirs("_assets", exist_ok=True)
    with open(SPEECH_FILE, "wb") as file:
        file.write(requests.get(SPEECH_URL).content)
'''
# This block isn't necessary because I already have a wav file saved.
# Let's see if we encounter codec problems though. monkaS

SPEECH_FILE= r"~\wavpath.wav"
if __name__=="__main__":
    from sys import argv
    if len(argv)==2:
        SPEECH_FILE = argv[1]
# Perhaps this is sufficient...

bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H

print("Sample Rate:", bundle.sample_rate)
print("Labels:", bundle.get_labels())

# Is the above model correct? Notes a 16K Sample Rate...
model = bundle.get_model().to(device)
print(model.__class__)
print()

# IPython.display.Audio(SPEECH_FILE)
# Who uses IPython anymore?

# From PyTorch Tutorial:  If the sampling rate is different from what the pipeline expects, then we can use torchaudio.functional.resample() for resampling. See above concern on sample rate.

waveform, sample_rate = torchaudio.load(SPEECH_FILE)
waveform = waveform.to(device)

if sample_rate != bundle.sample_rate:
    waveform = torchaudio.functional.resample(waveform, sample_rate, bundle.sample_rate)
# Oh Neat! They did the heavy lifting for me! That if/resample stanza is beautiful!

'''
with torch.inference_mode():
    features, _ = model.extract_features(waveform)
fig, ax = plt.subplots(len(features), 1, figsize=(16, 4.3 * len(features)))
for i, feats in enumerate(features):
    ax[i].imshow(feats[0].cpu())
    ax[i].set_title(f"Feature from transformer layer {i+1}")
    ax[i].set_xlabel("Feature dimension")
    ax[i].set_ylabel("Frame (time-axis)")
plt.tight_layout()
plt.show()
'''
# The above views the tensors which are outputs of a transformation layer. Wow!
# The above ALSO causes my entire environment to crash, HORRIBLY!
# The error comes from the dlls on the matplotlib module, so removed all the cool charts for this example.

with torch.inference_mode():
    emission, _ = model(waveform)
'''
plt.imshow(emission[0].cpu().T)
plt.title("Classification result")
plt.xlabel("Frame (time-axis)")
plt.ylabel("Class")
plt.show()
print("Class labels:", bundle.get_labels())
'''
# From the PyTorch Tutorial: Wav2Vec2 model provides method to perform the feature extraction and classification in one step. ... The output is in the form of logits. It is not in the form of probability.
# Let's just purge the plot and "extra" features of this tutorial.

class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def forward(self, emission: torch.Tensor) -> str:
        """Given a sequence emission over labels, get the best path string
        Args:
          emission (Tensor): Logit tensors. Shape `[num_seq, num_label]`.

        Returns:
          str: The resulting transcript
        """
        indices = torch.argmax(emission, dim=-1)  # [num_seq,]
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        return "".join([self.labels[i] for i in indices])

# Chewing...

decoder = GreedyCTCDecoder(labels=bundle.get_labels())
transcript = decoder(emission[0])
# Swallowing...

# Choking to death...
# Alone...
# With nobody to perform abdominal thrust...
# Is this...
# Gum under my chair?
# <CURTAINS>

def script_cleaner(transcript):
    import re
    transcript= transcript.replace('|',' ').lower()
    numeric_digits= {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'zero': '0',
        }
    for k in numeric_digits:
        transcript= transcript.replace(k, numeric_digits[k])
    transcript= re.sub('(?<=\d) (?=\d)+', '', transcript)
    for k in numeric_digits:
        transcript= transcript.replace(' '+numeric_digits[k]+' ', ' '+k+' ')
    return transcript

print(script_cleaner(transcript))
# Should really do more NLTK to clean up this output because it looks bad.
