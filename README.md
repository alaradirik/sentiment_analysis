It is recommended to create a virtual environment to seperate the development environments of different projects. If you have Anaconda installed on your computer, you can create a new environment by:
conda create -n YOUR_ENV_NAME python=3.6 

To run the files:
cd /PATH_TO_FOLDER/sentiment-analysis

optional: (if you are using a virtual environment)
source activate YOUR_ENV_NAME

pip install -r requirements.txt
To run the python scripts:
python main.py
Or launch the notebook and override the data rate limit:
jupyter-notebook --NotebookApp.iopub_data_rate_limit=10000000000