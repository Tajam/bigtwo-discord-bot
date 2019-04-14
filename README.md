# BigTwoBot for Discord
A simple Discord bot which allow members to play [Big Two](https://en.wikipedia.org/wiki/Big_two) card game in each channel.

Made from scratch using [discord.py](https://github.com/Rapptz/discord.py)

## Project need to be tested
I have done the first release of this bot. However, it's not tested yet. Some fatal bugs might exists.

## Combo detection logic
The ranking for suit and rank of the card is recorded in a .json file.

### Straight
Iterate throught all input cards. If the rank of the card number *I* is next rank of card number *I + 1*, add 1 to valid point. Return true if there is 4 valid points.

### Flush
Iterate throught all input cards. If any of the suit of card number *I* and card number *I + 1* is not match, return false.

### Royal Flush
Straight and Flush

### Full House
Group all input cards by rank. Return true if there is only 2 groups and the largest group contain 3 cards.

### Four of a Kind
Group all input cards by rank. Return true if there is only 2 groups and the largest group contain 4 cards.

## Combo Comparison

### Combo ranking
1. Royal Flush
2. Four of a Kind
3. Full House
4. Flush
5. Straight

### Leading card
For Straight, Full House and Four of a Kind, just compare the largest card in the group. Same logic used for Double and Triple combo.

### Suit first, rank second
For Flush and Royal Flush, must compare suit of the group first, then the largest card.