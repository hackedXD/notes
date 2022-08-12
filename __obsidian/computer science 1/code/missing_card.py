import asyncio
import random
from datetime import datetime
from functools import wraps

def log_time(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		start_time = datetime.now().microsecond
		ret_val, searches = await func(*args, **kwargs)
		delta_time = datetime.now().microsecond - start_time
		print(f"{func.__name__}:\tTook {delta_time}ms\n\t\t{searches} Searches\n\t\tCard: {ret_val['no']} of {ret_val['suite']}")
		return ret_val
	return wrapper

def generate_deck(shuffle=True, suites=["spades", "clubs", "hearts", "diamonds"], nos=range(1, 14)):
	deck = []
	for suite in suites:
		for no in nos:
			deck.append({
				"suite": suite,
				"no": no
			})
	
	if shuffle:
		random.shuffle(deck)

	return deck

@log_time
async def loop_and_check(deck):
	normal_deck = generate_deck()
	searches = 0
	for card in normal_deck:
		if not card in deck:
			return card, searches
		searches += 1
		await asyncio.sleep(1)

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
		await asyncio.sleep(1)


async def main():
	print("SHUFFLED DECK")

	deck = generate_deck()
	deck.pop(random.randint(0, 51))

	await asyncio.gather(
		loop_and_check(deck),
		sorted_suites(deck)
	)




asyncio.run(main())