from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from functools import total_ordering
import random

class Suit(Enum):
    CLUBS = "♣"
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"

    @classmethod
    def from_str(cls, s : str) -> Suit:
        match s:
            case "♣" | "c":
                return Suit.CLUBS
            case "♦" | "d":
                return Suit.DIAMONDS
            case "♥" | "h":
                return Suit.DIAMONDS
            case "♠" | "s":
                return Suit.SPADES
        raise ValueError("invalid string for suit: " + s)
    
    def __str__(self):
        return str(self.value)

RANK_CHARS = "23456789TJQKA"
RANK_SINGULAR_NAMES = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"]
RANK_PLURAL_NAMES = ["twos", "threes", "fours", "fives", "sixes", "sevens", "eights", "nines", "tens", "jacks", "queens", "kings", "aces"]

@total_ordering
class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    @classmethod
    def from_str(cls, s : str) -> Rank:
        for rank in Rank:
            if str(rank) == s:
                return rank
        raise ValueError("invalid string for rank: " + s)

    def __str__(self) -> str:
        return RANK_CHARS[self.value-2]

    def singular_name(self) -> str:
        return RANK_SINGULAR_NAMES[self.value-2]

    def plural_name(self) -> str:
        return RANK_PLURAL_NAMES[self.value-2]

    def __lt__(self, other: Rank) -> bool:
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

@total_ordering
@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    @classmethod
    def from_str_list(cls, card_strs : list[str]) -> list[Card]:
        return list(map(lambda s: Card.from_str(s), card_strs))
        
    @classmethod
    def deck(cls) -> list[Card]:
        cards : list[Card] = []
        for rank in Rank:
            for suit in Suit:
                card = Card(rank=rank, suit=suit)
                cards.append(card)
        random.shuffle(cards)
        return cards

    @classmethod
    def from_str(cls, s : str) -> Card:
        if len(s) != 2:
            raise ValueError("invalid string for card: " + s)
        rank = Rank.from_str(s[0])
        suit = Suit.from_str(s[1])
        return Card(rank=rank, suit=suit)

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __lt__(self, other: Card) -> bool:
        if self.__class__ is other.__class__:
            return self.rank < other.rank
        return NotImplemented
