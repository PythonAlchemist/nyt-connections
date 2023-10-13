# nyt-connections

Use LLMs to solve NYT Connections

# Setup

## Install dependencies

Setup Conda environment:

```
conda env create -f dev.yml
conda activate connections
```

# Data

Previous answers were scrapped from a blog following the nyt connections puzzle. The data is stored in `data/connections.csv` in it's raw state. The Dataset class contains cleaning methods for better use.

# Strategy

## 1. Use GPT-4 to generate 4x4 classification

Let's try to leverage the contextual understanding that GPT-4 contains and group all 4 sets of words in one shot, with the model exposing it's favorite for judging. We can then chat with the model to iterate
on it's answers by providing feedback just like humans would playing the game. We need to pass previous answers to the model to help it understand the context of the game. I have a feeling the way we describe
these examples to the model will have a larger impact than quantity of samples. GPT-4 is a stellar few shot learner. This will get pricey

## 2. Use OpenAI Embeddings

embedd each of the words and use a 16x16 distance matrix to find the closest words to each other. This implementation should be pretty cheap and is very deterministic and testable.

## 3. Fine Tune GPT-3.5

Use the GPT-3.5 model to fine tune on the connections dataset. This method will allow us to pass more training data into the model and have much cheaper inference costs
