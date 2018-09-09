# Introduction
The dataset used for this project is a small chunk of comments parsed from Hacker News forums in JSON format. Dataset consists of 10000 comments made by 2719 users and doesn't contain sentiment labels.

While VADER Sentiment Analysis is used for this project to perform a sentiment analysis, there are many other tools available for unsupervised sentiment analysis, such as AFINN, SentiWordNet, NVDIA Sentiment Discovery and Stanford CoreNLP to name a few.

# Setup
It is recommended to create a virtual environment to seperate the development environments of different projects, however this is completely optional. If you have Anaconda installed on your computer, you can create a new environment by:
``` python
conda create -n YOUR_ENV_NAME python=3.6
```

To run the scripts:
``` python
cd /PATH_TO_FOLDER/sentiment-analysis
```
Optional: (if you are using a virtual environment)
``` python
source activate YOUR_ENV_NAME
```
To install the dependencies:
``` python
pip install -r requirements.txt
```
To run the python scripts:
``` python
cd /PATH_TO_FOLDER/sentiment-analysis/scripts
python sentiment_analysis.py
```
To launch and run the notebooks and override the data rate limit:
```
jupyter-notebook --NotebookApp.iopub_data_rate_limit=10000000000
```
