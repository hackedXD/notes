# Find the missing card in a deck

### Setup the problem
You have a deck of cards, with one card missing. Your objective is to find the missing card. Firstly, you would have to generate this deck of cards.

```python
def generate_deck():
	deck = []
	for suite in ["spades", "clubs", "hearts", "diamonds"]:
		for no in range(1, 14):
			deck.append({
				"suite": suite,
				"no": no
			})
	return deck
```

This code generates the deck as a list of dictionaries with the following format ->

```python
[
	{
		"suite": "spades",
		"no": 1
	},
	{
		"suite": "hearts",
		"no": 5
	},
	{
		"suite": "diamonds",
		"no": 2
	},
	...
]
```


### My First Approach

So the first idea that came to mind, would be to loop over a normal deck, and check exactly which card isn't inside of the deck with the missing card. Here is it implemented. 

```python
@log_time
async def loop_and_check(deck):

	normal_deck = generate_deck()
	
	searches = 0
	
	for card in normal_deck:
		if not card in deck:
			return card, searches
	
	searches += 1
```

Output ->
```
loop_and_check: Took 51ms
                38 Searches
                Card: 1 of diamonds
```

### Sorted Suites
Another approach would be to sort the deck by the suite then check which suite would have the abnormal amount of cards.
```python
@log_time
async def sorted_suites(deck):
	
	# SORTING
	sorted_deck = {
		"spades": [],
		"clubs": [],
		"hearts": [],
		"diamonds": []
	}
	
	for card in deck:
		sorted_deck[card["suite"]].append(card)
	
	abnormal_suite = ""
	
	for suite in sorted_deck:
		if not len(sorted_deck[suite]) == 13:
			abnormal_suite = suite
	
	normal_suite = generate_deck(shuffle=False, suites=[abnormal_suite])
	
	searches = 0
	
	for card in normal_suite:
		if not card in sorted_deck[abnormal_suite]:
			return card, searches
		searches += 1
```

If you take the sort only, it takes around 6-8 ms.

```
sorted_suites:  Took 7ms
                0 Searches
                Card: None of None
```

However, Due to the lower amount of searching necessary, total time (10ms - 20ms) is way lower than the one of the method above.

```
sorted_suites:  Took 12ms
                11 Searches
                Card: 12 of clubs
```


