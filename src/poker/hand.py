from __future__ import annotations
from typing import Optional
from enum import Enum
from itertools import combinations
from functools import total_ordering
from dataclasses import dataclass
from src.poker.card import Card, Rank, Suit

@total_ordering
class Ranking(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    @classmethod
    def get_ranking(cls, cards : list[Card]) -> Ranking:
        flush = _has_flush(cards=cards)
        straight = _has_straight(cards=cards)
        if flush and straight and cards[0].rank == Rank.ACE:
            return Ranking.ROYAL_FLUSH
        if flush and straight and cards[0].rank != Rank.ACE:
            return Ranking.STRAIGHT_FLUSH
        if _has_pairs(cards=cards, pairs=[4,1]):
            return Ranking.FOUR_OF_A_KIND
        if _has_pairs(cards=cards, pairs=[3,2]):
            return Ranking.FULL_HOUSE
        if flush and not straight:
            return Ranking.FLUSH
        if straight and not flush:
            return Ranking.STRAIGHT
        if _has_pairs(cards=cards, pairs=[3,1,1]):
            return Ranking.THREE_OF_A_KIND
        if _has_pairs(cards=cards, pairs=[2,2,1]):
            return Ranking.TWO_PAIR
        if _has_pairs(cards=cards, pairs=[2,1,1,1]):
            return Ranking.PAIR
        return Ranking.HIGH_CARD

    def description(self, cards : list[Card]) -> str:
        match self:
            case Ranking.ROYAL_FLUSH:
                return "royal flush"
            case Ranking.STRAIGHT_FLUSH:
                return f"straight flush {cards[0].rank.singular_name()} high"
            case Ranking.FOUR_OF_A_KIND:
                return f"four of a kind {cards[0].rank.plural_name()}"
            case Ranking.FULL_HOUSE:
                return f"full house {cards[0].rank.plural_name()} full of {cards[4].rank.plural_name()}"
            case Ranking.FLUSH:
                return f"flush {cards[0].rank.singular_name()} high"
            case Ranking.STRAIGHT:
                return f"straight {cards[0].rank.singular_name()} high"
            case Ranking.THREE_OF_A_KIND:
                return f"three of a kind {cards[0].rank.plural_name()}"
            case Ranking.TWO_PAIR:
                return f"two pair {cards[0].rank.plural_name()} and {cards[3].rank.plural_name()}"                
            case Ranking.PAIR:
                return f"pair of {cards[0].rank.plural_name()}" 
            case Ranking.HIGH_CARD:
                return f"{cards[0].rank.singular_name()} high"

    def __lt__(self, other: Ranking) -> bool:
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

@total_ordering
@dataclass(frozen=True)
class Hand:
    cards : list[Card]
    ranking : Ranking
    description : str

    @classmethod
    def from_cards(cls, cards : list[Card]) -> Hand:
        if len(cards) < 5:
            raise ValueError("must have at least five cards")
        elif len(cards) == 5:
            formed = _form_cards(cards=cards)
            ranking = Ranking.get_ranking(cards=formed)
            description = ranking.description(cards=formed)
            return Hand(cards=formed, ranking=ranking, description=description)
        else:
            hand : Optional[Hand] = None
            for combo in combinations(cards, 5):
                combo_hand = Hand.from_cards(combo)
                if hand is None or combo_hand > hand:
                    hand = combo_hand
            return hand

    def __eq__(self, other: Hand) -> bool:
        if self.__class__ is other.__class__:
            if self.ranking != other.ranking:
                return False
            else:
                for i in range(5):
                    r1 = self.cards[i].rank
                    r2 = other.cards[i].rank
                    if r1 != r2:
                        return False
            return True
        return NotImplemented
    
    def __lt__(self, other: Hand) -> bool:
        if self.__class__ is other.__class__:
            if self.ranking != other.ranking:
                return self.ranking < other.ranking
            else:
                for i in range(5):
                    r1 = self.cards[i].rank
                    r2 = other.cards[i].rank
                    if r1 != r2:
                        return r1 < r2
            return True
        return NotImplemented


def _form_cards(cards: list[Card]) -> list[Card]:
    cards = sorted(cards, key=lambda x: x.rank.value, reverse=True)
    ranks = list(reversed(list(Rank)))
    formed = []
    for i in [4,3,2,1]:
        for rank in ranks:
            rank_cards = list(filter(lambda card: card.rank is rank, cards))
            if len(rank_cards) == i:
                formed.extend(rank_cards)
    return _form_low_straight(formed)

def _form_low_straight(cards: list[Card]) -> list[Card]:
    if (cards[0].rank is Rank.ACE and 
        cards[1].rank is Rank.FIVE and 
        cards[2].rank is Rank.FOUR and 
        cards[3].rank is Rank.THREE and 
        cards[4].rank is Rank.TWO):
        return [cards[1],cards[2],cards[3],cards[4],cards[0]]
    return cards

def _has_pairs(cards: list[Card], pairs: list[int]) -> bool:
    idx = 0
    for pair in pairs:
        pair_cards = cards[idx:idx+pair]
        paired = True
        for card in pair_cards:
            if card.rank != pair_cards[0].rank:
                paired = False
        if not paired:
            return False
        idx += pair
    return True

def _has_flush(cards: list[Card]) -> bool:
    suit = cards[0].suit
    for c in cards:
        if suit != c.suit:
            return False
    return True

def _has_straight(cards: list[Card]) -> bool:
    count = 0
    for i in range(1,5):
        card_1 = cards[i-1]
        card_2 = cards[i]
        if card_1.rank.value is card_2.rank.value + 1:
            count += 1
    return count == 4 or _has_low_straight(cards=cards)

def _has_low_straight(cards: list[Card]) -> bool:
    return ( 
        cards[0].rank is Rank.FIVE and 
        cards[1].rank is Rank.FOUR and 
        cards[2].rank is Rank.THREE and 
        cards[3].rank is Rank.TWO and
        cards[4].rank is Rank.ACE)