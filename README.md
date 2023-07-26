# Poker-AI

Poker Project with agents that can play Texas Hold'em No Limit.
There's also a clustering to get the types of Poker Players around the table.

We use texasholdem library :
* Code : https://github.com/SirRender00/texasholdem
* Doc : https://texasholdem.readthedocs.io/en/0.10/getting_started.html

# Install

You need Python 3.11 (or newer version).

Then git clone this repository (enther that command in a command prompt) : 

```bash
git clone git@github.com:LucasColas/Poker-AI.git
```

Go to the repository

```bash
cd Poker-AI
```

Now, you need to install the dependencies. 

You can either use requirements file or Poetry to install dependencies. 

## With Poetry
If you want to instal dependencies with Poetry. First, install [poetry](https://python-poetry.org/).

Create virtual environment :
```bash
poetry env use python
```

Then, activate virtual environment : 
```bash
poetry shell
```

Then, just run : 
```bash
poetry install
```



Finally, you can run the code.
You just need to run `main.py` :
```bash
python main.py
```
or 
```bash
python .\main.py
```

## With requirements.txt
Create a virtual environment (or not, it's up to you).
Then run the command : 
```
pip install -r requirements.txt
```

Finally, you can run the code.
You just need to run `main.py` :
```bash
python main.py
```
or 
```bash
python .\main.py
```

