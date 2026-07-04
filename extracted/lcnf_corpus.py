# Generated from Corpus

from __future__ import annotations
from dataclasses import dataclass
import functools
from typing import Any, Callable

@dataclass
class UFNode_mk:
    field_0: Any
    field_1: Any

UFNode = UFNode_mk

@dataclass
class Queue_mk:
    field_0: Any
    field_1: Any

Queue = Queue_mk

@dataclass
class Ord_mk:
    field_0: Any

Ord = Ord_mk

@dataclass
class Trie_node:
    field_0: Any
    field_1: Any

Trie = Trie_node

@dataclass
class RBTree_empty:
    pass

@dataclass
class RBTree_node:
    field_0: Any
    field_1: Any
    field_2: Any
    field_3: Any

RBTree = RBTree_empty | RBTree_node

@dataclass
class Point3D_mk:
    field_0: Any
    field_1: Any
    field_2: Any

Point3D = Point3D_mk

@dataclass
class X:
    pass

@dataclass
class O:
    pass

Player = X | O

@dataclass
class isFalse:
    field_0: Any

@dataclass
class isTrue:
    field_0: Any

Decidable = isFalse | isTrue

@dataclass
class ace:
    pass

@dataclass
class two:
    pass

@dataclass
class three:
    pass

@dataclass
class four:
    pass

@dataclass
class five:
    pass

@dataclass
class six:
    pass

@dataclass
class seven:
    pass

@dataclass
class eight:
    pass

@dataclass
class nine:
    pass

@dataclass
class ten:
    pass

@dataclass
class jack:
    pass

@dataclass
class queen:
    pass

@dataclass
class king:
    pass

Rank = ace | two | three | four | five | six | seven | eight | nine | ten | jack | queen | king

@dataclass
class rock:
    pass

@dataclass
class paper:
    pass

@dataclass
class scissors:
    pass

RPS = rock | paper | scissors

@dataclass
class lt:
    pass

@dataclass
class eq:
    pass

@dataclass
class gt:
    pass

Ordering = lt | eq | gt

@dataclass
class Stack_mk:
    field_0: Any

Stack = Stack_mk

@dataclass
class BlackjackHand_mk:
    field_0: Any

BlackjackHand = BlackjackHand_mk

@dataclass
class UnionFind_mk:
    field_0: Any

UnionFind = UnionFind_mk

@dataclass
class Card_mk:
    field_0: Any
    field_1: Any

Card = Card_mk

@dataclass
class List_nil:
    pass

@dataclass
class List_cons:
    field_0: Any
    field_1: Any

List = List_nil | List_cons

@dataclass
class TicTacToe_mk:
    field_0: Any
    field_1: Any

TicTacToe = TicTacToe_mk

@dataclass
class hearts:
    pass

@dataclass
class diamonds:
    pass

@dataclass
class clubs:
    pass

@dataclass
class spades:
    pass

Suit = hearts | diamonds | clubs | spades

@dataclass
class zero:
    pass

@dataclass
class succ:
    field_0: Any

Nat = zero | succ

@dataclass
class false:
    pass

@dataclass
class true:
    pass

Bool = false | true

@dataclass
class Heap_mk:
    field_0: Any

Heap = Heap_mk

@dataclass
class BinaryTree_empty:
    pass

@dataclass
class BinaryTree_node:
    field_0: Any
    field_1: Any
    field_2: Any

BinaryTree = BinaryTree_empty | BinaryTree_node

@dataclass
class Prod_mk:
    field_0: Any
    field_1: Any

Prod = Prod_mk

@dataclass
class BEq_mk:
    field_0: Any

BEq = BEq_mk

@dataclass
class left:
    field_0: Any

@dataclass
class right:
    field_0: Any

Either = left | right

@dataclass
class Graph_mk:
    field_0: Any
    field_1: Any

Graph = Graph_mk

@dataclass
class red:
    pass

@dataclass
class black:
    pass

Color = red | black

@dataclass
class Point2D_mk:
    field_0: Any
    field_1: Any

Point2D = Point2D_mk

@dataclass
class Graph_mk:
    field_0: Any
    field_1: Any

Graph = Graph_mk

@dataclass
class Nim_mk:
    field_0: Any

Nim = Nim_mk

@dataclass
class UnionFind_mk:
    field_0: Any
    field_1: Any

UnionFind = UnionFind_mk

@dataclass
class Option_none:
    pass

@dataclass
class Option_some:
    field_0: Any

Option = Option_none | Option_some

# Lean: Corpus.Production.countInversions.mergeAndCount.go
def merge_and_count_go(xs: list[int], ys: list[int], acc: list[int], inv: int) -> tuple[list[int], int]:
    while True:
        def _f_21276(ys_0: list[int]):
            _x_21273 = list(reversed(acc))
            _x_21274 = _x_21273 + ys_0
            _x_21275 = (_x_21274, inv)
            return _x_21275
        _alt_21277 = _f_21276
        _alt_21278 = _f_21276
        if len(xs) == 0:
            _x_21296 = _alt_21277(ys)
            return _x_21296
        else:
            head_21297 = xs[0]
            tail_21298 = xs[1:]
            if len(ys) == 0:
                _x_21299 = [head_21297] + tail_21298
                _x_21300 = _alt_21278(_x_21299)
                return _x_21300
            else:
                head_21301 = ys[0]
                tail_21302 = ys[1:]
                x = head_21297
                xs_ = tail_21298
                y = head_21301
                ys_ = tail_21302
                _x_21279 = x <= y
                if _x_21279:
                    _x_21290 = [y] + ys_
                    _x_21291 = [x] + acc
                    xs, ys, acc, inv = xs_, _x_21290, _x_21291, inv
                    continue
                else:
                    _x_21281 = [x] + xs_
                    _x_21282 = [y] + acc
                    _x_21286 = len(xs)
                    _x_21287 = inv + _x_21286
                    xs, ys, acc, inv = _x_21281, ys_, _x_21282, _x_21287
                    continue

# Lean: Corpus.Production.countInversions.mergeAndCount
def merge_and_count(xs_1: list[int], ys_2: list[int]) -> tuple[list[int], int]:
    _x_21307 = []
    _x_21308 = 0
    _x_21311 = merge_and_count_go(xs_1, ys_2, _x_21307, 0)
    return _x_21311

# Lean: Corpus.Production.countInversions.mergeCount
def merge_count(xs_3: list[int]) -> tuple[list[int], int]:
    _x_21313 = len(xs_3)
    _x_21314 = 1
    _x_21317 = _x_21313 <= 1
    if _x_21317:
        _x_21363 = 0
        _x_21366 = (xs_3, 0)
        return _x_21366
    else:
        _x_21322 = 2
        _x_21325 = _x_21313 // 2
        def _f_21353(left: list[int], right: list[int]):
            def _f_21346(sorted_l: list[int], inv_l: int):
                def _f_21339(sorted_r: list[int], inv_r: int):
                    def _f_21332(merged: list[int], inv_merge: int):
                        _x_21329 = inv_l + inv_r
                        _x_21330 = _x_21329 + inv_merge
                        _x_21331 = (merged, _x_21330)
                        return _x_21331
                    _alt_21333 = _f_21332
                    _x_21334 = merge_and_count(sorted_l, sorted_r)
                    match _x_21334:
                        case (fst_21335, snd_21336):
                            _x_21337 = _alt_21333(fst_21335, snd_21336)
                            return _x_21337
                _alt_21340 = _f_21339
                _x_21341 = merge_count(right)
                match _x_21341:
                    case (fst_21342, snd_21343):
                        _x_21344 = _alt_21340(fst_21342, snd_21343)
                        return _x_21344
            _alt_21347 = _f_21346
            _x_21348 = merge_count(left)
            match _x_21348:
                case (fst_21349, snd_21350):
                    _x_21351 = _alt_21347(fst_21349, snd_21350)
                    return _x_21351
        _alt_21354 = _f_21353
        _x_21355 = take_tr(None, _x_21325, xs_3)
        _x_21356 = (lambda n, xs: xs[n:])(xs_3)
        _x_21357 = (_x_21355, _x_21356)
        match _x_21357:
            case (fst_21358, snd_21359):
                _x_21360 = _alt_21354(fst_21358, snd_21359)
                return _x_21360

# Lean: Corpus.Production.maxSubarraySum.kadane
def kadane(xs_4: list[int], current_max: int, global_max: int) -> int:
    while True:
        def _f_21369():
            return global_max
        _alt_21370 = _f_21369
        if len(xs_4) == 0:
            _x_21383 = _alt_21370()
            return _x_21383
        else:
            head_21384 = xs_4[0]
            tail_21385 = xs_4[1:]
            x_5 = head_21384
            rest = tail_21385
            _x_21372 = max
            _x_21376 = current_max + x_5
            _x_21377 = _x_21372(x_5, _x_21376)
            _x_21378 = _x_21372(global_max, _x_21377)
            xs_4, current_max, global_max = rest, _x_21377, _x_21378
            continue

# Lean: Corpus.Production.lis.fill
def fill(xs_6: list[int], n: int, i: int, dp: list[int], parent: list[int]) -> tuple[list[int], list[int]]:
    while True:
        _x_21389 = n <= i
        if _x_21389:
            _x_21475 = (dp, parent)
            return _x_21475
        else:
            _x_21392 = _x_21391.field_2
            _x_21394 = _x_21392(_x_21393, xs_6, i)
            def _f_21463(x_21407: tuple[int, int], j: int):
                def _f_21457(acc_7: int, pj: int):
                    def _f_21409():
                        _x_21408 = False
                        return False
                    _alt_21410 = _f_21409
                    def _f_21423():
                        _x_21415 = _x_21414.field_2
                        _x_21416 = _x_21415(_x_21393, dp, j)
                        _x_21417 = 1
                        _x_21420 = _x_21416 + 1
                        _x_21421 = acc_7 < _x_21420
                        return _x_21421
                    _alt_21424 = _f_21423
                    _x_21425 = _x_21392(_x_21393, xs_6, j)
                    _x_21426 = _x_21425 < _x_21394
                    def _jp_21450(_y_21432: bool):
                        _x_21433 = True
                        _x_21434 = _y_21432 == True
                        if _x_21434:
                            _x_21442 = _x_21441.field_2
                            _x_21443 = _x_21442(_x_21393, dp, j)
                            _x_21444 = 1
                            _x_21447 = _x_21443 + 1
                            _x_21448 = (_x_21447, j)
                            return _x_21448
                        else:
                            _x_21436 = (acc_7, pj)
                            return _x_21436
                    def _jp_21453():
                        _x_21452 = _alt_21410()
                        return _jp_21450(_x_21452)
                    def _jp_21456():
                        _x_21455 = _alt_21424()
                        return _jp_21450(_x_21455)
                    if _x_21426:
                        return _jp_21456()
                    else:
                        return _jp_21453()
                _alt_21458 = _f_21457
                match x_21407:
                    case (fst_21459, snd_21460):
                        _x_21461 = _alt_21458(fst_21459, snd_21460)
                        return _x_21461
            _x_21464 = 1
            _x_21467 = (1, n)
            _x_21468 = list(range(i))
            _x_21469 = functools.reduce(_f_21463, _x_21468, _x_21467)
            match _x_21469:
                case (fst_21470, snd_21471):
                    max_len = fst_21470
                    max_j = snd_21471
                    _x_21398 = 1
                    _x_21401 = i + 1
                    _x_21402 = set_(None, dp, i, max_len)
                    _x_21403 = set_(None, parent, i, max_j)
                    xs_6, n, i, dp, parent = xs_6, n, _x_21401, _x_21402, _x_21403
                    continue

# Lean: Corpus.Production.lis.backtrack
def backtrack(xs_10: list[int], n_11: int, parent_: list[int], i_12: int, acc_13: list[int]) -> list[int]:
    while True:
        _x_21478 = n_11 <= i_12
        if _x_21478:
            return acc_13
        else:
            _x_21481 = _x_21480.field_2
            _x_21483 = _x_21481(_x_21482, parent_, i_12)
            _x_21485 = _x_21484.field_2
            _x_21486 = _x_21485(_x_21482, xs_10, i_12)
            _x_21487 = [_x_21486] + acc_13
            xs_10, n_11, parent_, i_12, acc_13 = xs_10, n_11, parent_, _x_21483, _x_21487
            continue

# Lean: Corpus.Production.lisLength.fill
def fill(xs_14: list[int], n_15: int, i_16: int, dp_17: list[int]) -> list[int]:
    while True:
        _x_21492 = n_15 <= i_16
        if _x_21492:
            return dp_17
        else:
            _x_21495 = _x_21494.field_2
            _x_21497 = _x_21495(_x_21496, xs_14, i_16)
            def _f_21516(acc_19: int, j_20: int):
                _x_21498 = _x_21495(_x_21496, xs_14, j_20)
                _x_21499 = _x_21498 < _x_21497
                if _x_21499:
                    _x_21503 = max
                    _x_21508 = _x_21507.field_2
                    _x_21509 = _x_21508(_x_21496, dp_17, j_20)
                    _x_21510 = 1
                    _x_21513 = _x_21509 + 1
                    _x_21514 = _x_21503(acc_19, _x_21513)
                    return _x_21514
                else:
                    return acc_19
            _x_21517 = 1
            _x_21520 = list(range(i_16))
            _x_21521 = functools.reduce(_f_21516, _x_21520, 1)
            _x_21525 = i_16 + 1
            _x_21526 = set_(None, dp_17, i_16, _x_21521)
            xs_14, n_15, i_16, dp_17 = xs_14, n_15, _x_21525, _x_21526
            continue

# Lean: Corpus.Production.matrixChainOrder.fill
def fill(dims: list[int], n_21: int, inf: int, len: int, i_22: int, dp_23: list[int]) -> list[int]:
    while True:
        _x_21531 = n_21 < len
        if _x_21531:
            return dp_23
        else:
            _x_21536 = i_22 + len
            _x_21537 = n_21 < _x_21536
            if _x_21537:
                _x_21597 = 1
                _x_21600 = len + 1
                _x_21601 = 0
                dims, n_21, inf, len, i_22, dp_23 = dims, n_21, inf, _x_21600, 0, dp_23
                continue
            else:
                _x_21542 = 1
                _x_21545 = _x_21536 - 1
                _x_21549 = i_22 * n_21
                _x_21550 = _x_21549 + _x_21545
                _x_21554 = len == 1
                _x_21555 = True
                _x_21556 = _x_21554 == True
                if _x_21556:
                    _x_21589 = i_22 + 1
                    _x_21590 = 0
                    _x_21593 = set_(None, dp_23, _x_21550, 0)
                    dims, n_21, inf, len, i_22, dp_23 = dims, n_21, inf, len, _x_21589, _x_21593
                    continue
                else:
                    def _f_21581(acc_25: int, k_: int):
                        _x_21558 = i_22 + k_
                        _x_21560 = _x_21559.field_2
                        _x_21562 = _x_21549 + _x_21558
                        _x_21563 = _x_21560(_x_21561, dp_23, _x_21562)
                        _x_21564 = _x_21558 + 1
                        _x_21565 = _x_21564 * n_21
                        _x_21566 = _x_21565 + _x_21545
                        _x_21567 = _x_21560(_x_21561, dp_23, _x_21566)
                        _x_21568 = _x_21563 + _x_21567
                        _x_21570 = _x_21569.field_2
                        _x_21571 = _x_21570(_x_21561, dims, i_22)
                        _x_21572 = _x_21570(_x_21561, dims, _x_21564)
                        _x_21573 = _x_21571 * _x_21572
                        _x_21574 = _x_21545 + 1
                        _x_21575 = _x_21570(_x_21561, dims, _x_21574)
                        _x_21576 = _x_21573 * _x_21575
                        _x_21577 = _x_21568 + _x_21576
                        _x_21579 = min
                        _x_21580 = _x_21579(acc_25, _x_21577)
                        return _x_21580
                    _x_21582 = len - 1
                    _x_21583 = list(range(_x_21582))
                    _x_21584 = functools.reduce(_f_21581, _x_21583, inf)
                    _x_21585 = i_22 + 1
                    _x_21586 = set_(None, dp_23, _x_21550, _x_21584)
                    dims, n_21, inf, len, i_22, dp_23 = dims, n_21, inf, len, _x_21585, _x_21586
                    continue

# Lean: Corpus.Production.coinChange.fill
def fill(coins: list[int], amount: int, inf_26: int, a: int, dp_27: list[int]) -> list[int]:
    while True:
        _x_21609 = amount < a
        if _x_21609:
            return dp_27
        else:
            def _f_21663(acc_28: int, c: int):
                def _f_21612():
                    _x_21611 = False
                    return False
                _alt_21613 = _f_21612
                def _f_21624():
                    _x_21615 = _x_21614.field_2
                    _x_21620 = a - c
                    _x_21621 = _x_21615(_x_21616, dp_27, _x_21620)
                    _x_21622 = _x_21621 < inf_26
                    return _x_21622
                _alt_21625 = _f_21624
                _x_21626 = c <= a
                def _jp_21656(_y_21632: bool):
                    _x_21633 = True
                    _x_21634 = _y_21632 == True
                    if _x_21634:
                        _x_21638 = min
                        _x_21643 = _x_21642.field_2
                        _x_21648 = a - c
                        _x_21649 = _x_21643(_x_21644, dp_27, _x_21648)
                        _x_21650 = 1
                        _x_21653 = _x_21649 + 1
                        _x_21654 = _x_21638(acc_28, _x_21653)
                        return _x_21654
                    else:
                        return acc_28
                def _jp_21659():
                    _x_21658 = _alt_21613()
                    return _jp_21656(_x_21658)
                def _jp_21662():
                    _x_21661 = _alt_21625()
                    return _jp_21656(_x_21661)
                if _x_21626:
                    return _jp_21662()
                else:
                    return _jp_21659()
            _x_21664 = functools.reduce(_f_21663, coins, inf_26)
            _x_21668 = 1
            _x_21671 = a + 1
            _x_21672 = set_(None, dp_27, a, _x_21664)
            coins, amount, inf_26, a, dp_27 = coins, amount, inf_26, _x_21671, _x_21672
            continue

# Lean: Corpus.Production.knapsack01.fill
def fill(capacity: int, weights: list[int], values: list[int], n_31: int, i_32: int, w: int, dp_33: list[int]) -> list[int]:
    _x_21677 = n_31 < i_32
    if _x_21677:
        return dp_33
    else:
        _x_21679 = capacity < w
        if _x_21679:
            _x_21744 = 1
            _x_21747 = i_32 + 1
            _x_21748 = 0
            _x_21751 = fill(capacity, weights, values, n_31, _x_21747, 0, dp_33)
            return _x_21751
        else:
            _x_21687 = 1
            _x_21690 = capacity + 1
            _x_21691 = i_32 * _x_21690
            _x_21692 = _x_21691 + w
            _x_21696 = 0
            _x_21699 = i_32 == 0
            _x_21700 = True
            _x_21701 = _x_21699 == True
            def _jp_21739(_y_21735: int):
                _x_21736 = w + 1
                _x_21737 = set_(None, dp_33, _x_21692, _y_21735)
                _x_21738 = fill(capacity, weights, values, n_31, i_32, _x_21736, _x_21737)
                return _x_21738
            if _x_21701:
                return _jp_21739(0)
            else:
                _x_21704 = _x_21703.field_2
                _x_21709 = i_32 - 1
                _x_21710 = _x_21704(_x_21705, weights, _x_21709)
                _x_21711 = _x_21704(_x_21705, values, _x_21709)
                _x_21712 = w < _x_21710
                if _x_21712:
                    _x_21728 = _x_21727.field_2
                    _x_21729 = _x_21709 * _x_21690
                    _x_21730 = _x_21729 + w
                    _x_21731 = _x_21728(_x_21705, dp_33, _x_21730)
                    return _jp_21739(_x_21731)
                else:
                    _x_21715 = max
                    _x_21717 = _x_21716.field_2
                    _x_21718 = _x_21709 * _x_21690
                    _x_21719 = _x_21718 + w
                    _x_21720 = _x_21717(_x_21705, dp_33, _x_21719)
                    _x_21721 = w - _x_21710
                    _x_21722 = _x_21718 + _x_21721
                    _x_21723 = _x_21717(_x_21705, dp_33, _x_21722)
                    _x_21724 = _x_21723 + _x_21711
                    _x_21725 = _x_21715(_x_21720, _x_21724)
                    return _jp_21739(_x_21725)

# Lean: Corpus.Production.intervalScheduling.select
def select(remaining: list[tuple[int, int]], last_end: int, acc_35: list[tuple[int, int]]) -> list[tuple[int, int]]:
    while True:
        def _f_21757():
            _x_21756 = list(reversed(acc_35))
            return _x_21756
        _alt_21758 = _f_21757
        if len(remaining) == 0:
            _x_21770 = _alt_21758()
            return _x_21770
        else:
            head_21771 = remaining[0]
            tail_21772 = remaining[1:]
            match head_21771:
                case (fst_21773, snd_21774):
                    s = fst_21773
                    e = snd_21774
                    rest_37 = tail_21772
                    _x_21759 = last_end <= s
                    if _x_21759:
                        _x_21763 = (s, e)
                        _x_21764 = [_x_21763] + acc_35
                        remaining, last_end, acc_35 = rest_37, e, _x_21764
                        continue
                    else:
                        remaining, last_end, acc_35 = rest_37, last_end, acc_35
                        continue

# Lean: Corpus.Production.editDistance.fill
def fill(xs_38: list[int], ys_39: list[int], m: int, n_40: int, i_41: int, j_42: int, dp_43: list[int]) -> list[int]:
    _x_21779 = m < i_41
    if _x_21779:
        return dp_43
    else:
        _x_21781 = n_40 < j_42
        if _x_21781:
            _x_21854 = 1
            _x_21857 = i_41 + 1
            _x_21858 = 0
            _x_21861 = fill(xs_38, ys_39, m, n_40, _x_21857, 0, dp_43)
            return _x_21861
        else:
            _x_21789 = 1
            _x_21792 = n_40 + 1
            _x_21793 = i_41 * _x_21792
            _x_21794 = _x_21793 + j_42
            _x_21798 = 0
            _x_21801 = i_41 == 0
            _x_21802 = True
            _x_21803 = _x_21801 == True
            def _jp_21849(_y_21845: int):
                _x_21846 = j_42 + 1
                _x_21847 = set_(None, dp_43, _x_21794, _y_21845)
                _x_21848 = fill(xs_38, ys_39, m, n_40, i_41, _x_21846, _x_21847)
                return _x_21848
            if _x_21803:
                return _jp_21849(j_42)
            else:
                _x_21805 = j_42 == 0
                _x_21806 = _x_21805 == True
                if _x_21806:
                    return _jp_21849(i_41)
                else:
                    _x_21809 = _x_21808.field_2
                    _x_21814 = i_41 - 1
                    _x_21815 = _x_21809(_x_21810, xs_38, _x_21814)
                    _x_21816 = j_42 - 1
                    _x_21817 = _x_21809(_x_21810, ys_39, _x_21816)
                    _x_21818 = _x_21815 == _x_21817
                    _x_21819 = _x_21818 == True
                    def _jp_21841(_y_21824: int):
                        _x_21826 = min
                        _x_21828 = _x_21827.field_2
                        _x_21829 = _x_21814 * _x_21792
                        _x_21830 = _x_21829 + j_42
                        _x_21831 = _x_21828(_x_21810, dp_43, _x_21830)
                        _x_21832 = _x_21831 + 1
                        _x_21833 = _x_21793 + _x_21816
                        _x_21834 = _x_21828(_x_21810, dp_43, _x_21833)
                        _x_21835 = _x_21834 + 1
                        _x_21836 = _x_21826(_x_21832, _x_21835)
                        _x_21837 = _x_21829 + _x_21816
                        _x_21838 = _x_21828(_x_21810, dp_43, _x_21837)
                        _x_21839 = _x_21838 + _y_21824
                        _x_21840 = _x_21826(_x_21836, _x_21839)
                        return _jp_21849(_x_21840)
                    if _x_21819:
                        return _jp_21841(0)
                    else:
                        return _jp_21841(0)

# Lean: Corpus.Production.lcs.backtrack
def backtrack(xs_48: list[int], ys_49: list[int], n_50: int, memo_: list[int], i_51: int, j_52: int, acc_53: list[int]) -> list[int]:
    def _f_21867():
        _x_21866 = True
        return True
    _alt_21868 = _f_21867
    def _f_21876():
        _x_21872 = 0
        _x_21875 = j_52 == 0
        return _x_21875
    _alt_21877 = _f_21876
    _x_21881 = 0
    _x_21884 = i_51 == 0
    def _jp_21936(_y_21889: bool):
        _x_21890 = True
        _x_21891 = _y_21889 == True
        if _x_21891:
            return acc_53
        else:
            _x_21894 = _x_21893.field_2
            _x_21899 = 1
            _x_21902 = i_51 - 1
            _x_21903 = _x_21894(_x_21895, xs_48, _x_21902)
            _x_21904 = j_52 - 1
            _x_21905 = _x_21894(_x_21895, ys_49, _x_21904)
            _x_21906 = _x_21903 == _x_21905
            _x_21907 = _x_21906 == True
            if _x_21907:
                _x_21931 = [_x_21903] + acc_53
                _x_21932 = backtrack(xs_48, ys_49, n_50, memo_, _x_21902, _x_21904, _x_21931)
                return _x_21932
            else:
                _x_21910 = _x_21909.field_2
                _x_21917 = n_50 + 1
                _x_21918 = i_51 * _x_21917
                _x_21919 = _x_21918 + _x_21904
                _x_21920 = _x_21910(_x_21895, memo_, _x_21919)
                _x_21921 = _x_21902 * _x_21917
                _x_21922 = _x_21921 + j_52
                _x_21923 = _x_21910(_x_21895, memo_, _x_21922)
                _x_21924 = _x_21920 < _x_21923
                if _x_21924:
                    _x_21928 = backtrack(xs_48, ys_49, n_50, memo_, _x_21902, j_52, acc_53)
                    return _x_21928
                else:
                    _x_21926 = backtrack(xs_48, ys_49, n_50, memo_, i_51, _x_21904, acc_53)
                    return _x_21926
    def _jp_21942():
        _x_21941 = _alt_21868()
        return _jp_21936(_x_21941)
    def _jp_21939():
        _x_21938 = _alt_21877()
        return _jp_21936(_x_21938)
    if _x_21884:
        return _jp_21942()
    else:
        return _jp_21939()

# Lean: Corpus.Production.lcs.fill
def fill(xs_58: list[int], ys_59: list[int], m_60: int, n_61: int, i_62: int, j_63: int, memo: list[int]) -> list[int]:
    _x_21944 = m_60 < i_62
    if _x_21944:
        return memo
    else:
        _x_21946 = n_61 < j_63
        if _x_21946:
            _x_22038 = 1
            _x_22041 = i_62 + 1
            _x_22042 = 0
            _x_22045 = fill(xs_58, ys_59, m_60, n_61, _x_22041, 0, memo)
            return _x_22045
        else:
            _x_21954 = 1
            _x_21957 = n_61 + 1
            _x_21958 = i_62 * _x_21957
            _x_21959 = _x_21958 + j_63
            def _f_21961():
                _x_21960 = True
                return True
            _alt_21962 = _f_21961
            def _f_21970():
                _x_21966 = 0
                _x_21969 = j_63 == 0
                return _x_21969
            _alt_21971 = _f_21970
            _x_21975 = 0
            _x_21978 = i_62 == 0
            def _jp_22027(_y_21983: bool):
                _x_21984 = True
                _x_21985 = _y_21983 == True
                if _x_21985:
                    _x_22023 = j_63 + 1
                    _x_22024 = set_(None, memo, _x_21959, 0)
                    _x_22025 = fill(xs_58, ys_59, m_60, n_61, i_62, _x_22023, _x_22024)
                    return _x_22025
                else:
                    _x_21988 = _x_21987.field_2
                    _x_21993 = i_62 - 1
                    _x_21994 = _x_21988(_x_21989, xs_58, _x_21993)
                    _x_21995 = j_63 - 1
                    _x_21996 = _x_21988(_x_21989, ys_59, _x_21995)
                    _x_21997 = _x_21994 == _x_21996
                    _x_21998 = _x_21997 == True
                    def _jp_22021(_y_22017: int):
                        _x_22018 = j_63 + 1
                        _x_22019 = set_(None, memo, _x_21959, _y_22017)
                        _x_22020 = fill(xs_58, ys_59, m_60, n_61, i_62, _x_22018, _x_22019)
                        return _x_22020
                    if _x_21998:
                        _x_22012 = _x_22011.field_2
                        _x_22013 = _x_21993 * _x_21957
                        _x_22014 = _x_22013 + _x_21995
                        _x_22015 = _x_22012(_x_21989, memo, _x_22014)
                        _x_22016 = _x_22015 + 1
                        return _jp_22021(_x_22016)
                    else:
                        _x_22001 = max
                        _x_22003 = _x_22002.field_2
                        _x_22004 = _x_21993 * _x_21957
                        _x_22005 = _x_22004 + j_63
                        _x_22006 = _x_22003(_x_21989, memo, _x_22005)
                        _x_22007 = _x_21958 + _x_21995
                        _x_22008 = _x_22003(_x_21989, memo, _x_22007)
                        _x_22009 = _x_22001(_x_22006, _x_22008)
                        return _jp_22021(_x_22009)
            def _jp_22033():
                _x_22032 = _alt_21962()
                return _jp_22027(_x_22032)
            def _jp_22030():
                _x_22029 = _alt_21971()
                return _jp_22027(_x_22029)
            if _x_21978:
                return _jp_22033()
            else:
                return _jp_22030()

# Lean: Corpus.Production.lcsLength.fill
def fill(xs_70: list[int], ys_71: list[int], m_72: int, n_73: int, i_74: int, j_75: int, memo_76: list[int]) -> list[int]:
    _x_22050 = m_72 < i_74
    if _x_22050:
        return memo_76
    else:
        _x_22052 = n_73 < j_75
        if _x_22052:
            _x_22144 = 1
            _x_22147 = i_74 + 1
            _x_22148 = 0
            _x_22151 = fill(xs_70, ys_71, m_72, n_73, _x_22147, 0, memo_76)
            return _x_22151
        else:
            _x_22060 = 1
            _x_22063 = n_73 + 1
            _x_22064 = i_74 * _x_22063
            _x_22065 = _x_22064 + j_75
            def _f_22067():
                _x_22066 = True
                return True
            _alt_22068 = _f_22067
            def _f_22076():
                _x_22072 = 0
                _x_22075 = j_75 == 0
                return _x_22075
            _alt_22077 = _f_22076
            _x_22081 = 0
            _x_22084 = i_74 == 0
            def _jp_22133(_y_22089: bool):
                _x_22090 = True
                _x_22091 = _y_22089 == True
                if _x_22091:
                    _x_22129 = j_75 + 1
                    _x_22130 = set_(None, memo_76, _x_22065, 0)
                    _x_22131 = fill(xs_70, ys_71, m_72, n_73, i_74, _x_22129, _x_22130)
                    return _x_22131
                else:
                    _x_22094 = _x_22093.field_2
                    _x_22099 = i_74 - 1
                    _x_22100 = _x_22094(_x_22095, xs_70, _x_22099)
                    _x_22101 = j_75 - 1
                    _x_22102 = _x_22094(_x_22095, ys_71, _x_22101)
                    _x_22103 = _x_22100 == _x_22102
                    _x_22104 = _x_22103 == True
                    def _jp_22127(_y_22123: int):
                        _x_22124 = j_75 + 1
                        _x_22125 = set_(None, memo_76, _x_22065, _y_22123)
                        _x_22126 = fill(xs_70, ys_71, m_72, n_73, i_74, _x_22124, _x_22125)
                        return _x_22126
                    if _x_22104:
                        _x_22118 = _x_22117.field_2
                        _x_22119 = _x_22099 * _x_22063
                        _x_22120 = _x_22119 + _x_22101
                        _x_22121 = _x_22118(_x_22095, memo_76, _x_22120)
                        _x_22122 = _x_22121 + 1
                        return _jp_22127(_x_22122)
                    else:
                        _x_22107 = max
                        _x_22109 = _x_22108.field_2
                        _x_22110 = _x_22099 * _x_22063
                        _x_22111 = _x_22110 + j_75
                        _x_22112 = _x_22109(_x_22095, memo_76, _x_22111)
                        _x_22113 = _x_22064 + _x_22101
                        _x_22114 = _x_22109(_x_22095, memo_76, _x_22113)
                        _x_22115 = _x_22107(_x_22112, _x_22114)
                        return _jp_22127(_x_22115)
            def _jp_22139():
                _x_22138 = _alt_22068()
                return _jp_22133(_x_22138)
            def _jp_22136():
                _x_22135 = _alt_22077()
                return _jp_22133(_x_22135)
            if _x_22084:
                return _jp_22139()
            else:
                return _jp_22136()

# Lean: Corpus.Production.computeZArray.matchLength
def match_length(s_83: list[str], t: list[str], i_84: int, j_85: int) -> int:
    def _f_22157():
        _x_22156 = True
        return True
    _alt_22158 = _f_22157
    def _f_22162():
        _x_22159 = len(t)
        _x_22160 = _x_22159 <= j_85
        return _x_22160
    _alt_22163 = _f_22162
    _x_22164 = len(s_83)
    _x_22165 = _x_22164 <= i_84
    def _jp_22206(_y_22171: bool):
        _x_22172 = True
        _x_22173 = _y_22171 == True
        if _x_22173:
            _x_22202 = 0
            return 0
        else:
            _x_22179 = _x_22178.field_2
            _x_22181 = _x_22179(_x_22180, s_83, i_84)
            _x_22182 = _x_22179(_x_22180, t, j_85)
            _x_22183 = _x_22181 == _x_22182
            _x_22184 = _x_22183 == True
            if _x_22184:
                _x_22193 = 1
                _x_22196 = i_84 + 1
                _x_22197 = j_85 + 1
                _x_22198 = match_length(s_83, t, _x_22196, _x_22197)
                _x_22199 = 1 + _x_22198
                return _x_22199
            else:
                _x_22186 = 0
                return 0
    def _jp_22212():
        _x_22211 = _alt_22158()
        return _jp_22206(_x_22211)
    def _jp_22209():
        _x_22208 = _alt_22163()
        return _jp_22206(_x_22208)
    if _x_22165:
        return _jp_22212()
    else:
        return _jp_22209()

# Lean: Corpus.Production.computeZArray.compute
def compute(s_88: list[str], n_89: int, z: list[int], i_90: int, l: int, r: int) -> list[int]:
    while True:
        _x_22214 = n_89 <= i_90
        if _x_22214:
            return z
        else:
            _x_22216 = r < i_90
            if _x_22216:
                _x_22249 = 0
                _x_22252 = match_length(s_88, s_88, i_90, 0)
                _x_22253 = set_(None, z, i_90, _x_22252)
                _x_22254 = 0 < _x_22252
                if _x_22254:
                    _x_22268 = 1
                    _x_22271 = i_90 + 1
                    _x_22275 = i_90 + _x_22252
                    _x_22276 = _x_22275 - 1
                    s_88, n_89, z, i_90, l, r = s_88, n_89, _x_22253, _x_22271, i_90, _x_22276
                    continue
                else:
                    _x_22259 = 1
                    _x_22262 = i_90 + 1
                    s_88, n_89, z, i_90, l, r = s_88, n_89, _x_22253, _x_22262, l, r
                    continue
            else:
                _x_22221 = i_90 - l
                _x_22223 = _x_22222.field_2
                _x_22225 = _x_22223(_x_22224, z, _x_22221)
                _x_22229 = r - i_90
                _x_22230 = 1
                _x_22233 = _x_22229 + 1
                _x_22234 = _x_22225 < _x_22233
                if _x_22234:
                    _x_22244 = set_(None, z, i_90, _x_22225)
                    _x_22245 = i_90 + 1
                    s_88, n_89, z, i_90, l, r = s_88, n_89, _x_22244, _x_22245, l, r
                    continue
                else:
                    _x_22236 = r + 1
                    _x_22237 = match_length(s_88, s_88, _x_22236, _x_22233)
                    _x_22238 = _x_22233 + _x_22237
                    _x_22239 = set_(None, z, i_90, _x_22238)
                    _x_22240 = i_90 + 1
                    _x_22241 = r + _x_22237
                    s_88, n_89, z, i_90, l, r = s_88, n_89, _x_22239, _x_22240, i_90, _x_22241
                    continue

# Lean: Corpus.Production.naiveStringMatchAll.checkMatch
def check_match(t_95: list[str], p: list[str], i_96: int, j_97: int) -> bool:
    while True:
        _x_22283 = len(p)
        _x_22284 = _x_22283 <= j_97
        if _x_22284:
            _x_22311 = True
            return True
        else:
            _x_22290 = _x_22289.field_2
            _x_22295 = i_96 + j_97
            _x_22296 = _x_22290(_x_22291, t_95, _x_22295)
            _x_22297 = _x_22290(_x_22291, p, j_97)
            _x_22298 = _x_22296 == _x_22297
            _x_22299 = True
            _x_22300 = _x_22298 == True
            if _x_22300:
                _x_22304 = 1
                _x_22307 = j_97 + 1
                t_95, p, i_96, j_97 = t_95, p, i_96, _x_22307
                continue
            else:
                _x_22302 = False
                return False

# Lean: Corpus.Production.naiveStringMatchAll.search
def search(t_98: list[str], p_99: list[str], n_100: int, m_101: int, i_102: int, acc_103: list[int]) -> list[int]:
    while True:
        _x_22317 = n_100 - m_101
        _x_22318 = _x_22317 < i_102
        if _x_22318:
            _x_22347 = list(reversed(acc_103))
            return _x_22347
        else:
            _x_22320 = 0
            _x_22323 = check_match(t_98, p_99, i_102, 0)
            _x_22324 = True
            _x_22325 = _x_22323 == True
            if _x_22325:
                _x_22339 = 1
                _x_22342 = i_102 + 1
                _x_22343 = [i_102] + acc_103
                t_98, p_99, n_100, m_101, i_102, acc_103 = t_98, p_99, n_100, m_101, _x_22342, _x_22343
                continue
            else:
                _x_22330 = 1
                _x_22333 = i_102 + 1
                t_98, p_99, n_100, m_101, i_102, acc_103 = t_98, p_99, n_100, m_101, _x_22333, acc_103
                continue

# Lean: Corpus.Production.naiveStringMatch.checkMatch
def check_match(t_104: list[str], p_105: list[str], i_106: int, j_107: int) -> bool:
    while True:
        _x_22350 = len(p_105)
        _x_22351 = _x_22350 <= j_107
        if _x_22351:
            _x_22378 = True
            return True
        else:
            _x_22357 = _x_22356.field_2
            _x_22362 = i_106 + j_107
            _x_22363 = _x_22357(_x_22358, t_104, _x_22362)
            _x_22364 = _x_22357(_x_22358, p_105, j_107)
            _x_22365 = _x_22363 == _x_22364
            _x_22366 = True
            _x_22367 = _x_22365 == True
            if _x_22367:
                _x_22371 = 1
                _x_22374 = j_107 + 1
                t_104, p_105, i_106, j_107 = t_104, p_105, i_106, _x_22374
                continue
            else:
                _x_22369 = False
                return False

# Lean: Corpus.Production.naiveStringMatch.search
def search(t_108: list[str], p_109: list[str], n_110: int, m_111: int, i_112: int) -> int | None:
    while True:
        _x_22384 = n_110 - m_111
        _x_22385 = _x_22384 < i_112
        if _x_22385:
            _x_22406 = None
            return _x_22406
        else:
            _x_22387 = 0
            _x_22390 = check_match(t_108, p_109, i_112, 0)
            _x_22391 = True
            _x_22392 = _x_22390 == True
            if _x_22392:
                _x_22403 = i_112
                return _x_22403
            else:
                _x_22397 = 1
                _x_22400 = i_112 + 1
                t_108, p_109, n_110, m_111, i_112 = t_108, p_109, n_110, m_111, _x_22400
                continue

# Lean: Corpus.Production.lomutoPartition.go
def lomuto_partition_go(hi: int, pivot: int, arr: list[int], i_113: int, j_114: int) -> tuple[list[int], int]:
    while True:
        _x_22409 = hi <= j_114
        if _x_22409:
            _x_22438 = swap_if_in_bounds(None, arr, i_113, hi)
            _x_22439 = (_x_22438, i_113)
            return _x_22439
        else:
            _x_22412 = _x_22411.field_2
            _x_22414 = _x_22412(_x_22413, arr, j_114)
            _x_22415 = _x_22414 < pivot
            if _x_22415:
                _x_22426 = swap_if_in_bounds(None, arr, i_113, j_114)
                _x_22430 = 1
                _x_22433 = i_113 + 1
                _x_22434 = j_114 + 1
                hi, pivot, arr, i_113, j_114 = hi, pivot, _x_22426, _x_22433, _x_22434
                continue
            else:
                _x_22420 = 1
                _x_22423 = j_114 + 1
                hi, pivot, arr, i_113, j_114 = hi, pivot, arr, i_113, _x_22423
                continue

# Lean: Corpus.Production.UnionFind.ofSize.build
def of_size_build(n_116: int, i_117: int, nodes: list[UFNode]) -> list[UFNode]:
    while True:
        _x_22442 = n_116 <= i_117
        if _x_22442:
            return nodes
        else:
            _x_22447 = 1
            _x_22450 = i_117 + 1
            _x_22451 = 0
            _x_22454 = UFNode_mk(i_117, 0)
            _x_22455 = array_push(None, nodes, _x_22454)
            n_116, i_117, nodes = n_116, _x_22450, _x_22455
            continue

# Lean: Corpus.Production.Color.ctorIdx
def ctor_idx(x_118: Color) -> int:
    match x_118:
        case red():
            _x_22460 = 0
            return _x_22460
        case black():
            _x_22461 = 1
            return _x_22461

# Lean: Corpus.Production.instBEqColor.beq
def beq(x_22464: Color, y_22465: Color) -> bool:
    _x_22469 = ctor_idx(x_22464)
    _x_22470 = ctor_idx(y_22465)
    _x_22471 = _x_22469 == _x_22470
    return _x_22471

# Lean: Corpus.Production.instBEqColor
def inst_beq_color() -> Any:
    _x_22474 = BEq_mk(_x_22473)
    return _x_22474

# Lean: Corpus.Sorting.unique.go
def unique_go(xs_119: list[int], seen: list[int]) -> list[int]:
    while True:
        def _f_22476():
            _x_22475 = list(reversed(seen))
            return _x_22475
        _alt_22477 = _f_22476
        if len(xs_119) == 0:
            _x_22492 = _alt_22477()
            return _x_22492
        else:
            head_22493 = xs_119[0]
            tail_22494 = xs_119[1:]
            x_121 = head_22493
            rest_122 = tail_22494
            _x_22480 = x_121 in seen
            _x_22481 = True
            _x_22482 = _x_22480 == True
            if _x_22482:
                xs_119, seen = rest_122, seen
                continue
            else:
                _x_22484 = [x_121] + seen
                xs_119, seen = rest_122, _x_22484
                continue

# Lean: Corpus.Sorting.mode.count
def count(x_123: int, xs_124: list[int]) -> int:
    def _f_22514(acc_125: int, y_126: int):
        _x_22501 = y_126 == x_123
        _x_22502 = True
        _x_22503 = _x_22501 == True
        if _x_22503:
            _x_22509 = 1
            _x_22512 = acc_125 + 1
            return _x_22512
        else:
            return acc_125
    _x_22515 = 0
    _x_22518 = functools.reduce(_f_22514, xs_124, 0)
    return _x_22518

# Lean: Corpus.Sorting.mode.go
def mode_go(xs_127: list[int], best: int | None, best_count: int) -> int | None:
    while True:
        def _f_22520():
            return best
        _alt_22521 = _f_22520
        if len(xs_127) == 0:
            _x_22533 = _alt_22521()
            return _x_22533
        else:
            head_22534 = xs_127[0]
            tail_22535 = xs_127[1:]
            x_129 = head_22534
            rest_130 = tail_22535
            _x_22522 = count(x_129, xs_127)
            _x_22523 = best_count < _x_22522
            if _x_22523:
                _x_22527 = x_129
                xs_127, best, best_count = rest_130, _x_22527, _x_22522
                continue
            else:
                xs_127, best, best_count = rest_130, best, best_count
                continue

# Lean: Corpus.Sorting.insertionSort.insert
def insertion_sort_insert(x_132: int, sorted: list[int]) -> list[int]:
    def _f_22541():
        _x_22539 = []
        _x_22540 = [x_132] + _x_22539
        return _x_22540
    _alt_22542 = _f_22541
    def _f_22551(y_134: int, ys_135: list[int]):
        _x_22543 = x_132 <= y_134
        if _x_22543:
            _x_22548 = [y_134] + ys_135
            _x_22549 = [x_132] + _x_22548
            return _x_22549
        else:
            _x_22545 = insertion_sort_insert(x_132, ys_135)
            _x_22546 = [y_134] + _x_22545
            return _x_22546
    _alt_22552 = _f_22551
    if len(sorted) == 0:
        _x_22554 = _alt_22542()
        return _x_22554
    else:
        head_22555 = sorted[0]
        tail_22556 = sorted[1:]
        _x_22557 = _alt_22552(head_22555, tail_22556)
        return _x_22557

# Lean: Corpus.Sorting.insertionSort
def insertion_sort(xs_136: list[int]) -> list[int]:
    def _f_22561(sorted_137: list[int], x_138: int):
        _x_22560 = insertion_sort_insert(x_138, sorted_137)
        return _x_22560
    _x_22562 = []
    _x_22563 = functools.reduce(_f_22561, xs_136, _x_22562)
    return _x_22563

# Lean: Corpus.Sorting.gnomeSort.go
def gnome_sort_go(n_139: int, pos: int, arr_140: list[int]) -> list[int]:
    _x_22565 = n_139 <= pos
    if _x_22565:
        return arr_140
    else:
        def _f_22568():
            _x_22567 = True
            return True
        _alt_22569 = _f_22568
        def _f_22584():
            _x_22571 = _x_22570.field_2
            _x_22576 = 1
            _x_22579 = pos - 1
            _x_22580 = _x_22571(_x_22572, arr_140, _x_22579)
            _x_22581 = _x_22571(_x_22572, arr_140, pos)
            _x_22582 = _x_22580 <= _x_22581
            return _x_22582
        _alt_22585 = _f_22584
        _x_22589 = 0
        _x_22592 = pos == 0
        def _jp_22620(_y_22597: bool):
            _x_22598 = True
            _x_22599 = _y_22597 == True
            if _x_22599:
                _x_22614 = 1
                _x_22617 = pos + 1
                _x_22618 = gnome_sort_go(n_139, _x_22617, arr_140)
                return _x_22618
            else:
                _x_22604 = 1
                _x_22607 = pos - 1
                _x_22608 = swap_if_in_bounds(None, arr_140, pos, _x_22607)
                _x_22609 = gnome_sort_go(n_139, _x_22607, _x_22608)
                return _x_22609
        def _jp_22626():
            _x_22625 = _alt_22569()
            return _jp_22620(_x_22625)
        def _jp_22623():
            _x_22622 = _alt_22585()
            return _jp_22620(_x_22622)
        if _x_22592:
            return _jp_22626()
        else:
            return _jp_22623()

# Lean: Corpus.Sorting.radixSort.go
def radix_sort_go(max_val: int, exp: int, xs_143: list[int]) -> list[int]:
    while True:
        _x_22630 = max_val < exp
        if _x_22630:
            return xs_143
        else:
            def _f_22647(arr_144: list[list[int]], x_145: int):
                _x_22638 = x_145 // exp
                _x_22639 = 10
                _x_22642 = _x_22638 % 10
                def _f_22645(x_22643: list[int]):
                    _x_22644 = [x_145] + x_22643
                    return _x_22644
                _x_22646 = modify(None, arr_144, _x_22642, _f_22645)
                return _x_22646
            _x_22648 = 10
            _x_22651 = []
            _x_22652 = array_replicate(None, 10, _x_22651)
            _x_22653 = functools.reduce(_f_22647, xs_143, _x_22652)
            def _f_22659(acc_146: list[int], bucket: list[int]):
                _x_22657 = list(reversed(bucket))
                _x_22658 = acc_146 + _x_22657
                return _x_22658
            _x_22660 = 0
            _x_22663 = len(_x_22653)
            _x_22664 = array_foldl(None, None, _f_22659, _x_22651, _x_22653, 0, _x_22663)
            _x_22668 = exp * 10
            max_val, exp, xs_143 = max_val, _x_22668, _x_22664
            continue

# Lean: Corpus.Sorting.countingSort.expand
def expand(max_val_148: int, counts: list[int], i_149: int, acc_150: list[int]) -> list[int]:
    while True:
        _x_22673 = max_val_148 < i_149
        if _x_22673:
            return acc_150
        else:
            _x_22678 = 1
            _x_22681 = i_149 + 1
            _x_22685 = 0
            _x_22688 = get_d(None, counts, i_149, 0)
            _x_22689 = replicate_tr(None, _x_22688, i_149)
            _x_22690 = acc_150 + _x_22689
            max_val_148, counts, i_149, acc_150 = max_val_148, counts, _x_22681, _x_22690
            continue

# Lean: Corpus.Sorting.selectionSort.go.findMin
def find_min(n_151: int, arr_152: list[int], j_153: int, min_idx: int) -> int:
    _x_22695 = n_151 <= j_153
    if _x_22695:
        return min_idx
    else:
        _x_22700 = 1
        _x_22703 = j_153 + 1
        _x_22705 = _x_22704.field_2
        _x_22707 = _x_22705(_x_22706, arr_152, j_153)
        _x_22708 = _x_22705(_x_22706, arr_152, min_idx)
        _x_22709 = _x_22707 < _x_22708
        def _jp_22714(_y_22712: int):
            _x_22713 = find_min(n_151, arr_152, _x_22703, _y_22712)
            return _x_22713
        if _x_22709:
            return _jp_22714(j_153)
        else:
            return _jp_22714(min_idx)

# Lean: Corpus.Sorting.selectionSort.go
def selection_sort_go(n_154: int, i_155: int, arr_156: list[int]) -> list[int]:
    while True:
        _x_22718 = n_154 <= i_155
        if _x_22718:
            return arr_156
        else:
            _x_22720 = find_min(n_154, arr_156, i_155, i_155)
            _x_22724 = 1
            _x_22727 = i_155 + 1
            _x_22728 = swap_if_in_bounds(None, arr_156, i_155, _x_22720)
            n_154, i_155, arr_156 = n_154, _x_22727, _x_22728
            continue

# Lean: Corpus.Sorting.bubbleSort.outer.inner
def outer_inner(n_158: int, i_159: int, j_160: int, arr_161: list[int]) -> list[int]:
    _x_22736 = n_158 - i_159
    _x_22737 = 1
    _x_22740 = _x_22736 - 1
    _x_22741 = _x_22740 <= j_160
    if _x_22741:
        return arr_161
    else:
        _x_22744 = _x_22743.field_2
        _x_22749 = j_160 + 1
        _x_22750 = _x_22744(_x_22745, arr_161, _x_22749)
        _x_22751 = _x_22744(_x_22745, arr_161, j_160)
        _x_22752 = _x_22750 < _x_22751
        def _jp_22758(_y_22756: list[int]):
            _x_22757 = outer_inner(n_158, i_159, _x_22749, _y_22756)
            return _x_22757
        if _x_22752:
            _x_22755 = swap_if_in_bounds(None, arr_161, j_160, _x_22749)
            return _jp_22758(_x_22755)
        else:
            return _jp_22758(arr_161)

# Lean: Corpus.Sorting.bubbleSort.outer
def outer(n_163: int, i_164: int, arr_165: list[int]) -> list[int]:
    while True:
        _x_22762 = n_163 <= i_164
        if _x_22762:
            return arr_165
        else:
            _x_22767 = 1
            _x_22770 = i_164 + 1
            _x_22771 = 0
            _x_22774 = outer_inner(n_163, i_164, 0, arr_165)
            n_163, i_164, arr_165 = n_163, _x_22770, _x_22774
            continue

# Lean: Corpus.Sequences.vanEck.go
def van_eck_go(n_166: int, i_167: int, prev: int, last_seen: list[tuple[int, int]], acc_168: list[int]) -> list[int]:
    _x_22779 = n_166 < i_167
    if _x_22779:
        _x_22842 = list(reversed(acc_168))
        return _x_22842
    else:
        def _f_22784():
            _x_22781 = 0
            return 0
        _alt_22785 = _f_22784
        def _f_22795(fst_22786: int, idx_170: int):
            _x_22790 = 1
            _x_22793 = i_167 - 1
            _x_22794 = _x_22793 - idx_170
            return _x_22794
        _alt_22796 = _f_22795
        _x_22803 = next((p_171 for p_171 in last_seen if (p_171[0] == prev)), None)
        def _jp_22833(_y_22811: int):
            _x_22815 = 1
            _x_22818 = i_167 - 1
            _x_22819 = (prev, _x_22818)
            def _f_22824(p_172: tuple[int, int]):
                _x_22822 = p_172[0]
                _x_22823 = (lambda a, b: a != b)(prev)
                return _x_22823
            _x_22825 = [x for x in last_seen if _f_22824(x)]
            _x_22826 = [_x_22819] + _x_22825
            _x_22830 = i_167 + 1
            _x_22831 = [_y_22811] + acc_168
            _x_22832 = van_eck_go(n_166, _x_22830, _y_22811, _x_22826, _x_22831)
            return _x_22832
        def _jp_22840(_y_22837: int, _y_22838: int):
            _x_22839 = _alt_22796(_y_22837, _y_22838)
            return _jp_22833(_x_22839)
        def _jp_22836():
            _x_22835 = _alt_22785()
            return _jp_22833(_x_22835)
        if _x_22803 is None:
            return _jp_22836()
        else:
            val_22806 = _x_22803
            match val_22806:
                case (fst_22807, snd_22808):
                    return _jp_22840(fst_22807, snd_22808)

# Lean: Corpus.Sequences.firstNPrimes.isPrime.check
def first_nprimes_is_prime_check(n_173: int, d: int) -> bool:
    while True:
        _x_22848 = d * d
        _x_22849 = n_173 < _x_22848
        if _x_22849:
            _x_22877 = True
            return True
        else:
            _x_22857 = n_173 % d
            _x_22858 = 0
            _x_22861 = _x_22857 == 0
            _x_22862 = True
            _x_22863 = _x_22861 == True
            if _x_22863:
                _x_22874 = False
                return False
            else:
                _x_22868 = 1
                _x_22871 = d + 1
                n_173, d = n_173, _x_22871
                continue

# Lean: Corpus.Sequences.firstNPrimes.isPrime
def first_nprimes_is_prime(n_174: int) -> bool:
    _x_22880 = 2
    _x_22883 = n_174 < 2
    if _x_22883:
        _x_22887 = False
        return False
    else:
        _x_22885 = first_nprimes_is_prime_check(n_174, 2)
        return _x_22885

# Lean: Corpus.Sequences.firstNPrimes.go
def first_nprimes_go(n_175: int, candidate: int, found: list[int]) -> list[int]:
    while True:
        _x_22890 = len(found)
        _x_22891 = n_175 <= _x_22890
        if _x_22891:
            _x_22917 = list(reversed(found))
            return _x_22917
        else:
            _x_22893 = first_nprimes_is_prime(candidate)
            _x_22894 = True
            _x_22895 = _x_22893 == True
            if _x_22895:
                _x_22909 = 1
                _x_22912 = candidate + 1
                _x_22913 = [candidate] + found
                n_175, candidate, found = n_175, _x_22912, _x_22913
                continue
            else:
                _x_22900 = 1
                _x_22903 = candidate + 1
                n_175, candidate, found = n_175, _x_22903, found
                continue

# Lean: Corpus.Sequences.recaman.go
def recaman_go(n_176: int, i_177: int, prev_178: int, seen_179: list[int], acc_180: list[int]) -> list[int]:
    _x_22920 = n_176 < i_177
    if _x_22920:
        _x_22973 = list(reversed(acc_180))
        return _x_22973
    else:
        _x_22925 = prev_178 - i_177
        def _f_22927():
            _x_22926 = False
            return False
        _alt_22928 = _f_22927
        def _f_22933():
            _x_22931 = _x_22925 in seen_179
            _x_22932 = not _x_22931
            return _x_22932
        _alt_22934 = _f_22933
        _x_22935 = 0
        _x_22938 = 0 < _x_22925
        def _jp_22965(_y_22944: bool):
            _x_22945 = True
            _x_22946 = _y_22944 == True
            def _jp_22964(_y_22953: int):
                _x_22957 = 1
                _x_22960 = i_177 + 1
                _x_22961 = [_y_22953] + seen_179
                _x_22962 = [_y_22953] + acc_180
                _x_22963 = recaman_go(n_176, _x_22960, _y_22953, _x_22961, _x_22962)
                return _x_22963
            if _x_22946:
                return _jp_22964(_x_22925)
            else:
                _x_22951 = prev_178 + i_177
                return _jp_22964(_x_22951)
        def _jp_22968():
            _x_22967 = _alt_22928()
            return _jp_22965(_x_22967)
        def _jp_22971():
            _x_22970 = _alt_22934()
            return _jp_22965(_x_22970)
        if _x_22938:
            return _jp_22971()
        else:
            return _jp_22968()

# Lean: Corpus.Sequences.lookAndSayNext.go
def look_and_say_next_go(xs_185: list[int], curr: int, count: int, acc_186: list[int]) -> list[int]:
    while True:
        def _f_22984():
            _x_22979 = []
            _x_22980 = [curr] + _x_22979
            _x_22981 = [count] + _x_22980
            _x_22982 = acc_186 + _x_22981
            _x_22983 = list(reversed(_x_22982))
            return _x_22983
        _alt_22985 = _f_22984
        if len(xs_185) == 0:
            _x_23012 = _alt_22985()
            return _x_23012
        else:
            head_23013 = xs_185[0]
            tail_23014 = xs_185[1:]
            x_188 = head_23013
            rest_189 = tail_23014
            _x_22989 = x_188 == curr
            _x_22990 = True
            _x_22991 = _x_22989 == True
            if _x_22991:
                _x_23003 = 1
                _x_23006 = count + 1
                xs_185, curr, count, acc_186 = rest_189, curr, _x_23006, acc_186
                continue
            else:
                _x_22993 = 1
                _x_22996 = [count] + acc_186
                _x_22997 = [curr] + _x_22996
                xs_185, curr, count, acc_186 = rest_189, x_188, 1, _x_22997
                continue

# Lean: Corpus.Sequences.repunit.go
def repunit_go(n_190: int, acc_191: int) -> int:
    while True:
        _x_23021 = 0
        _x_23024 = n_190 == 0
        _x_23025 = True
        _x_23026 = _x_23024 == True
        if _x_23026:
            return acc_191
        else:
            _x_23031 = 1
            _x_23034 = n_190 - 1
            _x_23041 = 10
            _x_23044 = acc_191 * 10
            _x_23045 = _x_23044 + 1
            n_190, acc_191 = _x_23034, _x_23045
            continue

# Lean: Corpus.Sequences.narayana.binomial.go
def binomial_go(n_192: int, k_193: int, i_194: int, acc_195: int) -> int:
    while True:
        _x_23053 = i_194 == k_193
        _x_23054 = True
        _x_23055 = _x_23053 == True
        if _x_23055:
            return acc_195
        else:
            _x_23060 = 1
            _x_23063 = i_194 + 1
            _x_23073 = n_192 - i_194
            _x_23074 = acc_195 * _x_23073
            _x_23075 = _x_23074 // _x_23063
            n_192, k_193, i_194, acc_195 = n_192, k_193, _x_23063, _x_23075
            continue

# Lean: Corpus.Sequences.narayana.binomial
def binomial(n_196: int, k_197: int) -> int:
    _x_23080 = n_196 < k_197
    if _x_23080:
        _x_23100 = 0
        return 0
    else:
        _x_23085 = n_196 - k_197
        _x_23086 = _x_23085 < k_197
        def _jp_23098(_y_23090: int):
            _x_23091 = 0
            _x_23094 = 1
            _x_23097 = binomial_go(n_196, _y_23090, 0, 1)
            return _x_23097
        if _x_23086:
            _x_23089 = n_196 - k_197
            return _jp_23098(_x_23089)
        else:
            return _jp_23098(k_197)

# Lean: Corpus.Sequences.motzkin.go
def motzkin_go(n_199: int, k_200: int, acc_201: int) -> int:
    while True:
        _x_23111 = 1
        _x_23114 = n_199 + 1
        _x_23115 = k_200 == _x_23114
        _x_23116 = True
        _x_23117 = _x_23115 == True
        if _x_23117:
            return acc_201
        else:
            _x_23119 = k_200 + 1
            _x_23123 = motzkin(k_200)
            _x_23127 = n_199 - 1
            _x_23128 = _x_23127 - k_200
            _x_23129 = motzkin(_x_23128)
            _x_23130 = _x_23123 * _x_23129
            _x_23131 = acc_201 + _x_23130
            n_199, k_200, acc_201 = n_199, _x_23119, _x_23131
            continue

# Lean: Corpus.Sequences.jacobsthal.go
def jacobsthal_go(n_202: int, a_203: int, b: int) -> int:
    while True:
        _x_23139 = 0
        _x_23142 = n_202 == 0
        _x_23143 = True
        _x_23144 = _x_23142 == True
        if _x_23144:
            return a_203
        else:
            _x_23149 = 1
            _x_23152 = n_202 - 1
            _x_23159 = 2
            _x_23162 = 2 * a_203
            _x_23163 = b + _x_23162
            n_202, a_203, b = _x_23152, b, _x_23163
            continue

# Lean: Corpus.Sequences.perrin.go
def perrin_go(n_204: int, a_205: int, b_206: int, c_207: int) -> int:
    while True:
        _x_23171 = 0
        _x_23174 = n_204 == 0
        _x_23175 = True
        _x_23176 = _x_23174 == True
        if _x_23176:
            return a_205
        else:
            _x_23181 = 1
            _x_23184 = n_204 - 1
            _x_23188 = a_205 + b_206
            n_204, a_205, b_206, c_207 = _x_23184, b_206, c_207, _x_23188
            continue

# Lean: Corpus.Sequences.padovan.go
def padovan_go(n_208: int, a_209: int, b_210: int, c_211: int) -> int:
    while True:
        _x_23196 = 0
        _x_23199 = n_208 == 0
        _x_23200 = True
        _x_23201 = _x_23199 == True
        if _x_23201:
            return a_209
        else:
            _x_23206 = 1
            _x_23209 = n_208 - 1
            _x_23213 = a_209 + b_210
            n_208, a_209, b_210, c_211 = _x_23209, b_210, c_211, _x_23213
            continue

# Lean: Corpus.Sequences.pell.go
def pell_go(n_212: int, a_213: int, b_214: int) -> int:
    while True:
        _x_23221 = 0
        _x_23224 = n_212 == 0
        _x_23225 = True
        _x_23226 = _x_23224 == True
        if _x_23226:
            return a_213
        else:
            _x_23231 = 1
            _x_23234 = n_212 - 1
            _x_23241 = 2
            _x_23244 = 2 * b_214
            _x_23245 = _x_23244 + a_213
            n_212, a_213, b_214 = _x_23234, b_214, _x_23245
            continue

# Lean: Corpus.Sequences.tribonacci.go
def tribonacci_go(n_215: int, a_216: int, b_217: int, c_218: int) -> int:
    while True:
        _x_23253 = 0
        _x_23256 = n_215 == 0
        _x_23257 = True
        _x_23258 = _x_23256 == True
        if _x_23258:
            return a_216
        else:
            _x_23263 = 1
            _x_23266 = n_215 - 1
            _x_23270 = a_216 + b_217
            _x_23271 = _x_23270 + c_218
            n_215, a_216, b_217, c_218 = _x_23266, b_217, c_218, _x_23271
            continue

# Lean: Corpus.Sequences.lucas.go
def lucas_go(n_219: int, a_220: int, b_221: int) -> int:
    while True:
        _x_23279 = 0
        _x_23282 = n_219 == 0
        _x_23283 = True
        _x_23284 = _x_23282 == True
        if _x_23284:
            return a_220
        else:
            _x_23289 = 1
            _x_23292 = n_219 - 1
            _x_23296 = a_220 + b_221
            n_219, a_220, b_221 = _x_23292, b_221, _x_23296
            continue

# Lean: Corpus.Sequences.fibonacci.go
def sequences_fibonacci_go(n_222: int, a_223: int, b_224: int) -> int:
    while True:
        _x_23304 = 0
        _x_23307 = n_222 == 0
        _x_23308 = True
        _x_23309 = _x_23307 == True
        if _x_23309:
            return a_223
        else:
            _x_23314 = 1
            _x_23317 = n_222 - 1
            _x_23321 = a_223 + b_224
            n_222, a_223, b_224 = _x_23317, b_224, _x_23321
            continue

# Lean: Corpus.Combinatorics.integerPartitions.go
def integer_partitions_go(n_225: int, max: int) -> list[list[int]]:
    _x_23329 = 0
    _x_23332 = n_225 == 0
    _x_23333 = True
    _x_23334 = _x_23332 == True
    if _x_23334:
        _x_23361 = []
        _x_23362 = []
        _x_23363 = [_x_23361] + _x_23362
        return _x_23363
    else:
        _x_23336 = max == 0
        _x_23337 = _x_23336 == True
        if _x_23337:
            _x_23358 = []
            return _x_23358
        else:
            def _f_23341(x_23339: list[int]):
                _x_23340 = [max] + x_23339
                return _x_23340
            _x_23345 = n_225 - max
            _x_23346 = integer_partitions_go(_x_23345, max)
            _x_23347 = [_f_23341(x) for x in _x_23346]
            _x_23348 = 1
            _x_23351 = max - 1
            _x_23352 = integer_partitions_go(n_225, _x_23351)
            _x_23356 = _x_23347 + _x_23352
            return _x_23356

# Lean: Corpus.Combinatorics.compositions.go
def compositions_go(n_226: int, k_227: int, acc_228: list[list[int]]) -> list[list[int]]:
    while True:
        _x_23366 = n_226 < k_227
        if _x_23366:
            return acc_228
        else:
            _x_23371 = 1
            _x_23374 = k_227 + 1
            def _f_23380(x_23378: list[int]):
                _x_23379 = [k_227] + x_23378
                return _x_23379
            _x_23384 = n_226 - k_227
            _x_23385 = compositions(_x_23384)
            _x_23386 = [_f_23380(x) for x in _x_23385]
            _x_23387 = acc_228 + _x_23386
            n_226, k_227, acc_228 = n_226, _x_23374, _x_23387
            continue

# Lean: Corpus.Combinatorics.prevPermutation.findI
def find_i(arr_229: list[int], i_230: int) -> int | None:
    while True:
        _x_23395 = 0
        _x_23398 = i_230 == 0
        _x_23399 = True
        _x_23400 = _x_23398 == True
        if _x_23400:
            _x_23421 = None
            return _x_23421
        else:
            _x_23403 = _x_23402.field_2
            _x_23405 = _x_23403(_x_23404, arr_229, i_230)
            _x_23409 = 1
            _x_23412 = i_230 - 1
            _x_23413 = _x_23403(_x_23404, arr_229, _x_23412)
            _x_23414 = _x_23405 < _x_23413
            if _x_23414:
                _x_23418 = _x_23412
                return _x_23418
            else:
                arr_229, i_230 = arr_229, _x_23412
                continue

# Lean: Corpus.Combinatorics.prevPermutation.reverseFrom.go
def reverse_from_go(arr_231: list[int], l_232: int, r_233: int) -> list[int]:
    while True:
        _x_23424 = r_233 <= l_232
        if _x_23424:
            return arr_231
        else:
            _x_23426 = swap_if_in_bounds(None, arr_231, l_232, r_233)
            _x_23430 = 1
            _x_23433 = l_232 + 1
            _x_23437 = r_233 - 1
            arr_231, l_232, r_233 = _x_23426, _x_23433, _x_23437
            continue

# Lean: Corpus.Combinatorics.prevPermutation.reverseFrom
def reverse_from(arr_234: list[int], start: int) -> list[int]:
    _x_23445 = len(arr_234)
    _x_23446 = 1
    _x_23449 = _x_23445 - 1
    _x_23450 = reverse_from_go(arr_234, start, _x_23449)
    return _x_23450

# Lean: Corpus.Combinatorics.prevPermutation.findJ
def find_j(arr_235: list[int], i_236: int, j_237: int) -> int:
    while True:
        _x_23458 = 1
        _x_23461 = i_236 + 1
        _x_23462 = j_237 == _x_23461
        _x_23463 = True
        _x_23464 = _x_23462 == True
        if _x_23464:
            return j_237
        else:
            _x_23467 = _x_23466.field_2
            _x_23472 = j_237 - 1
            _x_23473 = _x_23467(_x_23468, arr_235, _x_23472)
            _x_23474 = _x_23467(_x_23468, arr_235, i_236)
            _x_23475 = _x_23473 < _x_23474
            if _x_23475:
                _x_23479 = j_237 - 1
                return _x_23479
            else:
                arr_235, i_236, j_237 = arr_235, i_236, _x_23472
                continue

# Lean: Corpus.Combinatorics.nextPermutation.findI
def find_i(arr_238: list[int], i_239: int) -> int | None:
    while True:
        _x_23487 = 0
        _x_23490 = i_239 == 0
        _x_23491 = True
        _x_23492 = _x_23490 == True
        if _x_23492:
            _x_23513 = None
            return _x_23513
        else:
            _x_23495 = _x_23494.field_2
            _x_23500 = 1
            _x_23503 = i_239 - 1
            _x_23504 = _x_23495(_x_23496, arr_238, _x_23503)
            _x_23505 = _x_23495(_x_23496, arr_238, i_239)
            _x_23506 = _x_23504 < _x_23505
            if _x_23506:
                _x_23510 = _x_23503
                return _x_23510
            else:
                arr_238, i_239 = arr_238, _x_23503
                continue

# Lean: Corpus.Combinatorics.nextPermutation.reverseFrom.go
def reverse_from_go(arr_240: list[int], l_241: int, r_242: int) -> list[int]:
    while True:
        _x_23516 = r_242 <= l_241
        if _x_23516:
            return arr_240
        else:
            _x_23518 = swap_if_in_bounds(None, arr_240, l_241, r_242)
            _x_23522 = 1
            _x_23525 = l_241 + 1
            _x_23529 = r_242 - 1
            arr_240, l_241, r_242 = _x_23518, _x_23525, _x_23529
            continue

# Lean: Corpus.Combinatorics.nextPermutation.reverseFrom
def reverse_from(arr_243: list[int], start_244: int) -> list[int]:
    _x_23537 = len(arr_243)
    _x_23538 = 1
    _x_23541 = _x_23537 - 1
    _x_23542 = reverse_from_go(arr_243, start_244, _x_23541)
    return _x_23542

# Lean: Corpus.Combinatorics.nextPermutation.findJ
def find_j(arr_245: list[int], i_246: int, j_247: int) -> int:
    while True:
        _x_23550 = 1
        _x_23553 = i_246 + 1
        _x_23554 = j_247 == _x_23553
        _x_23555 = True
        _x_23556 = _x_23554 == True
        if _x_23556:
            return j_247
        else:
            _x_23559 = _x_23558.field_2
            _x_23561 = _x_23559(_x_23560, arr_245, i_246)
            _x_23565 = j_247 - 1
            _x_23566 = _x_23559(_x_23560, arr_245, _x_23565)
            _x_23567 = _x_23561 < _x_23566
            if _x_23567:
                _x_23571 = j_247 - 1
                return _x_23571
            else:
                arr_245, i_246, j_247 = arr_245, i_246, _x_23565
                continue

# Lean: Corpus.Combinatorics.permutationRank.go
def permutation_rank_go(n_248: int, code: list[int], pos_249: int, acc_250: int) -> int:
    while True:
        def _f_23576():
            return acc_250
        _alt_23577 = _f_23576
        if len(code) == 0:
            _x_23600 = _alt_23577()
            return _x_23600
        else:
            head_23601 = code[0]
            tail_23602 = code[1:]
            c_252 = head_23601
            rest_253 = tail_23602
            _x_23581 = 1
            _x_23584 = pos_249 + 1
            _x_23591 = n_248 - pos_249
            _x_23592 = _x_23591 - 1
            _x_23593 = factorial(_x_23592)
            _x_23594 = c_252 * _x_23593
            _x_23595 = acc_250 + _x_23594
            n_248, code, pos_249, acc_250 = n_248, rest_253, _x_23584, _x_23595
            continue

# Lean: Corpus.Combinatorics.nthPermutation.go
def nth_permutation_go(k_254: int, n_255: int, available: list[int], acc_256: list[int]) -> list[int]:
    while True:
        def _f_23607():
            _x_23606 = list(reversed(acc_256))
            return _x_23606
        _alt_23608 = _f_23607
        if len(available) == 0:
            _x_23642 = _alt_23608()
            return _x_23642
        else:
            _x_23646 = (lambda h_23643: _uniq_67840(available))(None)
            return _x_23646

# Lean: Corpus.Combinatorics.fromLehmerCode.go
def from_lehmer_code_go(code_258: list[int], available_259: list[int], acc_260: list[int]) -> list[int]:
    while True:
        def _f_23650():
            _x_23649 = list(reversed(acc_260))
            return _x_23649
        _alt_23651 = _f_23650
        if len(code_258) == 0:
            _x_23667 = _alt_23651()
            return _x_23667
        else:
            head_23668 = code_258[0]
            tail_23669 = code_258[1:]
            c_262 = head_23668
            rest_263 = tail_23669
            _x_23652 = 0
            _x_23655 = get_d(None, available_259, c_262, 0)
            def _f_23660(x_23656: int):
                _x_23659 = (lambda a, b: a != b)(_x_23655)
                return _x_23659
            _x_23661 = [x for x in available_259 if _f_23660(x)]
            _x_23662 = [_x_23655] + acc_260
            code_258, available_259, acc_260 = rest_263, _x_23661, _x_23662
            continue

# Lean: Corpus.Combinatorics.lehmerCode.go
def lehmer_code_go(perm: list[int], acc_264: list[int]) -> list[int]:
    while True:
        def _f_23674():
            _x_23673 = list(reversed(acc_264))
            return _x_23673
        _alt_23675 = _f_23674
        if len(perm) == 0:
            _x_23697 = _alt_23675()
            return _x_23697
        else:
            head_23698 = perm[0]
            tail_23699 = perm[1:]
            x_266 = head_23698
            rest_267 = tail_23699
            def _f_23687(acc_268: int, y_269: int):
                _x_23676 = y_269 < x_266
                if _x_23676:
                    _x_23682 = 1
                    _x_23685 = acc_268 + 1
                    return _x_23685
                else:
                    return acc_268
            _x_23688 = 0
            _x_23691 = functools.reduce(_f_23687, rest_267, 0)
            _x_23692 = [_x_23691] + acc_264
            perm, acc_264 = rest_267, _x_23692
            continue

# Lean: Corpus.Combinatorics.countInversions.count
def count(xs_271: list[int]) -> int:
    def _f_23706():
        _x_23703 = 0
        return 0
    _alt_23707 = _f_23706
    def _f_23726(x_273: int, rest_274: list[int]):
        def _f_23719(acc_275: int, y_276: int):
            _x_23711 = y_276 < x_273
            if _x_23711:
                _x_23714 = 1
                _x_23717 = acc_275 + 1
                return _x_23717
            else:
                return acc_275
        _x_23720 = 0
        _x_23723 = functools.reduce(_f_23719, rest_274, 0)
        _x_23724 = count(rest_274)
        _x_23725 = _x_23723 + _x_23724
        return _x_23725
    _alt_23727 = _f_23726
    if len(xs_271) == 0:
        _x_23729 = _alt_23707()
        return _x_23729
    else:
        head_23730 = xs_271[0]
        tail_23731 = xs_271[1:]
        _x_23732 = _alt_23727(head_23730, tail_23731)
        return _x_23732

# Lean: Corpus.Combinatorics.partitionCount.p
def p(n_277: int, k_278: int) -> int:
    _x_23738 = 0
    _x_23741 = n_277 == 0
    _x_23742 = True
    _x_23743 = _x_23741 == True
    if _x_23743:
        _x_23771 = 1
        return 1
    else:
        _x_23745 = k_278 == 0
        _x_23746 = _x_23745 == True
        if _x_23746:
            return 1
        else:
            _x_23748 = n_277 < k_278
            if _x_23748:
                _x_23765 = p(n_277, n_277)
                return _x_23765
            else:
                _x_23756 = n_277 - k_278
                _x_23757 = p(_x_23756, k_278)
                _x_23758 = 1
                _x_23761 = k_278 - 1
                _x_23762 = p(n_277, _x_23761)
                _x_23763 = _x_23757 + _x_23762
                return _x_23763

# Lean: Corpus.Combinatorics.binomial.go
def binomial_go(n_279: int, k_280: int, i_281: int, acc_282: int) -> int:
    while True:
        _x_23779 = i_281 == k_280
        _x_23780 = True
        _x_23781 = _x_23779 == True
        if _x_23781:
            return acc_282
        else:
            _x_23786 = 1
            _x_23789 = i_281 + 1
            _x_23799 = n_279 - i_281
            _x_23800 = acc_282 * _x_23799
            _x_23801 = _x_23800 // _x_23789
            n_279, k_280, i_281, acc_282 = n_279, k_280, _x_23789, _x_23801
            continue

# Lean: Corpus.Combinatorics.binomial
def binomial(n_283: int, k_284: int) -> int:
    _x_23806 = n_283 < k_284
    if _x_23806:
        _x_23826 = 0
        return 0
    else:
        _x_23811 = n_283 - k_284
        _x_23812 = _x_23811 < k_284
        def _jp_23824(_y_23816: int):
            _x_23817 = 0
            _x_23820 = 1
            _x_23823 = binomial_go(n_283, _y_23816, 0, 1)
            return _x_23823
        if _x_23812:
            _x_23815 = n_283 - k_284
            return _jp_23824(_x_23815)
        else:
            return _jp_23824(k_284)

# Lean: Corpus.Combinatorics.bell.go
def bell_go(n_286: int, i_287: int, acc_288: int) -> int:
    while True:
        _x_23837 = 1
        _x_23840 = n_286 + 1
        _x_23841 = i_287 == _x_23840
        _x_23842 = True
        _x_23843 = _x_23841 == True
        if _x_23843:
            return acc_288
        else:
            _x_23845 = i_287 + 1
            _x_23846 = stirling2(n_286, i_287)
            _x_23847 = acc_288 + _x_23846
            n_286, i_287, acc_288 = n_286, _x_23845, _x_23847
            continue

# Lean: Corpus.Combinatorics.factorial.go
def factorial_go(n_289: int, acc_290: int) -> int:
    while True:
        _x_23855 = 0
        _x_23858 = n_289 == 0
        _x_23859 = True
        _x_23860 = _x_23858 == True
        if _x_23860:
            return acc_290
        else:
            _x_23865 = 1
            _x_23868 = n_289 - 1
            _x_23872 = n_289 * acc_290
            n_289, acc_290 = _x_23868, _x_23872
            continue

# Lean: Corpus.Combinatorics.factorial
def factorial(n_291: int) -> int:
    _x_23877 = 1
    _x_23880 = factorial_go(n_291, 1)
    return _x_23880

# Lean: Corpus.Combinatorics.fallingFactorial.go
def falling_factorial_go(x_292: int, n_293: int, i_294: int, acc_295: int) -> int:
    while True:
        _x_23885 = i_294 == n_293
        _x_23886 = True
        _x_23887 = _x_23885 == True
        if _x_23887:
            return acc_295
        else:
            _x_23892 = 1
            _x_23895 = i_294 + 1
            _x_23902 = x_292 - i_294
            _x_23903 = acc_295 * _x_23902
            x_292, n_293, i_294, acc_295 = x_292, n_293, _x_23895, _x_23903
            continue

# Lean: Corpus.Combinatorics.risingFactorial.go
def rising_factorial_go(x_296: int, n_297: int, i_298: int, acc_299: int) -> int:
    while True:
        _x_23911 = i_298 == n_297
        _x_23912 = True
        _x_23913 = _x_23911 == True
        if _x_23913:
            return acc_299
        else:
            _x_23918 = 1
            _x_23921 = i_298 + 1
            _x_23925 = x_296 + i_298
            _x_23926 = acc_299 * _x_23925
            x_296, n_297, i_298, acc_299 = x_296, n_297, _x_23921, _x_23926
            continue

# Lean: Corpus.Geometry.segmentsIntersect.onSegment
def on_segment(p_300: Point2D, q: Point2D, r_301: Point2D) -> bool:
    def _f_23932():
        _x_23931 = False
        return False
    _alt_23933 = _f_23932
    def _f_23942():
        _x_23935 = min
        _x_23936 = p_300.field_1
        _x_23937 = r_301.field_1
        _x_23938 = _x_23935(_x_23936, _x_23937)
        _x_23939 = q.field_1
        _x_23940 = dec_le(_x_23938, _x_23939)
        return _x_23940
    _alt_23943 = _f_23942
    _alt_23944 = _f_23932
    def _f_23953():
        _x_23945 = q.field_1
        _x_23947 = max
        _x_23948 = p_300.field_1
        _x_23949 = r_301.field_1
        _x_23950 = _x_23947(_x_23948, _x_23949)
        _x_23951 = dec_le(_x_23945, _x_23950)
        return _x_23951
    _alt_23954 = _f_23953
    _alt_23955 = _f_23932
    def _f_23964():
        _x_23957 = min
        _x_23958 = p_300.field_0
        _x_23959 = r_301.field_0
        _x_23960 = _x_23957(_x_23958, _x_23959)
        _x_23961 = q.field_0
        _x_23962 = dec_le(_x_23960, _x_23961)
        return _x_23962
    _alt_23965 = _f_23964
    _x_23966 = q.field_0
    _x_23968 = max
    _x_23969 = p_300.field_0
    _x_23970 = r_301.field_0
    _x_23971 = _x_23968(_x_23969, _x_23970)
    _x_23972 = dec_le(_x_23966, _x_23971)
    def _jp_23996(_y_23978: bool):
        def _jp_23989(_y_23983: bool):
            if _y_23983:
                _x_23987 = _alt_23943()
                return _x_23987
            else:
                _x_23985 = _alt_23933()
                return _x_23985
        def _jp_23992():
            _x_23991 = _alt_23944()
            return _jp_23989(_x_23991)
        def _jp_23995():
            _x_23994 = _alt_23954()
            return _jp_23989(_x_23994)
        if _y_23978:
            return _jp_23995()
        else:
            return _jp_23992()
    def _jp_23999():
        _x_23998 = _alt_23955()
        return _jp_23996(_x_23998)
    def _jp_24002():
        _x_24001 = _alt_23965()
        return _jp_23996(_x_24001)
    if _x_23972:
        return _jp_24002()
    else:
        return _jp_23999()

# Lean: Corpus.Geometry.isConvexPolygon.checkSign
def check_sign(c_306: float, sign: bool | None) -> bool:
    def _f_24005():
        _x_24004 = True
        return True
    _alt_24006 = _f_24005
    def _f_24030(s_308: bool):
        _alt_24007 = _f_24005
        def _f_24017():
            _x_24011 = 0
            _x_24014 = dec_lt(0, c_306)
            _x_24016 = _x_24014 == s_308
            return _x_24016
        _alt_24018 = _f_24017
        _x_24021 = 0
        _x_24024 = c_306 == 0
        if _x_24024:
            _x_24028 = _alt_24007()
            return _x_24028
        else:
            _x_24026 = _alt_24018()
            return _x_24026
    _alt_24031 = _f_24030
    if sign is None:
        _x_24033 = _alt_24006()
        return _x_24033
    else:
        val_24034 = sign
        _x_24035 = _alt_24031(val_24034)
        return _x_24035

# Lean: Corpus.Geometry.isConvexPolygon.sub
def sub(a_310: Point2D, b_311: Point2D) -> Point2D:
    _x_24041 = a_310.field_0
    _x_24042 = b_311.field_0
    _x_24043 = _x_24041 - _x_24042
    _x_24044 = a_310.field_1
    _x_24045 = b_311.field_1
    _x_24046 = _x_24044 - _x_24045
    _x_24047 = Point2D_mk(_x_24043, _x_24046)
    return _x_24047

# Lean: Corpus.Geometry.isConvexPolygon.check
def is_convex_polygon_check(first: Point2D, second: Point2D, prev2: Point2D, prev1: Point2D, vs: list[Point2D], sign_312: bool | None) -> bool:
    def _f_24066():
        _x_24049 = sub(prev1, prev2)
        _x_24050 = sub(first, prev1)
        _x_24051 = cross2d(_x_24049, _x_24050)
        _x_24052 = sub(second, first)
        _x_24053 = cross2d(_x_24050, _x_24052)
        def _f_24055():
            _x_24054 = False
            return False
        _alt_24056 = _f_24055
        def _f_24058():
            _x_24057 = check_sign(_x_24053, sign_312)
            return _x_24057
        _alt_24059 = _f_24058
        _x_24060 = check_sign(_x_24051, sign_312)
        if _x_24060:
            _x_24064 = _alt_24059()
            return _x_24064
        else:
            _x_24062 = _alt_24056()
            return _x_24062
    _alt_24067 = _f_24066
    def _f_24098(v: Point2D, rest_: list[Point2D]):
        _x_24068 = sub(prev1, prev2)
        _x_24069 = sub(v, prev1)
        _x_24070 = cross2d(_x_24068, _x_24069)
        def _f_24072():
            _x_24071 = False
            return False
        _alt_24073 = _f_24072
        def _f_24090():
            _x_24076 = 0
            _x_24079 = _x_24070 == 0
            _x_24080 = True
            _x_24081 = _x_24079 == True
            def _jp_24089(_y_24087: bool | None):
                _x_24088 = is_convex_polygon_check(first, second, prev1, v, rest_, _y_24087)
                return _x_24088
            if _x_24081:
                return _jp_24089(sign_312)
            else:
                _x_24083 = dec_lt(0, _x_24070)
                _x_24085 = _x_24083
                return _jp_24089(_x_24085)
        _alt_24091 = _f_24090
        _x_24092 = check_sign(_x_24070, sign_312)
        if _x_24092:
            _x_24096 = _alt_24091()
            return _x_24096
        else:
            _x_24094 = _alt_24073()
            return _x_24094
    _alt_24099 = _f_24098
    if len(vs) == 0:
        _x_24101 = _alt_24067()
        return _x_24101
    else:
        head_24102 = vs[0]
        tail_24103 = vs[1:]
        _x_24104 = _alt_24099(head_24102, tail_24103)
        return _x_24104

# Lean: Corpus.Geometry.polygonArea.go
def polygon_area_go(vs_319: list[Point2D], first_320: Point2D, prev_321: Point2D, acc_322: float) -> float:
    while True:
        def _f_24119():
            _x_24113 = cross2d(prev_321, first_320)
            _x_24114 = acc_322 + _x_24113
            _x_24115 = 2
            _x_24118 = _x_24114 // 2
            return _x_24118
        _alt_24120 = _f_24119
        if len(vs_319) == 0:
            _x_24130 = _alt_24120()
            return _x_24130
        else:
            head_24131 = vs_319[0]
            tail_24132 = vs_319[1:]
            v_324 = head_24131
            rest_325 = tail_24132
            _x_24124 = cross2d(prev_321, v_324)
            _x_24125 = acc_322 + _x_24124
            vs_319, first_320, prev_321, acc_322 = rest_325, first_320, v_324, _x_24125
            continue

# Lean: Corpus.Geometry.pointInTriangle.sign
def sign(p1: Point2D, p2: Point2D, p3: Point2D) -> float:
    _x_24142 = p1.field_0
    _x_24143 = p3.field_0
    _x_24144 = _x_24142 - _x_24143
    _x_24145 = p2.field_1
    _x_24146 = p3.field_1
    _x_24147 = _x_24145 - _x_24146
    _x_24148 = _x_24144 * _x_24147
    _x_24149 = p2.field_0
    _x_24150 = _x_24149 - _x_24143
    _x_24151 = p1.field_1
    _x_24152 = _x_24151 - _x_24146
    _x_24153 = _x_24150 * _x_24152
    _x_24154 = _x_24148 - _x_24153
    return _x_24154

# Lean: Corpus.NumberTheory.isHarshad.digitSum
def digit_sum(n_326: int) -> int:
    _x_24159 = 0
    _x_24162 = n_326 == 0
    _x_24163 = True
    _x_24164 = _x_24162 == True
    if _x_24164:
        return 0
    else:
        _x_24172 = 10
        _x_24175 = n_326 % 10
        _x_24179 = n_326 // 10
        _x_24180 = digit_sum(_x_24179)
        _x_24181 = _x_24175 + _x_24180
        return _x_24181

# Lean: Corpus.NumberTheory.digitalRoot.digitSum
def digit_sum(n_327: int) -> int:
    _x_24189 = 0
    _x_24192 = n_327 == 0
    _x_24193 = True
    _x_24194 = _x_24192 == True
    if _x_24194:
        return 0
    else:
        _x_24202 = 10
        _x_24205 = n_327 % 10
        _x_24209 = n_327 // 10
        _x_24210 = digit_sum(_x_24209)
        _x_24211 = _x_24205 + _x_24210
        return _x_24211

# Lean: Corpus.NumberTheory.isqrt.go
def isqrt_go(n_328: int, x_329: int, fuel: int) -> int:
    while True:
        def _f_24216():
            return x_329
        _alt_24217 = _f_24216
        if fuel == 0:
            _x_24238 = _alt_24217()
            return _x_24238
        else:
            n_24239 = fuel - 1
            fuel_ = n_24239
            _x_24224 = n_328 // x_329
            _x_24225 = x_329 + _x_24224
            _x_24226 = 2
            _x_24229 = _x_24225 // 2
            _x_24230 = x_329 <= _x_24229
            if _x_24230:
                return x_329
            else:
                n_328, x_329, fuel = n_328, _x_24229, fuel_
                continue

# Lean: Corpus.NumberTheory.totient.gcd
def totient_gcd(a_332: int, b_333: int) -> int:
    while True:
        _x_24246 = 0
        _x_24249 = b_333 == 0
        _x_24250 = True
        _x_24251 = _x_24249 == True
        if _x_24251:
            return a_332
        else:
            _x_24256 = a_332 % b_333
            a_332, b_333 = b_333, _x_24256
            continue

# Lean: Corpus.NumberTheory.totient.count
def count(n_334: int, i_335: int, acc_336: int) -> int:
    while True:
        _x_24264 = i_335 == n_334
        _x_24265 = True
        _x_24266 = _x_24264 == True
        if _x_24266:
            return acc_336
        else:
            _x_24268 = totient_gcd(i_335, n_334)
            _x_24269 = 1
            _x_24272 = _x_24268 == 1
            _x_24273 = _x_24272 == True
            if _x_24273:
                _x_24284 = i_335 + 1
                _x_24285 = acc_336 + 1
                n_334, i_335, acc_336 = n_334, _x_24284, _x_24285
                continue
            else:
                _x_24278 = i_335 + 1
                n_334, i_335, acc_336 = n_334, _x_24278, acc_336
                continue

# Lean: Corpus.Advanced.Graph.topoSort.loop
def topo_sort_loop(g: Graph, queue: list[int], in_deg: list[int], result: list[int], fuel_337: int) -> list[int] | None:
    while True:
        def _f_24292():
            _x_24291 = None
            return _x_24291
        _alt_24293 = _f_24292
        if fuel_337 == 0:
            _x_24392 = _alt_24293()
            return _x_24392
        else:
            n_24393 = fuel_337 - 1
            fuel__339 = n_24393
            def _f_24308():
                _x_24297 = len(result)
                _x_24298 = g.field_0
                _x_24299 = _x_24297 == _x_24298
                _x_24300 = True
                _x_24301 = _x_24299 == True
                if _x_24301:
                    _x_24305 = list(reversed(result))
                    _x_24306 = _x_24305
                    return _x_24306
                else:
                    _x_24303 = None
                    return _x_24303
            _alt_24309 = _f_24308
            if len(queue) == 0:
                _x_24384 = _alt_24309()
                return _x_24384
            else:
                head_24385 = queue[0]
                tail_24386 = queue[1:]
                v_341 = head_24385
                rest_342 = tail_24386
                _x_24310 = [v_341] + result
                _x_24318 = g.field_1
                _x_24319 = [x_24311 for x_24311 in _x_24318 if (x_24311[0] == v_341)]
                def _f_24374(x_24323: tuple[list[int], list[int]], x_24324: tuple[int, int]):
                    def _f_24368(deg: list[int], q_343: list[int]):
                        def _f_24362(fst_24325: int, w_344: int):
                            def _f_24349(d_345: int):
                                _x_24329 = 1
                                _x_24332 = d_345 - 1
                                _x_24333 = set_tr(None, deg, w_344, _x_24332)
                                _x_24337 = 0
                                _x_24340 = _x_24332 == 0
                                _x_24341 = True
                                _x_24342 = _x_24340 == True
                                if _x_24342:
                                    _x_24346 = [w_344] + q_343
                                    _x_24347 = (_x_24333, _x_24346)
                                    return _x_24347
                                else:
                                    _x_24344 = (_x_24333, q_343)
                                    return _x_24344
                            _alt_24350 = _f_24349
                            def _f_24352():
                                _x_24351 = (deg, q_343)
                                return _x_24351
                            _alt_24353 = _f_24352
                            _x_24355 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                            _x_24356 = _x_24355(deg, w_344)
                            if _x_24356 is None:
                                _x_24358 = _alt_24353()
                                return _x_24358
                            else:
                                val_24359 = _x_24356
                                _x_24360 = _alt_24350(val_24359)
                                return _x_24360
                        _alt_24363 = _f_24362
                        match x_24324:
                            case (fst_24364, snd_24365):
                                _x_24366 = _alt_24363(fst_24364, snd_24365)
                                return _x_24366
                    _alt_24369 = _f_24368
                    match x_24323:
                        case (fst_24370, snd_24371):
                            _x_24372 = _alt_24369(fst_24370, snd_24371)
                            return _x_24372
                _x_24375 = (in_deg, rest_342)
                _x_24376 = functools.reduce(_f_24374, _x_24319, _x_24375)
                match _x_24376:
                    case (fst_24377, snd_24378):
                        new_in_deg = fst_24377
                        new_queue = snd_24378
                        g, queue, in_deg, result, fuel_337 = g, new_queue, new_in_deg, _x_24310, fuel__339
                        continue

# Lean: Corpus.Advanced.Graph.dfs.loop
def dfs_loop(g_347: Graph, stack: list[int], visited: list[int], fuel_348: int) -> list[int]:
    while True:
        def _f_24398():
            _x_24397 = list(reversed(visited))
            return _x_24397
        _alt_24399 = _f_24398
        if fuel_348 == 0:
            _x_24433 = _alt_24399()
            return _x_24433
        else:
            n_24434 = fuel_348 - 1
            fuel__350 = n_24434
            _alt_24400 = _f_24398
            if len(stack) == 0:
                _x_24425 = _alt_24400()
                return _x_24425
            else:
                head_24426 = stack[0]
                tail_24427 = stack[1:]
                v_351 = head_24426
                rest_352 = tail_24427
                _x_24403 = v_351 in visited
                _x_24404 = True
                _x_24405 = _x_24403 == True
                if _x_24405:
                    g_347, stack, visited, fuel_348 = g_347, rest_352, visited, fuel__350
                    continue
                else:
                    _x_24407 = [v_351] + visited
                    def _f_24411(x_24408: int):
                        _x_24409 = x_24408 in _x_24407
                        _x_24410 = not _x_24409
                        return _x_24410
                    _x_24412 = advanced_graph_neighbors(g_347, v_351)
                    _x_24413 = [x for x in _x_24412 if _f_24411(x)]
                    _x_24417 = _x_24413 + rest_352
                    g_347, stack, visited, fuel_348 = g_347, _x_24417, _x_24407, fuel__350
                    continue

# Lean: Corpus.Advanced.Graph.bfs.loop
def bfs_loop(g_353: Graph, queue_354: list[int], visited_355: list[int], fuel_356: int) -> list[int]:
    while True:
        def _f_24439():
            _x_24438 = list(reversed(visited_355))
            return _x_24438
        _alt_24440 = _f_24439
        if fuel_356 == 0:
            _x_24474 = _alt_24440()
            return _x_24474
        else:
            n_24475 = fuel_356 - 1
            fuel__358 = n_24475
            _alt_24441 = _f_24439
            if len(queue_354) == 0:
                _x_24466 = _alt_24441()
                return _x_24466
            else:
                head_24467 = queue_354[0]
                tail_24468 = queue_354[1:]
                v_359 = head_24467
                rest_360 = tail_24468
                _x_24444 = v_359 in visited_355
                _x_24445 = True
                _x_24446 = _x_24444 == True
                if _x_24446:
                    g_353, queue_354, visited_355, fuel_356 = g_353, rest_360, visited_355, fuel__358
                    continue
                else:
                    _x_24448 = [v_359] + visited_355
                    def _f_24452(x_24449: int):
                        _x_24450 = x_24449 in _x_24448
                        _x_24451 = not _x_24450
                        return _x_24451
                    _x_24453 = advanced_graph_neighbors(g_353, v_359)
                    _x_24454 = [x for x in _x_24453 if _f_24452(x)]
                    _x_24458 = rest_360 + _x_24454
                    g_353, queue_354, visited_355, fuel_356 = g_353, _x_24458, _x_24448, fuel__358
                    continue

# Lean: Corpus.Advanced.heapSort.extract
def extract(__363: Any, inst_24479: Any, h: Any, acc_364: list[Any], fuel_365: int) -> list[Any]:
    while True:
        def _f_24481():
            _x_24480 = list(reversed(acc_364))
            return _x_24480
        _alt_24482 = _f_24481
        if fuel_365 == 0:
            _x_24498 = _alt_24482()
            return _x_24498
        else:
            n_24499 = fuel_365 - 1
            fuel__367 = n_24499
            _alt_24483 = _f_24481
            _x_24489 = advanced_heap_min(None, h)
            if _x_24489 is None:
                _x_24491 = _alt_24483()
                return _x_24491
            else:
                val_24492 = _x_24489
                x_368 = val_24492
                _x_24484 = pop_min(None, inst_24479, h)
                _x_24485 = [x_368] + acc_364
                return extract(None, inst_24479, _x_24484, _x_24485, fuel__367)

# Lean: Corpus.DataStructures.Trie.hasPrefix.go
def has_prefix_go(t_369: Trie, chars: list[str]) -> bool:
    while True:
        def _f_24505(x_24503: Trie):
            _x_24504 = True
            return True
        _alt_24506 = _f_24505
        if len(chars) == 0:
            _x_24539 = _alt_24506(t_369)
            return _x_24539
        else:
            head_24540 = chars[0]
            tail_24541 = chars[1:]
            match t_369:
                case Trie_node(a_24542, a_24543):
                    a_24507 = a_24542
                    children = a_24543
                    c_370 = head_24540
                    cs = tail_24541
                    def _f_24513():
                        _x_24512 = False
                        return False
                    _alt_24514 = _f_24513
                    def _f_24527(x_24515: tuple[str, Trie]):
                        def _f_24521(ch: str, snd_24516: Trie):
                            _x_24520 = ch == c_370
                            return _x_24520
                        _alt_24522 = _f_24521
                        match x_24515:
                            case (fst_24523, snd_24524):
                                _x_24525 = _alt_24522(fst_24523, snd_24524)
                                return _x_24525
                    _x_24528 = next((x for x in children if _f_24527(x)), None)
                    if _x_24528 is None:
                        _x_24530 = _alt_24514()
                        return _x_24530
                    else:
                        val_24531 = _x_24528
                        match val_24531:
                            case (fst_24532, snd_24533):
                                fst_24508 = fst_24532
                                child = snd_24533
                                t_369, chars = child, cs
                                continue

# Lean: Corpus.DataStructures.Trie.contains.go
def trie_contains_go(t_372: Trie, chars_373: list[str]) -> bool:
    while True:
        def _f_24549(is_end: bool, a_24548: list[tuple[str, Trie]]):
            return is_end
        _alt_24550 = _f_24549
        match t_372:
            case Trie_node(a_24583, a_24584):
                if len(chars_373) == 0:
                    _x_24585 = _alt_24550(a_24583, a_24584)
                    return _x_24585
                else:
                    head_24586 = chars_373[0]
                    tail_24587 = chars_373[1:]
                    a_24551 = a_24583
                    children_374 = a_24584
                    c_375 = head_24586
                    cs_376 = tail_24587
                    def _f_24557():
                        _x_24556 = False
                        return False
                    _alt_24558 = _f_24557
                    def _f_24571(x_24559: tuple[str, Trie]):
                        def _f_24565(ch_378: str, snd_24560: Trie):
                            _x_24564 = ch_378 == c_375
                            return _x_24564
                        _alt_24566 = _f_24565
                        match x_24559:
                            case (fst_24567, snd_24568):
                                _x_24569 = _alt_24566(fst_24567, snd_24568)
                                return _x_24569
                    _x_24572 = next((x for x in children_374 if _f_24571(x)), None)
                    if _x_24572 is None:
                        _x_24574 = _alt_24558()
                        return _x_24574
                    else:
                        val_24575 = _x_24572
                        match val_24575:
                            case (fst_24576, snd_24577):
                                fst_24552 = fst_24576
                                child_379 = snd_24577
                                t_372, chars_373 = child_379, cs_376
                                continue

# Lean: Corpus.DataStructures.Trie.insert.go
def trie_insert_go(t_380: Trie, chars_381: list[str]) -> Trie:
    def _f_24594(is_end_382: bool, children_383: list[tuple[str, Trie]]):
        _x_24592 = True
        _x_24593 = Trie_node(True, children_383)
        return _x_24593
    _alt_24595 = _f_24594
    def _f_24657(is_end_384: bool, children_385: list[tuple[str, Trie]], c_386: str, cs_387: list[str]):
        def _f_24618(fst_24596: str, child_388: Trie):
            def _f_24616(x_24597: tuple[str, Trie]):
                def _f_24610(ch_389: str, t_: Trie):
                    _x_24601 = ch_389 == c_386
                    _x_24602 = True
                    _x_24603 = _x_24601 == True
                    if _x_24603:
                        _x_24607 = trie_insert_go(t_, cs_387)
                        _x_24608 = (ch_389, _x_24607)
                        return _x_24608
                    else:
                        _x_24605 = (ch_389, t_)
                        return _x_24605
                _alt_24611 = _f_24610
                match x_24597:
                    case (fst_24612, snd_24613):
                        _x_24614 = _alt_24611(fst_24612, snd_24613)
                        return _x_24614
            _x_24617 = [_f_24616(x) for x in children_385]
            return _x_24617
        _alt_24619 = _f_24618
        def _f_24624():
            _x_24620 = trie_empty()
            _x_24621 = trie_insert_go(_x_24620, cs_387)
            _x_24622 = (c_386, _x_24621)
            _x_24623 = [_x_24622] + children_385
            return _x_24623
        _alt_24625 = _f_24624
        def _f_24638(x_24626: tuple[str, Trie]):
            def _f_24632(ch_391: str, snd_24627: Trie):
                _x_24631 = ch_391 == c_386
                return _x_24631
            _alt_24633 = _f_24632
            match x_24626:
                case (fst_24634, snd_24635):
                    _x_24636 = _alt_24633(fst_24634, snd_24635)
                    return _x_24636
        _x_24639 = next((x for x in children_385 if _f_24638(x)), None)
        def _jp_24649(_y_24647: list[tuple[str, Trie]]):
            _x_24648 = Trie_node(is_end_384, _y_24647)
            return _x_24648
        def _jp_24652():
            _x_24651 = _alt_24625()
            return _jp_24649(_x_24651)
        def _jp_24656(_y_24653: str, _y_24654: Trie):
            _x_24655 = _alt_24619(_y_24653, _y_24654)
            return _jp_24649(_x_24655)
        if _x_24639 is None:
            return _jp_24652()
        else:
            val_24642 = _x_24639
            match val_24642:
                case (fst_24643, snd_24644):
                    return _jp_24656(fst_24643, snd_24644)
    _alt_24658 = _f_24657
    match t_380:
        case Trie_node(a_24659, a_24660):
            if len(chars_381) == 0:
                _x_24661 = _alt_24595(a_24659, a_24660)
                return _x_24661
            else:
                head_24662 = chars_381[0]
                tail_24663 = chars_381[1:]
                _x_24664 = _alt_24658(a_24659, a_24660, head_24662, tail_24663)
                return _x_24664

# Lean: Corpus.DataStructures.BinaryTree.levelOrder.go
def level_order_go(__392: Any, queue_393: list[Any], acc_394: list[Any], fuel_395: int) -> list[Any]:
    while True:
        def _f_24669():
            _x_24668 = list(reversed(acc_394))
            return _x_24668
        _alt_24670 = _f_24669
        if fuel_395 == 0:
            _x_24700 = _alt_24670()
            return _x_24700
        else:
            n_24701 = fuel_395 - 1
            fuel__397 = n_24701
            _alt_24671 = _f_24669
            if len(queue_393) == 0:
                _x_24687 = _alt_24671()
                return _x_24687
            else:
                head_24688 = queue_393[0]
                tail_24689 = queue_393[1:]
                match head_24688:
                    case BinaryTree_empty():
                        rest_398 = tail_24689
                        return level_order_go(None, rest_398, acc_394, fuel__397)
                    case BinaryTree_node(a_24691, a_24692, a_24693):
                        v_399 = a_24691
                        l_400 = a_24692
                        r_401 = a_24693
                        rest_402 = tail_24689
                        _x_24678 = []
                        _x_24679 = [r_401] + _x_24678
                        _x_24680 = [l_400] + _x_24679
                        _x_24681 = rest_402 + _x_24680
                        _x_24682 = [v_399] + acc_394
                        return level_order_go(None, _x_24681, _x_24682, fuel__397)

# Lean: Corpus.Games.RPS.ctorIdx
def ctor_idx(x_403: RPS) -> int:
    match x_403:
        case rock():
            _x_24705 = 0
            return _x_24705
        case paper():
            _x_24706 = 1
            return _x_24706
        case scissors():
            _x_24707 = 2
            return _x_24707

# Lean: Corpus.Games.instBEqRPS.beq
def beq(x_24710: RPS, y_24711: RPS) -> bool:
    _x_24715 = ctor_idx(x_24710)
    _x_24716 = ctor_idx(y_24711)
    _x_24717 = _x_24715 == _x_24716
    return _x_24717

# Lean: Corpus.Games.instBEqRPS
def inst_beq_rps() -> Any:
    _x_24720 = BEq_mk(_x_24719)
    return _x_24720

# Lean: Corpus.Games.rollDice.go
def roll_dice_go(sides: int, n_404: int, seed: int, acc_405: list[int]) -> tuple[list[int], int]:
    while True:
        def _f_24723():
            _x_24721 = list(reversed(acc_405))
            _x_24722 = (_x_24721, seed)
            return _x_24722
        _alt_24724 = _f_24723
        if n_404 == 0:
            _x_24764 = _alt_24724()
            return _x_24764
        else:
            n_24765 = n_404 - 1
            n_ = n_24765
            _x_24734 = 1103515245
            _x_24737 = seed * 1103515245
            _x_24738 = 12345
            _x_24741 = _x_24737 + 12345
            _x_24746 = 2
            _x_24749 = 31
            _x_24752 = 2 ** 31
            _x_24753 = _x_24741 % _x_24752
            _x_24754 = _x_24753 % sides
            _x_24755 = 1
            _x_24758 = _x_24754 + 1
            _x_24759 = [_x_24758] + acc_405
            sides, n_404, seed, acc_405 = sides, n_, _x_24753, _x_24759
            continue

# Lean: Corpus.Games.BlackjackHand.bestValue.adjust
def best_value_adjust(value_407: int, aces: int) -> int:
    while True:
        def _f_24769():
            return value_407
        _alt_24770 = _f_24769
        if aces == 0:
            _x_24789 = _alt_24770()
            return _x_24789
        else:
            n_24790 = aces - 1
            aces_ = n_24790
            _x_24771 = 21
            _x_24774 = value_407 <= 21
            if _x_24774:
                return value_407
            else:
                _x_24779 = 10
                _x_24782 = value_407 - 10
                value_407, aces = _x_24782, aces_
                continue

# Lean: Corpus.Games.Rank.ctorIdx
def ctor_idx(x_409: Rank) -> int:
    match x_409:
        case ace():
            _x_24794 = 0
            return _x_24794
        case two():
            _x_24795 = 1
            return _x_24795
        case three():
            _x_24796 = 2
            return _x_24796
        case four():
            _x_24797 = 3
            return _x_24797
        case five():
            _x_24798 = 4
            return _x_24798
        case six():
            _x_24799 = 5
            return _x_24799
        case seven():
            _x_24800 = 6
            return _x_24800
        case eight():
            _x_24801 = 7
            return _x_24801
        case nine():
            _x_24802 = 8
            return _x_24802
        case ten():
            _x_24803 = 9
            return _x_24803
        case jack():
            _x_24804 = 10
            return _x_24804
        case queen():
            _x_24805 = 11
            return _x_24805
        case king():
            _x_24806 = 12
            return _x_24806

# Lean: Corpus.Games.instBEqRank.beq
def beq(x_24809: Rank, y_24810: Rank) -> bool:
    _x_24814 = ctor_idx(x_24809)
    _x_24815 = ctor_idx(y_24810)
    _x_24816 = _x_24814 == _x_24815
    return _x_24816

# Lean: Corpus.Games.instBEqRank
def inst_beq_rank() -> Any:
    _x_24819 = BEq_mk(_x_24818)
    return _x_24819

# Lean: Corpus.Games.Player.ctorIdx
def ctor_idx(x_410: Player) -> int:
    match x_410:
        case X():
            _x_24820 = 0
            return _x_24820
        case O():
            _x_24821 = 1
            return _x_24821

# Lean: Corpus.Games.instBEqPlayer.beq
def beq(x_24824: Player, y_24825: Player) -> bool:
    _x_24829 = ctor_idx(x_24824)
    _x_24830 = ctor_idx(y_24825)
    _x_24831 = _x_24829 == _x_24830
    return _x_24831

# Lean: Corpus.Games.instBEqPlayer
def inst_beq_player() -> Any:
    _x_24834 = BEq_mk(_x_24833)
    return _x_24834

# Lean: Corpus.Strings.words.go
def words_go(chars_411: list[str], current: list[str], acc_412: list[str]) -> list[str]:
    while True:
        def _f_24846():
            _x_24835 = len(current) == 0
            _x_24836 = True
            _x_24837 = _x_24835 == True
            if _x_24837:
                _x_24844 = list(reversed(acc_412))
                return _x_24844
            else:
                _x_24839 = list(reversed(current))
                _x_24840 = ''.join(_x_24839)
                _x_24841 = [_x_24840] + acc_412
                _x_24842 = list(reversed(_x_24841))
                return _x_24842
        _alt_24847 = _f_24846
        if len(chars_411) == 0:
            _x_24876 = _alt_24847()
            return _x_24876
        else:
            head_24877 = chars_411[0]
            tail_24878 = chars_411[1:]
            c_414 = head_24877
            cs_415 = tail_24878
            _x_24851 = 32
            _x_24852 = chr(_x_24851)
            _x_24853 = c_414 == _x_24852
            _x_24854 = True
            _x_24855 = _x_24853 == True
            if _x_24855:
                _x_24860 = len(current) == 0
                _x_24861 = _x_24860 == True
                if _x_24861:
                    _x_24869 = []
                    chars_411, current, acc_412 = cs_415, _x_24869, acc_412
                    continue
                else:
                    _x_24863 = []
                    _x_24864 = list(reversed(current))
                    _x_24865 = ''.join(_x_24864)
                    _x_24866 = [_x_24865] + acc_412
                    chars_411, current, acc_412 = cs_415, _x_24863, _x_24866
                    continue
            else:
                _x_24857 = [c_414] + current
                chars_411, current, acc_412 = cs_415, _x_24857, acc_412
                continue

# Lean: Corpus.Strings.splitOn.go
def split_on_go(sep: str, chars_416: list[str], current_417: list[str], acc_418: list[str]) -> list[str]:
    while True:
        def _f_24886():
            _x_24882 = list(reversed(current_417))
            _x_24883 = ''.join(_x_24882)
            _x_24884 = [_x_24883] + acc_418
            _x_24885 = list(reversed(_x_24884))
            return _x_24885
        _alt_24887 = _f_24886
        if len(chars_416) == 0:
            _x_24919 = _alt_24887()
            return _x_24919
        else:
            _x_24923 = (lambda h_24920: _uniq_71773(chars_416))(None)
            return _x_24923

# Lean: Corpus.Strings.count.go
def count_go(sub: str, chars_420: list[str], cnt: int) -> int:
    while True:
        def _f_24926():
            return cnt
        _alt_24927 = _f_24926
        if len(chars_420) == 0:
            _x_24949 = _alt_24927()
            return _x_24949
        else:
            head_24950 = chars_420[0]
            tail_24951 = chars_420[1:]
            c_422 = head_24950
            cs_423 = tail_24951
            _x_24928 = [c_422] + cs_423
            _x_24929 = ''.join(_x_24928)
            _x_24931 = starts_with(None, _x_24929, sub, _x_24930)
            _x_24932 = True
            _x_24933 = _x_24931 == True
            if _x_24933:
                _x_24940 = 1
                _x_24943 = cnt + 1
                sub, chars_420, cnt = sub, cs_423, _x_24943
                continue
            else:
                sub, chars_420, cnt = sub, cs_423, cnt
                continue

# Lean: Corpus.Strings.indexOf.go
def index_of_go(sub_424: str, chars_425: list[str], idx_426: int) -> int | None:
    while True:
        def _f_24970():
            _x_24958 = len(sub_424)
            _x_24959 = 0
            _x_24962 = _x_24958 == 0
            _x_24963 = True
            _x_24964 = _x_24962 == True
            if _x_24964:
                _x_24968 = idx_426
                return _x_24968
            else:
                _x_24966 = None
                return _x_24966
        _alt_24971 = _f_24970
        if len(chars_425) == 0:
            _x_24993 = _alt_24971()
            return _x_24993
        else:
            head_24994 = chars_425[0]
            tail_24995 = chars_425[1:]
            c_428 = head_24994
            cs_429 = tail_24995
            _x_24972 = [c_428] + cs_429
            _x_24973 = ''.join(_x_24972)
            _x_24975 = starts_with(None, _x_24973, sub_424, _x_24974)
            _x_24976 = True
            _x_24977 = _x_24975 == True
            if _x_24977:
                _x_24988 = idx_426
                return _x_24988
            else:
                _x_24982 = 1
                _x_24985 = idx_426 + 1
                sub_424, chars_425, idx_426 = sub_424, cs_429, _x_24985
                continue

# Lean: Corpus.Strings.contains.go
def strings_contains_go(sub_430: str, chars_431: list[str]) -> bool:
    while True:
        def _f_25007():
            _x_25002 = len(sub_430)
            _x_25003 = 0
            _x_25006 = _x_25002 == 0
            return _x_25006
        _alt_25008 = _f_25007
        if len(chars_431) == 0:
            _x_25023 = _alt_25008()
            return _x_25023
        else:
            head_25024 = chars_431[0]
            tail_25025 = chars_431[1:]
            c_433 = head_25024
            cs_434 = tail_25025
            _x_25009 = [c_433] + cs_434
            _x_25010 = ''.join(_x_25009)
            _x_25012 = starts_with(None, _x_25010, sub_430, _x_25011)
            _x_25013 = True
            _x_25014 = _x_25012 == True
            if _x_25014:
                _x_25018 = True
                return True
            else:
                sub_430, chars_431 = sub_430, cs_434
                continue

# Lean: Corpus.Strings.replicate.go
def strings_replicate_go(s_435: str, n_436: int, acc_437: str) -> str:
    while True:
        def _f_25029():
            return acc_437
        _alt_25030 = _f_25029
        if n_436 == 0:
            _x_25039 = _alt_25030()
            return _x_25039
        else:
            n_25040 = n_436 - 1
            n__439 = n_25040
            _x_25034 = acc_437 + s_435
            s_435, n_436, acc_437 = s_435, n__439, _x_25034
            continue

# Lean: Corpus.Math.digitalRoot.go
def digital_root_go(n_440: int, fuel_441: int) -> int:
    while True:
        def _f_25044():
            return n_440
        _alt_25045 = _f_25044
        if fuel_441 == 0:
            _x_25058 = _alt_25045()
            return _x_25058
        else:
            n_25059 = fuel_441 - 1
            fuel__443 = n_25059
            _x_25046 = 10
            _x_25049 = digit_sum(n_440, 10)
            _x_25050 = _x_25049 < 10
            if _x_25050:
                return _x_25049
            else:
                n_440, fuel_441 = _x_25049, fuel__443
                continue

# Lean: Corpus.Math.digits.go
def digits_go(base: int, n_445: int, acc_446: list[int]) -> list[int]:
    while True:
        _x_25066 = 0
        _x_25069 = n_445 == 0
        _x_25070 = True
        _x_25071 = _x_25069 == True
        if _x_25071:
            _x_25084 = len(acc_446) == 0
            _x_25085 = _x_25084 == True
            if _x_25085:
                _x_25088 = []
                _x_25089 = [0] + _x_25088
                return _x_25089
            else:
                return acc_446
        else:
            _x_25076 = n_445 // base
            _x_25080 = n_445 % base
            _x_25081 = [_x_25080] + acc_446
            base, n_445, acc_446 = base, _x_25076, _x_25081
            continue

# Lean: Corpus.Math.isqrt.go
def isqrt_go(n_447: int, x_448: int, fuel_449: int) -> int:
    while True:
        def _f_25093():
            return x_448
        _alt_25094 = _f_25093
        if fuel_449 == 0:
            _x_25115 = _alt_25094()
            return _x_25115
        else:
            n_25116 = fuel_449 - 1
            fuel__451 = n_25116
            _x_25101 = n_447 // x_448
            _x_25102 = x_448 + _x_25101
            _x_25103 = 2
            _x_25106 = _x_25102 // 2
            _x_25107 = x_448 <= _x_25106
            if _x_25107:
                return x_448
            else:
                n_447, x_448, fuel_449 = n_447, _x_25106, fuel__451
                continue

# Lean: Corpus.Math.binomial.go
def binomial_go(n_452: int, k_453: int, num: int, den: int, i_454: int) -> int:
    while True:
        _x_25120 = k_453 < i_454
        if _x_25120:
            _x_25144 = num // den
            return _x_25144
        else:
            _x_25131 = n_452 - i_454
            _x_25132 = 1
            _x_25135 = _x_25131 + 1
            _x_25136 = num * _x_25135
            _x_25137 = den * i_454
            _x_25138 = i_454 + 1
            n_452, k_453, num, den, i_454 = n_452, k_453, _x_25136, _x_25137, _x_25138
            continue

# Lean: Corpus.Math.tribonacci.go
def tribonacci_go(a_455: int, b_456: int, c_457: int, k_458: int) -> int:
    while True:
        def _f_25147():
            return a_455
        _alt_25148 = _f_25147
        if k_458 == 0:
            _x_25158 = _alt_25148()
            return _x_25158
        else:
            n_25159 = k_458 - 1
            k__460 = n_25159
            _x_25152 = a_455 + b_456
            _x_25153 = _x_25152 + c_457
            a_455, b_456, c_457, k_458 = b_456, c_457, _x_25153, k__460
            continue

# Lean: Corpus.Math.lucas.go
def lucas_go(a_461: int, b_462: int, k_463: int) -> int:
    while True:
        def _f_25163():
            return a_461
        _alt_25164 = _f_25163
        if k_463 == 0:
            _x_25173 = _alt_25164()
            return _x_25173
        else:
            n_25174 = k_463 - 1
            k__465 = n_25174
            _x_25168 = a_461 + b_462
            a_461, b_462, k_463 = b_462, _x_25168, k__465
            continue

# Lean: Corpus.Math.fibonacci.go
def math_fibonacci_go(a_466: int, b_467: int, k_468: int) -> int:
    while True:
        def _f_25178():
            return a_466
        _alt_25179 = _f_25178
        if k_468 == 0:
            _x_25188 = _alt_25179()
            return _x_25188
        else:
            n_25189 = k_468 - 1
            k__470 = n_25189
            _x_25183 = a_466 + b_467
            a_466, b_467, k_468 = b_467, _x_25183, k__470
            continue

# Lean: Corpus.Math.divisors.go
def divisors_go(n_471: int, d_472: int, acc_473: list[int]) -> list[int]:
    while True:
        _x_25196 = d_472 * d_472
        _x_25197 = n_471 < _x_25196
        if _x_25197:
            return acc_473
        else:
            _x_25205 = n_471 % d_472
            _x_25206 = 0
            _x_25209 = _x_25205 == 0
            _x_25210 = True
            _x_25211 = _x_25209 == True
            if _x_25211:
                _x_25222 = _x_25196 == n_471
                _x_25223 = _x_25222 == True
                if _x_25223:
                    _x_25243 = 1
                    _x_25246 = d_472 + 1
                    _x_25247 = [d_472] + acc_473
                    n_471, d_472, acc_473 = n_471, _x_25246, _x_25247
                    continue
                else:
                    _x_25228 = 1
                    _x_25231 = d_472 + 1
                    _x_25235 = n_471 // d_472
                    _x_25236 = [_x_25235] + acc_473
                    _x_25237 = [d_472] + _x_25236
                    n_471, d_472, acc_473 = n_471, _x_25231, _x_25237
                    continue
            else:
                _x_25216 = 1
                _x_25219 = d_472 + 1
                n_471, d_472, acc_473 = n_471, _x_25219, acc_473
                continue

# Lean: Corpus.Math.primeFactors.go
def math_prime_factors_go(n_474: int, d_475: int, acc_476: list[int], fuel_477: int) -> list[int]:
    while True:
        def _f_25255():
            _x_25254 = list(reversed(acc_476))
            return _x_25254
        _alt_25256 = _f_25255
        if fuel_477 == 0:
            _x_25305 = _alt_25256()
            return _x_25305
        else:
            n_25306 = fuel_477 - 1
            fuel__479 = n_25306
            _x_25257 = 1
            _x_25260 = n_474 <= 1
            if _x_25260:
                _x_25300 = list(reversed(acc_476))
                return _x_25300
            else:
                _x_25265 = d_475 * d_475
                _x_25266 = n_474 < _x_25265
                if _x_25266:
                    _x_25296 = [n_474] + acc_476
                    _x_25297 = list(reversed(_x_25296))
                    return _x_25297
                else:
                    _x_25274 = n_474 % d_475
                    _x_25275 = 0
                    _x_25278 = _x_25274 == 0
                    _x_25279 = True
                    _x_25280 = _x_25278 == True
                    if _x_25280:
                        _x_25291 = n_474 // d_475
                        _x_25292 = [d_475] + acc_476
                        n_474, d_475, acc_476, fuel_477 = _x_25291, d_475, _x_25292, fuel__479
                        continue
                    else:
                        _x_25285 = d_475 + 1
                        n_474, d_475, acc_476, fuel_477 = n_474, _x_25285, acc_476, fuel__479
                        continue

# Lean: Corpus.Math.isPrime.check
def math_is_prime_check(n_480: int, d_481: int, fuel_482: int) -> bool:
    while True:
        def _f_25311():
            _x_25310 = True
            return True
        _alt_25312 = _f_25311
        if fuel_482 == 0:
            _x_25350 = _alt_25312()
            return _x_25350
        else:
            n_25351 = fuel_482 - 1
            fuel__484 = n_25351
            _x_25316 = d_481 * d_481
            _x_25317 = n_480 < _x_25316
            if _x_25317:
                _x_25345 = True
                return True
            else:
                _x_25325 = n_480 % d_481
                _x_25326 = 0
                _x_25329 = _x_25325 == 0
                _x_25330 = True
                _x_25331 = _x_25329 == True
                if _x_25331:
                    _x_25342 = False
                    return False
                else:
                    _x_25336 = 1
                    _x_25339 = d_481 + 1
                    n_480, d_481, fuel_482 = n_480, _x_25339, fuel__484
                    continue

# Lean: Corpus.Math.modPow.go
def mod_pow_go(m_485: int, b_486: int, e_487: int, acc_488: int) -> int:
    while True:
        def _f_25359():
            _x_25358 = acc_488 % m_485
            return _x_25358
        _alt_25360 = _f_25359
        _x_25405 = 0
        _x_25408 = e_487 == 0
        if _x_25408:
            _x_25411 = _alt_25360()
            return _x_25411
        else:
            x_25361 = e_487
            _x_25368 = 2
            _x_25371 = e_487 % 2
            _x_25372 = 0
            _x_25375 = _x_25371 == 0
            _x_25376 = True
            _x_25377 = _x_25375 == True
            if _x_25377:
                _x_25395 = b_486 * b_486
                _x_25396 = _x_25395 % m_485
                _x_25400 = e_487 // 2
                m_485, b_486, e_487, acc_488 = m_485, _x_25396, _x_25400, acc_488
                continue
            else:
                _x_25382 = b_486 * b_486
                _x_25383 = _x_25382 % m_485
                _x_25387 = e_487 // 2
                _x_25388 = acc_488 * b_486
                _x_25389 = _x_25388 % m_485
                m_485, b_486, e_487, acc_488 = m_485, _x_25383, _x_25387, _x_25389
                continue

# Lean: Corpus.Math.fastPow.go
def fast_pow_go(b_490: int, e_491: int, acc_492: int) -> int:
    while True:
        def _f_25415():
            return acc_492
        _alt_25416 = _f_25415
        _x_25458 = 0
        _x_25461 = e_491 == 0
        if _x_25461:
            _x_25464 = _alt_25416()
            return _x_25464
        else:
            x_25417 = e_491
            _x_25424 = 2
            _x_25427 = e_491 % 2
            _x_25428 = 0
            _x_25431 = _x_25427 == 0
            _x_25432 = True
            _x_25433 = _x_25431 == True
            if _x_25433:
                _x_25449 = b_490 * b_490
                _x_25453 = e_491 // 2
                b_490, e_491, acc_492 = _x_25449, _x_25453, acc_492
                continue
            else:
                _x_25438 = b_490 * b_490
                _x_25442 = e_491 // 2
                _x_25443 = acc_492 * b_490
                b_490, e_491, acc_492 = _x_25438, _x_25442, _x_25443
                continue

# Lean: Corpus.Algorithms.reverse.go
def algorithms_reverse_go(__494: Any, xs_495: list[Any], acc_496: list[Any]) -> list[Any]:
    while True:
        def _f_25468():
            return acc_496
        _alt_25469 = _f_25468
        if len(xs_495) == 0:
            _x_25475 = _alt_25469()
            return _x_25475
        else:
            head_25476 = xs_495[0]
            tail_25477 = xs_495[1:]
            x_498 = head_25476
            xs__499 = tail_25477
            _x_25470 = [x_498] + acc_496
            return algorithms_reverse_go(None, xs__499, _x_25470)

# Lean: Corpus.Algorithms.power.go
def power_go(b_500: int, e_501: int, acc_502: int) -> int:
    while True:
        def _f_25481():
            return acc_502
        _alt_25482 = _f_25481
        _x_25524 = 0
        _x_25527 = e_501 == 0
        if _x_25527:
            _x_25530 = _alt_25482()
            return _x_25530
        else:
            x_25483 = e_501
            _x_25490 = 2
            _x_25493 = e_501 % 2
            _x_25494 = 0
            _x_25497 = _x_25493 == 0
            _x_25498 = True
            _x_25499 = _x_25497 == True
            if _x_25499:
                _x_25515 = b_500 * b_500
                _x_25519 = e_501 // 2
                b_500, e_501, acc_502 = _x_25515, _x_25519, acc_502
                continue
            else:
                _x_25504 = b_500 * b_500
                _x_25508 = e_501 // 2
                _x_25509 = acc_502 * b_500
                b_500, e_501, acc_502 = _x_25504, _x_25508, _x_25509
                continue

# Lean: Corpus.Algorithms.fibonacci.go
def algorithms_fibonacci_go(a_504: int, b_505: int, k_506: int) -> int:
    while True:
        def _f_25534():
            return a_504
        _alt_25535 = _f_25534
        if k_506 == 0:
            _x_25544 = _alt_25535()
            return _x_25544
        else:
            n_25545 = k_506 - 1
            k__508 = n_25545
            _x_25539 = a_504 + b_505
            a_504, b_505, k_506 = b_505, _x_25539, k__508
            continue

# Lean: Corpus.Algorithms.primeFactors.go
def algorithms_prime_factors_go(n_509: int, d_510: int, acc_511: list[int], fuel_512: int) -> list[int]:
    while True:
        def _f_25550():
            _x_25549 = list(reversed(acc_511))
            return _x_25549
        _alt_25551 = _f_25550
        if fuel_512 == 0:
            _x_25600 = _alt_25551()
            return _x_25600
        else:
            n_25601 = fuel_512 - 1
            fuel__514 = n_25601
            _x_25552 = 1
            _x_25555 = n_509 <= 1
            if _x_25555:
                _x_25595 = list(reversed(acc_511))
                return _x_25595
            else:
                _x_25560 = d_510 * d_510
                _x_25561 = n_509 < _x_25560
                if _x_25561:
                    _x_25591 = [n_509] + acc_511
                    _x_25592 = list(reversed(_x_25591))
                    return _x_25592
                else:
                    _x_25569 = n_509 % d_510
                    _x_25570 = 0
                    _x_25573 = _x_25569 == 0
                    _x_25574 = True
                    _x_25575 = _x_25573 == True
                    if _x_25575:
                        _x_25586 = n_509 // d_510
                        _x_25587 = [d_510] + acc_511
                        n_509, d_510, acc_511, fuel_512 = _x_25586, d_510, _x_25587, fuel__514
                        continue
                    else:
                        _x_25580 = d_510 + 1
                        n_509, d_510, acc_511, fuel_512 = n_509, _x_25580, acc_511, fuel__514
                        continue

# Lean: Corpus.Algorithms.isPrime.check
def algorithms_is_prime_check(n_515: int, d_516: int, fuel_517: int) -> bool:
    while True:
        def _f_25606():
            _x_25605 = True
            return True
        _alt_25607 = _f_25606
        if fuel_517 == 0:
            _x_25645 = _alt_25607()
            return _x_25645
        else:
            n_25646 = fuel_517 - 1
            fuel__519 = n_25646
            _x_25611 = d_516 * d_516
            _x_25612 = n_515 < _x_25611
            if _x_25612:
                _x_25640 = True
                return True
            else:
                _x_25620 = n_515 % d_516
                _x_25621 = 0
                _x_25624 = _x_25620 == 0
                _x_25625 = True
                _x_25626 = _x_25624 == True
                if _x_25626:
                    _x_25637 = False
                    return False
                else:
                    _x_25631 = 1
                    _x_25634 = d_516 + 1
                    n_515, d_516, fuel_517 = n_515, _x_25634, fuel__519
                    continue

# Lean: Corpus.Algorithms.binarySearch.go
def binary_search_go(arr_520: list[int], target: int, lo: int, hi_521: int, fuel_522: int) -> int | None:
    while True:
        def _f_25651():
            _x_25650 = None
            return _x_25650
        _alt_25652 = _f_25651
        if fuel_522 == 0:
            _x_25707 = _alt_25652()
            return _x_25707
        else:
            n_25708 = fuel_522 - 1
            fuel__524 = n_25708
            _x_25653 = hi_521 <= lo
            if _x_25653:
                _x_25702 = None
                return _x_25702
            else:
                _x_25664 = hi_521 - lo
                _x_25665 = 2
                _x_25668 = _x_25664 // 2
                _x_25669 = lo + _x_25668
                _alt_25670 = _f_25651
                _x_25694 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                _x_25695 = _x_25694(arr_520, _x_25669)
                if _x_25695 is None:
                    _x_25697 = _alt_25670()
                    return _x_25697
                else:
                    val_25698 = _x_25695
                    v_526 = val_25698
                    _x_25674 = v_526 == target
                    _x_25675 = True
                    _x_25676 = _x_25674 == True
                    if _x_25676:
                        _x_25689 = _x_25669
                        return _x_25689
                    else:
                        _x_25678 = v_526 < target
                        if _x_25678:
                            _x_25682 = 1
                            _x_25685 = _x_25669 + 1
                            arr_520, target, lo, hi_521, fuel_522 = arr_520, target, _x_25685, hi_521, fuel__524
                            continue
                        else:
                            arr_520, target, lo, hi_521, fuel_522 = arr_520, target, lo, _x_25669, fuel__524
                            continue

# Lean: Corpus.Algorithms.linearSearch.go
def linear_search_go(target_527: int, xs_528: list[int], idx_529: int) -> int | None:
    while True:
        def _f_25713():
            _x_25712 = None
            return _x_25712
        _alt_25714 = _f_25713
        if len(xs_528) == 0:
            _x_25736 = _alt_25714()
            return _x_25736
        else:
            head_25737 = xs_528[0]
            tail_25738 = xs_528[1:]
            x_531 = head_25737
            xs__532 = tail_25738
            _x_25718 = x_531 == target_527
            _x_25719 = True
            _x_25720 = _x_25718 == True
            if _x_25720:
                _x_25731 = idx_529
                return _x_25731
            else:
                _x_25725 = 1
                _x_25728 = idx_529 + 1
                target_527, xs_528, idx_529 = target_527, xs__532, _x_25728
                continue

# Lean: Corpus.Algorithms.insertionSort.insert
def insertion_sort_insert(x_533: int, sorted_534: list[int]) -> list[int]:
    def _f_25744():
        _x_25742 = []
        _x_25743 = [x_533] + _x_25742
        return _x_25743
    _alt_25745 = _f_25744
    def _f_25754(y_536: int, ys_537: list[int]):
        _x_25746 = x_533 <= y_536
        if _x_25746:
            _x_25751 = [y_536] + ys_537
            _x_25752 = [x_533] + _x_25751
            return _x_25752
        else:
            _x_25748 = insertion_sort_insert(x_533, ys_537)
            _x_25749 = [y_536] + _x_25748
            return _x_25749
    _alt_25755 = _f_25754
    if len(sorted_534) == 0:
        _x_25757 = _alt_25745()
        return _x_25757
    else:
        head_25758 = sorted_534[0]
        tail_25759 = sorted_534[1:]
        _x_25760 = _alt_25755(head_25758, tail_25759)
        return _x_25760

# Lean: Corpus.Algorithms.insertionSort.sort
def insertion_sort_sort(unsorted: list[int], acc_538: list[int]) -> list[int]:
    while True:
        def _f_25763():
            return acc_538
        _alt_25764 = _f_25763
        if len(unsorted) == 0:
            _x_25770 = _alt_25764()
            return _x_25770
        else:
            head_25771 = unsorted[0]
            tail_25772 = unsorted[1:]
            x_540 = head_25771
            xs_541 = tail_25772
            _x_25765 = insertion_sort_insert(x_540, acc_538)
            unsorted, acc_538 = xs_541, _x_25765
            continue

# Lean: Corpus.Algorithms.insertionSort
def insertion_sort(xs_542: list[int]) -> list[int]:
    _x_25776 = []
    _x_25777 = insertion_sort_sort(xs_542, _x_25776)
    return _x_25777

# Lean: Corpus.Algorithms.merge
def algorithms_merge(xs_543: list[int], ys_544: list[int]) -> list[int]:
    _alt_25780 = (lambda ys_545: ys_545)
    _alt_25781 = (lambda ys_545: ys_545)
    def _f_25792(x_546: int, xs__547: list[int], y_548: int, ys__549: list[int]):
        _x_25782 = x_546 <= y_548
        if _x_25782:
            _x_25788 = [y_548] + ys__549
            _x_25789 = algorithms_merge(xs__547, _x_25788)
            _x_25790 = [x_546] + _x_25789
            return _x_25790
        else:
            _x_25784 = [x_546] + xs__547
            _x_25785 = algorithms_merge(_x_25784, ys__549)
            _x_25786 = [y_548] + _x_25785
            return _x_25786
    _alt_25793 = _f_25792
    if len(xs_543) == 0:
        _x_25794 = _alt_25780(ys_544)
        return _x_25794
    else:
        head_25795 = xs_543[0]
        tail_25796 = xs_543[1:]
        if len(ys_544) == 0:
            _x_25797 = [head_25795] + tail_25796
            _x_25798 = _alt_25781(_x_25797)
            return _x_25798
        else:
            head_25799 = ys_544[0]
            tail_25800 = ys_544[1:]
            _x_25801 = _alt_25793(head_25795, tail_25796, head_25799, tail_25800)
            return _x_25801

# Lean: Corpus.Algorithms.split
def algorithms_split(xs_550: list[int]) -> tuple[list[int], list[int]]:
    def _f_25807():
        _x_25805 = []
        _x_25806 = (_x_25805, _x_25805)
        return _x_25806
    _alt_25808 = _f_25807
    def _f_25812(x_552: int):
        _x_25809 = []
        _x_25810 = [x_552] + _x_25809
        _x_25811 = (_x_25810, _x_25809)
        return _x_25811
    _alt_25813 = _f_25812
    def _f_25824(x_553: int, y_554: int, rest_555: list[int]):
        def _f_25817(l_556: list[int], r_557: list[int]):
            _x_25814 = [x_553] + l_556
            _x_25815 = [y_554] + r_557
            _x_25816 = (_x_25814, _x_25815)
            return _x_25816
        _alt_25818 = _f_25817
        _x_25819 = algorithms_split(rest_555)
        match _x_25819:
            case (fst_25820, snd_25821):
                _x_25822 = _alt_25818(fst_25820, snd_25821)
                return _x_25822
    _alt_25825 = _f_25824
    if len(xs_550) == 0:
        _x_25827 = _alt_25808()
        return _x_25827
    else:
        head_25828 = xs_550[0]
        tail_25829 = xs_550[1:]
        if len(tail_25829) == 0:
            _x_25830 = _alt_25813(head_25828)
            return _x_25830
        else:
            head_25831 = tail_25829[0]
            tail_25832 = tail_25829[1:]
            _x_25833 = _alt_25825(head_25828, head_25831, tail_25832)
            return _x_25833

# Lean: Corpus.Algorithms.mergeSort
def merge_sort(xs_558: list[int]) -> list[int]:
    def _f_25838():
        _x_25837 = []
        return _x_25837
    _alt_25839 = _f_25838
    def _f_25842(x_560: int):
        _x_25840 = []
        _x_25841 = [x_560] + _x_25840
        return _x_25841
    _alt_25843 = _f_25842
    def _f_25855(x_25844: list[int]):
        def _f_25848(l_561: list[int], r_562: list[int]):
            _x_25845 = merge_sort(l_561)
            _x_25846 = merge_sort(r_562)
            _x_25847 = algorithms_merge(_x_25845, _x_25846)
            return _x_25847
        _alt_25849 = _f_25848
        _x_25850 = algorithms_split(xs_558)
        match _x_25850:
            case (fst_25851, snd_25852):
                _x_25853 = _alt_25849(fst_25851, snd_25852)
                return _x_25853
    _alt_25856 = _f_25855
    if len(xs_558) == 0:
        _x_25858 = _alt_25839()
        return _x_25858
    else:
        head_25859 = xs_558[0]
        tail_25860 = xs_558[1:]
        if len(tail_25860) == 0:
            _x_25861 = _alt_25843(head_25859)
            return _x_25861
        else:
            def _f_25865(h_25862: Any):
                _x_25863 = [head_25859] + tail_25860
                _x_25864 = _alt_25856(_x_25863)
                return _x_25864
            _x_25866 = _f_25865(None)
            return _x_25866

# Lean: Corpus.Algorithms.linearSearch
def linear_search(xs_563: list[int], target_564: int) -> int | None:
    _x_25870 = 0
    _x_25873 = linear_search_go(target_564, xs_563, 0)
    return _x_25873

# Lean: Corpus.Algorithms.binarySearch
def binary_search(arr_565: list[int], target_566: int) -> int | None:
    _x_25875 = 0
    _x_25878 = len(arr_565)
    _x_25879 = binary_search_go(arr_565, target_566, 0, _x_25878, _x_25878)
    return _x_25879

# Lean: Corpus.Algorithms.gcd
def algorithms_gcd(a_567: int, b_568: int) -> int:
    while True:
        _x_25884 = 0
        _x_25887 = b_568 == 0
        _x_25888 = True
        _x_25889 = _x_25887 == True
        if _x_25889:
            return a_567
        else:
            _x_25894 = a_567 % b_568
            a_567, b_568 = b_568, _x_25894
            continue

# Lean: Corpus.Algorithms.lcm
def algorithms_lcm(a_569: int, b_570: int) -> int:
    def _f_25900():
        _x_25899 = True
        return True
    _alt_25901 = _f_25900
    def _f_25909():
        _x_25905 = 0
        _x_25908 = b_570 == 0
        return _x_25908
    _alt_25910 = _f_25909
    _x_25914 = 0
    _x_25917 = a_569 == 0
    def _jp_25938(_y_25922: bool):
        _x_25923 = True
        _x_25924 = _y_25922 == True
        if _x_25924:
            return 0
        else:
            _x_25932 = algorithms_gcd(a_569, b_570)
            _x_25933 = a_569 // _x_25932
            _x_25934 = _x_25933 * b_570
            return _x_25934
    def _jp_25941():
        _x_25940 = _alt_25910()
        return _jp_25938(_x_25940)
    def _jp_25944():
        _x_25943 = _alt_25901()
        return _jp_25938(_x_25943)
    if _x_25917:
        return _jp_25944()
    else:
        return _jp_25941()

# Lean: Corpus.Algorithms.isPrime
def algorithms_is_prime(n_573: int) -> bool:
    _x_25946 = 2
    _x_25949 = n_573 < 2
    if _x_25949:
        _x_25953 = False
        return False
    else:
        _x_25951 = algorithms_is_prime_check(n_573, 2, n_573)
        return _x_25951

# Lean: Corpus.Algorithms.primeFactors
def algorithms_prime_factors(n_574: int) -> list[int]:
    _x_25956 = 2
    _x_25959 = []
    _x_25960 = algorithms_prime_factors_go(n_574, 2, _x_25959, n_574)
    return _x_25960

# Lean: Corpus.Algorithms.fibonacci
def algorithms_fibonacci(n_575: int) -> int:
    _x_25962 = 0
    _x_25965 = 1
    _x_25968 = algorithms_fibonacci_go(0, 1, n_575)
    return _x_25968

# Lean: Corpus.Algorithms.power
def power(base_576: int, exp_577: int) -> int:
    _x_25970 = 1
    _x_25973 = power_go(base_576, exp_577, 1)
    return _x_25973

# Lean: Corpus.Algorithms.reverse
def algorithms_reverse(__578: Any, xs_579: list[Any]) -> list[Any]:
    _x_25975 = []
    _x_25976 = algorithms_reverse_go(None, xs_579, _x_25975)
    return _x_25976

# Lean: Corpus.Algorithms.take
def algorithms_take(__580: Any, n_581: int, xs_582: list[Any]) -> list[Any]:
    def _f_25980(x_25978: list[Any]):
        _x_25979 = []
        return _x_25979
    _alt_25981 = _f_25980
    def _f_25984(x_25982: int):
        _x_25983 = []
        return _x_25983
    _alt_25985 = _f_25984
    def _f_25988(n__583: int, x_584: Any, xs__585: list[Any]):
        _x_25986 = algorithms_take(None, n__583, xs__585)
        _x_25987 = [x_584] + _x_25986
        return _x_25987
    _alt_25989 = _f_25988
    if n_581 == 0:
        _x_25990 = _alt_25981(xs_582)
        return _x_25990
    else:
        n_25991 = n_581 - 1
        if len(xs_582) == 0:
            _x_25992 = n_25991 + 1
            _x_25993 = _alt_25985(_x_25992)
            return _x_25993
        else:
            head_25994 = xs_582[0]
            tail_25995 = xs_582[1:]
            _x_25996 = _alt_25989(n_25991, head_25994, tail_25995)
            return _x_25996

# Lean: Corpus.Algorithms.drop
def algorithms_drop(__586: Any, n_587: int, xs_588: list[Any]) -> list[Any]:
    while True:
        _alt_26001 = (lambda xs_589: xs_589)
        def _f_26004(x_26002: int):
            _x_26003 = []
            return _x_26003
        _alt_26005 = _f_26004
        if n_587 == 0:
            _x_26010 = _alt_26001(xs_588)
            return _x_26010
        else:
            n_26011 = n_587 - 1
            if len(xs_588) == 0:
                _x_26012 = n_26011 + 1
                _x_26013 = _alt_26005(_x_26012)
                return _x_26013
            else:
                head_26014 = xs_588[0]
                tail_26015 = xs_588[1:]
                n__590 = n_26011
                head_26006 = head_26014
                xs__591 = tail_26015
                return algorithms_drop(None, n__590, xs__591)

# Lean: Corpus.Algorithms.filter
def algorithms_filter(__592: Any, p_593: Callable[[Any], bool], xs_594: list[Any]) -> list[Any]:
    def _f_26021():
        _x_26020 = []
        return _x_26020
    _alt_26022 = _f_26021
    def _f_26032(x_596: Any, xs__597: list[Any]):
        _x_26023 = p_593(x_596)
        _x_26024 = True
        _x_26025 = _x_26023 == True
        if _x_26025:
            _x_26029 = algorithms_filter(None, p_593, xs__597)
            _x_26030 = [x_596] + _x_26029
            return _x_26030
        else:
            _x_26027 = algorithms_filter(None, p_593, xs__597)
            return _x_26027
    _alt_26033 = _f_26032
    if len(xs_594) == 0:
        _x_26035 = _alt_26022()
        return _x_26035
    else:
        head_26036 = xs_594[0]
        tail_26037 = xs_594[1:]
        _x_26038 = _alt_26033(head_26036, tail_26037)
        return _x_26038

# Lean: Corpus.Algorithms.map
def algorithms_map(__598: Any, __599: Any, f: Callable[[Any], Any], xs_600: list[Any]) -> list[Any]:
    def _f_26042():
        _x_26041 = []
        return _x_26041
    _alt_26043 = _f_26042
    def _f_26047(x_602: Any, xs__603: list[Any]):
        _x_26044 = f(x_602)
        _x_26045 = algorithms_map(None, None, f, xs__603)
        _x_26046 = [_x_26044] + _x_26045
        return _x_26046
    _alt_26048 = _f_26047
    if len(xs_600) == 0:
        _x_26050 = _alt_26043()
        return _x_26050
    else:
        head_26051 = xs_600[0]
        tail_26052 = xs_600[1:]
        _x_26053 = _alt_26048(head_26051, tail_26052)
        return _x_26053

# Lean: Corpus.Algorithms.foldl
def algorithms_foldl(__604: Any, __605: Any, f_606: Callable[[Any, Any], Any], init: Any, xs_607: list[Any]) -> Any:
    while True:
        def _f_26056():
            return init
        _alt_26057 = _f_26056
        if len(xs_607) == 0:
            _x_26063 = _alt_26057()
            return _x_26063
        else:
            head_26064 = xs_607[0]
            tail_26065 = xs_607[1:]
            x_609 = head_26064
            xs__610 = tail_26065
            _x_26058 = f_606(init, x_609)
            return algorithms_foldl(None, None, f_606, _x_26058, xs__610)

# Lean: Corpus.Algorithms.foldr
def algorithms_foldr(__611: Any, __612: Any, f_613: Callable[[Any, Any], Any], init_614: Any, xs_615: list[Any]) -> Any:
    def _f_26069():
        return init_614
    _alt_26070 = _f_26069
    def _f_26073(x_617: Any, xs__618: list[Any]):
        _x_26071 = algorithms_foldr(None, None, f_613, init_614, xs__618)
        _x_26072 = f_613(x_617, _x_26071)
        return _x_26072
    _alt_26074 = _f_26073
    if len(xs_615) == 0:
        _x_26076 = _alt_26070()
        return _x_26076
    else:
        head_26077 = xs_615[0]
        tail_26078 = xs_615[1:]
        _x_26079 = _alt_26074(head_26077, tail_26078)
        return _x_26079

# Lean: Corpus.Algorithms.zip
def algorithms_zip(__619: Any, __620: Any, xs_621: list[Any], ys_622: list[Any]) -> list[tuple[Any, Any]]:
    def _f_26084(x_26082: list[Any]):
        _x_26083 = []
        return _x_26083
    _alt_26085 = _f_26084
    def _f_26088(x_26086: list[Any]):
        _x_26087 = []
        return _x_26087
    _alt_26089 = _f_26088
    def _f_26093(x_623: Any, xs__624: list[Any], y_625: Any, ys__626: list[Any]):
        _x_26090 = (x_623, y_625)
        _x_26091 = algorithms_zip(None, None, xs__624, ys__626)
        _x_26092 = [_x_26090] + _x_26091
        return _x_26092
    _alt_26094 = _f_26093
    if len(xs_621) == 0:
        _x_26095 = _alt_26085(ys_622)
        return _x_26095
    else:
        head_26096 = xs_621[0]
        tail_26097 = xs_621[1:]
        if len(ys_622) == 0:
            _x_26098 = [head_26096] + tail_26097
            _x_26099 = _alt_26089(_x_26098)
            return _x_26099
        else:
            head_26100 = ys_622[0]
            tail_26101 = ys_622[1:]
            _x_26102 = _alt_26094(head_26096, tail_26097, head_26100, tail_26101)
            return _x_26102

# Lean: Corpus.Algorithms.unzip
def unzip(__627: Any, __628: Any, xys: list[tuple[Any, Any]]) -> tuple[list[Any], list[Any]]:
    def _f_26109():
        _x_26106 = []
        _x_26107 = []
        _x_26108 = (_x_26106, _x_26107)
        return _x_26108
    _alt_26110 = _f_26109
    def _f_26121(x_630: Any, y_631: Any, rest_632: list[tuple[Any, Any]]):
        def _f_26114(xs_633: list[Any], ys_634: list[Any]):
            _x_26111 = [x_630] + xs_633
            _x_26112 = [y_631] + ys_634
            _x_26113 = (_x_26111, _x_26112)
            return _x_26113
        _alt_26115 = _f_26114
        _x_26116 = unzip(None, None, rest_632)
        match _x_26116:
            case (fst_26117, snd_26118):
                _x_26119 = _alt_26115(fst_26117, snd_26118)
                return _x_26119
    _alt_26122 = _f_26121
    if len(xys) == 0:
        _x_26124 = _alt_26110()
        return _x_26124
    else:
        head_26125 = xys[0]
        tail_26126 = xys[1:]
        match head_26125:
            case (fst_26127, snd_26128):
                _x_26129 = _alt_26122(fst_26127, snd_26128, tail_26126)
                return _x_26129

# Lean: Corpus.Algorithms.concat
def algorithms_concat(__635: Any, xss: list[list[Any]]) -> list[Any]:
    def _f_26134():
        _x_26133 = []
        return _x_26133
    _alt_26135 = _f_26134
    def _f_26141(xs_637: list[Any], xss_: list[list[Any]]):
        _x_26139 = algorithms_concat(None, xss_)
        _x_26140 = xs_637 + _x_26139
        return _x_26140
    _alt_26142 = _f_26141
    if len(xss) == 0:
        _x_26144 = _alt_26135()
        return _x_26144
    else:
        head_26145 = xss[0]
        tail_26146 = xss[1:]
        _x_26147 = _alt_26142(head_26145, tail_26146)
        return _x_26147

# Lean: Corpus.Algorithms.intersperse
def intersperse(__638: Any, sep_639: Any, xs_640: list[Any]) -> list[Any]:
    def _f_26151():
        _x_26150 = []
        return _x_26150
    _alt_26152 = _f_26151
    def _f_26155(x_642: Any):
        _x_26153 = []
        _x_26154 = [x_642] + _x_26153
        return _x_26154
    _alt_26156 = _f_26155
    def _f_26160(x_643: Any, xs__644: list[Any]):
        _x_26157 = intersperse(None, sep_639, xs__644)
        _x_26158 = [sep_639] + _x_26157
        _x_26159 = [x_643] + _x_26158
        return _x_26159
    _alt_26161 = _f_26160
    if len(xs_640) == 0:
        _x_26163 = _alt_26152()
        return _x_26163
    else:
        head_26164 = xs_640[0]
        tail_26165 = xs_640[1:]
        if len(tail_26165) == 0:
            _x_26166 = _alt_26156(head_26164)
            return _x_26166
        else:
            _x_26170 = (lambda h_26167: _alt_26161(head_26164, tail_26165))(None)
            return _x_26170

# Lean: Corpus.Algorithms.span
def span(__645: Any, p_646: Callable[[Any], bool], xs_647: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_26176():
        _x_26174 = []
        _x_26175 = (_x_26174, _x_26174)
        return _x_26175
    _alt_26177 = _f_26176
    def _f_26195(x_649: Any, xs__650: list[Any]):
        _x_26178 = p_646(x_649)
        _x_26179 = True
        _x_26180 = _x_26178 == True
        if _x_26180:
            def _f_26187(ys_651: list[Any], zs: list[Any]):
                _x_26185 = [x_649] + ys_651
                _x_26186 = (_x_26185, zs)
                return _x_26186
            _alt_26188 = _f_26187
            _x_26189 = span(None, p_646, xs__650)
            match _x_26189:
                case (fst_26190, snd_26191):
                    _x_26192 = _alt_26188(fst_26190, snd_26191)
                    return _x_26192
        else:
            _x_26182 = []
            _x_26183 = (_x_26182, xs_647)
            return _x_26183
    _alt_26196 = _f_26195
    if len(xs_647) == 0:
        _x_26198 = _alt_26177()
        return _x_26198
    else:
        head_26199 = xs_647[0]
        tail_26200 = xs_647[1:]
        _x_26201 = _alt_26196(head_26199, tail_26200)
        return _x_26201

# Lean: Corpus.Algorithms.partition
def partition(__652: Any, p_653: Callable[[Any], bool], xs_654: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_26206():
        _x_26204 = []
        _x_26205 = (_x_26204, _x_26204)
        return _x_26205
    _alt_26207 = _f_26206
    def _f_26225(x_656: Any, xs__657: list[Any]):
        def _f_26218(yes: list[Any], no: list[Any]):
            _x_26208 = p_653(x_656)
            _x_26209 = True
            _x_26210 = _x_26208 == True
            if _x_26210:
                _x_26215 = [x_656] + yes
                _x_26216 = (_x_26215, no)
                return _x_26216
            else:
                _x_26212 = [x_656] + no
                _x_26213 = (yes, _x_26212)
                return _x_26213
        _alt_26219 = _f_26218
        _x_26220 = partition(None, p_653, xs__657)
        match _x_26220:
            case (fst_26221, snd_26222):
                _x_26223 = _alt_26219(fst_26221, snd_26222)
                return _x_26223
    _alt_26226 = _f_26225
    if len(xs_654) == 0:
        _x_26228 = _alt_26207()
        return _x_26228
    else:
        head_26229 = xs_654[0]
        tail_26230 = xs_654[1:]
        _x_26231 = _alt_26226(head_26229, tail_26230)
        return _x_26231

# Lean: Corpus.Algorithms.groupBy
def group_by(__658: Any, eq: Callable[[Any, Any], bool], xs_659: list[Any]) -> list[list[Any]]:
    def _f_26235():
        _x_26234 = []
        return _x_26234
    _alt_26236 = _f_26235
    def _f_26248(x_661: Any, xs__662: list[Any]):
        def _f_26240(same: list[Any], rest_663: list[Any]):
            _x_26237 = [x_661] + same
            _x_26238 = group_by(None, eq, rest_663)
            _x_26239 = [_x_26237] + _x_26238
            return _x_26239
        _alt_26241 = _f_26240
        _x_26242 = eq(x_661)
        _x_26243 = span(None, _x_26242, xs__662)
        match _x_26243:
            case (fst_26244, snd_26245):
                _x_26246 = _alt_26241(fst_26244, snd_26245)
                return _x_26246
    _alt_26249 = _f_26248
    if len(xs_659) == 0:
        _x_26251 = _alt_26236()
        return _x_26251
    else:
        head_26252 = xs_659[0]
        tail_26253 = xs_659[1:]
        _x_26254 = _alt_26249(head_26252, tail_26253)
        return _x_26254

# Lean: Corpus.Algorithms.isPalindrome
def algorithms_is_palindrome(s_664: str) -> bool:
    _x_26257 = list(s_664)
    _x_26262 = list(reversed(_x_26257))
    _x_26263 = _x_26257 == _x_26262
    return _x_26263

# Lean: Corpus.Algorithms.countChar
def algorithms_count_char(c_666: str, s_667: str) -> int:
    def _f_26281(acc_668: int, x_669: str):
        _x_26268 = x_669 == c_666
        _x_26269 = True
        _x_26270 = _x_26268 == True
        if _x_26270:
            _x_26276 = 1
            _x_26279 = acc_668 + 1
            return _x_26279
        else:
            return acc_668
    _x_26282 = 0
    _x_26285 = list(s_667)
    _x_26286 = functools.reduce(_f_26281, _x_26285, 0)
    return _x_26286

# Lean: Corpus.Algorithms.replaceChar
def replace_char(old: str, new: str, s_670: str) -> str:
    def _f_26297(c_671: str):
        _x_26291 = c_671 == old
        _x_26292 = True
        _x_26293 = _x_26291 == True
        if _x_26293:
            return new
        else:
            return c_671
    _x_26298 = list(s_670)
    _x_26299 = [_f_26297(x) for x in _x_26298]
    _x_26300 = ''.join(_x_26299)
    return _x_26300

# Lean: Corpus.Math.abs
def math_abs(x_672: int) -> int:
    _x_26302 = 0
    _x_26305 = x_672 < 0
    if _x_26305:
        _x_26310 = -x_672
        return _x_26310
    else:
        return x_672

# Lean: Corpus.Math.sign
def sign(x_673: int) -> int:
    _x_26313 = 0
    _x_26316 = x_673 < 0
    if _x_26316:
        _x_26329 = 1
        _x_26332 = -1
        return _x_26332
    else:
        _x_26318 = 0 < x_673
        if _x_26318:
            _x_26322 = 1
            return 1
        else:
            return 1

# Lean: Corpus.Math.min
def math_min(a_674: int, b_675: int) -> int:
    _x_26335 = a_674 <= b_675
    if _x_26335:
        return a_674
    else:
        return b_675

# Lean: Corpus.Math.max
def math_max(a_676: int, b_677: int) -> int:
    _x_26340 = b_677 <= a_676
    if _x_26340:
        return a_676
    else:
        return b_677

# Lean: Corpus.Math.clamp
def clamp(lo_678: int, hi_679: int, x_680: int) -> int:
    _x_26345 = math_max(lo_678, x_680)
    _x_26346 = math_min(hi_679, _x_26345)
    return _x_26346

# Lean: Corpus.Math.divMod
def div_mod(a_681: int, b_682: int) -> tuple[int, int]:
    _x_26351 = a_681 // b_682
    _x_26355 = a_681 % b_682
    _x_26356 = (_x_26351, _x_26355)
    return _x_26356

# Lean: Corpus.Math.pow
def pow(base_683: int, exp_684: int) -> int:
    def _f_26361():
        _x_26358 = 1
        return 1
    _alt_26362 = _f_26361
    def _f_26368(n_686: int):
        _x_26366 = pow(base_683, n_686)
        _x_26367 = base_683 * _x_26366
        return _x_26367
    _alt_26369 = _f_26368
    if exp_684 == 0:
        _x_26371 = _alt_26362()
        return _x_26371
    else:
        n_26372 = exp_684 - 1
        _x_26373 = _alt_26369(n_26372)
        return _x_26373

# Lean: Corpus.Math.fastPow
def fast_pow(base_687: int, exp_688: int) -> int:
    _x_26376 = 1
    _x_26379 = fast_pow_go(base_687, exp_688, 1)
    return _x_26379

# Lean: Corpus.Math.modPow
def mod_pow(base_689: int, exp_690: int, m_691: int) -> int:
    _x_26384 = base_689 % m_691
    _x_26385 = 1
    _x_26388 = mod_pow_go(m_691, _x_26384, exp_690, 1)
    return _x_26388

# Lean: Corpus.Math.gcd
def math_gcd(a_692: int, b_693: int) -> int:
    while True:
        _x_26393 = 0
        _x_26396 = b_693 == 0
        _x_26397 = True
        _x_26398 = _x_26396 == True
        if _x_26398:
            return a_692
        else:
            _x_26403 = a_692 % b_693
            a_692, b_693 = b_693, _x_26403
            continue

# Lean: Corpus.Math.lcm
def math_lcm(a_694: int, b_695: int) -> int:
    def _f_26409():
        _x_26408 = True
        return True
    _alt_26410 = _f_26409
    def _f_26418():
        _x_26414 = 0
        _x_26417 = b_695 == 0
        return _x_26417
    _alt_26419 = _f_26418
    _x_26423 = 0
    _x_26426 = a_694 == 0
    def _jp_26447(_y_26431: bool):
        _x_26432 = True
        _x_26433 = _y_26431 == True
        if _x_26433:
            return 0
        else:
            _x_26441 = math_gcd(a_694, b_695)
            _x_26442 = a_694 // _x_26441
            _x_26443 = _x_26442 * b_695
            return _x_26443
    def _jp_26450():
        _x_26449 = _alt_26419()
        return _jp_26447(_x_26449)
    def _jp_26453():
        _x_26452 = _alt_26410()
        return _jp_26447(_x_26452)
    if _x_26426:
        return _jp_26453()
    else:
        return _jp_26450()

# Lean: Corpus.Math.coprime
def coprime(a_698: int, b_699: int) -> bool:
    _x_26458 = math_gcd(a_698, b_699)
    _x_26459 = 1
    _x_26462 = _x_26458 == 1
    return _x_26462

# Lean: Corpus.Math.isPrime
def math_is_prime(n_700: int) -> bool:
    _x_26464 = 2
    _x_26467 = n_700 < 2
    if _x_26467:
        _x_26471 = False
        return False
    else:
        _x_26469 = math_is_prime_check(n_700, 2, n_700)
        return _x_26469

# Lean: Corpus.Math.primeFactors
def math_prime_factors(n_701: int) -> list[int]:
    _x_26474 = 2
    _x_26477 = []
    _x_26478 = math_prime_factors_go(n_701, 2, _x_26477, n_701)
    return _x_26478

# Lean: Corpus.Math.divisors
def divisors(n_702: int) -> list[int]:
    _x_26480 = 1
    _x_26483 = []
    _x_26484 = divisors_go(n_702, 1, _x_26483)
    _x_26485 = list(reversed(_x_26484))
    return _x_26485

# Lean: Corpus.Math.numDivisors
def num_divisors(n_703: int) -> int:
    _x_26487 = divisors(n_703)
    _x_26488 = len(_x_26487)
    return _x_26488

# Lean: Corpus.Math.sumDivisors
def sum_divisors(n_704: int) -> int:
    def _f_26496(x1_26490: int, x2_26491: int):
        _x_26495 = x1_26490 + x2_26491
        return _x_26495
    _x_26497 = 0
    _x_26500 = divisors(n_704)
    _x_26501 = functools.reduce(_f_26496, _x_26500, 0)
    return _x_26501

# Lean: Corpus.Math.fibonacci
def math_fibonacci(n_705: int) -> int:
    _x_26503 = 0
    _x_26506 = 1
    _x_26509 = math_fibonacci_go(0, 1, n_705)
    return _x_26509

# Lean: Corpus.Math.lucas
def lucas(n_706: int) -> int:
    _x_26511 = 2
    _x_26514 = 1
    _x_26517 = lucas_go(2, 1, n_706)
    return _x_26517

# Lean: Corpus.Math.tribonacci
def tribonacci(n_707: int) -> int:
    _x_26519 = 0
    _x_26522 = 1
    _x_26525 = tribonacci_go(0, 0, 1, n_707)
    return _x_26525

# Lean: Corpus.Math.factorial
def factorial(n_708: int) -> int:
    def _f_26530():
        _x_26527 = 1
        return 1
    _alt_26531 = _f_26530
    def _f_26544(n__710: int):
        _x_26538 = 1
        _x_26541 = n__710 + 1
        _x_26542 = factorial(n__710)
        _x_26543 = _x_26541 * _x_26542
        return _x_26543
    _alt_26545 = _f_26544
    if n_708 == 0:
        _x_26547 = _alt_26531()
        return _x_26547
    else:
        n_26548 = n_708 - 1
        _x_26549 = _alt_26545(n_26548)
        return _x_26549

# Lean: Corpus.Math.binomial
def binomial(n_711: int, k_712: int) -> int:
    _x_26552 = n_711 < k_712
    if _x_26552:
        _x_26559 = 0
        return 0
    else:
        _x_26554 = 1
        _x_26557 = binomial_go(n_711, k_712, 1, 1, 1)
        return _x_26557

# Lean: Corpus.Math.catalan
def catalan(n_713: int) -> int:
    _x_26570 = 2
    _x_26573 = 2 * n_713
    _x_26574 = binomial(_x_26573, n_713)
    _x_26578 = 1
    _x_26581 = n_713 + 1
    _x_26582 = _x_26574 // _x_26581
    return _x_26582

# Lean: Corpus.Math.permutations
def permutations(n_714: int, k_715: int) -> int:
    _x_26584 = n_714 < k_715
    if _x_26584:
        _x_26597 = 0
        return 0
    else:
        _x_26589 = factorial(n_714)
        _x_26593 = n_714 - k_715
        _x_26594 = factorial(_x_26593)
        _x_26595 = _x_26589 // _x_26594
        return _x_26595

# Lean: Corpus.Math.triangularNumber
def triangular_number(n_716: int) -> int:
    _x_26611 = 1
    _x_26614 = n_716 + 1
    _x_26615 = n_716 * _x_26614
    _x_26616 = 2
    _x_26619 = _x_26615 // 2
    return _x_26619

# Lean: Corpus.Math.squareNumber
def square_number(n_717: int) -> int:
    _x_26624 = n_717 * n_717
    return _x_26624

# Lean: Corpus.Math.pentagonalNumber
def pentagonal_number(n_718: int) -> int:
    _x_26635 = 3
    _x_26638 = 3 * n_718
    _x_26639 = 1
    _x_26642 = _x_26638 - 1
    _x_26643 = n_718 * _x_26642
    _x_26644 = 2
    _x_26647 = _x_26643 // 2
    return _x_26647

# Lean: Corpus.Math.hexagonalNumber
def hexagonal_number(n_719: int) -> int:
    _x_26655 = 2
    _x_26658 = 2 * n_719
    _x_26659 = 1
    _x_26662 = _x_26658 - 1
    _x_26663 = n_719 * _x_26662
    return _x_26663

# Lean: Corpus.Math.isTriangular
def is_triangular(n_720: int) -> bool:
    _x_26677 = 8
    _x_26680 = 8 * n_720
    _x_26681 = 1
    _x_26684 = _x_26680 + 1
    _x_26685 = isqrt(_x_26684)
    _x_26686 = _x_26685 - 1
    _x_26687 = 2
    _x_26690 = _x_26686 // 2
    _x_26694 = _x_26690 + 1
    _x_26695 = _x_26690 * _x_26694
    _x_26696 = _x_26695 // 2
    _x_26697 = _x_26696 == n_720
    return _x_26697

# Lean: Corpus.Math.isSquare
def is_square(n_722: int) -> bool:
    _x_26699 = isqrt(n_722)
    _x_26706 = _x_26699 * _x_26699
    _x_26707 = _x_26706 == n_722
    return _x_26707

# Lean: Corpus.Math.isqrt
def isqrt(n_724: int) -> int:
    _x_26712 = 0
    _x_26715 = n_724 == 0
    _x_26716 = True
    _x_26717 = _x_26715 == True
    if _x_26717:
        return 0
    else:
        _x_26719 = isqrt_go(n_724, n_724, n_724)
        return _x_26719

# Lean: Corpus.Math.digits
def digits(n_725: int, base_726: int) -> list[int]:
    _x_26724 = 2
    _x_26727 = base_726 < 2
    if _x_26727:
        _x_26732 = []
        return _x_26732
    else:
        _x_26729 = []
        _x_26730 = digits_go(base_726, n_725, _x_26729)
        return _x_26730

# Lean: Corpus.Math.fromDigits
def from_digits(ds: list[int], base_727: int) -> int:
    def _f_26743(acc_728: int, d_729: int):
        _x_26741 = acc_728 * base_727
        _x_26742 = _x_26741 + d_729
        return _x_26742
    _x_26744 = 0
    _x_26747 = functools.reduce(_f_26743, ds, 0)
    return _x_26747

# Lean: Corpus.Math.numDigits
def num_digits(n_730: int, base_731: int) -> int:
    _x_26749 = digits(n_730, base_731)
    _x_26750 = len(_x_26749)
    return _x_26750

# Lean: Corpus.Math.numDigits10
def num_digits10(n_732: int) -> int:
    _x_26752 = 10
    _x_26755 = num_digits(n_732, 10)
    return _x_26755

# Lean: Corpus.Math.digitSum
def digit_sum(n_733: int, base_734: int) -> int:
    def _f_26763(x1_26757: int, x2_26758: int):
        _x_26762 = x1_26757 + x2_26758
        return _x_26762
    _x_26764 = 0
    _x_26767 = digits(n_733, base_734)
    _x_26768 = functools.reduce(_f_26763, _x_26767, 0)
    return _x_26768

# Lean: Corpus.Math.digitSum10
def digit_sum10(n_735: int) -> int:
    _x_26770 = 10
    _x_26773 = digit_sum(n_735, 10)
    return _x_26773

# Lean: Corpus.Math.digitalRoot
def digital_root(n_736: int) -> int:
    _x_26775 = 100
    _x_26778 = digital_root_go(n_736, 100)
    return _x_26778

# Lean: Corpus.Math.reverseDigits
def reverse_digits(n_737: int) -> int:
    _x_26780 = 10
    _x_26783 = digits(n_737, 10)
    _x_26784 = list(reversed(_x_26783))
    _x_26785 = from_digits(_x_26784, 10)
    return _x_26785

# Lean: Corpus.Math.isPalindromeNum
def is_palindrome_num(n_738: int) -> bool:
    _x_26790 = reverse_digits(n_738)
    _x_26791 = n_738 == _x_26790
    return _x_26791

# Lean: Corpus.Math.isEven
def is_even(n_739: int) -> bool:
    _x_26799 = 2
    _x_26802 = n_739 % 2
    _x_26803 = 0
    _x_26806 = _x_26802 == 0
    return _x_26806

# Lean: Corpus.Math.isOdd
def is_odd(n_740: int) -> bool:
    _x_26814 = 2
    _x_26817 = n_740 % 2
    _x_26818 = 1
    _x_26821 = _x_26817 == 1
    return _x_26821

# Lean: Corpus.Functional.id
def functional_id(__741: Any, x_742: Any) -> Any:
    return x_742

# Lean: Corpus.Functional.const
def functional_const(__743: Any, __744: Any, x_745: Any, y_746: Any) -> Any:
    return x_745

# Lean: Corpus.Functional.flip
def functional_flip(__747: Any, __748: Any, __749: Any, f_750: Callable[[Any, Any], Any], y_751: Any, x_752: Any) -> Any:
    _x_26825 = f_750(x_752, y_751)
    return _x_26825

# Lean: Corpus.Functional.compose
def functional_compose(__753: Any, __754: Any, __755: Any, f_756: Callable[[Any], Any], g_757: Callable[[Any], Any], x_758: Any) -> Any:
    _x_26827 = g_757(x_758)
    _x_26828 = f_756(_x_26827)
    return _x_26828

# Lean: Corpus.Functional.pipe
def pipe(__759: Any, __760: Any, x_761: Any, f_762: Callable[[Any], Any]) -> Any:
    _x_26830 = f_762(x_761)
    return _x_26830

# Lean: Corpus.Functional.apply
def functional_apply(__763: Any, __764: Any, f_765: Callable[[Any], Any], x_766: Any) -> Any:
    _x_26832 = f_765(x_766)
    return _x_26832

# Lean: Corpus.Functional.curry
def curry(__767: Any, __768: Any, __769: Any, f_770: Callable[[tuple[Any, Any]], Any], x_771: Any, y_772: Any) -> Any:
    _x_26834 = (x_771, y_772)
    _x_26835 = f_770(_x_26834)
    return _x_26835

# Lean: Corpus.Functional.uncurry
def uncurry(__773: Any, __774: Any, __775: Any, f_776: Callable[[Any, Any], Any], p_777: tuple[Any, Any]) -> Any:
    _x_26837 = p_777[0]
    _x_26838 = p_777[1]
    _x_26839 = f_776(_x_26837, _x_26838)
    return _x_26839

# Lean: Corpus.Functional.Option.map
def option_map(__778: Any, __779: Any, f_780: Callable[[Any], Any], x_26841: Any | None) -> Any | None:
    def _f_26843():
        _x_26842 = None
        return _x_26842
    _alt_26844 = _f_26843
    def _f_26847(x_782: Any):
        _x_26845 = f_780(x_782)
        _x_26846 = _x_26845
        return _x_26846
    _alt_26848 = _f_26847
    if x_26841 is None:
        _x_26850 = _alt_26844()
        return _x_26850
    else:
        val_26851 = x_26841
        _x_26852 = _alt_26848(val_26851)
        return _x_26852

# Lean: Corpus.Functional.Option.bind
def option_bind(__783: Any, __784: Any, x_785: Any | None, f_786: Callable[[Any], Any | None]) -> Any | None:
    def _f_26856():
        _x_26855 = None
        return _x_26855
    _alt_26857 = _f_26856
    _alt_26860 = (lambda a_788: f_786(a_788))
    if x_785 is None:
        _x_26862 = _alt_26857()
        return _x_26862
    else:
        val_26863 = x_785
        _x_26864 = _alt_26860(val_26863)
        return _x_26864

# Lean: Corpus.Functional.Option.filter
def option_filter(__789: Any, p_790: Callable[[Any], bool], x_26867: Any | None) -> Any | None:
    def _f_26869():
        _x_26868 = None
        return _x_26868
    _alt_26870 = _f_26869
    def _f_26879(x_792: Any):
        _x_26871 = p_790(x_792)
        _x_26872 = True
        _x_26873 = _x_26871 == True
        if _x_26873:
            _x_26877 = x_792
            return _x_26877
        else:
            _x_26875 = None
            return _x_26875
    _alt_26880 = _f_26879
    if x_26867 is None:
        _x_26882 = _alt_26870()
        return _x_26882
    else:
        val_26883 = x_26867
        _x_26884 = _alt_26880(val_26883)
        return _x_26884

# Lean: Corpus.Functional.Option.getOrElse
def get_or_else(__793: Any, x_794: Any | None, default: Any) -> Any:
    def _f_26887():
        return default
    _alt_26888 = _f_26887
    _alt_26890 = (lambda a_796: a_796)
    if x_794 is None:
        _x_26892 = _alt_26888()
        return _x_26892
    else:
        val_26893 = x_794
        _x_26894 = _alt_26890(val_26893)
        return _x_26894

# Lean: Corpus.Functional.Option.orElse
def or_else(__797: Any, x_798: Any | None, y_799: Any | None) -> Any | None:
    def _f_26898(a_800: Any):
        _x_26897 = a_800
        return _x_26897
    _alt_26899 = _f_26898
    def _f_26900():
        return y_799
    _alt_26901 = _f_26900
    if x_798 is None:
        _x_26903 = _alt_26901()
        return _x_26903
    else:
        val_26904 = x_798
        _x_26905 = _alt_26899(val_26904)
        return _x_26905

# Lean: Corpus.Functional.Option.zip
def option_zip(__802: Any, __803: Any, x_804: Any | None, y_805: Any | None) -> tuple[Any, Any] | None:
    def _f_26910(a_806: Any, b_807: Any):
        _x_26908 = (a_806, b_807)
        _x_26909 = _x_26908
        return _x_26909
    _alt_26911 = _f_26910
    def _f_26915(x_26912: Any | None, x_26913: Any | None):
        _x_26914 = None
        return _x_26914
    _alt_26916 = _f_26915
    if x_804 is None:
        _x_26929 = (lambda h_26926: _alt_26916(x_804, y_805))(None)
        return _x_26929
    else:
        val_26917 = x_804
        if y_805 is None:
            def _f_26923(h_26920: Any):
                _x_26921 = val_26917
                _x_26922 = _alt_26916(_x_26921, y_805)
                return _x_26922
            _x_26924 = _f_26923(None)
            return _x_26924
        else:
            val_26918 = y_805
            _x_26919 = _alt_26911(val_26917, val_26918)
            return _x_26919

# Lean: Corpus.Functional.List.head?
def head_(__808: Any, xs_809: list[Any]) -> Any | None:
    def _f_26933():
        _x_26932 = None
        return _x_26932
    _alt_26934 = _f_26933
    def _f_26937(x_811: Any, tail_26935: list[Any]):
        _x_26936 = x_811
        return _x_26936
    _alt_26938 = _f_26937
    if len(xs_809) == 0:
        _x_26940 = _alt_26934()
        return _x_26940
    else:
        head_26941 = xs_809[0]
        tail_26942 = xs_809[1:]
        _x_26943 = _alt_26938(head_26941, tail_26942)
        return _x_26943

# Lean: Corpus.Functional.List.tail?
def tail_(__812: Any, xs_813: list[Any]) -> list[Any] | None:
    def _f_26947():
        _x_26946 = None
        return _x_26946
    _alt_26948 = _f_26947
    def _f_26951(head_26949: Any, xs__815: list[Any]):
        _x_26950 = xs__815
        return _x_26950
    _alt_26952 = _f_26951
    if len(xs_813) == 0:
        _x_26954 = _alt_26948()
        return _x_26954
    else:
        head_26955 = xs_813[0]
        tail_26956 = xs_813[1:]
        _x_26957 = _alt_26952(head_26955, tail_26956)
        return _x_26957

# Lean: Corpus.Functional.List.last?
def last_(__816: Any, xs_817: list[Any]) -> Any | None:
    while True:
        def _f_26961():
            _x_26960 = None
            return _x_26960
        _alt_26962 = _f_26961
        def _f_26964(x_819: Any):
            _x_26963 = x_819
            return _x_26963
        _alt_26965 = _f_26964
        if len(xs_817) == 0:
            _x_26971 = _alt_26962()
            return _x_26971
        else:
            head_26972 = xs_817[0]
            tail_26973 = xs_817[1:]
            if len(tail_26973) == 0:
                _x_26974 = _alt_26965(head_26972)
                return _x_26974
            else:
                _x_26978 = (lambda h_26975: _uniq_78536(head_26972, tail_26973))(None)
                return _x_26978

# Lean: Corpus.Functional.List.nth
def nth(__820: Any, xs_821: list[Any], n_822: int) -> Any | None:
    while True:
        def _f_26984(x_26982: int):
            _x_26983 = None
            return _x_26983
        _alt_26985 = _f_26984
        def _f_26988(x_823: Any, tail_26986: list[Any]):
            _x_26987 = x_823
            return _x_26987
        _alt_26989 = _f_26988
        if len(xs_821) == 0:
            _x_26994 = _alt_26985(n_822)
            return _x_26994
        else:
            head_26995 = xs_821[0]
            tail_26996 = xs_821[1:]
            if n_822 == 0:
                _x_26997 = _alt_26989(head_26995, tail_26996)
                return _x_26997
            else:
                n_26998 = n_822 - 1
                head_26990 = head_26995
                xs__824 = tail_26996
                n__825 = n_26998
                return nth(None, xs__824, n__825)

# Lean: Corpus.Functional.List.updateAt
def update_at(__826: Any, xs_827: list[Any], n_828: int, f_829: Callable[[Any], Any]) -> list[Any]:
    def _f_27005(x_27003: int):
        _x_27004 = []
        return _x_27004
    _alt_27006 = _f_27005
    def _f_27009(x_830: Any, xs__831: list[Any]):
        _x_27007 = f_829(x_830)
        _x_27008 = [_x_27007] + xs__831
        return _x_27008
    _alt_27010 = _f_27009
    def _f_27013(x_832: Any, xs__833: list[Any], n__834: int):
        _x_27011 = update_at(None, xs__833, n__834, f_829)
        _x_27012 = [x_832] + _x_27011
        return _x_27012
    _alt_27014 = _f_27013
    if len(xs_827) == 0:
        _x_27015 = _alt_27006(n_828)
        return _x_27015
    else:
        head_27016 = xs_827[0]
        tail_27017 = xs_827[1:]
        if n_828 == 0:
            _x_27018 = _alt_27010(head_27016, tail_27017)
            return _x_27018
        else:
            n_27019 = n_828 - 1
            _x_27020 = _alt_27014(head_27016, tail_27017, n_27019)
            return _x_27020

# Lean: Corpus.Functional.List.insertAt
def insert_at(__835: Any, xs_836: list[Any], n_837: int, x_838: Any) -> list[Any]:
    def _f_27025(xs_839: list[Any]):
        _x_27024 = [x_838] + xs_839
        return _x_27024
    _alt_27026 = _f_27025
    def _f_27030(x_27027: int):
        _x_27028 = []
        _x_27029 = [x_838] + _x_27028
        return _x_27029
    _alt_27031 = _f_27030
    def _f_27034(y_840: Any, ys_841: list[Any], n__842: int):
        _x_27032 = insert_at(None, ys_841, n__842, x_838)
        _x_27033 = [y_840] + _x_27032
        return _x_27033
    _alt_27035 = _f_27034
    if n_837 == 0:
        _x_27036 = _alt_27026(xs_836)
        return _x_27036
    else:
        n_27037 = n_837 - 1
        if len(xs_836) == 0:
            _x_27038 = n_27037 + 1
            _x_27039 = _alt_27031(_x_27038)
            return _x_27039
        else:
            head_27040 = xs_836[0]
            tail_27041 = xs_836[1:]
            _x_27042 = _alt_27035(head_27040, tail_27041, n_27037)
            return _x_27042

# Lean: Corpus.Functional.List.removeAt
def remove_at(__843: Any, xs_844: list[Any], n_845: int) -> list[Any]:
    def _f_27048(x_27046: int):
        _x_27047 = []
        return _x_27047
    _alt_27049 = _f_27048
    def _f_27051(head_27050: Any, xs__846: list[Any]):
        return xs__846
    _alt_27052 = _f_27051
    def _f_27055(x_847: Any, xs__848: list[Any], n__849: int):
        _x_27053 = remove_at(None, xs__848, n__849)
        _x_27054 = [x_847] + _x_27053
        return _x_27054
    _alt_27056 = _f_27055
    if len(xs_844) == 0:
        _x_27057 = _alt_27049(n_845)
        return _x_27057
    else:
        head_27058 = xs_844[0]
        tail_27059 = xs_844[1:]
        if n_845 == 0:
            _x_27060 = _alt_27052(head_27058, tail_27059)
            return _x_27060
        else:
            n_27061 = n_845 - 1
            _x_27062 = _alt_27056(head_27058, tail_27059, n_27061)
            return _x_27062

# Lean: Corpus.Functional.List.splitAt
def split_at(__850: Any, n_851: int, xs_852: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_27068(xs_853: list[Any]):
        _x_27066 = []
        _x_27067 = (_x_27066, xs_853)
        return _x_27067
    _alt_27069 = _f_27068
    def _f_27073(x_27070: int):
        _x_27071 = []
        _x_27072 = (_x_27071, _x_27071)
        return _x_27072
    _alt_27074 = _f_27073
    def _f_27084(n__854: int, x_855: Any, xs__856: list[Any]):
        def _f_27077(l_857: list[Any], r_858: list[Any]):
            _x_27075 = [x_855] + l_857
            _x_27076 = (_x_27075, r_858)
            return _x_27076
        _alt_27078 = _f_27077
        _x_27079 = split_at(None, n__854, xs__856)
        match _x_27079:
            case (fst_27080, snd_27081):
                _x_27082 = _alt_27078(fst_27080, snd_27081)
                return _x_27082
    _alt_27085 = _f_27084
    if n_851 == 0:
        _x_27086 = _alt_27069(xs_852)
        return _x_27086
    else:
        n_27087 = n_851 - 1
        if len(xs_852) == 0:
            _x_27088 = n_27087 + 1
            _x_27089 = _alt_27074(_x_27088)
            return _x_27089
        else:
            head_27090 = xs_852[0]
            tail_27091 = xs_852[1:]
            _x_27092 = _alt_27085(n_27087, head_27090, tail_27091)
            return _x_27092

# Lean: Corpus.Functional.List.takeWhile
def take_while(__859: Any, p_860: Callable[[Any], bool], xs_861: list[Any]) -> list[Any]:
    def _f_27097():
        _x_27096 = []
        return _x_27096
    _alt_27098 = _f_27097
    def _f_27108(x_863: Any, xs__864: list[Any]):
        _x_27099 = p_860(x_863)
        _x_27100 = True
        _x_27101 = _x_27099 == True
        if _x_27101:
            _x_27105 = take_while(None, p_860, xs__864)
            _x_27106 = [x_863] + _x_27105
            return _x_27106
        else:
            _x_27103 = []
            return _x_27103
    _alt_27109 = _f_27108
    if len(xs_861) == 0:
        _x_27111 = _alt_27098()
        return _x_27111
    else:
        head_27112 = xs_861[0]
        tail_27113 = xs_861[1:]
        _x_27114 = _alt_27109(head_27112, tail_27113)
        return _x_27114

# Lean: Corpus.Functional.List.dropWhile
def drop_while(__865: Any, p_866: Callable[[Any], bool], xs_867: list[Any]) -> list[Any]:
    while True:
        def _f_27118():
            _x_27117 = []
            return _x_27117
        _alt_27119 = _f_27118
        if len(xs_867) == 0:
            _x_27131 = _alt_27119()
            return _x_27131
        else:
            head_27132 = xs_867[0]
            tail_27133 = xs_867[1:]
            x_869 = head_27132
            xs__870 = tail_27133
            _x_27120 = p_866(x_869)
            _x_27121 = True
            _x_27122 = _x_27120 == True
            if _x_27122:
                return drop_while(None, p_866, xs__870)
            else:
                _x_27124 = [x_869] + xs__870
                return _x_27124

# Lean: Corpus.Functional.List.replicate
def list_replicate(__871: Any, n_872: int, x_873: Any) -> list[Any]:
    def _f_27138():
        _x_27137 = []
        return _x_27137
    _alt_27139 = _f_27138
    def _f_27142(n__875: int):
        _x_27140 = list_replicate(None, n__875, x_873)
        _x_27141 = [x_873] + _x_27140
        return _x_27141
    _alt_27143 = _f_27142
    if n_872 == 0:
        _x_27145 = _alt_27139()
        return _x_27145
    else:
        n_27146 = n_872 - 1
        _x_27147 = _alt_27143(n_27146)
        return _x_27147

# Lean: Corpus.Functional.List.scanl
def scanl(__876: Any, __877: Any, f_878: Callable[[Any, Any], Any], init_879: Any, xs_880: list[Any]) -> list[Any]:
    def _f_27151():
        _x_27150 = []
        return _x_27150
    _alt_27152 = _f_27151
    def _f_27155(x_882: Any, xs__883: list[Any]):
        _x_27153 = f_878(init_879, x_882)
        _x_27154 = scanl(None, None, f_878, _x_27153, xs__883)
        return _x_27154
    _alt_27156 = _f_27155
    def _jp_27164(_y_27162: list[Any]):
        _x_27163 = [init_879] + _y_27162
        return _x_27163
    def _jp_27167():
        _x_27166 = _alt_27152()
        return _jp_27164(_x_27166)
    def _jp_27171(_y_27168: Any, _y_27169: list[Any]):
        _x_27170 = _alt_27156(_y_27168, _y_27169)
        return _jp_27164(_x_27170)
    if len(xs_880) == 0:
        return _jp_27167()
    else:
        head_27159 = xs_880[0]
        tail_27160 = xs_880[1:]
        return _jp_27171(head_27159, tail_27160)

# Lean: Corpus.Functional.List.interleave
def interleave(__884: Any, xs_885: list[Any], ys_886: list[Any]) -> list[Any]:
    _alt_27174 = (lambda ys_887: ys_887)
    _alt_27175 = (lambda ys_887: ys_887)
    def _f_27179(x_888: Any, xs__889: list[Any], y_890: Any, ys__891: list[Any]):
        _x_27176 = interleave(None, xs__889, ys__891)
        _x_27177 = [y_890] + _x_27176
        _x_27178 = [x_888] + _x_27177
        return _x_27178
    _alt_27180 = _f_27179
    if len(xs_885) == 0:
        _x_27181 = _alt_27174(ys_886)
        return _x_27181
    else:
        head_27182 = xs_885[0]
        tail_27183 = xs_885[1:]
        if len(ys_886) == 0:
            _x_27184 = [head_27182] + tail_27183
            _x_27185 = _alt_27175(_x_27184)
            return _x_27185
        else:
            head_27186 = ys_886[0]
            tail_27187 = ys_886[1:]
            _x_27188 = _alt_27180(head_27182, tail_27183, head_27186, tail_27187)
            return _x_27188

# Lean: Corpus.Functional.Either.map
def either_map(__892: Any, __893: Any, __894: Any, f_895: Callable[[Any], Any], x_27192: Any) -> Any:
    def _f_27194(a_896: Any):
        _x_27193 = left(a_896)
        return _x_27193
    _alt_27195 = _f_27194
    def _f_27198(b_897: Any):
        _x_27196 = f_895(b_897)
        _x_27197 = right(_x_27196)
        return _x_27197
    _alt_27199 = _f_27198
    match x_27192:
        case left(a_27200):
            _x_27201 = _alt_27195(a_27200)
            return _x_27201
        case right(a_27202):
            _x_27203 = _alt_27199(a_27202)
            return _x_27203

# Lean: Corpus.Functional.Either.mapLeft
def map_left(__898: Any, __899: Any, __900: Any, f_901: Callable[[Any], Any], x_27206: Any) -> Any:
    def _f_27209(a_902: Any):
        _x_27207 = f_901(a_902)
        _x_27208 = left(_x_27207)
        return _x_27208
    _alt_27210 = _f_27209
    def _f_27212(b_903: Any):
        _x_27211 = right(b_903)
        return _x_27211
    _alt_27213 = _f_27212
    match x_27206:
        case left(a_27214):
            _x_27215 = _alt_27210(a_27214)
            return _x_27215
        case right(a_27216):
            _x_27217 = _alt_27213(a_27216)
            return _x_27217

# Lean: Corpus.Functional.Either.bind
def either_bind(__904: Any, __905: Any, __906: Any, x_907: Any, f_908: Callable[[Any], Any]) -> Any:
    def _f_27221(a_909: Any):
        _x_27220 = left(a_909)
        return _x_27220
    _alt_27222 = _f_27221
    _alt_27225 = (lambda b_910: f_908(b_910))
    match x_907:
        case left(a_27226):
            _x_27227 = _alt_27222(a_27226)
            return _x_27227
        case right(a_27228):
            _x_27229 = _alt_27225(a_27228)
            return _x_27229

# Lean: Corpus.Functional.Either.isLeft
def is_left(__911: Any, __912: Any, x_27232: Any) -> bool:
    def _f_27235(a_27233: Any):
        _x_27234 = True
        return True
    _alt_27236 = _f_27235
    def _f_27239(a_27237: Any):
        _x_27238 = False
        return False
    _alt_27240 = _f_27239
    match x_27232:
        case left(a_27241):
            _x_27242 = _alt_27236(a_27241)
            return _x_27242
        case right(a_27243):
            _x_27244 = _alt_27240(a_27243)
            return _x_27244

# Lean: Corpus.Functional.Either.isRight
def is_right(__913: Any, __914: Any, x_27247: Any) -> bool:
    def _f_27250(a_27248: Any):
        _x_27249 = False
        return False
    _alt_27251 = _f_27250
    def _f_27254(a_27252: Any):
        _x_27253 = True
        return True
    _alt_27255 = _f_27254
    match x_27247:
        case left(a_27256):
            _x_27257 = _alt_27251(a_27256)
            return _x_27257
        case right(a_27258):
            _x_27259 = _alt_27255(a_27258)
            return _x_27259

# Lean: Corpus.Strings.isEmpty
def strings_is_empty(s_915: str) -> bool:
    _x_27265 = len(s_915)
    _x_27266 = 0
    _x_27269 = _x_27265 == 0
    return _x_27269

# Lean: Corpus.Strings.isNotEmpty
def is_not_empty(s_916: str) -> bool:
    _x_27271 = 0
    _x_27274 = len(s_916)
    _x_27275 = 0 < _x_27274
    return _x_27275

# Lean: Corpus.Strings.head
def head(s_917: str) -> str | None:
    _x_27278 = list(s_917)
    _x_27279 = (lambda xs: xs[0] if xs else None)(_x_27278)
    return _x_27279

# Lean: Corpus.Strings.tail
def tail(s_918: str) -> str:
    def _f_27282():
        _x_27281 = ""
        return _x_27281
    _alt_27283 = _f_27282
    def _f_27286(head_27284: str, cs_920: list[str]):
        _x_27285 = ''.join(cs_920)
        return _x_27285
    _alt_27287 = _f_27286
    _x_27288 = list(s_918)
    if len(_x_27288) == 0:
        _x_27290 = _alt_27283()
        return _x_27290
    else:
        head_27291 = _x_27288[0]
        tail_27292 = _x_27288[1:]
        _x_27293 = _alt_27287(head_27291, tail_27292)
        return _x_27293

# Lean: Corpus.Strings.last
def last(s_921: str) -> str | None:
    _x_27296 = list(s_921)
    _x_27297 = (lambda xs: xs[-1] if xs else None)(_x_27296)
    return _x_27297

# Lean: Corpus.Strings.init
def init(s_922: str) -> str:
    _x_27299 = list(s_922)
    _x_27300 = drop_last_tr(None, _x_27299)
    _x_27301 = ''.join(_x_27300)
    return _x_27301

# Lean: Corpus.Strings.take
def strings_take(n_923: int, s_924: str) -> str:
    _x_27303 = list(s_924)
    _x_27304 = take_tr(None, n_923, _x_27303)
    _x_27305 = ''.join(_x_27304)
    return _x_27305

# Lean: Corpus.Strings.drop
def strings_drop(n_925: int, s_926: str) -> str:
    _x_27307 = list(s_926)
    _x_27308 = (lambda n, xs: xs[n:])(_x_27307)
    _x_27309 = ''.join(_x_27308)
    return _x_27309

# Lean: Corpus.Strings.charAt
def char_at(s_927: str, i_928: int) -> str | None:
    _x_27312 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_27313 = list(s_927)
    _x_27314 = _x_27312(_x_27313, i_928)
    return _x_27314

# Lean: Corpus.Strings.substring
def substring(s_929: str, start_930: int, len_931: int) -> str:
    _x_27316 = list(s_929)
    _x_27317 = (lambda n, xs: xs[n:])(_x_27316)
    _x_27318 = take_tr(None, len_931, _x_27317)
    _x_27319 = ''.join(_x_27318)
    return _x_27319

# Lean: Corpus.Strings.slice
def slice(s_932: str, start_933: int, stop: int) -> str:
    _x_27324 = stop - start_933
    _x_27325 = substring(s_932, start_933, _x_27324)
    return _x_27325

# Lean: Corpus.Strings.append
def append(s1: str, s2: str) -> str:
    _x_27330 = s1 + s2
    return _x_27330

# Lean: Corpus.Strings.concat
def strings_concat(ss: list[str]) -> str:
    def _f_27338(x1_27332: str, x2_27333: str):
        _x_27337 = x1_27332 + x2_27333
        return _x_27337
    _x_27339 = ""
    _x_27340 = functools.reduce(_f_27338, ss, _x_27339)
    return _x_27340

# Lean: Corpus.Strings.intercalate
def intercalate(sep_934: str, ss_935: list[str]) -> str:
    def _f_27343():
        _x_27342 = ""
        return _x_27342
    _alt_27344 = _f_27343
    _alt_27346 = (lambda s_937: s_937)
    def _f_27353(s_938: str, rest_939: list[str]):
        _x_27350 = s_938 + sep_934
        _x_27351 = intercalate(sep_934, rest_939)
        _x_27352 = _x_27350 + _x_27351
        return _x_27352
    _alt_27354 = _f_27353
    if len(ss_935) == 0:
        _x_27356 = _alt_27344()
        return _x_27356
    else:
        head_27357 = ss_935[0]
        tail_27358 = ss_935[1:]
        if len(tail_27358) == 0:
            _x_27359 = _alt_27346(head_27357)
            return _x_27359
        else:
            _x_27363 = (lambda h_27360: _alt_27354(head_27357, tail_27358))(None)
            return _x_27363

# Lean: Corpus.Strings.join
def join(ss_940: list[str]) -> str:
    _x_27367 = strings_concat(ss_940)
    return _x_27367

# Lean: Corpus.Strings.replicate
def strings_replicate(n_941: int, s_942: str) -> str:
    _x_27369 = ""
    _x_27370 = strings_replicate_go(s_942, n_941, _x_27369)
    return _x_27370

# Lean: Corpus.Strings.reverse
def strings_reverse(s_943: str) -> str:
    _x_27372 = list(s_943)
    _x_27373 = list(reversed(_x_27372))
    _x_27374 = ''.join(_x_27373)
    return _x_27374

# Lean: Corpus.Strings.toUpper
def to_upper(s_944: str) -> str:
    _x_27376 = (lambda c: c.upper())
    _x_27377 = list(s_944)
    _x_27378 = [_x_27376(x) for x in _x_27377]
    _x_27379 = ''.join(_x_27378)
    return _x_27379

# Lean: Corpus.Strings.toLower
def to_lower(s_945: str) -> str:
    _x_27381 = (lambda c: c.lower())
    _x_27382 = list(s_945)
    _x_27383 = [_x_27381(x) for x in _x_27382]
    _x_27384 = ''.join(_x_27383)
    return _x_27384

# Lean: Corpus.Strings.capitalize
def capitalize(s_946: str) -> str:
    def _f_27387():
        _x_27386 = ""
        return _x_27386
    _alt_27388 = _f_27387
    def _f_27392(c_948: str, cs_949: list[str]):
        _x_27389 = (lambda c: c.upper())(c_948)
        _x_27390 = [_x_27389] + cs_949
        _x_27391 = ''.join(_x_27390)
        return _x_27391
    _alt_27393 = _f_27392
    _x_27394 = list(s_946)
    if len(_x_27394) == 0:
        _x_27396 = _alt_27388()
        return _x_27396
    else:
        head_27397 = _x_27394[0]
        tail_27398 = _x_27394[1:]
        _x_27399 = _alt_27393(head_27397, tail_27398)
        return _x_27399

# Lean: Corpus.Strings.swapCase
def swap_case(s_950: str) -> str:
    def _f_27415(c_951: str):
        _x_27402 = (lambda c: c.isupper())(c_951)
        _x_27403 = True
        _x_27404 = _x_27402 == True
        if _x_27404:
            _x_27413 = (lambda c: c.lower())(c_951)
            return _x_27413
        else:
            _x_27406 = (lambda c: c.islower())(c_951)
            _x_27407 = _x_27406 == True
            if _x_27407:
                _x_27410 = (lambda c: c.upper())(c_951)
                return _x_27410
            else:
                return c_951
    _x_27416 = list(s_950)
    _x_27417 = [_f_27415(x) for x in _x_27416]
    _x_27418 = ''.join(_x_27417)
    return _x_27418

# Lean: Corpus.Strings.trimLeft
def trim_left(s_952: str) -> str:
    _x_27428 = list(s_952)
    _x_27429 = drop_while(None, (lambda x_27420: (x_27420 == chr(32))), _x_27428)
    _x_27430 = ''.join(_x_27429)
    return _x_27430

# Lean: Corpus.Strings.trimRight
def trim_right(s_953: str) -> str:
    _x_27440 = list(s_953)
    _x_27441 = list(reversed(_x_27440))
    _x_27442 = drop_while(None, (lambda x_27432: (x_27432 == chr(32))), _x_27441)
    _x_27443 = list(reversed(_x_27442))
    _x_27444 = ''.join(_x_27443)
    return _x_27444

# Lean: Corpus.Strings.trim
def trim(s_954: str) -> str:
    _x_27446 = trim_left(s_954)
    _x_27447 = trim_right(_x_27446)
    return _x_27447

# Lean: Corpus.Strings.padLeft
def pad_left(n_955: int, c_956: str, s_957: str) -> str:
    _x_27449 = len(s_957)
    _x_27450 = n_955 <= _x_27449
    if _x_27450:
        return s_957
    else:
        _x_27458 = n_955 - _x_27449
        _x_27459 = replicate_tr(None, _x_27458, c_956)
        _x_27460 = ''.join(_x_27459)
        _x_27461 = _x_27460 + s_957
        return _x_27461

# Lean: Corpus.Strings.padRight
def pad_right(n_958: int, c_959: str, s_960: str) -> str:
    _x_27465 = len(s_960)
    _x_27466 = n_958 <= _x_27465
    if _x_27466:
        return s_960
    else:
        _x_27474 = n_958 - _x_27465
        _x_27475 = replicate_tr(None, _x_27474, c_959)
        _x_27476 = ''.join(_x_27475)
        _x_27477 = s_960 + _x_27476
        return _x_27477

# Lean: Corpus.Strings.center
def center(n_961: int, c_962: str, s_963: str) -> str:
    _x_27481 = len(s_963)
    _x_27482 = n_961 <= _x_27481
    if _x_27482:
        return s_963
    else:
        _x_27487 = n_961 - _x_27481
        _x_27491 = 2
        _x_27494 = _x_27487 // 2
        _x_27495 = _x_27487 - _x_27494
        _x_27499 = replicate_tr(None, _x_27494, c_962)
        _x_27500 = ''.join(_x_27499)
        _x_27501 = _x_27500 + s_963
        _x_27502 = replicate_tr(None, _x_27495, c_962)
        _x_27503 = ''.join(_x_27502)
        _x_27504 = _x_27501 + _x_27503
        return _x_27504

# Lean: Corpus.Strings.contains
def strings_contains(s_964: str, sub_965: str) -> bool:
    _x_27508 = list(s_964)
    _x_27509 = strings_contains_go(sub_965, _x_27508)
    return _x_27509

# Lean: Corpus.Strings.indexOf
def index_of(s_966: str, sub_967: str) -> int | None:
    _x_27511 = list(s_966)
    _x_27512 = 0
    _x_27515 = index_of_go(sub_967, _x_27511, 0)
    return _x_27515

# Lean: Corpus.Strings.count
def count(s_968: str, sub_969: str) -> int:
    _x_27517 = list(s_968)
    _x_27518 = 0
    _x_27521 = count_go(sub_969, _x_27517, 0)
    return _x_27521

# Lean: Corpus.Strings.countChar
def strings_count_char(c_970: str, s_971: str) -> int:
    def _f_27539(acc_972: int, x_973: str):
        _x_27526 = x_973 == c_970
        _x_27527 = True
        _x_27528 = _x_27526 == True
        if _x_27528:
            _x_27534 = 1
            _x_27537 = acc_972 + 1
            return _x_27537
        else:
            return acc_972
    _x_27540 = 0
    _x_27543 = list(s_971)
    _x_27544 = functools.reduce(_f_27539, _x_27543, 0)
    return _x_27544

# Lean: Corpus.Strings.startsWith
def starts_with(s_974: str, pfx: str) -> bool:
    _x_27550 = len(pfx)
    _x_27551 = list(s_974)
    _x_27552 = take_tr(None, _x_27550, _x_27551)
    _x_27553 = list(pfx)
    _x_27554 = _x_27552 == _x_27553
    return _x_27554

# Lean: Corpus.Strings.endsWith
def ends_with(s_975: str, suffix: str) -> bool:
    _x_27560 = len(suffix)
    _x_27561 = list(s_975)
    _x_27562 = list(reversed(_x_27561))
    _x_27563 = take_tr(None, _x_27560, _x_27562)
    _x_27564 = list(suffix)
    _x_27565 = list(reversed(_x_27564))
    _x_27566 = _x_27563 == _x_27565
    return _x_27566

# Lean: Corpus.Strings.isPalindrome
def strings_is_palindrome(s_976: str) -> bool:
    _x_27568 = (lambda c: c.lower())
    def _f_27581(c_977: str):
        def _f_27570():
            _x_27569 = True
            return True
        _alt_27571 = _f_27570
        def _f_27573():
            _x_27572 = str.isdigit(c_977)
            return _x_27572
        _alt_27574 = _f_27573
        _x_27575 = str.isalpha(c_977)
        if _x_27575:
            _x_27579 = _alt_27571()
            return _x_27579
        else:
            _x_27577 = _alt_27574()
            return _x_27577
    _x_27582 = list(s_976)
    _x_27583 = [x for x in _x_27582 if _f_27581(x)]
    _x_27584 = [_x_27568(x) for x in _x_27583]
    _x_27589 = list(reversed(_x_27584))
    _x_27590 = _x_27584 == _x_27589
    return _x_27590

# Lean: Corpus.Strings.isDigits
def is_digits(s_981: str) -> bool:
    def _f_27593():
        _x_27592 = False
        return False
    _alt_27594 = _f_27593
    def _f_27598():
        _x_27595 = list(s_981)
        _x_27596 = str.isdigit
        _x_27597 = all(_x_27596(x) for x in _x_27595)
        return _x_27597
    _alt_27599 = _f_27598
    _x_27600 = len(s_981) == 0
    _x_27601 = not _x_27600
    if _x_27601:
        _x_27605 = _alt_27599()
        return _x_27605
    else:
        _x_27603 = _alt_27594()
        return _x_27603

# Lean: Corpus.Strings.isAlpha
def is_alpha(s_984: str) -> bool:
    def _f_27609():
        _x_27608 = False
        return False
    _alt_27610 = _f_27609
    def _f_27614():
        _x_27611 = list(s_984)
        _x_27612 = str.isalpha
        _x_27613 = all(_x_27612(x) for x in _x_27611)
        return _x_27613
    _alt_27615 = _f_27614
    _x_27616 = len(s_984) == 0
    _x_27617 = not _x_27616
    if _x_27617:
        _x_27621 = _alt_27615()
        return _x_27621
    else:
        _x_27619 = _alt_27610()
        return _x_27619

# Lean: Corpus.Strings.splitOn
def split_on(s_987: str, sep_988: str) -> list[str]:
    _x_27624 = len(sep_988) == 0
    _x_27625 = True
    _x_27626 = _x_27624 == True
    if _x_27626:
        _x_27633 = []
        _x_27634 = [s_987] + _x_27633
        return _x_27634
    else:
        _x_27628 = list(s_987)
        _x_27629 = []
        _x_27630 = []
        _x_27631 = split_on_go(sep_988, _x_27628, _x_27629, _x_27630)
        return _x_27631

# Lean: Corpus.Strings.lines
def lines(s_989: str) -> list[str]:
    _x_27637 = "\n"
    _x_27638 = split_on(s_989, _x_27637)
    return _x_27638

# Lean: Corpus.Strings.words
def words(s_990: str) -> list[str]:
    _x_27640 = list(s_990)
    _x_27641 = []
    _x_27642 = []
    _x_27643 = words_go(_x_27640, _x_27641, _x_27642)
    return _x_27643

# Lean: Corpus.Strings.unlines
def unlines(ss_991: list[str]) -> str:
    _x_27645 = "\n"
    _x_27646 = intercalate(_x_27645, ss_991)
    return _x_27646

# Lean: Corpus.Strings.unwords
def unwords(ss_992: list[str]) -> str:
    _x_27648 = " "
    _x_27649 = intercalate(_x_27648, ss_992)
    return _x_27649

# Lean: Corpus.Strings.replace
def replace(s_993: str, old_994: str, new_995: str) -> str:
    _x_27651 = split_on(s_993, old_994)
    _x_27652 = intercalate(new_995, _x_27651)
    return _x_27652

# Lean: Corpus.Strings.replaceFirst
def replace_first(s_996: str, old_997: str, new_998: str) -> str:
    def _f_27654():
        return s_996
    _alt_27655 = _f_27654
    def _f_27668(i_1000: int):
        _x_27659 = strings_take(i_1000, s_996)
        _x_27660 = _x_27659 + new_998
        _x_27664 = len(old_997)
        _x_27665 = i_1000 + _x_27664
        _x_27666 = strings_drop(_x_27665, s_996)
        _x_27667 = _x_27660 + _x_27666
        return _x_27667
    _alt_27669 = _f_27668
    _x_27670 = index_of(s_996, old_997)
    if _x_27670 is None:
        _x_27672 = _alt_27655()
        return _x_27672
    else:
        val_27673 = _x_27670
        _x_27674 = _alt_27669(val_27673)
        return _x_27674

# Lean: Corpus.Strings.removePrefix
def remove_prefix(pfx_1001: str, s_1002: str) -> str:
    _x_27677 = starts_with(s_1002, pfx_1001)
    _x_27678 = True
    _x_27679 = _x_27677 == True
    if _x_27679:
        _x_27682 = len(pfx_1001)
        _x_27683 = strings_drop(_x_27682, s_1002)
        return _x_27683
    else:
        return s_1002

# Lean: Corpus.Strings.removeSuffix
def remove_suffix(suffix_1003: str, s_1004: str) -> str:
    _x_27686 = ends_with(s_1004, suffix_1003)
    _x_27687 = True
    _x_27688 = _x_27686 == True
    if _x_27688:
        _x_27694 = len(s_1004)
        _x_27695 = len(suffix_1003)
        _x_27696 = _x_27694 - _x_27695
        _x_27697 = strings_take(_x_27696, s_1004)
        return _x_27697
    else:
        return s_1004

# Lean: Corpus.Strings.toCharList
def to_char_list(s_1005: str) -> list[str]:
    _x_27700 = list(s_1005)
    return _x_27700

# Lean: Corpus.Strings.fromCharList
def from_char_list(cs_1006: list[str]) -> str:
    _x_27702 = ''.join(cs_1006)
    return _x_27702

# Lean: Corpus.Strings.filterChars
def filter_chars(p_1007: Callable[[str], bool], s_1008: str) -> str:
    _x_27704 = list(s_1008)
    _x_27705 = [x for x in _x_27704 if p_1007(x)]
    _x_27706 = ''.join(_x_27705)
    return _x_27706

# Lean: Corpus.Strings.mapChars
def map_chars(f_1009: Callable[[str], str], s_1010: str) -> str:
    _x_27708 = list(s_1010)
    _x_27709 = [f_1009(x) for x in _x_27708]
    _x_27710 = ''.join(_x_27709)
    return _x_27710

# Lean: Corpus.Strings.ord
def strings_ord(c_1011: str) -> int:
    _x_27712 = ord(c_1011)
    return _x_27712

# Lean: Corpus.Strings.chr
def strings_chr(n_1012: int) -> str:
    _x_27714 = chr(n_1012)
    return _x_27714

# Lean: Corpus.Strings.toAsciiCodes
def to_ascii_codes(s_1013: str) -> list[int]:
    _x_27716 = ord
    _x_27717 = list(s_1013)
    _x_27718 = [_x_27716(x) for x in _x_27717]
    return _x_27718

# Lean: Corpus.Strings.fromAsciiCodes
def from_ascii_codes(ns: list[int]) -> str:
    _x_27720 = chr
    _x_27721 = [_x_27720(x) for x in ns]
    _x_27722 = ''.join(_x_27721)
    return _x_27722

# Lean: Corpus.Games.Player.other
def other(x_27724: Player) -> Player:
    def _f_27726():
        _x_27725 = O()
        return _x_27725
    _alt_27727 = _f_27726
    def _f_27729():
        _x_27728 = X()
        return _x_27728
    _alt_27730 = _f_27729
    match x_27724:
        case X():
            _x_27732 = _alt_27727()
            return _x_27732
        case O():
            _x_27734 = _alt_27730()
            return _x_27734

# Lean: Corpus.Games.TicTacToe.empty
def tic_tac_toe_empty() -> TicTacToe:
    _x_27737 = 9
    _x_27740 = None
    _x_27741 = replicate_tr(None, 9, _x_27740)
    _x_27742 = X()
    _x_27743 = TicTacToe_mk(_x_27741, _x_27742)
    return _x_27743

# Lean: Corpus.Games.TicTacToe.get
def tic_tac_toe_get(g_1016: TicTacToe, row: int, col: int) -> Player | None:
    _alt_27745 = (lambda p_1017: p_1017)
    def _f_27747():
        _x_27746 = None
        return _x_27746
    _alt_27748 = _f_27747
    _x_27750 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_27751 = g_1016.field_0
    _x_27758 = 3
    _x_27761 = row * 3
    _x_27762 = _x_27761 + col
    _x_27763 = _x_27750(_x_27751, _x_27762)
    if _x_27763 is None:
        _x_27765 = _alt_27748()
        return _x_27765
    else:
        val_27766 = _x_27763
        _x_27767 = _alt_27745(val_27766)
        return _x_27767

# Lean: Corpus.Games.TicTacToe.set
def tic_tac_toe_set(g_1019: TicTacToe, row_1020: int, col_1021: int) -> TicTacToe | None:
    _x_27776 = 3
    _x_27779 = row_1020 * 3
    _x_27780 = _x_27779 + col_1021
    _x_27781 = 9
    _x_27784 = 9 <= _x_27780
    if _x_27784:
        _x_27818 = None
        return _x_27818
    else:
        def _f_27793():
            _x_27786 = g_1019.field_0
            _x_27787 = g_1019.field_1
            _x_27788 = _x_27787
            _x_27789 = set_tr(None, _x_27786, _x_27780, _x_27788)
            _x_27790 = other(_x_27787)
            _x_27791 = TicTacToe_mk(_x_27789, _x_27790)
            _x_27792 = _x_27791
            return _x_27792
        _alt_27794 = _f_27793
        def _f_27797(x_27795: Player | None | None):
            _x_27796 = None
            return _x_27796
        _alt_27798 = _f_27797
        _x_27800 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_27801 = g_1019.field_0
        _x_27802 = _x_27800(_x_27801, _x_27780)
        if _x_27802 is None:
            _x_27815 = (lambda h_27812: _alt_27798(_x_27802))(None)
            return _x_27815
        else:
            val_27803 = _x_27802
            if val_27803 is None:
                _x_27805 = _alt_27794()
                return _x_27805
            else:
                def _f_27809(h_27806: Any):
                    _x_27807 = val_27803
                    _x_27808 = _alt_27798(_x_27807)
                    return _x_27808
                _x_27810 = _f_27809(None)
                return _x_27810

# Lean: Corpus.Games.TicTacToe.checkLine
def check_line(g_1024: TicTacToe, i1: int, i2: int, i3: int) -> Player | None:
    def _f_27851(p1_1025: Player, p2_1026: Player, p3_1027: Player):
        def _f_27822():
            _x_27821 = False
            return False
        _alt_27823 = _f_27822
        def _f_27827():
            _x_27826 = p2_1026 == p3_1027
            return _x_27826
        _alt_27828 = _f_27827
        _x_27831 = p1_1025 == p2_1026
        def _jp_27844(_y_27836: bool):
            _x_27837 = True
            _x_27838 = _y_27836 == True
            if _x_27838:
                _x_27842 = p1_1025
                return _x_27842
            else:
                _x_27840 = None
                return _x_27840
        def _jp_27847():
            _x_27846 = _alt_27823()
            return _jp_27844(_x_27846)
        def _jp_27850():
            _x_27849 = _alt_27828()
            return _jp_27844(_x_27849)
        if _x_27831:
            return _jp_27850()
        else:
            return _jp_27847()
    _alt_27852 = _f_27851
    def _f_27857(x_27853: Player | None | None, x_27854: Player | None | None, x_27855: Player | None | None):
        _x_27856 = None
        return _x_27856
    _alt_27858 = _f_27857
    _x_27860 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_27861 = g_1024.field_0
    _x_27862 = _x_27860(_x_27861, i1)
    if _x_27862 is None:
        _x_27921 = (lambda h_27916: _alt_27858(_x_27862, _x_27860(_x_27861, i2), _x_27860(_x_27861, i3)))(None)
        return _x_27921
    else:
        val_27863 = _x_27862
        if val_27863 is None:
            def _f_27913(h_27908: Any):
                _x_27909 = val_27863
                _x_27910 = _x_27860(_x_27861, i2)
                _x_27911 = _x_27860(_x_27861, i3)
                _x_27912 = _alt_27858(_x_27909, _x_27910, _x_27911)
                return _x_27912
            _x_27914 = _f_27913(None)
            return _x_27914
        else:
            val_27864 = val_27863
            _x_27865 = _x_27860(_x_27861, i2)
            if _x_27865 is None:
                def _f_27905(h_27900: Any):
                    _x_27901 = val_27864
                    _x_27902 = _x_27901
                    _x_27903 = _x_27860(_x_27861, i3)
                    _x_27904 = _alt_27858(_x_27902, _x_27865, _x_27903)
                    return _x_27904
                _x_27906 = _f_27905(None)
                return _x_27906
            else:
                val_27866 = _x_27865
                if val_27866 is None:
                    def _f_27897(h_27891: Any):
                        _x_27892 = val_27864
                        _x_27893 = _x_27892
                        _x_27894 = val_27866
                        _x_27895 = _x_27860(_x_27861, i3)
                        _x_27896 = _alt_27858(_x_27893, _x_27894, _x_27895)
                        return _x_27896
                    _x_27898 = _f_27897(None)
                    return _x_27898
                else:
                    val_27867 = val_27866
                    _x_27868 = _x_27860(_x_27861, i3)
                    if _x_27868 is None:
                        def _f_27888(h_27882: Any):
                            _x_27883 = val_27864
                            _x_27884 = _x_27883
                            _x_27885 = val_27867
                            _x_27886 = _x_27885
                            _x_27887 = _alt_27858(_x_27884, _x_27886, _x_27868)
                            return _x_27887
                        _x_27889 = _f_27888(None)
                        return _x_27889
                    else:
                        val_27869 = _x_27868
                        if val_27869 is None:
                            def _f_27879(h_27872: Any):
                                _x_27873 = val_27864
                                _x_27874 = _x_27873
                                _x_27875 = val_27867
                                _x_27876 = _x_27875
                                _x_27877 = val_27869
                                _x_27878 = _alt_27858(_x_27874, _x_27876, _x_27877)
                                return _x_27878
                            _x_27880 = _f_27879(None)
                            return _x_27880
                        else:
                            val_27870 = val_27869
                            _x_27871 = _alt_27852(val_27864, val_27867, val_27870)
                            return _x_27871

# Lean: Corpus.Games.TicTacToe.winner
def winner(g_1030: TicTacToe) -> Player | None:
    _x_27924 = 0
    _x_27927 = 1
    _x_27930 = 2
    _x_27933 = (1, 2)
    _x_27934 = (0, _x_27933)
    _x_27935 = 3
    _x_27938 = 4
    _x_27941 = 5
    _x_27944 = (4, 5)
    _x_27945 = (3, _x_27944)
    _x_27946 = 6
    _x_27949 = 7
    _x_27952 = 8
    _x_27955 = (7, 8)
    _x_27956 = (6, _x_27955)
    _x_27957 = (3, 6)
    _x_27958 = (0, _x_27957)
    _x_27959 = (4, 7)
    _x_27960 = (1, _x_27959)
    _x_27961 = (5, 8)
    _x_27962 = (2, _x_27961)
    _x_27963 = (4, 8)
    _x_27964 = (0, _x_27963)
    _x_27965 = (4, 6)
    _x_27966 = (2, _x_27965)
    _x_27967 = []
    _x_27968 = [_x_27966] + _x_27967
    _x_27969 = [_x_27964] + _x_27968
    _x_27970 = [_x_27962] + _x_27969
    _x_27971 = [_x_27960] + _x_27970
    _x_27972 = [_x_27958] + _x_27971
    _x_27973 = [_x_27956] + _x_27972
    _x_27974 = [_x_27945] + _x_27973
    _x_27975 = [_x_27934] + _x_27974
    def _f_27987(x_27976: tuple[int, tuple[int, int]]):
        def _f_27978(i1_1031: int, i2_1032: int, i3_1033: int):
            _x_27977 = check_line(g_1030, i1_1031, i2_1032, i3_1033)
            return _x_27977
        _alt_27979 = _f_27978
        match x_27976:
            case (fst_27980, snd_27981):
                match snd_27981:
                    case (fst_27982, snd_27983):
                        _x_27984 = _alt_27979(fst_27980, fst_27982, snd_27983)
                        return _x_27984
    _x_27988 = next((_y for x in _x_27975 if (_y := _f_27987(x)) is not None), None)
    return _x_27988

# Lean: Corpus.Games.TicTacToe.isDraw
def is_draw(g_1034: TicTacToe) -> bool:
    def _f_27991():
        _x_27990 = False
        return False
    _alt_27992 = _f_27991
    def _f_27996():
        _x_27993 = g_1034.field_0
        _x_27994 = (lambda x: x is not None)(None)
        _x_27995 = all(_x_27994(x) for x in _x_27993)
        return _x_27995
    _alt_27997 = _f_27996
    _x_27998 = winner(g_1034)
    _x_27999 = (lambda x: x is None)(_x_27998)
    if _x_27999:
        _x_28003 = _alt_27997()
        return _x_28003
    else:
        _x_28001 = _alt_27992()
        return _x_28001

# Lean: Corpus.Games.TicTacToe.isOver
def tic_tac_toe_is_over(g_1037: TicTacToe) -> bool:
    def _f_28007():
        _x_28006 = True
        return True
    _alt_28008 = _f_28007
    def _f_28010():
        _x_28009 = is_draw(g_1037)
        return _x_28009
    _alt_28011 = _f_28010
    _x_28012 = winner(g_1037)
    _x_28013 = (lambda x: x is not None)(_x_28012)
    if _x_28013:
        _x_28017 = _alt_28008()
        return _x_28017
    else:
        _x_28015 = _alt_28011()
        return _x_28015

# Lean: Corpus.Games.TicTacToe.validMoves
def valid_moves(g_1040: TicTacToe) -> list[tuple[int, int]]:
    _x_28020 = tic_tac_toe_is_over(g_1040)
    _x_28021 = True
    _x_28022 = _x_28020 == True
    if _x_28022:
        _x_28068 = []
        return _x_28068
    else:
        def _f_28061(i_1041: int):
            def _f_28037():
                _x_28027 = 3
                _x_28030 = i_1041 // 3
                _x_28034 = i_1041 % 3
                _x_28035 = (_x_28030, _x_28034)
                _x_28036 = _x_28035
                return _x_28036
            _alt_28038 = _f_28037
            def _f_28041(x_28039: Player | None | None):
                _x_28040 = None
                return _x_28040
            _alt_28042 = _f_28041
            _x_28044 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_28045 = g_1040.field_0
            _x_28046 = _x_28044(_x_28045, i_1041)
            if _x_28046 is None:
                _x_28059 = (lambda h_28056: _alt_28042(_x_28046))(None)
                return _x_28059
            else:
                val_28047 = _x_28046
                if val_28047 is None:
                    _x_28049 = _alt_28038()
                    return _x_28049
                else:
                    def _f_28053(h_28050: Any):
                        _x_28051 = val_28047
                        _x_28052 = _alt_28042(_x_28051)
                        return _x_28052
                    _x_28054 = _f_28053(None)
                    return _x_28054
        _x_28062 = 9
        _x_28065 = list(range(9))
        _x_28066 = [_y for x in _x_28065 if (_y := _f_28061(x)) is not None]
        return _x_28066

# Lean: Corpus.Games.Nim.create
def nim_create(sizes: list[int]) -> Nim:
    _x_28071 = Nim_mk(sizes)
    return _x_28071

# Lean: Corpus.Games.Nim.take
def nim_take(g_1043: Nim, pile: int, count_1044: int) -> Nim | None:
    def _f_28111(n_1045: int):
        def _f_28074():
            _x_28073 = False
            return False
        _alt_28075 = _f_28074
        def _f_28078():
            _x_28076 = count_1044 <= n_1045
            return _x_28076
        _alt_28079 = _f_28078
        _x_28080 = 0
        _x_28083 = 0 < count_1044
        def _jp_28104(_y_28089: bool):
            _x_28090 = True
            _x_28091 = _y_28089 == True
            if _x_28091:
                _x_28095 = g_1043.field_0
                _x_28099 = n_1045 - count_1044
                _x_28100 = set_tr(None, _x_28095, pile, _x_28099)
                _x_28101 = Nim_mk(_x_28100)
                _x_28102 = _x_28101
                return _x_28102
            else:
                _x_28093 = None
                return _x_28093
        def _jp_28110():
            _x_28109 = _alt_28079()
            return _jp_28104(_x_28109)
        def _jp_28107():
            _x_28106 = _alt_28075()
            return _jp_28104(_x_28106)
        if _x_28083:
            return _jp_28110()
        else:
            return _jp_28107()
    _alt_28112 = _f_28111
    def _f_28114():
        _x_28113 = None
        return _x_28113
    _alt_28115 = _f_28114
    _x_28117 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_28118 = g_1043.field_0
    _x_28119 = _x_28117(_x_28118, pile)
    if _x_28119 is None:
        _x_28121 = _alt_28115()
        return _x_28121
    else:
        val_28122 = _x_28119
        _x_28123 = _alt_28112(val_28122)
        return _x_28123

# Lean: Corpus.Games.Nim.isOver
def nim_is_over(g_1049: Nim) -> bool:
    _x_28126 = g_1049.field_0
    _x_28136 = all((x_28127 == 0) for x_28127 in _x_28126)
    return _x_28136

# Lean: Corpus.Games.Nim.nimSum
def nim_sum(g_1050: Nim) -> int:
    _x_28138 = (lambda a, b: a ^ b)
    _x_28139 = 0
    _x_28142 = g_1050.field_0
    _x_28143 = functools.reduce(_x_28138, _x_28142, 0)
    return _x_28143

# Lean: Corpus.Games.Nim.isWinningPosition
def is_winning_position(g_1051: Nim) -> bool:
    _x_28147 = nim_sum(g_1051)
    _x_28148 = 0
    _x_28151 = (lambda a, b: a != b)(0)
    return _x_28151

# Lean: Corpus.Games.Card.value
def value(c_1052: Card) -> int:
    def _f_28156():
        _x_28153 = 11
        return 11
    _alt_28157 = _f_28156
    def _f_28161():
        _x_28158 = 2
        return 2
    _alt_28162 = _f_28161
    def _f_28166():
        _x_28163 = 3
        return 3
    _alt_28167 = _f_28166
    def _f_28171():
        _x_28168 = 4
        return 4
    _alt_28172 = _f_28171
    def _f_28176():
        _x_28173 = 5
        return 5
    _alt_28177 = _f_28176
    def _f_28181():
        _x_28178 = 6
        return 6
    _alt_28182 = _f_28181
    def _f_28186():
        _x_28183 = 7
        return 7
    _alt_28187 = _f_28186
    def _f_28191():
        _x_28188 = 8
        return 8
    _alt_28192 = _f_28191
    def _f_28196():
        _x_28193 = 9
        return 9
    _alt_28197 = _f_28196
    def _f_28201():
        _x_28198 = 10
        return 10
    _alt_28202 = _f_28201
    _alt_28203 = _f_28201
    _alt_28204 = _f_28201
    _alt_28205 = _f_28201
    _x_28206 = c_1052.field_0
    match _x_28206:
        case ace():
            _x_28208 = _alt_28157()
            return _x_28208
        case two():
            _x_28210 = _alt_28162()
            return _x_28210
        case three():
            _x_28212 = _alt_28167()
            return _x_28212
        case four():
            _x_28214 = _alt_28172()
            return _x_28214
        case five():
            _x_28216 = _alt_28177()
            return _x_28216
        case six():
            _x_28218 = _alt_28182()
            return _x_28218
        case seven():
            _x_28220 = _alt_28187()
            return _x_28220
        case eight():
            _x_28222 = _alt_28192()
            return _x_28222
        case nine():
            _x_28224 = _alt_28197()
            return _x_28224
        case ten():
            _x_28226 = _alt_28202()
            return _x_28226
        case jack():
            _x_28228 = _alt_28203()
            return _x_28228
        case queen():
            _x_28230 = _alt_28204()
            return _x_28230
        case king():
            _x_28232 = _alt_28205()
            return _x_28232

# Lean: Corpus.Games.Card.isAce
def is_ace(c_1063: Card) -> bool:
    _x_28237 = c_1063.field_0
    _x_28238 = ace()
    _x_28239 = _x_28237 == _x_28238
    return _x_28239

# Lean: Corpus.Games.BlackjackHand.empty
def blackjack_hand_empty() -> BlackjackHand:
    _x_28241 = []
    _x_28242 = BlackjackHand_mk(_x_28241)
    return _x_28242

# Lean: Corpus.Games.BlackjackHand.add
def add(h_1064: BlackjackHand, c_1065: Card) -> BlackjackHand:
    _x_28243 = h_1064.field_0
    _x_28244 = [c_1065] + _x_28243
    _x_28245 = BlackjackHand_mk(_x_28244)
    return _x_28245

# Lean: Corpus.Games.BlackjackHand.hardValue
def hard_value(h_1066: BlackjackHand) -> int:
    def _f_28252(acc_1067: int, c_1068: Card):
        _x_28250 = value(c_1068)
        _x_28251 = acc_1067 + _x_28250
        return _x_28251
    _x_28253 = 0
    _x_28256 = h_1066.field_0
    _x_28257 = functools.reduce(_f_28252, _x_28256, 0)
    return _x_28257

# Lean: Corpus.Games.BlackjackHand.numAces
def num_aces(h_1069: BlackjackHand) -> int:
    _x_28259 = is_ace()
    _x_28260 = h_1069.field_0
    _x_28261 = [x for x in _x_28260 if _x_28259(x)]
    _x_28262 = len(_x_28261)
    return _x_28262

# Lean: Corpus.Games.BlackjackHand.bestValue
def best_value(h_1070: BlackjackHand) -> int:
    _x_28264 = hard_value(h_1070)
    _x_28265 = num_aces(h_1070)
    _x_28266 = best_value_adjust(_x_28264, _x_28265)
    return _x_28266

# Lean: Corpus.Games.BlackjackHand.isBust
def is_bust(h_1071: BlackjackHand) -> bool:
    _x_28268 = 21
    _x_28271 = best_value(h_1071)
    _x_28272 = 21 < _x_28271
    return _x_28272

# Lean: Corpus.Games.BlackjackHand.isBlackjack
def is_blackjack(h_1072: BlackjackHand) -> bool:
    def _f_28276():
        _x_28275 = False
        return False
    _alt_28277 = _f_28276
    def _f_28286():
        _x_28281 = best_value(h_1072)
        _x_28282 = 21
        _x_28285 = _x_28281 == 21
        return _x_28285
    _alt_28287 = _f_28286
    _x_28291 = h_1072.field_0
    _x_28292 = len(_x_28291)
    _x_28293 = 2
    _x_28296 = _x_28292 == 2
    if _x_28296:
        _x_28300 = _alt_28287()
        return _x_28300
    else:
        _x_28298 = _alt_28277()
        return _x_28298

# Lean: Corpus.Games.roll
def roll(sides_1075: int, seed_1076: int) -> int:
    _x_28312 = 1103515245
    _x_28315 = seed_1076 * 1103515245
    _x_28316 = 12345
    _x_28319 = _x_28315 + 12345
    _x_28324 = 2
    _x_28327 = 31
    _x_28330 = 2 ** 31
    _x_28331 = _x_28319 % _x_28330
    _x_28332 = _x_28331 % sides_1075
    _x_28333 = 1
    _x_28336 = _x_28332 + 1
    return _x_28336

# Lean: Corpus.Games.rollDice
def roll_dice(num_dice: int, sides_1077: int, seed_1078: int) -> tuple[list[int], int]:
    _x_28338 = []
    _x_28339 = roll_dice_go(sides_1077, num_dice, seed_1078, _x_28338)
    return _x_28339

# Lean: Corpus.Games.sumDice
def sum_dice(dice: list[int]) -> int:
    def _f_28347(x1_28341: int, x2_28342: int):
        _x_28346 = x1_28341 + x2_28342
        return _x_28346
    _x_28348 = 0
    _x_28351 = functools.reduce(_f_28347, dice, 0)
    return _x_28351

# Lean: Corpus.Games.yahtzeeScore
def yahtzee_score(dice_1079: list[int]) -> int:
    _x_28355 = len(dice_1079)
    _x_28356 = 5
    _x_28359 = (lambda a, b: a != b)(5)
    _x_28360 = True
    _x_28361 = _x_28359 == True
    if _x_28361:
        _x_28505 = 0
        return 0
    else:
        _x_28363 = list(dice_1079)
        def _f_28368(x1_28364: int, x2_28365: int):
            _x_28366 = x1_28364 < x2_28365
            return _x_28366
        _x_28369 = 0
        _x_28375 = len(_x_28363)
        _x_28376 = 1
        _x_28379 = _x_28375 - 1
        _x_28380 = sorted(0, key=functools.cmp_to_key(lambda a, b: -1 if _x_28379(a, b) else 1))
        _x_28381 = list(_x_28380)
        def _f_28392(n_1081: int):
            _x_28390 = [x_28382 for x_28382 in dice_1079 if (x_28382 == (n_1081 + 1))]
            _x_28391 = len(_x_28390)
            return _x_28391
        _x_28393 = 6
        _x_28396 = list(range(6))
        _x_28397 = [_f_28392(x) for x in _x_28396]
        _x_28399 = max
        _x_28400 = functools.reduce(_x_28399, _x_28397, 0)
        def _f_28407(x1_28401: int, x2_28402: int):
            _x_28406 = x1_28401 + x2_28402
            return _x_28406
        _x_28408 = functools.reduce(_f_28407, dice_1079, 0)
        _x_28410 = _x_28400 == 5
        _x_28411 = _x_28410 == True
        if _x_28411:
            _x_28500 = 50
            return 50
        else:
            def _f_28414():
                _x_28413 = True
                return True
            _alt_28415 = _f_28414
            def _f_28434():
                _x_28418 = 2
                _x_28421 = 3
                _x_28424 = 4
                _x_28427 = []
                _x_28428 = [6] + _x_28427
                _x_28429 = [5] + _x_28428
                _x_28430 = [4] + _x_28429
                _x_28431 = [3] + _x_28430
                _x_28432 = [2] + _x_28431
                _x_28433 = _x_28381 == _x_28432
                return _x_28433
            _alt_28435 = _f_28434
            _x_28438 = 2
            _x_28441 = 3
            _x_28444 = 4
            _x_28447 = []
            _x_28448 = [5] + _x_28447
            _x_28449 = [4] + _x_28448
            _x_28450 = [3] + _x_28449
            _x_28451 = [2] + _x_28450
            _x_28452 = [1] + _x_28451
            _x_28453 = _x_28381 == _x_28452
            def _jp_28492(_y_28458: bool):
                _x_28459 = _y_28458 == True
                if _x_28459:
                    _x_28488 = 40
                    return 40
                else:
                    def _f_28462():
                        _x_28461 = False
                        return False
                    _alt_28463 = _f_28462
                    def _f_28465():
                        _x_28464 = 2 in _x_28397
                        return _x_28464
                    _alt_28466 = _f_28465
                    _x_28467 = 3 in _x_28397
                    def _jp_28480(_y_28472: bool):
                        _x_28473 = _y_28472 == True
                        if _x_28473:
                            _x_28476 = 25
                            return 25
                        else:
                            return _x_28408
                    def _jp_28483():
                        _x_28482 = _alt_28463()
                        return _jp_28480(_x_28482)
                    def _jp_28486():
                        _x_28485 = _alt_28466()
                        return _jp_28480(_x_28485)
                    if _x_28467:
                        return _jp_28486()
                    else:
                        return _jp_28483()
            def _jp_28495():
                _x_28494 = _alt_28435()
                return _jp_28492(_x_28494)
            def _jp_28498():
                _x_28497 = _alt_28415()
                return _jp_28492(_x_28497)
            if _x_28453:
                return _jp_28498()
            else:
                return _jp_28495()

# Lean: Corpus.Games.RPS.beats
def beats(x_28510: RPS, x_28511: RPS) -> bool:
    def _f_28513():
        _x_28512 = True
        return True
    _alt_28514 = _f_28513
    _alt_28515 = _f_28513
    _alt_28516 = _f_28513
    def _f_28520(x_28517: RPS, x_28518: RPS):
        _x_28519 = False
        return False
    _alt_28521 = _f_28520
    match x_28510:
        case rock():
            match x_28511:
                case scissors():
                    _x_28523 = _alt_28514()
                    return _x_28523
                case _:
                    def _f_28527(h_28524: Any):
                        _x_28525 = rock()
                        _x_28526 = _alt_28521(_x_28525, x_28511)
                        return _x_28526
                    _x_28528 = _f_28527(None)
                    return _x_28528
        case paper():
            match x_28511:
                case rock():
                    _x_28531 = _alt_28515()
                    return _x_28531
                case _:
                    def _f_28535(h_28532: Any):
                        _x_28533 = paper()
                        _x_28534 = _alt_28521(_x_28533, x_28511)
                        return _x_28534
                    _x_28536 = _f_28535(None)
                    return _x_28536
        case scissors():
            match x_28511:
                case paper():
                    _x_28539 = _alt_28516()
                    return _x_28539
                case _:
                    def _f_28543(h_28540: Any):
                        _x_28541 = scissors()
                        _x_28542 = _alt_28521(_x_28541, x_28511)
                        return _x_28542
                    _x_28544 = _f_28543(None)
                    return _x_28544

# Lean: Corpus.Games.RPS.compare
def compare(a_1088: RPS, b_1089: RPS) -> int:
    _x_28550 = a_1088 == b_1089
    _x_28551 = True
    _x_28552 = _x_28550 == True
    if _x_28552:
        _x_28569 = 0
        return 0
    else:
        _x_28554 = beats(a_1088, b_1089)
        _x_28555 = _x_28554 == True
        if _x_28555:
            _x_28564 = 1
            return 1
        else:
            _x_28559 = 1
            _x_28562 = -1
            return _x_28562

# Lean: Corpus.Games.RPS.fromNat
def from_nat(x_28574: int) -> RPS | None:
    def _f_28577():
        _x_28575 = rock()
        _x_28576 = _x_28575
        return _x_28576
    _alt_28578 = _f_28577
    def _f_28581():
        _x_28579 = paper()
        _x_28580 = _x_28579
        return _x_28580
    _alt_28582 = _f_28581
    def _f_28585():
        _x_28583 = scissors()
        _x_28584 = _x_28583
        return _x_28584
    _alt_28586 = _f_28585
    def _f_28589(x_28587: int):
        _x_28588 = None
        return _x_28588
    _alt_28590 = _f_28589
    _x_28591 = 0
    _x_28594 = x_28574 == 0
    if _x_28594:
        _x_28613 = _alt_28578()
        return _x_28613
    else:
        _x_28595 = 1
        _x_28598 = x_28574 == 1
        if _x_28598:
            _x_28609 = _alt_28582()
            return _x_28609
        else:
            _x_28599 = 2
            _x_28602 = x_28574 == 2
            if _x_28602:
                _x_28605 = _alt_28586()
                return _x_28605
            else:
                _x_28603 = _alt_28590(x_28574)
                return _x_28603

# Lean: Corpus.Games.isValidSudokuRow
def is_valid_sudoku_row(row_1093: list[int]) -> bool:
    def _f_28624(x_28617: int):
        _x_28620 = 0
        _x_28623 = (lambda a, b: a != b)(0)
        return _x_28623
    _x_28625 = [x for x in row_1093 if _f_28624(x)]
    _x_28629 = len(_x_28625)
    _x_28630 = {x for x in row_1093 if _f_28624(x)}
    _x_28631 = len(_x_28630)
    _x_28632 = _x_28629 == _x_28631
    return _x_28632

# Lean: Corpus.Games.isValidSudokuGrid
def is_valid_sudoku_grid(grid: list[list[int]]) -> bool:
    _x_28634 = is_valid_sudoku_row()
    _x_28635 = all(_x_28634(x) for x in grid)
    def _f_28641(c_1094: int):
        def _f_28639(row_1095: list[int]):
            _x_28637 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_28638 = _x_28637(row_1095, c_1094)
            return _x_28638
        _x_28640 = [_y for x in grid if (_y := _f_28639(x)) is not None]
        return _x_28640
    _x_28642 = 9
    _x_28645 = list(range(9))
    _x_28646 = [_f_28641(x) for x in _x_28645]
    _x_28647 = all(_x_28634(x) for x in _x_28646)
    def _f_28704(br: int):
        def _f_28698(bc: int):
            def _f_28692(r_1096: int):
                def _f_28686(c_1097: int):
                    def _f_28662(row_1098: list[int]):
                        _x_28649 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                        _x_28656 = 3
                        _x_28659 = bc * 3
                        _x_28660 = _x_28659 + c_1097
                        _x_28661 = _x_28649(row_1098, _x_28660)
                        return _x_28661
                    _alt_28663 = _f_28662
                    def _f_28665():
                        _x_28664 = None
                        return _x_28664
                    _alt_28666 = _f_28665
                    _x_28668 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                    _x_28675 = 3
                    _x_28678 = br * 3
                    _x_28679 = _x_28678 + r_1096
                    _x_28680 = _x_28668(grid, _x_28679)
                    if _x_28680 is None:
                        _x_28682 = _alt_28666()
                        return _x_28682
                    else:
                        val_28683 = _x_28680
                        _x_28684 = _alt_28663(val_28683)
                        return _x_28684
                _x_28687 = 3
                _x_28690 = list(range(3))
                _x_28691 = [_y for x in _x_28690 if (_y := _f_28686(x)) is not None]
                return _x_28691
            _x_28693 = 3
            _x_28696 = list(range(3))
            _x_28697 = flat_map_tr(None, None, _f_28692, _x_28696)
            return _x_28697
        _x_28699 = 3
        _x_28702 = list(range(3))
        _x_28703 = [_f_28698(x) for x in _x_28702]
        return _x_28703
    _x_28705 = 3
    _x_28708 = list(range(3))
    _x_28709 = flat_map_tr(None, None, _f_28704, _x_28708)
    _x_28710 = all(_x_28634(x) for x in _x_28709)
    def _f_28712():
        _x_28711 = False
        return False
    _alt_28713 = _f_28712
    def _f_28714():
        return _x_28710
    _alt_28715 = _f_28714
    _alt_28716 = _f_28712
    def _f_28717():
        return _x_28647
    _alt_28718 = _f_28717
    def _jp_28729(_y_28723: bool):
        if _y_28723:
            _x_28727 = _alt_28715()
            return _x_28727
        else:
            _x_28725 = _alt_28713()
            return _x_28725
    def _jp_28735():
        _x_28734 = _alt_28718()
        return _jp_28729(_x_28734)
    def _jp_28732():
        _x_28731 = _alt_28716()
        return _jp_28729(_x_28731)
    if _x_28635:
        return _jp_28735()
    else:
        return _jp_28732()

# Lean: Corpus.DataStructures.Stack.empty
def stack_empty(__1103: Any) -> Any:
    _x_28737 = []
    _x_28738 = Stack_mk(_x_28737)
    return _x_28738

# Lean: Corpus.DataStructures.Stack.push
def stack_push(__1104: Any, s_1105: Any, x_1106: Any) -> Any:
    _x_28740 = s_1105.field_0
    _x_28741 = [x_1106] + _x_28740
    _x_28742 = Stack_mk(_x_28741)
    return _x_28742

# Lean: Corpus.DataStructures.Stack.pop
def pop(__1107: Any, s_1108: Any) -> tuple[Any, Any] | None:
    def _f_28745():
        _x_28744 = None
        return _x_28744
    _alt_28746 = _f_28745
    def _f_28750(x_1110: Any, xs_1111: list[Any]):
        _x_28747 = Stack_mk(xs_1111)
        _x_28748 = (x_1110, _x_28747)
        _x_28749 = _x_28748
        return _x_28749
    _alt_28751 = _f_28750
    _x_28752 = s_1108.field_0
    if len(_x_28752) == 0:
        _x_28754 = _alt_28746()
        return _x_28754
    else:
        head_28755 = _x_28752[0]
        tail_28756 = _x_28752[1:]
        _x_28757 = _alt_28751(head_28755, tail_28756)
        return _x_28757

# Lean: Corpus.DataStructures.Stack.peek
def peek(__1112: Any, s_1113: Any) -> Any | None:
    _x_28760 = s_1113.field_0
    _x_28761 = (lambda xs: xs[0] if xs else None)(_x_28760)
    return _x_28761

# Lean: Corpus.DataStructures.Stack.isEmpty
def stack_is_empty(__1114: Any, s_1115: Any) -> bool:
    _x_28763 = s_1115.field_0
    _x_28764 = len(_x_28763) == 0
    return _x_28764

# Lean: Corpus.DataStructures.Stack.size
def stack_size(__1116: Any, s_1117: Any) -> int:
    _x_28766 = s_1117.field_0
    _x_28767 = len(_x_28766)
    return _x_28767

# Lean: Corpus.DataStructures.Queue.empty
def queue_empty(__1118: Any) -> Any:
    _x_28769 = []
    _x_28770 = Queue_mk(_x_28769, _x_28769)
    return _x_28770

# Lean: Corpus.DataStructures.Queue.enqueue
def enqueue(__1119: Any, q_1120: Any, x_1121: Any) -> Any:
    _x_28772 = q_1120.field_0
    _x_28773 = q_1120.field_1
    _x_28774 = [x_1121] + _x_28773
    _x_28775 = Queue_mk(_x_28772, _x_28774)
    return _x_28775

# Lean: Corpus.DataStructures.Queue.dequeue
def dequeue(__1122: Any, q_1123: Any) -> tuple[Any, Any] | None:
    def _f_28781(x_1124: Any, xs_1125: list[Any]):
        _x_28777 = q_1123.field_1
        _x_28778 = Queue_mk(xs_1125, _x_28777)
        _x_28779 = (x_1124, _x_28778)
        _x_28780 = _x_28779
        return _x_28780
    _alt_28782 = _f_28781
    def _f_28800():
        def _f_28784():
            _x_28783 = None
            return _x_28783
        _alt_28785 = _f_28784
        def _f_28790(x_1128: Any, xs_1129: list[Any]):
            _x_28786 = []
            _x_28787 = Queue_mk(xs_1129, _x_28786)
            _x_28788 = (x_1128, _x_28787)
            _x_28789 = _x_28788
            return _x_28789
        _alt_28791 = _f_28790
        _x_28792 = q_1123.field_1
        _x_28793 = list(reversed(_x_28792))
        if len(_x_28793) == 0:
            _x_28795 = _alt_28785()
            return _x_28795
        else:
            head_28796 = _x_28793[0]
            tail_28797 = _x_28793[1:]
            _x_28798 = _alt_28791(head_28796, tail_28797)
            return _x_28798
    _alt_28801 = _f_28800
    _x_28802 = q_1123.field_0
    if len(_x_28802) == 0:
        _x_28804 = _alt_28801()
        return _x_28804
    else:
        head_28805 = _x_28802[0]
        tail_28806 = _x_28802[1:]
        _x_28807 = _alt_28782(head_28805, tail_28806)
        return _x_28807

# Lean: Corpus.DataStructures.Queue.isEmpty
def queue_is_empty(__1130: Any, q_1131: Any) -> bool:
    def _f_28811():
        _x_28810 = False
        return False
    _alt_28812 = _f_28811
    def _f_28815():
        _x_28813 = q_1131.field_1
        _x_28814 = len(_x_28813) == 0
        return _x_28814
    _alt_28816 = _f_28815
    _x_28817 = q_1131.field_0
    _x_28818 = len(_x_28817) == 0
    if _x_28818:
        _x_28822 = _alt_28816()
        return _x_28822
    else:
        _x_28820 = _alt_28812()
        return _x_28820

# Lean: Corpus.DataStructures.Queue.size
def queue_size(__1134: Any, q_1135: Any) -> int:
    _x_28828 = q_1135.field_0
    _x_28829 = len(_x_28828)
    _x_28830 = q_1135.field_1
    _x_28831 = len(_x_28830)
    _x_28832 = _x_28829 + _x_28831
    return _x_28832

# Lean: Corpus.DataStructures.BinaryTree.singleton
def singleton(__1136: Any, x_1137: Any) -> Any:
    _x_28834 = BinaryTree_empty()
    _x_28835 = BinaryTree_node(x_1137, _x_28834, _x_28834)
    return _x_28835

# Lean: Corpus.DataStructures.BinaryTree.size
def binary_tree_size(__1138: Any, t_1139: Any) -> int:
    def _f_28840():
        _x_28837 = 0
        return 0
    _alt_28841 = _f_28840
    def _f_28853(a_28842: Any, l_1141: Any, r_1142: Any):
        _x_28846 = 1
        _x_28849 = binary_tree_size(None, l_1141)
        _x_28850 = 1 + _x_28849
        _x_28851 = binary_tree_size(None, r_1142)
        _x_28852 = _x_28850 + _x_28851
        return _x_28852
    _alt_28854 = _f_28853
    match t_1139:
        case BinaryTree_empty():
            _x_28856 = _alt_28841()
            return _x_28856
        case BinaryTree_node(a_28857, a_28858, a_28859):
            _x_28860 = _alt_28854(a_28857, a_28858, a_28859)
            return _x_28860

# Lean: Corpus.DataStructures.BinaryTree.height
def height(__1143: Any, t_1144: Any) -> int:
    def _f_28866():
        _x_28863 = 0
        return 0
    _alt_28867 = _f_28866
    def _f_28881(a_28868: Any, l_1146: Any, r_1147: Any):
        _x_28872 = 1
        _x_28876 = max
        _x_28877 = height(None, l_1146)
        _x_28878 = height(None, r_1147)
        _x_28879 = _x_28876(_x_28877, _x_28878)
        _x_28880 = 1 + _x_28879
        return _x_28880
    _alt_28882 = _f_28881
    match t_1144:
        case BinaryTree_empty():
            _x_28884 = _alt_28867()
            return _x_28884
        case BinaryTree_node(a_28885, a_28886, a_28887):
            _x_28888 = _alt_28882(a_28885, a_28886, a_28887)
            return _x_28888

# Lean: Corpus.DataStructures.BinaryTree.inorder
def inorder(__1148: Any, t_1149: Any) -> list[Any]:
    def _f_28892():
        _x_28891 = []
        return _x_28891
    _alt_28893 = _f_28892
    def _f_28903(v_1151: Any, l_1152: Any, r_1153: Any):
        _x_28897 = inorder(None, l_1152)
        _x_28898 = []
        _x_28899 = [v_1151] + _x_28898
        _x_28900 = _x_28897 + _x_28899
        _x_28901 = inorder(None, r_1153)
        _x_28902 = _x_28900 + _x_28901
        return _x_28902
    _alt_28904 = _f_28903
    match t_1149:
        case BinaryTree_empty():
            _x_28906 = _alt_28893()
            return _x_28906
        case BinaryTree_node(a_28907, a_28908, a_28909):
            _x_28910 = _alt_28904(a_28907, a_28908, a_28909)
            return _x_28910

# Lean: Corpus.DataStructures.BinaryTree.preorder
def preorder(__1154: Any, t_1155: Any) -> list[Any]:
    def _f_28914():
        _x_28913 = []
        return _x_28913
    _alt_28915 = _f_28914
    def _f_28925(v_1157: Any, l_1158: Any, r_1159: Any):
        _x_28919 = []
        _x_28920 = [v_1157] + _x_28919
        _x_28921 = preorder(None, l_1158)
        _x_28922 = _x_28920 + _x_28921
        _x_28923 = preorder(None, r_1159)
        _x_28924 = _x_28922 + _x_28923
        return _x_28924
    _alt_28926 = _f_28925
    match t_1155:
        case BinaryTree_empty():
            _x_28928 = _alt_28915()
            return _x_28928
        case BinaryTree_node(a_28929, a_28930, a_28931):
            _x_28932 = _alt_28926(a_28929, a_28930, a_28931)
            return _x_28932

# Lean: Corpus.DataStructures.BinaryTree.postorder
def postorder(__1160: Any, t_1161: Any) -> list[Any]:
    def _f_28936():
        _x_28935 = []
        return _x_28935
    _alt_28937 = _f_28936
    def _f_28947(v_1163: Any, l_1164: Any, r_1165: Any):
        _x_28941 = postorder(None, l_1164)
        _x_28942 = postorder(None, r_1165)
        _x_28943 = _x_28941 + _x_28942
        _x_28944 = []
        _x_28945 = [v_1163] + _x_28944
        _x_28946 = _x_28943 + _x_28945
        return _x_28946
    _alt_28948 = _f_28947
    match t_1161:
        case BinaryTree_empty():
            _x_28950 = _alt_28937()
            return _x_28950
        case BinaryTree_node(a_28951, a_28952, a_28953):
            _x_28954 = _alt_28948(a_28951, a_28952, a_28953)
            return _x_28954

# Lean: Corpus.DataStructures.BinaryTree.levelOrder
def level_order(__1166: Any, t_1167: Any) -> list[Any]:
    _x_28957 = []
    _x_28958 = [t_1167] + _x_28957
    _x_28959 = []
    _x_28960 = 10000
    _x_28963 = level_order_go(None, _x_28958, _x_28959, 10000)
    return _x_28963

# Lean: Corpus.DataStructures.BinaryTree.mirror
def mirror(__1168: Any, t_1169: Any) -> Any:
    def _f_28966():
        _x_28965 = BinaryTree_empty()
        return _x_28965
    _alt_28967 = _f_28966
    def _f_28971(v_1171: Any, l_1172: Any, r_1173: Any):
        _x_28968 = mirror(None, r_1173)
        _x_28969 = mirror(None, l_1172)
        _x_28970 = BinaryTree_node(v_1171, _x_28968, _x_28969)
        return _x_28970
    _alt_28972 = _f_28971
    match t_1169:
        case BinaryTree_empty():
            _x_28974 = _alt_28967()
            return _x_28974
        case BinaryTree_node(a_28975, a_28976, a_28977):
            _x_28978 = _alt_28972(a_28975, a_28976, a_28977)
            return _x_28978

# Lean: Corpus.DataStructures.BinaryTree.map
def binary_tree_map(__1174: Any, __1175: Any, f_1176: Callable[[Any], Any], t_1177: Any) -> Any:
    def _f_28982():
        _x_28981 = BinaryTree_empty()
        return _x_28981
    _alt_28983 = _f_28982
    def _f_28988(v_1179: Any, l_1180: Any, r_1181: Any):
        _x_28984 = f_1176(v_1179)
        _x_28985 = binary_tree_map(None, None, f_1176, l_1180)
        _x_28986 = binary_tree_map(None, None, f_1176, r_1181)
        _x_28987 = BinaryTree_node(_x_28984, _x_28985, _x_28986)
        return _x_28987
    _alt_28989 = _f_28988
    match t_1177:
        case BinaryTree_empty():
            _x_28991 = _alt_28983()
            return _x_28991
        case BinaryTree_node(a_28992, a_28993, a_28994):
            _x_28995 = _alt_28989(a_28992, a_28993, a_28994)
            return _x_28995

# Lean: Corpus.DataStructures.BinaryTree.fold
def binary_tree_fold(__1182: Any, __1183: Any, f_1184: Callable[[Any, Any], Any], init_1185: Any, t_1186: Any) -> Any:
    def _f_28998():
        return init_1185
    _alt_28999 = _f_28998
    def _f_29003(v_1188: Any, l_1189: Any, r_1190: Any):
        _x_29000 = binary_tree_fold(None, None, f_1184, init_1185, l_1189)
        _x_29001 = f_1184(_x_29000, v_1188)
        _x_29002 = binary_tree_fold(None, None, f_1184, _x_29001, r_1190)
        return _x_29002
    _alt_29004 = _f_29003
    match t_1186:
        case BinaryTree_empty():
            _x_29006 = _alt_28999()
            return _x_29006
        case BinaryTree_node(a_29007, a_29008, a_29009):
            _x_29010 = _alt_29004(a_29007, a_29008, a_29009)
            return _x_29010

# Lean: Corpus.DataStructures.AssocList.empty
def assoc_list_empty(__1191: Any, __1192: Any) -> list[tuple[Any, Any]]:
    _x_29013 = []
    return _x_29013

# Lean: Corpus.DataStructures.AssocList.insert
def assoc_list_insert(__1193: Any, __1194: Any, inst_29015: Any, m_1195: list[tuple[Any, Any]], k_1196: Any, v_1197: Any) -> list[tuple[Any, Any]]:
    _x_29016 = (k_1196, v_1197)
    def _f_29026(x_29017: tuple[Any, Any]):
        def _f_29020(k__1198: Any, snd_29018: Any):
            _x_29019 = (lambda a, b: a != b)(k_1196)
            return _x_29019
        _alt_29021 = _f_29020
        match x_29017:
            case (fst_29022, snd_29023):
                _x_29024 = _alt_29021(fst_29022, snd_29023)
                return _x_29024
    _x_29027 = [x for x in m_1195 if _f_29026(x)]
    _x_29028 = [_x_29016] + _x_29027
    return _x_29028

# Lean: Corpus.DataStructures.AssocList.lookup
def lookup(__1199: Any, __1200: Any, inst_29030: Any, m_1201: list[tuple[Any, Any]], k_1202: Any) -> Any | None:
    def _f_29032():
        _x_29031 = None
        return _x_29031
    _alt_29033 = _f_29032
    def _f_29043(k__1204: Any, v_1205: Any, rest_1206: list[tuple[Any, Any]]):
        _x_29034 = inst_29030.field_0
        _x_29035 = _x_29034(k_1202, k__1204)
        _x_29036 = True
        _x_29037 = _x_29035 == True
        if _x_29037:
            _x_29041 = v_1205
            return _x_29041
        else:
            _x_29039 = lookup(None, None, inst_29030, k_1202, rest_1206)
            return _x_29039
    _alt_29044 = _f_29043
    if len(m_1201) == 0:
        _x_29046 = _alt_29033()
        return _x_29046
    else:
        head_29047 = m_1201[0]
        tail_29048 = m_1201[1:]
        match head_29047:
            case (fst_29049, snd_29050):
                _x_29051 = _alt_29044(fst_29049, snd_29050, tail_29048)
                return _x_29051

# Lean: Corpus.DataStructures.AssocList.remove
def remove(__1207: Any, __1208: Any, inst_29055: Any, m_1209: list[tuple[Any, Any]], k_1210: Any) -> list[tuple[Any, Any]]:
    def _f_29065(x_29056: tuple[Any, Any]):
        def _f_29059(k__1211: Any, snd_29057: Any):
            _x_29058 = (lambda a, b: a != b)(k_1210)
            return _x_29058
        _alt_29060 = _f_29059
        match x_29056:
            case (fst_29061, snd_29062):
                _x_29063 = _alt_29060(fst_29061, snd_29062)
                return _x_29063
    _x_29066 = [x for x in m_1209 if _f_29065(x)]
    return _x_29066

# Lean: Corpus.DataStructures.AssocList.keys
def keys(__1212: Any, __1213: Any, m_1214: list[tuple[Any, Any]]) -> list[Any]:
    _x_29070 = [self[0] for self in m_1214]
    return _x_29070

# Lean: Corpus.DataStructures.AssocList.values
def values(__1215: Any, __1216: Any, m_1217: list[tuple[Any, Any]]) -> list[Any]:
    _x_29074 = [self_1218[1] for self_1218 in m_1217]
    return _x_29074

# Lean: Corpus.DataStructures.AssocList.size
def assoc_list_size(__1219: Any, __1220: Any, m_1221: list[tuple[Any, Any]]) -> int:
    _x_29076 = len(m_1221)
    return _x_29076

# Lean: Corpus.DataStructures.Graph.empty
def data_structures_graph_empty(__1222: Any) -> Any:
    _x_29078 = []
    _x_29079 = []
    _x_29080 = Graph_mk(_x_29078, _x_29079)
    return _x_29080

# Lean: Corpus.DataStructures.Graph.addVertex
def data_structures_graph_add_vertex(__1223: Any, inst_29082: Any, g_1224: Any, v_1225: Any) -> Any:
    _x_29083 = g_1224.field_0
    _x_29084 = v_1225 in _x_29083
    _x_29085 = True
    _x_29086 = _x_29084 == True
    if _x_29086:
        return g_1224
    else:
        _x_29088 = [v_1225] + _x_29083
        _x_29089 = g_1224.field_1
        _x_29090 = Graph_mk(_x_29088, _x_29089)
        return _x_29090

# Lean: Corpus.DataStructures.Graph.addEdge
def data_structures_graph_add_edge(__1226: Any, inst_29094: Any, g_1227: Any, u: Any, v_1228: Any) -> Any:
    _x_29095 = data_structures_graph_add_vertex(None, inst_29094, g_1227, u)
    _x_29096 = data_structures_graph_add_vertex(None, inst_29094, _x_29095, v_1228)
    _x_29097 = _x_29096.field_0
    _x_29098 = (u, v_1228)
    _x_29099 = _x_29096.field_1
    _x_29100 = [_x_29098] + _x_29099
    _x_29101 = Graph_mk(_x_29097, _x_29100)
    return _x_29101

# Lean: Corpus.DataStructures.Graph.neighbors
def data_structures_graph_neighbors(__1229: Any, inst_29103: Any, g_1230: Any, v_1231: Any) -> list[Any]:
    def _f_29126(x_29104: tuple[Any, Any]):
        def _f_29120(u_1232: Any, w_1233: Any):
            _x_29105 = inst_29103.field_0
            _x_29106 = _x_29105(u_1232, v_1231)
            _x_29107 = True
            _x_29108 = _x_29106 == True
            if _x_29108:
                _x_29118 = w_1233
                return _x_29118
            else:
                _x_29110 = _x_29105(w_1233, v_1231)
                _x_29111 = _x_29110 == True
                if _x_29111:
                    _x_29115 = u_1232
                    return _x_29115
                else:
                    _x_29113 = None
                    return _x_29113
        _alt_29121 = _f_29120
        match x_29104:
            case (fst_29122, snd_29123):
                _x_29124 = _alt_29121(fst_29122, snd_29123)
                return _x_29124
    _x_29127 = g_1230.field_1
    _x_29128 = [_y for x in _x_29127 if (_y := _f_29126(x)) is not None]
    return _x_29128

# Lean: Corpus.DataStructures.Graph.degree
def degree(__1234: Any, inst_29130: Any, g_1235: Any, v_1236: Any) -> int:
    _x_29131 = data_structures_graph_neighbors(None, inst_29130, g_1235, v_1236)
    _x_29132 = len(_x_29131)
    return _x_29132

# Lean: Corpus.DataStructures.Graph.hasEdge
def has_edge(__1237: Any, inst_29134: Any, g_1238: Any, u_1239: Any, v_1240: Any) -> bool:
    _x_29135 = g_1238.field_1
    def _f_29188(x_29136: tuple[Any, Any]):
        def _f_29182(a_1241: Any, b_1242: Any):
            def _f_29138():
                _x_29137 = True
                return True
            _alt_29139 = _f_29138
            def _f_29154():
                def _f_29141():
                    _x_29140 = False
                    return False
                _alt_29142 = _f_29141
                def _f_29145():
                    _x_29143 = inst_29134.field_0
                    _x_29144 = _x_29143(b_1242, u_1239)
                    return _x_29144
                _alt_29146 = _f_29145
                _x_29147 = inst_29134.field_0
                _x_29148 = _x_29147(a_1241, v_1240)
                if _x_29148:
                    _x_29152 = _alt_29146()
                    return _x_29152
                else:
                    _x_29150 = _alt_29142()
                    return _x_29150
            _alt_29155 = _f_29154
            def _f_29157():
                _x_29156 = False
                return False
            _alt_29158 = _f_29157
            def _f_29161():
                _x_29159 = inst_29134.field_0
                _x_29160 = _x_29159(b_1242, v_1240)
                return _x_29160
            _alt_29162 = _f_29161
            _x_29163 = inst_29134.field_0
            _x_29164 = _x_29163(a_1241, u_1239)
            def _jp_29175(_y_29169: bool):
                if _y_29169:
                    _x_29173 = _alt_29139()
                    return _x_29173
                else:
                    _x_29171 = _alt_29155()
                    return _x_29171
            def _jp_29178():
                _x_29177 = _alt_29158()
                return _jp_29175(_x_29177)
            def _jp_29181():
                _x_29180 = _alt_29162()
                return _jp_29175(_x_29180)
            if _x_29164:
                return _jp_29181()
            else:
                return _jp_29178()
        _alt_29183 = _f_29182
        match x_29136:
            case (fst_29184, snd_29185):
                _x_29186 = _alt_29183(fst_29184, snd_29185)
                return _x_29186
    _x_29189 = any(_f_29188(x) for x in _x_29135)
    return _x_29189

# Lean: Corpus.DataStructures.Trie.empty
def trie_empty() -> Trie:
    _x_29191 = False
    _x_29192 = []
    _x_29193 = Trie_node(False, _x_29192)
    return _x_29193

# Lean: Corpus.DataStructures.Trie.insert
def trie_insert(t_1249: Trie, s_1250: str) -> Trie:
    _x_29194 = list(s_1250)
    _x_29195 = trie_insert_go(t_1249, _x_29194)
    return _x_29195

# Lean: Corpus.DataStructures.Trie.contains
def trie_contains(t_1251: Trie, s_1252: str) -> bool:
    _x_29197 = list(s_1252)
    _x_29198 = trie_contains_go(t_1251, _x_29197)
    return _x_29198

# Lean: Corpus.DataStructures.Trie.hasPrefix
def has_prefix(t_1253: Trie, pfx_1254: str) -> bool:
    _x_29200 = list(pfx_1254)
    _x_29201 = has_prefix_go(t_1253, _x_29200)
    return _x_29201

# Lean: Corpus.Advanced.Heap.empty
def advanced_heap_empty(__1255: Any) -> Any:
    _x_29203 = []
    _x_29204 = Heap_mk(_x_29203)
    return _x_29204

# Lean: Corpus.Advanced.Heap.isEmpty
def advanced_heap_is_empty(__1256: Any, h_1257: Any) -> bool:
    _x_29206 = h_1257.field_0
    _x_29207 = len(_x_29206) == 0
    return _x_29207

# Lean: Corpus.Advanced.Heap.size
def advanced_heap_size(__1258: Any, h_1259: Any) -> int:
    _x_29209 = h_1259.field_0
    _x_29210 = len(_x_29209)
    return _x_29210

# Lean: Corpus.Advanced.parent
def parent(i_1260: int) -> int:
    _x_29218 = 1
    _x_29221 = i_1260 - 1
    _x_29222 = 2
    _x_29225 = _x_29221 // 2
    return _x_29225

# Lean: Corpus.Advanced.leftChild
def left_child(i_1261: int) -> int:
    _x_29233 = 2
    _x_29236 = 2 * i_1261
    _x_29237 = 1
    _x_29240 = _x_29236 + 1
    return _x_29240

# Lean: Corpus.Advanced.rightChild
def right_child(i_1262: int) -> int:
    _x_29248 = 2
    _x_29251 = 2 * i_1262
    _x_29252 = _x_29251 + 2
    return _x_29252

# Lean: Corpus.Advanced.swapAt
def swap_at(__1263: Any, xs_1264: list[Any], i_1265: int, j_1266: int) -> list[Any]:
    def _f_29256(a_1267: Any, b_1268: Any):
        _x_29254 = set_tr(None, xs_1264, i_1265, b_1268)
        _x_29255 = set_tr(None, _x_29254, j_1266, a_1267)
        return _x_29255
    _alt_29257 = _f_29256
    def _f_29260(x_29258: Any | None, x_29259: Any | None):
        return xs_1264
    _alt_29261 = _f_29260
    _x_29263 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_29264 = _x_29263(xs_1264, i_1265)
    if _x_29264 is None:
        _x_29279 = (lambda h_29275: _alt_29261(_x_29264, _x_29263(xs_1264, j_1266)))(None)
        return _x_29279
    else:
        val_29265 = _x_29264
        _x_29266 = _x_29263(xs_1264, j_1266)
        if _x_29266 is None:
            def _f_29272(h_29269: Any):
                _x_29270 = val_29265
                _x_29271 = _alt_29261(_x_29270, _x_29266)
                return _x_29271
            _x_29273 = _f_29272(None)
            return _x_29273
        else:
            val_29267 = _x_29266
            _x_29268 = _alt_29257(val_29265, val_29267)
            return _x_29268

# Lean: Corpus.Advanced.siftUp
def sift_up(__1269: Any, inst_29282: Any, xs_1270: list[Any], i_1271: int) -> list[Any]:
    while True:
        _x_29286 = 0
        _x_29289 = i_1271 == 0
        _x_29290 = True
        _x_29291 = _x_29289 == True
        if _x_29291:
            return xs_1270
        else:
            _x_29293 = parent(i_1271)
            def _f_29311(x_29309: Any | None, x_29310: Any | None):
                return xs_1270
            _alt_29312 = _f_29311
            _x_29314 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_29315 = _x_29314(xs_1270, i_1271)
            if _x_29315 is None:
                _x_29330 = (lambda h_29326: _alt_29312(_x_29315, _x_29314(xs_1270, _x_29293)))(None)
                return _x_29330
            else:
                val_29316 = _x_29315
                _x_29317 = _x_29314(xs_1270, _x_29293)
                if _x_29317 is None:
                    def _f_29323(h_29320: Any):
                        _x_29321 = val_29316
                        _x_29322 = _alt_29312(_x_29321, _x_29317)
                        return _x_29322
                    _x_29324 = _f_29323(None)
                    return _x_29324
                else:
                    val_29318 = _x_29317
                    vi_1273 = val_29316
                    vp = val_29318
                    _x_29297 = inst_29282.field_0
                    _x_29298 = _x_29297(vi_1273, vp)
                    _x_29299 = -1
                    _x_29300 = _x_29298 == _x_29299
                    _x_29301 = _x_29300 == True
                    if _x_29301:
                        _x_29304 = swap_at(None, xs_1270, i_1271, _x_29293)
                        return sift_up(None, inst_29282, _x_29304, _x_29293)
                    else:
                        return xs_1270

# Lean: Corpus.Advanced.siftDown
def sift_down(__1274: Any, inst_29335: Any, xs_1275: list[Any], i_1276: int) -> list[Any]:
    _x_29336 = len(xs_1275)
    _x_29337 = left_child(i_1276)
    _x_29338 = right_child(i_1276)
    _x_29339 = _x_29336 <= _x_29337
    if _x_29339:
        return xs_1275
    else:
        _x_29341 = _x_29336 <= _x_29338
        def _jp_29421(_y_29381: int):
            def _f_29396(vi_1280: Any, vs_1281: Any):
                _x_29385 = inst_29335.field_0
                _x_29386 = _x_29385(vs_1281, vi_1280)
                _x_29387 = -1
                _x_29388 = _x_29386 == _x_29387
                _x_29389 = True
                _x_29390 = _x_29388 == True
                if _x_29390:
                    _x_29393 = swap_at(None, xs_1275, i_1276, _y_29381)
                    _x_29394 = sift_down(None, inst_29335, _x_29393, _y_29381)
                    return _x_29394
                else:
                    return xs_1275
            _alt_29397 = _f_29396
            def _f_29400(x_29398: Any | None, x_29399: Any | None):
                return xs_1275
            _alt_29401 = _f_29400
            _x_29403 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_29404 = _x_29403(xs_1275, i_1276)
            if _x_29404 is None:
                _x_29419 = (lambda h_29415: _alt_29401(_x_29404, _x_29403(xs_1275, _y_29381)))(None)
                return _x_29419
            else:
                val_29405 = _x_29404
                _x_29406 = _x_29403(xs_1275, _y_29381)
                if _x_29406 is None:
                    def _f_29412(h_29409: Any):
                        _x_29410 = val_29405
                        _x_29411 = _alt_29401(_x_29410, _x_29406)
                        return _x_29411
                    _x_29413 = _f_29412(None)
                    return _x_29413
                else:
                    val_29407 = _x_29406
                    _x_29408 = _alt_29397(val_29405, val_29407)
                    return _x_29408
        if _x_29341:
            return _jp_29421(_x_29337)
        else:
            def _f_29355(vl: Any, vr: Any):
                _x_29346 = inst_29335.field_0
                _x_29347 = _x_29346(vl, vr)
                _x_29348 = -1
                _x_29349 = _x_29347 == _x_29348
                _x_29350 = True
                _x_29351 = _x_29349 == True
                if _x_29351:
                    return _x_29337
                else:
                    return _x_29338
            _alt_29356 = _f_29355
            def _jp_29425(_y_29422: Any, _y_29423: Any):
                _x_29424 = _alt_29356(_y_29422, _y_29423)
                return _jp_29421(_x_29424)
            def _f_29359(x_29357: Any | None, x_29358: Any | None):
                return _x_29337
            _alt_29360 = _f_29359
            _x_29362 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_29363 = _x_29362(xs_1275, _x_29337)
            if _x_29363 is None:
                _x_29378 = (lambda h_29374: _alt_29360(_x_29363, _x_29362(xs_1275, _x_29338)))(None)
                return _jp_29421(_x_29378)
            else:
                val_29364 = _x_29363
                _x_29365 = _x_29362(xs_1275, _x_29338)
                if _x_29365 is None:
                    def _f_29371(h_29368: Any):
                        _x_29369 = val_29364
                        _x_29370 = _alt_29360(_x_29369, _x_29365)
                        return _x_29370
                    _x_29372 = _f_29371(None)
                    return _jp_29421(_x_29372)
                else:
                    val_29366 = _x_29365
                    return _jp_29425(val_29364, val_29366)

# Lean: Corpus.Advanced.Heap.insert
def advanced_heap_insert(__1282: Any, inst_29429: Any, h_1283: Any, x_1284: Any) -> Any:
    _x_29433 = h_1283.field_0
    _x_29434 = []
    _x_29435 = [x_1284] + _x_29434
    _x_29436 = _x_29433 + _x_29435
    _x_29440 = len(_x_29436)
    _x_29441 = 1
    _x_29444 = _x_29440 - 1
    _x_29445 = sift_up(None, inst_29429, _x_29436, _x_29444)
    _x_29446 = Heap_mk(_x_29445)
    return _x_29446

# Lean: Corpus.Advanced.Heap.min
def advanced_heap_min(__1285: Any, h_1286: Any) -> Any | None:
    _x_29448 = h_1286.field_0
    _x_29449 = (lambda xs: xs[0] if xs else None)(_x_29448)
    return _x_29449

# Lean: Corpus.Advanced.Heap.popMin
def pop_min(__1287: Any, inst_29451: Any, h_1288: Any) -> Any:
    def _f_29452():
        return h_1288
    _alt_29453 = _f_29452
    def _f_29457(head_29454: Any):
        _x_29455 = []
        _x_29456 = Heap_mk(_x_29455)
        return _x_29456
    _alt_29458 = _f_29457
    def _f_29479(head_29459: Any, rest_1290: list[Any]):
        def _f_29462():
            _x_29460 = []
            _x_29461 = Heap_mk(_x_29460)
            return _x_29461
        _alt_29463 = _f_29462
        def _f_29471(last: Any):
            _x_29464 = drop_last_tr(None, rest_1290)
            _x_29465 = [last] + _x_29464
            _x_29466 = 0
            _x_29469 = sift_down(None, inst_29451, _x_29465, 0)
            _x_29470 = Heap_mk(_x_29469)
            return _x_29470
        _alt_29472 = _f_29471
        _x_29473 = (lambda xs: xs[-1] if xs else None)(rest_1290)
        if _x_29473 is None:
            _x_29475 = _alt_29463()
            return _x_29475
        else:
            val_29476 = _x_29473
            _x_29477 = _alt_29472(val_29476)
            return _x_29477
    _alt_29480 = _f_29479
    _x_29481 = h_1288.field_0
    if len(_x_29481) == 0:
        _x_29483 = _alt_29453()
        return _x_29483
    else:
        head_29484 = _x_29481[0]
        tail_29485 = _x_29481[1:]
        if len(tail_29485) == 0:
            _x_29486 = _alt_29458(head_29484)
            return _x_29486
        else:
            _x_29490 = (lambda h_29487: _alt_29480(head_29484, tail_29485))(None)
            return _x_29490

# Lean: Corpus.Advanced.Heap.ofList
def of_list(__1292: Any, inst_29494: Any, xs_1293: list[Any]) -> Any:
    def _f_29498(x1_29495: Any, x2_29496: Any):
        _x_29497 = advanced_heap_insert(None, inst_29494, x1_29495, x2_29496)
        return _x_29497
    _x_29499 = advanced_heap_empty(None)
    _x_29500 = functools.reduce(_f_29498, xs_1293, _x_29499)
    return _x_29500

# Lean: Corpus.Advanced.heapSort
def heap_sort(__1294: Any, inst_29502: Any, xs_1295: list[Any]) -> list[Any]:
    _x_29503 = of_list(None, inst_29502, xs_1295)
    _x_29504 = []
    _x_29508 = len(xs_1295)
    _x_29509 = 1
    _x_29512 = _x_29508 + 1
    _x_29513 = extract(None, inst_29502, _x_29503, _x_29504, _x_29512)
    return _x_29513

# Lean: Corpus.Advanced.UnionFind.empty
def advanced_union_find_empty() -> UnionFind:
    _x_29515 = []
    _x_29516 = UnionFind_mk(_x_29515, _x_29515)
    return _x_29516

# Lean: Corpus.Advanced.UnionFind.size
def advanced_union_find_size(uf: UnionFind) -> int:
    _x_29517 = uf.field_0
    _x_29518 = len(_x_29517)
    return _x_29518

# Lean: Corpus.Advanced.UnionFind.push
def advanced_union_find_push(uf_1296: UnionFind) -> UnionFind:
    _x_29520 = uf_1296.field_0
    _x_29521 = len(_x_29520)
    _x_29525 = []
    _x_29526 = [_x_29521] + _x_29525
    _x_29527 = _x_29520 + _x_29526
    _x_29528 = uf_1296.field_1
    _x_29529 = 0
    _x_29532 = [0] + _x_29525
    _x_29533 = _x_29528 + _x_29532
    _x_29534 = UnionFind_mk(_x_29527, _x_29533)
    return _x_29534

# Lean: Corpus.Advanced.UnionFind.ofSize
def of_size(n_1298: int) -> UnionFind:
    _x_29536 = list(range(n_1298))
    _x_29537 = 0
    _x_29540 = replicate_tr(None, n_1298, 0)
    _x_29541 = UnionFind_mk(_x_29536, _x_29540)
    return _x_29541

# Lean: Corpus.Advanced.UnionFind.root
def root(uf_1299: UnionFind, i_1300: int) -> int:
    while True:
        def _f_29543():
            return i_1300
        _alt_29544 = _f_29543
        _x_29558 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_29559 = uf_1299.field_0
        _x_29560 = _x_29558(_x_29559, i_1300)
        if _x_29560 is None:
            _x_29562 = _alt_29544()
            return _x_29562
        else:
            val_29563 = _x_29560
            p_1302 = val_29563
            _x_29548 = p_1302 == i_1300
            _x_29549 = True
            _x_29550 = _x_29548 == True
            if _x_29550:
                return i_1300
            else:
                uf_1299, i_1300 = uf_1299, p_1302
                continue

# Lean: Corpus.Advanced.UnionFind.equiv
def equiv(uf_1303: UnionFind, i_1304: int, j_1305: int) -> bool:
    _x_29570 = root(uf_1303, i_1304)
    _x_29571 = root(uf_1303, j_1305)
    _x_29572 = _x_29570 == _x_29571
    return _x_29572

# Lean: Corpus.Advanced.UnionFind.union
def union(uf_1306: UnionFind, i_1307: int, j_1308: int) -> UnionFind:
    _x_29574 = root(uf_1306, i_1307)
    _x_29575 = root(uf_1306, j_1308)
    _x_29579 = _x_29574 == _x_29575
    _x_29580 = True
    _x_29581 = _x_29579 == True
    if _x_29581:
        return uf_1306
    else:
        def _f_29611(ranki: int, rankj: int):
            _x_29583 = ranki < rankj
            if _x_29583:
                _x_29606 = uf_1306.field_0
                _x_29607 = set_tr(None, _x_29606, _x_29574, _x_29575)
                _x_29608 = uf_1306.field_1
                _x_29609 = UnionFind_mk(_x_29607, _x_29608)
                return _x_29609
            else:
                _x_29585 = rankj < ranki
                if _x_29585:
                    _x_29600 = uf_1306.field_0
                    _x_29601 = set_tr(None, _x_29600, _x_29575, _x_29574)
                    _x_29602 = uf_1306.field_1
                    _x_29603 = UnionFind_mk(_x_29601, _x_29602)
                    return _x_29603
                else:
                    _x_29587 = uf_1306.field_0
                    _x_29588 = set_tr(None, _x_29587, _x_29575, _x_29574)
                    _x_29589 = uf_1306.field_1
                    _x_29593 = 1
                    _x_29596 = ranki + 1
                    _x_29597 = set_tr(None, _x_29589, _x_29574, _x_29596)
                    _x_29598 = UnionFind_mk(_x_29588, _x_29597)
                    return _x_29598
        _alt_29612 = _f_29611
        def _f_29615(x_29613: int | None, x_29614: int | None):
            return uf_1306
        _alt_29616 = _f_29615
        _x_29618 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_29619 = uf_1306.field_1
        _x_29620 = _x_29618(_x_29619, _x_29574)
        if _x_29620 is None:
            _x_29635 = (lambda h_29631: _alt_29616(_x_29620, _x_29618(_x_29619, _x_29575)))(None)
            return _x_29635
        else:
            val_29621 = _x_29620
            _x_29622 = _x_29618(_x_29619, _x_29575)
            if _x_29622 is None:
                def _f_29628(h_29625: Any):
                    _x_29626 = val_29621
                    _x_29627 = _alt_29616(_x_29626, _x_29622)
                    return _x_29627
                _x_29629 = _f_29628(None)
                return _x_29629
            else:
                val_29623 = _x_29622
                _x_29624 = _alt_29612(val_29621, val_29623)
                return _x_29624

# Lean: Corpus.Advanced.UnionFind.numSets
def num_sets(uf_1309: UnionFind) -> int:
    def _f_29645(i_1310: int):
        _x_29643 = root(uf_1309, i_1310)
        _x_29644 = _x_29643 == i_1310
        return _x_29644
    _x_29646 = advanced_union_find_size(uf_1309)
    _x_29647 = list(range(_x_29646))
    _x_29648 = [x for x in _x_29647 if _f_29645(x)]
    _x_29649 = len(_x_29648)
    return _x_29649

# Lean: Corpus.Advanced.Graph.empty
def advanced_graph_empty() -> Graph:
    _x_29651 = 0
    _x_29654 = []
    _x_29655 = Graph_mk(0, _x_29654)
    return _x_29655

# Lean: Corpus.Advanced.Graph.addVertex
def advanced_graph_add_vertex(g_1311: Graph) -> Graph:
    _x_29659 = g_1311.field_0
    _x_29660 = 1
    _x_29663 = _x_29659 + 1
    _x_29664 = g_1311.field_1
    _x_29665 = Graph_mk(_x_29663, _x_29664)
    return _x_29665

# Lean: Corpus.Advanced.Graph.addEdge
def advanced_graph_add_edge(g_1312: Graph, u_1313: int, v_1314: int) -> Graph:
    _x_29667 = g_1312.field_0
    _x_29668 = (u_1313, v_1314)
    _x_29669 = g_1312.field_1
    _x_29670 = [_x_29668] + _x_29669
    _x_29671 = Graph_mk(_x_29667, _x_29670)
    return _x_29671

# Lean: Corpus.Advanced.Graph.neighbors
def advanced_graph_neighbors(g_1315: Graph, v_1316: int) -> list[int]:
    def _f_29697(x_29673: tuple[int, int]):
        def _f_29691(u_1317: int, w_1318: int):
            _x_29677 = u_1317 == v_1316
            _x_29678 = True
            _x_29679 = _x_29677 == True
            if _x_29679:
                _x_29689 = w_1318
                return _x_29689
            else:
                _x_29681 = w_1318 == v_1316
                _x_29682 = _x_29681 == True
                if _x_29682:
                    _x_29686 = u_1317
                    return _x_29686
                else:
                    _x_29684 = None
                    return _x_29684
        _alt_29692 = _f_29691
        match x_29673:
            case (fst_29693, snd_29694):
                _x_29695 = _alt_29692(fst_29693, snd_29694)
                return _x_29695
    _x_29698 = g_1315.field_1
    _x_29699 = [_y for x in _x_29698 if (_y := _f_29697(x)) is not None]
    return _x_29699

# Lean: Corpus.Advanced.Graph.bfs
def bfs(g_1319: Graph, start_1320: int) -> list[int]:
    _x_29701 = []
    _x_29702 = [start_1320] + _x_29701
    _x_29706 = g_1319.field_0
    _x_29707 = g_1319.field_1
    _x_29708 = len(_x_29707)
    _x_29709 = _x_29706 + _x_29708
    _x_29710 = 1
    _x_29713 = _x_29709 + 1
    _x_29714 = bfs_loop(g_1319, _x_29702, _x_29701, _x_29713)
    return _x_29714

# Lean: Corpus.Advanced.Graph.dfs
def dfs(g_1321: Graph, start_1322: int) -> list[int]:
    _x_29716 = []
    _x_29717 = [start_1322] + _x_29716
    _x_29721 = g_1321.field_0
    _x_29722 = g_1321.field_1
    _x_29723 = len(_x_29722)
    _x_29724 = _x_29721 + _x_29723
    _x_29725 = 1
    _x_29728 = _x_29724 + 1
    _x_29729 = dfs_loop(g_1321, _x_29717, _x_29716, _x_29728)
    return _x_29729

# Lean: Corpus.Advanced.Graph.isConnected
def is_connected(g_1323: Graph) -> bool:
    _x_29734 = g_1323.field_0
    _x_29735 = 0
    _x_29738 = _x_29734 == 0
    _x_29739 = True
    _x_29740 = _x_29738 == True
    if _x_29740:
        _x_29746 = True
        return True
    else:
        _x_29742 = bfs(g_1323, 0)
        _x_29743 = len(_x_29742)
        _x_29744 = _x_29743 == _x_29734
        return _x_29744

# Lean: Corpus.Advanced.Graph.topoSort
def topo_sort(g_1325: Graph) -> list[int] | None:
    def _f_29759(v_1326: int):
        _x_29756 = g_1325.field_1
        _x_29757 = [x_29749 for x_29749 in _x_29756 if (x_29749[1] == v_1326)]
        _x_29758 = len(_x_29757)
        return _x_29758
    _x_29760 = g_1325.field_0
    _x_29761 = list(range(_x_29760))
    _x_29762 = [_f_29759(x) for x in _x_29761]
    def _f_29786(v_1327: int):
        _alt_29764 = (lambda x_1328: x_1328)
        def _f_29766():
            _x_29765 = False
            return False
        _alt_29767 = _f_29766
        _x_29778 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_29779 = _x_29778(_x_29762, v_1327)
        _x_29780 = option_map(None, None, (lambda x_29768: (x_29768 == 0)), _x_29779)
        if _x_29780 is None:
            _x_29782 = _alt_29767()
            return _x_29782
        else:
            val_29783 = _x_29780
            _x_29784 = _alt_29764(val_29783)
            return _x_29784
    _x_29787 = [x for x in _x_29761 if _f_29786(x)]
    _x_29788 = []
    _x_29792 = 1
    _x_29795 = _x_29760 + 1
    _x_29796 = topo_sort_loop(g_1325, _x_29787, _x_29762, _x_29788, _x_29795)
    return _x_29796

# Lean: Corpus.Advanced.Graph.hasCycle
def has_cycle(g_1330: Graph) -> bool:
    _x_29798 = topo_sort(g_1330)
    _x_29799 = (lambda x: x is None)(_x_29798)
    return _x_29799

# Lean: Corpus.Advanced.Matrix.get
def advanced_matrix_get(m_1331: list[list[int]], i_1332: int, j_1333: int) -> int | None:
    def _f_29802():
        _x_29801 = None
        return _x_29801
    _alt_29803 = _f_29802
    def _f_29807(row_1335: list[int]):
        _x_29805 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_29806 = _x_29805(row_1335, j_1333)
        return _x_29806
    _alt_29808 = _f_29807
    _x_29810 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_29811 = _x_29810(m_1331, i_1332)
    if _x_29811 is None:
        _x_29813 = _alt_29803()
        return _x_29813
    else:
        val_29814 = _x_29811
        _x_29815 = _alt_29808(val_29814)
        return _x_29815

# Lean: Corpus.Advanced.Matrix.set
def advanced_matrix_set(m_1336: list[list[int]], i_1337: int, j_1338: int, v_1339: int) -> list[list[int]]:
    def _f_29852(x_29818: tuple[list[int], int]):
        def _f_29846(row_1340: list[int], idx_1341: int):
            _x_29822 = idx_1341 == i_1337
            _x_29823 = True
            _x_29824 = _x_29822 == True
            if _x_29824:
                def _f_29839(x_29827: tuple[int, int]):
                    def _f_29833(val_1342: int, jdx: int):
                        _x_29828 = jdx == j_1338
                        _x_29829 = _x_29828 == True
                        if _x_29829:
                            return v_1339
                        else:
                            return val_1342
                    _alt_29834 = _f_29833
                    match x_29827:
                        case (fst_29835, snd_29836):
                            _x_29837 = _alt_29834(fst_29835, snd_29836)
                            return _x_29837
                _x_29840 = 0
                _x_29843 = zip_idx_tr(None, row_1340, 0)
                _x_29844 = [_f_29839(x) for x in _x_29843]
                return _x_29844
            else:
                return row_1340
        _alt_29847 = _f_29846
        match x_29818:
            case (fst_29848, snd_29849):
                _x_29850 = _alt_29847(fst_29848, snd_29849)
                return _x_29850
    _x_29853 = 0
    _x_29856 = zip_idx_tr(None, m_1336, 0)
    _x_29857 = [_f_29852(x) for x in _x_29856]
    return _x_29857

# Lean: Corpus.Advanced.Matrix.create
def advanced_matrix_create(n_1343: int, fill: int) -> list[list[int]]:
    _x_29859 = replicate_tr(None, n_1343, fill)
    _x_29860 = replicate_tr(None, n_1343, _x_29859)
    return _x_29860

# Lean: Corpus.Advanced.floydWarshall
def floyd_warshall(n_1344: int, edges: list[tuple[int, tuple[int, int]]]) -> list[list[int]]:
    _x_29862 = 1000000000
    _x_29865 = advanced_matrix_create(n_1344, 1000000000)
    def _f_29870(m_1347: list[list[int]], i_1348: int):
        _x_29866 = 0
        _x_29869 = advanced_matrix_set(m_1347, i_1348, i_1348, 0)
        return _x_29869
    _x_29871 = list(range(n_1344))
    _x_29872 = functools.reduce(_f_29870, _x_29871, _x_29865)
    def _f_29884(m_1349: list[list[int]], x_29873: tuple[int, tuple[int, int]]):
        def _f_29875(u_1350: int, v_1351: int, w_1352: int):
            _x_29874 = advanced_matrix_set(m_1349, u_1350, v_1351, w_1352)
            return _x_29874
        _alt_29876 = _f_29875
        match x_29873:
            case (fst_29877, snd_29878):
                match snd_29878:
                    case (fst_29879, snd_29880):
                        _x_29881 = _alt_29876(fst_29877, fst_29879, snd_29880)
                        return _x_29881
    _x_29885 = functools.reduce(_f_29884, edges, _x_29872)
    def _f_29934(dist: list[list[int]], k_1353: int):
        def _f_29932(d_1354: list[list[int]], i_1355: int):
            def _f_29930(d_: list[list[int]], j_1356: int):
                def _f_29895(dik: int, dkj: int, dij: int):
                    _x_29889 = dik + dkj
                    _x_29890 = _x_29889 < dij
                    if _x_29890:
                        _x_29893 = advanced_matrix_set(d_, i_1355, j_1356, _x_29889)
                        return _x_29893
                    else:
                        return d_
                _alt_29896 = _f_29895
                def _f_29900(x_29897: int | None, x_29898: int | None, x_29899: int | None):
                    return d_
                _alt_29901 = _f_29900
                _x_29902 = advanced_matrix_get(d_, i_1355, k_1353)
                if _x_29902 is None:
                    def _f_29927(h_29923: Any):
                        _x_29924 = advanced_matrix_get(d_, k_1353, j_1356)
                        _x_29925 = advanced_matrix_get(d_, i_1355, j_1356)
                        _x_29926 = _alt_29901(_x_29902, _x_29924, _x_29925)
                        return _x_29926
                    _x_29928 = _f_29927(None)
                    return _x_29928
                else:
                    val_29903 = _x_29902
                    _x_29904 = advanced_matrix_get(d_, k_1353, j_1356)
                    if _x_29904 is None:
                        def _f_29920(h_29916: Any):
                            _x_29917 = val_29903
                            _x_29918 = advanced_matrix_get(d_, i_1355, j_1356)
                            _x_29919 = _alt_29901(_x_29917, _x_29904, _x_29918)
                            return _x_29919
                        _x_29921 = _f_29920(None)
                        return _x_29921
                    else:
                        val_29905 = _x_29904
                        _x_29906 = advanced_matrix_get(d_, i_1355, j_1356)
                        if _x_29906 is None:
                            def _f_29913(h_29909: Any):
                                _x_29910 = val_29903
                                _x_29911 = val_29905
                                _x_29912 = _alt_29901(_x_29910, _x_29911, _x_29906)
                                return _x_29912
                            _x_29914 = _f_29913(None)
                            return _x_29914
                        else:
                            val_29907 = _x_29906
                            _x_29908 = _alt_29896(val_29903, val_29905, val_29907)
                            return _x_29908
            _x_29931 = functools.reduce(_f_29930, _x_29871, d_1354)
            return _x_29931
        _x_29933 = functools.reduce(_f_29932, _x_29871, dist)
        return _x_29933
    _x_29935 = functools.reduce(_f_29934, _x_29871, _x_29885)
    return _x_29935

# Lean: Corpus.NumberTheory.extGcd
def ext_gcd(a_1357: int, b_1358: int) -> tuple[int, tuple[int, int]]:
    _x_29940 = 0
    _x_29943 = b_1358 == 0
    _x_29944 = True
    _x_29945 = _x_29943 == True
    if _x_29945:
        _x_29979 = 1
        _x_29984 = (1, a_1357)
        _x_29985 = (1, _x_29984)
        return _x_29985
    else:
        def _f_29964(x_1359: int, y_1360: int, g_1361: int):
            _x_29957 = cast(None, _x_29956, a_1357)
            _x_29958 = cast(None, _x_29956, b_1358)
            _x_29959 = _x_29957 // _x_29958
            _x_29960 = _x_29959 * y_1360
            _x_29961 = x_1359 - _x_29960
            _x_29962 = (_x_29961, g_1361)
            _x_29963 = (y_1360, _x_29962)
            return _x_29963
        _alt_29965 = _f_29964
        _x_29969 = a_1357 % b_1358
        _x_29970 = ext_gcd(b_1358, _x_29969)
        match _x_29970:
            case (fst_29971, snd_29972):
                match snd_29972:
                    case (fst_29973, snd_29974):
                        _x_29975 = _alt_29965(fst_29971, fst_29973, snd_29974)
                        return _x_29975

# Lean: Corpus.NumberTheory.modInverse
def mod_inverse(a_1362: int, m_1363: int) -> int | None:
    def _f_30015(x_1364: int, fst_29988: int, g_1365: int):
        _x_29992 = 1
        _x_29995 = g_1365 == 1
        _x_29996 = True
        _x_29997 = _x_29995 == True
        if _x_29997:
            _x_30008 = cast(None, _x_30007, m_1363)
            _x_30009 = x_1364 % _x_30008
            _x_30010 = _x_30009 + _x_30008
            _x_30011 = _x_30010 % _x_30008
            _x_30012 = to_nat(_x_30011)
            _x_30013 = _x_30012
            return _x_30013
        else:
            _x_29999 = None
            return _x_29999
    _alt_30016 = _f_30015
    _x_30017 = ext_gcd(a_1362, m_1363)
    match _x_30017:
        case (fst_30018, snd_30019):
            match snd_30019:
                case (fst_30020, snd_30021):
                    _x_30022 = _alt_30016(fst_30018, fst_30020, snd_30021)
                    return _x_30022

# Lean: Corpus.NumberTheory.totient
def totient(n_1366: int) -> int:
    _x_30026 = 1
    _x_30029 = n_1366 <= 1
    if _x_30029:
        return n_1366
    else:
        _x_30031 = 0
        _x_30034 = count(n_1366, 1, 0)
        return _x_30034

# Lean: Corpus.NumberTheory.isPerfect
def is_perfect(n_1367: int) -> bool:
    _x_30038 = 2
    _x_30041 = n_1367 < 2
    if _x_30041:
        _x_30096 = False
        return False
    else:
        def _f_30085(acc_1368: int, i_1369: int):
            def _f_30044():
                _x_30043 = False
                return False
            _alt_30045 = _f_30044
            def _f_30057():
                _x_30052 = n_1367 % i_1369
                _x_30053 = 0
                _x_30056 = _x_30052 == 0
                return _x_30056
            _alt_30058 = _f_30057
            _x_30059 = 0
            _x_30062 = 0 < i_1369
            def _jp_30078(_y_30068: bool):
                _x_30069 = True
                _x_30070 = _y_30068 == True
                if _x_30070:
                    _x_30076 = acc_1368 + i_1369
                    return _x_30076
                else:
                    return acc_1368
            def _jp_30081():
                _x_30080 = _alt_30045()
                return _jp_30078(_x_30080)
            def _jp_30084():
                _x_30083 = _alt_30058()
                return _jp_30078(_x_30083)
            if _x_30062:
                return _jp_30084()
            else:
                return _jp_30081()
        _x_30086 = 0
        _x_30089 = list(range(n_1367))
        _x_30090 = functools.reduce(_f_30085, _x_30089, 0)
        _x_30094 = _x_30090 == n_1367
        return _x_30094

# Lean: Corpus.NumberTheory.isAbundant
def is_abundant(n_1372: int) -> bool:
    _x_30099 = 2
    _x_30102 = n_1372 < 2
    if _x_30102:
        _x_30155 = False
        return False
    else:
        def _f_30146(acc_1373: int, i_1374: int):
            def _f_30105():
                _x_30104 = False
                return False
            _alt_30106 = _f_30105
            def _f_30118():
                _x_30113 = n_1372 % i_1374
                _x_30114 = 0
                _x_30117 = _x_30113 == 0
                return _x_30117
            _alt_30119 = _f_30118
            _x_30120 = 0
            _x_30123 = 0 < i_1374
            def _jp_30139(_y_30129: bool):
                _x_30130 = True
                _x_30131 = _y_30129 == True
                if _x_30131:
                    _x_30137 = acc_1373 + i_1374
                    return _x_30137
                else:
                    return acc_1373
            def _jp_30142():
                _x_30141 = _alt_30106()
                return _jp_30139(_x_30141)
            def _jp_30145():
                _x_30144 = _alt_30119()
                return _jp_30139(_x_30144)
            if _x_30123:
                return _jp_30145()
            else:
                return _jp_30142()
        _x_30147 = 0
        _x_30150 = list(range(n_1372))
        _x_30151 = functools.reduce(_f_30146, _x_30150, 0)
        _x_30152 = n_1372 < _x_30151
        return _x_30152

# Lean: Corpus.NumberTheory.isDeficient
def is_deficient(n_1378: int) -> bool:
    _x_30158 = 1
    _x_30161 = n_1378 < 1
    if _x_30161:
        _x_30214 = False
        return False
    else:
        def _f_30205(acc_1379: int, i_1380: int):
            def _f_30164():
                _x_30163 = False
                return False
            _alt_30165 = _f_30164
            def _f_30177():
                _x_30172 = n_1378 % i_1380
                _x_30173 = 0
                _x_30176 = _x_30172 == 0
                return _x_30176
            _alt_30178 = _f_30177
            _x_30179 = 0
            _x_30182 = 0 < i_1380
            def _jp_30198(_y_30188: bool):
                _x_30189 = True
                _x_30190 = _y_30188 == True
                if _x_30190:
                    _x_30196 = acc_1379 + i_1380
                    return _x_30196
                else:
                    return acc_1379
            def _jp_30204():
                _x_30203 = _alt_30178()
                return _jp_30198(_x_30203)
            def _jp_30201():
                _x_30200 = _alt_30165()
                return _jp_30198(_x_30200)
            if _x_30182:
                return _jp_30204()
            else:
                return _jp_30201()
        _x_30206 = 0
        _x_30209 = list(range(n_1378))
        _x_30210 = functools.reduce(_f_30205, _x_30209, 0)
        _x_30211 = _x_30210 < n_1378
        return _x_30211

# Lean: Corpus.NumberTheory.collatzLength
def collatz_length(n_1384: int) -> int:
    _x_30217 = 1
    _x_30220 = n_1384 <= 1
    if _x_30220:
        _x_30260 = 0
        return 0
    else:
        _x_30231 = 2
        _x_30234 = n_1384 % 2
        _x_30235 = 0
        _x_30238 = _x_30234 == 0
        _x_30239 = True
        _x_30240 = _x_30238 == True
        def _jp_30258(_y_30255: int):
            _x_30256 = collatz_length(_y_30255)
            _x_30257 = 1 + _x_30256
            return _x_30257
        if _x_30240:
            _x_30254 = n_1384 // 2
            return _jp_30258(_x_30254)
        else:
            _x_30245 = 3
            _x_30248 = 3 * n_1384
            _x_30249 = _x_30248 + 1
            return _jp_30258(_x_30249)

# Lean: Corpus.NumberTheory.isqrt
def isqrt(n_1385: int) -> int:
    _x_30268 = 0
    _x_30271 = n_1385 == 0
    _x_30272 = True
    _x_30273 = _x_30271 == True
    if _x_30273:
        return 0
    else:
        _x_30275 = isqrt_go(n_1385, n_1385, n_1385)
        return _x_30275

# Lean: Corpus.NumberTheory.isPerfectSquare
def is_perfect_square(n_1386: int) -> bool:
    _x_30280 = isqrt(n_1386)
    _x_30287 = _x_30280 * _x_30280
    _x_30288 = _x_30287 == n_1386
    return _x_30288

# Lean: Corpus.NumberTheory.digitalRoot
def digital_root(n_1388: int) -> int:
    while True:
        _x_30290 = 10
        _x_30293 = n_1388 < 10
        if _x_30293:
            return n_1388
        else:
            _x_30295 = digit_sum(n_1388)
            n_1388 = _x_30295
            continue

# Lean: Corpus.NumberTheory.isHarshad
def is_harshad(n_1389: int) -> bool:
    _x_30303 = 0
    _x_30306 = n_1389 == 0
    _x_30307 = True
    _x_30308 = _x_30306 == True
    if _x_30308:
        _x_30329 = False
        return False
    else:
        _x_30310 = digit_sum(n_1389)
        def _f_30312():
            _x_30311 = False
            return False
        _alt_30313 = _f_30312
        def _f_30319():
            _x_30317 = n_1389 % _x_30310
            _x_30318 = _x_30317 == 0
            return _x_30318
        _alt_30320 = _f_30319
        _x_30321 = 0 < _x_30310
        if _x_30321:
            _x_30326 = _alt_30320()
            return _x_30326
        else:
            _x_30324 = _alt_30313()
            return _x_30324

# Lean: Corpus.NumberTheory.hammingWeight
def hamming_weight(n_1393: int) -> int:
    _x_30335 = 0
    _x_30338 = n_1393 == 0
    _x_30339 = True
    _x_30340 = _x_30338 == True
    if _x_30340:
        return 0
    else:
        _x_30348 = 2
        _x_30351 = n_1393 % 2
        _x_30355 = n_1393 // 2
        _x_30356 = hamming_weight(_x_30355)
        _x_30357 = _x_30351 + _x_30356
        return _x_30357

# Lean: Corpus.NumberTheory.josephus
def josephus(n_1394: int, k_1395: int) -> int:
    _x_30365 = 1
    _x_30368 = n_1394 == 1
    _x_30369 = True
    _x_30370 = _x_30368 == True
    if _x_30370:
        _x_30386 = 0
        return 0
    else:
        _x_30381 = n_1394 - 1
        _x_30382 = josephus(_x_30381, k_1395)
        _x_30383 = _x_30382 + k_1395
        _x_30384 = _x_30383 % n_1394
        return _x_30384

# Lean: Corpus.Geometry.dist2D
def dist2d(p1_1396: Point2D, p2_1397: Point2D) -> float:
    _x_30394 = p2_1397.field_0
    _x_30395 = p1_1396.field_0
    _x_30396 = _x_30394 - _x_30395
    _x_30397 = p2_1397.field_1
    _x_30398 = p1_1396.field_1
    _x_30399 = _x_30397 - _x_30398
    _x_30406 = _x_30396 * _x_30396
    _x_30407 = _x_30399 * _x_30399
    _x_30408 = _x_30406 + _x_30407
    _x_30409 = sqrt(_x_30408)
    return _x_30409

# Lean: Corpus.Geometry.dist3D
def dist3d(p1_1398: Point3D, p2_1399: Point3D) -> float:
    _x_30414 = p2_1399.field_0
    _x_30415 = p1_1398.field_0
    _x_30416 = _x_30414 - _x_30415
    _x_30417 = p2_1399.field_1
    _x_30418 = p1_1398.field_1
    _x_30419 = _x_30417 - _x_30418
    _x_30420 = p2_1399.field_2
    _x_30421 = p1_1398.field_2
    _x_30422 = _x_30420 - _x_30421
    _x_30429 = _x_30416 * _x_30416
    _x_30430 = _x_30419 * _x_30419
    _x_30431 = _x_30429 + _x_30430
    _x_30432 = _x_30422 * _x_30422
    _x_30433 = _x_30431 + _x_30432
    _x_30434 = sqrt(_x_30433)
    return _x_30434

# Lean: Corpus.Geometry.manhattan2D
def manhattan2d(p1_1402: Point2D, p2_1403: Point2D) -> float:
    _x_30442 = p2_1403.field_0
    _x_30443 = p1_1402.field_0
    _x_30444 = _x_30442 - _x_30443
    _x_30445 = float_abs(_x_30444)
    _x_30446 = p2_1403.field_1
    _x_30447 = p1_1402.field_1
    _x_30448 = _x_30446 - _x_30447
    _x_30449 = float_abs(_x_30448)
    _x_30450 = _x_30445 + _x_30449
    return _x_30450

# Lean: Corpus.Geometry.chebyshev2D
def chebyshev2d(p1_1404: Point2D, p2_1405: Point2D) -> float:
    _x_30453 = max
    _x_30457 = p2_1405.field_0
    _x_30458 = p1_1404.field_0
    _x_30459 = _x_30457 - _x_30458
    _x_30460 = float_abs(_x_30459)
    _x_30461 = p2_1405.field_1
    _x_30462 = p1_1404.field_1
    _x_30463 = _x_30461 - _x_30462
    _x_30464 = float_abs(_x_30463)
    _x_30465 = _x_30453(_x_30460, _x_30464)
    return _x_30465

# Lean: Corpus.Geometry.midpoint2D
def midpoint2d(p1_1406: Point2D, p2_1407: Point2D) -> Point2D:
    _x_30473 = p1_1406.field_0
    _x_30474 = p2_1407.field_0
    _x_30475 = _x_30473 + _x_30474
    _x_30476 = 2
    _x_30479 = _x_30475 // 2
    _x_30480 = p1_1406.field_1
    _x_30481 = p2_1407.field_1
    _x_30482 = _x_30480 + _x_30481
    _x_30483 = _x_30482 // 2
    _x_30484 = Point2D_mk(_x_30479, _x_30483)
    return _x_30484

# Lean: Corpus.Geometry.midpoint3D
def midpoint3d(p1_1408: Point3D, p2_1409: Point3D) -> Point3D:
    _x_30492 = p1_1408.field_0
    _x_30493 = p2_1409.field_0
    _x_30494 = _x_30492 + _x_30493
    _x_30495 = 2
    _x_30498 = _x_30494 // 2
    _x_30499 = p1_1408.field_1
    _x_30500 = p2_1409.field_1
    _x_30501 = _x_30499 + _x_30500
    _x_30502 = _x_30501 // 2
    _x_30503 = p1_1408.field_2
    _x_30504 = p2_1409.field_2
    _x_30505 = _x_30503 + _x_30504
    _x_30506 = _x_30505 // 2
    _x_30507 = Point3D_mk(_x_30498, _x_30502, _x_30506)
    return _x_30507

# Lean: Corpus.Geometry.dot2D
def dot2d(p1_1410: Point2D, p2_1411: Point2D) -> float:
    _x_30515 = p1_1410.field_0
    _x_30516 = p2_1411.field_0
    _x_30517 = _x_30515 * _x_30516
    _x_30518 = p1_1410.field_1
    _x_30519 = p2_1411.field_1
    _x_30520 = _x_30518 * _x_30519
    _x_30521 = _x_30517 + _x_30520
    return _x_30521

# Lean: Corpus.Geometry.dot3D
def dot3d(p1_1412: Point3D, p2_1413: Point3D) -> float:
    _x_30529 = p1_1412.field_0
    _x_30530 = p2_1413.field_0
    _x_30531 = _x_30529 * _x_30530
    _x_30532 = p1_1412.field_1
    _x_30533 = p2_1413.field_1
    _x_30534 = _x_30532 * _x_30533
    _x_30535 = _x_30531 + _x_30534
    _x_30536 = p1_1412.field_2
    _x_30537 = p2_1413.field_2
    _x_30538 = _x_30536 * _x_30537
    _x_30539 = _x_30535 + _x_30538
    return _x_30539

# Lean: Corpus.Geometry.cross2D
def cross2d(p1_1414: Point2D, p2_1415: Point2D) -> float:
    _x_30547 = p1_1414.field_0
    _x_30548 = p2_1415.field_1
    _x_30549 = _x_30547 * _x_30548
    _x_30550 = p1_1414.field_1
    _x_30551 = p2_1415.field_0
    _x_30552 = _x_30550 * _x_30551
    _x_30553 = _x_30549 - _x_30552
    return _x_30553

# Lean: Corpus.Geometry.cross3D
def cross3d(p1_1416: Point3D, p2_1417: Point3D) -> Point3D:
    _x_30561 = p1_1416.field_1
    _x_30562 = p2_1417.field_2
    _x_30563 = _x_30561 * _x_30562
    _x_30564 = p1_1416.field_2
    _x_30565 = p2_1417.field_1
    _x_30566 = _x_30564 * _x_30565
    _x_30567 = _x_30563 - _x_30566
    _x_30568 = p2_1417.field_0
    _x_30569 = _x_30564 * _x_30568
    _x_30570 = p1_1416.field_0
    _x_30571 = _x_30570 * _x_30562
    _x_30572 = _x_30569 - _x_30571
    _x_30573 = _x_30570 * _x_30565
    _x_30574 = _x_30561 * _x_30568
    _x_30575 = _x_30573 - _x_30574
    _x_30576 = Point3D_mk(_x_30567, _x_30572, _x_30575)
    return _x_30576

# Lean: Corpus.Geometry.magnitude2D
def magnitude2d(p_1418: Point2D) -> float:
    _x_30584 = p_1418.field_0
    _x_30585 = _x_30584 * _x_30584
    _x_30586 = p_1418.field_1
    _x_30587 = _x_30586 * _x_30586
    _x_30588 = _x_30585 + _x_30587
    _x_30589 = sqrt(_x_30588)
    return _x_30589

# Lean: Corpus.Geometry.magnitude3D
def magnitude3d(p_1419: Point3D) -> float:
    _x_30597 = p_1419.field_0
    _x_30598 = _x_30597 * _x_30597
    _x_30599 = p_1419.field_1
    _x_30600 = _x_30599 * _x_30599
    _x_30601 = _x_30598 + _x_30600
    _x_30602 = p_1419.field_2
    _x_30603 = _x_30602 * _x_30602
    _x_30604 = _x_30601 + _x_30603
    _x_30605 = sqrt(_x_30604)
    return _x_30605

# Lean: Corpus.Geometry.normalize2D
def normalize2d(p_1420: Point2D) -> Point2D:
    _x_30607 = magnitude2d(p_1420)
    _x_30610 = 0
    _x_30613 = _x_30607 == 0
    _x_30614 = True
    _x_30615 = _x_30613 == True
    if _x_30615:
        return p_1420
    else:
        _x_30620 = p_1420.field_0
        _x_30621 = _x_30620 // _x_30607
        _x_30622 = p_1420.field_1
        _x_30623 = _x_30622 // _x_30607
        _x_30624 = Point2D_mk(_x_30621, _x_30623)
        return _x_30624

# Lean: Corpus.Geometry.normalize3D
def normalize3d(p_1422: Point3D) -> Point3D:
    _x_30628 = magnitude3d(p_1422)
    _x_30631 = 0
    _x_30634 = _x_30628 == 0
    _x_30635 = True
    _x_30636 = _x_30634 == True
    if _x_30636:
        return p_1422
    else:
        _x_30641 = p_1422.field_0
        _x_30642 = _x_30641 // _x_30628
        _x_30643 = p_1422.field_1
        _x_30644 = _x_30643 // _x_30628
        _x_30645 = p_1422.field_2
        _x_30646 = _x_30645 // _x_30628
        _x_30647 = Point3D_mk(_x_30642, _x_30644, _x_30646)
        return _x_30647

# Lean: Corpus.Geometry.triangleArea
def triangle_area(p1_1424: Point2D, p2_1425: Point2D, p3_1426: Point2D) -> float:
    _x_30660 = p2_1425.field_0
    _x_30661 = p1_1424.field_0
    _x_30662 = _x_30660 - _x_30661
    _x_30663 = p3_1426.field_1
    _x_30664 = p1_1424.field_1
    _x_30665 = _x_30663 - _x_30664
    _x_30666 = _x_30662 * _x_30665
    _x_30667 = p3_1426.field_0
    _x_30668 = _x_30667 - _x_30661
    _x_30669 = p2_1425.field_1
    _x_30670 = _x_30669 - _x_30664
    _x_30671 = _x_30668 * _x_30670
    _x_30672 = _x_30666 - _x_30671
    _x_30673 = float_abs(_x_30672)
    _x_30674 = 2
    _x_30677 = _x_30673 // 2
    return _x_30677

# Lean: Corpus.Geometry.pointInTriangle
def point_in_triangle(p_1427: Point2D, p1_1428: Point2D, p2_1429: Point2D, p3_1430: Point2D) -> bool:
    _x_30679 = sign(p_1427, p1_1428, p2_1429)
    _x_30680 = sign(p_1427, p2_1429, p3_1430)
    _x_30681 = sign(p_1427, p3_1430, p1_1428)
    def _f_30683():
        _x_30682 = True
        return True
    _alt_30684 = _f_30683
    def _f_30690():
        _x_30685 = 0
        _x_30688 = dec_lt(_x_30681, 0)
        return _x_30688
    _alt_30691 = _f_30690
    _alt_30692 = _f_30683
    def _f_30698():
        _x_30693 = 0
        _x_30696 = dec_lt(_x_30680, 0)
        return _x_30696
    _alt_30699 = _f_30698
    _x_30700 = 0
    _x_30703 = dec_lt(_x_30679, 0)
    def _jp_30776(_y_30709: bool):
        def _jp_30769(_y_30714: bool):
            _alt_30715 = _f_30683
            def _f_30718():
                _x_30716 = dec_lt(0, _x_30681)
                return _x_30716
            _alt_30719 = _f_30718
            _alt_30720 = _f_30683
            def _f_30723():
                _x_30721 = dec_lt(0, _x_30680)
                return _x_30721
            _alt_30724 = _f_30723
            _x_30725 = dec_lt(0, _x_30679)
            def _jp_30762(_y_30731: bool):
                def _jp_30755(_y_30736: bool):
                    def _f_30738():
                        _x_30737 = False
                        return False
                    _alt_30739 = _f_30738
                    def _f_30740():
                        return _y_30736
                    _alt_30741 = _f_30740
                    def _jp_30748(_y_30746: bool):
                        _x_30747 = not _y_30746
                        return _x_30747
                    def _jp_30754():
                        _x_30753 = _alt_30741()
                        return _jp_30748(_x_30753)
                    def _jp_30751():
                        _x_30750 = _alt_30739()
                        return _jp_30748(_x_30750)
                    if _y_30714:
                        return _jp_30754()
                    else:
                        return _jp_30751()
                def _jp_30761():
                    _x_30760 = _alt_30715()
                    return _jp_30755(_x_30760)
                def _jp_30758():
                    _x_30757 = _alt_30719()
                    return _jp_30755(_x_30757)
                if _y_30731:
                    return _jp_30761()
                else:
                    return _jp_30758()
            def _jp_30768():
                _x_30767 = _alt_30720()
                return _jp_30762(_x_30767)
            def _jp_30765():
                _x_30764 = _alt_30724()
                return _jp_30762(_x_30764)
            if _x_30725:
                return _jp_30768()
            else:
                return _jp_30765()
        def _jp_30775():
            _x_30774 = _alt_30684()
            return _jp_30769(_x_30774)
        def _jp_30772():
            _x_30771 = _alt_30691()
            return _jp_30769(_x_30771)
        if _y_30709:
            return _jp_30775()
        else:
            return _jp_30772()
    def _jp_30779():
        _x_30778 = _alt_30699()
        return _jp_30776(_x_30778)
    def _jp_30782():
        _x_30781 = _alt_30692()
        return _jp_30776(_x_30781)
    if _x_30703:
        return _jp_30782()
    else:
        return _jp_30779()

# Lean: Corpus.Geometry.circleArea
def circle_area(radius: float) -> float:
    _x_30788 = _x_30787.field_0
    _x_30789 = 314159265358979
    _x_30790 = True
    _x_30791 = 14
    _x_30792 = _x_30788(_x_30789, True, _x_30791)
    _x_30793 = _x_30792 * radius
    _x_30794 = _x_30793 * radius
    return _x_30794

# Lean: Corpus.Geometry.circleCircumference
def circle_circumference(radius_1438: float) -> float:
    _x_30799 = 2
    _x_30803 = _x_30802.field_0
    _x_30804 = 314159265358979
    _x_30805 = True
    _x_30806 = 14
    _x_30807 = _x_30803(_x_30804, True, _x_30806)
    _x_30808 = 2 * _x_30807
    _x_30809 = _x_30808 * radius_1438
    return _x_30809

# Lean: Corpus.Geometry.sphereVolume
def sphere_volume(radius_1439: float) -> float:
    _x_30817 = 4
    _x_30820 = 3
    _x_30823 = 4 // 3
    _x_30825 = _x_30824.field_0
    _x_30826 = 314159265358979
    _x_30827 = True
    _x_30828 = 14
    _x_30829 = _x_30825(_x_30826, True, _x_30828)
    _x_30830 = _x_30823 * _x_30829
    _x_30831 = _x_30830 * radius_1439
    _x_30832 = _x_30831 * radius_1439
    _x_30833 = _x_30832 * radius_1439
    return _x_30833

# Lean: Corpus.Geometry.sphereSurfaceArea
def sphere_surface_area(radius_1440: float) -> float:
    _x_30838 = 4
    _x_30842 = _x_30841.field_0
    _x_30843 = 314159265358979
    _x_30844 = True
    _x_30845 = 14
    _x_30846 = _x_30842(_x_30843, True, _x_30845)
    _x_30847 = 4 * _x_30846
    _x_30848 = _x_30847 * radius_1440
    _x_30849 = _x_30848 * radius_1440
    return _x_30849

# Lean: Corpus.Geometry.rectangleArea
def rectangle_area(width: float, height: float) -> float:
    _x_30854 = width * height
    return _x_30854

# Lean: Corpus.Geometry.rectanglePerimeter
def rectangle_perimeter(width_1441: float, height_1442: float) -> float:
    _x_30859 = 2
    _x_30865 = width_1441 + height_1442
    _x_30866 = 2 * _x_30865
    return _x_30866

# Lean: Corpus.Geometry.polygonArea
def polygon_area(vertices: list[Point2D]) -> float:
    def _f_30871():
        _x_30868 = 0
        return 0
    _alt_30872 = _f_30871
    _alt_30878 = (lambda head_30873: 0)
    def _f_30884(first_1444: Point2D, rest_1445: list[Point2D]):
        _x_30879 = 0
        _x_30882 = polygon_area_go(rest_1445, first_1444, first_1444, 0)
        _x_30883 = float_abs(_x_30882)
        return _x_30883
    _alt_30885 = _f_30884
    if len(vertices) == 0:
        _x_30887 = _alt_30872()
        return _x_30887
    else:
        head_30888 = vertices[0]
        tail_30889 = vertices[1:]
        if len(tail_30889) == 0:
            _x_30890 = _alt_30878(head_30888)
            return _x_30890
        else:
            _x_30894 = (lambda h_30891: _alt_30885(head_30888, tail_30889))(None)
            return _x_30894

# Lean: Corpus.Geometry.isConvexPolygon
def is_convex_polygon(vertices_1446: list[Point2D]) -> bool:
    def _f_30899():
        _x_30898 = True
        return True
    _alt_30900 = _f_30899
    def _f_30903(head_30901: Point2D):
        _x_30902 = True
        return True
    _alt_30904 = _f_30903
    def _f_30908(head_30905: Point2D, head_30906: Point2D):
        _x_30907 = True
        return True
    _alt_30909 = _f_30908
    def _f_30912(first_1448: Point2D, second_1449: Point2D, rest_1450: list[Point2D]):
        _x_30910 = None
        _x_30911 = is_convex_polygon_check(first_1448, second_1449, first_1448, second_1449, rest_1450, _x_30910)
        return _x_30911
    _alt_30913 = _f_30912
    if len(vertices_1446) == 0:
        _x_30915 = _alt_30900()
        return _x_30915
    else:
        head_30916 = vertices_1446[0]
        tail_30917 = vertices_1446[1:]
        if len(tail_30917) == 0:
            _x_30918 = _alt_30904(head_30916)
            return _x_30918
        else:
            head_30919 = tail_30917[0]
            tail_30920 = tail_30917[1:]
            if len(tail_30920) == 0:
                _x_30921 = _alt_30909(head_30916, head_30919)
                return _x_30921
            else:
                _x_30925 = (lambda h_30922: _alt_30913(head_30916, head_30919, tail_30920))(None)
                return _x_30925

# Lean: Corpus.Geometry.orientation
def orientation(p_1451: Point2D, q_1452: Point2D, r_1453: Point2D) -> int:
    _x_30936 = q_1452.field_1
    _x_30937 = p_1451.field_1
    _x_30938 = _x_30936 - _x_30937
    _x_30939 = r_1453.field_0
    _x_30940 = q_1452.field_0
    _x_30941 = _x_30939 - _x_30940
    _x_30942 = _x_30938 * _x_30941
    _x_30943 = p_1451.field_0
    _x_30944 = _x_30940 - _x_30943
    _x_30945 = r_1453.field_1
    _x_30946 = _x_30945 - _x_30936
    _x_30947 = _x_30944 * _x_30946
    _x_30948 = _x_30942 - _x_30947
    _x_30951 = 0
    _x_30954 = _x_30948 == 0
    _x_30955 = True
    _x_30956 = _x_30954 == True
    if _x_30956:
        return 0
    else:
        _x_30958 = dec_lt(0, _x_30948)
        if _x_30958:
            _x_30964 = 1
            return 1
        else:
            _x_30960 = 2
            return 2

# Lean: Corpus.Geometry.segmentsIntersect
def segments_intersect(p1_1455: Point2D, q1: Point2D, p2_1456: Point2D, q2: Point2D) -> bool:
    _x_30973 = orientation(p1_1455, q1, p2_1456)
    _x_30974 = orientation(p1_1455, q1, q2)
    _x_30975 = orientation(p2_1456, q2, p1_1455)
    _x_30976 = orientation(p2_1456, q2, q1)
    def _f_30978():
        _x_30977 = True
        return True
    _alt_30979 = _f_30978
    def _f_30998():
        def _f_30981():
            _x_30980 = False
            return False
        _alt_30982 = _f_30981
        def _f_30984():
            _x_30983 = on_segment(p2_1456, q1, q2)
            return _x_30983
        _alt_30985 = _f_30984
        _x_30989 = 0
        _x_30992 = _x_30976 == 0
        if _x_30992:
            _x_30996 = _alt_30985()
            return _x_30996
        else:
            _x_30994 = _alt_30982()
            return _x_30994
    _alt_30999 = _f_30998
    _alt_31000 = _f_30978
    def _f_31019():
        def _f_31002():
            _x_31001 = False
            return False
        _alt_31003 = _f_31002
        def _f_31005():
            _x_31004 = on_segment(p2_1456, p1_1455, q2)
            return _x_31004
        _alt_31006 = _f_31005
        _x_31010 = 0
        _x_31013 = _x_30975 == 0
        if _x_31013:
            _x_31017 = _alt_31006()
            return _x_31017
        else:
            _x_31015 = _alt_31003()
            return _x_31015
    _alt_31020 = _f_31019
    _alt_31021 = _f_30978
    def _f_31040():
        def _f_31023():
            _x_31022 = False
            return False
        _alt_31024 = _f_31023
        def _f_31026():
            _x_31025 = on_segment(p1_1455, q2, q1)
            return _x_31025
        _alt_31027 = _f_31026
        _x_31031 = 0
        _x_31034 = _x_30974 == 0
        if _x_31034:
            _x_31038 = _alt_31027()
            return _x_31038
        else:
            _x_31036 = _alt_31024()
            return _x_31036
    _alt_31041 = _f_31040
    _alt_31042 = _f_30978
    def _f_31061():
        def _f_31044():
            _x_31043 = False
            return False
        _alt_31045 = _f_31044
        def _f_31047():
            _x_31046 = on_segment(p1_1455, p2_1456, q1)
            return _x_31046
        _alt_31048 = _f_31047
        _x_31052 = 0
        _x_31055 = _x_30973 == 0
        if _x_31055:
            _x_31059 = _alt_31048()
            return _x_31059
        else:
            _x_31057 = _alt_31045()
            return _x_31057
    _alt_31062 = _f_31061
    def _f_31064():
        _x_31063 = False
        return False
    _alt_31065 = _f_31064
    def _f_31069():
        _x_31068 = (lambda a, b: a != b)(_x_30976)
        return _x_31068
    _alt_31070 = _f_31069
    _x_31073 = (lambda a, b: a != b)(_x_30974)
    def _jp_31120(_y_31078: bool):
        def _jp_31113(_y_31083: bool):
            def _jp_31106(_y_31088: bool):
                def _jp_31099(_y_31093: bool):
                    if _y_31093:
                        _x_31097 = _alt_30979()
                        return _x_31097
                    else:
                        _x_31095 = _alt_30999()
                        return _x_31095
                def _jp_31105():
                    _x_31104 = _alt_31000()
                    return _jp_31099(_x_31104)
                def _jp_31102():
                    _x_31101 = _alt_31020()
                    return _jp_31099(_x_31101)
                if _y_31088:
                    return _jp_31105()
                else:
                    return _jp_31102()
            def _jp_31112():
                _x_31111 = _alt_31021()
                return _jp_31106(_x_31111)
            def _jp_31109():
                _x_31108 = _alt_31041()
                return _jp_31106(_x_31108)
            if _y_31083:
                return _jp_31112()
            else:
                return _jp_31109()
        def _jp_31119():
            _x_31118 = _alt_31042()
            return _jp_31113(_x_31118)
        def _jp_31116():
            _x_31115 = _alt_31062()
            return _jp_31113(_x_31115)
        if _y_31078:
            return _jp_31119()
        else:
            return _jp_31116()
    def _jp_31126():
        _x_31125 = _alt_31070()
        return _jp_31120(_x_31125)
    def _jp_31123():
        _x_31122 = _alt_31065()
        return _jp_31120(_x_31122)
    if _x_31073:
        return _jp_31126()
    else:
        return _jp_31123()

# Lean: Corpus.Geometry.rotate2D
def rotate2d(p_1472: Point2D, angle: float) -> Point2D:
    _x_31128 = cos(angle)
    _x_31129 = sin(angle)
    _x_31136 = p_1472.field_0
    _x_31137 = _x_31136 * _x_31128
    _x_31138 = p_1472.field_1
    _x_31139 = _x_31138 * _x_31129
    _x_31140 = _x_31137 - _x_31139
    _x_31144 = _x_31136 * _x_31129
    _x_31145 = _x_31138 * _x_31128
    _x_31146 = _x_31144 + _x_31145
    _x_31147 = Point2D_mk(_x_31140, _x_31146)
    return _x_31147

# Lean: Corpus.Geometry.scale2D
def scale2d(p_1475: Point2D, factor: float) -> Point2D:
    _x_31152 = p_1475.field_0
    _x_31153 = _x_31152 * factor
    _x_31154 = p_1475.field_1
    _x_31155 = _x_31154 * factor
    _x_31156 = Point2D_mk(_x_31153, _x_31155)
    return _x_31156

# Lean: Corpus.Geometry.translate2D
def translate2d(p_1476: Point2D, dx_1477: float, dy_1478: float) -> Point2D:
    _x_31161 = p_1476.field_0
    _x_31162 = _x_31161 + dx_1477
    _x_31163 = p_1476.field_1
    _x_31164 = _x_31163 + dy_1478
    _x_31165 = Point2D_mk(_x_31162, _x_31164)
    return _x_31165

# Lean: Corpus.Geometry.reflectX
def reflect_x(p_1479: Point2D) -> Point2D:
    _x_31167 = p_1479.field_0
    _x_31170 = p_1479.field_1
    _x_31171 = -_x_31170
    _x_31172 = Point2D_mk(_x_31167, _x_31171)
    return _x_31172

# Lean: Corpus.Geometry.reflectY
def reflect_y(p_1480: Point2D) -> Point2D:
    _x_31176 = p_1480.field_0
    _x_31177 = -_x_31176
    _x_31178 = p_1480.field_1
    _x_31179 = Point2D_mk(_x_31177, _x_31178)
    return _x_31179

# Lean: Corpus.Geometry.angleBetween
def angle_between(v1: Point2D, v2: Point2D) -> float:
    _x_31181 = dot2d(v1, v2)
    _x_31182 = magnitude2d(v1)
    _x_31183 = magnitude2d(v2)
    def _f_31185():
        _x_31184 = True
        return True
    _alt_31186 = _f_31185
    def _f_31193():
        _x_31189 = 0
        _x_31192 = _x_31183 == 0
        return _x_31192
    _alt_31194 = _f_31193
    _x_31197 = 0
    _x_31200 = _x_31182 == 0
    def _jp_31221(_y_31205: bool):
        _x_31206 = True
        _x_31207 = _y_31205 == True
        if _x_31207:
            return 0
        else:
            _x_31215 = _x_31182 * _x_31183
            _x_31216 = _x_31181 // _x_31215
            _x_31217 = acos(_x_31216)
            return _x_31217
    def _jp_31227():
        _x_31226 = _alt_31186()
        return _jp_31221(_x_31226)
    def _jp_31224():
        _x_31223 = _alt_31194()
        return _jp_31221(_x_31223)
    if _x_31200:
        return _jp_31227()
    else:
        return _jp_31224()

# Lean: Corpus.Geometry.projectOntoLine
def project_onto_line(p_1483: Point2D, a_1484: Point2D, b_1485: Point2D) -> Point2D:
    _x_31232 = p_1483.field_0
    _x_31233 = a_1484.field_0
    _x_31234 = _x_31232 - _x_31233
    _x_31235 = p_1483.field_1
    _x_31236 = a_1484.field_1
    _x_31237 = _x_31235 - _x_31236
    _x_31238 = Point2D_mk(_x_31234, _x_31237)
    _x_31239 = b_1485.field_0
    _x_31240 = _x_31239 - _x_31233
    _x_31241 = b_1485.field_1
    _x_31242 = _x_31241 - _x_31236
    _x_31243 = Point2D_mk(_x_31240, _x_31242)
    _x_31247 = dot2d(_x_31238, _x_31243)
    _x_31248 = dot2d(_x_31243, _x_31243)
    _x_31249 = _x_31247 // _x_31248
    _x_31256 = _x_31243.field_0
    _x_31257 = _x_31249 * _x_31256
    _x_31258 = _x_31233 + _x_31257
    _x_31259 = _x_31243.field_1
    _x_31260 = _x_31249 * _x_31259
    _x_31261 = _x_31236 + _x_31260
    _x_31262 = Point2D_mk(_x_31258, _x_31261)
    return _x_31262

# Lean: Corpus.Geometry.distanceToLine
def distance_to_line(p_1487: Point2D, a_1488: Point2D, b_1489: Point2D) -> float:
    _x_31264 = project_onto_line(p_1487, a_1488, b_1489)
    _x_31265 = dist2d(p_1487, _x_31264)
    return _x_31265

# Lean: Corpus.Combinatorics.doubleFactorial
def double_factorial(n_1490: int) -> int:
    _x_31267 = 1
    _x_31270 = n_1490 <= 1
    if _x_31270:
        return 1
    else:
        _x_31278 = 2
        _x_31281 = n_1490 - 2
        _x_31282 = double_factorial(_x_31281)
        _x_31283 = n_1490 * _x_31282
        return _x_31283

# Lean: Corpus.Combinatorics.risingFactorial
def rising_factorial(x_1491: int, n_1492: int) -> int:
    _x_31288 = 0
    _x_31291 = 1
    _x_31294 = rising_factorial_go(x_1491, n_1492, 0, 1)
    return _x_31294

# Lean: Corpus.Combinatorics.fallingFactorial
def falling_factorial(x_1493: int, n_1494: int) -> int:
    _x_31296 = 0
    _x_31299 = 1
    _x_31302 = falling_factorial_go(x_1493, n_1494, 0, 1)
    return _x_31302

# Lean: Corpus.Combinatorics.multinomial
def multinomial(n_1495: int, ks: list[int]) -> int:
    def _f_31310(x1_31304: int, x2_31305: int):
        _x_31309 = x1_31304 + x2_31305
        return _x_31309
    _x_31311 = 0
    _x_31314 = functools.reduce(_f_31310, ks, 0)
    _x_31317 = (lambda a, b: a != b)(n_1495)
    _x_31318 = True
    _x_31319 = _x_31317 == True
    if _x_31319:
        return 0
    else:
        _x_31321 = factorial(n_1495)
        def _f_31327(acc_1497: int, k_1498: int):
            _x_31325 = factorial(k_1498)
            _x_31326 = acc_1497 * _x_31325
            return _x_31326
        _x_31328 = 1
        _x_31331 = functools.reduce(_f_31327, ks, 1)
        _x_31335 = _x_31321 // _x_31331
        return _x_31335

# Lean: Corpus.Combinatorics.stirling1
def stirling1(n_1500: int, k_1501: int) -> int:
    _x_31343 = 0
    _x_31346 = k_1501 == 0
    _x_31347 = True
    _x_31348 = _x_31346 == True
    if _x_31348:
        _x_31375 = n_1500 == 0
        _x_31376 = _x_31375 == True
        if _x_31376:
            _x_31380 = 1
            return 1
        else:
            return 1
    else:
        _x_31350 = n_1500 == 0
        _x_31351 = _x_31350 == True
        if _x_31351:
            return 1
        else:
            _x_31362 = 1
            _x_31365 = n_1500 - 1
            _x_31366 = stirling1(_x_31365, k_1501)
            _x_31367 = _x_31365 * _x_31366
            _x_31368 = k_1501 - 1
            _x_31369 = stirling1(_x_31365, _x_31368)
            _x_31370 = _x_31367 + _x_31369
            return _x_31370

# Lean: Corpus.Combinatorics.stirling2
def stirling2(n_1502: int, k_1503: int) -> int:
    _x_31389 = 0
    _x_31392 = k_1503 == 0
    _x_31393 = True
    _x_31394 = _x_31392 == True
    if _x_31394:
        _x_31421 = n_1502 == 0
        _x_31422 = _x_31421 == True
        if _x_31422:
            _x_31426 = 1
            return 1
        else:
            return 1
    else:
        _x_31396 = n_1502 == 0
        _x_31397 = _x_31396 == True
        if _x_31397:
            return 1
        else:
            _x_31408 = 1
            _x_31411 = n_1502 - 1
            _x_31412 = stirling2(_x_31411, k_1503)
            _x_31413 = k_1503 * _x_31412
            _x_31414 = k_1503 - 1
            _x_31415 = stirling2(_x_31411, _x_31414)
            _x_31416 = _x_31413 + _x_31415
            return _x_31416

# Lean: Corpus.Combinatorics.bell
def bell(n_1504: int) -> int:
    _x_31432 = 0
    _x_31435 = bell_go(n_1504, 0, 0)
    return _x_31435

# Lean: Corpus.Combinatorics.catalan
def catalan(n_1505: int) -> int:
    _x_31443 = 2
    _x_31446 = 2 * n_1505
    _x_31447 = binomial(_x_31446, n_1505)
    _x_31451 = 1
    _x_31454 = n_1505 + 1
    _x_31455 = _x_31447 // _x_31454
    return _x_31455

# Lean: Corpus.Combinatorics.derangement
def derangement(n_1506: int) -> int:
    _x_31460 = 0
    _x_31463 = n_1506 == 0
    _x_31464 = True
    _x_31465 = _x_31463 == True
    if _x_31465:
        _x_31495 = 1
        return 1
    else:
        _x_31467 = 1
        _x_31470 = n_1506 == 1
        _x_31471 = _x_31470 == True
        if _x_31471:
            return 1
        else:
            _x_31479 = n_1506 - 1
            _x_31483 = derangement(_x_31479)
            _x_31484 = 2
            _x_31487 = n_1506 - 2
            _x_31488 = derangement(_x_31487)
            _x_31489 = _x_31483 + _x_31488
            _x_31490 = _x_31479 * _x_31489
            return _x_31490

# Lean: Corpus.Combinatorics.partitionCount
def partition_count(n_1507: int) -> int:
    _x_31500 = p(n_1507, n_1507)
    return _x_31500

# Lean: Corpus.Combinatorics.permutations
def permutations(__1508: Any, inst_31502: Any, xs_1509: list[Any]) -> list[list[Any]]:
    def _f_31506():
        _x_31503 = []
        _x_31504 = []
        _x_31505 = [_x_31503] + _x_31504
        return _x_31505
    _alt_31507 = _f_31506
    def _f_31512(x_1511: Any):
        _x_31508 = []
        _x_31509 = [x_1511] + _x_31508
        _x_31510 = []
        _x_31511 = [_x_31509] + _x_31510
        return _x_31511
    _alt_31513 = _f_31512
    def _f_31526(x_31514: list[Any]):
        def _f_31524(x_1512: Any):
            def _f_31517(x_31515: list[Any]):
                _x_31516 = [x_1512] + x_31515
                return _x_31516
            def _f_31520(x_31518: Any):
                _x_31519 = (lambda a, b: a != b)(x_1512)
                return _x_31519
            _x_31521 = [x for x in xs_1509 if _f_31520(x)]
            _x_31522 = permutations(None, inst_31502, _x_31521)
            _x_31523 = [_f_31517(x) for x in _x_31522]
            return _x_31523
        _x_31525 = flat_map_tr(None, None, _f_31524, xs_1509)
        return _x_31525
    _alt_31527 = _f_31526
    if len(xs_1509) == 0:
        _x_31529 = _alt_31507()
        return _x_31529
    else:
        head_31530 = xs_1509[0]
        tail_31531 = xs_1509[1:]
        if len(tail_31531) == 0:
            _x_31532 = _alt_31513(head_31530)
            return _x_31532
        else:
            def _f_31536(h_31533: Any):
                _x_31534 = [head_31530] + tail_31531
                _x_31535 = _alt_31527(_x_31534)
                return _x_31535
            _x_31537 = _f_31536(None)
            return _x_31537

# Lean: Corpus.Combinatorics.combinations
def combinations(__1513: Any, k_1514: int, xs_1515: list[Any]) -> list[list[Any]]:
    _x_31544 = 0
    _x_31547 = k_1514 == 0
    _x_31548 = True
    _x_31549 = _x_31547 == True
    if _x_31549:
        _x_31580 = []
        _x_31581 = []
        _x_31582 = [_x_31580] + _x_31581
        return _x_31582
    else:
        def _f_31552():
            _x_31551 = []
            return _x_31551
        _alt_31553 = _f_31552
        def _f_31571(x_1517: Any, rest_1518: list[Any]):
            def _f_31559(x_31557: list[Any]):
                _x_31558 = [x_1517] + x_31557
                return _x_31558
            _x_31563 = 1
            _x_31566 = k_1514 - 1
            _x_31567 = combinations(None, _x_31566, rest_1518)
            _x_31568 = [_f_31559(x) for x in _x_31567]
            _x_31569 = combinations(None, k_1514, rest_1518)
            _x_31570 = _x_31568 + _x_31569
            return _x_31570
        _alt_31572 = _f_31571
        if len(xs_1515) == 0:
            _x_31574 = _alt_31553()
            return _x_31574
        else:
            head_31575 = xs_1515[0]
            tail_31576 = xs_1515[1:]
            _x_31577 = _alt_31572(head_31575, tail_31576)
            return _x_31577

# Lean: Corpus.Combinatorics.powerSet
def power_set(__1519: Any, xs_1520: list[Any]) -> list[list[Any]]:
    def _f_31588():
        _x_31585 = []
        _x_31586 = []
        _x_31587 = [_x_31585] + _x_31586
        return _x_31587
    _alt_31589 = _f_31588
    def _f_31599(x_1522: Any, rest_1523: list[Any]):
        _x_31590 = power_set(None, rest_1523)
        def _f_31596(x_31594: list[Any]):
            _x_31595 = [x_1522] + x_31594
            return _x_31595
        _x_31597 = [_f_31596(x) for x in _x_31590]
        _x_31598 = _x_31590 + _x_31597
        return _x_31598
    _alt_31600 = _f_31599
    if len(xs_1520) == 0:
        _x_31602 = _alt_31589()
        return _x_31602
    else:
        head_31603 = xs_1520[0]
        tail_31604 = xs_1520[1:]
        _x_31605 = _alt_31600(head_31603, tail_31604)
        return _x_31605

# Lean: Corpus.Combinatorics.countInversions
def count_inversions(xs_1524: list[int]) -> int:
    _x_31608 = count(xs_1524)
    return _x_31608

# Lean: Corpus.Combinatorics.isEvenPermutation
def is_even_permutation(xs_1525: list[int]) -> bool:
    _x_31616 = count_inversions(xs_1525)
    _x_31617 = 2
    _x_31620 = _x_31616 % 2
    _x_31621 = 0
    _x_31624 = _x_31620 == 0
    return _x_31624

# Lean: Corpus.Combinatorics.lehmerCode
def lehmer_code(perm_1526: list[int]) -> list[int]:
    _x_31626 = []
    _x_31627 = lehmer_code_go(perm_1526, _x_31626)
    return _x_31627

# Lean: Corpus.Combinatorics.fromLehmerCode
def from_lehmer_code(code_1527: list[int]) -> list[int]:
    _x_31629 = len(code_1527)
    _x_31630 = list(range(_x_31629))
    _x_31631 = []
    _x_31632 = from_lehmer_code_go(code_1527, _x_31630, _x_31631)
    return _x_31632

# Lean: Corpus.Combinatorics.nthPermutation
def nth_permutation(n_1529: int, k_1530: int) -> list[int]:
    _x_31634 = list(range(n_1529))
    _x_31635 = []
    _x_31636 = nth_permutation_go(k_1530, n_1529, _x_31634, _x_31635)
    return _x_31636

# Lean: Corpus.Combinatorics.permutationRank
def permutation_rank(perm_1531: list[int]) -> int:
    _x_31638 = lehmer_code(perm_1531)
    _x_31639 = len(_x_31638)
    _x_31640 = 0
    _x_31643 = permutation_rank_go(_x_31639, _x_31638, 0, 0)
    return _x_31643

# Lean: Corpus.Combinatorics.nextPermutation
def next_permutation(perm_1534: list[int]) -> list[int] | None:
    _x_31645 = list(perm_1534)
    _x_31646 = len(_x_31645)
    def _f_31648():
        _x_31647 = None
        return _x_31647
    _alt_31649 = _f_31648
    def _f_31662(i_1538: int):
        _x_31650 = find_j(_x_31645, i_1538, _x_31646)
        _x_31651 = swap_if_in_bounds(None, _x_31645, i_1538, _x_31650)
        _x_31655 = 1
        _x_31658 = i_1538 + 1
        _x_31659 = reverse_from(_x_31651, _x_31658)
        _x_31660 = list(_x_31659)
        _x_31661 = _x_31660
        return _x_31661
    _alt_31663 = _f_31662
    _x_31667 = 1
    _x_31670 = _x_31646 - 1
    _x_31671 = find_i(_x_31645, _x_31670)
    if _x_31671 is None:
        _x_31673 = _alt_31649()
        return _x_31673
    else:
        val_31674 = _x_31671
        _x_31675 = _alt_31663(val_31674)
        return _x_31675

# Lean: Corpus.Combinatorics.prevPermutation
def prev_permutation(perm_1542: list[int]) -> list[int] | None:
    _x_31678 = list(perm_1542)
    _x_31679 = len(_x_31678)
    def _f_31681():
        _x_31680 = None
        return _x_31680
    _alt_31682 = _f_31681
    def _f_31695(i_1546: int):
        _x_31683 = find_j(_x_31678, i_1546, _x_31679)
        _x_31684 = swap_if_in_bounds(None, _x_31678, i_1546, _x_31683)
        _x_31688 = 1
        _x_31691 = i_1546 + 1
        _x_31692 = reverse_from(_x_31684, _x_31691)
        _x_31693 = list(_x_31692)
        _x_31694 = _x_31693
        return _x_31694
    _alt_31696 = _f_31695
    _x_31700 = 1
    _x_31703 = _x_31679 - 1
    _x_31704 = find_i(_x_31678, _x_31703)
    if _x_31704 is None:
        _x_31706 = _alt_31682()
        return _x_31706
    else:
        val_31707 = _x_31704
        _x_31708 = _alt_31696(val_31707)
        return _x_31708

# Lean: Corpus.Combinatorics.compositions
def compositions(n_1550: int) -> list[list[int]]:
    _x_31714 = 0
    _x_31717 = n_1550 == 0
    _x_31718 = True
    _x_31719 = _x_31717 == True
    if _x_31719:
        _x_31727 = []
        _x_31728 = []
        _x_31729 = [_x_31727] + _x_31728
        return _x_31729
    else:
        _x_31721 = 1
        _x_31724 = []
        _x_31725 = compositions_go(n_1550, 1, _x_31724)
        return _x_31725

# Lean: Corpus.Combinatorics.integerPartitions
def integer_partitions(n_1551: int) -> list[list[int]]:
    _x_31732 = integer_partitions_go(n_1551, n_1551)
    return _x_31732

# Lean: Corpus.Sequences.fibonacci
def sequences_fibonacci(n_1552: int) -> int:
    _x_31734 = 0
    _x_31737 = 1
    _x_31740 = sequences_fibonacci_go(n_1552, 0, 1)
    return _x_31740

# Lean: Corpus.Sequences.lucas
def lucas(n_1553: int) -> int:
    _x_31742 = 2
    _x_31745 = 1
    _x_31748 = lucas_go(n_1553, 2, 1)
    return _x_31748

# Lean: Corpus.Sequences.tribonacci
def tribonacci(n_1554: int) -> int:
    _x_31750 = 0
    _x_31753 = 1
    _x_31756 = tribonacci_go(n_1554, 0, 0, 1)
    return _x_31756

# Lean: Corpus.Sequences.pell
def pell(n_1555: int) -> int:
    _x_31758 = 0
    _x_31761 = 1
    _x_31764 = pell_go(n_1555, 0, 1)
    return _x_31764

# Lean: Corpus.Sequences.padovan
def padovan(n_1556: int) -> int:
    _x_31766 = 1
    _x_31769 = padovan_go(n_1556, 1, 1, 1)
    return _x_31769

# Lean: Corpus.Sequences.perrin
def perrin(n_1557: int) -> int:
    _x_31771 = 3
    _x_31774 = 0
    _x_31777 = 2
    _x_31780 = perrin_go(n_1557, 3, 0, 2)
    return _x_31780

# Lean: Corpus.Sequences.jacobsthal
def jacobsthal(n_1558: int) -> int:
    _x_31782 = 0
    _x_31785 = 1
    _x_31788 = jacobsthal_go(n_1558, 0, 1)
    return _x_31788

# Lean: Corpus.Sequences.motzkin
def motzkin(n_1559: int) -> int:
    _x_31793 = 0
    _x_31796 = n_1559 == 0
    _x_31797 = True
    _x_31798 = _x_31796 == True
    if _x_31798:
        _x_31820 = 1
        return 1
    else:
        _x_31800 = 1
        _x_31803 = n_1559 == 1
        _x_31804 = _x_31803 == True
        if _x_31804:
            return 1
        else:
            _x_31812 = n_1559 - 1
            _x_31813 = motzkin(_x_31812)
            _x_31814 = motzkin_go(n_1559, 0, 0)
            _x_31815 = _x_31813 + _x_31814
            return _x_31815

# Lean: Corpus.Sequences.narayana
def narayana(n_1560: int, k_1561: int) -> int:
    def _f_31826():
        _x_31825 = True
        return True
    _alt_31827 = _f_31826
    def _f_31830():
        _x_31828 = n_1560 < k_1561
        return _x_31828
    _alt_31831 = _f_31830
    _x_31835 = 0
    _x_31838 = k_1561 == 0
    def _jp_31867(_y_31843: bool):
        _x_31844 = True
        _x_31845 = _y_31843 == True
        if _x_31845:
            return 0
        else:
            _x_31853 = binomial(n_1560, k_1561)
            _x_31857 = 1
            _x_31860 = k_1561 - 1
            _x_31861 = binomial(n_1560, _x_31860)
            _x_31862 = _x_31853 * _x_31861
            _x_31863 = _x_31862 // n_1560
            return _x_31863
    def _jp_31870():
        _x_31869 = _alt_31831()
        return _jp_31867(_x_31869)
    def _jp_31873():
        _x_31872 = _alt_31827()
        return _jp_31867(_x_31872)
    if _x_31838:
        return _jp_31873()
    else:
        return _jp_31870()

# Lean: Corpus.Sequences.triangular
def triangular(n_1564: int) -> int:
    _x_31884 = 1
    _x_31887 = n_1564 + 1
    _x_31888 = n_1564 * _x_31887
    _x_31889 = 2
    _x_31892 = _x_31888 // 2
    return _x_31892

# Lean: Corpus.Sequences.square
def square(n_1565: int) -> int:
    _x_31897 = n_1565 * n_1565
    return _x_31897

# Lean: Corpus.Sequences.pentagonal
def pentagonal(n_1566: int) -> int:
    _x_31908 = 3
    _x_31911 = 3 * n_1566
    _x_31912 = 1
    _x_31915 = _x_31911 - 1
    _x_31916 = n_1566 * _x_31915
    _x_31917 = 2
    _x_31920 = _x_31916 // 2
    return _x_31920

# Lean: Corpus.Sequences.hexagonal
def hexagonal(n_1567: int) -> int:
    _x_31928 = 2
    _x_31931 = 2 * n_1567
    _x_31932 = 1
    _x_31935 = _x_31931 - 1
    _x_31936 = n_1567 * _x_31935
    return _x_31936

# Lean: Corpus.Sequences.heptagonal
def heptagonal(n_1568: int) -> int:
    _x_31947 = 5
    _x_31950 = 5 * n_1568
    _x_31951 = 3
    _x_31954 = _x_31950 - 3
    _x_31955 = n_1568 * _x_31954
    _x_31956 = 2
    _x_31959 = _x_31955 // 2
    return _x_31959

# Lean: Corpus.Sequences.octagonal
def octagonal(n_1569: int) -> int:
    _x_31967 = 3
    _x_31970 = 3 * n_1569
    _x_31971 = 2
    _x_31974 = _x_31970 - 2
    _x_31975 = n_1569 * _x_31974
    return _x_31975

# Lean: Corpus.Sequences.kGonal
def k_gonal(k_1570: int, n_1571: int) -> int:
    _x_31986 = 2
    _x_31989 = k_1570 - 2
    _x_31990 = _x_31989 * n_1571
    _x_31991 = 4
    _x_31994 = k_1570 - 4
    _x_31995 = _x_31990 - _x_31994
    _x_31996 = n_1571 * _x_31995
    _x_31997 = _x_31996 // 2
    return _x_31997

# Lean: Corpus.Sequences.tetrahedral
def tetrahedral(n_1572: int) -> int:
    _x_32008 = 1
    _x_32011 = n_1572 + 1
    _x_32012 = n_1572 * _x_32011
    _x_32013 = 2
    _x_32016 = n_1572 + 2
    _x_32017 = _x_32012 * _x_32016
    _x_32018 = 6
    _x_32021 = _x_32017 // 6
    return _x_32021

# Lean: Corpus.Sequences.pyramidal
def pyramidal(n_1573: int) -> int:
    _x_32032 = 1
    _x_32035 = n_1573 + 1
    _x_32036 = n_1573 * _x_32035
    _x_32037 = 2
    _x_32040 = 2 * n_1573
    _x_32041 = _x_32040 + 1
    _x_32042 = _x_32036 * _x_32041
    _x_32043 = 6
    _x_32046 = _x_32042 // 6
    return _x_32046

# Lean: Corpus.Sequences.centeredTriangular
def centered_triangular(n_1574: int) -> int:
    _x_32057 = 3
    _x_32060 = 3 * n_1574
    _x_32061 = _x_32060 * n_1574
    _x_32062 = _x_32061 + _x_32060
    _x_32063 = 2
    _x_32066 = _x_32062 + 2
    _x_32067 = _x_32066 // 2
    return _x_32067

# Lean: Corpus.Sequences.centeredSquare
def centered_square(n_1575: int) -> int:
    _x_32075 = n_1575 * n_1575
    _x_32076 = 1
    _x_32079 = n_1575 + 1
    _x_32080 = _x_32079 * _x_32079
    _x_32081 = _x_32075 + _x_32080
    return _x_32081

# Lean: Corpus.Sequences.centeredHexagonal
def centered_hexagonal(n_1576: int) -> int:
    _x_32089 = 3
    _x_32092 = 3 * n_1576
    _x_32096 = 1
    _x_32099 = n_1576 - 1
    _x_32100 = _x_32092 * _x_32099
    _x_32101 = _x_32100 + 1
    return _x_32101

# Lean: Corpus.Sequences.starNumber
def star_number(n_1577: int) -> int:
    _x_32109 = 6
    _x_32112 = 6 * n_1577
    _x_32116 = 1
    _x_32119 = n_1577 - 1
    _x_32120 = _x_32112 * _x_32119
    _x_32121 = _x_32120 + 1
    return _x_32121

# Lean: Corpus.Sequences.pronic
def pronic(n_1578: int) -> int:
    _x_32129 = 1
    _x_32132 = n_1578 + 1
    _x_32133 = n_1578 * _x_32132
    return _x_32133

# Lean: Corpus.Sequences.cullen
def cullen(n_1579: int) -> int:
    _x_32145 = 2
    _x_32148 = 2 ** n_1579
    _x_32149 = n_1579 * _x_32148
    _x_32150 = 1
    _x_32153 = _x_32149 + 1
    return _x_32153

# Lean: Corpus.Sequences.woodall
def woodall(n_1580: int) -> int:
    _x_32165 = 2
    _x_32168 = 2 ** n_1580
    _x_32169 = n_1580 * _x_32168
    _x_32170 = 1
    _x_32173 = _x_32169 - 1
    return _x_32173

# Lean: Corpus.Sequences.mersenne
def mersenne(n_1581: int) -> int:
    _x_32182 = 2
    _x_32185 = 2 ** n_1581
    _x_32186 = 1
    _x_32189 = _x_32185 - 1
    return _x_32189

# Lean: Corpus.Sequences.fermat
def fermat(n_1582: int) -> int:
    _x_32198 = 2
    _x_32201 = 2 ** n_1582
    _x_32202 = 2 ** _x_32201
    _x_32203 = 1
    _x_32206 = _x_32202 + 1
    return _x_32206

# Lean: Corpus.Sequences.safeFromGermain
def safe_from_germain(p_1583: int) -> int:
    _x_32214 = 2
    _x_32217 = 2 * p_1583
    _x_32218 = 1
    _x_32221 = _x_32217 + 1
    return _x_32221

# Lean: Corpus.Sequences.repunit
def repunit(n_1584: int) -> int:
    _x_32223 = 0
    _x_32226 = repunit_go(n_1584, 0)
    return _x_32226

# Lean: Corpus.Sequences.lookAndSayNext
def look_and_say_next(xs_1585: list[int]) -> list[int]:
    def _f_32229():
        _x_32228 = []
        return _x_32228
    _alt_32230 = _f_32229
    def _f_32237(x_1587: int, rest_1588: list[int]):
        _x_32231 = 1
        _x_32234 = []
        _x_32235 = look_and_say_next_go(rest_1588, x_1587, 1, _x_32234)
        _x_32236 = list(reversed(_x_32235))
        return _x_32236
    _alt_32238 = _f_32237
    if len(xs_1585) == 0:
        _x_32240 = _alt_32230()
        return _x_32240
    else:
        head_32241 = xs_1585[0]
        tail_32242 = xs_1585[1:]
        _x_32243 = _alt_32238(head_32241, tail_32242)
        return _x_32243

# Lean: Corpus.Sequences.collatzSequence
def collatz_sequence(n_1589: int) -> list[int]:
    _x_32246 = 1
    _x_32249 = n_1589 <= 1
    if _x_32249:
        _x_32289 = []
        _x_32290 = [n_1589] + _x_32289
        return _x_32290
    else:
        _x_32257 = 2
        _x_32260 = n_1589 % 2
        _x_32261 = 0
        _x_32264 = _x_32260 == 0
        _x_32265 = True
        _x_32266 = _x_32264 == True
        def _jp_32287(_y_32284: int):
            _x_32285 = collatz_sequence(_y_32284)
            _x_32286 = [n_1589] + _x_32285
            return _x_32286
        if _x_32266:
            _x_32283 = n_1589 // 2
            return _jp_32287(_x_32283)
        else:
            _x_32274 = 3
            _x_32277 = 3 * n_1589
            _x_32278 = _x_32277 + 1
            return _jp_32287(_x_32278)

# Lean: Corpus.Sequences.recaman
def recaman(n_1590: int) -> list[int]:
    _x_32293 = 1
    _x_32296 = 0
    _x_32299 = []
    _x_32300 = [0] + _x_32299
    _x_32301 = recaman_go(n_1590, 1, 0, _x_32300, _x_32300)
    return _x_32301

# Lean: Corpus.Sequences.sylvester
def sylvester(n_1591: int) -> int:
    _x_32306 = 0
    _x_32309 = n_1591 == 0
    _x_32310 = True
    _x_32311 = _x_32309 == True
    if _x_32311:
        _x_32331 = 2
        return 2
    else:
        _x_32316 = 1
        _x_32319 = n_1591 - 1
        _x_32320 = sylvester(_x_32319)
        _x_32327 = _x_32320 * _x_32320
        _x_32328 = _x_32327 - _x_32320
        _x_32329 = _x_32328 + 1
        return _x_32329

# Lean: Corpus.Sequences.alcuin
def alcuin(n_1593: int) -> int:
    _x_32342 = 12
    _x_32345 = n_1593 % 12
    _x_32346 = 0
    _x_32349 = _x_32345 == 0
    _x_32350 = True
    _x_32351 = _x_32349 == True
    if _x_32351:
        _x_32433 = n_1593 * n_1593
        _x_32434 = _x_32433 // 12
        return _x_32434
    else:
        def _f_32354():
            _x_32353 = True
            return True
        _alt_32355 = _f_32354
        def _f_32360():
            _x_32356 = 9
            _x_32359 = _x_32345 == 9
            return _x_32359
        _alt_32361 = _f_32360
        _x_32362 = 3
        _x_32365 = _x_32345 == 3
        def _jp_32419(_y_32370: bool):
            _x_32371 = _y_32370 == True
            if _x_32371:
                _x_32415 = n_1593 * n_1593
                _x_32416 = _x_32415 - 3
                _x_32417 = _x_32416 // 12
                return _x_32417
            else:
                _x_32373 = 6
                _x_32376 = _x_32345 == 6
                _x_32377 = _x_32376 == True
                if _x_32377:
                    _x_32401 = n_1593 * n_1593
                    _x_32402 = _x_32401 - 12
                    _x_32403 = _x_32402 // 12
                    return _x_32403
                else:
                    _x_32388 = n_1593 * n_1593
                    _x_32389 = _x_32388 + 3
                    _x_32390 = _x_32389 // 12
                    return _x_32390
        def _jp_32425():
            _x_32424 = _alt_32355()
            return _jp_32419(_x_32424)
        def _jp_32422():
            _x_32421 = _alt_32361()
            return _jp_32419(_x_32421)
        if _x_32365:
            return _jp_32425()
        else:
            return _jp_32422()

# Lean: Corpus.Sequences.firstNPrimes
def first_nprimes(n_1596: int) -> list[int]:
    _x_32437 = 2
    _x_32440 = []
    _x_32441 = first_nprimes_go(n_1596, 2, _x_32440)
    return _x_32441

# Lean: Corpus.Sequences.vanEck
def van_eck(n_1597: int) -> list[int]:
    _x_32443 = 1
    _x_32446 = 0
    _x_32449 = []
    _x_32450 = []
    _x_32451 = [0] + _x_32450
    _x_32452 = van_eck_go(n_1597, 1, 0, _x_32449, _x_32451)
    return _x_32452

# Lean: Corpus.Sorting.bubbleSort
def bubble_sort(xs_1598: list[int]) -> list[int]:
    _x_32454 = len(xs_1598)
    _x_32455 = list(xs_1598)
    _x_32456 = 0
    _x_32459 = outer(_x_32454, 0, _x_32455)
    _x_32460 = list(_x_32459)
    return _x_32460

# Lean: Corpus.Sorting.selectionSort
def selection_sort(xs_1601: list[int]) -> list[int]:
    _x_32462 = len(xs_1601)
    _x_32463 = list(xs_1601)
    _x_32464 = 0
    _x_32467 = selection_sort_go(_x_32462, 0, _x_32463)
    _x_32468 = list(_x_32467)
    return _x_32468

# Lean: Corpus.Sorting.countingSort
def counting_sort(xs_1604: list[int], max_val_1605: int) -> list[int]:
    def _f_32482(arr_1606: list[int], x_1607: int):
        _x_32473 = 0
        _x_32476 = get_d(None, arr_1606, x_1607, 0)
        _x_32477 = 1
        _x_32480 = _x_32476 + 1
        _x_32481 = set_(None, arr_1606, x_1607, _x_32480)
        return _x_32481
    _x_32486 = 1
    _x_32489 = max_val_1605 + 1
    _x_32490 = 0
    _x_32493 = array_replicate(None, _x_32489, 0)
    _x_32494 = functools.reduce(_f_32482, xs_1604, _x_32493)
    _x_32495 = []
    _x_32496 = expand(max_val_1605, _x_32494, 0, _x_32495)
    return _x_32496

# Lean: Corpus.Sorting.radixSort
def radix_sort(xs_1609: list[int]) -> list[int]:
    _x_32499 = max
    _x_32500 = 0
    _x_32503 = functools.reduce(_x_32499, xs_1609, 0)
    _x_32504 = 1
    _x_32507 = radix_sort_go(_x_32503, 1, xs_1609)
    return _x_32507

# Lean: Corpus.Sorting.gnomeSort
def gnome_sort(xs_1611: list[int]) -> list[int]:
    _x_32509 = len(xs_1611)
    _x_32510 = list(xs_1611)
    _x_32511 = 0
    _x_32514 = gnome_sort_go(_x_32509, 0, _x_32510)
    _x_32515 = list(_x_32514)
    return _x_32515

# Lean: Corpus.Sorting.isSorted
def is_sorted(xs_1614: list[int]) -> bool:
    while True:
        def _f_32518():
            _x_32517 = True
            return True
        _alt_32519 = _f_32518
        def _f_32522(head_32520: int):
            _x_32521 = True
            return True
        _alt_32523 = _f_32522
        if len(xs_1614) == 0:
            _x_32541 = _alt_32519()
            return _x_32541
        else:
            head_32542 = xs_1614[0]
            tail_32543 = xs_1614[1:]
            if len(tail_32543) == 0:
                _x_32544 = _alt_32523(head_32542)
                return _x_32544
            else:
                head_32545 = tail_32543[0]
                tail_32546 = tail_32543[1:]
                x_1616 = head_32542
                y_1617 = head_32545
                rest_1618 = tail_32546
                def _f_32525():
                    _x_32524 = False
                    return False
                _alt_32526 = _f_32525
                _x_32531 = x_1616 <= y_1617
                if _x_32531:
                    _x_32527 = [y_1617] + rest_1618
                    xs_1614 = _x_32527
                    continue
                else:
                    _x_32534 = _alt_32526()
                    return _x_32534

# Lean: Corpus.Sorting.isSortedDesc
def is_sorted_desc(xs_1621: list[int]) -> bool:
    while True:
        def _f_32552():
            _x_32551 = True
            return True
        _alt_32553 = _f_32552
        def _f_32556(head_32554: int):
            _x_32555 = True
            return True
        _alt_32557 = _f_32556
        if len(xs_1621) == 0:
            _x_32575 = _alt_32553()
            return _x_32575
        else:
            head_32576 = xs_1621[0]
            tail_32577 = xs_1621[1:]
            if len(tail_32577) == 0:
                _x_32578 = _alt_32557(head_32576)
                return _x_32578
            else:
                head_32579 = tail_32577[0]
                tail_32580 = tail_32577[1:]
                x_1623 = head_32576
                y_1624 = head_32579
                rest_1625 = tail_32580
                def _f_32559():
                    _x_32558 = False
                    return False
                _alt_32560 = _f_32559
                _x_32565 = y_1624 <= x_1623
                if _x_32565:
                    _x_32561 = [y_1624] + rest_1625
                    xs_1621 = _x_32561
                    continue
                else:
                    _x_32568 = _alt_32560()
                    return _x_32568

# Lean: Corpus.Sorting.findMin
def find_min(xs_1628: list[int]) -> int | None:
    def _f_32605(acc_1629: int | None, x_1630: int):
        def _f_32585():
            return x_1630
        _alt_32586 = _f_32585
        def _f_32590(m_1632: int):
            _x_32588 = min
            _x_32589 = _x_32588(m_1632, x_1630)
            return _x_32589
        _alt_32591 = _f_32590
        def _jp_32598(_y_32596: int):
            _x_32597 = _y_32596
            return _x_32597
        def _jp_32601():
            _x_32600 = _alt_32586()
            return _jp_32598(_x_32600)
        def _jp_32604(_y_32602: int):
            _x_32603 = _alt_32591(_y_32602)
            return _jp_32598(_x_32603)
        if acc_1629 is None:
            return _jp_32601()
        else:
            val_32594 = acc_1629
            return _jp_32604(val_32594)
    _x_32606 = None
    _x_32607 = functools.reduce(_f_32605, xs_1628, _x_32606)
    return _x_32607

# Lean: Corpus.Sorting.findMax
def find_max(xs_1633: list[int]) -> int | None:
    def _f_32629(acc_1634: int | None, x_1635: int):
        def _f_32609():
            return x_1635
        _alt_32610 = _f_32609
        def _f_32614(m_1637: int):
            _x_32612 = max
            _x_32613 = _x_32612(m_1637, x_1635)
            return _x_32613
        _alt_32615 = _f_32614
        def _jp_32622(_y_32620: int):
            _x_32621 = _y_32620
            return _x_32621
        def _jp_32628(_y_32626: int):
            _x_32627 = _alt_32615(_y_32626)
            return _jp_32622(_x_32627)
        def _jp_32625():
            _x_32624 = _alt_32610()
            return _jp_32622(_x_32624)
        if acc_1634 is None:
            return _jp_32625()
        else:
            val_32618 = acc_1634
            return _jp_32628(val_32618)
    _x_32630 = None
    _x_32631 = functools.reduce(_f_32629, xs_1633, _x_32630)
    return _x_32631

# Lean: Corpus.Sorting.kthSmallest
def kth_smallest(xs_1638: list[int], k_1639: int) -> int | None:
    _x_32633 = insertion_sort(xs_1638)
    _x_32635 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_32636 = _x_32635(_x_32633, k_1639)
    return _x_32636

# Lean: Corpus.Sorting.kthLargest
def kth_largest(xs_1641: list[int], k_1642: int) -> int | None:
    _x_32638 = insertion_sort(xs_1641)
    _x_32639 = len(_x_32638)
    _x_32640 = _x_32639 <= k_1642
    if _x_32640:
        _x_32654 = None
        return _x_32654
    else:
        _x_32643 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_32647 = 1
        _x_32650 = _x_32639 - 1
        _x_32651 = _x_32650 - k_1642
        _x_32652 = _x_32643(_x_32638, _x_32651)
        return _x_32652

# Lean: Corpus.Sorting.median
def median(xs_1644: list[int]) -> int | None:
    _x_32657 = len(xs_1644) == 0
    _x_32658 = True
    _x_32659 = _x_32657 == True
    if _x_32659:
        _x_32674 = None
        return _x_32674
    else:
        _x_32661 = insertion_sort(xs_1644)
        _x_32662 = len(_x_32661)
        _x_32664 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_32668 = 2
        _x_32671 = _x_32662 // 2
        _x_32672 = _x_32664(_x_32661, _x_32671)
        return _x_32672

# Lean: Corpus.Sorting.mode
def mode(xs_1647: list[int]) -> int | None:
    _x_32677 = None
    _x_32678 = 0
    _x_32681 = mode_go(xs_1647, _x_32677, 0)
    return _x_32681

# Lean: Corpus.Sorting.unique
def unique(xs_1648: list[int]) -> list[int]:
    _x_32683 = []
    _x_32684 = unique_go(xs_1648, _x_32683)
    return _x_32684

# Lean: Corpus.Sorting.removeDupsSorted
def remove_dups_sorted(xs_1649: list[int]) -> list[int]:
    def _f_32687():
        _x_32686 = []
        return _x_32686
    _alt_32688 = _f_32687
    def _f_32691(x_1651: int):
        _x_32689 = []
        _x_32690 = [x_1651] + _x_32689
        return _x_32690
    _alt_32692 = _f_32691
    def _f_32707(x_1652: int, y_1653: int, rest_1654: list[int]):
        _x_32696 = x_1652 == y_1653
        _x_32697 = True
        _x_32698 = _x_32696 == True
        if _x_32698:
            _x_32704 = [y_1653] + rest_1654
            _x_32705 = remove_dups_sorted(_x_32704)
            return _x_32705
        else:
            _x_32700 = [y_1653] + rest_1654
            _x_32701 = remove_dups_sorted(_x_32700)
            _x_32702 = [x_1652] + _x_32701
            return _x_32702
    _alt_32708 = _f_32707
    if len(xs_1649) == 0:
        _x_32710 = _alt_32688()
        return _x_32710
    else:
        head_32711 = xs_1649[0]
        tail_32712 = xs_1649[1:]
        if len(tail_32712) == 0:
            _x_32713 = _alt_32692(head_32711)
            return _x_32713
        else:
            head_32714 = tail_32712[0]
            tail_32715 = tail_32712[1:]
            _x_32716 = _alt_32708(head_32711, head_32714, tail_32715)
            return _x_32716

# Lean: Corpus.Production.RBTree.singleton
def singleton(__1655: Any, x_1656: Any) -> Any:
    _x_32720 = red()
    _x_32721 = RBTree_empty()
    _x_32722 = RBTree_node(_x_32720, _x_32721, x_1656, _x_32721)
    return _x_32722

# Lean: Corpus.Production.RBTree.member
def member(__1657: Any, inst_32724: Any, x_1658: Any, x_32725: Any) -> bool:
    while True:
        def _f_32727():
            _x_32726 = False
            return False
        _alt_32728 = _f_32727
        match x_32725:
            case RBTree_empty():
                _x_32751 = _alt_32728()
                return _x_32751
            case RBTree_node(a_32752, a_32753, a_32754, a_32755):
                a_32729 = a_32752
                l_1660 = a_32753
                y_1661 = a_32754
                r_1662 = a_32755
                def _f_32734():
                    _x_32733 = True
                    return True
                _alt_32735 = _f_32734
                _x_32739 = inst_32724.field_0
                _x_32740 = _x_32739(x_1658, y_1661)
                match _x_32740:
                    case lt():
                        return member(None, inst_32724, x_1658, l_1660)
                    case eq():
                        _x_32744 = _alt_32735()
                        return _x_32744
                    case gt():
                        return member(None, inst_32724, x_1658, r_1662)

# Lean: Corpus.Production.RBTree.balance
def balance(__1666: Any, x_32759: Color, x_32760: Any, x_32761: Any, x_32762: Any) -> Any:
    def _f_32768(a_1667: Any, x_1668: Any, b_1669: Any, y_1670: Any, c_1671: Any, z_1672: Any, d_1673: Any):
        _x_32763 = red()
        _x_32764 = black()
        _x_32765 = RBTree_node(_x_32764, a_1667, x_1668, b_1669)
        _x_32766 = RBTree_node(_x_32764, c_1671, z_1672, d_1673)
        _x_32767 = RBTree_node(_x_32763, _x_32765, y_1670, _x_32766)
        return _x_32767
    _alt_32769 = _f_32768
    _alt_32770 = _f_32768
    _alt_32771 = _f_32768
    _alt_32772 = _f_32768
    def _f_32774(c_1674: Color, l_1675: Any, x_1676: Any, r_1677: Any):
        _x_32773 = RBTree_node(c_1674, l_1675, x_1676, r_1677)
        return _x_32773
    _alt_32775 = _f_32774
    match x_32759:
        case black():
            match x_32760:
                case RBTree_node(a_32776, a_32777, a_32778, a_32779):
                    match a_32776:
                        case red():
                            match a_32777:
                                case RBTree_node(a_32780, a_32781, a_32782, a_32783):
                                    match a_32780:
                                        case red():
                                            _x_32784 = _alt_32769(a_32781, a_32782, a_32783, a_32778, a_32779, x_32761, x_32762)
                                            return _x_32784
                                        case _:
                                            def _f_33009(h_32785: Any):
                                                match a_32779:
                                                    case RBTree_node(a_32786, a_32787, a_32788, a_32789):
                                                        match a_32786:
                                                            case red():
                                                                _x_32790 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                _x_32791 = _alt_32770(_x_32790, a_32778, a_32787, a_32788, a_32789, x_32761, x_32762)
                                                                return _x_32791
                                                            case _:
                                                                def _f_32902(h_32792: Any):
                                                                    match x_32762:
                                                                        case RBTree_node(a_32793, a_32794, a_32795, a_32796):
                                                                            match a_32793:
                                                                                case red():
                                                                                    match a_32794:
                                                                                        case RBTree_node(a_32797, a_32798, a_32799, a_32800):
                                                                                            match a_32797:
                                                                                                case red():
                                                                                                    _x_32801 = red()
                                                                                                    _x_32802 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                    _x_32803 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                                    _x_32804 = RBTree_node(_x_32801, _x_32802, a_32778, _x_32803)
                                                                                                    _x_32805 = _alt_32771(_x_32804, x_32761, a_32798, a_32799, a_32800, a_32795, a_32796)
                                                                                                    return _x_32805
                                                                                                case _:
                                                                                                    def _f_32842(h_32806: Any):
                                                                                                        match a_32796:
                                                                                                            case RBTree_node(a_32807, a_32808, a_32809, a_32810):
                                                                                                                match a_32807:
                                                                                                                    case red():
                                                                                                                        _x_32811 = red()
                                                                                                                        _x_32812 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                                        _x_32813 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                                                        _x_32814 = RBTree_node(_x_32811, _x_32812, a_32778, _x_32813)
                                                                                                                        _x_32815 = RBTree_node(a_32797, a_32798, a_32799, a_32800)
                                                                                                                        _x_32816 = _alt_32772(_x_32814, x_32761, _x_32815, a_32795, a_32808, a_32809, a_32810)
                                                                                                                        return _x_32816
                                                                                                                    case _:
                                                                                                                        def _f_32827(h_32817: Any):
                                                                                                                            _x_32818 = black()
                                                                                                                            _x_32819 = red()
                                                                                                                            _x_32820 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                                            _x_32821 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                                                            _x_32822 = RBTree_node(_x_32819, _x_32820, a_32778, _x_32821)
                                                                                                                            _x_32823 = RBTree_node(a_32797, a_32798, a_32799, a_32800)
                                                                                                                            _x_32824 = RBTree_node(a_32807, a_32808, a_32809, a_32810)
                                                                                                                            _x_32825 = RBTree_node(_x_32819, _x_32823, a_32795, _x_32824)
                                                                                                                            _x_32826 = _alt_32775(_x_32818, _x_32822, x_32761, _x_32825)
                                                                                                                            return _x_32826
                                                                                                                        _x_32828 = _f_32827(None)
                                                                                                                        return _x_32828
                                                                                                            case _:
                                                                                                                def _f_32839(h_32830: Any):
                                                                                                                    _x_32831 = black()
                                                                                                                    _x_32832 = red()
                                                                                                                    _x_32833 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                                    _x_32834 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                                                    _x_32835 = RBTree_node(_x_32832, _x_32833, a_32778, _x_32834)
                                                                                                                    _x_32836 = RBTree_node(a_32797, a_32798, a_32799, a_32800)
                                                                                                                    _x_32837 = RBTree_node(_x_32832, _x_32836, a_32795, a_32796)
                                                                                                                    _x_32838 = _alt_32775(_x_32831, _x_32835, x_32761, _x_32837)
                                                                                                                    return _x_32838
                                                                                                                _x_32840 = _f_32839(None)
                                                                                                                return _x_32840
                                                                                                    _x_32843 = _f_32842(None)
                                                                                                    return _x_32843
                                                                                        case _:
                                                                                            def _f_32878(h_32845: Any):
                                                                                                match a_32796:
                                                                                                    case RBTree_node(a_32846, a_32847, a_32848, a_32849):
                                                                                                        match a_32846:
                                                                                                            case red():
                                                                                                                _x_32850 = red()
                                                                                                                _x_32851 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                                _x_32852 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                                                _x_32853 = RBTree_node(_x_32850, _x_32851, a_32778, _x_32852)
                                                                                                                _x_32854 = _alt_32772(_x_32853, x_32761, a_32794, a_32795, a_32847, a_32848, a_32849)
                                                                                                                return _x_32854
                                                                                                            case _:
                                                                                                                def _f_32864(h_32855: Any):
                                                                                                                    _x_32856 = black()
                                                                                                                    _x_32857 = red()
                                                                                                                    _x_32858 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                                    _x_32859 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                                                    _x_32860 = RBTree_node(_x_32857, _x_32858, a_32778, _x_32859)
                                                                                                                    _x_32861 = RBTree_node(a_32846, a_32847, a_32848, a_32849)
                                                                                                                    _x_32862 = RBTree_node(_x_32857, a_32794, a_32795, _x_32861)
                                                                                                                    _x_32863 = _alt_32775(_x_32856, _x_32860, x_32761, _x_32862)
                                                                                                                    return _x_32863
                                                                                                                _x_32865 = _f_32864(None)
                                                                                                                return _x_32865
                                                                                                    case _:
                                                                                                        def _f_32875(h_32867: Any):
                                                                                                            _x_32868 = black()
                                                                                                            _x_32869 = red()
                                                                                                            _x_32870 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                            _x_32871 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                                            _x_32872 = RBTree_node(_x_32869, _x_32870, a_32778, _x_32871)
                                                                                                            _x_32873 = RBTree_node(_x_32869, a_32794, a_32795, a_32796)
                                                                                                            _x_32874 = _alt_32775(_x_32868, _x_32872, x_32761, _x_32873)
                                                                                                            return _x_32874
                                                                                                        _x_32876 = _f_32875(None)
                                                                                                        return _x_32876
                                                                                            _x_32879 = _f_32878(None)
                                                                                            return _x_32879
                                                                                case _:
                                                                                    def _f_32889(h_32881: Any):
                                                                                        _x_32882 = black()
                                                                                        _x_32883 = red()
                                                                                        _x_32884 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                        _x_32885 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                        _x_32886 = RBTree_node(_x_32883, _x_32884, a_32778, _x_32885)
                                                                                        _x_32887 = RBTree_node(a_32793, a_32794, a_32795, a_32796)
                                                                                        _x_32888 = _alt_32775(_x_32882, _x_32886, x_32761, _x_32887)
                                                                                        return _x_32888
                                                                                    _x_32890 = _f_32889(None)
                                                                                    return _x_32890
                                                                        case _:
                                                                            def _f_32899(h_32892: Any):
                                                                                _x_32893 = black()
                                                                                _x_32894 = red()
                                                                                _x_32895 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                _x_32896 = RBTree_node(a_32786, a_32787, a_32788, a_32789)
                                                                                _x_32897 = RBTree_node(_x_32894, _x_32895, a_32778, _x_32896)
                                                                                _x_32898 = _alt_32775(_x_32893, _x_32897, x_32761, x_32762)
                                                                                return _x_32898
                                                                            _x_32900 = _f_32899(None)
                                                                            return _x_32900
                                                                _x_32903 = _f_32902(None)
                                                                return _x_32903
                                                    case _:
                                                        def _f_33006(h_32905: Any):
                                                            match x_32762:
                                                                case RBTree_node(a_32906, a_32907, a_32908, a_32909):
                                                                    match a_32906:
                                                                        case red():
                                                                            match a_32907:
                                                                                case RBTree_node(a_32910, a_32911, a_32912, a_32913):
                                                                                    match a_32910:
                                                                                        case red():
                                                                                            _x_32914 = red()
                                                                                            _x_32915 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                            _x_32916 = RBTree_node(_x_32914, _x_32915, a_32778, a_32779)
                                                                                            _x_32917 = _alt_32771(_x_32916, x_32761, a_32911, a_32912, a_32913, a_32908, a_32909)
                                                                                            return _x_32917
                                                                                        case _:
                                                                                            def _f_32951(h_32918: Any):
                                                                                                match a_32909:
                                                                                                    case RBTree_node(a_32919, a_32920, a_32921, a_32922):
                                                                                                        match a_32919:
                                                                                                            case red():
                                                                                                                _x_32923 = red()
                                                                                                                _x_32924 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                                _x_32925 = RBTree_node(_x_32923, _x_32924, a_32778, a_32779)
                                                                                                                _x_32926 = RBTree_node(a_32910, a_32911, a_32912, a_32913)
                                                                                                                _x_32927 = _alt_32772(_x_32925, x_32761, _x_32926, a_32908, a_32920, a_32921, a_32922)
                                                                                                                return _x_32927
                                                                                                            case _:
                                                                                                                def _f_32937(h_32928: Any):
                                                                                                                    _x_32929 = black()
                                                                                                                    _x_32930 = red()
                                                                                                                    _x_32931 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                                    _x_32932 = RBTree_node(_x_32930, _x_32931, a_32778, a_32779)
                                                                                                                    _x_32933 = RBTree_node(a_32910, a_32911, a_32912, a_32913)
                                                                                                                    _x_32934 = RBTree_node(a_32919, a_32920, a_32921, a_32922)
                                                                                                                    _x_32935 = RBTree_node(_x_32930, _x_32933, a_32908, _x_32934)
                                                                                                                    _x_32936 = _alt_32775(_x_32929, _x_32932, x_32761, _x_32935)
                                                                                                                    return _x_32936
                                                                                                                _x_32938 = _f_32937(None)
                                                                                                                return _x_32938
                                                                                                    case _:
                                                                                                        def _f_32948(h_32940: Any):
                                                                                                            _x_32941 = black()
                                                                                                            _x_32942 = red()
                                                                                                            _x_32943 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                            _x_32944 = RBTree_node(_x_32942, _x_32943, a_32778, a_32779)
                                                                                                            _x_32945 = RBTree_node(a_32910, a_32911, a_32912, a_32913)
                                                                                                            _x_32946 = RBTree_node(_x_32942, _x_32945, a_32908, a_32909)
                                                                                                            _x_32947 = _alt_32775(_x_32941, _x_32944, x_32761, _x_32946)
                                                                                                            return _x_32947
                                                                                                        _x_32949 = _f_32948(None)
                                                                                                        return _x_32949
                                                                                            _x_32952 = _f_32951(None)
                                                                                            return _x_32952
                                                                                case _:
                                                                                    def _f_32984(h_32954: Any):
                                                                                        match a_32909:
                                                                                            case RBTree_node(a_32955, a_32956, a_32957, a_32958):
                                                                                                match a_32955:
                                                                                                    case red():
                                                                                                        _x_32959 = red()
                                                                                                        _x_32960 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                        _x_32961 = RBTree_node(_x_32959, _x_32960, a_32778, a_32779)
                                                                                                        _x_32962 = _alt_32772(_x_32961, x_32761, a_32907, a_32908, a_32956, a_32957, a_32958)
                                                                                                        return _x_32962
                                                                                                    case _:
                                                                                                        def _f_32971(h_32963: Any):
                                                                                                            _x_32964 = black()
                                                                                                            _x_32965 = red()
                                                                                                            _x_32966 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                            _x_32967 = RBTree_node(_x_32965, _x_32966, a_32778, a_32779)
                                                                                                            _x_32968 = RBTree_node(a_32955, a_32956, a_32957, a_32958)
                                                                                                            _x_32969 = RBTree_node(_x_32965, a_32907, a_32908, _x_32968)
                                                                                                            _x_32970 = _alt_32775(_x_32964, _x_32967, x_32761, _x_32969)
                                                                                                            return _x_32970
                                                                                                        _x_32972 = _f_32971(None)
                                                                                                        return _x_32972
                                                                                            case _:
                                                                                                def _f_32981(h_32974: Any):
                                                                                                    _x_32975 = black()
                                                                                                    _x_32976 = red()
                                                                                                    _x_32977 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                                    _x_32978 = RBTree_node(_x_32976, _x_32977, a_32778, a_32779)
                                                                                                    _x_32979 = RBTree_node(_x_32976, a_32907, a_32908, a_32909)
                                                                                                    _x_32980 = _alt_32775(_x_32975, _x_32978, x_32761, _x_32979)
                                                                                                    return _x_32980
                                                                                                _x_32982 = _f_32981(None)
                                                                                                return _x_32982
                                                                                    _x_32985 = _f_32984(None)
                                                                                    return _x_32985
                                                                        case _:
                                                                            def _f_32994(h_32987: Any):
                                                                                _x_32988 = black()
                                                                                _x_32989 = red()
                                                                                _x_32990 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                                _x_32991 = RBTree_node(_x_32989, _x_32990, a_32778, a_32779)
                                                                                _x_32992 = RBTree_node(a_32906, a_32907, a_32908, a_32909)
                                                                                _x_32993 = _alt_32775(_x_32988, _x_32991, x_32761, _x_32992)
                                                                                return _x_32993
                                                                            _x_32995 = _f_32994(None)
                                                                            return _x_32995
                                                                case _:
                                                                    def _f_33003(h_32997: Any):
                                                                        _x_32998 = black()
                                                                        _x_32999 = red()
                                                                        _x_33000 = RBTree_node(a_32780, a_32781, a_32782, a_32783)
                                                                        _x_33001 = RBTree_node(_x_32999, _x_33000, a_32778, a_32779)
                                                                        _x_33002 = _alt_32775(_x_32998, _x_33001, x_32761, x_32762)
                                                                        return _x_33002
                                                                    _x_33004 = _f_33003(None)
                                                                    return _x_33004
                                                        _x_33007 = _f_33006(None)
                                                        return _x_33007
                                            _x_33010 = _f_33009(None)
                                            return _x_33010
                                case _:
                                    def _f_33217(h_33012: Any):
                                        match a_32779:
                                            case RBTree_node(a_33013, a_33014, a_33015, a_33016):
                                                match a_33013:
                                                    case red():
                                                        _x_33017 = _alt_32770(a_32777, a_32778, a_33014, a_33015, a_33016, x_32761, x_32762)
                                                        return _x_33017
                                                    case _:
                                                        def _f_33119(h_33018: Any):
                                                            match x_32762:
                                                                case RBTree_node(a_33019, a_33020, a_33021, a_33022):
                                                                    match a_33019:
                                                                        case red():
                                                                            match a_33020:
                                                                                case RBTree_node(a_33023, a_33024, a_33025, a_33026):
                                                                                    match a_33023:
                                                                                        case red():
                                                                                            _x_33027 = red()
                                                                                            _x_33028 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                            _x_33029 = RBTree_node(_x_33027, a_32777, a_32778, _x_33028)
                                                                                            _x_33030 = _alt_32771(_x_33029, x_32761, a_33024, a_33025, a_33026, a_33021, a_33022)
                                                                                            return _x_33030
                                                                                        case _:
                                                                                            def _f_33064(h_33031: Any):
                                                                                                match a_33022:
                                                                                                    case RBTree_node(a_33032, a_33033, a_33034, a_33035):
                                                                                                        match a_33032:
                                                                                                            case red():
                                                                                                                _x_33036 = red()
                                                                                                                _x_33037 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                                                _x_33038 = RBTree_node(_x_33036, a_32777, a_32778, _x_33037)
                                                                                                                _x_33039 = RBTree_node(a_33023, a_33024, a_33025, a_33026)
                                                                                                                _x_33040 = _alt_32772(_x_33038, x_32761, _x_33039, a_33021, a_33033, a_33034, a_33035)
                                                                                                                return _x_33040
                                                                                                            case _:
                                                                                                                def _f_33050(h_33041: Any):
                                                                                                                    _x_33042 = black()
                                                                                                                    _x_33043 = red()
                                                                                                                    _x_33044 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                                                    _x_33045 = RBTree_node(_x_33043, a_32777, a_32778, _x_33044)
                                                                                                                    _x_33046 = RBTree_node(a_33023, a_33024, a_33025, a_33026)
                                                                                                                    _x_33047 = RBTree_node(a_33032, a_33033, a_33034, a_33035)
                                                                                                                    _x_33048 = RBTree_node(_x_33043, _x_33046, a_33021, _x_33047)
                                                                                                                    _x_33049 = _alt_32775(_x_33042, _x_33045, x_32761, _x_33048)
                                                                                                                    return _x_33049
                                                                                                                _x_33051 = _f_33050(None)
                                                                                                                return _x_33051
                                                                                                    case _:
                                                                                                        def _f_33061(h_33053: Any):
                                                                                                            _x_33054 = black()
                                                                                                            _x_33055 = red()
                                                                                                            _x_33056 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                                            _x_33057 = RBTree_node(_x_33055, a_32777, a_32778, _x_33056)
                                                                                                            _x_33058 = RBTree_node(a_33023, a_33024, a_33025, a_33026)
                                                                                                            _x_33059 = RBTree_node(_x_33055, _x_33058, a_33021, a_33022)
                                                                                                            _x_33060 = _alt_32775(_x_33054, _x_33057, x_32761, _x_33059)
                                                                                                            return _x_33060
                                                                                                        _x_33062 = _f_33061(None)
                                                                                                        return _x_33062
                                                                                            _x_33065 = _f_33064(None)
                                                                                            return _x_33065
                                                                                case _:
                                                                                    def _f_33097(h_33067: Any):
                                                                                        match a_33022:
                                                                                            case RBTree_node(a_33068, a_33069, a_33070, a_33071):
                                                                                                match a_33068:
                                                                                                    case red():
                                                                                                        _x_33072 = red()
                                                                                                        _x_33073 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                                        _x_33074 = RBTree_node(_x_33072, a_32777, a_32778, _x_33073)
                                                                                                        _x_33075 = _alt_32772(_x_33074, x_32761, a_33020, a_33021, a_33069, a_33070, a_33071)
                                                                                                        return _x_33075
                                                                                                    case _:
                                                                                                        def _f_33084(h_33076: Any):
                                                                                                            _x_33077 = black()
                                                                                                            _x_33078 = red()
                                                                                                            _x_33079 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                                            _x_33080 = RBTree_node(_x_33078, a_32777, a_32778, _x_33079)
                                                                                                            _x_33081 = RBTree_node(a_33068, a_33069, a_33070, a_33071)
                                                                                                            _x_33082 = RBTree_node(_x_33078, a_33020, a_33021, _x_33081)
                                                                                                            _x_33083 = _alt_32775(_x_33077, _x_33080, x_32761, _x_33082)
                                                                                                            return _x_33083
                                                                                                        _x_33085 = _f_33084(None)
                                                                                                        return _x_33085
                                                                                            case _:
                                                                                                def _f_33094(h_33087: Any):
                                                                                                    _x_33088 = black()
                                                                                                    _x_33089 = red()
                                                                                                    _x_33090 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                                    _x_33091 = RBTree_node(_x_33089, a_32777, a_32778, _x_33090)
                                                                                                    _x_33092 = RBTree_node(_x_33089, a_33020, a_33021, a_33022)
                                                                                                    _x_33093 = _alt_32775(_x_33088, _x_33091, x_32761, _x_33092)
                                                                                                    return _x_33093
                                                                                                _x_33095 = _f_33094(None)
                                                                                                return _x_33095
                                                                                    _x_33098 = _f_33097(None)
                                                                                    return _x_33098
                                                                        case _:
                                                                            def _f_33107(h_33100: Any):
                                                                                _x_33101 = black()
                                                                                _x_33102 = red()
                                                                                _x_33103 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                                _x_33104 = RBTree_node(_x_33102, a_32777, a_32778, _x_33103)
                                                                                _x_33105 = RBTree_node(a_33019, a_33020, a_33021, a_33022)
                                                                                _x_33106 = _alt_32775(_x_33101, _x_33104, x_32761, _x_33105)
                                                                                return _x_33106
                                                                            _x_33108 = _f_33107(None)
                                                                            return _x_33108
                                                                case _:
                                                                    def _f_33116(h_33110: Any):
                                                                        _x_33111 = black()
                                                                        _x_33112 = red()
                                                                        _x_33113 = RBTree_node(a_33013, a_33014, a_33015, a_33016)
                                                                        _x_33114 = RBTree_node(_x_33112, a_32777, a_32778, _x_33113)
                                                                        _x_33115 = _alt_32775(_x_33111, _x_33114, x_32761, x_32762)
                                                                        return _x_33115
                                                                    _x_33117 = _f_33116(None)
                                                                    return _x_33117
                                                        _x_33120 = _f_33119(None)
                                                        return _x_33120
                                            case _:
                                                def _f_33214(h_33122: Any):
                                                    match x_32762:
                                                        case RBTree_node(a_33123, a_33124, a_33125, a_33126):
                                                            match a_33123:
                                                                case red():
                                                                    match a_33124:
                                                                        case RBTree_node(a_33127, a_33128, a_33129, a_33130):
                                                                            match a_33127:
                                                                                case red():
                                                                                    _x_33131 = red()
                                                                                    _x_33132 = RBTree_node(_x_33131, a_32777, a_32778, a_32779)
                                                                                    _x_33133 = _alt_32771(_x_33132, x_32761, a_33128, a_33129, a_33130, a_33125, a_33126)
                                                                                    return _x_33133
                                                                                case _:
                                                                                    def _f_33164(h_33134: Any):
                                                                                        match a_33126:
                                                                                            case RBTree_node(a_33135, a_33136, a_33137, a_33138):
                                                                                                match a_33135:
                                                                                                    case red():
                                                                                                        _x_33139 = red()
                                                                                                        _x_33140 = RBTree_node(_x_33139, a_32777, a_32778, a_32779)
                                                                                                        _x_33141 = RBTree_node(a_33127, a_33128, a_33129, a_33130)
                                                                                                        _x_33142 = _alt_32772(_x_33140, x_32761, _x_33141, a_33125, a_33136, a_33137, a_33138)
                                                                                                        return _x_33142
                                                                                                    case _:
                                                                                                        def _f_33151(h_33143: Any):
                                                                                                            _x_33144 = black()
                                                                                                            _x_33145 = red()
                                                                                                            _x_33146 = RBTree_node(_x_33145, a_32777, a_32778, a_32779)
                                                                                                            _x_33147 = RBTree_node(a_33127, a_33128, a_33129, a_33130)
                                                                                                            _x_33148 = RBTree_node(a_33135, a_33136, a_33137, a_33138)
                                                                                                            _x_33149 = RBTree_node(_x_33145, _x_33147, a_33125, _x_33148)
                                                                                                            _x_33150 = _alt_32775(_x_33144, _x_33146, x_32761, _x_33149)
                                                                                                            return _x_33150
                                                                                                        _x_33152 = _f_33151(None)
                                                                                                        return _x_33152
                                                                                            case _:
                                                                                                def _f_33161(h_33154: Any):
                                                                                                    _x_33155 = black()
                                                                                                    _x_33156 = red()
                                                                                                    _x_33157 = RBTree_node(_x_33156, a_32777, a_32778, a_32779)
                                                                                                    _x_33158 = RBTree_node(a_33127, a_33128, a_33129, a_33130)
                                                                                                    _x_33159 = RBTree_node(_x_33156, _x_33158, a_33125, a_33126)
                                                                                                    _x_33160 = _alt_32775(_x_33155, _x_33157, x_32761, _x_33159)
                                                                                                    return _x_33160
                                                                                                _x_33162 = _f_33161(None)
                                                                                                return _x_33162
                                                                                    _x_33165 = _f_33164(None)
                                                                                    return _x_33165
                                                                        case _:
                                                                            def _f_33194(h_33167: Any):
                                                                                match a_33126:
                                                                                    case RBTree_node(a_33168, a_33169, a_33170, a_33171):
                                                                                        match a_33168:
                                                                                            case red():
                                                                                                _x_33172 = red()
                                                                                                _x_33173 = RBTree_node(_x_33172, a_32777, a_32778, a_32779)
                                                                                                _x_33174 = _alt_32772(_x_33173, x_32761, a_33124, a_33125, a_33169, a_33170, a_33171)
                                                                                                return _x_33174
                                                                                            case _:
                                                                                                def _f_33182(h_33175: Any):
                                                                                                    _x_33176 = black()
                                                                                                    _x_33177 = red()
                                                                                                    _x_33178 = RBTree_node(_x_33177, a_32777, a_32778, a_32779)
                                                                                                    _x_33179 = RBTree_node(a_33168, a_33169, a_33170, a_33171)
                                                                                                    _x_33180 = RBTree_node(_x_33177, a_33124, a_33125, _x_33179)
                                                                                                    _x_33181 = _alt_32775(_x_33176, _x_33178, x_32761, _x_33180)
                                                                                                    return _x_33181
                                                                                                _x_33183 = _f_33182(None)
                                                                                                return _x_33183
                                                                                    case _:
                                                                                        def _f_33191(h_33185: Any):
                                                                                            _x_33186 = black()
                                                                                            _x_33187 = red()
                                                                                            _x_33188 = RBTree_node(_x_33187, a_32777, a_32778, a_32779)
                                                                                            _x_33189 = RBTree_node(_x_33187, a_33124, a_33125, a_33126)
                                                                                            _x_33190 = _alt_32775(_x_33186, _x_33188, x_32761, _x_33189)
                                                                                            return _x_33190
                                                                                        _x_33192 = _f_33191(None)
                                                                                        return _x_33192
                                                                            _x_33195 = _f_33194(None)
                                                                            return _x_33195
                                                                case _:
                                                                    def _f_33203(h_33197: Any):
                                                                        _x_33198 = black()
                                                                        _x_33199 = red()
                                                                        _x_33200 = RBTree_node(_x_33199, a_32777, a_32778, a_32779)
                                                                        _x_33201 = RBTree_node(a_33123, a_33124, a_33125, a_33126)
                                                                        _x_33202 = _alt_32775(_x_33198, _x_33200, x_32761, _x_33201)
                                                                        return _x_33202
                                                                    _x_33204 = _f_33203(None)
                                                                    return _x_33204
                                                        case _:
                                                            def _f_33211(h_33206: Any):
                                                                _x_33207 = black()
                                                                _x_33208 = red()
                                                                _x_33209 = RBTree_node(_x_33208, a_32777, a_32778, a_32779)
                                                                _x_33210 = _alt_32775(_x_33207, _x_33209, x_32761, x_32762)
                                                                return _x_33210
                                                            _x_33212 = _f_33211(None)
                                                            return _x_33212
                                                _x_33215 = _f_33214(None)
                                                return _x_33215
                                    _x_33218 = _f_33217(None)
                                    return _x_33218
                        case _:
                            def _f_33307(h_33220: Any):
                                match x_32762:
                                    case RBTree_node(a_33221, a_33222, a_33223, a_33224):
                                        match a_33221:
                                            case red():
                                                match a_33222:
                                                    case RBTree_node(a_33225, a_33226, a_33227, a_33228):
                                                        match a_33225:
                                                            case red():
                                                                _x_33229 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                                _x_33230 = _alt_32771(_x_33229, x_32761, a_33226, a_33227, a_33228, a_33223, a_33224)
                                                                return _x_33230
                                                            case _:
                                                                def _f_33260(h_33231: Any):
                                                                    match a_33224:
                                                                        case RBTree_node(a_33232, a_33233, a_33234, a_33235):
                                                                            match a_33232:
                                                                                case red():
                                                                                    _x_33236 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                                                    _x_33237 = RBTree_node(a_33225, a_33226, a_33227, a_33228)
                                                                                    _x_33238 = _alt_32772(_x_33236, x_32761, _x_33237, a_33223, a_33233, a_33234, a_33235)
                                                                                    return _x_33238
                                                                                case _:
                                                                                    def _f_33247(h_33239: Any):
                                                                                        _x_33240 = black()
                                                                                        _x_33241 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                                                        _x_33242 = red()
                                                                                        _x_33243 = RBTree_node(a_33225, a_33226, a_33227, a_33228)
                                                                                        _x_33244 = RBTree_node(a_33232, a_33233, a_33234, a_33235)
                                                                                        _x_33245 = RBTree_node(_x_33242, _x_33243, a_33223, _x_33244)
                                                                                        _x_33246 = _alt_32775(_x_33240, _x_33241, x_32761, _x_33245)
                                                                                        return _x_33246
                                                                                    _x_33248 = _f_33247(None)
                                                                                    return _x_33248
                                                                        case _:
                                                                            def _f_33257(h_33250: Any):
                                                                                _x_33251 = black()
                                                                                _x_33252 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                                                _x_33253 = red()
                                                                                _x_33254 = RBTree_node(a_33225, a_33226, a_33227, a_33228)
                                                                                _x_33255 = RBTree_node(_x_33253, _x_33254, a_33223, a_33224)
                                                                                _x_33256 = _alt_32775(_x_33251, _x_33252, x_32761, _x_33255)
                                                                                return _x_33256
                                                                            _x_33258 = _f_33257(None)
                                                                            return _x_33258
                                                                _x_33261 = _f_33260(None)
                                                                return _x_33261
                                                    case _:
                                                        def _f_33289(h_33263: Any):
                                                            match a_33224:
                                                                case RBTree_node(a_33264, a_33265, a_33266, a_33267):
                                                                    match a_33264:
                                                                        case red():
                                                                            _x_33268 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                                            _x_33269 = _alt_32772(_x_33268, x_32761, a_33222, a_33223, a_33265, a_33266, a_33267)
                                                                            return _x_33269
                                                                        case _:
                                                                            def _f_33277(h_33270: Any):
                                                                                _x_33271 = black()
                                                                                _x_33272 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                                                _x_33273 = red()
                                                                                _x_33274 = RBTree_node(a_33264, a_33265, a_33266, a_33267)
                                                                                _x_33275 = RBTree_node(_x_33273, a_33222, a_33223, _x_33274)
                                                                                _x_33276 = _alt_32775(_x_33271, _x_33272, x_32761, _x_33275)
                                                                                return _x_33276
                                                                            _x_33278 = _f_33277(None)
                                                                            return _x_33278
                                                                case _:
                                                                    def _f_33286(h_33280: Any):
                                                                        _x_33281 = black()
                                                                        _x_33282 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                                        _x_33283 = red()
                                                                        _x_33284 = RBTree_node(_x_33283, a_33222, a_33223, a_33224)
                                                                        _x_33285 = _alt_32775(_x_33281, _x_33282, x_32761, _x_33284)
                                                                        return _x_33285
                                                                    _x_33287 = _f_33286(None)
                                                                    return _x_33287
                                                        _x_33290 = _f_33289(None)
                                                        return _x_33290
                                            case _:
                                                def _f_33297(h_33292: Any):
                                                    _x_33293 = black()
                                                    _x_33294 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                                    _x_33295 = RBTree_node(a_33221, a_33222, a_33223, a_33224)
                                                    _x_33296 = _alt_32775(_x_33293, _x_33294, x_32761, _x_33295)
                                                    return _x_33296
                                                _x_33298 = _f_33297(None)
                                                return _x_33298
                                    case _:
                                        def _f_33304(h_33300: Any):
                                            _x_33301 = black()
                                            _x_33302 = RBTree_node(a_32776, a_32777, a_32778, a_32779)
                                            _x_33303 = _alt_32775(_x_33301, _x_33302, x_32761, x_32762)
                                            return _x_33303
                                        _x_33305 = _f_33304(None)
                                        return _x_33305
                            _x_33308 = _f_33307(None)
                            return _x_33308
                case _:
                    def _f_33388(h_33310: Any):
                        match x_32762:
                            case RBTree_node(a_33311, a_33312, a_33313, a_33314):
                                match a_33311:
                                    case red():
                                        match a_33312:
                                            case RBTree_node(a_33315, a_33316, a_33317, a_33318):
                                                match a_33315:
                                                    case red():
                                                        _x_33319 = _alt_32771(x_32760, x_32761, a_33316, a_33317, a_33318, a_33313, a_33314)
                                                        return _x_33319
                                                    case _:
                                                        def _f_33346(h_33320: Any):
                                                            match a_33314:
                                                                case RBTree_node(a_33321, a_33322, a_33323, a_33324):
                                                                    match a_33321:
                                                                        case red():
                                                                            _x_33325 = RBTree_node(a_33315, a_33316, a_33317, a_33318)
                                                                            _x_33326 = _alt_32772(x_32760, x_32761, _x_33325, a_33313, a_33322, a_33323, a_33324)
                                                                            return _x_33326
                                                                        case _:
                                                                            def _f_33334(h_33327: Any):
                                                                                _x_33328 = black()
                                                                                _x_33329 = red()
                                                                                _x_33330 = RBTree_node(a_33315, a_33316, a_33317, a_33318)
                                                                                _x_33331 = RBTree_node(a_33321, a_33322, a_33323, a_33324)
                                                                                _x_33332 = RBTree_node(_x_33329, _x_33330, a_33313, _x_33331)
                                                                                _x_33333 = _alt_32775(_x_33328, x_32760, x_32761, _x_33332)
                                                                                return _x_33333
                                                                            _x_33335 = _f_33334(None)
                                                                            return _x_33335
                                                                case _:
                                                                    def _f_33343(h_33337: Any):
                                                                        _x_33338 = black()
                                                                        _x_33339 = red()
                                                                        _x_33340 = RBTree_node(a_33315, a_33316, a_33317, a_33318)
                                                                        _x_33341 = RBTree_node(_x_33339, _x_33340, a_33313, a_33314)
                                                                        _x_33342 = _alt_32775(_x_33338, x_32760, x_32761, _x_33341)
                                                                        return _x_33342
                                                                    _x_33344 = _f_33343(None)
                                                                    return _x_33344
                                                        _x_33347 = _f_33346(None)
                                                        return _x_33347
                                            case _:
                                                def _f_33372(h_33349: Any):
                                                    match a_33314:
                                                        case RBTree_node(a_33350, a_33351, a_33352, a_33353):
                                                            match a_33350:
                                                                case red():
                                                                    _x_33354 = _alt_32772(x_32760, x_32761, a_33312, a_33313, a_33351, a_33352, a_33353)
                                                                    return _x_33354
                                                                case _:
                                                                    def _f_33361(h_33355: Any):
                                                                        _x_33356 = black()
                                                                        _x_33357 = red()
                                                                        _x_33358 = RBTree_node(a_33350, a_33351, a_33352, a_33353)
                                                                        _x_33359 = RBTree_node(_x_33357, a_33312, a_33313, _x_33358)
                                                                        _x_33360 = _alt_32775(_x_33356, x_32760, x_32761, _x_33359)
                                                                        return _x_33360
                                                                    _x_33362 = _f_33361(None)
                                                                    return _x_33362
                                                        case _:
                                                            def _f_33369(h_33364: Any):
                                                                _x_33365 = black()
                                                                _x_33366 = red()
                                                                _x_33367 = RBTree_node(_x_33366, a_33312, a_33313, a_33314)
                                                                _x_33368 = _alt_32775(_x_33365, x_32760, x_32761, _x_33367)
                                                                return _x_33368
                                                            _x_33370 = _f_33369(None)
                                                            return _x_33370
                                                _x_33373 = _f_33372(None)
                                                return _x_33373
                                    case _:
                                        def _f_33379(h_33375: Any):
                                            _x_33376 = black()
                                            _x_33377 = RBTree_node(a_33311, a_33312, a_33313, a_33314)
                                            _x_33378 = _alt_32775(_x_33376, x_32760, x_32761, _x_33377)
                                            return _x_33378
                                        _x_33380 = _f_33379(None)
                                        return _x_33380
                            case _:
                                def _f_33385(h_33382: Any):
                                    _x_33383 = black()
                                    _x_33384 = _alt_32775(_x_33383, x_32760, x_32761, x_32762)
                                    return _x_33384
                                _x_33386 = _f_33385(None)
                                return _x_33386
                    _x_33389 = _f_33388(None)
                    return _x_33389
        case _:
            _x_33394 = (lambda h_33391: _alt_32775(x_32759, x_32760, x_32761, x_32762))(None)
            return _x_33394

# Lean: Corpus.Production.RBTree.insertAux
def insert_aux(__1678: Any, inst_33397: Any, x_1679: Any, x_33398: Any) -> Any:
    def _f_33402():
        _x_33399 = red()
        _x_33400 = RBTree_empty()
        _x_33401 = RBTree_node(_x_33399, _x_33400, x_1679, _x_33400)
        return _x_33401
    _alt_33403 = _f_33402
    def _f_33424(c_1681: Color, l_1682: Any, y_1683: Any, r_1684: Any):
        def _f_33406():
            _x_33404 = insert_aux(None, inst_33397, x_1679, l_1682)
            _x_33405 = balance(None, c_1681, _x_33404, y_1683, r_1684)
            return _x_33405
        _alt_33407 = _f_33406
        def _f_33409():
            _x_33408 = RBTree_node(c_1681, l_1682, y_1683, r_1684)
            return _x_33408
        _alt_33410 = _f_33409
        def _f_33413():
            _x_33411 = insert_aux(None, inst_33397, x_1679, r_1684)
            _x_33412 = balance(None, c_1681, l_1682, y_1683, _x_33411)
            return _x_33412
        _alt_33414 = _f_33413
        _x_33415 = inst_33397.field_0
        _x_33416 = _x_33415(x_1679, y_1683)
        match _x_33416:
            case lt():
                _x_33418 = _alt_33407()
                return _x_33418
            case eq():
                _x_33420 = _alt_33410()
                return _x_33420
            case gt():
                _x_33422 = _alt_33414()
                return _x_33422
    _alt_33425 = _f_33424
    match x_33398:
        case RBTree_empty():
            _x_33427 = _alt_33403()
            return _x_33427
        case RBTree_node(a_33428, a_33429, a_33430, a_33431):
            _x_33432 = _alt_33425(a_33428, a_33429, a_33430, a_33431)
            return _x_33432

# Lean: Corpus.Production.RBTree.makeBlack
def make_black(__1688: Any, x_33435: Any) -> Any:
    def _f_33439(a_33436: Color, l_1689: Any, x_1690: Any, r_1691: Any):
        _x_33437 = black()
        _x_33438 = RBTree_node(_x_33437, l_1689, x_1690, r_1691)
        return _x_33438
    _alt_33440 = _f_33439
    _alt_33442 = (lambda t_1692: t_1692)
    match x_33435:
        case RBTree_node(a_33443, a_33444, a_33445, a_33446):
            _x_33447 = _alt_33440(a_33443, a_33444, a_33445, a_33446)
            return _x_33447
        case _:
            _x_33451 = (lambda h_33448: _alt_33442(x_33435))(None)
            return _x_33451

# Lean: Corpus.Production.RBTree.insert
def rbtree_insert(__1693: Any, inst_33454: Any, x_1694: Any, t_1695: Any) -> Any:
    _x_33455 = insert_aux(None, inst_33454, x_1694, t_1695)
    _x_33456 = make_black(None, _x_33455)
    return _x_33456

# Lean: Corpus.Production.RBTree.toList
def to_list(__1696: Any, x_33458: Any) -> list[Any]:
    def _f_33460():
        _x_33459 = []
        return _x_33459
    _alt_33461 = _f_33460
    def _f_33472(a_33462: Color, l_1698: Any, x_1699: Any, r_1700: Any):
        _x_33466 = list(l_1698)
        _x_33467 = []
        _x_33468 = [x_1699] + _x_33467
        _x_33469 = _x_33466 + _x_33468
        _x_33470 = list(r_1700)
        _x_33471 = _x_33469 + _x_33470
        return _x_33471
    _alt_33473 = _f_33472
    match x_33458:
        case RBTree_empty():
            _x_33475 = _alt_33461()
            return _x_33475
        case RBTree_node(a_33476, a_33477, a_33478, a_33479):
            _x_33480 = _alt_33473(a_33476, a_33477, a_33478, a_33479)
            return _x_33480

# Lean: Corpus.Production.RBTree.fromList
def from_list(__1701: Any, inst_33483: Any, xs_1702: list[Any]) -> Any:
    def _f_33485(t_1703: Any, x_1704: Any):
        _x_33484 = rbtree_insert(None, inst_33483, x_1704, t_1703)
        return _x_33484
    _x_33486 = RBTree_empty()
    _x_33487 = functools.reduce(_f_33485, xs_1702, _x_33486)
    return _x_33487

# Lean: Corpus.Production.RBTree.size
def rbtree_size(__1705: Any, x_33489: Any) -> int:
    def _f_33493():
        _x_33490 = 0
        return 0
    _alt_33494 = _f_33493
    def _f_33507(a_33495: Color, l_1707: Any, a_33496: Any, r_1708: Any):
        _x_33500 = 1
        _x_33503 = rbtree_size(None, l_1707)
        _x_33504 = 1 + _x_33503
        _x_33505 = rbtree_size(None, r_1708)
        _x_33506 = _x_33504 + _x_33505
        return _x_33506
    _alt_33508 = _f_33507
    match x_33489:
        case RBTree_empty():
            _x_33510 = _alt_33494()
            return _x_33510
        case RBTree_node(a_33511, a_33512, a_33513, a_33514):
            _x_33515 = _alt_33508(a_33511, a_33512, a_33513, a_33514)
            return _x_33515

# Lean: Corpus.Production.RBTree.height
def height(__1709: Any, x_33518: Any) -> int:
    def _f_33522():
        _x_33519 = 0
        return 0
    _alt_33523 = _f_33522
    def _f_33538(a_33524: Color, l_1711: Any, a_33525: Any, r_1712: Any):
        _x_33529 = 1
        _x_33533 = max
        _x_33534 = height(None, l_1711)
        _x_33535 = height(None, r_1712)
        _x_33536 = _x_33533(_x_33534, _x_33535)
        _x_33537 = 1 + _x_33536
        return _x_33537
    _alt_33539 = _f_33538
    match x_33518:
        case RBTree_empty():
            _x_33541 = _alt_33523()
            return _x_33541
        case RBTree_node(a_33542, a_33543, a_33544, a_33545):
            _x_33546 = _alt_33539(a_33542, a_33543, a_33544, a_33545)
            return _x_33546

# Lean: Corpus.Production.RBTree.blackHeight
def black_height(__1713: Any, x_33549: Any) -> int:
    def _f_33553():
        _x_33550 = 1
        return 1
    _alt_33554 = _f_33553
    def _f_33578(c_1715: Color, l_1716: Any, a_33555: Any, a_33556: Any):
        _x_33562 = black()
        _x_33563 = c_1715 == _x_33562
        _x_33564 = True
        _x_33565 = _x_33563 == True
        def _jp_33577(_y_33574: int):
            _x_33575 = black_height(None, l_1716)
            _x_33576 = _y_33574 + _x_33575
            return _x_33576
        if _x_33565:
            _x_33571 = 1
            return _jp_33577(1)
        else:
            _x_33567 = 0
            return _jp_33577(0)
    _alt_33579 = _f_33578
    match x_33549:
        case RBTree_empty():
            _x_33581 = _alt_33554()
            return _x_33581
        case RBTree_node(a_33582, a_33583, a_33584, a_33585):
            _x_33586 = _alt_33579(a_33582, a_33583, a_33584, a_33585)
            return _x_33586

# Lean: Corpus.Production.UnionFind.empty
def production_union_find_empty() -> UnionFind:
    _x_33589 = []
    _x_33590 = list(_x_33589)
    _x_33591 = UnionFind_mk(_x_33590)
    return _x_33591

# Lean: Corpus.Production.UnionFind.size
def production_union_find_size(uf_1717: UnionFind) -> int:
    _x_33592 = uf_1717.field_0
    _x_33593 = len(_x_33592)
    return _x_33593

# Lean: Corpus.Production.UnionFind.push
def production_union_find_push(uf_1718: UnionFind) -> UnionFind:
    _x_33595 = uf_1718.field_0
    _x_33596 = len(_x_33595)
    _x_33597 = 0
    _x_33600 = UFNode_mk(_x_33596, 0)
    _x_33601 = array_push(None, _x_33595, _x_33600)
    _x_33602 = UnionFind_mk(_x_33601)
    return _x_33602

# Lean: Corpus.Production.UnionFind.findWithPath
def find_with_path(nodes_1719: list[UFNode], x_1720: int) -> int:
    while True:
        _x_33604 = len(nodes_1719)
        _x_33605 = x_1720 < _x_33604
        if _x_33605:
            _x_33607 = (lambda xs, i: 0 <= i < len(xs))
            _x_33608 = _x_33607(nodes_1719, x_1720, None)
            _x_33609 = _x_33608.field_0
            _x_33613 = _x_33609 == x_1720
            _x_33614 = True
            _x_33615 = _x_33613 == True
            if _x_33615:
                return x_1720
            else:
                nodes_1719, x_1720 = nodes_1719, _x_33609
                continue
        else:
            return x_1720

# Lean: Corpus.Production.UnionFind.findRoot
def find_root(uf_1722: UnionFind, x_1723: int) -> int:
    _x_33622 = uf_1722.field_0
    _x_33623 = find_with_path(_x_33622, x_1723)
    return _x_33623

# Lean: Corpus.Production.UnionFind.connected
def connected(uf_1724: UnionFind, x_1725: int, y_1726: int) -> bool:
    _x_33628 = find_root(uf_1724, x_1725)
    _x_33629 = find_root(uf_1724, y_1726)
    _x_33630 = _x_33628 == _x_33629
    return _x_33630

# Lean: Corpus.Production.UnionFind.union
def union(uf_1727: UnionFind, x_1728: int, y_1729: int) -> UnionFind:
    _x_33632 = find_root(uf_1727, x_1728)
    _x_33633 = find_root(uf_1727, y_1729)
    _x_33637 = _x_33632 == _x_33633
    _x_33638 = True
    _x_33639 = _x_33637 == True
    if _x_33639:
        return uf_1727
    else:
        _x_33641 = uf_1727.field_0
        _x_33642 = len(_x_33641)
        _x_33643 = _x_33632 < _x_33642
        if _x_33643:
            _x_33644 = _x_33633 < _x_33642
            if _x_33644:
                _x_33646 = (lambda xs, i: 0 <= i < len(xs))
                _x_33647 = _x_33646(_x_33641, _x_33632, None)
                _x_33648 = _x_33647.field_1
                _x_33649 = _x_33646(_x_33641, _x_33633, None)
                _x_33650 = _x_33649.field_1
                _x_33651 = _x_33648 < _x_33650
                if _x_33651:
                    _x_33673 = UFNode_mk(_x_33633, _x_33648)
                    _x_33674 = set_(None, _x_33641, _x_33632, _x_33673)
                    _x_33675 = UnionFind_mk(_x_33674)
                    return _x_33675
                else:
                    _x_33653 = _x_33650 < _x_33648
                    if _x_33653:
                        _x_33668 = UFNode_mk(_x_33632, _x_33650)
                        _x_33669 = set_(None, _x_33641, _x_33633, _x_33668)
                        _x_33670 = UnionFind_mk(_x_33669)
                        return _x_33670
                    else:
                        _x_33655 = UFNode_mk(_x_33632, _x_33650)
                        _x_33656 = set_(None, _x_33641, _x_33633, _x_33655)
                        _x_33660 = 1
                        _x_33663 = _x_33648 + 1
                        _x_33664 = UFNode_mk(_x_33632, _x_33663)
                        _x_33665 = set_(None, _x_33656, _x_33632, _x_33664)
                        _x_33666 = UnionFind_mk(_x_33665)
                        return _x_33666
            else:
                return uf_1727
        else:
            return uf_1727

# Lean: Corpus.Production.UnionFind.numComponents
def num_components(uf_1730: UnionFind) -> int:
    def _f_33695(i_1731: int):
        _x_33682 = uf_1730.field_0
        _x_33683 = len(_x_33682)
        _x_33684 = i_1731 < _x_33683
        if _x_33684:
            _x_33690 = (lambda xs, i: 0 <= i < len(xs))
            _x_33691 = _x_33690(_x_33682, i_1731, None)
            _x_33692 = _x_33691.field_0
            _x_33693 = _x_33692 == i_1731
            return _x_33693
        else:
            _x_33685 = False
            return False
    _x_33696 = uf_1730.field_0
    _x_33697 = len(_x_33696)
    _x_33698 = list(range(_x_33697))
    _x_33699 = [x for x in _x_33698 if _f_33695(x)]
    _x_33700 = len(_x_33699)
    return _x_33700

# Lean: Corpus.Production.UnionFind.ofSize
def of_size(n_1733: int) -> UnionFind:
    _x_33702 = 0
    _x_33705 = []
    _x_33706 = list(_x_33705)
    _x_33707 = of_size_build(n_1733, 0, _x_33706)
    _x_33708 = UnionFind_mk(_x_33707)
    return _x_33708

# Lean: Corpus.Production.lomutoPartition
def lomuto_partition(arr_1734: list[int], lo_1735: int, hi_1736: int) -> tuple[list[int], int]:
    _x_33710 = hi_1736 <= lo_1735
    if _x_33710:
        _x_33718 = (arr_1734, lo_1735)
        return _x_33718
    else:
        _x_33713 = _x_33712.field_2
        _x_33715 = _x_33713(_x_33714, arr_1734, hi_1736)
        _x_33716 = lomuto_partition_go(hi_1736, _x_33715, arr_1734, lo_1735, lo_1735)
        return _x_33716

# Lean: Corpus.Production.quicksortAux
def quicksort_aux(arr_1738: list[int], lo_1739: int, hi_1740: int) -> list[int]:
    _x_33721 = hi_1740 <= lo_1739
    if _x_33721:
        return arr_1738
    else:
        def _f_33751(arr__1741: list[int], p_1742: int):
            _x_33723 = 0
            _x_33726 = 0 < p_1742
            def _jp_33750(_y_33737: list[int]):
                _x_33741 = 1
                _x_33744 = p_1742 + 1
                _x_33745 = _x_33744 < hi_1740
                if _x_33745:
                    _x_33748 = quicksort_aux(_y_33737, _x_33744, hi_1740)
                    return _x_33748
                else:
                    return _y_33737
            if _x_33726:
                _x_33732 = 1
                _x_33735 = p_1742 - 1
                _x_33736 = quicksort_aux(arr__1741, lo_1739, _x_33735)
                return _jp_33750(_x_33736)
            else:
                return _jp_33750(arr__1741)
        _alt_33752 = _f_33751
        _x_33753 = lomuto_partition(arr_1738, lo_1739, hi_1740)
        match _x_33753:
            case (fst_33754, snd_33755):
                _x_33756 = _alt_33752(fst_33754, snd_33755)
                return _x_33756

# Lean: Corpus.Production.quicksort
def quicksort(arr_1743: list[int]) -> list[int]:
    _x_33761 = len(arr_1743)
    _x_33762 = 1
    _x_33765 = _x_33761 <= 1
    if _x_33765:
        return arr_1743
    else:
        _x_33767 = 0
        _x_33773 = _x_33761 - 1
        _x_33774 = quicksort_aux(arr_1743, 0, _x_33773)
        return _x_33774

# Lean: Corpus.Production.naiveStringMatch
def naive_string_match(text: str, pattern: str) -> int | None:
    _x_33778 = list(text)
    _x_33779 = list(pattern)
    _x_33780 = len(_x_33778)
    _x_33781 = len(_x_33779)
    _x_33785 = 0
    _x_33788 = _x_33781 == 0
    _x_33789 = True
    _x_33790 = _x_33788 == True
    if _x_33790:
        _x_33799 = 0
        return _x_33799
    else:
        _x_33792 = _x_33780 < _x_33781
        if _x_33792:
            _x_33796 = None
            return _x_33796
        else:
            _x_33794 = search(_x_33778, _x_33779, _x_33780, _x_33781, 0)
            return _x_33794

# Lean: Corpus.Production.naiveStringMatchAll
def naive_string_match_all(text_1748: str, pattern_1749: str) -> list[int]:
    _x_33802 = list(text_1748)
    _x_33803 = list(pattern_1749)
    _x_33804 = len(_x_33802)
    _x_33805 = len(_x_33803)
    _x_33809 = 0
    _x_33812 = _x_33805 == 0
    _x_33813 = True
    _x_33814 = _x_33812 == True
    if _x_33814:
        _x_33827 = 1
        _x_33830 = _x_33804 + 1
        _x_33831 = list(range(_x_33830))
        return _x_33831
    else:
        _x_33816 = _x_33804 < _x_33805
        if _x_33816:
            _x_33821 = []
            return _x_33821
        else:
            _x_33818 = []
            _x_33819 = search(_x_33802, _x_33803, _x_33804, _x_33805, 0, _x_33818)
            return _x_33819

# Lean: Corpus.Production.computeZArray
def compute_zarray(s_1754: list[str]) -> list[int]:
    _x_33834 = len(s_1754)
    _x_33838 = 0
    _x_33841 = _x_33834 == 0
    _x_33842 = True
    _x_33843 = _x_33841 == True
    if _x_33843:
        _x_33852 = []
        _x_33853 = list(_x_33852)
        return _x_33853
    else:
        _x_33845 = array_replicate(None, _x_33834, 0)
        _x_33846 = set_(None, _x_33845, 0, _x_33834)
        _x_33847 = 1
        _x_33850 = compute(s_1754, _x_33834, _x_33846, 1, 0, 0)
        return _x_33850

# Lean: Corpus.Production.lcsLength
def lcs_length(xs_1758: list[int], ys_1759: list[int]) -> int:
    _x_33856 = len(xs_1758)
    _x_33857 = len(ys_1759)
    _x_33864 = 1
    _x_33867 = _x_33856 + 1
    _x_33868 = _x_33857 + 1
    _x_33869 = _x_33867 * _x_33868
    _x_33870 = 0
    _x_33873 = array_replicate(None, _x_33869, 0)
    _x_33874 = fill(xs_1758, ys_1759, _x_33856, _x_33857, 0, 0, _x_33873)
    _x_33876 = _x_33875.field_2
    _x_33878 = _x_33856 * _x_33868
    _x_33879 = _x_33878 + _x_33857
    _x_33880 = _x_33876(_x_33877, _x_33874, _x_33879)
    return _x_33880

# Lean: Corpus.Production.lcs
def lcs(xs_1764: list[int], ys_1765: list[int]) -> list[int]:
    _x_33882 = len(xs_1764)
    _x_33883 = len(ys_1765)
    _x_33890 = 1
    _x_33893 = _x_33882 + 1
    _x_33894 = _x_33883 + 1
    _x_33895 = _x_33893 * _x_33894
    _x_33896 = 0
    _x_33899 = array_replicate(None, _x_33895, 0)
    _x_33900 = fill(xs_1764, ys_1765, _x_33882, _x_33883, 0, 0, _x_33899)
    _x_33901 = []
    _x_33902 = backtrack(xs_1764, ys_1765, _x_33883, _x_33900, _x_33882, _x_33883, _x_33901)
    return _x_33902

# Lean: Corpus.Production.editDistance
def edit_distance(xs_1770: list[int], ys_1771: list[int]) -> int:
    _x_33904 = len(xs_1770)
    _x_33905 = len(ys_1771)
    _x_33912 = 1
    _x_33915 = _x_33904 + 1
    _x_33916 = _x_33905 + 1
    _x_33917 = _x_33915 * _x_33916
    _x_33918 = 0
    _x_33921 = array_replicate(None, _x_33917, 0)
    _x_33922 = fill(xs_1770, ys_1771, _x_33904, _x_33905, 0, 0, _x_33921)
    _x_33924 = _x_33923.field_2
    _x_33926 = _x_33904 * _x_33916
    _x_33927 = _x_33926 + _x_33905
    _x_33928 = _x_33924(_x_33925, _x_33922, _x_33927)
    return _x_33928

# Lean: Corpus.Production.intervalScheduling
def interval_scheduling(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    _x_33930 = list(intervals)
    def _f_33935(a_1775: tuple[int, int], b_1776: tuple[int, int]):
        _x_33931 = a_1775[1]
        _x_33932 = b_1776[1]
        _x_33933 = _x_33931 < _x_33932
        return _x_33933
    _x_33936 = 0
    _x_33942 = len(_x_33930)
    _x_33943 = 1
    _x_33946 = _x_33942 - 1
    _x_33947 = sorted(0, key=functools.cmp_to_key(lambda a, b: -1 if _x_33946(a, b) else 1))
    _x_33948 = list(_x_33947)
    _x_33949 = []
    _x_33950 = select(_x_33948, 0, _x_33949)
    return _x_33950

# Lean: Corpus.Production.knapsack01
def knapsack01(capacity_1778: int, weights_1779: list[int], values_1780: list[int]) -> int:
    _x_33952 = len(weights_1779)
    _x_33959 = 1
    _x_33962 = _x_33952 + 1
    _x_33963 = capacity_1778 + 1
    _x_33964 = _x_33962 * _x_33963
    _x_33965 = 0
    _x_33968 = array_replicate(None, _x_33964, 0)
    _x_33969 = fill(capacity_1778, weights_1779, values_1780, _x_33952, 0, 0, _x_33968)
    _x_33971 = _x_33970.field_2
    _x_33973 = _x_33952 * _x_33963
    _x_33974 = _x_33973 + capacity_1778
    _x_33975 = _x_33971(_x_33972, _x_33969, _x_33974)
    return _x_33975

# Lean: Corpus.Production.coinChange
def coin_change(coins_1784: list[int], amount_1785: int) -> int | None:
    _x_33980 = 1
    _x_33983 = amount_1785 + 1
    _x_33984 = amount_1785 + 1
    _x_33985 = array_replicate(None, _x_33984, _x_33983)
    _x_33986 = 0
    _x_33989 = set_(None, _x_33985, 0, 0)
    _x_33990 = fill(coins_1784, amount_1785, _x_33983, 1, _x_33989)
    _x_33992 = _x_33991.field_2
    _x_33994 = _x_33992(_x_33993, _x_33990, amount_1785)
    _x_33995 = _x_33983 <= _x_33994
    if _x_33995:
        _x_33999 = None
        return _x_33999
    else:
        _x_33997 = _x_33994
        return _x_33997

# Lean: Corpus.Production.matrixChainOrder
def matrix_chain_order(dims_1790: list[int]) -> int:
    _x_34005 = len(dims_1790)
    _x_34006 = 1
    _x_34009 = _x_34005 - 1
    _x_34010 = _x_34009 <= 1
    if _x_34010:
        _x_34030 = 0
        return 0
    else:
        _x_34012 = 1000000000
        _x_34018 = _x_34009 * _x_34009
        _x_34019 = array_replicate(None, _x_34018, 1000000000)
        _x_34020 = 0
        _x_34023 = fill(dims_1790, _x_34009, 1000000000, 1, 0, _x_34019)
        _x_34025 = _x_34024.field_2
        _x_34027 = _x_34009 - 1
        _x_34028 = _x_34025(_x_34026, _x_34023, _x_34027)
        return _x_34028

# Lean: Corpus.Production.lisLength
def lis_length(xs_1795: list[int]) -> int:
    _x_34035 = len(xs_1795)
    _x_34039 = 0
    _x_34042 = _x_34035 == 0
    _x_34043 = True
    _x_34044 = _x_34042 == True
    if _x_34044:
        return 0
    else:
        _x_34046 = 1
        _x_34049 = array_replicate(None, _x_34035, 1)
        _x_34050 = fill(xs_1795, _x_34035, 0, _x_34049)
        _x_34052 = max
        _x_34053 = len(_x_34050)
        _x_34054 = array_foldl(None, None, _x_34052, 0, _x_34050, 0, _x_34053)
        return _x_34054

# Lean: Corpus.Production.lis
def lis(xs_1799: list[int]) -> list[int]:
    _x_34059 = len(xs_1799)
    _x_34063 = 0
    _x_34066 = _x_34059 == 0
    _x_34067 = True
    _x_34068 = _x_34066 == True
    if _x_34068:
        _x_34113 = []
        return _x_34113
    else:
        _x_34070 = 1
        _x_34073 = array_replicate(None, _x_34059, 1)
        _x_34074 = array_replicate(None, _x_34059, _x_34059)
        def _f_34105(dp__1803: list[int], parent__1804: list[int]):
            def _f_34078(fst_34075: int, max_idx: int):
                _x_34076 = []
                _x_34077 = backtrack(xs_1799, _x_34059, parent__1804, max_idx, _x_34076)
                return _x_34077
            _alt_34079 = _f_34078
            def _f_34097(x_34080: tuple[int, int], i_1805: int):
                def _f_34091(max_val_1806: int, max_i: int):
                    _x_34082 = _x_34081.field_2
                    _x_34084 = _x_34082(_x_34083, dp__1803, i_1805)
                    _x_34085 = max_val_1806 < _x_34084
                    if _x_34085:
                        _x_34089 = (_x_34084, i_1805)
                        return _x_34089
                    else:
                        _x_34087 = (max_val_1806, max_i)
                        return _x_34087
                _alt_34092 = _f_34091
                match x_34080:
                    case (fst_34093, snd_34094):
                        _x_34095 = _alt_34092(fst_34093, snd_34094)
                        return _x_34095
            _x_34098 = (0, 0)
            _x_34099 = list(range(_x_34059))
            _x_34100 = functools.reduce(_f_34097, _x_34099, _x_34098)
            match _x_34100:
                case (fst_34101, snd_34102):
                    _x_34103 = _alt_34079(fst_34101, snd_34102)
                    return _x_34103
        _alt_34106 = _f_34105
        _x_34107 = fill(xs_1799, _x_34059, 0, _x_34073, _x_34074)
        match _x_34107:
            case (fst_34108, snd_34109):
                _x_34110 = _alt_34106(fst_34108, snd_34109)
                return _x_34110

# Lean: Corpus.Production.maxSubarraySum
def max_subarray_sum(xs_1807: list[int]) -> int:
    def _f_34119():
        _x_34116 = 0
        return 0
    _alt_34120 = _f_34119
    def _f_34122(x_1809: int, rest_1810: list[int]):
        _x_34121 = kadane(rest_1810, x_1809, x_1809)
        return _x_34121
    _alt_34123 = _f_34122
    if len(xs_1807) == 0:
        _x_34125 = _alt_34120()
        return _x_34125
    else:
        head_34126 = xs_1807[0]
        tail_34127 = xs_1807[1:]
        _x_34128 = _alt_34123(head_34126, tail_34127)
        return _x_34128

# Lean: Corpus.Production.countInversions
def count_inversions(xs_1811: list[int]) -> int:
    _x_34131 = merge_count(xs_1811)
    _x_34132 = _x_34131[1]
    return _x_34132


