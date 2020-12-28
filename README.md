# Goof Troop Randomizer : Version 2.0
Data structure & Project management by Niamek, 
Randomizer logic and code organization by Charles342

# Features:
## Dark rooms (d,D, alldark, nodark)
There are 6 dark rooms in the original game.
- d : Randomize which rooms are dark. There will be 6 dark rooms like in vanilla.
- D : Randomize which rooms are dark. There can be a number higher than 6, following a normalized distribution (mean : 12,standard deviation : 5))
- alldark : All rooms will be dark. For now, the bosses won't be a dark room.
- nodark : No dark rooms.
## icy rooms (s, S, allicy, noicy):
There are 2 icy rooms in the original game. The amount of dark rooms is changed with these options.
- s : Randomize which rooms are icy. There will be 2 icy rooms like in vanilla.
- S : Randomize which rooms are icy. There can be a number higher than 2, following a normalized distribution (mean : 12,standard deviation : 5))
- allicy : All rooms will be dark. For now, the bosses won't be a dark room.
- noicy : No dark rooms.
## First room
Randomize which room you initially start a world with one of the exits of the world. Rooms with more exits will have more chance of being the starter.

## Items (i,I)
- i : Shuffle the items. Each world keeps its items pool.
- I : Randomize the items.

## Exits (e, u, U)
- e : Randomize the exits.
- u : Do not match the direction for the exits and their destination. In other words : a north exit can lead to a west exit instead of an always south exit.
- U : Do not pair exits. WARNING : There is probably a risk (low risk) of generating an incompletable seed with this flag.

## Other stuffs
### Password cheat : Enable the world selection. If not enabled, the passwords are random.
- World 2 : Cherry, Banana, Cherry, Cherry, Cherry
- World 3 Cherry, Cherry, Banana, Cherry, Cherry
- World 4 Cherry, Cherry, Cherry, Banana, Cherry
- World 5 Cherry, Cherry, Cherry, Cherry, Banana
### One Hit Knock Out (ohko)
All source of damages will one hit knock out now. Hearts no longer protects you from losing a life.
# Community and links
Github project : https://github.com/GB127/GT-Rando

Goof Troop's Discord server : https://discord.gg/4MJT3Y5tgk