# RxWikipeadiaSearcherExample

## Steps to setup app

1. Make sure you have [Python3.7](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/) installed.
1. *(Optional)* Create a new virtual environment: `python3.7 -m venv venv`, and activate it `source venv/bin/activate`
1. Install required packages (rx and tornado): `pip install -r requirements.txt`

## Steps to start the app

1. *(Optional)* Set the `PORT` environment variable: `export PORT=8081`, by default app will listen `http://localhost:8080`
1. Run the app: `python main.py`
1. Proceed to the link from console or just type in browser: `http://localhost:{PORT}`
