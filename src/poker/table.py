from __future__ import annotations
from typing import Optional
from enum import Enum
from dataclasses import dataclass
from src.poker.card import Card
from src.poker.hand import Hand

RAISE_LIMIT = 4

class Seat(Enum):
    One = 1
    Two = 2

    def next(self) -> Seat:
        if self == Seat.One:
            return Seat.Two
        return Seat.One

class Action(Enum):
    Fold = 0
    CheckCall = 1
    BetRaise = 2

class Round(Enum):
    Preflop = 0
    Flop = 1
    Turn = 2
    River = 3

    def next(self) -> Round:
        match self:
            case Round.Preflop:
                return Round.Flop
            case Round.Flop:
                return Round.Turn
            case Round.Turn:
                return Round.River
            case Round.River:
                return Round.Preflop
@dataclass
class Player:
    chips : int
    hole_cards : list[Card]
    round_committed : int
    acted : bool
    all_in : bool

@dataclass
class Table:
    seats : dict[Seat,Player]
    button : Seat
    turn : Seat
    round : Round
    pot : int
    round_outstanding : int
    deck : list[Card]
    board : list[Card]

    @classmethod
    def start(cls):
        p1 = Player(chips=199, hole_cards=[], round_committed=1, acted=False, all_in=False)
        p2 = Player(chips=198, hole_cards=[], round_committed=2, acted=False, all_in=False)
        seats = {Seat.One: p1, Seat.Two: p2}
        table = Table(seats=seats, button=Seat.One, turn=Seat.One, round=Round.Preflop, pot=3, round_outstanding=2, deck=[], board=[])
        table._deal_next_hand()
        return table
    
    def action(self, action: Action):
        bet_size = self._bet_size()
        match action:
            case Action.Fold:
                self._payout(seat=self.turn.next(), chips=self.pot)
                self._new_hand()
                self.round = Round.Preflop
                return
            case Action.CheckCall:
                diff = self.round_outstanding - self._current_player().round_committed
                self._add_to_pot(p=self._current_player(), chips=diff)
            case Action.BetRaise:
                diff = self.round_outstanding - self._current_player().round_committed
                self._add_to_pot(p=self._current_player(), chips=diff + bet_size)
                self._other_player().acted = False
        self._current_player().acted = True
        self._next()

    def _next(self):
        if not self._everyone_acted():
            self.turn = self.turn.next()
            return
        self._reset_round()
        self.round = self.round.next()
        match self.round:
            case Round.Preflop:
                self._showdown()
                # TODO check if one player is out
                self._new_hand()
            case Round.Flop:
                self.board = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
                self.turn = self.button.next()
            case Round.Turn | Round.River:
                self.board = self.board + [self.deck.pop()]
                self.turn = self.button.next()
    
    def _new_hand(self):
        self.button = self.button.next()
        self.turn = self.button
        self._put_in_blinds()
        self._deal_next_hand()

    def _showdown(self):
        hands : dict[Seat,Hand] = {}
        for seat, p in self.seats.items():
            cards = self.board+p.hole_cards
            hands[seat] = Hand.from_cards(cards=cards)
        h1 = hands[Seat.One]
        h2 = hands[Seat.Two] 
        if h1 > h2:
            self._payout(seat=Seat.One, chips=self.pot)
        elif h2 > h1:
            self._payout(seat=Seat.Two, chips=self.pot)
        else:
            # tie
            self._payout(seat=Seat.One, chips=self.pot/2)
            self._payout(seat=Seat.Two, chips=self.pot/2)
        
    def _payout(self, seat: Seat, chips: int):
        self.pot -= chips
        self.seats[seat].chips += chips

    def _deal_next_hand(self):
        self.deck = Card.deck()
        for p in self.seats.values():
            p.hole_cards = [self.deck.pop(), self.deck.pop()]
        self.board = []

    def _put_in_blinds(self):
        self._add_to_pot(p=self.seats[self.button], chips=1)
        self._add_to_pot(p=self.seats[self.button.next()], chips=2)
        
    def _add_to_pot(self, p: Player, chips: int):
        p_chips = min(chips, p.chips)
        p.chips -= p_chips
        self.pot += p_chips
        p.round_committed += p_chips
        if p.round_committed > self.round_outstanding:
            self.round_outstanding = p.round_committed
        if p.chips == 0:
            p.all_in = True
    
    def _current_player(self) -> Player:
        return self.seats[self.turn]

    def _other_player(self) -> Player:
        return self.seats[self.turn.next()]

    def _everyone_acted(self) -> bool:
        return self._current_player().acted and self._other_player().acted
    
    def _reset_round(self):
        for p in self.seats.values():
            p.acted = False
            p.round_committed = 0
        self.round_outstanding = 0

    def _bet_size(self):
        return 2 if self.round in [Round.Preflop, Round.Flop] else 4