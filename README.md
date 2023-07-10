## MTG mana calculator

#### Credit to u/KumaTheBear72685 for the inspiration for this. 
His code can be found at https://docs.google.com/document/u/0/d/1H68Lp_EJp27l3dIi2zaTDZ27dUpwjDssx0VmdPTWiGA/mobilebasic?usp=gmail

I rewrote most of it to be more pythonic and reusable. The code in this repo is attempting to allow for this functionality to be dynamic and allow people to import decklists from other places, parse them using scryfall data, calculate mana production for a given card, and run lots of simulations for the given decks.


#### Usage
Create a venv and install requirements:
```shell
# create a venv
python -m venv mtg_venv

# Activate it
source mtg_venv/bin/activate

# Install requirements (just requests)
pip install -r requirements.txt
```

You can run the code in an IDE or directly from the terminal. Edit main.py to tweak the numbers. Command line args coming soon. 