# Generated from Corpus

from __future__ import annotations
from dataclasses import dataclass
import functools
from typing import Any, Callable

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
class Stack_mk:
    field_0: Any

Stack = Stack_mk

@dataclass
class BlackjackHand_mk:
    field_0: Any

BlackjackHand = BlackjackHand_mk

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

# Lean: Corpus.Sorting.unique.go
def unique_go(xs: list[int], seen: list[int]) -> list[int]:
    def _f_9949():
        _x_9948 = list(reversed(seen))
        return _x_9948
    _alt_9950 = _f_9949
    def _f_9961(x: int, rest: list[int]):
        _x_9952 = x in seen
        _x_9953 = True
        if _x_9952:
            _x_9959 = unique_go(rest, seen)
            return _x_9959
        else:
            _x_9956 = [x] + seen
            _x_9957 = unique_go(rest, _x_9956)
            return _x_9957
    _alt_9962 = _f_9961
    if len(xs) == 0:
        _x_9964 = _alt_9950()
        return _x_9964
    else:
        head_9965 = xs[0]
        tail_9966 = xs[1:]
        _x_9967 = _alt_9962(head_9965, tail_9966)
        return _x_9967

# Lean: Corpus.Sorting.mode.count
def count(x_0: int, xs_1: list[int]) -> int:
    def _f_9985(acc: int, y: int):
        _x_9972 = y == x_0
        _x_9973 = True
        if _x_9972:
            _x_9980 = 1
            _x_9983 = acc + 1
            return _x_9983
        else:
            return acc
    _x_9986 = 0
    _x_9989 = functools.reduce(_f_9985, xs_1, 0)
    return _x_9989

# Lean: Corpus.Sorting.mode.go
def mode_go(xs_2: list[int], best: int | None, best_count: int) -> int | None:
    def _f_9991():
        return best
    _alt_9992 = _f_9991
    def _f_10001(x_4: int, rest_5: list[int]):
        _x_9993 = count(x_4, xs_2)
        _x_9994 = best_count < _x_9993
        if _x_9994:
            _x_9998 = x_4
            _x_9999 = mode_go(rest_5, _x_9998, _x_9993)
            return _x_9999
        else:
            _x_9996 = mode_go(rest_5, best, best_count)
            return _x_9996
    _alt_10002 = _f_10001
    if len(xs_2) == 0:
        _x_10004 = _alt_9992()
        return _x_10004
    else:
        head_10005 = xs_2[0]
        tail_10006 = xs_2[1:]
        _x_10007 = _alt_10002(head_10005, tail_10006)
        return _x_10007

# Lean: Corpus.Sorting.gnomeSort.go
def gnome_sort_go(n: int, pos: int, arr: list[int]) -> list[int]:
    _x_10010 = n <= pos
    if _x_10010:
        return arr
    else:
        def _f_10013():
            _x_10012 = True
            return True
        _alt_10014 = _f_10013
        def _f_10033():
            def _f_10018(xs_8: list[int], i: int):
                _x_10016 = len(xs_8)
                _x_10017 = i < _x_10016
                return _x_10017
            _x_10020 = _x_10019.get_elem__2
            _x_10025 = 1
            _x_10028 = pos - 1
            _x_10029 = _x_10020(_x_10021, arr, _x_10028)
            _x_10030 = _x_10020(_x_10021, arr, pos)
            _x_10031 = _x_10029 <= _x_10030
            return _x_10031
        _alt_10034 = _f_10033
        _x_10037 = 0
        _x_10040 = pos == 0
        def _jp_10068(_y_10045: bool):
            _x_10046 = True
            if _y_10045:
                _x_10062 = 1
                _x_10065 = pos + 1
                _x_10066 = gnome_sort_go(n, _x_10065, arr)
                return _x_10066
            else:
                _x_10052 = 1
                _x_10055 = pos - 1
                _x_10056 = swap_(None, arr, pos, _x_10055)
                _x_10057 = gnome_sort_go(n, _x_10055, _x_10056)
                return _x_10057
        def _jp_10071():
            _x_10070 = _alt_10034()
            return _jp_10068(_x_10070)
        def _jp_10074():
            _x_10073 = _alt_10014()
            return _jp_10068(_x_10073)
        if _x_10040:
            return _jp_10074()
        else:
            return _jp_10071()

# Lean: Corpus.Sorting.radixSort.go
def radix_sort_go(max_val: int, exp: int, xs_9: list[int]) -> list[int]:
    _x_10078 = max_val < exp
    if _x_10078:
        return xs_9
    else:
        def _f_10095(arr_10: list[list[int]], x_11: int):
            _x_10086 = x_11 // exp
            _x_10087 = 10
            _x_10090 = _x_10086 % 10
            def _f_10093(x_10091: list[int]):
                _x_10092 = [x_11] + x_10091
                return _x_10092
            _x_10094 = modify(None, arr_10, _x_10090, _f_10093)
            return _x_10094
        _x_10096 = 10
        _x_10099 = []
        _x_10100 = mk_array(None, 10, _x_10099)
        _x_10101 = functools.reduce(_f_10095, xs_9, _x_10100)
        def _f_10107(acc_12: list[int], bucket: list[int]):
            _x_10105 = list(reversed(bucket))
            _x_10106 = acc_12 + _x_10105
            return _x_10106
        _x_10108 = 0
        _x_10111 = len(_x_10101)
        _x_10112 = array_foldl(None, None, _f_10107, _x_10099, _x_10101, 0, _x_10111)
        _x_10116 = exp * 10
        _x_10117 = radix_sort_go(max_val, _x_10116, _x_10112)
        return _x_10117

# Lean: Corpus.Sorting.countingSort.expand
def expand(max_val_13: int, counts: list[int], i_14: int, acc_15: list[int]) -> list[int]:
    _x_10121 = max_val_13 < i_14
    if _x_10121:
        return acc_15
    else:
        _x_10126 = 1
        _x_10129 = i_14 + 1
        _x_10133 = 0
        _x_10136 = get_d(None, counts, i_14, 0)
        _x_10137 = list_replicate(None, _x_10136, i_14)
        _x_10138 = acc_15 + _x_10137
        _x_10139 = expand(max_val_13, counts, _x_10129, _x_10138)
        return _x_10139

# Lean: Corpus.Sorting.selectionSort.go.findMin
def find_min(n_16: int, arr_17: list[int], j: int, min_idx: int) -> int:
    _x_10143 = n_16 <= j
    if _x_10143:
        return min_idx
    else:
        _x_10148 = 1
        _x_10151 = j + 1
        def _f_10155(xs_18: list[int], i_19: int):
            _x_10153 = len(xs_18)
            _x_10154 = i_19 < _x_10153
            return _x_10154
        _x_10157 = _x_10156.get_elem__2
        _x_10159 = _x_10157(_x_10158, arr_17, j)
        _x_10160 = _x_10157(_x_10158, arr_17, min_idx)
        _x_10161 = _x_10159 < _x_10160
        def _jp_10166(_y_10164: int):
            _x_10165 = find_min(n_16, arr_17, _x_10151, _y_10164)
            return _x_10165
        if _x_10161:
            return _jp_10166(j)
        else:
            return _jp_10166(min_idx)

# Lean: Corpus.Sorting.selectionSort.go
def selection_sort_go(n_20: int, i_21: int, arr_22: list[int]) -> list[int]:
    _x_10170 = n_20 <= i_21
    if _x_10170:
        return arr_22
    else:
        _x_10172 = find_min(n_20, arr_22, i_21, i_21)
        _x_10176 = 1
        _x_10179 = i_21 + 1
        _x_10180 = swap_(None, arr_22, i_21, _x_10172)
        _x_10181 = selection_sort_go(n_20, _x_10179, _x_10180)
        return _x_10181

# Lean: Corpus.Sorting.bubbleSort.outer.inner
def outer_inner(n_24: int, i_25: int, j_26: int, arr_27: list[int]) -> list[int]:
    _x_10188 = n_24 - i_25
    _x_10189 = 1
    _x_10192 = _x_10188 - 1
    _x_10193 = _x_10192 <= j_26
    if _x_10193:
        return arr_27
    else:
        def _f_10198(xs_28: list[int], i_29: int):
            _x_10196 = len(xs_28)
            _x_10197 = i_29 < _x_10196
            return _x_10197
        _x_10200 = _x_10199.get_elem__2
        _x_10205 = j_26 + 1
        _x_10206 = _x_10200(_x_10201, arr_27, _x_10205)
        _x_10207 = _x_10200(_x_10201, arr_27, j_26)
        _x_10208 = _x_10206 < _x_10207
        def _jp_10214(_y_10212: list[int]):
            _x_10213 = outer_inner(n_24, i_25, _x_10205, _y_10212)
            return _x_10213
        if _x_10208:
            _x_10211 = swap_(None, arr_27, j_26, _x_10205)
            return _jp_10214(_x_10211)
        else:
            return _jp_10214(arr_27)

# Lean: Corpus.Sorting.bubbleSort.outer
def outer(n_31: int, i_32: int, arr_33: list[int]) -> list[int]:
    _x_10218 = n_31 <= i_32
    if _x_10218:
        return arr_33
    else:
        _x_10223 = 1
        _x_10226 = i_32 + 1
        _x_10227 = 0
        _x_10230 = outer_inner(n_31, i_32, 0, arr_33)
        _x_10231 = outer(n_31, _x_10226, _x_10230)
        return _x_10231

# Lean: Corpus.Sequences.vanEck.go
def van_eck_go(n_34: int, i_35: int, prev: int, last_seen: list[tuple[int, int]], acc_36: list[int]) -> list[int]:
    _x_10235 = n_34 < i_35
    if _x_10235:
        _x_10296 = list(reversed(acc_36))
        return _x_10296
    else:
        def _f_10240():
            _x_10237 = 0
            return 0
        _alt_10241 = _f_10240
        def _f_10251(fst_10242: int, idx: int):
            _x_10246 = 1
            _x_10249 = i_35 - 1
            _x_10250 = _x_10249 - idx
            return _x_10250
        _alt_10252 = _f_10251
        def _f_10257(p: tuple[int, int]):
            _x_10255 = p[0]
            _x_10256 = _x_10255 == prev
            return _x_10256
        _x_10258 = next((x for x in last_seen if _f_10257(x)), None)
        def _jp_10287(_y_10266: int):
            _x_10270 = 1
            _x_10273 = i_35 - 1
            _x_10274 = (prev, _x_10273)
            def _f_10278(p_38: tuple[int, int]):
                _x_10276 = p_38[0]
                _x_10277 = (lambda a, b: a != b)(prev)
                return _x_10277
            _x_10279 = [x for x in last_seen if _f_10278(x)]
            _x_10280 = [_x_10274] + _x_10279
            _x_10284 = i_35 + 1
            _x_10285 = [_y_10266] + acc_36
            _x_10286 = van_eck_go(n_34, _x_10284, _y_10266, _x_10280, _x_10285)
            return _x_10286
        def _jp_10294(_y_10291: int, _y_10292: int):
            _x_10293 = _alt_10252(_y_10291, _y_10292)
            return _jp_10287(_x_10293)
        def _jp_10290():
            _x_10289 = _alt_10241()
            return _jp_10287(_x_10289)
        if _x_10258 is None:
            return _jp_10290()
        else:
            val_10261 = _x_10258
            match val_10261:
                case (fst_10262, snd_10263):
                    return _jp_10294(fst_10262, snd_10263)

# Lean: Corpus.Sequences.firstNPrimes.isPrime.check
def first_nprimes_is_prime_check(n_39: int, d: int) -> bool:
    _x_10302 = d * d
    _x_10303 = n_39 < _x_10302
    if _x_10303:
        _x_10330 = True
        return True
    else:
        _x_10310 = n_39 % d
        _x_10311 = 0
        _x_10314 = _x_10310 == 0
        _x_10315 = True
        if _x_10314:
            _x_10327 = False
            return False
        else:
            _x_10321 = 1
            _x_10324 = d + 1
            _x_10325 = first_nprimes_is_prime_check(n_39, _x_10324)
            return _x_10325

# Lean: Corpus.Sequences.firstNPrimes.isPrime
def first_nprimes_is_prime(n_40: int) -> bool:
    _x_10333 = 2
    _x_10336 = n_40 < 2
    if _x_10336:
        _x_10340 = False
        return False
    else:
        _x_10338 = first_nprimes_is_prime_check(n_40, 2)
        return _x_10338

# Lean: Corpus.Sequences.firstNPrimes.go
def first_nprimes_go(n_41: int, candidate: int, found: list[int]) -> list[int]:
    _x_10343 = len(found)
    _x_10344 = n_41 <= _x_10343
    if _x_10344:
        _x_10370 = list(reversed(found))
        return _x_10370
    else:
        _x_10346 = first_nprimes_is_prime(candidate)
        _x_10347 = True
        if _x_10346:
            _x_10362 = 1
            _x_10365 = candidate + 1
            _x_10366 = [candidate] + found
            _x_10367 = first_nprimes_go(n_41, _x_10365, _x_10366)
            return _x_10367
        else:
            _x_10353 = 1
            _x_10356 = candidate + 1
            _x_10357 = first_nprimes_go(n_41, _x_10356, found)
            return _x_10357

# Lean: Corpus.Sequences.recaman.go
def recaman_go(n_42: int, i_43: int, prev_44: int, seen_45: list[int], acc_46: list[int]) -> list[int]:
    _x_10373 = n_42 < i_43
    if _x_10373:
        _x_10425 = list(reversed(acc_46))
        return _x_10425
    else:
        _x_10378 = prev_44 - i_43
        def _f_10380():
            _x_10379 = False
            return False
        _alt_10381 = _f_10380
        def _f_10385():
            _x_10383 = _x_10378 in seen_45
            _x_10384 = not _x_10383
            return _x_10384
        _alt_10386 = _f_10385
        _x_10387 = 0
        _x_10390 = 0 < _x_10378
        def _jp_10417(_y_10396: bool):
            _x_10397 = True
            def _jp_10416(_y_10405: int):
                _x_10409 = 1
                _x_10412 = i_43 + 1
                _x_10413 = [_y_10405] + seen_45
                _x_10414 = [_y_10405] + acc_46
                _x_10415 = recaman_go(n_42, _x_10412, _y_10405, _x_10413, _x_10414)
                return _x_10415
            if _y_10396:
                return _jp_10416(_x_10378)
            else:
                _x_10403 = prev_44 + i_43
                return _jp_10416(_x_10403)
        def _jp_10423():
            _x_10422 = _alt_10386()
            return _jp_10417(_x_10422)
        def _jp_10420():
            _x_10419 = _alt_10381()
            return _jp_10417(_x_10419)
        if _x_10390:
            return _jp_10423()
        else:
            return _jp_10420()

# Lean: Corpus.Sequences.lookAndSayNext.go
def look_and_say_next_go(xs_51: list[int], curr: int, count: int, acc_52: list[int]) -> list[int]:
    def _f_10436():
        _x_10431 = []
        _x_10432 = [curr] + _x_10431
        _x_10433 = [count] + _x_10432
        _x_10434 = acc_52 + _x_10433
        _x_10435 = list(reversed(_x_10434))
        return _x_10435
    _alt_10437 = _f_10436
    def _f_10460(x_54: int, rest_55: list[int]):
        _x_10440 = x_54 == curr
        _x_10441 = True
        if _x_10440:
            _x_10454 = 1
            _x_10457 = count + 1
            _x_10458 = look_and_say_next_go(rest_55, curr, _x_10457, acc_52)
            return _x_10458
        else:
            _x_10444 = 1
            _x_10447 = [count] + acc_52
            _x_10448 = [curr] + _x_10447
            _x_10449 = look_and_say_next_go(rest_55, x_54, 1, _x_10448)
            return _x_10449
    _alt_10461 = _f_10460
    if len(xs_51) == 0:
        _x_10463 = _alt_10437()
        return _x_10463
    else:
        head_10464 = xs_51[0]
        tail_10465 = xs_51[1:]
        _x_10466 = _alt_10461(head_10464, tail_10465)
        return _x_10466

# Lean: Corpus.Sequences.repunit.go
def repunit_go(n_56: int, acc_57: int) -> int:
    _x_10471 = 0
    _x_10474 = n_56 == 0
    _x_10475 = True
    if _x_10474:
        return acc_57
    else:
        _x_10481 = 1
        _x_10484 = n_56 - 1
        _x_10491 = 10
        _x_10494 = acc_57 * 10
        _x_10495 = _x_10494 + 1
        _x_10496 = repunit_go(_x_10484, _x_10495)
        return _x_10496

# Lean: Corpus.Sequences.narayana.binomial.go
def binomial_go(n_58: int, k: int, i_59: int, acc_60: int) -> int:
    _x_10502 = i_59 == k
    _x_10503 = True
    if _x_10502:
        return acc_60
    else:
        _x_10509 = 1
        _x_10512 = i_59 + 1
        _x_10522 = n_58 - i_59
        _x_10523 = acc_60 * _x_10522
        _x_10524 = _x_10523 // _x_10512
        _x_10525 = binomial_go(n_58, k, _x_10512, _x_10524)
        return _x_10525

# Lean: Corpus.Sequences.narayana.binomial
def binomial(n_61: int, k_62: int) -> int:
    _x_10529 = n_61 < k_62
    if _x_10529:
        _x_10548 = 0
        return 0
    else:
        _x_10534 = n_61 - k_62
        _x_10535 = _x_10534 < k_62
        def _jp_10546(_y_10538: int):
            _x_10539 = 0
            _x_10542 = 1
            _x_10545 = binomial_go(n_61, _y_10538, 0, 1)
            return _x_10545
        if _x_10535:
            return _jp_10546(_x_10534)
        else:
            return _jp_10546(k_62)

# Lean: Corpus.Sequences.motzkin.go
def motzkin_go(n_64: int, k_65: int, acc_66: int) -> int:
    _x_10558 = 1
    _x_10561 = n_64 + 1
    _x_10562 = k_65 == _x_10561
    _x_10563 = True
    if _x_10562:
        return acc_66
    else:
        _x_10566 = k_65 + 1
        _x_10570 = motzkin(k_65)
        _x_10574 = n_64 - 1
        _x_10575 = _x_10574 - k_65
        _x_10576 = motzkin(_x_10575)
        _x_10577 = _x_10570 * _x_10576
        _x_10578 = acc_66 + _x_10577
        _x_10579 = motzkin_go(n_64, _x_10566, _x_10578)
        return _x_10579

# Lean: Corpus.Sequences.jacobsthal.go
def jacobsthal_go(n_67: int, a: int, b: int) -> int:
    _x_10585 = 0
    _x_10588 = n_67 == 0
    _x_10589 = True
    if _x_10588:
        return a
    else:
        _x_10595 = 1
        _x_10598 = n_67 - 1
        _x_10605 = 2
        _x_10608 = 2 * a
        _x_10609 = b + _x_10608
        _x_10610 = jacobsthal_go(_x_10598, b, _x_10609)
        return _x_10610

# Lean: Corpus.Sequences.perrin.go
def perrin_go(n_68: int, a_69: int, b_70: int, c_71: int) -> int:
    _x_10616 = 0
    _x_10619 = n_68 == 0
    _x_10620 = True
    if _x_10619:
        return a_69
    else:
        _x_10626 = 1
        _x_10629 = n_68 - 1
        _x_10633 = a_69 + b_70
        _x_10634 = perrin_go(_x_10629, b_70, c_71, _x_10633)
        return _x_10634

# Lean: Corpus.Sequences.padovan.go
def padovan_go(n_72: int, a_73: int, b_74: int, c_75: int) -> int:
    _x_10640 = 0
    _x_10643 = n_72 == 0
    _x_10644 = True
    if _x_10643:
        return a_73
    else:
        _x_10650 = 1
        _x_10653 = n_72 - 1
        _x_10657 = a_73 + b_74
        _x_10658 = padovan_go(_x_10653, b_74, c_75, _x_10657)
        return _x_10658

# Lean: Corpus.Sequences.pell.go
def pell_go(n_76: int, a_77: int, b_78: int) -> int:
    _x_10664 = 0
    _x_10667 = n_76 == 0
    _x_10668 = True
    if _x_10667:
        return a_77
    else:
        _x_10674 = 1
        _x_10677 = n_76 - 1
        _x_10684 = 2
        _x_10687 = 2 * b_78
        _x_10688 = _x_10687 + a_77
        _x_10689 = pell_go(_x_10677, b_78, _x_10688)
        return _x_10689

# Lean: Corpus.Sequences.tribonacci.go
def tribonacci_go(n_79: int, a_80: int, b_81: int, c_82: int) -> int:
    _x_10695 = 0
    _x_10698 = n_79 == 0
    _x_10699 = True
    if _x_10698:
        return a_80
    else:
        _x_10705 = 1
        _x_10708 = n_79 - 1
        _x_10712 = a_80 + b_81
        _x_10713 = _x_10712 + c_82
        _x_10714 = tribonacci_go(_x_10708, b_81, c_82, _x_10713)
        return _x_10714

# Lean: Corpus.Sequences.lucas.go
def lucas_go(n_83: int, a_84: int, b_85: int) -> int:
    _x_10720 = 0
    _x_10723 = n_83 == 0
    _x_10724 = True
    if _x_10723:
        return a_84
    else:
        _x_10730 = 1
        _x_10733 = n_83 - 1
        _x_10737 = a_84 + b_85
        _x_10738 = lucas_go(_x_10733, b_85, _x_10737)
        return _x_10738

# Lean: Corpus.Sequences.fibonacci.go
def sequences_fibonacci_go(n_86: int, a_87: int, b_88: int) -> int:
    _x_10744 = 0
    _x_10747 = n_86 == 0
    _x_10748 = True
    if _x_10747:
        return a_87
    else:
        _x_10754 = 1
        _x_10757 = n_86 - 1
        _x_10761 = a_87 + b_88
        _x_10762 = sequences_fibonacci_go(_x_10757, b_88, _x_10761)
        return _x_10762

# Lean: Corpus.Combinatorics.integerPartitions.go
def integer_partitions_go(n_89: int, max: int) -> list[list[int]]:
    _x_10768 = 0
    _x_10771 = n_89 == 0
    _x_10772 = True
    if _x_10771:
        _x_10800 = []
        _x_10801 = []
        _x_10802 = [_x_10800] + _x_10801
        return _x_10802
    else:
        _x_10775 = max == 0
        if _x_10775:
            _x_10797 = []
            return _x_10797
        else:
            def _f_10780(x_10778: list[int]):
                _x_10779 = [max] + x_10778
                return _x_10779
            _x_10784 = n_89 - max
            _x_10785 = integer_partitions_go(_x_10784, max)
            _x_10786 = [_f_10780(x) for x in _x_10785]
            _x_10787 = 1
            _x_10790 = max - 1
            _x_10791 = integer_partitions_go(n_89, _x_10790)
            _x_10795 = _x_10786 + _x_10791
            return _x_10795

# Lean: Corpus.Combinatorics.compositions.go
def compositions_go(n_90: int, k_91: int, acc_92: list[list[int]]) -> list[list[int]]:
    _x_10805 = n_90 < k_91
    if _x_10805:
        return acc_92
    else:
        _x_10810 = 1
        _x_10813 = k_91 + 1
        def _f_10819(x_10817: list[int]):
            _x_10818 = [k_91] + x_10817
            return _x_10818
        _x_10823 = n_90 - k_91
        _x_10824 = compositions(_x_10823)
        _x_10825 = [_f_10819(x) for x in _x_10824]
        _x_10826 = acc_92 + _x_10825
        _x_10827 = compositions_go(n_90, _x_10813, _x_10826)
        return _x_10827

# Lean: Corpus.Combinatorics.prevPermutation.findI
def find_i(arr_93: list[int], i_94: int) -> int | None:
    _x_10833 = 0
    _x_10836 = i_94 == 0
    _x_10837 = True
    if _x_10836:
        _x_10863 = None
        return _x_10863
    else:
        def _f_10843(xs_95: list[int], i_96: int):
            _x_10841 = len(xs_95)
            _x_10842 = i_96 < _x_10841
            return _x_10842
        _x_10845 = _x_10844.get_elem__2
        _x_10847 = _x_10845(_x_10846, arr_93, i_94)
        _x_10851 = 1
        _x_10854 = i_94 - 1
        _x_10855 = _x_10845(_x_10846, arr_93, _x_10854)
        _x_10856 = _x_10847 < _x_10855
        if _x_10856:
            _x_10860 = _x_10854
            return _x_10860
        else:
            _x_10858 = find_i(arr_93, _x_10854)
            return _x_10858

# Lean: Corpus.Combinatorics.prevPermutation.reverseFrom.go
def reverse_from_go(arr_97: list[int], l: int, r: int) -> list[int]:
    _x_10866 = r <= l
    if _x_10866:
        return arr_97
    else:
        _x_10868 = swap_(None, arr_97, l, r)
        _x_10872 = 1
        _x_10875 = l + 1
        _x_10879 = r - 1
        _x_10880 = reverse_from_go(_x_10868, _x_10875, _x_10879)
        return _x_10880

# Lean: Corpus.Combinatorics.prevPermutation.reverseFrom
def reverse_from(arr_98: list[int], start: int) -> list[int]:
    _x_10887 = len(arr_98)
    _x_10888 = 1
    _x_10891 = _x_10887 - 1
    _x_10892 = reverse_from_go(arr_98, start, _x_10891)
    return _x_10892

# Lean: Corpus.Combinatorics.prevPermutation.findJ
def find_j(arr_99: list[int], i_100: int, j_101: int) -> int:
    _x_10899 = 1
    _x_10902 = i_100 + 1
    _x_10903 = j_101 == _x_10902
    _x_10904 = True
    if _x_10903:
        return j_101
    else:
        def _f_10910(xs_102: list[int], i_103: int):
            _x_10908 = len(xs_102)
            _x_10909 = i_103 < _x_10908
            return _x_10909
        _x_10912 = _x_10911.get_elem__2
        _x_10917 = j_101 - 1
        _x_10918 = _x_10912(_x_10913, arr_99, _x_10917)
        _x_10919 = _x_10912(_x_10913, arr_99, i_100)
        _x_10920 = _x_10918 < _x_10919
        if _x_10920:
            return _x_10917
        else:
            _x_10922 = find_j(arr_99, i_100, _x_10917)
            return _x_10922

# Lean: Corpus.Combinatorics.nextPermutation.findI
def find_i(arr_104: list[int], i_105: int) -> int | None:
    _x_10930 = 0
    _x_10933 = i_105 == 0
    _x_10934 = True
    if _x_10933:
        _x_10960 = None
        return _x_10960
    else:
        def _f_10940(xs_106: list[int], i_107: int):
            _x_10938 = len(xs_106)
            _x_10939 = i_107 < _x_10938
            return _x_10939
        _x_10942 = _x_10941.get_elem__2
        _x_10947 = 1
        _x_10950 = i_105 - 1
        _x_10951 = _x_10942(_x_10943, arr_104, _x_10950)
        _x_10952 = _x_10942(_x_10943, arr_104, i_105)
        _x_10953 = _x_10951 < _x_10952
        if _x_10953:
            _x_10957 = _x_10950
            return _x_10957
        else:
            _x_10955 = find_i(arr_104, _x_10950)
            return _x_10955

# Lean: Corpus.Combinatorics.nextPermutation.reverseFrom.go
def reverse_from_go(arr_108: list[int], l_109: int, r_110: int) -> list[int]:
    _x_10963 = r_110 <= l_109
    if _x_10963:
        return arr_108
    else:
        _x_10965 = swap_(None, arr_108, l_109, r_110)
        _x_10969 = 1
        _x_10972 = l_109 + 1
        _x_10976 = r_110 - 1
        _x_10977 = reverse_from_go(_x_10965, _x_10972, _x_10976)
        return _x_10977

# Lean: Corpus.Combinatorics.nextPermutation.reverseFrom
def reverse_from(arr_111: list[int], start_112: int) -> list[int]:
    _x_10984 = len(arr_111)
    _x_10985 = 1
    _x_10988 = _x_10984 - 1
    _x_10989 = reverse_from_go(arr_111, start_112, _x_10988)
    return _x_10989

# Lean: Corpus.Combinatorics.nextPermutation.findJ
def find_j(arr_113: list[int], i_114: int, j_115: int) -> int:
    _x_10996 = 1
    _x_10999 = i_114 + 1
    _x_11000 = j_115 == _x_10999
    _x_11001 = True
    if _x_11000:
        return j_115
    else:
        def _f_11007(xs_116: list[int], i_117: int):
            _x_11005 = len(xs_116)
            _x_11006 = i_117 < _x_11005
            return _x_11006
        _x_11009 = _x_11008.get_elem__2
        _x_11011 = _x_11009(_x_11010, arr_113, i_114)
        _x_11015 = j_115 - 1
        _x_11016 = _x_11009(_x_11010, arr_113, _x_11015)
        _x_11017 = _x_11011 < _x_11016
        if _x_11017:
            return _x_11015
        else:
            _x_11019 = find_j(arr_113, i_114, _x_11015)
            return _x_11019

# Lean: Corpus.Combinatorics.permutationRank.go
def permutation_rank_go(n_118: int, code: list[int], pos_119: int, acc_120: int) -> int:
    def _f_11025():
        return acc_120
    _alt_11026 = _f_11025
    def _f_11046(c_122: int, rest_123: list[int]):
        _x_11030 = 1
        _x_11033 = pos_119 + 1
        _x_11040 = n_118 - pos_119
        _x_11041 = _x_11040 - 1
        _x_11042 = factorial(_x_11041)
        _x_11043 = c_122 * _x_11042
        _x_11044 = acc_120 + _x_11043
        _x_11045 = permutation_rank_go(n_118, rest_123, _x_11033, _x_11044)
        return _x_11045
    _alt_11047 = _f_11046
    if len(code) == 0:
        _x_11049 = _alt_11026()
        return _x_11049
    else:
        head_11050 = code[0]
        tail_11051 = code[1:]
        _x_11052 = _alt_11047(head_11050, tail_11051)
        return _x_11052

# Lean: Corpus.Combinatorics.nthPermutation.go
def nth_permutation_go(k_124: int, n_125: int, available: list[int], acc_126: list[int]) -> list[int]:
    def _f_11056():
        _x_11055 = list(reversed(acc_126))
        return _x_11055
    _alt_11057 = _f_11056
    def _f_11087(x_11058: list[int]):
        _x_11062 = len(available)
        _x_11063 = 1
        _x_11066 = _x_11062 - 1
        _x_11067 = factorial(_x_11066)
        _x_11071 = k_124 // _x_11067
        _x_11072 = 0
        _x_11075 = get_d(None, available, _x_11071, 0)
        _x_11079 = k_124 % _x_11067
        def _f_11083(x_11080: int):
            _x_11082 = (lambda a, b: a != b)(_x_11075)
            return _x_11082
        _x_11084 = [x for x in available if _f_11083(x)]
        _x_11085 = [_x_11075] + acc_126
        _x_11086 = nth_permutation_go(_x_11079, n_125, _x_11084, _x_11085)
        return _x_11086
    _alt_11088 = _f_11087
    if len(available) == 0:
        _x_11090 = _alt_11057()
        return _x_11090
    else:
        head_11091 = available[0]
        tail_11092 = available[1:]
        _x_11093 = [head_11091] + tail_11092
        _x_11094 = _alt_11088(_x_11093)
        return _x_11094

# Lean: Corpus.Combinatorics.fromLehmerCode.go
def from_lehmer_code_go(code_129: list[int], available_130: list[int], acc_131: list[int]) -> list[int]:
    def _f_11098():
        _x_11097 = list(reversed(acc_131))
        return _x_11097
    _alt_11099 = _f_11098
    def _f_11111(c_133: int, rest_134: list[int]):
        _x_11100 = 0
        _x_11103 = get_d(None, available_130, c_133, 0)
        def _f_11107(x_11104: int):
            _x_11106 = (lambda a, b: a != b)(_x_11103)
            return _x_11106
        _x_11108 = [x for x in available_130 if _f_11107(x)]
        _x_11109 = [_x_11103] + acc_131
        _x_11110 = from_lehmer_code_go(rest_134, _x_11108, _x_11109)
        return _x_11110
    _alt_11112 = _f_11111
    if len(code_129) == 0:
        _x_11114 = _alt_11099()
        return _x_11114
    else:
        head_11115 = code_129[0]
        tail_11116 = code_129[1:]
        _x_11117 = _alt_11112(head_11115, tail_11116)
        return _x_11117

# Lean: Corpus.Combinatorics.lehmerCode.go
def lehmer_code_go(perm: list[int], acc_136: list[int]) -> list[int]:
    def _f_11121():
        _x_11120 = list(reversed(acc_136))
        return _x_11120
    _alt_11122 = _f_11121
    def _f_11141(x_138: int, rest_139: list[int]):
        def _f_11134(acc_140: int, y_141: int):
            _x_11123 = y_141 < x_138
            if _x_11123:
                _x_11129 = 1
                _x_11132 = acc_140 + 1
                return _x_11132
            else:
                return acc_140
        _x_11135 = 0
        _x_11138 = functools.reduce(_f_11134, rest_139, 0)
        _x_11139 = [_x_11138] + acc_136
        _x_11140 = lehmer_code_go(rest_139, _x_11139)
        return _x_11140
    _alt_11142 = _f_11141
    if len(perm) == 0:
        _x_11144 = _alt_11122()
        return _x_11144
    else:
        head_11145 = perm[0]
        tail_11146 = perm[1:]
        _x_11147 = _alt_11142(head_11145, tail_11146)
        return _x_11147

# Lean: Corpus.Combinatorics.countInversions.count
def count(xs_143: list[int]) -> int:
    def _f_11153():
        _x_11150 = 0
        return 0
    _alt_11154 = _f_11153
    def _f_11173(x_145: int, rest_146: list[int]):
        def _f_11166(acc_147: int, y_148: int):
            _x_11158 = y_148 < x_145
            if _x_11158:
                _x_11161 = 1
                _x_11164 = acc_147 + 1
                return _x_11164
            else:
                return acc_147
        _x_11167 = 0
        _x_11170 = functools.reduce(_f_11166, rest_146, 0)
        _x_11171 = count(rest_146)
        _x_11172 = _x_11170 + _x_11171
        return _x_11172
    _alt_11174 = _f_11173
    if len(xs_143) == 0:
        _x_11176 = _alt_11154()
        return _x_11176
    else:
        head_11177 = xs_143[0]
        tail_11178 = xs_143[1:]
        _x_11179 = _alt_11174(head_11177, tail_11178)
        return _x_11179

# Lean: Corpus.Combinatorics.partitionCount.p
def p(n_149: int, k_150: int) -> int:
    _x_11184 = 0
    _x_11187 = n_149 == 0
    _x_11188 = True
    if _x_11187:
        _x_11216 = 1
        return 1
    else:
        _x_11191 = k_150 == 0
        if _x_11191:
            return 0
        else:
            _x_11194 = n_149 < k_150
            if _x_11194:
                _x_11211 = p(n_149, n_149)
                return _x_11211
            else:
                _x_11202 = n_149 - k_150
                _x_11203 = p(_x_11202, k_150)
                _x_11204 = 1
                _x_11207 = k_150 - 1
                _x_11208 = p(n_149, _x_11207)
                _x_11209 = _x_11203 + _x_11208
                return _x_11209

# Lean: Corpus.Combinatorics.bell.go
def bell_go(n_151: int, i_152: int, acc_153: int) -> int:
    _x_11226 = 1
    _x_11229 = n_151 + 1
    _x_11230 = i_152 == _x_11229
    _x_11231 = True
    if _x_11230:
        return acc_153
    else:
        _x_11234 = i_152 + 1
        _x_11235 = stirling2(n_151, i_152)
        _x_11236 = acc_153 + _x_11235
        _x_11237 = bell_go(n_151, _x_11234, _x_11236)
        return _x_11237

# Lean: Corpus.Combinatorics.fallingFactorial.go
def falling_factorial_go(x_154: int, n_155: int, i_156: int, acc_157: int) -> int:
    _x_11243 = i_156 == n_155
    _x_11244 = True
    if _x_11243:
        return acc_157
    else:
        _x_11250 = 1
        _x_11253 = i_156 + 1
        _x_11260 = x_154 - i_156
        _x_11261 = acc_157 * _x_11260
        _x_11262 = falling_factorial_go(x_154, n_155, _x_11253, _x_11261)
        return _x_11262

# Lean: Corpus.Combinatorics.risingFactorial.go
def rising_factorial_go(x_158: int, n_159: int, i_160: int, acc_161: int) -> int:
    _x_11268 = i_160 == n_159
    _x_11269 = True
    if _x_11268:
        return acc_161
    else:
        _x_11275 = 1
        _x_11278 = i_160 + 1
        _x_11282 = x_158 + i_160
        _x_11283 = acc_161 * _x_11282
        _x_11284 = rising_factorial_go(x_158, n_159, _x_11278, _x_11283)
        return _x_11284

# Lean: Corpus.Geometry.segmentsIntersect.onSegment
def on_segment(p_162: Point2D, q: Point2D, r_163: Point2D) -> bool:
    def _f_11289():
        _x_11288 = False
        return False
    _alt_11290 = _f_11289
    def _f_11299():
        _x_11292 = min
        _x_11293 = p_162.point2d_1
        _x_11294 = r_163.point2d_1
        _x_11295 = _x_11292(_x_11293, _x_11294)
        _x_11296 = q.point2d_1
        _x_11297 = float_dec_le(_x_11295, _x_11296)
        return _x_11297
    _alt_11300 = _f_11299
    _alt_11301 = _f_11289
    def _f_11310():
        _x_11302 = q.point2d_1
        _x_11304 = max
        _x_11305 = p_162.point2d_1
        _x_11306 = r_163.point2d_1
        _x_11307 = _x_11304(_x_11305, _x_11306)
        _x_11308 = float_dec_le(_x_11302, _x_11307)
        return _x_11308
    _alt_11311 = _f_11310
    _alt_11312 = _f_11289
    def _f_11321():
        _x_11314 = min
        _x_11315 = p_162.point2d_0
        _x_11316 = r_163.point2d_0
        _x_11317 = _x_11314(_x_11315, _x_11316)
        _x_11318 = q.point2d_0
        _x_11319 = float_dec_le(_x_11317, _x_11318)
        return _x_11319
    _alt_11322 = _f_11321
    _x_11323 = q.point2d_0
    _x_11325 = max
    _x_11326 = p_162.point2d_0
    _x_11327 = r_163.point2d_0
    _x_11328 = _x_11325(_x_11326, _x_11327)
    _x_11329 = float_dec_le(_x_11323, _x_11328)
    def _jp_11353(_y_11335: bool):
        def _jp_11346(_y_11340: bool):
            if _y_11340:
                _x_11344 = _alt_11300()
                return _x_11344
            else:
                _x_11342 = _alt_11290()
                return _x_11342
        def _jp_11352():
            _x_11351 = _alt_11311()
            return _jp_11346(_x_11351)
        def _jp_11349():
            _x_11348 = _alt_11301()
            return _jp_11346(_x_11348)
        if _y_11335:
            return _jp_11352()
        else:
            return _jp_11349()
    def _jp_11359():
        _x_11358 = _alt_11322()
        return _jp_11353(_x_11358)
    def _jp_11356():
        _x_11355 = _alt_11312()
        return _jp_11353(_x_11355)
    if _x_11329:
        return _jp_11359()
    else:
        return _jp_11356()

# Lean: Corpus.Geometry.isConvexPolygon.checkSign
def check_sign(c_168: float, sign: bool | None) -> bool:
    def _f_11362():
        _x_11361 = True
        return True
    _alt_11363 = _f_11362
    def _f_11387(s: bool):
        _alt_11364 = _f_11362
        def _f_11374():
            _x_11368 = 0
            _x_11371 = float_dec_lt(0, c_168)
            _x_11373 = _x_11371 == s
            return _x_11373
        _alt_11375 = _f_11374
        _x_11378 = 0
        _x_11381 = c_168 == 0
        if _x_11381:
            _x_11385 = _alt_11364()
            return _x_11385
        else:
            _x_11383 = _alt_11375()
            return _x_11383
    _alt_11388 = _f_11387
    if sign is None:
        _x_11390 = _alt_11363()
        return _x_11390
    else:
        val_11391 = sign
        _x_11392 = _alt_11388(val_11391)
        return _x_11392

# Lean: Corpus.Geometry.isConvexPolygon.sub
def sub(a_171: Point2D, b_172: Point2D) -> Point2D:
    _x_11398 = a_171.point2d_0
    _x_11399 = b_172.point2d_0
    _x_11400 = _x_11398 - _x_11399
    _x_11401 = a_171.point2d_1
    _x_11402 = b_172.point2d_1
    _x_11403 = _x_11401 - _x_11402
    _x_11404 = Point2D_mk(_x_11400, _x_11403)
    return _x_11404

# Lean: Corpus.Geometry.isConvexPolygon.check
def is_convex_polygon_check(first: Point2D, second: Point2D, prev2: Point2D, prev1: Point2D, vs: list[Point2D], sign_173: bool | None) -> bool:
    def _f_11423():
        _x_11406 = sub(prev1, prev2)
        _x_11407 = sub(first, prev1)
        _x_11408 = cross2d(_x_11406, _x_11407)
        _x_11409 = sub(second, first)
        _x_11410 = cross2d(_x_11407, _x_11409)
        def _f_11412():
            _x_11411 = False
            return False
        _alt_11413 = _f_11412
        def _f_11415():
            _x_11414 = check_sign(_x_11410, sign_173)
            return _x_11414
        _alt_11416 = _f_11415
        _x_11417 = check_sign(_x_11408, sign_173)
        if _x_11417:
            _x_11421 = _alt_11416()
            return _x_11421
        else:
            _x_11419 = _alt_11413()
            return _x_11419
    _alt_11424 = _f_11423
    def _f_11455(v: Point2D, rest_: list[Point2D]):
        _x_11425 = sub(prev1, prev2)
        _x_11426 = sub(v, prev1)
        _x_11427 = cross2d(_x_11425, _x_11426)
        def _f_11429():
            _x_11428 = False
            return False
        _alt_11430 = _f_11429
        def _f_11447():
            _x_11433 = 0
            _x_11436 = _x_11427 == 0
            _x_11437 = True
            def _jp_11446(_y_11444: bool | None):
                _x_11445 = is_convex_polygon_check(first, second, prev1, v, rest_, _y_11444)
                return _x_11445
            if _x_11436:
                return _jp_11446(sign_173)
            else:
                _x_11440 = float_dec_lt(0, _x_11427)
                _x_11442 = _x_11440
                return _jp_11446(_x_11442)
        _alt_11448 = _f_11447
        _x_11449 = check_sign(_x_11427, sign_173)
        if _x_11449:
            _x_11453 = _alt_11448()
            return _x_11453
        else:
            _x_11451 = _alt_11430()
            return _x_11451
    _alt_11456 = _f_11455
    if len(vs) == 0:
        _x_11458 = _alt_11424()
        return _x_11458
    else:
        head_11459 = vs[0]
        tail_11460 = vs[1:]
        _x_11461 = _alt_11456(head_11459, tail_11460)
        return _x_11461

# Lean: Corpus.Geometry.polygonArea.go
def polygon_area_go(vs_180: list[Point2D], first_181: Point2D, prev_182: Point2D, acc_183: float) -> float:
    def _f_11476():
        _x_11470 = cross2d(prev_182, first_181)
        _x_11471 = acc_183 + _x_11470
        _x_11472 = 2
        _x_11475 = _x_11471 // 2
        return _x_11475
    _alt_11477 = _f_11476
    def _f_11484(v_185: Point2D, rest_186: list[Point2D]):
        _x_11481 = cross2d(prev_182, v_185)
        _x_11482 = acc_183 + _x_11481
        _x_11483 = polygon_area_go(rest_186, first_181, v_185, _x_11482)
        return _x_11483
    _alt_11485 = _f_11484
    if len(vs_180) == 0:
        _x_11487 = _alt_11477()
        return _x_11487
    else:
        head_11488 = vs_180[0]
        tail_11489 = vs_180[1:]
        _x_11490 = _alt_11485(head_11488, tail_11489)
        return _x_11490

# Lean: Corpus.Geometry.pointInTriangle.sign
def sign(p1: Point2D, p2: Point2D, p3: Point2D) -> float:
    _x_11499 = p1.point2d_0
    _x_11500 = p3.point2d_0
    _x_11501 = _x_11499 - _x_11500
    _x_11502 = p2.point2d_1
    _x_11503 = p3.point2d_1
    _x_11504 = _x_11502 - _x_11503
    _x_11505 = _x_11501 * _x_11504
    _x_11506 = p2.point2d_0
    _x_11507 = _x_11506 - _x_11500
    _x_11508 = p1.point2d_1
    _x_11509 = _x_11508 - _x_11503
    _x_11510 = _x_11507 * _x_11509
    _x_11511 = _x_11505 - _x_11510
    return _x_11511

# Lean: Corpus.NumberTheory.isHarshad.digitSum
def digit_sum(n_187: int) -> int:
    _x_11515 = 0
    _x_11518 = n_187 == 0
    _x_11519 = True
    if _x_11518:
        return 0
    else:
        _x_11528 = 10
        _x_11531 = n_187 % 10
        _x_11535 = n_187 // 10
        _x_11536 = digit_sum(_x_11535)
        _x_11537 = _x_11531 + _x_11536
        return _x_11537

# Lean: Corpus.NumberTheory.digitalRoot.digitSum
def digit_sum(n_188: int) -> int:
    _x_11543 = 0
    _x_11546 = n_188 == 0
    _x_11547 = True
    if _x_11546:
        return 0
    else:
        _x_11556 = 10
        _x_11559 = n_188 % 10
        _x_11563 = n_188 // 10
        _x_11564 = digit_sum(_x_11563)
        _x_11565 = _x_11559 + _x_11564
        return _x_11565

# Lean: Corpus.NumberTheory.isqrt.go
def isqrt_go(n_189: int, x_190: int, fuel: int) -> int:
    def _f_11569():
        return x_190
    _alt_11570 = _f_11569
    def _f_11588(fuel_: int):
        _x_11577 = n_189 // x_190
        _x_11578 = x_190 + _x_11577
        _x_11579 = 2
        _x_11582 = _x_11578 // 2
        _x_11583 = x_190 <= _x_11582
        if _x_11583:
            return x_190
        else:
            _x_11585 = isqrt_go(n_189, _x_11582, fuel_)
            return _x_11585
    _alt_11589 = _f_11588
    if fuel == 0:
        _x_11591 = _alt_11570()
        return _x_11591
    else:
        n_11592 = fuel - 1
        _x_11593 = _alt_11589(n_11592)
        return _x_11593

# Lean: Corpus.NumberTheory.totient.gcd
def totient_gcd(a_193: int, b_194: int) -> int:
    _x_11598 = 0
    _x_11601 = b_194 == 0
    _x_11602 = True
    if _x_11601:
        return a_193
    else:
        _x_11608 = a_193 % b_194
        _x_11609 = totient_gcd(b_194, _x_11608)
        return _x_11609

# Lean: Corpus.NumberTheory.totient.count
def count(n_195: int, i_196: int, acc_197: int) -> int:
    _x_11615 = i_196 == n_195
    _x_11616 = True
    if _x_11615:
        return acc_197
    else:
        _x_11619 = totient_gcd(i_196, n_195)
        _x_11620 = 1
        _x_11623 = _x_11619 == 1
        if _x_11623:
            _x_11635 = i_196 + 1
            _x_11636 = acc_197 + 1
            _x_11637 = count(n_195, _x_11635, _x_11636)
            return _x_11637
        else:
            _x_11629 = i_196 + 1
            _x_11630 = count(n_195, _x_11629, acc_197)
            return _x_11630

# Lean: Corpus.Advanced.Graph.topoSort.loop
def topo_sort_loop(g: Graph, queue: list[int], in_deg: list[int], result: list[int], fuel_198: int) -> list[int] | None:
    def _f_11643():
        _x_11642 = None
        return _x_11642
    _alt_11644 = _f_11643
    def _f_11735(fuel__200: int):
        def _f_11658():
            _x_11647 = len(result)
            _x_11648 = g.advanced_graph_0
            _x_11649 = _x_11647 == _x_11648
            _x_11650 = True
            if _x_11649:
                _x_11655 = list(reversed(result))
                _x_11656 = _x_11655
                return _x_11656
            else:
                _x_11653 = None
                return _x_11653
        _alt_11659 = _f_11658
        def _f_11727(v_202: int, rest_203: list[int]):
            _x_11660 = [v_202] + result
            def _f_11666(x_11661: tuple[int, int]):
                _x_11664 = x_11661[0]
                _x_11665 = _x_11664 == v_202
                return _x_11665
            _x_11667 = g.advanced_graph_1
            _x_11668 = [x for x in _x_11667 if _f_11666(x)]
            def _f_11670(new_in_deg: list[int], new_queue: list[int]):
                _x_11669 = topo_sort_loop(g, new_queue, new_in_deg, _x_11660, fuel__200)
                return _x_11669
            _alt_11671 = _f_11670
            def _f_11720(x_11672: tuple[list[int], list[int]], x_11673: tuple[int, int]):
                def _f_11714(deg: list[int], q_204: list[int]):
                    def _f_11708(fst_11674: int, w: int):
                        def _f_11697(d_205: int):
                            _x_11678 = 1
                            _x_11681 = d_205 - 1
                            _x_11682 = deg[:w] + [_x_11681] + deg[w+1:]
                            _x_11685 = 0
                            _x_11688 = _x_11681 == 0
                            _x_11689 = True
                            if _x_11688:
                                _x_11694 = [w] + q_204
                                _x_11695 = (_x_11682, _x_11694)
                                return _x_11695
                            else:
                                _x_11692 = (_x_11682, q_204)
                                return _x_11692
                        _alt_11698 = _f_11697
                        def _f_11700():
                            _x_11699 = (deg, q_204)
                            return _x_11699
                        _alt_11701 = _f_11700
                        _x_11702 = deg[w] if 0 <= w < len(deg) else None
                        if _x_11702 is None:
                            _x_11704 = _alt_11701()
                            return _x_11704
                        else:
                            val_11705 = _x_11702
                            _x_11706 = _alt_11698(val_11705)
                            return _x_11706
                    _alt_11709 = _f_11708
                    match x_11673:
                        case (fst_11710, snd_11711):
                            _x_11712 = _alt_11709(fst_11710, snd_11711)
                            return _x_11712
                _alt_11715 = _f_11714
                match x_11672:
                    case (fst_11716, snd_11717):
                        _x_11718 = _alt_11715(fst_11716, snd_11717)
                        return _x_11718
            _x_11721 = (in_deg, rest_203)
            _x_11722 = functools.reduce(_f_11720, _x_11668, _x_11721)
            match _x_11722:
                case (fst_11723, snd_11724):
                    _x_11725 = _alt_11671(fst_11723, snd_11724)
                    return _x_11725
        _alt_11728 = _f_11727
        if len(queue) == 0:
            _x_11730 = _alt_11659()
            return _x_11730
        else:
            head_11731 = queue[0]
            tail_11732 = queue[1:]
            _x_11733 = _alt_11728(head_11731, tail_11732)
            return _x_11733
    _alt_11736 = _f_11735
    if fuel_198 == 0:
        _x_11738 = _alt_11644()
        return _x_11738
    else:
        n_11739 = fuel_198 - 1
        _x_11740 = _alt_11736(n_11739)
        return _x_11740

# Lean: Corpus.Advanced.Graph.dfs.loop
def dfs_loop(g_207: Graph, stack: list[int], visited: list[int], fuel_208: int) -> list[int]:
    def _f_11744():
        _x_11743 = list(reversed(visited))
        return _x_11743
    _alt_11745 = _f_11744
    def _f_11775(fuel__210: int):
        _alt_11746 = _f_11744
        def _f_11767(v_211: int, rest_212: list[int]):
            _x_11748 = v_211 in visited
            _x_11749 = True
            if _x_11748:
                _x_11765 = dfs_loop(g_207, rest_212, visited, fuel__210)
                return _x_11765
            else:
                _x_11752 = [v_211] + visited
                def _f_11756(x_11753: int):
                    _x_11754 = x_11753 in _x_11752
                    _x_11755 = not _x_11754
                    return _x_11755
                _x_11757 = advanced_graph_neighbors(g_207, v_211)
                _x_11758 = [x for x in _x_11757 if _f_11756(x)]
                _x_11762 = _x_11758 + rest_212
                _x_11763 = dfs_loop(g_207, _x_11762, _x_11752, fuel__210)
                return _x_11763
        _alt_11768 = _f_11767
        if len(stack) == 0:
            _x_11770 = _alt_11746()
            return _x_11770
        else:
            head_11771 = stack[0]
            tail_11772 = stack[1:]
            _x_11773 = _alt_11768(head_11771, tail_11772)
            return _x_11773
    _alt_11776 = _f_11775
    if fuel_208 == 0:
        _x_11778 = _alt_11745()
        return _x_11778
    else:
        n_11779 = fuel_208 - 1
        _x_11780 = _alt_11776(n_11779)
        return _x_11780

# Lean: Corpus.Advanced.Graph.bfs.loop
def bfs_loop(g_213: Graph, queue_214: list[int], visited_215: list[int], fuel_216: int) -> list[int]:
    def _f_11784():
        _x_11783 = list(reversed(visited_215))
        return _x_11783
    _alt_11785 = _f_11784
    def _f_11815(fuel__218: int):
        _alt_11786 = _f_11784
        def _f_11807(v_219: int, rest_220: list[int]):
            _x_11788 = v_219 in visited_215
            _x_11789 = True
            if _x_11788:
                _x_11805 = bfs_loop(g_213, rest_220, visited_215, fuel__218)
                return _x_11805
            else:
                _x_11792 = [v_219] + visited_215
                def _f_11796(x_11793: int):
                    _x_11794 = x_11793 in _x_11792
                    _x_11795 = not _x_11794
                    return _x_11795
                _x_11797 = advanced_graph_neighbors(g_213, v_219)
                _x_11798 = [x for x in _x_11797 if _f_11796(x)]
                _x_11802 = rest_220 + _x_11798
                _x_11803 = bfs_loop(g_213, _x_11802, _x_11792, fuel__218)
                return _x_11803
        _alt_11808 = _f_11807
        if len(queue_214) == 0:
            _x_11810 = _alt_11786()
            return _x_11810
        else:
            head_11811 = queue_214[0]
            tail_11812 = queue_214[1:]
            _x_11813 = _alt_11808(head_11811, tail_11812)
            return _x_11813
    _alt_11816 = _f_11815
    if fuel_216 == 0:
        _x_11818 = _alt_11785()
        return _x_11818
    else:
        n_11819 = fuel_216 - 1
        _x_11820 = _alt_11816(n_11819)
        return _x_11820

# Lean: Corpus.Advanced.heapSort.extract
def extract(__223: Any, inst_11823: Any, h: Any, acc_224: list[Any], fuel_225: int) -> list[Any]:
    def _f_11825():
        _x_11824 = list(reversed(acc_224))
        return _x_11824
    _alt_11826 = _f_11825
    def _f_11839(fuel__227: int):
        _alt_11827 = _f_11825
        def _f_11831(x_228: Any):
            _x_11828 = pop_min(None, inst_11823, h)
            _x_11829 = [x_228] + acc_224
            _x_11830 = extract(None, inst_11823, _x_11828, _x_11829, fuel__227)
            return _x_11830
        _alt_11832 = _f_11831
        _x_11833 = advanced_heap_min(None, h)
        if _x_11833 is None:
            _x_11835 = _alt_11827()
            return _x_11835
        else:
            val_11836 = _x_11833
            _x_11837 = _alt_11832(val_11836)
            return _x_11837
    _alt_11840 = _f_11839
    if fuel_225 == 0:
        _x_11842 = _alt_11826()
        return _x_11842
    else:
        n_11843 = fuel_225 - 1
        _x_11844 = _alt_11840(n_11843)
        return _x_11844

# Lean: Corpus.DataStructures.Trie.hasPrefix.go
def has_prefix_go(t: Trie, chars: list[str]) -> bool:
    def _f_11849(x_11847: Trie):
        _x_11848 = True
        return True
    _alt_11850 = _f_11849
    def _f_11881(a_11851: bool, children: list[tuple[str, Trie]], c_229: str, cs: list[str]):
        def _f_11854(fst_11852: str, child: Trie):
            _x_11853 = has_prefix_go(child, cs)
            return _x_11853
        _alt_11855 = _f_11854
        def _f_11857():
            _x_11856 = False
            return False
        _alt_11858 = _f_11857
        def _f_11871(x_11859: tuple[str, Trie]):
            def _f_11865(ch: str, snd_11860: Trie):
                _x_11864 = ch == c_229
                return _x_11864
            _alt_11866 = _f_11865
            match x_11859:
                case (fst_11867, snd_11868):
                    _x_11869 = _alt_11866(fst_11867, snd_11868)
                    return _x_11869
        _x_11872 = next((x for x in children if _f_11871(x)), None)
        if _x_11872 is None:
            _x_11874 = _alt_11858()
            return _x_11874
        else:
            val_11875 = _x_11872
            match val_11875:
                case (fst_11876, snd_11877):
                    _x_11878 = _alt_11855(fst_11876, snd_11877)
                    return _x_11878
    _alt_11882 = _f_11881
    match t:
        case Trie_node(a_11883, a_11884):
            if len(chars) == 0:
                _x_11885 = Trie_node(a_11883, a_11884)
                _x_11886 = _alt_11850(_x_11885)
                return _x_11886
            else:
                head_11887 = chars[0]
                tail_11888 = chars[1:]
                _x_11889 = _alt_11882(a_11883, a_11884, head_11887, tail_11888)
                return _x_11889

# Lean: Corpus.DataStructures.Trie.contains.go
def trie_contains_go(t_231: Trie, chars_232: list[str]) -> bool:
    def _f_11894(is_end: bool, a_11893: list[tuple[str, Trie]]):
        return is_end
    _alt_11895 = _f_11894
    def _f_11926(a_11896: bool, children_233: list[tuple[str, Trie]], c_234: str, cs_235: list[str]):
        def _f_11899(fst_11897: str, child_236: Trie):
            _x_11898 = trie_contains_go(child_236, cs_235)
            return _x_11898
        _alt_11900 = _f_11899
        def _f_11902():
            _x_11901 = False
            return False
        _alt_11903 = _f_11902
        def _f_11916(x_11904: tuple[str, Trie]):
            def _f_11910(ch_238: str, snd_11905: Trie):
                _x_11909 = ch_238 == c_234
                return _x_11909
            _alt_11911 = _f_11910
            match x_11904:
                case (fst_11912, snd_11913):
                    _x_11914 = _alt_11911(fst_11912, snd_11913)
                    return _x_11914
        _x_11917 = next((x for x in children_233 if _f_11916(x)), None)
        if _x_11917 is None:
            _x_11919 = _alt_11903()
            return _x_11919
        else:
            val_11920 = _x_11917
            match val_11920:
                case (fst_11921, snd_11922):
                    _x_11923 = _alt_11900(fst_11921, snd_11922)
                    return _x_11923
    _alt_11927 = _f_11926
    match t_231:
        case Trie_node(a_11928, a_11929):
            if len(chars_232) == 0:
                _x_11930 = _alt_11895(a_11928, a_11929)
                return _x_11930
            else:
                head_11931 = chars_232[0]
                tail_11932 = chars_232[1:]
                _x_11933 = _alt_11927(a_11928, a_11929, head_11931, tail_11932)
                return _x_11933

# Lean: Corpus.DataStructures.Trie.insert.go
def trie_insert_go(t_239: Trie, chars_240: list[str]) -> Trie:
    def _f_11939(is_end_241: bool, children_242: list[tuple[str, Trie]]):
        _x_11937 = True
        _x_11938 = Trie_node(True, children_242)
        return _x_11938
    _alt_11940 = _f_11939
    def _f_12002(is_end_243: bool, children_244: list[tuple[str, Trie]], c_245: str, cs_246: list[str]):
        def _f_11963(fst_11941: str, child_247: Trie):
            def _f_11961(x_11942: tuple[str, Trie]):
                def _f_11955(ch_248: str, t_: Trie):
                    _x_11946 = ch_248 == c_245
                    _x_11947 = True
                    if _x_11946:
                        _x_11952 = trie_insert_go(t_, cs_246)
                        _x_11953 = (ch_248, _x_11952)
                        return _x_11953
                    else:
                        _x_11950 = (ch_248, t_)
                        return _x_11950
                _alt_11956 = _f_11955
                match x_11942:
                    case (fst_11957, snd_11958):
                        _x_11959 = _alt_11956(fst_11957, snd_11958)
                        return _x_11959
            _x_11962 = [_f_11961(x) for x in children_244]
            return _x_11962
        _alt_11964 = _f_11963
        def _f_11969():
            _x_11965 = trie_empty()
            _x_11966 = trie_insert_go(_x_11965, cs_246)
            _x_11967 = (c_245, _x_11966)
            _x_11968 = [_x_11967] + children_244
            return _x_11968
        _alt_11970 = _f_11969
        def _f_11983(x_11971: tuple[str, Trie]):
            def _f_11977(ch_250: str, snd_11972: Trie):
                _x_11976 = ch_250 == c_245
                return _x_11976
            _alt_11978 = _f_11977
            match x_11971:
                case (fst_11979, snd_11980):
                    _x_11981 = _alt_11978(fst_11979, snd_11980)
                    return _x_11981
        _x_11984 = next((x for x in children_244 if _f_11983(x)), None)
        def _jp_11994(_y_11992: list[tuple[str, Trie]]):
            _x_11993 = Trie_node(is_end_243, _y_11992)
            return _x_11993
        def _jp_11997():
            _x_11996 = _alt_11970()
            return _jp_11994(_x_11996)
        def _jp_12001(_y_11998: str, _y_11999: Trie):
            _x_12000 = _alt_11964(_y_11998, _y_11999)
            return _jp_11994(_x_12000)
        if _x_11984 is None:
            return _jp_11997()
        else:
            val_11987 = _x_11984
            match val_11987:
                case (fst_11988, snd_11989):
                    return _jp_12001(fst_11988, snd_11989)
    _alt_12003 = _f_12002
    match t_239:
        case Trie_node(a_12004, a_12005):
            if len(chars_240) == 0:
                _x_12006 = _alt_11940(a_12004, a_12005)
                return _x_12006
            else:
                head_12007 = chars_240[0]
                tail_12008 = chars_240[1:]
                _x_12009 = _alt_12003(a_12004, a_12005, head_12007, tail_12008)
                return _x_12009

# Lean: Corpus.DataStructures.BinaryTree.levelOrder.go
def level_order_go(__251: Any, queue_252: list[Any], acc_253: list[Any], fuel_254: int) -> list[Any]:
    def _f_12014():
        _x_12013 = list(reversed(acc_253))
        return _x_12013
    _alt_12015 = _f_12014
    def _f_12042(fuel__256: int):
        _alt_12016 = _f_12014
        def _f_12018(rest_257: list[Any]):
            _x_12017 = level_order_go(None, rest_257, acc_253, fuel__256)
            return _x_12017
        _alt_12019 = _f_12018
        def _f_12029(v_258: Any, l_259: Any, r_260: Any, rest_261: list[Any]):
            _x_12023 = []
            _x_12024 = [r_260] + _x_12023
            _x_12025 = [l_259] + _x_12024
            _x_12026 = rest_261 + _x_12025
            _x_12027 = [v_258] + acc_253
            _x_12028 = level_order_go(None, _x_12026, _x_12027, fuel__256)
            return _x_12028
        _alt_12030 = _f_12029
        if len(queue_252) == 0:
            _x_12032 = _alt_12016()
            return _x_12032
        else:
            head_12033 = queue_252[0]
            tail_12034 = queue_252[1:]
            match head_12033:
                case BinaryTree_empty():
                    _x_12035 = _alt_12019(tail_12034)
                    return _x_12035
                case BinaryTree_node(a_12036, a_12037, a_12038):
                    _x_12039 = _alt_12030(a_12036, a_12037, a_12038, tail_12034)
                    return _x_12039
    _alt_12043 = _f_12042
    if fuel_254 == 0:
        _x_12045 = _alt_12015()
        return _x_12045
    else:
        n_12046 = fuel_254 - 1
        _x_12047 = _alt_12043(n_12046)
        return _x_12047

# Lean: Corpus.Games.rollDice.go
def roll_dice_go(sides: int, n_262: int, seed: int, acc_263: list[int]) -> tuple[list[int], int]:
    def _f_12052():
        _x_12050 = list(reversed(acc_263))
        _x_12051 = (_x_12050, seed)
        return _x_12051
    _alt_12053 = _f_12052
    def _f_12090(n_: int):
        _x_12063 = 1103515245
        _x_12066 = seed * 1103515245
        _x_12067 = 12345
        _x_12070 = _x_12066 + 12345
        _x_12075 = 2
        _x_12078 = 31
        _x_12081 = 2 ** 31
        _x_12082 = _x_12070 % _x_12081
        _x_12083 = _x_12082 % sides
        _x_12084 = 1
        _x_12087 = _x_12083 + 1
        _x_12088 = [_x_12087] + acc_263
        _x_12089 = roll_dice_go(sides, n_, _x_12082, _x_12088)
        return _x_12089
    _alt_12091 = _f_12090
    if n_262 == 0:
        _x_12093 = _alt_12053()
        return _x_12093
    else:
        n_12094 = n_262 - 1
        _x_12095 = _alt_12091(n_12094)
        return _x_12095

# Lean: Corpus.Games.BlackjackHand.bestValue.adjust
def best_value_adjust(value_265: int, aces: int) -> int:
    def _f_12098():
        return value_265
    _alt_12099 = _f_12098
    def _f_12115(aces_: int):
        _x_12100 = 21
        _x_12103 = value_265 <= 21
        if _x_12103:
            return value_265
        else:
            _x_12108 = 10
            _x_12111 = value_265 - 10
            _x_12112 = best_value_adjust(_x_12111, aces_)
            return _x_12112
    _alt_12116 = _f_12115
    if aces == 0:
        _x_12118 = _alt_12099()
        return _x_12118
    else:
        n_12119 = aces - 1
        _x_12120 = _alt_12116(n_12119)
        return _x_12120

# Lean: Corpus.Strings.words.go
def words_go(chars_267: list[str], current: list[str], acc_268: list[str]) -> list[str]:
    def _f_12134():
        _x_12123 = len(current) == 0
        _x_12124 = True
        if _x_12123:
            _x_12132 = list(reversed(acc_268))
            return _x_12132
        else:
            _x_12127 = list(reversed(current))
            _x_12128 = ''.join(_x_12127)
            _x_12129 = [_x_12128] + acc_268
            _x_12130 = list(reversed(_x_12129))
            return _x_12130
    _alt_12135 = _f_12134
    def _f_12161(c_270: str, cs_271: list[str]):
        _x_12139 = 32
        _x_12140 = chr(_x_12139)
        _x_12141 = c_270 == _x_12140
        _x_12142 = True
        if _x_12141:
            _x_12148 = len(current) == 0
            if _x_12148:
                _x_12157 = []
                _x_12158 = words_go(cs_271, _x_12157, acc_268)
                return _x_12158
            else:
                _x_12151 = []
                _x_12152 = list(reversed(current))
                _x_12153 = ''.join(_x_12152)
                _x_12154 = [_x_12153] + acc_268
                _x_12155 = words_go(cs_271, _x_12151, _x_12154)
                return _x_12155
        else:
            _x_12145 = [c_270] + current
            _x_12146 = words_go(cs_271, _x_12145, acc_268)
            return _x_12146
    _alt_12162 = _f_12161
    if len(chars_267) == 0:
        _x_12164 = _alt_12135()
        return _x_12164
    else:
        head_12165 = chars_267[0]
        tail_12166 = chars_267[1:]
        _x_12167 = _alt_12162(head_12165, tail_12166)
        return _x_12167

# Lean: Corpus.Strings.splitOn.go
def split_on_go(sep: str, chars_272: list[str], current_273: list[str], acc_274: list[str]) -> list[str]:
    def _f_12174():
        _x_12170 = list(reversed(current_273))
        _x_12171 = ''.join(_x_12170)
        _x_12172 = [_x_12171] + acc_274
        _x_12173 = list(reversed(_x_12172))
        return _x_12173
    _alt_12175 = _f_12174
    def _f_12203(cs_276: list[str]):
        _x_12176 = ''.join(cs_276)
        _x_12177 = starts_with(_x_12176, sep)
        _x_12178 = True
        if _x_12177:
            _x_12195 = len(sep)
            _x_12196 = (lambda n, xs: xs[n:])(cs_276)
            _x_12197 = []
            _x_12198 = list(reversed(current_273))
            _x_12199 = ''.join(_x_12198)
            _x_12200 = [_x_12199] + acc_274
            _x_12201 = split_on_go(sep, _x_12196, _x_12197, _x_12200)
            return _x_12201
        else:
            def _f_12183(c_277: str, cs_: list[str]):
                _x_12181 = [c_277] + current_273
                _x_12182 = split_on_go(sep, cs_, _x_12181, acc_274)
                return _x_12182
            _alt_12184 = _f_12183
            def _f_12186():
                _x_12185 = list(reversed(acc_274))
                return _x_12185
            _alt_12187 = _f_12186
            if len(cs_276) == 0:
                _x_12189 = _alt_12187()
                return _x_12189
            else:
                head_12190 = cs_276[0]
                tail_12191 = cs_276[1:]
                _x_12192 = _alt_12184(head_12190, tail_12191)
                return _x_12192
    _alt_12204 = _f_12203
    if len(chars_272) == 0:
        _x_12206 = _alt_12175()
        return _x_12206
    else:
        head_12207 = chars_272[0]
        tail_12208 = chars_272[1:]
        _x_12209 = [head_12207] + tail_12208
        _x_12210 = _alt_12204(_x_12209)
        return _x_12210

# Lean: Corpus.Strings.count.go
def count_go(sub: str, chars_279: list[str], cnt: int) -> int:
    def _f_12213():
        return cnt
    _alt_12214 = _f_12213
    def _f_12232(c_281: str, cs_282: list[str]):
        _x_12215 = [c_281] + cs_282
        _x_12216 = ''.join(_x_12215)
        _x_12217 = starts_with(_x_12216, sub)
        _x_12218 = True
        if _x_12217:
            _x_12226 = 1
            _x_12229 = cnt + 1
            _x_12230 = count_go(sub, cs_282, _x_12229)
            return _x_12230
        else:
            _x_12221 = count_go(sub, cs_282, cnt)
            return _x_12221
    _alt_12233 = _f_12232
    if len(chars_279) == 0:
        _x_12235 = _alt_12214()
        return _x_12235
    else:
        head_12236 = chars_279[0]
        tail_12237 = chars_279[1:]
        _x_12238 = _alt_12233(head_12236, tail_12237)
        return _x_12238

# Lean: Corpus.Strings.indexOf.go
def index_of_go(sub_283: str, chars_284: list[str], idx_285: int) -> int | None:
    def _f_12255():
        _x_12243 = len(sub_283)
        _x_12244 = 0
        _x_12247 = _x_12243 == 0
        _x_12248 = True
        if _x_12247:
            _x_12253 = idx_285
            return _x_12253
        else:
            _x_12251 = None
            return _x_12251
    _alt_12256 = _f_12255
    def _f_12274(c_287: str, cs_288: list[str]):
        _x_12257 = [c_287] + cs_288
        _x_12258 = ''.join(_x_12257)
        _x_12259 = starts_with(_x_12258, sub_283)
        _x_12260 = True
        if _x_12259:
            _x_12272 = idx_285
            return _x_12272
        else:
            _x_12266 = 1
            _x_12269 = idx_285 + 1
            _x_12270 = index_of_go(sub_283, cs_288, _x_12269)
            return _x_12270
    _alt_12275 = _f_12274
    if len(chars_284) == 0:
        _x_12277 = _alt_12256()
        return _x_12277
    else:
        head_12278 = chars_284[0]
        tail_12279 = chars_284[1:]
        _x_12280 = _alt_12275(head_12278, tail_12279)
        return _x_12280

# Lean: Corpus.Strings.contains.go
def strings_contains_go(sub_289: str, chars_290: list[str]) -> bool:
    def _f_12290():
        _x_12285 = len(sub_289)
        _x_12286 = 0
        _x_12289 = _x_12285 == 0
        return _x_12289
    _alt_12291 = _f_12290
    def _f_12301(c_292: str, cs_293: list[str]):
        _x_12292 = [c_292] + cs_293
        _x_12293 = ''.join(_x_12292)
        _x_12294 = starts_with(_x_12293, sub_289)
        _x_12295 = True
        if _x_12294:
            return True
        else:
            _x_12298 = strings_contains_go(sub_289, cs_293)
            return _x_12298
    _alt_12302 = _f_12301
    if len(chars_290) == 0:
        _x_12304 = _alt_12291()
        return _x_12304
    else:
        head_12305 = chars_290[0]
        tail_12306 = chars_290[1:]
        _x_12307 = _alt_12302(head_12305, tail_12306)
        return _x_12307

# Lean: Corpus.Strings.replicate.go
def strings_replicate_go(s_294: str, n_295: int, acc_296: str) -> str:
    def _f_12310():
        return acc_296
    _alt_12311 = _f_12310
    def _f_12317(n__298: int):
        _x_12315 = acc_296 + s_294
        _x_12316 = strings_replicate_go(s_294, n__298, _x_12315)
        return _x_12316
    _alt_12318 = _f_12317
    if n_295 == 0:
        _x_12320 = _alt_12311()
        return _x_12320
    else:
        n_12321 = n_295 - 1
        _x_12322 = _alt_12318(n_12321)
        return _x_12322

# Lean: Corpus.Math.digitalRoot.go
def digital_root_go(n_299: int, fuel_300: int) -> int:
    def _f_12325():
        return n_299
    _alt_12326 = _f_12325
    def _f_12336(fuel__302: int):
        _x_12327 = 10
        _x_12330 = digit_sum(n_299, 10)
        _x_12331 = _x_12330 < 10
        if _x_12331:
            return _x_12330
        else:
            _x_12333 = digital_root_go(_x_12330, fuel__302)
            return _x_12333
    _alt_12337 = _f_12336
    if fuel_300 == 0:
        _x_12339 = _alt_12326()
        return _x_12339
    else:
        n_12340 = fuel_300 - 1
        _x_12341 = _alt_12337(n_12340)
        return _x_12341

# Lean: Corpus.Math.digits.go
def digits_go(base: int, n_304: int, acc_305: list[int]) -> list[int]:
    _x_12346 = 0
    _x_12349 = n_304 == 0
    _x_12350 = True
    if _x_12349:
        _x_12364 = len(acc_305) == 0
        if _x_12364:
            _x_12368 = []
            _x_12369 = [0] + _x_12368
            return _x_12369
        else:
            return acc_305
    else:
        _x_12356 = n_304 // base
        _x_12360 = n_304 % base
        _x_12361 = [_x_12360] + acc_305
        _x_12362 = digits_go(base, _x_12356, _x_12361)
        return _x_12362

# Lean: Corpus.Math.isqrt.go
def isqrt_go(n_306: int, x_307: int, fuel_308: int) -> int:
    def _f_12373():
        return x_307
    _alt_12374 = _f_12373
    def _f_12392(fuel__310: int):
        _x_12381 = n_306 // x_307
        _x_12382 = x_307 + _x_12381
        _x_12383 = 2
        _x_12386 = _x_12382 // 2
        _x_12387 = x_307 <= _x_12386
        if _x_12387:
            return x_307
        else:
            _x_12389 = isqrt_go(n_306, _x_12386, fuel__310)
            return _x_12389
    _alt_12393 = _f_12392
    if fuel_308 == 0:
        _x_12395 = _alt_12374()
        return _x_12395
    else:
        n_12396 = fuel_308 - 1
        _x_12397 = _alt_12393(n_12396)
        return _x_12397

# Lean: Corpus.Math.binomial.go
def binomial_go(n_311: int, k_312: int, num: int, den: int, i_313: int) -> int:
    _x_12400 = k_312 < i_313
    if _x_12400:
        _x_12424 = num // den
        return _x_12424
    else:
        _x_12411 = n_311 - i_313
        _x_12412 = 1
        _x_12415 = _x_12411 + 1
        _x_12416 = num * _x_12415
        _x_12417 = den * i_313
        _x_12418 = i_313 + 1
        _x_12419 = binomial_go(n_311, k_312, _x_12416, _x_12417, _x_12418)
        return _x_12419

# Lean: Corpus.Math.tribonacci.go
def tribonacci_go(a_314: int, b_315: int, c_316: int, k_317: int) -> int:
    def _f_12427():
        return a_314
    _alt_12428 = _f_12427
    def _f_12435(k_: int):
        _x_12432 = a_314 + b_315
        _x_12433 = _x_12432 + c_316
        _x_12434 = tribonacci_go(b_315, c_316, _x_12433, k_)
        return _x_12434
    _alt_12436 = _f_12435
    if k_317 == 0:
        _x_12438 = _alt_12428()
        return _x_12438
    else:
        n_12439 = k_317 - 1
        _x_12440 = _alt_12436(n_12439)
        return _x_12440

# Lean: Corpus.Math.lucas.go
def lucas_go(a_319: int, b_320: int, k_321: int) -> int:
    def _f_12443():
        return a_319
    _alt_12444 = _f_12443
    def _f_12450(k__323: int):
        _x_12448 = a_319 + b_320
        _x_12449 = lucas_go(b_320, _x_12448, k__323)
        return _x_12449
    _alt_12451 = _f_12450
    if k_321 == 0:
        _x_12453 = _alt_12444()
        return _x_12453
    else:
        n_12454 = k_321 - 1
        _x_12455 = _alt_12451(n_12454)
        return _x_12455

# Lean: Corpus.Math.fibonacci.go
def math_fibonacci_go(a_324: int, b_325: int, k_326: int) -> int:
    def _f_12458():
        return a_324
    _alt_12459 = _f_12458
    def _f_12465(k__328: int):
        _x_12463 = a_324 + b_325
        _x_12464 = math_fibonacci_go(b_325, _x_12463, k__328)
        return _x_12464
    _alt_12466 = _f_12465
    if k_326 == 0:
        _x_12468 = _alt_12459()
        return _x_12468
    else:
        n_12469 = k_326 - 1
        _x_12470 = _alt_12466(n_12469)
        return _x_12470

# Lean: Corpus.Math.divisors.go
def divisors_go(n_329: int, d_330: int, acc_331: list[int]) -> list[int]:
    _x_12476 = d_330 * d_330
    _x_12477 = n_329 < _x_12476
    if _x_12477:
        return acc_331
    else:
        _x_12484 = n_329 % d_330
        _x_12485 = 0
        _x_12488 = _x_12484 == 0
        _x_12489 = True
        if _x_12488:
            _x_12501 = _x_12476 == n_329
            if _x_12501:
                _x_12522 = 1
                _x_12525 = d_330 + 1
                _x_12526 = [d_330] + acc_331
                _x_12527 = divisors_go(n_329, _x_12525, _x_12526)
                return _x_12527
            else:
                _x_12507 = 1
                _x_12510 = d_330 + 1
                _x_12514 = n_329 // d_330
                _x_12515 = [_x_12514] + acc_331
                _x_12516 = [d_330] + _x_12515
                _x_12517 = divisors_go(n_329, _x_12510, _x_12516)
                return _x_12517
        else:
            _x_12495 = 1
            _x_12498 = d_330 + 1
            _x_12499 = divisors_go(n_329, _x_12498, acc_331)
            return _x_12499

# Lean: Corpus.Math.primeFactors.go
def math_prime_factors_go(n_332: int, d_333: int, acc_334: list[int], fuel_335: int) -> list[int]:
    def _f_12534():
        _x_12533 = list(reversed(acc_334))
        return _x_12533
    _alt_12535 = _f_12534
    def _f_12580(fuel__337: int):
        _x_12536 = 1
        _x_12539 = n_332 <= 1
        if _x_12539:
            _x_12578 = list(reversed(acc_334))
            return _x_12578
        else:
            _x_12544 = d_333 * d_333
            _x_12545 = n_332 < _x_12544
            if _x_12545:
                _x_12574 = [n_332] + acc_334
                _x_12575 = list(reversed(_x_12574))
                return _x_12575
            else:
                _x_12552 = n_332 % d_333
                _x_12553 = 0
                _x_12556 = _x_12552 == 0
                _x_12557 = True
                if _x_12556:
                    _x_12569 = n_332 // d_333
                    _x_12570 = [d_333] + acc_334
                    _x_12571 = math_prime_factors_go(_x_12569, d_333, _x_12570, fuel__337)
                    return _x_12571
                else:
                    _x_12563 = d_333 + 1
                    _x_12564 = math_prime_factors_go(n_332, _x_12563, acc_334, fuel__337)
                    return _x_12564
    _alt_12581 = _f_12580
    if fuel_335 == 0:
        _x_12583 = _alt_12535()
        return _x_12583
    else:
        n_12584 = fuel_335 - 1
        _x_12585 = _alt_12581(n_12584)
        return _x_12585

# Lean: Corpus.Math.isPrime.check
def math_is_prime_check(n_338: int, d_339: int, fuel_340: int) -> bool:
    def _f_12589():
        _x_12588 = True
        return True
    _alt_12590 = _f_12589
    def _f_12624(fuel__342: int):
        _x_12594 = d_339 * d_339
        _x_12595 = n_338 < _x_12594
        if _x_12595:
            _x_12622 = True
            return True
        else:
            _x_12602 = n_338 % d_339
            _x_12603 = 0
            _x_12606 = _x_12602 == 0
            _x_12607 = True
            if _x_12606:
                _x_12619 = False
                return False
            else:
                _x_12613 = 1
                _x_12616 = d_339 + 1
                _x_12617 = math_is_prime_check(n_338, _x_12616, fuel__342)
                return _x_12617
    _alt_12625 = _f_12624
    if fuel_340 == 0:
        _x_12627 = _alt_12590()
        return _x_12627
    else:
        n_12628 = fuel_340 - 1
        _x_12629 = _alt_12625(n_12628)
        return _x_12629

# Lean: Corpus.Math.modPow.go
def mod_pow_go(m: int, b_343: int, e: int, acc_344: int) -> int:
    def _f_12636():
        _x_12635 = acc_344 % m
        return _x_12635
    _alt_12637 = _f_12636
    def _f_12679(x_12638: int):
        _x_12644 = 2
        _x_12647 = e % 2
        _x_12648 = 0
        _x_12651 = _x_12647 == 0
        _x_12652 = True
        if _x_12651:
            _x_12671 = b_343 * b_343
            _x_12672 = _x_12671 % m
            _x_12676 = e // 2
            _x_12677 = mod_pow_go(m, _x_12672, _x_12676, acc_344)
            return _x_12677
        else:
            _x_12658 = b_343 * b_343
            _x_12659 = _x_12658 % m
            _x_12663 = e // 2
            _x_12664 = acc_344 * b_343
            _x_12665 = _x_12664 % m
            _x_12666 = mod_pow_go(m, _x_12659, _x_12663, _x_12665)
            return _x_12666
    _alt_12680 = _f_12679
    _x_12681 = 0
    if e:
        _x_12685 = _alt_12680(e)
        return _x_12685
    else:
        _x_12687 = _alt_12637()
        return _x_12687

# Lean: Corpus.Math.fastPow.go
def fast_pow_go(b_346: int, e_347: int, acc_348: int) -> int:
    def _f_12690():
        return acc_348
    _alt_12691 = _f_12690
    def _f_12730(x_12692: int):
        _x_12698 = 2
        _x_12701 = e_347 % 2
        _x_12702 = 0
        _x_12705 = _x_12701 == 0
        _x_12706 = True
        if _x_12705:
            _x_12723 = b_346 * b_346
            _x_12727 = e_347 // 2
            _x_12728 = fast_pow_go(_x_12723, _x_12727, acc_348)
            return _x_12728
        else:
            _x_12712 = b_346 * b_346
            _x_12716 = e_347 // 2
            _x_12717 = acc_348 * b_346
            _x_12718 = fast_pow_go(_x_12712, _x_12716, _x_12717)
            return _x_12718
    _alt_12731 = _f_12730
    _x_12732 = 0
    if e_347:
        _x_12736 = _alt_12731(e_347)
        return _x_12736
    else:
        _x_12738 = _alt_12691()
        return _x_12738

# Lean: Corpus.Algorithms.reverse.go
def algorithms_reverse_go(__350: Any, xs_351: list[Any], acc_352: list[Any]) -> list[Any]:
    def _f_12741():
        return acc_352
    _alt_12742 = _f_12741
    def _f_12745(x_354: Any, xs_: list[Any]):
        _x_12743 = [x_354] + acc_352
        _x_12744 = algorithms_reverse_go(None, xs_, _x_12743)
        return _x_12744
    _alt_12746 = _f_12745
    if len(xs_351) == 0:
        _x_12748 = _alt_12742()
        return _x_12748
    else:
        head_12749 = xs_351[0]
        tail_12750 = xs_351[1:]
        _x_12751 = _alt_12746(head_12749, tail_12750)
        return _x_12751

# Lean: Corpus.Algorithms.power.go
def power_go(b_355: int, e_356: int, acc_357: int) -> int:
    def _f_12754():
        return acc_357
    _alt_12755 = _f_12754
    def _f_12794(x_12756: int):
        _x_12762 = 2
        _x_12765 = e_356 % 2
        _x_12766 = 0
        _x_12769 = _x_12765 == 0
        _x_12770 = True
        if _x_12769:
            _x_12787 = b_355 * b_355
            _x_12791 = e_356 // 2
            _x_12792 = power_go(_x_12787, _x_12791, acc_357)
            return _x_12792
        else:
            _x_12776 = b_355 * b_355
            _x_12780 = e_356 // 2
            _x_12781 = acc_357 * b_355
            _x_12782 = power_go(_x_12776, _x_12780, _x_12781)
            return _x_12782
    _alt_12795 = _f_12794
    _x_12796 = 0
    if e_356:
        _x_12800 = _alt_12795(e_356)
        return _x_12800
    else:
        _x_12802 = _alt_12755()
        return _x_12802

# Lean: Corpus.Algorithms.fibonacci.go
def algorithms_fibonacci_go(a_359: int, b_360: int, k_361: int) -> int:
    def _f_12805():
        return a_359
    _alt_12806 = _f_12805
    def _f_12812(k__363: int):
        _x_12810 = a_359 + b_360
        _x_12811 = algorithms_fibonacci_go(b_360, _x_12810, k__363)
        return _x_12811
    _alt_12813 = _f_12812
    if k_361 == 0:
        _x_12815 = _alt_12806()
        return _x_12815
    else:
        n_12816 = k_361 - 1
        _x_12817 = _alt_12813(n_12816)
        return _x_12817

# Lean: Corpus.Algorithms.primeFactors.go
def algorithms_prime_factors_go(n_364: int, d_365: int, acc_366: list[int], fuel_367: int) -> list[int]:
    def _f_12821():
        _x_12820 = list(reversed(acc_366))
        return _x_12820
    _alt_12822 = _f_12821
    def _f_12867(fuel__369: int):
        _x_12823 = 1
        _x_12826 = n_364 <= 1
        if _x_12826:
            _x_12865 = list(reversed(acc_366))
            return _x_12865
        else:
            _x_12831 = d_365 * d_365
            _x_12832 = n_364 < _x_12831
            if _x_12832:
                _x_12861 = [n_364] + acc_366
                _x_12862 = list(reversed(_x_12861))
                return _x_12862
            else:
                _x_12839 = n_364 % d_365
                _x_12840 = 0
                _x_12843 = _x_12839 == 0
                _x_12844 = True
                if _x_12843:
                    _x_12856 = n_364 // d_365
                    _x_12857 = [d_365] + acc_366
                    _x_12858 = algorithms_prime_factors_go(_x_12856, d_365, _x_12857, fuel__369)
                    return _x_12858
                else:
                    _x_12850 = d_365 + 1
                    _x_12851 = algorithms_prime_factors_go(n_364, _x_12850, acc_366, fuel__369)
                    return _x_12851
    _alt_12868 = _f_12867
    if fuel_367 == 0:
        _x_12870 = _alt_12822()
        return _x_12870
    else:
        n_12871 = fuel_367 - 1
        _x_12872 = _alt_12868(n_12871)
        return _x_12872

# Lean: Corpus.Algorithms.isPrime.check
def algorithms_is_prime_check(n_370: int, d_371: int, fuel_372: int) -> bool:
    def _f_12876():
        _x_12875 = True
        return True
    _alt_12877 = _f_12876
    def _f_12911(fuel__374: int):
        _x_12881 = d_371 * d_371
        _x_12882 = n_370 < _x_12881
        if _x_12882:
            _x_12909 = True
            return True
        else:
            _x_12889 = n_370 % d_371
            _x_12890 = 0
            _x_12893 = _x_12889 == 0
            _x_12894 = True
            if _x_12893:
                _x_12906 = False
                return False
            else:
                _x_12900 = 1
                _x_12903 = d_371 + 1
                _x_12904 = algorithms_is_prime_check(n_370, _x_12903, fuel__374)
                return _x_12904
    _alt_12912 = _f_12911
    if fuel_372 == 0:
        _x_12914 = _alt_12877()
        return _x_12914
    else:
        n_12915 = fuel_372 - 1
        _x_12916 = _alt_12912(n_12915)
        return _x_12916

# Lean: Corpus.Algorithms.binarySearch.go
def binary_search_go(arr_375: list[int], target: int, lo: int, hi: int, fuel_376: int) -> int | None:
    def _f_12920():
        _x_12919 = None
        return _x_12919
    _alt_12921 = _f_12920
    def _f_12976(fuel__378: int):
        _x_12922 = hi <= lo
        if _x_12922:
            _x_12974 = None
            return _x_12974
        else:
            _x_12933 = hi - lo
            _x_12934 = 2
            _x_12937 = _x_12933 // 2
            _x_12938 = lo + _x_12937
            _alt_12939 = _f_12920
            def _f_12959(v_379: int):
                _x_12942 = v_379 == target
                _x_12943 = True
                if _x_12942:
                    _x_12957 = _x_12938
                    return _x_12957
                else:
                    _x_12946 = v_379 < target
                    if _x_12946:
                        _x_12950 = 1
                        _x_12953 = _x_12938 + 1
                        _x_12954 = binary_search_go(arr_375, target, _x_12953, hi, fuel__378)
                        return _x_12954
                    else:
                        _x_12948 = binary_search_go(arr_375, target, lo, _x_12938, fuel__378)
                        return _x_12948
            _alt_12960 = _f_12959
            def _f_12964(xs_380: list[int], i_381: int):
                _x_12962 = len(xs_380)
                _x_12963 = i_381 < _x_12962
                return _x_12963
            _x_12966 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_12967 = _x_12966(arr_375, _x_12938)
            if _x_12967 is None:
                _x_12969 = _alt_12939()
                return _x_12969
            else:
                val_12970 = _x_12967
                _x_12971 = _alt_12960(val_12970)
                return _x_12971
    _alt_12977 = _f_12976
    if fuel_376 == 0:
        _x_12979 = _alt_12921()
        return _x_12979
    else:
        n_12980 = fuel_376 - 1
        _x_12981 = _alt_12977(n_12980)
        return _x_12981

# Lean: Corpus.Algorithms.linearSearch.go
def linear_search_go(target_382: int, xs_383: list[int], idx_384: int) -> int | None:
    def _f_12985():
        _x_12984 = None
        return _x_12984
    _alt_12986 = _f_12985
    def _f_13004(x_386: int, xs__387: list[int]):
        _x_12989 = x_386 == target_382
        _x_12990 = True
        if _x_12989:
            _x_13002 = idx_384
            return _x_13002
        else:
            _x_12996 = 1
            _x_12999 = idx_384 + 1
            _x_13000 = linear_search_go(target_382, xs__387, _x_12999)
            return _x_13000
    _alt_13005 = _f_13004
    if len(xs_383) == 0:
        _x_13007 = _alt_12986()
        return _x_13007
    else:
        head_13008 = xs_383[0]
        tail_13009 = xs_383[1:]
        _x_13010 = _alt_13005(head_13008, tail_13009)
        return _x_13010

# Lean: Corpus.Algorithms.insertionSort.insert
def insertion_sort_insert(x_388: int, sorted_389: list[int]) -> list[int]:
    def _f_13015():
        _x_13013 = []
        _x_13014 = [x_388] + _x_13013
        return _x_13014
    _alt_13016 = _f_13015
    def _f_13025(y_391: int, ys: list[int]):
        _x_13017 = x_388 <= y_391
        if _x_13017:
            _x_13022 = [y_391] + ys
            _x_13023 = [x_388] + _x_13022
            return _x_13023
        else:
            _x_13019 = insertion_sort_insert(x_388, ys)
            _x_13020 = [y_391] + _x_13019
            return _x_13020
    _alt_13026 = _f_13025
    if len(sorted_389) == 0:
        _x_13028 = _alt_13016()
        return _x_13028
    else:
        head_13029 = sorted_389[0]
        tail_13030 = sorted_389[1:]
        _x_13031 = _alt_13026(head_13029, tail_13030)
        return _x_13031

# Lean: Corpus.Algorithms.insertionSort.sort
def insertion_sort_sort(unsorted: list[int], acc_392: list[int]) -> list[int]:
    def _f_13034():
        return acc_392
    _alt_13035 = _f_13034
    def _f_13038(x_394: int, xs_395: list[int]):
        _x_13036 = insertion_sort_insert(x_394, acc_392)
        _x_13037 = insertion_sort_sort(xs_395, _x_13036)
        return _x_13037
    _alt_13039 = _f_13038
    if len(unsorted) == 0:
        _x_13041 = _alt_13035()
        return _x_13041
    else:
        head_13042 = unsorted[0]
        tail_13043 = unsorted[1:]
        _x_13044 = _alt_13039(head_13042, tail_13043)
        return _x_13044

# Lean: Corpus.Algorithms.insertionSort
def insertion_sort(xs_396: list[int]) -> list[int]:
    _x_13047 = []
    _x_13048 = insertion_sort_sort(xs_396, _x_13047)
    return _x_13048

# Lean: Corpus.Algorithms.merge
def algorithms_merge(xs_397: list[int], ys_398: list[int]) -> list[int]:
    def _f_13050(ys_399: list[int]):
        return ys_399
    _alt_13051 = _f_13050
    _alt_13052 = _f_13050
    def _f_13063(x_400: int, xs__401: list[int], y_402: int, ys_: list[int]):
        _x_13053 = x_400 <= y_402
        if _x_13053:
            _x_13059 = [y_402] + ys_
            _x_13060 = algorithms_merge(xs__401, _x_13059)
            _x_13061 = [x_400] + _x_13060
            return _x_13061
        else:
            _x_13055 = [x_400] + xs__401
            _x_13056 = algorithms_merge(_x_13055, ys_)
            _x_13057 = [y_402] + _x_13056
            return _x_13057
    _alt_13064 = _f_13063
    if len(xs_397) == 0:
        if len(ys_398) == 0:
            _x_13065 = []
            _x_13066 = _alt_13051(_x_13065)
            return _x_13066
        else:
            head_13067 = ys_398[0]
            tail_13068 = ys_398[1:]
            _x_13069 = [head_13067] + tail_13068
            _x_13070 = _alt_13051(_x_13069)
            return _x_13070
    else:
        head_13072 = xs_397[0]
        tail_13073 = xs_397[1:]
        if len(ys_398) == 0:
            _x_13074 = [head_13072] + tail_13073
            _x_13075 = _alt_13052(_x_13074)
            return _x_13075
        else:
            head_13076 = ys_398[0]
            tail_13077 = ys_398[1:]
            _x_13078 = _alt_13064(head_13072, tail_13073, head_13076, tail_13077)
            return _x_13078

# Lean: Corpus.Algorithms.split
def algorithms_split(xs_403: list[int]) -> tuple[list[int], list[int]]:
    def _f_13084():
        _x_13082 = []
        _x_13083 = (_x_13082, _x_13082)
        return _x_13083
    _alt_13085 = _f_13084
    def _f_13089(x_405: int):
        _x_13086 = []
        _x_13087 = [x_405] + _x_13086
        _x_13088 = (_x_13087, _x_13086)
        return _x_13088
    _alt_13090 = _f_13089
    def _f_13101(x_406: int, y_407: int, rest_408: list[int]):
        def _f_13094(l_409: list[int], r_410: list[int]):
            _x_13091 = [x_406] + l_409
            _x_13092 = [y_407] + r_410
            _x_13093 = (_x_13091, _x_13092)
            return _x_13093
        _alt_13095 = _f_13094
        _x_13096 = algorithms_split(rest_408)
        match _x_13096:
            case (fst_13097, snd_13098):
                _x_13099 = _alt_13095(fst_13097, snd_13098)
                return _x_13099
    _alt_13102 = _f_13101
    if len(xs_403) == 0:
        _x_13104 = _alt_13085()
        return _x_13104
    else:
        head_13105 = xs_403[0]
        tail_13106 = xs_403[1:]
        if len(tail_13106) == 0:
            _x_13107 = _alt_13090(head_13105)
            return _x_13107
        else:
            head_13108 = tail_13106[0]
            tail_13109 = tail_13106[1:]
            _x_13110 = _alt_13102(head_13105, head_13108, tail_13109)
            return _x_13110

# Lean: Corpus.Algorithms.mergeSort
def merge_sort(xs_411: list[int]) -> list[int]:
    def _f_13115():
        _x_13114 = []
        return _x_13114
    _alt_13116 = _f_13115
    def _f_13119(x_413: int):
        _x_13117 = []
        _x_13118 = [x_413] + _x_13117
        return _x_13118
    _alt_13120 = _f_13119
    def _f_13132(x_13121: list[int]):
        def _f_13125(l_414: list[int], r_415: list[int]):
            _x_13122 = merge_sort(l_414)
            _x_13123 = merge_sort(r_415)
            _x_13124 = algorithms_merge(_x_13122, _x_13123)
            return _x_13124
        _alt_13126 = _f_13125
        _x_13127 = algorithms_split(xs_411)
        match _x_13127:
            case (fst_13128, snd_13129):
                _x_13130 = _alt_13126(fst_13128, snd_13129)
                return _x_13130
    _alt_13133 = _f_13132
    if len(xs_411) == 0:
        _x_13135 = _alt_13116()
        return _x_13135
    else:
        head_13136 = xs_411[0]
        tail_13137 = xs_411[1:]
        if len(tail_13137) == 0:
            _x_13138 = _alt_13120(head_13136)
            return _x_13138
        else:
            head_13139 = tail_13137[0]
            tail_13140 = tail_13137[1:]
            _x_13141 = [head_13139] + tail_13140
            _x_13142 = [head_13136] + _x_13141
            _x_13143 = _alt_13133(_x_13142)
            return _x_13143

# Lean: Corpus.Algorithms.linearSearch
def linear_search(xs_416: list[int], target_417: int) -> int | None:
    _x_13147 = 0
    _x_13150 = linear_search_go(target_417, xs_416, 0)
    return _x_13150

# Lean: Corpus.Algorithms.binarySearch
def binary_search(arr_418: list[int], target_419: int) -> int | None:
    _x_13152 = 0
    _x_13155 = len(arr_418)
    _x_13156 = binary_search_go(arr_418, target_419, 0, _x_13155, _x_13155)
    return _x_13156

# Lean: Corpus.Algorithms.gcd
def algorithms_gcd(a_420: int, b_421: int) -> int:
    _x_13160 = 0
    _x_13163 = b_421 == 0
    _x_13164 = True
    if _x_13163:
        return a_420
    else:
        _x_13170 = a_420 % b_421
        _x_13171 = algorithms_gcd(b_421, _x_13170)
        return _x_13171

# Lean: Corpus.Algorithms.lcm
def algorithms_lcm(a_422: int, b_423: int) -> int:
    def _f_13176():
        _x_13175 = True
        return True
    _alt_13177 = _f_13176
    def _f_13184():
        _x_13180 = 0
        _x_13183 = b_423 == 0
        return _x_13183
    _alt_13185 = _f_13184
    _x_13188 = 0
    _x_13191 = a_422 == 0
    def _jp_13211(_y_13196: bool):
        _x_13197 = True
        if _y_13196:
            return 0
        else:
            _x_13206 = algorithms_gcd(a_422, b_423)
            _x_13207 = a_422 // _x_13206
            _x_13208 = _x_13207 * b_423
            return _x_13208
    def _jp_13217():
        _x_13216 = _alt_13177()
        return _jp_13211(_x_13216)
    def _jp_13214():
        _x_13213 = _alt_13185()
        return _jp_13211(_x_13213)
    if _x_13191:
        return _jp_13217()
    else:
        return _jp_13214()

# Lean: Corpus.Algorithms.isPrime
def algorithms_is_prime(n_426: int) -> bool:
    _x_13219 = 2
    _x_13222 = n_426 < 2
    if _x_13222:
        _x_13226 = False
        return False
    else:
        _x_13224 = algorithms_is_prime_check(n_426, 2, n_426)
        return _x_13224

# Lean: Corpus.Algorithms.primeFactors
def algorithms_prime_factors(n_427: int) -> list[int]:
    _x_13229 = 2
    _x_13232 = []
    _x_13233 = algorithms_prime_factors_go(n_427, 2, _x_13232, n_427)
    return _x_13233

# Lean: Corpus.Algorithms.fibonacci
def algorithms_fibonacci(n_428: int) -> int:
    _x_13235 = 0
    _x_13238 = 1
    _x_13241 = algorithms_fibonacci_go(0, 1, n_428)
    return _x_13241

# Lean: Corpus.Algorithms.power
def power(base_429: int, exp_430: int) -> int:
    _x_13243 = 1
    _x_13246 = power_go(base_429, exp_430, 1)
    return _x_13246

# Lean: Corpus.Algorithms.reverse
def algorithms_reverse(__431: Any, xs_432: list[Any]) -> list[Any]:
    _x_13248 = []
    _x_13249 = algorithms_reverse_go(None, xs_432, _x_13248)
    return _x_13249

# Lean: Corpus.Algorithms.take
def algorithms_take(__433: Any, n_434: int, xs_435: list[Any]) -> list[Any]:
    def _f_13253(x_13251: list[Any]):
        _x_13252 = []
        return _x_13252
    _alt_13254 = _f_13253
    def _f_13257(x_13255: int):
        _x_13256 = []
        return _x_13256
    _alt_13258 = _f_13257
    def _f_13261(n__436: int, x_437: Any, xs__438: list[Any]):
        _x_13259 = algorithms_take(None, n__436, xs__438)
        _x_13260 = [x_437] + _x_13259
        return _x_13260
    _alt_13262 = _f_13261
    if n_434 == 0:
        if len(xs_435) == 0:
            _x_13263 = []
            _x_13264 = _alt_13254(_x_13263)
            return _x_13264
        else:
            head_13265 = xs_435[0]
            tail_13266 = xs_435[1:]
            _x_13267 = [head_13265] + tail_13266
            _x_13268 = _alt_13254(_x_13267)
            return _x_13268
    else:
        n_13270 = n_434 - 1
        if len(xs_435) == 0:
            _x_13271 = n_13270 + 1
            _x_13272 = _alt_13258(_x_13271)
            return _x_13272
        else:
            head_13273 = xs_435[0]
            tail_13274 = xs_435[1:]
            _x_13275 = _alt_13262(n_13270, head_13273, tail_13274)
            return _x_13275

# Lean: Corpus.Algorithms.drop
def algorithms_drop(__439: Any, n_440: int, xs_441: list[Any]) -> list[Any]:
    def _f_13279(xs_442: list[Any]):
        return xs_442
    _alt_13280 = _f_13279
    def _f_13283(x_13281: int):
        _x_13282 = []
        return _x_13282
    _alt_13284 = _f_13283
    def _f_13287(n__443: int, head_13285: Any, xs__444: list[Any]):
        _x_13286 = algorithms_drop(None, n__443, xs__444)
        return _x_13286
    _alt_13288 = _f_13287
    if n_440 == 0:
        if len(xs_441) == 0:
            _x_13289 = []
            _x_13290 = _alt_13280(_x_13289)
            return _x_13290
        else:
            head_13291 = xs_441[0]
            tail_13292 = xs_441[1:]
            _x_13293 = [head_13291] + tail_13292
            _x_13294 = _alt_13280(_x_13293)
            return _x_13294
    else:
        n_13296 = n_440 - 1
        if len(xs_441) == 0:
            _x_13297 = n_13296 + 1
            _x_13298 = _alt_13284(_x_13297)
            return _x_13298
        else:
            head_13299 = xs_441[0]
            tail_13300 = xs_441[1:]
            _x_13301 = _alt_13288(n_13296, head_13299, tail_13300)
            return _x_13301

# Lean: Corpus.Algorithms.filter
def algorithms_filter(__445: Any, p_446: Callable[[Any], bool], xs_447: list[Any]) -> list[Any]:
    def _f_13306():
        _x_13305 = []
        return _x_13305
    _alt_13307 = _f_13306
    def _f_13317(x_449: Any, xs__450: list[Any]):
        _x_13308 = p_446(x_449)
        _x_13309 = True
        if _x_13308:
            _x_13314 = algorithms_filter(None, p_446, xs__450)
            _x_13315 = [x_449] + _x_13314
            return _x_13315
        else:
            _x_13312 = algorithms_filter(None, p_446, xs__450)
            return _x_13312
    _alt_13318 = _f_13317
    if len(xs_447) == 0:
        _x_13320 = _alt_13307()
        return _x_13320
    else:
        head_13321 = xs_447[0]
        tail_13322 = xs_447[1:]
        _x_13323 = _alt_13318(head_13321, tail_13322)
        return _x_13323

# Lean: Corpus.Algorithms.map
def algorithms_map(__451: Any, __452: Any, f: Callable[[Any], Any], xs_453: list[Any]) -> list[Any]:
    def _f_13327():
        _x_13326 = []
        return _x_13326
    _alt_13328 = _f_13327
    def _f_13332(x_455: Any, xs__456: list[Any]):
        _x_13329 = f(x_455)
        _x_13330 = algorithms_map(None, None, f, xs__456)
        _x_13331 = [_x_13329] + _x_13330
        return _x_13331
    _alt_13333 = _f_13332
    if len(xs_453) == 0:
        _x_13335 = _alt_13328()
        return _x_13335
    else:
        head_13336 = xs_453[0]
        tail_13337 = xs_453[1:]
        _x_13338 = _alt_13333(head_13336, tail_13337)
        return _x_13338

# Lean: Corpus.Algorithms.foldl
def algorithms_foldl(__457: Any, __458: Any, f_459: Callable[[Any, Any], Any], init: Any, xs_460: list[Any]) -> Any:
    def _f_13341():
        return init
    _alt_13342 = _f_13341
    def _f_13345(x_462: Any, xs__463: list[Any]):
        _x_13343 = f_459(init, x_462)
        _x_13344 = algorithms_foldl(None, None, f_459, _x_13343, xs__463)
        return _x_13344
    _alt_13346 = _f_13345
    if len(xs_460) == 0:
        _x_13348 = _alt_13342()
        return _x_13348
    else:
        head_13349 = xs_460[0]
        tail_13350 = xs_460[1:]
        _x_13351 = _alt_13346(head_13349, tail_13350)
        return _x_13351

# Lean: Corpus.Algorithms.foldr
def algorithms_foldr(__464: Any, __465: Any, f_466: Callable[[Any, Any], Any], init_467: Any, xs_468: list[Any]) -> Any:
    def _f_13354():
        return init_467
    _alt_13355 = _f_13354
    def _f_13358(x_470: Any, xs__471: list[Any]):
        _x_13356 = algorithms_foldr(None, None, f_466, init_467, xs__471)
        _x_13357 = f_466(x_470, _x_13356)
        return _x_13357
    _alt_13359 = _f_13358
    if len(xs_468) == 0:
        _x_13361 = _alt_13355()
        return _x_13361
    else:
        head_13362 = xs_468[0]
        tail_13363 = xs_468[1:]
        _x_13364 = _alt_13359(head_13362, tail_13363)
        return _x_13364

# Lean: Corpus.Algorithms.zip
def algorithms_zip(__472: Any, __473: Any, xs_474: list[Any], ys_475: list[Any]) -> list[tuple[Any, Any]]:
    def _f_13369(x_13367: list[Any]):
        _x_13368 = []
        return _x_13368
    _alt_13370 = _f_13369
    def _f_13373(x_13371: list[Any]):
        _x_13372 = []
        return _x_13372
    _alt_13374 = _f_13373
    def _f_13378(x_476: Any, xs__477: list[Any], y_478: Any, ys__479: list[Any]):
        _x_13375 = (x_476, y_478)
        _x_13376 = algorithms_zip(None, None, xs__477, ys__479)
        _x_13377 = [_x_13375] + _x_13376
        return _x_13377
    _alt_13379 = _f_13378
    if len(xs_474) == 0:
        if len(ys_475) == 0:
            _x_13380 = []
            _x_13381 = _alt_13370(_x_13380)
            return _x_13381
        else:
            head_13382 = ys_475[0]
            tail_13383 = ys_475[1:]
            _x_13384 = [head_13382] + tail_13383
            _x_13385 = _alt_13370(_x_13384)
            return _x_13385
    else:
        head_13387 = xs_474[0]
        tail_13388 = xs_474[1:]
        if len(ys_475) == 0:
            _x_13389 = [head_13387] + tail_13388
            _x_13390 = _alt_13374(_x_13389)
            return _x_13390
        else:
            head_13391 = ys_475[0]
            tail_13392 = ys_475[1:]
            _x_13393 = _alt_13379(head_13387, tail_13388, head_13391, tail_13392)
            return _x_13393

# Lean: Corpus.Algorithms.unzip
def unzip(__480: Any, __481: Any, xys: list[tuple[Any, Any]]) -> tuple[list[Any], list[Any]]:
    def _f_13400():
        _x_13397 = []
        _x_13398 = []
        _x_13399 = (_x_13397, _x_13398)
        return _x_13399
    _alt_13401 = _f_13400
    def _f_13412(x_483: Any, y_484: Any, rest_485: list[tuple[Any, Any]]):
        def _f_13405(xs_486: list[Any], ys_487: list[Any]):
            _x_13402 = [x_483] + xs_486
            _x_13403 = [y_484] + ys_487
            _x_13404 = (_x_13402, _x_13403)
            return _x_13404
        _alt_13406 = _f_13405
        _x_13407 = unzip(None, None, rest_485)
        match _x_13407:
            case (fst_13408, snd_13409):
                _x_13410 = _alt_13406(fst_13408, snd_13409)
                return _x_13410
    _alt_13413 = _f_13412
    if len(xys) == 0:
        _x_13415 = _alt_13401()
        return _x_13415
    else:
        head_13416 = xys[0]
        tail_13417 = xys[1:]
        match head_13416:
            case (fst_13418, snd_13419):
                _x_13420 = _alt_13413(fst_13418, snd_13419, tail_13417)
                return _x_13420

# Lean: Corpus.Algorithms.concat
def algorithms_concat(__488: Any, xss: list[list[Any]]) -> list[Any]:
    def _f_13425():
        _x_13424 = []
        return _x_13424
    _alt_13426 = _f_13425
    def _f_13432(xs_490: list[Any], xss_: list[list[Any]]):
        _x_13430 = algorithms_concat(None, xss_)
        _x_13431 = xs_490 + _x_13430
        return _x_13431
    _alt_13433 = _f_13432
    if len(xss) == 0:
        _x_13435 = _alt_13426()
        return _x_13435
    else:
        head_13436 = xss[0]
        tail_13437 = xss[1:]
        _x_13438 = _alt_13433(head_13436, tail_13437)
        return _x_13438

# Lean: Corpus.Algorithms.intersperse
def intersperse(__491: Any, sep_492: Any, xs_493: list[Any]) -> list[Any]:
    def _f_13442():
        _x_13441 = []
        return _x_13441
    _alt_13443 = _f_13442
    def _f_13446(x_495: Any):
        _x_13444 = []
        _x_13445 = [x_495] + _x_13444
        return _x_13445
    _alt_13447 = _f_13446
    def _f_13451(x_496: Any, xs__497: list[Any]):
        _x_13448 = intersperse(None, sep_492, xs__497)
        _x_13449 = [sep_492] + _x_13448
        _x_13450 = [x_496] + _x_13449
        return _x_13450
    _alt_13452 = _f_13451
    if len(xs_493) == 0:
        _x_13454 = _alt_13443()
        return _x_13454
    else:
        head_13455 = xs_493[0]
        tail_13456 = xs_493[1:]
        if len(tail_13456) == 0:
            _x_13457 = _alt_13447(head_13455)
            return _x_13457
        else:
            head_13458 = tail_13456[0]
            tail_13459 = tail_13456[1:]
            _x_13460 = [head_13458] + tail_13459
            _x_13461 = _alt_13452(head_13455, _x_13460)
            return _x_13461

# Lean: Corpus.Algorithms.span
def span(__498: Any, p_499: Callable[[Any], bool], xs_500: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_13467():
        _x_13465 = []
        _x_13466 = (_x_13465, _x_13465)
        return _x_13466
    _alt_13468 = _f_13467
    def _f_13486(x_502: Any, xs__503: list[Any]):
        _x_13469 = p_499(x_502)
        _x_13470 = True
        if _x_13469:
            def _f_13478(ys_504: list[Any], zs: list[Any]):
                _x_13476 = [x_502] + ys_504
                _x_13477 = (_x_13476, zs)
                return _x_13477
            _alt_13479 = _f_13478
            _x_13480 = span(None, p_499, xs__503)
            match _x_13480:
                case (fst_13481, snd_13482):
                    _x_13483 = _alt_13479(fst_13481, snd_13482)
                    return _x_13483
        else:
            _x_13473 = []
            _x_13474 = (_x_13473, xs_500)
            return _x_13474
    _alt_13487 = _f_13486
    if len(xs_500) == 0:
        _x_13489 = _alt_13468()
        return _x_13489
    else:
        head_13490 = xs_500[0]
        tail_13491 = xs_500[1:]
        _x_13492 = _alt_13487(head_13490, tail_13491)
        return _x_13492

# Lean: Corpus.Algorithms.partition
def partition(__505: Any, p_506: Callable[[Any], bool], xs_507: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_13497():
        _x_13495 = []
        _x_13496 = (_x_13495, _x_13495)
        return _x_13496
    _alt_13498 = _f_13497
    def _f_13516(x_509: Any, xs__510: list[Any]):
        def _f_13509(yes: list[Any], no: list[Any]):
            _x_13499 = p_506(x_509)
            _x_13500 = True
            if _x_13499:
                _x_13506 = [x_509] + yes
                _x_13507 = (_x_13506, no)
                return _x_13507
            else:
                _x_13503 = [x_509] + no
                _x_13504 = (yes, _x_13503)
                return _x_13504
        _alt_13510 = _f_13509
        _x_13511 = partition(None, p_506, xs__510)
        match _x_13511:
            case (fst_13512, snd_13513):
                _x_13514 = _alt_13510(fst_13512, snd_13513)
                return _x_13514
    _alt_13517 = _f_13516
    if len(xs_507) == 0:
        _x_13519 = _alt_13498()
        return _x_13519
    else:
        head_13520 = xs_507[0]
        tail_13521 = xs_507[1:]
        _x_13522 = _alt_13517(head_13520, tail_13521)
        return _x_13522

# Lean: Corpus.Algorithms.groupBy
def group_by(__511: Any, eq: Callable[[Any, Any], bool], xs_512: list[Any]) -> list[list[Any]]:
    def _f_13526():
        _x_13525 = []
        return _x_13525
    _alt_13527 = _f_13526
    def _f_13539(x_514: Any, xs__515: list[Any]):
        def _f_13531(same: list[Any], rest_516: list[Any]):
            _x_13528 = [x_514] + same
            _x_13529 = group_by(None, eq, rest_516)
            _x_13530 = [_x_13528] + _x_13529
            return _x_13530
        _alt_13532 = _f_13531
        _x_13533 = eq(x_514)
        _x_13534 = span(None, _x_13533, xs__515)
        match _x_13534:
            case (fst_13535, snd_13536):
                _x_13537 = _alt_13532(fst_13535, snd_13536)
                return _x_13537
    _alt_13540 = _f_13539
    if len(xs_512) == 0:
        _x_13542 = _alt_13527()
        return _x_13542
    else:
        head_13543 = xs_512[0]
        tail_13544 = xs_512[1:]
        _x_13545 = _alt_13540(head_13543, tail_13544)
        return _x_13545

# Lean: Corpus.Algorithms.isPalindrome
def algorithms_is_palindrome(s_517: str) -> bool:
    _x_13548 = list(s_517)
    _x_13553 = list(reversed(_x_13548))
    _x_13554 = _x_13548 == _x_13553
    return _x_13554

# Lean: Corpus.Algorithms.countChar
def algorithms_count_char(c_519: str, s_520: str) -> int:
    def _f_13572(acc_521: int, x_522: str):
        _x_13559 = x_522 == c_519
        _x_13560 = True
        if _x_13559:
            _x_13567 = 1
            _x_13570 = acc_521 + 1
            return _x_13570
        else:
            return acc_521
    _x_13573 = 0
    _x_13576 = list(s_520)
    _x_13577 = functools.reduce(_f_13572, _x_13576, 0)
    return _x_13577

# Lean: Corpus.Algorithms.replaceChar
def replace_char(old: str, new: str, s_523: str) -> str:
    def _f_13588(c_524: str):
        _x_13582 = c_524 == old
        _x_13583 = True
        if _x_13582:
            return new
        else:
            return c_524
    _x_13589 = list(s_523)
    _x_13590 = [_f_13588(x) for x in _x_13589]
    _x_13591 = ''.join(_x_13590)
    return _x_13591

# Lean: Corpus.Math.abs
def math_abs(x_525: int) -> int:
    _x_13593 = 0
    _x_13596 = x_525 < 0
    if _x_13596:
        _x_13601 = -x_525
        return _x_13601
    else:
        return x_525

# Lean: Corpus.Math.sign
def sign(x_526: int) -> int:
    _x_13604 = 0
    _x_13607 = x_526 < 0
    if _x_13607:
        _x_13619 = 1
        _x_13622 = -1
        return _x_13622
    else:
        _x_13609 = 0 < x_526
        if _x_13609:
            _x_13612 = 1
            return 1
        else:
            return 0

# Lean: Corpus.Math.min
def math_min(a_527: int, b_528: int) -> int:
    _x_13625 = a_527 <= b_528
    if _x_13625:
        return a_527
    else:
        return b_528

# Lean: Corpus.Math.max
def math_max(a_529: int, b_530: int) -> int:
    _x_13630 = b_530 <= a_529
    if _x_13630:
        return a_529
    else:
        return b_530

# Lean: Corpus.Math.clamp
def clamp(lo_531: int, hi_532: int, x_533: int) -> int:
    _x_13635 = math_max(lo_531, x_533)
    _x_13636 = math_min(hi_532, _x_13635)
    return _x_13636

# Lean: Corpus.Math.divMod
def div_mod(a_534: int, b_535: int) -> tuple[int, int]:
    _x_13641 = a_534 // b_535
    _x_13645 = a_534 % b_535
    _x_13646 = (_x_13641, _x_13645)
    return _x_13646

# Lean: Corpus.Math.pow
def pow(base_536: int, exp_537: int) -> int:
    def _f_13651():
        _x_13648 = 1
        return 1
    _alt_13652 = _f_13651
    def _f_13658(n_539: int):
        _x_13656 = pow(base_536, n_539)
        _x_13657 = base_536 * _x_13656
        return _x_13657
    _alt_13659 = _f_13658
    if exp_537 == 0:
        _x_13661 = _alt_13652()
        return _x_13661
    else:
        n_13662 = exp_537 - 1
        _x_13663 = _alt_13659(n_13662)
        return _x_13663

# Lean: Corpus.Math.fastPow
def fast_pow(base_540: int, exp_541: int) -> int:
    _x_13666 = 1
    _x_13669 = fast_pow_go(base_540, exp_541, 1)
    return _x_13669

# Lean: Corpus.Math.modPow
def mod_pow(base_542: int, exp_543: int, m_544: int) -> int:
    _x_13674 = base_542 % m_544
    _x_13675 = 1
    _x_13678 = mod_pow_go(m_544, _x_13674, exp_543, 1)
    return _x_13678

# Lean: Corpus.Math.gcd
def math_gcd(a_545: int, b_546: int) -> int:
    _x_13682 = 0
    _x_13685 = b_546 == 0
    _x_13686 = True
    if _x_13685:
        return a_545
    else:
        _x_13692 = a_545 % b_546
        _x_13693 = math_gcd(b_546, _x_13692)
        return _x_13693

# Lean: Corpus.Math.lcm
def math_lcm(a_547: int, b_548: int) -> int:
    def _f_13698():
        _x_13697 = True
        return True
    _alt_13699 = _f_13698
    def _f_13706():
        _x_13702 = 0
        _x_13705 = b_548 == 0
        return _x_13705
    _alt_13707 = _f_13706
    _x_13710 = 0
    _x_13713 = a_547 == 0
    def _jp_13733(_y_13718: bool):
        _x_13719 = True
        if _y_13718:
            return 0
        else:
            _x_13728 = math_gcd(a_547, b_548)
            _x_13729 = a_547 // _x_13728
            _x_13730 = _x_13729 * b_548
            return _x_13730
    def _jp_13739():
        _x_13738 = _alt_13699()
        return _jp_13733(_x_13738)
    def _jp_13736():
        _x_13735 = _alt_13707()
        return _jp_13733(_x_13735)
    if _x_13713:
        return _jp_13739()
    else:
        return _jp_13736()

# Lean: Corpus.Math.coprime
def coprime(a_551: int, b_552: int) -> bool:
    _x_13743 = math_gcd(a_551, b_552)
    _x_13744 = 1
    _x_13747 = _x_13743 == 1
    return _x_13747

# Lean: Corpus.Math.isPrime
def math_is_prime(n_553: int) -> bool:
    _x_13749 = 2
    _x_13752 = n_553 < 2
    if _x_13752:
        _x_13756 = False
        return False
    else:
        _x_13754 = math_is_prime_check(n_553, 2, n_553)
        return _x_13754

# Lean: Corpus.Math.primeFactors
def math_prime_factors(n_554: int) -> list[int]:
    _x_13759 = 2
    _x_13762 = []
    _x_13763 = math_prime_factors_go(n_554, 2, _x_13762, n_554)
    return _x_13763

# Lean: Corpus.Math.divisors
def divisors(n_555: int) -> list[int]:
    _x_13765 = 1
    _x_13768 = []
    _x_13769 = divisors_go(n_555, 1, _x_13768)
    _x_13770 = list(reversed(_x_13769))
    return _x_13770

# Lean: Corpus.Math.numDivisors
def num_divisors(n_556: int) -> int:
    _x_13772 = divisors(n_556)
    _x_13773 = len(_x_13772)
    return _x_13773

# Lean: Corpus.Math.sumDivisors
def sum_divisors(n_557: int) -> int:
    def _f_13781(x1_13775: int, x2_13776: int):
        _x_13780 = x1_13775 + x2_13776
        return _x_13780
    _x_13782 = 0
    _x_13785 = divisors(n_557)
    _x_13786 = functools.reduce(_f_13781, _x_13785, 0)
    return _x_13786

# Lean: Corpus.Math.fibonacci
def math_fibonacci(n_558: int) -> int:
    _x_13788 = 0
    _x_13791 = 1
    _x_13794 = math_fibonacci_go(0, 1, n_558)
    return _x_13794

# Lean: Corpus.Math.lucas
def lucas(n_559: int) -> int:
    _x_13796 = 2
    _x_13799 = 1
    _x_13802 = lucas_go(2, 1, n_559)
    return _x_13802

# Lean: Corpus.Math.tribonacci
def tribonacci(n_560: int) -> int:
    _x_13804 = 0
    _x_13807 = 1
    _x_13810 = tribonacci_go(0, 0, 1, n_560)
    return _x_13810

# Lean: Corpus.Math.factorial
def factorial(n_561: int) -> int:
    def _f_13815():
        _x_13812 = 1
        return 1
    _alt_13816 = _f_13815
    def _f_13829(n__563: int):
        _x_13823 = 1
        _x_13826 = n__563 + 1
        _x_13827 = factorial(n__563)
        _x_13828 = _x_13826 * _x_13827
        return _x_13828
    _alt_13830 = _f_13829
    if n_561 == 0:
        _x_13832 = _alt_13816()
        return _x_13832
    else:
        n_13833 = n_561 - 1
        _x_13834 = _alt_13830(n_13833)
        return _x_13834

# Lean: Corpus.Math.binomial
def binomial(n_564: int, k_565: int) -> int:
    _x_13837 = n_564 < k_565
    if _x_13837:
        _x_13844 = 0
        return 0
    else:
        _x_13839 = 1
        _x_13842 = binomial_go(n_564, k_565, 1, 1, 1)
        return _x_13842

# Lean: Corpus.Math.catalan
def catalan(n_566: int) -> int:
    _x_13855 = 2
    _x_13858 = 2 * n_566
    _x_13859 = binomial(_x_13858, n_566)
    _x_13863 = 1
    _x_13866 = n_566 + 1
    _x_13867 = _x_13859 // _x_13866
    return _x_13867

# Lean: Corpus.Math.permutations
def permutations(n_567: int, k_568: int) -> int:
    _x_13869 = n_567 < k_568
    if _x_13869:
        _x_13882 = 0
        return 0
    else:
        _x_13874 = factorial(n_567)
        _x_13878 = n_567 - k_568
        _x_13879 = factorial(_x_13878)
        _x_13880 = _x_13874 // _x_13879
        return _x_13880

# Lean: Corpus.Math.triangularNumber
def triangular_number(n_569: int) -> int:
    _x_13896 = 1
    _x_13899 = n_569 + 1
    _x_13900 = n_569 * _x_13899
    _x_13901 = 2
    _x_13904 = _x_13900 // 2
    return _x_13904

# Lean: Corpus.Math.squareNumber
def square_number(n_570: int) -> int:
    _x_13909 = n_570 * n_570
    return _x_13909

# Lean: Corpus.Math.pentagonalNumber
def pentagonal_number(n_571: int) -> int:
    _x_13920 = 3
    _x_13923 = 3 * n_571
    _x_13924 = 1
    _x_13927 = _x_13923 - 1
    _x_13928 = n_571 * _x_13927
    _x_13929 = 2
    _x_13932 = _x_13928 // 2
    return _x_13932

# Lean: Corpus.Math.hexagonalNumber
def hexagonal_number(n_572: int) -> int:
    _x_13940 = 2
    _x_13943 = 2 * n_572
    _x_13944 = 1
    _x_13947 = _x_13943 - 1
    _x_13948 = n_572 * _x_13947
    return _x_13948

# Lean: Corpus.Math.isTriangular
def is_triangular(n_573: int) -> bool:
    _x_13962 = 8
    _x_13965 = 8 * n_573
    _x_13966 = 1
    _x_13969 = _x_13965 + 1
    _x_13970 = isqrt(_x_13969)
    _x_13971 = _x_13970 - 1
    _x_13972 = 2
    _x_13975 = _x_13971 // 2
    _x_13978 = _x_13975 + 1
    _x_13979 = _x_13975 * _x_13978
    _x_13980 = _x_13979 // 2
    _x_13981 = _x_13980 == n_573
    return _x_13981

# Lean: Corpus.Math.isSquare
def is_square(n_575: int) -> bool:
    _x_13983 = isqrt(n_575)
    _x_13989 = _x_13983 * _x_13983
    _x_13990 = _x_13989 == n_575
    return _x_13990

# Lean: Corpus.Math.isqrt
def isqrt(n_577: int) -> int:
    _x_13994 = 0
    _x_13997 = n_577 == 0
    _x_13998 = True
    if _x_13997:
        return 0
    else:
        _x_14001 = isqrt_go(n_577, n_577, n_577)
        return _x_14001

# Lean: Corpus.Math.digits
def digits(n_578: int, base_579: int) -> list[int]:
    _x_14005 = 2
    _x_14008 = base_579 < 2
    if _x_14008:
        _x_14013 = []
        return _x_14013
    else:
        _x_14010 = []
        _x_14011 = digits_go(base_579, n_578, _x_14010)
        return _x_14011

# Lean: Corpus.Math.fromDigits
def from_digits(ds: list[int], base_580: int) -> int:
    def _f_14024(acc_581: int, d_582: int):
        _x_14022 = acc_581 * base_580
        _x_14023 = _x_14022 + d_582
        return _x_14023
    _x_14025 = 0
    _x_14028 = functools.reduce(_f_14024, ds, 0)
    return _x_14028

# Lean: Corpus.Math.numDigits
def num_digits(n_583: int, base_584: int) -> int:
    _x_14030 = digits(n_583, base_584)
    _x_14031 = len(_x_14030)
    return _x_14031

# Lean: Corpus.Math.numDigits10
def num_digits10(n_585: int) -> int:
    _x_14033 = 10
    _x_14036 = num_digits(n_585, 10)
    return _x_14036

# Lean: Corpus.Math.digitSum
def digit_sum(n_586: int, base_587: int) -> int:
    def _f_14044(x1_14038: int, x2_14039: int):
        _x_14043 = x1_14038 + x2_14039
        return _x_14043
    _x_14045 = 0
    _x_14048 = digits(n_586, base_587)
    _x_14049 = functools.reduce(_f_14044, _x_14048, 0)
    return _x_14049

# Lean: Corpus.Math.digitSum10
def digit_sum10(n_588: int) -> int:
    _x_14051 = 10
    _x_14054 = digit_sum(n_588, 10)
    return _x_14054

# Lean: Corpus.Math.digitalRoot
def digital_root(n_589: int) -> int:
    _x_14056 = 100
    _x_14059 = digital_root_go(n_589, 100)
    return _x_14059

# Lean: Corpus.Math.reverseDigits
def reverse_digits(n_590: int) -> int:
    _x_14061 = 10
    _x_14064 = digits(n_590, 10)
    _x_14065 = list(reversed(_x_14064))
    _x_14066 = from_digits(_x_14065, 10)
    return _x_14066

# Lean: Corpus.Math.isPalindromeNum
def is_palindrome_num(n_591: int) -> bool:
    _x_14070 = reverse_digits(n_591)
    _x_14071 = n_591 == _x_14070
    return _x_14071

# Lean: Corpus.Math.isEven
def is_even(n_592: int) -> bool:
    _x_14078 = 2
    _x_14081 = n_592 % 2
    _x_14082 = 0
    _x_14085 = _x_14081 == 0
    return _x_14085

# Lean: Corpus.Math.isOdd
def is_odd(n_593: int) -> bool:
    _x_14092 = 2
    _x_14095 = n_593 % 2
    _x_14096 = 1
    _x_14099 = _x_14095 == 1
    return _x_14099

# Lean: Corpus.Functional.id
def functional_id(__594: Any, x_595: Any) -> Any:
    return x_595

# Lean: Corpus.Functional.const
def functional_const(__596: Any, __597: Any, x_598: Any, y_599: Any) -> Any:
    return x_598

# Lean: Corpus.Functional.flip
def functional_flip(__600: Any, __601: Any, __602: Any, f_603: Callable[[Any, Any], Any], y_604: Any, x_605: Any) -> Any:
    _x_14103 = f_603(x_605, y_604)
    return _x_14103

# Lean: Corpus.Functional.compose
def functional_compose(__606: Any, __607: Any, __608: Any, f_609: Callable[[Any], Any], g_610: Callable[[Any], Any], x_611: Any) -> Any:
    _x_14105 = g_610(x_611)
    _x_14106 = f_609(_x_14105)
    return _x_14106

# Lean: Corpus.Functional.pipe
def pipe(__612: Any, __613: Any, x_614: Any, f_615: Callable[[Any], Any]) -> Any:
    _x_14108 = f_615(x_614)
    return _x_14108

# Lean: Corpus.Functional.apply
def functional_apply(__616: Any, __617: Any, f_618: Callable[[Any], Any], x_619: Any) -> Any:
    _x_14110 = f_618(x_619)
    return _x_14110

# Lean: Corpus.Functional.curry
def curry(__620: Any, __621: Any, __622: Any, f_623: Callable[[tuple[Any, Any]], Any], x_624: Any, y_625: Any) -> Any:
    _x_14112 = (x_624, y_625)
    _x_14113 = f_623(_x_14112)
    return _x_14113

# Lean: Corpus.Functional.uncurry
def uncurry(__626: Any, __627: Any, __628: Any, f_629: Callable[[Any, Any], Any], p_630: tuple[Any, Any]) -> Any:
    _x_14115 = p_630[0]
    _x_14116 = p_630[1]
    _x_14117 = f_629(_x_14115, _x_14116)
    return _x_14117

# Lean: Corpus.Functional.Option.map
def option_map(__631: Any, __632: Any, f_633: Callable[[Any], Any], x_14119: Any | None) -> Any | None:
    def _f_14121():
        _x_14120 = None
        return _x_14120
    _alt_14122 = _f_14121
    def _f_14125(x_635: Any):
        _x_14123 = f_633(x_635)
        _x_14124 = _x_14123
        return _x_14124
    _alt_14126 = _f_14125
    if x_14119 is None:
        _x_14128 = _alt_14122()
        return _x_14128
    else:
        val_14129 = x_14119
        _x_14130 = _alt_14126(val_14129)
        return _x_14130

# Lean: Corpus.Functional.Option.bind
def option_bind(__636: Any, __637: Any, x_638: Any | None, f_639: Callable[[Any], Any | None]) -> Any | None:
    def _f_14134():
        _x_14133 = None
        return _x_14133
    _alt_14135 = _f_14134
    def _f_14137(a_641: Any):
        _x_14136 = f_639(a_641)
        return _x_14136
    _alt_14138 = _f_14137
    if x_638 is None:
        _x_14140 = _alt_14135()
        return _x_14140
    else:
        val_14141 = x_638
        _x_14142 = _alt_14138(val_14141)
        return _x_14142

# Lean: Corpus.Functional.Option.filter
def option_filter(__642: Any, p_643: Callable[[Any], bool], x_14145: Any | None) -> Any | None:
    def _f_14147():
        _x_14146 = None
        return _x_14146
    _alt_14148 = _f_14147
    def _f_14157(x_645: Any):
        _x_14149 = p_643(x_645)
        _x_14150 = True
        if _x_14149:
            _x_14155 = x_645
            return _x_14155
        else:
            _x_14153 = None
            return _x_14153
    _alt_14158 = _f_14157
    if x_14145 is None:
        _x_14160 = _alt_14148()
        return _x_14160
    else:
        val_14161 = x_14145
        _x_14162 = _alt_14158(val_14161)
        return _x_14162

# Lean: Corpus.Functional.Option.getOrElse
def get_or_else(__646: Any, x_647: Any | None, default: Any) -> Any:
    def _f_14165():
        return default
    _alt_14166 = _f_14165
    def _f_14167(a_649: Any):
        return a_649
    _alt_14168 = _f_14167
    if x_647 is None:
        _x_14170 = _alt_14166()
        return _x_14170
    else:
        val_14171 = x_647
        _x_14172 = _alt_14168(val_14171)
        return _x_14172

# Lean: Corpus.Functional.Option.orElse
def or_else(__650: Any, x_651: Any | None, y_652: Any | None) -> Any | None:
    def _f_14176(a_653: Any):
        _x_14175 = a_653
        return _x_14175
    _alt_14177 = _f_14176
    def _f_14178():
        return y_652
    _alt_14179 = _f_14178
    if x_651 is None:
        _x_14181 = _alt_14179()
        return _x_14181
    else:
        val_14182 = x_651
        _x_14183 = _alt_14177(val_14182)
        return _x_14183

# Lean: Corpus.Functional.Option.zip
def option_zip(__655: Any, __656: Any, x_657: Any | None, y_658: Any | None) -> tuple[Any, Any] | None:
    def _f_14188(a_659: Any, b_660: Any):
        _x_14186 = (a_659, b_660)
        _x_14187 = _x_14186
        return _x_14187
    _alt_14189 = _f_14188
    def _f_14193(x_14190: Any | None, x_14191: Any | None):
        _x_14192 = None
        return _x_14192
    _alt_14194 = _f_14193
    if x_657 is None:
        _x_14195 = None
        _x_14196 = _alt_14194(_x_14195, y_658)
        return _x_14196
    else:
        val_14197 = x_657
        if y_658 is None:
            _x_14198 = val_14197
            _x_14199 = None
            _x_14200 = _alt_14194(_x_14198, _x_14199)
            return _x_14200
        else:
            val_14201 = y_658
            _x_14202 = _alt_14189(val_14197, val_14201)
            return _x_14202

# Lean: Corpus.Functional.List.head?
def head_(__661: Any, xs_662: list[Any]) -> Any | None:
    def _f_14207():
        _x_14206 = None
        return _x_14206
    _alt_14208 = _f_14207
    def _f_14211(x_664: Any, tail_14209: list[Any]):
        _x_14210 = x_664
        return _x_14210
    _alt_14212 = _f_14211
    if len(xs_662) == 0:
        _x_14214 = _alt_14208()
        return _x_14214
    else:
        head_14215 = xs_662[0]
        tail_14216 = xs_662[1:]
        _x_14217 = _alt_14212(head_14215, tail_14216)
        return _x_14217

# Lean: Corpus.Functional.List.tail?
def tail_(__665: Any, xs_666: list[Any]) -> list[Any] | None:
    def _f_14221():
        _x_14220 = None
        return _x_14220
    _alt_14222 = _f_14221
    def _f_14225(head_14223: Any, xs__668: list[Any]):
        _x_14224 = xs__668
        return _x_14224
    _alt_14226 = _f_14225
    if len(xs_666) == 0:
        _x_14228 = _alt_14222()
        return _x_14228
    else:
        head_14229 = xs_666[0]
        tail_14230 = xs_666[1:]
        _x_14231 = _alt_14226(head_14229, tail_14230)
        return _x_14231

# Lean: Corpus.Functional.List.last?
def last_(__669: Any, xs_670: list[Any]) -> Any | None:
    def _f_14235():
        _x_14234 = None
        return _x_14234
    _alt_14236 = _f_14235
    def _f_14238(x_672: Any):
        _x_14237 = x_672
        return _x_14237
    _alt_14239 = _f_14238
    def _f_14242(head_14240: Any, xs__673: list[Any]):
        _x_14241 = last_(None, xs__673)
        return _x_14241
    _alt_14243 = _f_14242
    if len(xs_670) == 0:
        _x_14245 = _alt_14236()
        return _x_14245
    else:
        head_14246 = xs_670[0]
        tail_14247 = xs_670[1:]
        if len(tail_14247) == 0:
            _x_14248 = _alt_14239(head_14246)
            return _x_14248
        else:
            head_14249 = tail_14247[0]
            tail_14250 = tail_14247[1:]
            _x_14251 = [head_14249] + tail_14250
            _x_14252 = _alt_14243(head_14246, _x_14251)
            return _x_14252

# Lean: Corpus.Functional.List.nth
def nth(__674: Any, xs_675: list[Any], n_676: int) -> Any | None:
    def _f_14258(x_14256: int):
        _x_14257 = None
        return _x_14257
    _alt_14259 = _f_14258
    def _f_14262(x_677: Any, tail_14260: list[Any]):
        _x_14261 = x_677
        return _x_14261
    _alt_14263 = _f_14262
    def _f_14266(head_14264: Any, xs__678: list[Any], n__679: int):
        _x_14265 = nth(None, xs__678, n__679)
        return _x_14265
    _alt_14267 = _f_14266
    if len(xs_675) == 0:
        _x_14268 = _alt_14259(n_676)
        return _x_14268
    else:
        head_14269 = xs_675[0]
        tail_14270 = xs_675[1:]
        if n_676 == 0:
            _x_14271 = _alt_14263(head_14269, tail_14270)
            return _x_14271
        else:
            n_14272 = n_676 - 1
            _x_14273 = _alt_14267(head_14269, tail_14270, n_14272)
            return _x_14273

# Lean: Corpus.Functional.List.updateAt
def update_at(__680: Any, xs_681: list[Any], n_682: int, f_683: Callable[[Any], Any]) -> list[Any]:
    def _f_14279(x_14277: int):
        _x_14278 = []
        return _x_14278
    _alt_14280 = _f_14279
    def _f_14283(x_684: Any, xs__685: list[Any]):
        _x_14281 = f_683(x_684)
        _x_14282 = [_x_14281] + xs__685
        return _x_14282
    _alt_14284 = _f_14283
    def _f_14287(x_686: Any, xs__687: list[Any], n__688: int):
        _x_14285 = update_at(None, xs__687, n__688, f_683)
        _x_14286 = [x_686] + _x_14285
        return _x_14286
    _alt_14288 = _f_14287
    if len(xs_681) == 0:
        _x_14289 = _alt_14280(n_682)
        return _x_14289
    else:
        head_14290 = xs_681[0]
        tail_14291 = xs_681[1:]
        if n_682 == 0:
            _x_14292 = _alt_14284(head_14290, tail_14291)
            return _x_14292
        else:
            n_14293 = n_682 - 1
            _x_14294 = _alt_14288(head_14290, tail_14291, n_14293)
            return _x_14294

# Lean: Corpus.Functional.List.insertAt
def insert_at(__689: Any, xs_690: list[Any], n_691: int, x_692: Any) -> list[Any]:
    def _f_14299(xs_693: list[Any]):
        _x_14298 = [x_692] + xs_693
        return _x_14298
    _alt_14300 = _f_14299
    def _f_14304(x_14301: int):
        _x_14302 = []
        _x_14303 = [x_692] + _x_14302
        return _x_14303
    _alt_14305 = _f_14304
    def _f_14308(y_694: Any, ys_695: list[Any], n__696: int):
        _x_14306 = insert_at(None, ys_695, n__696, x_692)
        _x_14307 = [y_694] + _x_14306
        return _x_14307
    _alt_14309 = _f_14308
    if len(xs_690) == 0:
        _x_14310 = 0
        if n_691:
            _x_14314 = _alt_14305(n_691)
            return _x_14314
        else:
            _x_14315 = []
            _x_14316 = _alt_14300(_x_14315)
            return _x_14316
    else:
        head_14318 = xs_690[0]
        tail_14319 = xs_690[1:]
        if n_691 == 0:
            _x_14320 = [head_14318] + tail_14319
            _x_14321 = _alt_14300(_x_14320)
            return _x_14321
        else:
            n_14322 = n_691 - 1
            _x_14323 = _alt_14309(head_14318, tail_14319, n_14322)
            return _x_14323

# Lean: Corpus.Functional.List.removeAt
def remove_at(__697: Any, xs_698: list[Any], n_699: int) -> list[Any]:
    def _f_14329(x_14327: int):
        _x_14328 = []
        return _x_14328
    _alt_14330 = _f_14329
    def _f_14332(head_14331: Any, xs__700: list[Any]):
        return xs__700
    _alt_14333 = _f_14332
    def _f_14336(x_701: Any, xs__702: list[Any], n__703: int):
        _x_14334 = remove_at(None, xs__702, n__703)
        _x_14335 = [x_701] + _x_14334
        return _x_14335
    _alt_14337 = _f_14336
    if len(xs_698) == 0:
        _x_14338 = _alt_14330(n_699)
        return _x_14338
    else:
        head_14339 = xs_698[0]
        tail_14340 = xs_698[1:]
        if n_699 == 0:
            _x_14341 = _alt_14333(head_14339, tail_14340)
            return _x_14341
        else:
            n_14342 = n_699 - 1
            _x_14343 = _alt_14337(head_14339, tail_14340, n_14342)
            return _x_14343

# Lean: Corpus.Functional.List.splitAt
def split_at(__704: Any, n_705: int, xs_706: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_14349(xs_707: list[Any]):
        _x_14347 = []
        _x_14348 = (_x_14347, xs_707)
        return _x_14348
    _alt_14350 = _f_14349
    def _f_14354(x_14351: int):
        _x_14352 = []
        _x_14353 = (_x_14352, _x_14352)
        return _x_14353
    _alt_14355 = _f_14354
    def _f_14365(n__708: int, x_709: Any, xs__710: list[Any]):
        def _f_14358(l_711: list[Any], r_712: list[Any]):
            _x_14356 = [x_709] + l_711
            _x_14357 = (_x_14356, r_712)
            return _x_14357
        _alt_14359 = _f_14358
        _x_14360 = split_at(None, n__708, xs__710)
        match _x_14360:
            case (fst_14361, snd_14362):
                _x_14363 = _alt_14359(fst_14361, snd_14362)
                return _x_14363
    _alt_14366 = _f_14365
    if n_705 == 0:
        if len(xs_706) == 0:
            _x_14367 = []
            _x_14368 = _alt_14350(_x_14367)
            return _x_14368
        else:
            head_14369 = xs_706[0]
            tail_14370 = xs_706[1:]
            _x_14371 = [head_14369] + tail_14370
            _x_14372 = _alt_14350(_x_14371)
            return _x_14372
    else:
        n_14374 = n_705 - 1
        if len(xs_706) == 0:
            _x_14375 = n_14374 + 1
            _x_14376 = _alt_14355(_x_14375)
            return _x_14376
        else:
            head_14377 = xs_706[0]
            tail_14378 = xs_706[1:]
            _x_14379 = _alt_14366(n_14374, head_14377, tail_14378)
            return _x_14379

# Lean: Corpus.Functional.List.takeWhile
def take_while(__713: Any, p_714: Callable[[Any], bool], xs_715: list[Any]) -> list[Any]:
    def _f_14384():
        _x_14383 = []
        return _x_14383
    _alt_14385 = _f_14384
    def _f_14395(x_717: Any, xs__718: list[Any]):
        _x_14386 = p_714(x_717)
        _x_14387 = True
        if _x_14386:
            _x_14392 = take_while(None, p_714, xs__718)
            _x_14393 = [x_717] + _x_14392
            return _x_14393
        else:
            _x_14390 = []
            return _x_14390
    _alt_14396 = _f_14395
    if len(xs_715) == 0:
        _x_14398 = _alt_14385()
        return _x_14398
    else:
        head_14399 = xs_715[0]
        tail_14400 = xs_715[1:]
        _x_14401 = _alt_14396(head_14399, tail_14400)
        return _x_14401

# Lean: Corpus.Functional.List.dropWhile
def drop_while(__719: Any, p_720: Callable[[Any], bool], xs_721: list[Any]) -> list[Any]:
    def _f_14405():
        _x_14404 = []
        return _x_14404
    _alt_14406 = _f_14405
    def _f_14415(x_723: Any, xs__724: list[Any]):
        _x_14407 = p_720(x_723)
        _x_14408 = True
        if _x_14407:
            _x_14413 = drop_while(None, p_720, xs__724)
            return _x_14413
        else:
            _x_14411 = [x_723] + xs__724
            return _x_14411
    _alt_14416 = _f_14415
    if len(xs_721) == 0:
        _x_14418 = _alt_14406()
        return _x_14418
    else:
        head_14419 = xs_721[0]
        tail_14420 = xs_721[1:]
        _x_14421 = _alt_14416(head_14419, tail_14420)
        return _x_14421

# Lean: Corpus.Functional.List.replicate
def list_replicate(__725: Any, n_726: int, x_727: Any) -> list[Any]:
    def _f_14425():
        _x_14424 = []
        return _x_14424
    _alt_14426 = _f_14425
    def _f_14429(n__729: int):
        _x_14427 = list_replicate(None, n__729, x_727)
        _x_14428 = [x_727] + _x_14427
        return _x_14428
    _alt_14430 = _f_14429
    if n_726 == 0:
        _x_14432 = _alt_14426()
        return _x_14432
    else:
        n_14433 = n_726 - 1
        _x_14434 = _alt_14430(n_14433)
        return _x_14434

# Lean: Corpus.Functional.List.scanl
def scanl(__730: Any, __731: Any, f_732: Callable[[Any, Any], Any], init_733: Any, xs_734: list[Any]) -> list[Any]:
    def _f_14438():
        _x_14437 = []
        return _x_14437
    _alt_14439 = _f_14438
    def _f_14442(x_736: Any, xs__737: list[Any]):
        _x_14440 = f_732(init_733, x_736)
        _x_14441 = scanl(None, None, f_732, _x_14440, xs__737)
        return _x_14441
    _alt_14443 = _f_14442
    def _jp_14451(_y_14449: list[Any]):
        _x_14450 = [init_733] + _y_14449
        return _x_14450
    def _jp_14454():
        _x_14453 = _alt_14439()
        return _jp_14451(_x_14453)
    def _jp_14458(_y_14455: Any, _y_14456: list[Any]):
        _x_14457 = _alt_14443(_y_14455, _y_14456)
        return _jp_14451(_x_14457)
    if len(xs_734) == 0:
        return _jp_14454()
    else:
        head_14446 = xs_734[0]
        tail_14447 = xs_734[1:]
        return _jp_14458(head_14446, tail_14447)

# Lean: Corpus.Functional.List.interleave
def interleave(__738: Any, xs_739: list[Any], ys_740: list[Any]) -> list[Any]:
    def _f_14460(ys_741: list[Any]):
        return ys_741
    _alt_14461 = _f_14460
    _alt_14462 = _f_14460
    def _f_14466(x_742: Any, xs__743: list[Any], y_744: Any, ys__745: list[Any]):
        _x_14463 = interleave(None, xs__743, ys__745)
        _x_14464 = [y_744] + _x_14463
        _x_14465 = [x_742] + _x_14464
        return _x_14465
    _alt_14467 = _f_14466
    if len(xs_739) == 0:
        if len(ys_740) == 0:
            _x_14468 = []
            _x_14469 = _alt_14461(_x_14468)
            return _x_14469
        else:
            head_14470 = ys_740[0]
            tail_14471 = ys_740[1:]
            _x_14472 = [head_14470] + tail_14471
            _x_14473 = _alt_14461(_x_14472)
            return _x_14473
    else:
        head_14475 = xs_739[0]
        tail_14476 = xs_739[1:]
        if len(ys_740) == 0:
            _x_14477 = [head_14475] + tail_14476
            _x_14478 = _alt_14462(_x_14477)
            return _x_14478
        else:
            head_14479 = ys_740[0]
            tail_14480 = ys_740[1:]
            _x_14481 = _alt_14467(head_14475, tail_14476, head_14479, tail_14480)
            return _x_14481

# Lean: Corpus.Functional.Either.map
def either_map(__746: Any, __747: Any, __748: Any, f_749: Callable[[Any], Any], x_14485: Any) -> Any:
    def _f_14487(a_750: Any):
        _x_14486 = left(None, None, a_750)
        return _x_14486
    _alt_14488 = _f_14487
    def _f_14491(b_751: Any):
        _x_14489 = f_749(b_751)
        _x_14490 = right(None, None, _x_14489)
        return _x_14490
    _alt_14492 = _f_14491
    match x_14485:
        case left(a_14493):
            _x_14494 = _alt_14488(a_14493)
            return _x_14494
        case right(a_14495):
            _x_14496 = _alt_14492(a_14495)
            return _x_14496

# Lean: Corpus.Functional.Either.mapLeft
def map_left(__752: Any, __753: Any, __754: Any, f_755: Callable[[Any], Any], x_14499: Any) -> Any:
    def _f_14502(a_756: Any):
        _x_14500 = f_755(a_756)
        _x_14501 = left(None, None, _x_14500)
        return _x_14501
    _alt_14503 = _f_14502
    def _f_14505(b_757: Any):
        _x_14504 = right(None, None, b_757)
        return _x_14504
    _alt_14506 = _f_14505
    match x_14499:
        case left(a_14507):
            _x_14508 = _alt_14503(a_14507)
            return _x_14508
        case right(a_14509):
            _x_14510 = _alt_14506(a_14509)
            return _x_14510

# Lean: Corpus.Functional.Either.bind
def either_bind(__758: Any, __759: Any, __760: Any, x_761: Any, f_762: Callable[[Any], Any]) -> Any:
    def _f_14514(a_763: Any):
        _x_14513 = left(None, None, a_763)
        return _x_14513
    _alt_14515 = _f_14514
    def _f_14517(b_764: Any):
        _x_14516 = f_762(b_764)
        return _x_14516
    _alt_14518 = _f_14517
    match x_761:
        case left(a_14519):
            _x_14520 = _alt_14515(a_14519)
            return _x_14520
        case right(a_14521):
            _x_14522 = _alt_14518(a_14521)
            return _x_14522

# Lean: Corpus.Functional.Either.isLeft
def is_left(__765: Any, __766: Any, x_14525: Any) -> bool:
    def _f_14528(a_14526: Any):
        _x_14527 = True
        return True
    _alt_14529 = _f_14528
    def _f_14532(a_14530: Any):
        _x_14531 = False
        return False
    _alt_14533 = _f_14532
    match x_14525:
        case left(a_14534):
            _x_14535 = _alt_14529(a_14534)
            return _x_14535
        case right(a_14536):
            _x_14537 = _alt_14533(a_14536)
            return _x_14537

# Lean: Corpus.Functional.Either.isRight
def is_right(__767: Any, __768: Any, x_14540: Any) -> bool:
    def _f_14543(a_14541: Any):
        _x_14542 = False
        return False
    _alt_14544 = _f_14543
    def _f_14547(a_14545: Any):
        _x_14546 = True
        return True
    _alt_14548 = _f_14547
    match x_14540:
        case left(a_14549):
            _x_14550 = _alt_14544(a_14549)
            return _x_14550
        case right(a_14551):
            _x_14552 = _alt_14548(a_14551)
            return _x_14552

# Lean: Corpus.Strings.isEmpty
def strings_is_empty(s_769: str) -> bool:
    _x_14557 = len(s_769)
    _x_14558 = 0
    _x_14561 = _x_14557 == 0
    return _x_14561

# Lean: Corpus.Strings.isNotEmpty
def is_not_empty(s_770: str) -> bool:
    _x_14563 = 0
    _x_14566 = len(s_770)
    _x_14567 = 0 < _x_14566
    return _x_14567

# Lean: Corpus.Strings.head
def head(s_771: str) -> str | None:
    _x_14570 = list(s_771)
    _x_14571 = (lambda xs: xs[0] if xs else None)(_x_14570)
    return _x_14571

# Lean: Corpus.Strings.tail
def tail(s_772: str) -> str:
    def _f_14574():
        _x_14573 = ""
        return _x_14573
    _alt_14575 = _f_14574
    def _f_14578(head_14576: str, cs_774: list[str]):
        _x_14577 = ''.join(cs_774)
        return _x_14577
    _alt_14579 = _f_14578
    _x_14580 = list(s_772)
    if len(_x_14580) == 0:
        _x_14582 = _alt_14575()
        return _x_14582
    else:
        head_14583 = _x_14580[0]
        tail_14584 = _x_14580[1:]
        _x_14585 = _alt_14579(head_14583, tail_14584)
        return _x_14585

# Lean: Corpus.Strings.last
def last(s_775: str) -> str | None:
    _x_14588 = list(s_775)
    _x_14589 = (lambda xs: xs[-1] if xs else None)(_x_14588)
    return _x_14589

# Lean: Corpus.Strings.init
def init(s_776: str) -> str:
    _x_14591 = list(s_776)
    _x_14592 = (lambda xs: xs[:-1])(_x_14591)
    _x_14593 = ''.join(_x_14592)
    return _x_14593

# Lean: Corpus.Strings.take
def strings_take(n_777: int, s_778: str) -> str:
    _x_14595 = list(s_778)
    _x_14596 = (lambda n, xs: xs[:n])(_x_14595)
    _x_14597 = ''.join(_x_14596)
    return _x_14597

# Lean: Corpus.Strings.drop
def strings_drop(n_779: int, s_780: str) -> str:
    _x_14599 = list(s_780)
    _x_14600 = (lambda n, xs: xs[n:])(_x_14599)
    _x_14601 = ''.join(_x_14600)
    return _x_14601

# Lean: Corpus.Strings.charAt
def char_at(s_781: str, i_782: int) -> str | None:
    def _f_14606(xs_783: list[str], i_784: int):
        _x_14604 = len(xs_783)
        _x_14605 = i_784 < _x_14604
        return _x_14605
    _x_14608 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_14609 = list(s_781)
    _x_14610 = _x_14608(_x_14609, i_782)
    return _x_14610

# Lean: Corpus.Strings.substring
def substring(s_785: str, start_786: int, len: int) -> str:
    _x_14612 = list(s_785)
    _x_14613 = (lambda n, xs: xs[n:])(_x_14612)
    _x_14614 = (lambda n, xs: xs[:n])(_x_14613)
    _x_14615 = ''.join(_x_14614)
    return _x_14615

# Lean: Corpus.Strings.slice
def slice(s_787: str, start_788: int, stop: int) -> str:
    _x_14620 = stop - start_788
    _x_14621 = substring(s_787, start_788, _x_14620)
    return _x_14621

# Lean: Corpus.Strings.append
def append(s1: str, s2: str) -> str:
    _x_14626 = s1 + s2
    return _x_14626

# Lean: Corpus.Strings.concat
def strings_concat(ss: list[str]) -> str:
    def _f_14634(x1_14628: str, x2_14629: str):
        _x_14633 = x1_14628 + x2_14629
        return _x_14633
    _x_14635 = ""
    _x_14636 = functools.reduce(_f_14634, ss, _x_14635)
    return _x_14636

# Lean: Corpus.Strings.intercalate
def intercalate(sep_789: str, ss_790: list[str]) -> str:
    def _f_14639():
        _x_14638 = ""
        return _x_14638
    _alt_14640 = _f_14639
    def _f_14641(s_792: str):
        return s_792
    _alt_14642 = _f_14641
    def _f_14649(s_793: str, rest_794: list[str]):
        _x_14646 = s_793 + sep_789
        _x_14647 = intercalate(sep_789, rest_794)
        _x_14648 = _x_14646 + _x_14647
        return _x_14648
    _alt_14650 = _f_14649
    if len(ss_790) == 0:
        _x_14652 = _alt_14640()
        return _x_14652
    else:
        head_14653 = ss_790[0]
        tail_14654 = ss_790[1:]
        if len(tail_14654) == 0:
            _x_14655 = _alt_14642(head_14653)
            return _x_14655
        else:
            head_14656 = tail_14654[0]
            tail_14657 = tail_14654[1:]
            _x_14658 = [head_14656] + tail_14657
            _x_14659 = _alt_14650(head_14653, _x_14658)
            return _x_14659

# Lean: Corpus.Strings.join
def join(ss_795: list[str]) -> str:
    _x_14663 = strings_concat(ss_795)
    return _x_14663

# Lean: Corpus.Strings.replicate
def strings_replicate(n_796: int, s_797: str) -> str:
    _x_14665 = ""
    _x_14666 = strings_replicate_go(s_797, n_796, _x_14665)
    return _x_14666

# Lean: Corpus.Strings.reverse
def strings_reverse(s_798: str) -> str:
    _x_14668 = list(s_798)
    _x_14669 = list(reversed(_x_14668))
    _x_14670 = ''.join(_x_14669)
    return _x_14670

# Lean: Corpus.Strings.toUpper
def to_upper(s_799: str) -> str:
    _x_14672 = (lambda c: c.upper())
    _x_14673 = list(s_799)
    _x_14674 = [_x_14672(x) for x in _x_14673]
    _x_14675 = ''.join(_x_14674)
    return _x_14675

# Lean: Corpus.Strings.toLower
def to_lower(s_800: str) -> str:
    _x_14677 = (lambda c: c.lower())
    _x_14678 = list(s_800)
    _x_14679 = [_x_14677(x) for x in _x_14678]
    _x_14680 = ''.join(_x_14679)
    return _x_14680

# Lean: Corpus.Strings.capitalize
def capitalize(s_801: str) -> str:
    def _f_14683():
        _x_14682 = ""
        return _x_14682
    _alt_14684 = _f_14683
    def _f_14688(c_803: str, cs_804: list[str]):
        _x_14685 = (lambda c: c.upper())(c_803)
        _x_14686 = [_x_14685] + cs_804
        _x_14687 = ''.join(_x_14686)
        return _x_14687
    _alt_14689 = _f_14688
    _x_14690 = list(s_801)
    if len(_x_14690) == 0:
        _x_14692 = _alt_14684()
        return _x_14692
    else:
        head_14693 = _x_14690[0]
        tail_14694 = _x_14690[1:]
        _x_14695 = _alt_14689(head_14693, tail_14694)
        return _x_14695

# Lean: Corpus.Strings.swapCase
def swap_case(s_805: str) -> str:
    def _f_14711(c_806: str):
        _x_14698 = (lambda c: c.isupper())(c_806)
        _x_14699 = True
        if _x_14698:
            _x_14709 = (lambda c: c.lower())(c_806)
            return _x_14709
        else:
            _x_14702 = (lambda c: c.islower())(c_806)
            if _x_14702:
                _x_14706 = (lambda c: c.upper())(c_806)
                return _x_14706
            else:
                return c_806
    _x_14712 = list(s_805)
    _x_14713 = [_f_14711(x) for x in _x_14712]
    _x_14714 = ''.join(_x_14713)
    return _x_14714

# Lean: Corpus.Strings.trimLeft
def trim_left(s_807: str) -> str:
    def _f_14723(x_14716: str):
        _x_14720 = 32
        _x_14721 = chr(_x_14720)
        _x_14722 = x_14716 == _x_14721
        return _x_14722
    _x_14724 = list(s_807)
    _x_14725 = drop_while(None, _f_14723, _x_14724)
    _x_14726 = ''.join(_x_14725)
    return _x_14726

# Lean: Corpus.Strings.trimRight
def trim_right(s_808: str) -> str:
    def _f_14735(x_14728: str):
        _x_14732 = 32
        _x_14733 = chr(_x_14732)
        _x_14734 = x_14728 == _x_14733
        return _x_14734
    _x_14736 = list(s_808)
    _x_14737 = list(reversed(_x_14736))
    _x_14738 = drop_while(None, _f_14735, _x_14737)
    _x_14739 = list(reversed(_x_14738))
    _x_14740 = ''.join(_x_14739)
    return _x_14740

# Lean: Corpus.Strings.trim
def trim(s_809: str) -> str:
    _x_14742 = trim_left(s_809)
    _x_14743 = trim_right(_x_14742)
    return _x_14743

# Lean: Corpus.Strings.padLeft
def pad_left(n_810: int, c_811: str, s_812: str) -> str:
    _x_14745 = len(s_812)
    _x_14746 = n_810 <= _x_14745
    if _x_14746:
        return s_812
    else:
        _x_14754 = n_810 - _x_14745
        _x_14755 = list_replicate(None, _x_14754, c_811)
        _x_14756 = ''.join(_x_14755)
        _x_14757 = _x_14756 + s_812
        return _x_14757

# Lean: Corpus.Strings.padRight
def pad_right(n_813: int, c_814: str, s_815: str) -> str:
    _x_14761 = len(s_815)
    _x_14762 = n_813 <= _x_14761
    if _x_14762:
        return s_815
    else:
        _x_14770 = n_813 - _x_14761
        _x_14771 = list_replicate(None, _x_14770, c_814)
        _x_14772 = ''.join(_x_14771)
        _x_14773 = s_815 + _x_14772
        return _x_14773

# Lean: Corpus.Strings.center
def center(n_816: int, c_817: str, s_818: str) -> str:
    _x_14777 = len(s_818)
    _x_14778 = n_816 <= _x_14777
    if _x_14778:
        return s_818
    else:
        _x_14783 = n_816 - _x_14777
        _x_14787 = 2
        _x_14790 = _x_14783 // 2
        _x_14791 = _x_14783 - _x_14790
        _x_14795 = list_replicate(None, _x_14790, c_817)
        _x_14796 = ''.join(_x_14795)
        _x_14797 = _x_14796 + s_818
        _x_14798 = list_replicate(None, _x_14791, c_817)
        _x_14799 = ''.join(_x_14798)
        _x_14800 = _x_14797 + _x_14799
        return _x_14800

# Lean: Corpus.Strings.contains
def strings_contains(s_819: str, sub_820: str) -> bool:
    _x_14804 = list(s_819)
    _x_14805 = strings_contains_go(sub_820, _x_14804)
    return _x_14805

# Lean: Corpus.Strings.indexOf
def index_of(s_821: str, sub_822: str) -> int | None:
    _x_14807 = list(s_821)
    _x_14808 = 0
    _x_14811 = index_of_go(sub_822, _x_14807, 0)
    return _x_14811

# Lean: Corpus.Strings.count
def count(s_823: str, sub_824: str) -> int:
    _x_14813 = list(s_823)
    _x_14814 = 0
    _x_14817 = count_go(sub_824, _x_14813, 0)
    return _x_14817

# Lean: Corpus.Strings.countChar
def strings_count_char(c_825: str, s_826: str) -> int:
    def _f_14835(acc_827: int, x_828: str):
        _x_14822 = x_828 == c_825
        _x_14823 = True
        if _x_14822:
            _x_14830 = 1
            _x_14833 = acc_827 + 1
            return _x_14833
        else:
            return acc_827
    _x_14836 = 0
    _x_14839 = list(s_826)
    _x_14840 = functools.reduce(_f_14835, _x_14839, 0)
    return _x_14840

# Lean: Corpus.Strings.startsWith
def starts_with(s_829: str, pfx: str) -> bool:
    _x_14846 = len(pfx)
    _x_14847 = list(s_829)
    _x_14848 = (lambda n, xs: xs[:n])(_x_14847)
    _x_14849 = list(pfx)
    _x_14850 = _x_14848 == _x_14849
    return _x_14850

# Lean: Corpus.Strings.endsWith
def ends_with(s_830: str, suffix: str) -> bool:
    _x_14856 = len(suffix)
    _x_14857 = list(s_830)
    _x_14858 = list(reversed(_x_14857))
    _x_14859 = (lambda n, xs: xs[:n])(_x_14858)
    _x_14860 = list(suffix)
    _x_14861 = list(reversed(_x_14860))
    _x_14862 = _x_14859 == _x_14861
    return _x_14862

# Lean: Corpus.Strings.isPalindrome
def strings_is_palindrome(s_831: str) -> bool:
    _x_14864 = (lambda c: c.lower())
    def _f_14877(c_832: str):
        def _f_14866():
            _x_14865 = True
            return True
        _alt_14867 = _f_14866
        def _f_14869():
            _x_14868 = str.isdigit(c_832)
            return _x_14868
        _alt_14870 = _f_14869
        _x_14871 = str.isalpha(c_832)
        if _x_14871:
            _x_14875 = _alt_14867()
            return _x_14875
        else:
            _x_14873 = _alt_14870()
            return _x_14873
    _x_14878 = list(s_831)
    _x_14879 = [x for x in _x_14878 if _f_14877(x)]
    _x_14880 = [_x_14864(x) for x in _x_14879]
    _x_14885 = list(reversed(_x_14880))
    _x_14886 = _x_14880 == _x_14885
    return _x_14886

# Lean: Corpus.Strings.isDigits
def is_digits(s_836: str) -> bool:
    def _f_14889():
        _x_14888 = False
        return False
    _alt_14890 = _f_14889
    def _f_14894():
        _x_14891 = list(s_836)
        _x_14892 = str.isdigit
        _x_14893 = all(_x_14892(x) for x in _x_14891)
        return _x_14893
    _alt_14895 = _f_14894
    _x_14896 = len(s_836) == 0
    _x_14897 = not _x_14896
    if _x_14897:
        _x_14901 = _alt_14895()
        return _x_14901
    else:
        _x_14899 = _alt_14890()
        return _x_14899

# Lean: Corpus.Strings.isAlpha
def is_alpha(s_839: str) -> bool:
    def _f_14905():
        _x_14904 = False
        return False
    _alt_14906 = _f_14905
    def _f_14910():
        _x_14907 = list(s_839)
        _x_14908 = str.isalpha
        _x_14909 = all(_x_14908(x) for x in _x_14907)
        return _x_14909
    _alt_14911 = _f_14910
    _x_14912 = len(s_839) == 0
    _x_14913 = not _x_14912
    if _x_14913:
        _x_14917 = _alt_14911()
        return _x_14917
    else:
        _x_14915 = _alt_14906()
        return _x_14915

# Lean: Corpus.Strings.splitOn
def split_on(s_842: str, sep_843: str) -> list[str]:
    _x_14920 = len(sep_843) == 0
    _x_14921 = True
    if _x_14920:
        _x_14929 = []
        _x_14930 = [s_842] + _x_14929
        return _x_14930
    else:
        _x_14924 = list(s_842)
        _x_14925 = []
        _x_14926 = []
        _x_14927 = split_on_go(sep_843, _x_14924, _x_14925, _x_14926)
        return _x_14927

# Lean: Corpus.Strings.lines
def lines(s_844: str) -> list[str]:
    _x_14933 = "\n"
    _x_14934 = split_on(s_844, _x_14933)
    return _x_14934

# Lean: Corpus.Strings.words
def words(s_845: str) -> list[str]:
    _x_14936 = list(s_845)
    _x_14937 = []
    _x_14938 = []
    _x_14939 = words_go(_x_14936, _x_14937, _x_14938)
    return _x_14939

# Lean: Corpus.Strings.unlines
def unlines(ss_846: list[str]) -> str:
    _x_14941 = "\n"
    _x_14942 = intercalate(_x_14941, ss_846)
    return _x_14942

# Lean: Corpus.Strings.unwords
def unwords(ss_847: list[str]) -> str:
    _x_14944 = " "
    _x_14945 = intercalate(_x_14944, ss_847)
    return _x_14945

# Lean: Corpus.Strings.replace
def replace(s_848: str, old_849: str, new_850: str) -> str:
    _x_14947 = split_on(s_848, old_849)
    _x_14948 = intercalate(new_850, _x_14947)
    return _x_14948

# Lean: Corpus.Strings.replaceFirst
def replace_first(s_851: str, old_852: str, new_853: str) -> str:
    def _f_14950():
        return s_851
    _alt_14951 = _f_14950
    def _f_14964(i_855: int):
        _x_14955 = strings_take(i_855, s_851)
        _x_14956 = _x_14955 + new_853
        _x_14960 = len(old_852)
        _x_14961 = i_855 + _x_14960
        _x_14962 = strings_drop(_x_14961, s_851)
        _x_14963 = _x_14956 + _x_14962
        return _x_14963
    _alt_14965 = _f_14964
    _x_14966 = index_of(s_851, old_852)
    if _x_14966 is None:
        _x_14968 = _alt_14951()
        return _x_14968
    else:
        val_14969 = _x_14966
        _x_14970 = _alt_14965(val_14969)
        return _x_14970

# Lean: Corpus.Strings.removePrefix
def remove_prefix(pfx_856: str, s_857: str) -> str:
    _x_14973 = starts_with(s_857, pfx_856)
    _x_14974 = True
    if _x_14973:
        _x_14978 = len(pfx_856)
        _x_14979 = strings_drop(_x_14978, s_857)
        return _x_14979
    else:
        return s_857

# Lean: Corpus.Strings.removeSuffix
def remove_suffix(suffix_858: str, s_859: str) -> str:
    _x_14982 = ends_with(s_859, suffix_858)
    _x_14983 = True
    if _x_14982:
        _x_14990 = len(s_859)
        _x_14991 = len(suffix_858)
        _x_14992 = _x_14990 - _x_14991
        _x_14993 = strings_take(_x_14992, s_859)
        return _x_14993
    else:
        return s_859

# Lean: Corpus.Strings.toCharList
def to_char_list(s_860: str) -> list[str]:
    _x_14996 = list(s_860)
    return _x_14996

# Lean: Corpus.Strings.fromCharList
def from_char_list(cs_861: list[str]) -> str:
    _x_14998 = ''.join(cs_861)
    return _x_14998

# Lean: Corpus.Strings.filterChars
def filter_chars(p_862: Callable[[str], bool], s_863: str) -> str:
    _x_15000 = list(s_863)
    _x_15001 = [x for x in _x_15000 if p_862(x)]
    _x_15002 = ''.join(_x_15001)
    return _x_15002

# Lean: Corpus.Strings.mapChars
def map_chars(f_864: Callable[[str], str], s_865: str) -> str:
    _x_15004 = list(s_865)
    _x_15005 = [f_864(x) for x in _x_15004]
    _x_15006 = ''.join(_x_15005)
    return _x_15006

# Lean: Corpus.Strings.ord
def strings_ord(c_866: str) -> int:
    _x_15008 = ord(c_866)
    return _x_15008

# Lean: Corpus.Strings.chr
def strings_chr(n_867: int) -> str:
    _x_15010 = chr(n_867)
    return _x_15010

# Lean: Corpus.Strings.toAsciiCodes
def to_ascii_codes(s_868: str) -> list[int]:
    _x_15012 = ord
    _x_15013 = list(s_868)
    _x_15014 = [_x_15012(x) for x in _x_15013]
    return _x_15014

# Lean: Corpus.Strings.fromAsciiCodes
def from_ascii_codes(ns: list[int]) -> str:
    _x_15016 = chr
    _x_15017 = [_x_15016(x) for x in ns]
    _x_15018 = ''.join(_x_15017)
    return _x_15018

# Lean: Corpus.Games.Player.other
def other(x_15020: Player) -> Player:
    def _f_15022():
        _x_15021 = O()
        return _x_15021
    _alt_15023 = _f_15022
    def _f_15025():
        _x_15024 = X()
        return _x_15024
    _alt_15026 = _f_15025
    match x_15020:
        case X():
            _x_15028 = _alt_15023()
            return _x_15028
        case O():
            _x_15030 = _alt_15026()
            return _x_15030

# Lean: Corpus.Games.TicTacToe.empty
def tic_tac_toe_empty() -> TicTacToe:
    _x_15033 = 9
    _x_15036 = None
    _x_15037 = list_replicate(None, 9, _x_15036)
    _x_15038 = X()
    _x_15039 = TicTacToe_mk(_x_15037, _x_15038)
    return _x_15039

# Lean: Corpus.Games.TicTacToe.get
def tic_tac_toe_get(g_871: TicTacToe, row: int, col: int) -> Player | None:
    def _f_15040(p_872: Player | None):
        return p_872
    _alt_15041 = _f_15040
    def _f_15043():
        _x_15042 = None
        return _x_15042
    _alt_15044 = _f_15043
    def _f_15048(xs_874: list[Player | None], i_875: int):
        _x_15046 = len(xs_874)
        _x_15047 = i_875 < _x_15046
        return _x_15047
    _x_15050 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_15051 = g_871.tic_tac_toe_0
    _x_15058 = 3
    _x_15061 = row * 3
    _x_15062 = _x_15061 + col
    _x_15063 = _x_15050(_x_15051, _x_15062)
    if _x_15063 is None:
        _x_15065 = _alt_15044()
        return _x_15065
    else:
        val_15066 = _x_15063
        _x_15067 = _alt_15041(val_15066)
        return _x_15067

# Lean: Corpus.Games.TicTacToe.set
def tic_tac_toe_set(g_876: TicTacToe, row_877: int, col_878: int) -> TicTacToe | None:
    _x_15076 = 3
    _x_15079 = row_877 * 3
    _x_15080 = _x_15079 + col_878
    _x_15081 = 9
    _x_15084 = 9 <= _x_15080
    if _x_15084:
        _x_15119 = None
        return _x_15119
    else:
        def _f_15093():
            _x_15086 = g_876.tic_tac_toe_0
            _x_15087 = g_876.tic_tac_toe_1
            _x_15088 = _x_15087
            _x_15089 = _x_15086[:_x_15080] + [_x_15088] + _x_15086[_x_15080+1:]
            _x_15090 = other(_x_15087)
            _x_15091 = TicTacToe_mk(_x_15089, _x_15090)
            _x_15092 = _x_15091
            return _x_15092
        _alt_15094 = _f_15093
        def _f_15097(x_15095: Player | None | None):
            _x_15096 = None
            return _x_15096
        _alt_15098 = _f_15097
        def _f_15102(xs_881: list[Player | None], i_882: int):
            _x_15100 = len(xs_881)
            _x_15101 = i_882 < _x_15100
            return _x_15101
        _x_15104 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_15105 = g_876.tic_tac_toe_0
        _x_15106 = _x_15104(_x_15105, _x_15080)
        if _x_15106 is None:
            _x_15107 = None
            _x_15108 = _alt_15098(_x_15107)
            return _x_15108
        else:
            val_15109 = _x_15106
            if val_15109 is None:
                _x_15111 = _alt_15094()
                return _x_15111
            else:
                val_15112 = val_15109
                _x_15113 = val_15112
                _x_15114 = _x_15113
                _x_15115 = _alt_15098(_x_15114)
                return _x_15115

# Lean: Corpus.Games.TicTacToe.checkLine
def check_line(g_883: TicTacToe, i1: int, i2: int, i3: int) -> Player | None:
    def _f_15152(p1_884: Player, p2_885: Player, p3_886: Player):
        def _f_15123():
            _x_15122 = False
            return False
        _alt_15124 = _f_15123
        def _f_15128():
            _x_15127 = p2_885 == p3_886
            return _x_15127
        _alt_15129 = _f_15128
        _x_15132 = p1_884 == p2_885
        def _jp_15145(_y_15137: bool):
            _x_15138 = True
            if _y_15137:
                _x_15143 = p1_884
                return _x_15143
            else:
                _x_15141 = None
                return _x_15141
        def _jp_15151():
            _x_15150 = _alt_15129()
            return _jp_15145(_x_15150)
        def _jp_15148():
            _x_15147 = _alt_15124()
            return _jp_15145(_x_15147)
        if _x_15132:
            return _jp_15151()
        else:
            return _jp_15148()
    _alt_15153 = _f_15152
    def _f_15158(x_15154: Player | None | None, x_15155: Player | None | None, x_15156: Player | None | None):
        _x_15157 = None
        return _x_15157
    _alt_15159 = _f_15158
    def _f_15163(xs_889: list[Player | None], i_890: int):
        _x_15161 = len(xs_889)
        _x_15162 = i_890 < _x_15161
        return _x_15162
    _x_15165 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_15166 = g_883.tic_tac_toe_0
    _x_15167 = _x_15165(_x_15166, i1)
    if _x_15167 is None:
        _x_15168 = None
        _x_15169 = _x_15165(_x_15166, i2)
        _x_15170 = _x_15165(_x_15166, i3)
        _x_15171 = _alt_15159(_x_15168, _x_15169, _x_15170)
        return _x_15171
    else:
        val_15172 = _x_15167
        if val_15172 is None:
            _x_15173 = None
            _x_15174 = _x_15173
            _x_15175 = _x_15165(_x_15166, i2)
            _x_15176 = _x_15165(_x_15166, i3)
            _x_15177 = _alt_15159(_x_15174, _x_15175, _x_15176)
            return _x_15177
        else:
            val_15178 = val_15172
            _x_15179 = _x_15165(_x_15166, i2)
            if _x_15179 is None:
                _x_15180 = val_15178
                _x_15181 = _x_15180
                _x_15182 = None
                _x_15183 = _x_15165(_x_15166, i3)
                _x_15184 = _alt_15159(_x_15181, _x_15182, _x_15183)
                return _x_15184
            else:
                val_15185 = _x_15179
                if val_15185 is None:
                    _x_15186 = val_15178
                    _x_15187 = _x_15186
                    _x_15188 = None
                    _x_15189 = _x_15188
                    _x_15190 = _x_15165(_x_15166, i3)
                    _x_15191 = _alt_15159(_x_15187, _x_15189, _x_15190)
                    return _x_15191
                else:
                    val_15192 = val_15185
                    _x_15193 = _x_15165(_x_15166, i3)
                    if _x_15193 is None:
                        _x_15194 = val_15178
                        _x_15195 = _x_15194
                        _x_15196 = val_15192
                        _x_15197 = _x_15196
                        _x_15198 = None
                        _x_15199 = _alt_15159(_x_15195, _x_15197, _x_15198)
                        return _x_15199
                    else:
                        val_15200 = _x_15193
                        if val_15200 is None:
                            _x_15201 = val_15178
                            _x_15202 = _x_15201
                            _x_15203 = val_15192
                            _x_15204 = _x_15203
                            _x_15205 = None
                            _x_15206 = _x_15205
                            _x_15207 = _alt_15159(_x_15202, _x_15204, _x_15206)
                            return _x_15207
                        else:
                            val_15208 = val_15200
                            _x_15209 = _alt_15153(val_15178, val_15192, val_15208)
                            return _x_15209

# Lean: Corpus.Games.TicTacToe.winner
def winner(g_891: TicTacToe) -> Player | None:
    _x_15217 = 0
    _x_15220 = 1
    _x_15223 = 2
    _x_15226 = (1, 2)
    _x_15227 = (0, _x_15226)
    _x_15228 = 3
    _x_15231 = 4
    _x_15234 = 5
    _x_15237 = (4, 5)
    _x_15238 = (3, _x_15237)
    _x_15239 = 6
    _x_15242 = 7
    _x_15245 = 8
    _x_15248 = (7, 8)
    _x_15249 = (6, _x_15248)
    _x_15250 = (3, 6)
    _x_15251 = (0, _x_15250)
    _x_15252 = (4, 7)
    _x_15253 = (1, _x_15252)
    _x_15254 = (5, 8)
    _x_15255 = (2, _x_15254)
    _x_15256 = (4, 8)
    _x_15257 = (0, _x_15256)
    _x_15258 = (4, 6)
    _x_15259 = (2, _x_15258)
    _x_15260 = []
    _x_15261 = [_x_15259] + _x_15260
    _x_15262 = [_x_15257] + _x_15261
    _x_15263 = [_x_15255] + _x_15262
    _x_15264 = [_x_15253] + _x_15263
    _x_15265 = [_x_15251] + _x_15264
    _x_15266 = [_x_15249] + _x_15265
    _x_15267 = [_x_15238] + _x_15266
    _x_15268 = [_x_15227] + _x_15267
    def _f_15280(x_15269: tuple[int, tuple[int, int]]):
        def _f_15271(i1_892: int, i2_893: int, i3_894: int):
            _x_15270 = check_line(g_891, i1_892, i2_893, i3_894)
            return _x_15270
        _alt_15272 = _f_15271
        match x_15269:
            case (fst_15273, snd_15274):
                match snd_15274:
                    case (fst_15275, snd_15276):
                        _x_15277 = _alt_15272(fst_15273, fst_15275, snd_15276)
                        return _x_15277
    _x_15281 = next((y for x in _x_15268 if (y := _f_15280(x)) is not None), None)
    return _x_15281

# Lean: Corpus.Games.TicTacToe.isDraw
def is_draw(g_895: TicTacToe) -> bool:
    def _f_15284():
        _x_15283 = False
        return False
    _alt_15285 = _f_15284
    def _f_15289():
        _x_15286 = g_895.tic_tac_toe_0
        _x_15287 = (lambda x: x is not None)(None)
        _x_15288 = all(_x_15287(x) for x in _x_15286)
        return _x_15288
    _alt_15290 = _f_15289
    _x_15291 = winner(g_895)
    _x_15292 = (lambda x: x is None)(_x_15291)
    if _x_15292:
        _x_15296 = _alt_15290()
        return _x_15296
    else:
        _x_15294 = _alt_15285()
        return _x_15294

# Lean: Corpus.Games.TicTacToe.isOver
def tic_tac_toe_is_over(g_898: TicTacToe) -> bool:
    def _f_15300():
        _x_15299 = True
        return True
    _alt_15301 = _f_15300
    def _f_15303():
        _x_15302 = is_draw(g_898)
        return _x_15302
    _alt_15304 = _f_15303
    _x_15305 = winner(g_898)
    _x_15306 = (lambda x: x is not None)(_x_15305)
    if _x_15306:
        _x_15310 = _alt_15301()
        return _x_15310
    else:
        _x_15308 = _alt_15304()
        return _x_15308

# Lean: Corpus.Games.TicTacToe.validMoves
def valid_moves(g_901: TicTacToe) -> list[tuple[int, int]]:
    _x_15313 = tic_tac_toe_is_over(g_901)
    _x_15314 = True
    if _x_15313:
        _x_15362 = []
        return _x_15362
    else:
        def _f_15355(i_902: int):
            def _f_15330():
                _x_15320 = 3
                _x_15323 = i_902 // 3
                _x_15327 = i_902 % 3
                _x_15328 = (_x_15323, _x_15327)
                _x_15329 = _x_15328
                return _x_15329
            _alt_15331 = _f_15330
            def _f_15334(x_15332: Player | None | None):
                _x_15333 = None
                return _x_15333
            _alt_15335 = _f_15334
            def _f_15339(xs_904: list[Player | None], i_905: int):
                _x_15337 = len(xs_904)
                _x_15338 = i_905 < _x_15337
                return _x_15338
            _x_15341 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_15342 = g_901.tic_tac_toe_0
            _x_15343 = _x_15341(_x_15342, i_902)
            if _x_15343 is None:
                _x_15344 = None
                _x_15345 = _alt_15335(_x_15344)
                return _x_15345
            else:
                val_15346 = _x_15343
                if val_15346 is None:
                    _x_15348 = _alt_15331()
                    return _x_15348
                else:
                    val_15349 = val_15346
                    _x_15350 = val_15349
                    _x_15351 = _x_15350
                    _x_15352 = _alt_15335(_x_15351)
                    return _x_15352
        _x_15356 = 9
        _x_15359 = list(range(9))
        _x_15360 = [y for x in _x_15359 if (y := _f_15355(x)) is not None]
        return _x_15360

# Lean: Corpus.Games.Nim.create
def nim_create(sizes: list[int]) -> Nim:
    _x_15365 = Nim_mk(sizes)
    return _x_15365

# Lean: Corpus.Games.Nim.take
def nim_take(g_906: Nim, pile: int, count_907: int) -> Nim | None:
    def _f_15405(n_908: int):
        def _f_15368():
            _x_15367 = False
            return False
        _alt_15369 = _f_15368
        def _f_15372():
            _x_15370 = count_907 <= n_908
            return _x_15370
        _alt_15373 = _f_15372
        _x_15374 = 0
        _x_15377 = 0 < count_907
        def _jp_15398(_y_15383: bool):
            _x_15384 = True
            if _y_15383:
                _x_15389 = g_906.nim_0
                _x_15393 = n_908 - count_907
                _x_15394 = _x_15389[:pile] + [_x_15393] + _x_15389[pile+1:]
                _x_15395 = Nim_mk(_x_15394)
                _x_15396 = _x_15395
                return _x_15396
            else:
                _x_15387 = None
                return _x_15387
        def _jp_15404():
            _x_15403 = _alt_15373()
            return _jp_15398(_x_15403)
        def _jp_15401():
            _x_15400 = _alt_15369()
            return _jp_15398(_x_15400)
        if _x_15377:
            return _jp_15404()
        else:
            return _jp_15401()
    _alt_15406 = _f_15405
    def _f_15408():
        _x_15407 = None
        return _x_15407
    _alt_15409 = _f_15408
    def _f_15413(xs_912: list[int], i_913: int):
        _x_15411 = len(xs_912)
        _x_15412 = i_913 < _x_15411
        return _x_15412
    _x_15415 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_15416 = g_906.nim_0
    _x_15417 = _x_15415(_x_15416, pile)
    if _x_15417 is None:
        _x_15419 = _alt_15409()
        return _x_15419
    else:
        val_15420 = _x_15417
        _x_15421 = _alt_15406(val_15420)
        return _x_15421

# Lean: Corpus.Games.Nim.isOver
def nim_is_over(g_914: Nim) -> bool:
    _x_15424 = g_914.nim_0
    def _f_15432(x_15425: int):
        _x_15428 = 0
        _x_15431 = x_15425 == 0
        return _x_15431
    _x_15433 = all(_f_15432(x) for x in _x_15424)
    return _x_15433

# Lean: Corpus.Games.Nim.nimSum
def nim_sum(g_915: Nim) -> int:
    _x_15435 = (lambda a, b: a ^ b)
    _x_15436 = 0
    _x_15439 = g_915.nim_0
    _x_15440 = functools.reduce(_x_15435, _x_15439, 0)
    return _x_15440

# Lean: Corpus.Games.Nim.isWinningPosition
def is_winning_position(g_916: Nim) -> bool:
    _x_15443 = nim_sum(g_916)
    _x_15444 = 0
    _x_15447 = (lambda a, b: a != b)(0)
    return _x_15447

# Lean: Corpus.Games.Card.value
def value(c_917: Card) -> int:
    def _f_15452():
        _x_15449 = 11
        return 11
    _alt_15453 = _f_15452
    def _f_15457():
        _x_15454 = 2
        return 2
    _alt_15458 = _f_15457
    def _f_15462():
        _x_15459 = 3
        return 3
    _alt_15463 = _f_15462
    def _f_15467():
        _x_15464 = 4
        return 4
    _alt_15468 = _f_15467
    def _f_15472():
        _x_15469 = 5
        return 5
    _alt_15473 = _f_15472
    def _f_15477():
        _x_15474 = 6
        return 6
    _alt_15478 = _f_15477
    def _f_15482():
        _x_15479 = 7
        return 7
    _alt_15483 = _f_15482
    def _f_15487():
        _x_15484 = 8
        return 8
    _alt_15488 = _f_15487
    def _f_15492():
        _x_15489 = 9
        return 9
    _alt_15493 = _f_15492
    def _f_15497():
        _x_15494 = 10
        return 10
    _alt_15498 = _f_15497
    _alt_15499 = _f_15497
    _alt_15500 = _f_15497
    _alt_15501 = _f_15497
    _x_15502 = c_917.card_0
    match _x_15502:
        case ace():
            _x_15504 = _alt_15453()
            return _x_15504
        case two():
            _x_15506 = _alt_15458()
            return _x_15506
        case three():
            _x_15508 = _alt_15463()
            return _x_15508
        case four():
            _x_15510 = _alt_15468()
            return _x_15510
        case five():
            _x_15512 = _alt_15473()
            return _x_15512
        case six():
            _x_15514 = _alt_15478()
            return _x_15514
        case seven():
            _x_15516 = _alt_15483()
            return _x_15516
        case eight():
            _x_15518 = _alt_15488()
            return _x_15518
        case nine():
            _x_15520 = _alt_15493()
            return _x_15520
        case ten():
            _x_15522 = _alt_15498()
            return _x_15522
        case jack():
            _x_15524 = _alt_15499()
            return _x_15524
        case queen():
            _x_15526 = _alt_15500()
            return _x_15526
        case king():
            _x_15528 = _alt_15501()
            return _x_15528

# Lean: Corpus.Games.Card.isAce
def is_ace(c_928: Card) -> bool:
    _x_15533 = c_928.card_0
    _x_15534 = ace()
    _x_15535 = _x_15533 == _x_15534
    return _x_15535

# Lean: Corpus.Games.BlackjackHand.empty
def blackjack_hand_empty() -> BlackjackHand:
    _x_15537 = []
    _x_15538 = BlackjackHand_mk(_x_15537)
    return _x_15538

# Lean: Corpus.Games.BlackjackHand.add
def add(h_929: BlackjackHand, c_930: Card) -> BlackjackHand:
    _x_15539 = h_929.blackjack_hand_0
    _x_15540 = [c_930] + _x_15539
    _x_15541 = BlackjackHand_mk(_x_15540)
    return _x_15541

# Lean: Corpus.Games.BlackjackHand.hardValue
def hard_value(h_931: BlackjackHand) -> int:
    def _f_15548(acc_932: int, c_933: Card):
        _x_15546 = value(c_933)
        _x_15547 = acc_932 + _x_15546
        return _x_15547
    _x_15549 = 0
    _x_15552 = h_931.blackjack_hand_0
    _x_15553 = functools.reduce(_f_15548, _x_15552, 0)
    return _x_15553

# Lean: Corpus.Games.BlackjackHand.numAces
def num_aces(h_934: BlackjackHand) -> int:
    _x_15555 = is_ace()
    _x_15556 = h_934.blackjack_hand_0
    _x_15557 = [x for x in _x_15556 if _x_15555(x)]
    _x_15558 = len(_x_15557)
    return _x_15558

# Lean: Corpus.Games.BlackjackHand.bestValue
def best_value(h_935: BlackjackHand) -> int:
    _x_15560 = hard_value(h_935)
    _x_15561 = num_aces(h_935)
    _x_15562 = best_value_adjust(_x_15560, _x_15561)
    return _x_15562

# Lean: Corpus.Games.BlackjackHand.isBust
def is_bust(h_936: BlackjackHand) -> bool:
    _x_15564 = 21
    _x_15567 = best_value(h_936)
    _x_15568 = 21 < _x_15567
    return _x_15568

# Lean: Corpus.Games.BlackjackHand.isBlackjack
def is_blackjack(h_937: BlackjackHand) -> bool:
    def _f_15572():
        _x_15571 = False
        return False
    _alt_15573 = _f_15572
    def _f_15581():
        _x_15576 = best_value(h_937)
        _x_15577 = 21
        _x_15580 = _x_15576 == 21
        return _x_15580
    _alt_15582 = _f_15581
    _x_15585 = h_937.blackjack_hand_0
    _x_15586 = len(_x_15585)
    _x_15587 = 2
    _x_15590 = _x_15586 == 2
    if _x_15590:
        _x_15594 = _alt_15582()
        return _x_15594
    else:
        _x_15592 = _alt_15573()
        return _x_15592

# Lean: Corpus.Games.roll
def roll(sides_940: int, seed_941: int) -> int:
    _x_15606 = 1103515245
    _x_15609 = seed_941 * 1103515245
    _x_15610 = 12345
    _x_15613 = _x_15609 + 12345
    _x_15618 = 2
    _x_15621 = 31
    _x_15624 = 2 ** 31
    _x_15625 = _x_15613 % _x_15624
    _x_15626 = _x_15625 % sides_940
    _x_15627 = 1
    _x_15630 = _x_15626 + 1
    return _x_15630

# Lean: Corpus.Games.rollDice
def roll_dice(num_dice: int, sides_942: int, seed_943: int) -> tuple[list[int], int]:
    _x_15632 = []
    _x_15633 = roll_dice_go(sides_942, num_dice, seed_943, _x_15632)
    return _x_15633

# Lean: Corpus.Games.sumDice
def sum_dice(dice: list[int]) -> int:
    def _f_15641(x1_15635: int, x2_15636: int):
        _x_15640 = x1_15635 + x2_15636
        return _x_15640
    _x_15642 = 0
    _x_15645 = functools.reduce(_f_15641, dice, 0)
    return _x_15645

# Lean: Corpus.Games.yahtzeeScore
def yahtzee_score(dice_944: list[int]) -> int:
    _x_15648 = len(dice_944)
    _x_15649 = 5
    _x_15652 = (lambda a, b: a != b)(5)
    _x_15653 = True
    if _x_15652:
        _x_15797 = 0
        return 0
    else:
        _x_15656 = list(dice_944)
        def _f_15661(x1_15657: int, x2_15658: int):
            _x_15659 = x1_15657 < x2_15658
            return _x_15659
        _x_15662 = 0
        _x_15668 = len(_x_15656)
        _x_15669 = 1
        _x_15672 = _x_15668 - 1
        _x_15673 = sorted(0, key=functools.cmp_to_key(lambda a, b: -1 if _x_15672(a, b) else 1))
        _x_15674 = list(_x_15673)
        def _f_15685(n_946: int):
            def _f_15682(x_15675: int):
                _x_15680 = n_946 + 1
                _x_15681 = x_15675 == _x_15680
                return _x_15681
            _x_15683 = [x for x in dice_944 if _f_15682(x)]
            _x_15684 = len(_x_15683)
            return _x_15684
        _x_15686 = 6
        _x_15689 = list(range(6))
        _x_15690 = [_f_15685(x) for x in _x_15689]
        _x_15692 = max
        _x_15693 = functools.reduce(_x_15692, _x_15690, 0)
        def _f_15700(x1_15694: int, x2_15695: int):
            _x_15699 = x1_15694 + x2_15695
            return _x_15699
        _x_15701 = functools.reduce(_f_15700, dice_944, 0)
        _x_15703 = _x_15693 == 5
        if _x_15703:
            _x_15792 = 50
            return 50
        else:
            def _f_15706():
                return True
            _alt_15707 = _f_15706
            def _f_15726():
                _x_15710 = 2
                _x_15713 = 3
                _x_15716 = 4
                _x_15719 = []
                _x_15720 = [6] + _x_15719
                _x_15721 = [5] + _x_15720
                _x_15722 = [4] + _x_15721
                _x_15723 = [3] + _x_15722
                _x_15724 = [2] + _x_15723
                _x_15725 = _x_15674 == _x_15724
                return _x_15725
            _alt_15727 = _f_15726
            _x_15730 = 2
            _x_15733 = 3
            _x_15736 = 4
            _x_15739 = []
            _x_15740 = [5] + _x_15739
            _x_15741 = [4] + _x_15740
            _x_15742 = [3] + _x_15741
            _x_15743 = [2] + _x_15742
            _x_15744 = [1] + _x_15743
            _x_15745 = _x_15674 == _x_15744
            def _jp_15784(_y_15750: bool):
                if _y_15750:
                    _x_15780 = 40
                    return 40
                else:
                    def _f_15754():
                        _x_15753 = False
                        return False
                    _alt_15755 = _f_15754
                    def _f_15757():
                        _x_15756 = 2 in _x_15690
                        return _x_15756
                    _alt_15758 = _f_15757
                    _x_15759 = 3 in _x_15690
                    def _jp_15772(_y_15764: bool):
                        if _y_15764:
                            _x_15768 = 25
                            return 25
                        else:
                            return _x_15701
                    def _jp_15775():
                        _x_15774 = _alt_15755()
                        return _jp_15772(_x_15774)
                    def _jp_15778():
                        _x_15777 = _alt_15758()
                        return _jp_15772(_x_15777)
                    if _x_15759:
                        return _jp_15778()
                    else:
                        return _jp_15775()
            def _jp_15790():
                _x_15789 = _alt_15707()
                return _jp_15784(_x_15789)
            def _jp_15787():
                _x_15786 = _alt_15727()
                return _jp_15784(_x_15786)
            if _x_15745:
                return _jp_15790()
            else:
                return _jp_15787()

# Lean: Corpus.Games.RPS.beats
def beats(x_15802: RPS, x_15803: RPS) -> bool:
    def _f_15805():
        _x_15804 = True
        return True
    _alt_15806 = _f_15805
    _alt_15807 = _f_15805
    _alt_15808 = _f_15805
    def _f_15812(x_15809: RPS, x_15810: RPS):
        _x_15811 = False
        return False
    _alt_15813 = _f_15812
    match x_15802:
        case rock():
            match x_15803:
                case rock():
                    _x_15814 = rock()
                    _x_15815 = _alt_15813(_x_15814, _x_15814)
                    return _x_15815
                case paper():
                    _x_15816 = rock()
                    _x_15817 = paper()
                    _x_15818 = _alt_15813(_x_15816, _x_15817)
                    return _x_15818
                case scissors():
                    _x_15820 = _alt_15806()
                    return _x_15820
        case paper():
            match x_15803:
                case rock():
                    _x_15823 = _alt_15807()
                    return _x_15823
                case paper():
                    _x_15824 = paper()
                    _x_15825 = _alt_15813(_x_15824, _x_15824)
                    return _x_15825
                case scissors():
                    _x_15826 = paper()
                    _x_15827 = scissors()
                    _x_15828 = _alt_15813(_x_15826, _x_15827)
                    return _x_15828
        case scissors():
            match x_15803:
                case rock():
                    _x_15830 = scissors()
                    _x_15831 = rock()
                    _x_15832 = _alt_15813(_x_15830, _x_15831)
                    return _x_15832
                case paper():
                    _x_15834 = _alt_15808()
                    return _x_15834
                case scissors():
                    _x_15835 = scissors()
                    _x_15836 = _alt_15813(_x_15835, _x_15835)
                    return _x_15836

# Lean: Corpus.Games.RPS.compare
def compare(a_953: RPS, b_954: RPS) -> int:
    _x_15842 = a_953 == b_954
    _x_15843 = True
    if _x_15842:
        _x_15861 = 0
        return 0
    else:
        _x_15846 = beats(a_953, b_954)
        if _x_15846:
            _x_15856 = 1
            return 1
        else:
            _x_15851 = 1
            _x_15854 = -1
            return _x_15854

# Lean: Corpus.Games.RPS.fromNat
def from_nat(x_15866: int) -> RPS | None:
    def _f_15869():
        _x_15867 = rock()
        _x_15868 = _x_15867
        return _x_15868
    _alt_15870 = _f_15869
    def _f_15873():
        _x_15871 = paper()
        _x_15872 = _x_15871
        return _x_15872
    _alt_15874 = _f_15873
    def _f_15877():
        _x_15875 = scissors()
        _x_15876 = _x_15875
        return _x_15876
    _alt_15878 = _f_15877
    def _f_15881(x_15879: int):
        _x_15880 = None
        return _x_15880
    _alt_15882 = _f_15881
    _x_15883 = 0
    if x_15866:
        _x_15887 = 1
        if x_15866:
            _x_15891 = 2
            if x_15866:
                _x_15895 = _alt_15882(x_15866)
                return _x_15895
            else:
                def _f_15898(h_1: Any, h_2: Any):
                    _x_15897 = _alt_15878()
                    return _x_15897
                _x_15899 = _f_15898(None, None)
                return _x_15899
        else:
            def _f_15903(h_1_958: Any):
                _x_15902 = _alt_15874()
                return _x_15902
            _x_15904 = _f_15903(None)
            return _x_15904
    else:
        _x_15907 = _alt_15870()
        return _x_15907

# Lean: Corpus.Games.isValidSudokuRow
def is_valid_sudoku_row(row_959: list[int]) -> bool:
    def _f_15916(x_15910: int):
        _x_15912 = 0
        _x_15915 = (lambda a, b: a != b)(0)
        return _x_15915
    _x_15917 = [x for x in row_959 if _f_15916(x)]
    _x_15920 = len(_x_15917)
    _x_15921 = list(dict.fromkeys(_x_15917))
    _x_15922 = len(_x_15921)
    _x_15923 = _x_15920 == _x_15922
    return _x_15923

# Lean: Corpus.Games.isValidSudokuGrid
def is_valid_sudoku_grid(grid: list[list[int]]) -> bool:
    _x_15925 = is_valid_sudoku_row()
    _x_15926 = all(_x_15925(x) for x in grid)
    def _f_15936(c_960: int):
        def _f_15934(row_961: list[int]):
            def _f_15930(xs_962: list[int], i_963: int):
                _x_15928 = len(xs_962)
                _x_15929 = i_963 < _x_15928
                return _x_15929
            _x_15932 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_15933 = _x_15932(row_961, c_960)
            return _x_15933
        _x_15935 = [y for x in grid if (y := _f_15934(x)) is not None]
        return _x_15935
    _x_15937 = 9
    _x_15940 = list(range(9))
    _x_15941 = [_f_15936(x) for x in _x_15940]
    _x_15942 = all(_x_15925(x) for x in _x_15941)
    _x_15943 = 3
    _x_15946 = list(range(3))
    def _f_15993(br: int):
        def _f_15991(bc: int):
            def _f_15989(r_964: int):
                def _f_15987(c_965: int):
                    def _f_15962(row_966: list[int]):
                        def _f_15950(xs_967: list[int], i_968: int):
                            _x_15948 = len(xs_967)
                            _x_15949 = i_968 < _x_15948
                            return _x_15949
                        _x_15952 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                        _x_15959 = bc * 3
                        _x_15960 = _x_15959 + c_965
                        _x_15961 = _x_15952(row_966, _x_15960)
                        return _x_15961
                    _alt_15963 = _f_15962
                    def _f_15965():
                        _x_15964 = None
                        return _x_15964
                    _alt_15966 = _f_15965
                    def _f_15970(xs_970: list[list[int]], i_971: int):
                        _x_15968 = len(xs_970)
                        _x_15969 = i_971 < _x_15968
                        return _x_15969
                    _x_15972 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                    _x_15979 = br * 3
                    _x_15980 = _x_15979 + r_964
                    _x_15981 = _x_15972(grid, _x_15980)
                    if _x_15981 is None:
                        _x_15983 = _alt_15966()
                        return _x_15983
                    else:
                        val_15984 = _x_15981
                        _x_15985 = _alt_15963(val_15984)
                        return _x_15985
                _x_15988 = [y for x in _x_15946 if (y := _f_15987(x)) is not None]
                return _x_15988
            _x_15990 = [y for x in _x_15946 for y in _f_15989(x)]
            return _x_15990
        _x_15992 = [_f_15991(x) for x in _x_15946]
        return _x_15992
    _x_15994 = [y for x in _x_15946 for y in _f_15993(x)]
    _x_15995 = all(_x_15925(x) for x in _x_15994)
    def _f_15997():
        _x_15996 = False
        return False
    _alt_15998 = _f_15997
    def _f_15999():
        return _x_15995
    _alt_16000 = _f_15999
    _alt_16001 = _f_15997
    def _f_16002():
        return _x_15942
    _alt_16003 = _f_16002
    def _jp_16014(_y_16008: bool):
        if _y_16008:
            _x_16012 = _alt_16000()
            return _x_16012
        else:
            _x_16010 = _alt_15998()
            return _x_16010
    def _jp_16017():
        _x_16016 = _alt_16001()
        return _jp_16014(_x_16016)
    def _jp_16020():
        _x_16019 = _alt_16003()
        return _jp_16014(_x_16019)
    if _x_15926:
        return _jp_16020()
    else:
        return _jp_16017()

# Lean: Corpus.DataStructures.Stack.empty
def stack_empty(__975: Any) -> Any:
    _x_16022 = []
    _x_16023 = Stack_mk(None, _x_16022)
    return _x_16023

# Lean: Corpus.DataStructures.Stack.push
def stack_push(__976: Any, s_977: Any, x_978: Any) -> Any:
    _x_16025 = s_977.stack_0
    _x_16026 = [x_978] + _x_16025
    _x_16027 = Stack_mk(None, _x_16026)
    return _x_16027

# Lean: Corpus.DataStructures.Stack.pop
def pop(__979: Any, s_980: Any) -> tuple[Any, Any] | None:
    def _f_16030():
        _x_16029 = None
        return _x_16029
    _alt_16031 = _f_16030
    def _f_16035(x_982: Any, xs_983: list[Any]):
        _x_16032 = Stack_mk(None, xs_983)
        _x_16033 = (x_982, _x_16032)
        _x_16034 = _x_16033
        return _x_16034
    _alt_16036 = _f_16035
    _x_16037 = s_980.stack_0
    if len(_x_16037) == 0:
        _x_16039 = _alt_16031()
        return _x_16039
    else:
        head_16040 = _x_16037[0]
        tail_16041 = _x_16037[1:]
        _x_16042 = _alt_16036(head_16040, tail_16041)
        return _x_16042

# Lean: Corpus.DataStructures.Stack.peek
def peek(__984: Any, s_985: Any) -> Any | None:
    _x_16045 = s_985.stack_0
    _x_16046 = (lambda xs: xs[0] if xs else None)(_x_16045)
    return _x_16046

# Lean: Corpus.DataStructures.Stack.isEmpty
def stack_is_empty(__986: Any, s_987: Any) -> bool:
    _x_16048 = s_987.stack_0
    _x_16049 = len(_x_16048) == 0
    return _x_16049

# Lean: Corpus.DataStructures.Stack.size
def stack_size(__988: Any, s_989: Any) -> int:
    _x_16051 = s_989.stack_0
    _x_16052 = len(_x_16051)
    return _x_16052

# Lean: Corpus.DataStructures.Queue.empty
def queue_empty(__990: Any) -> Any:
    _x_16054 = []
    _x_16055 = Queue_mk(None, _x_16054, _x_16054)
    return _x_16055

# Lean: Corpus.DataStructures.Queue.enqueue
def enqueue(__991: Any, q_992: Any, x_993: Any) -> Any:
    _x_16057 = q_992.queue_0
    _x_16058 = q_992.queue_1
    _x_16059 = [x_993] + _x_16058
    _x_16060 = Queue_mk(None, _x_16057, _x_16059)
    return _x_16060

# Lean: Corpus.DataStructures.Queue.dequeue
def dequeue(__994: Any, q_995: Any) -> tuple[Any, Any] | None:
    def _f_16066(x_996: Any, xs_997: list[Any]):
        _x_16062 = q_995.queue_1
        _x_16063 = Queue_mk(None, xs_997, _x_16062)
        _x_16064 = (x_996, _x_16063)
        _x_16065 = _x_16064
        return _x_16065
    _alt_16067 = _f_16066
    def _f_16085():
        def _f_16069():
            _x_16068 = None
            return _x_16068
        _alt_16070 = _f_16069
        def _f_16075(x_1000: Any, xs_1001: list[Any]):
            _x_16071 = []
            _x_16072 = Queue_mk(None, xs_1001, _x_16071)
            _x_16073 = (x_1000, _x_16072)
            _x_16074 = _x_16073
            return _x_16074
        _alt_16076 = _f_16075
        _x_16077 = q_995.queue_1
        _x_16078 = list(reversed(_x_16077))
        if len(_x_16078) == 0:
            _x_16080 = _alt_16070()
            return _x_16080
        else:
            head_16081 = _x_16078[0]
            tail_16082 = _x_16078[1:]
            _x_16083 = _alt_16076(head_16081, tail_16082)
            return _x_16083
    _alt_16086 = _f_16085
    _x_16087 = q_995.queue_0
    if len(_x_16087) == 0:
        _x_16089 = _alt_16086()
        return _x_16089
    else:
        head_16090 = _x_16087[0]
        tail_16091 = _x_16087[1:]
        _x_16092 = _alt_16067(head_16090, tail_16091)
        return _x_16092

# Lean: Corpus.DataStructures.Queue.isEmpty
def queue_is_empty(__1002: Any, q_1003: Any) -> bool:
    def _f_16096():
        _x_16095 = False
        return False
    _alt_16097 = _f_16096
    def _f_16100():
        _x_16098 = q_1003.queue_1
        _x_16099 = len(_x_16098) == 0
        return _x_16099
    _alt_16101 = _f_16100
    _x_16102 = q_1003.queue_0
    _x_16103 = len(_x_16102) == 0
    if _x_16103:
        _x_16107 = _alt_16101()
        return _x_16107
    else:
        _x_16105 = _alt_16097()
        return _x_16105

# Lean: Corpus.DataStructures.Queue.size
def queue_size(__1006: Any, q_1007: Any) -> int:
    _x_16113 = q_1007.queue_0
    _x_16114 = len(_x_16113)
    _x_16115 = q_1007.queue_1
    _x_16116 = len(_x_16115)
    _x_16117 = _x_16114 + _x_16116
    return _x_16117

# Lean: Corpus.DataStructures.BinaryTree.singleton
def singleton(__1008: Any, x_1009: Any) -> Any:
    _x_16119 = BinaryTree_empty(None)
    _x_16120 = BinaryTree_node(None, x_1009, _x_16119, _x_16119)
    return _x_16120

# Lean: Corpus.DataStructures.BinaryTree.size
def binary_tree_size(__1010: Any, t_1011: Any) -> int:
    def _f_16125():
        _x_16122 = 0
        return 0
    _alt_16126 = _f_16125
    def _f_16138(a_16127: Any, l_1013: Any, r_1014: Any):
        _x_16131 = 1
        _x_16134 = binary_tree_size(None, l_1013)
        _x_16135 = 1 + _x_16134
        _x_16136 = binary_tree_size(None, r_1014)
        _x_16137 = _x_16135 + _x_16136
        return _x_16137
    _alt_16139 = _f_16138
    match t_1011:
        case BinaryTree_empty():
            _x_16141 = _alt_16126()
            return _x_16141
        case BinaryTree_node(a_16142, a_16143, a_16144):
            _x_16145 = _alt_16139(a_16142, a_16143, a_16144)
            return _x_16145

# Lean: Corpus.DataStructures.BinaryTree.height
def height(__1015: Any, t_1016: Any) -> int:
    def _f_16151():
        _x_16148 = 0
        return 0
    _alt_16152 = _f_16151
    def _f_16166(a_16153: Any, l_1018: Any, r_1019: Any):
        _x_16157 = 1
        _x_16161 = max
        _x_16162 = height(None, l_1018)
        _x_16163 = height(None, r_1019)
        _x_16164 = _x_16161(_x_16162, _x_16163)
        _x_16165 = 1 + _x_16164
        return _x_16165
    _alt_16167 = _f_16166
    match t_1016:
        case BinaryTree_empty():
            _x_16169 = _alt_16152()
            return _x_16169
        case BinaryTree_node(a_16170, a_16171, a_16172):
            _x_16173 = _alt_16167(a_16170, a_16171, a_16172)
            return _x_16173

# Lean: Corpus.DataStructures.BinaryTree.inorder
def inorder(__1020: Any, t_1021: Any) -> list[Any]:
    def _f_16177():
        _x_16176 = []
        return _x_16176
    _alt_16178 = _f_16177
    def _f_16188(v_1023: Any, l_1024: Any, r_1025: Any):
        _x_16182 = inorder(None, l_1024)
        _x_16183 = []
        _x_16184 = [v_1023] + _x_16183
        _x_16185 = _x_16182 + _x_16184
        _x_16186 = inorder(None, r_1025)
        _x_16187 = _x_16185 + _x_16186
        return _x_16187
    _alt_16189 = _f_16188
    match t_1021:
        case BinaryTree_empty():
            _x_16191 = _alt_16178()
            return _x_16191
        case BinaryTree_node(a_16192, a_16193, a_16194):
            _x_16195 = _alt_16189(a_16192, a_16193, a_16194)
            return _x_16195

# Lean: Corpus.DataStructures.BinaryTree.preorder
def preorder(__1026: Any, t_1027: Any) -> list[Any]:
    def _f_16199():
        _x_16198 = []
        return _x_16198
    _alt_16200 = _f_16199
    def _f_16210(v_1029: Any, l_1030: Any, r_1031: Any):
        _x_16204 = []
        _x_16205 = [v_1029] + _x_16204
        _x_16206 = preorder(None, l_1030)
        _x_16207 = _x_16205 + _x_16206
        _x_16208 = preorder(None, r_1031)
        _x_16209 = _x_16207 + _x_16208
        return _x_16209
    _alt_16211 = _f_16210
    match t_1027:
        case BinaryTree_empty():
            _x_16213 = _alt_16200()
            return _x_16213
        case BinaryTree_node(a_16214, a_16215, a_16216):
            _x_16217 = _alt_16211(a_16214, a_16215, a_16216)
            return _x_16217

# Lean: Corpus.DataStructures.BinaryTree.postorder
def postorder(__1032: Any, t_1033: Any) -> list[Any]:
    def _f_16221():
        _x_16220 = []
        return _x_16220
    _alt_16222 = _f_16221
    def _f_16232(v_1035: Any, l_1036: Any, r_1037: Any):
        _x_16226 = postorder(None, l_1036)
        _x_16227 = postorder(None, r_1037)
        _x_16228 = _x_16226 + _x_16227
        _x_16229 = []
        _x_16230 = [v_1035] + _x_16229
        _x_16231 = _x_16228 + _x_16230
        return _x_16231
    _alt_16233 = _f_16232
    match t_1033:
        case BinaryTree_empty():
            _x_16235 = _alt_16222()
            return _x_16235
        case BinaryTree_node(a_16236, a_16237, a_16238):
            _x_16239 = _alt_16233(a_16236, a_16237, a_16238)
            return _x_16239

# Lean: Corpus.DataStructures.BinaryTree.levelOrder
def level_order(__1038: Any, t_1039: Any) -> list[Any]:
    _x_16242 = []
    _x_16243 = [t_1039] + _x_16242
    _x_16244 = []
    _x_16245 = 10000
    _x_16248 = level_order_go(None, _x_16243, _x_16244, 10000)
    return _x_16248

# Lean: Corpus.DataStructures.BinaryTree.mirror
def mirror(__1040: Any, t_1041: Any) -> Any:
    def _f_16251():
        _x_16250 = BinaryTree_empty(None)
        return _x_16250
    _alt_16252 = _f_16251
    def _f_16256(v_1043: Any, l_1044: Any, r_1045: Any):
        _x_16253 = mirror(None, r_1045)
        _x_16254 = mirror(None, l_1044)
        _x_16255 = BinaryTree_node(None, v_1043, _x_16253, _x_16254)
        return _x_16255
    _alt_16257 = _f_16256
    match t_1041:
        case BinaryTree_empty():
            _x_16259 = _alt_16252()
            return _x_16259
        case BinaryTree_node(a_16260, a_16261, a_16262):
            _x_16263 = _alt_16257(a_16260, a_16261, a_16262)
            return _x_16263

# Lean: Corpus.DataStructures.BinaryTree.map
def binary_tree_map(__1046: Any, __1047: Any, f_1048: Callable[[Any], Any], t_1049: Any) -> Any:
    def _f_16267():
        _x_16266 = BinaryTree_empty(None)
        return _x_16266
    _alt_16268 = _f_16267
    def _f_16273(v_1051: Any, l_1052: Any, r_1053: Any):
        _x_16269 = f_1048(v_1051)
        _x_16270 = binary_tree_map(None, None, f_1048, l_1052)
        _x_16271 = binary_tree_map(None, None, f_1048, r_1053)
        _x_16272 = BinaryTree_node(None, _x_16269, _x_16270, _x_16271)
        return _x_16272
    _alt_16274 = _f_16273
    match t_1049:
        case BinaryTree_empty():
            _x_16276 = _alt_16268()
            return _x_16276
        case BinaryTree_node(a_16277, a_16278, a_16279):
            _x_16280 = _alt_16274(a_16277, a_16278, a_16279)
            return _x_16280

# Lean: Corpus.DataStructures.BinaryTree.fold
def binary_tree_fold(__1054: Any, __1055: Any, f_1056: Callable[[Any, Any], Any], init_1057: Any, t_1058: Any) -> Any:
    def _f_16283():
        return init_1057
    _alt_16284 = _f_16283
    def _f_16288(v_1060: Any, l_1061: Any, r_1062: Any):
        _x_16285 = binary_tree_fold(None, None, f_1056, init_1057, l_1061)
        _x_16286 = f_1056(_x_16285, v_1060)
        _x_16287 = binary_tree_fold(None, None, f_1056, _x_16286, r_1062)
        return _x_16287
    _alt_16289 = _f_16288
    match t_1058:
        case BinaryTree_empty():
            _x_16291 = _alt_16284()
            return _x_16291
        case BinaryTree_node(a_16292, a_16293, a_16294):
            _x_16295 = _alt_16289(a_16292, a_16293, a_16294)
            return _x_16295

# Lean: Corpus.DataStructures.AssocList.empty
def assoc_list_empty(__1063: Any, __1064: Any) -> list[tuple[Any, Any]]:
    _x_16298 = []
    return _x_16298

# Lean: Corpus.DataStructures.AssocList.insert
def assoc_list_insert(__1065: Any, __1066: Any, inst_16300: Any, m_1067: list[tuple[Any, Any]], k_1068: Any, v_1069: Any) -> list[tuple[Any, Any]]:
    _x_16301 = (k_1068, v_1069)
    def _f_16311(x_16302: tuple[Any, Any]):
        def _f_16305(k__1070: Any, snd_16303: Any):
            _x_16304 = (lambda a, b: a != b)(k_1068)
            return _x_16304
        _alt_16306 = _f_16305
        match x_16302:
            case (fst_16307, snd_16308):
                _x_16309 = _alt_16306(fst_16307, snd_16308)
                return _x_16309
    _x_16312 = [x for x in m_1067 if _f_16311(x)]
    _x_16313 = [_x_16301] + _x_16312
    return _x_16313

# Lean: Corpus.DataStructures.AssocList.lookup
def lookup(__1071: Any, __1072: Any, inst_16315: Any, m_1073: list[tuple[Any, Any]], k_1074: Any) -> Any | None:
    def _f_16317():
        _x_16316 = None
        return _x_16316
    _alt_16318 = _f_16317
    def _f_16328(k__1076: Any, v_1077: Any, rest_1078: list[tuple[Any, Any]]):
        _x_16319 = inst_16315.beq_0
        _x_16320 = _x_16319(k_1074, k__1076)
        _x_16321 = True
        if _x_16320:
            _x_16326 = v_1077
            return _x_16326
        else:
            _x_16324 = lookup(None, None, inst_16315, k_1074, rest_1078)
            return _x_16324
    _alt_16329 = _f_16328
    if len(m_1073) == 0:
        _x_16331 = _alt_16318()
        return _x_16331
    else:
        head_16332 = m_1073[0]
        tail_16333 = m_1073[1:]
        match head_16332:
            case (fst_16334, snd_16335):
                _x_16336 = _alt_16329(fst_16334, snd_16335, tail_16333)
                return _x_16336

# Lean: Corpus.DataStructures.AssocList.remove
def remove(__1079: Any, __1080: Any, inst_16340: Any, m_1081: list[tuple[Any, Any]], k_1082: Any) -> list[tuple[Any, Any]]:
    def _f_16350(x_16341: tuple[Any, Any]):
        def _f_16344(k__1083: Any, snd_16342: Any):
            _x_16343 = (lambda a, b: a != b)(k_1082)
            return _x_16343
        _alt_16345 = _f_16344
        match x_16341:
            case (fst_16346, snd_16347):
                _x_16348 = _alt_16345(fst_16346, snd_16347)
                return _x_16348
    _x_16351 = [x for x in m_1081 if _f_16350(x)]
    return _x_16351

# Lean: Corpus.DataStructures.AssocList.keys
def keys(__1084: Any, __1085: Any, m_1086: list[tuple[Any, Any]]) -> list[Any]:
    def _f_16354(self: tuple[Any, Any]):
        _x_16353 = self[0]
        return _x_16353
    _x_16355 = [_f_16354(x) for x in m_1086]
    return _x_16355

# Lean: Corpus.DataStructures.AssocList.values
def values(__1087: Any, __1088: Any, m_1089: list[tuple[Any, Any]]) -> list[Any]:
    def _f_16358(self_1090: tuple[Any, Any]):
        _x_16357 = self_1090[1]
        return _x_16357
    _x_16359 = [_f_16358(x) for x in m_1089]
    return _x_16359

# Lean: Corpus.DataStructures.AssocList.size
def assoc_list_size(__1091: Any, __1092: Any, m_1093: list[tuple[Any, Any]]) -> int:
    _x_16361 = len(m_1093)
    return _x_16361

# Lean: Corpus.DataStructures.Graph.empty
def data_structures_graph_empty(__1094: Any) -> Any:
    _x_16363 = []
    _x_16364 = []
    _x_16365 = Graph_mk(None, _x_16363, _x_16364)
    return _x_16365

# Lean: Corpus.DataStructures.Graph.addVertex
def data_structures_graph_add_vertex(__1095: Any, inst_16367: Any, g_1096: Any, v_1097: Any) -> Any:
    _x_16368 = g_1096.data_structures_graph_0
    _x_16369 = v_1097 in _x_16368
    _x_16370 = True
    if _x_16369:
        return g_1096
    else:
        _x_16373 = [v_1097] + _x_16368
        _x_16374 = g_1096.data_structures_graph_1
        _x_16375 = Graph_mk(None, _x_16373, _x_16374)
        return _x_16375

# Lean: Corpus.DataStructures.Graph.addEdge
def data_structures_graph_add_edge(__1098: Any, inst_16379: Any, g_1099: Any, u: Any, v_1100: Any) -> Any:
    _x_16380 = data_structures_graph_add_vertex(None, inst_16379, g_1099, u)
    _x_16381 = data_structures_graph_add_vertex(None, inst_16379, _x_16380, v_1100)
    _x_16382 = _x_16381.data_structures_graph_0
    _x_16383 = (u, v_1100)
    _x_16384 = _x_16381.data_structures_graph_1
    _x_16385 = [_x_16383] + _x_16384
    _x_16386 = Graph_mk(None, _x_16382, _x_16385)
    return _x_16386

# Lean: Corpus.DataStructures.Graph.neighbors
def data_structures_graph_neighbors(__1101: Any, inst_16388: Any, g_1102: Any, v_1103: Any) -> list[Any]:
    def _f_16411(x_16389: tuple[Any, Any]):
        def _f_16405(u_1104: Any, w_1105: Any):
            _x_16390 = inst_16388.beq_0
            _x_16391 = _x_16390(u_1104, v_1103)
            _x_16392 = True
            if _x_16391:
                _x_16403 = w_1105
                return _x_16403
            else:
                _x_16395 = _x_16390(w_1105, v_1103)
                if _x_16395:
                    _x_16400 = u_1104
                    return _x_16400
                else:
                    _x_16398 = None
                    return _x_16398
        _alt_16406 = _f_16405
        match x_16389:
            case (fst_16407, snd_16408):
                _x_16409 = _alt_16406(fst_16407, snd_16408)
                return _x_16409
    _x_16412 = g_1102.data_structures_graph_1
    _x_16413 = [y for x in _x_16412 if (y := _f_16411(x)) is not None]
    return _x_16413

# Lean: Corpus.DataStructures.Graph.degree
def degree(__1106: Any, inst_16415: Any, g_1107: Any, v_1108: Any) -> int:
    _x_16416 = data_structures_graph_neighbors(None, inst_16415, g_1107, v_1108)
    _x_16417 = len(_x_16416)
    return _x_16417

# Lean: Corpus.DataStructures.Graph.hasEdge
def has_edge(__1109: Any, inst_16419: Any, g_1110: Any, u_1111: Any, v_1112: Any) -> bool:
    _x_16420 = g_1110.data_structures_graph_1
    def _f_16473(x_16421: tuple[Any, Any]):
        def _f_16467(a_1113: Any, b_1114: Any):
            def _f_16423():
                _x_16422 = True
                return True
            _alt_16424 = _f_16423
            def _f_16439():
                def _f_16426():
                    _x_16425 = False
                    return False
                _alt_16427 = _f_16426
                def _f_16430():
                    _x_16428 = inst_16419.beq_0
                    _x_16429 = _x_16428(b_1114, u_1111)
                    return _x_16429
                _alt_16431 = _f_16430
                _x_16432 = inst_16419.beq_0
                _x_16433 = _x_16432(a_1113, v_1112)
                if _x_16433:
                    _x_16437 = _alt_16431()
                    return _x_16437
                else:
                    _x_16435 = _alt_16427()
                    return _x_16435
            _alt_16440 = _f_16439
            def _f_16442():
                _x_16441 = False
                return False
            _alt_16443 = _f_16442
            def _f_16446():
                _x_16444 = inst_16419.beq_0
                _x_16445 = _x_16444(b_1114, v_1112)
                return _x_16445
            _alt_16447 = _f_16446
            _x_16448 = inst_16419.beq_0
            _x_16449 = _x_16448(a_1113, u_1111)
            def _jp_16460(_y_16454: bool):
                if _y_16454:
                    _x_16458 = _alt_16424()
                    return _x_16458
                else:
                    _x_16456 = _alt_16440()
                    return _x_16456
            def _jp_16463():
                _x_16462 = _alt_16443()
                return _jp_16460(_x_16462)
            def _jp_16466():
                _x_16465 = _alt_16447()
                return _jp_16460(_x_16465)
            if _x_16449:
                return _jp_16466()
            else:
                return _jp_16463()
        _alt_16468 = _f_16467
        match x_16421:
            case (fst_16469, snd_16470):
                _x_16471 = _alt_16468(fst_16469, snd_16470)
                return _x_16471
    _x_16474 = any(_f_16473(x) for x in _x_16420)
    return _x_16474

# Lean: Corpus.DataStructures.Trie.empty
def trie_empty() -> Trie:
    _x_16476 = False
    _x_16477 = []
    _x_16478 = Trie_node(False, _x_16477)
    return _x_16478

# Lean: Corpus.DataStructures.Trie.insert
def trie_insert(t_1121: Trie, s_1122: str) -> Trie:
    _x_16479 = list(s_1122)
    _x_16480 = trie_insert_go(t_1121, _x_16479)
    return _x_16480

# Lean: Corpus.DataStructures.Trie.contains
def trie_contains(t_1123: Trie, s_1124: str) -> bool:
    _x_16482 = list(s_1124)
    _x_16483 = trie_contains_go(t_1123, _x_16482)
    return _x_16483

# Lean: Corpus.DataStructures.Trie.hasPrefix
def has_prefix(t_1125: Trie, pfx_1126: str) -> bool:
    _x_16485 = list(pfx_1126)
    _x_16486 = has_prefix_go(t_1125, _x_16485)
    return _x_16486

# Lean: Corpus.Advanced.Heap.empty
def advanced_heap_empty(__1127: Any) -> Any:
    _x_16488 = []
    _x_16489 = Heap_mk(None, _x_16488)
    return _x_16489

# Lean: Corpus.Advanced.Heap.isEmpty
def advanced_heap_is_empty(__1128: Any, h_1129: Any) -> bool:
    _x_16491 = h_1129.heap_0
    _x_16492 = len(_x_16491) == 0
    return _x_16492

# Lean: Corpus.Advanced.Heap.size
def advanced_heap_size(__1130: Any, h_1131: Any) -> int:
    _x_16494 = h_1131.heap_0
    _x_16495 = len(_x_16494)
    return _x_16495

# Lean: Corpus.Advanced.parent
def parent(i_1132: int) -> int:
    _x_16503 = 1
    _x_16506 = i_1132 - 1
    _x_16507 = 2
    _x_16510 = _x_16506 // 2
    return _x_16510

# Lean: Corpus.Advanced.leftChild
def left_child(i_1133: int) -> int:
    _x_16518 = 2
    _x_16521 = 2 * i_1133
    _x_16522 = 1
    _x_16525 = _x_16521 + 1
    return _x_16525

# Lean: Corpus.Advanced.rightChild
def right_child(i_1134: int) -> int:
    _x_16533 = 2
    _x_16536 = 2 * i_1134
    _x_16537 = _x_16536 + 2
    return _x_16537

# Lean: Corpus.Advanced.swapAt
def swap_at(__1135: Any, xs_1136: list[Any], i_1137: int, j_1138: int) -> list[Any]:
    def _f_16541(a_1139: Any, b_1140: Any):
        _x_16539 = xs_1136[:i_1137] + [b_1140] + xs_1136[i_1137+1:]
        _x_16540 = _x_16539[:j_1138] + [a_1139] + _x_16539[j_1138+1:]
        return _x_16540
    _alt_16542 = _f_16541
    def _f_16545(x_16543: Any | None, x_16544: Any | None):
        return xs_1136
    _alt_16546 = _f_16545
    _x_16547 = xs_1136[i_1137] if 0 <= i_1137 < len(xs_1136) else None
    if _x_16547 is None:
        _x_16548 = None
        _x_16549 = xs_1136[j_1138] if 0 <= j_1138 < len(xs_1136) else None
        _x_16550 = _alt_16546(_x_16548, _x_16549)
        return _x_16550
    else:
        val_16551 = _x_16547
        _x_16552 = xs_1136[j_1138] if 0 <= j_1138 < len(xs_1136) else None
        if _x_16552 is None:
            _x_16553 = val_16551
            _x_16554 = None
            _x_16555 = _alt_16546(_x_16553, _x_16554)
            return _x_16555
        else:
            val_16556 = _x_16552
            _x_16557 = _alt_16542(val_16551, val_16556)
            return _x_16557

# Lean: Corpus.Advanced.siftUp
def sift_up(__1141: Any, inst_16561: Any, xs_1142: list[Any], i_1143: int) -> list[Any]:
    _x_16564 = 0
    _x_16567 = i_1143 == 0
    _x_16568 = True
    if _x_16567:
        return xs_1142
    else:
        _x_16571 = parent(i_1143)
        def _f_16584(vi: Any, vp: Any):
            _x_16574 = inst_16561.ord_0
            _x_16575 = _x_16574(vi, vp)
            _x_16576 = -1
            _x_16577 = _x_16575 == _x_16576
            if _x_16577:
                _x_16581 = swap_at(None, xs_1142, i_1143, _x_16571)
                _x_16582 = sift_up(None, inst_16561, _x_16581, _x_16571)
                return _x_16582
            else:
                return xs_1142
        _alt_16585 = _f_16584
        def _f_16588(x_16586: Any | None, x_16587: Any | None):
            return xs_1142
        _alt_16589 = _f_16588
        _x_16590 = xs_1142[i_1143] if 0 <= i_1143 < len(xs_1142) else None
        if _x_16590 is None:
            _x_16591 = None
            _x_16592 = xs_1142[_x_16571] if 0 <= _x_16571 < len(xs_1142) else None
            _x_16593 = _alt_16589(_x_16591, _x_16592)
            return _x_16593
        else:
            val_16594 = _x_16590
            _x_16595 = xs_1142[_x_16571] if 0 <= _x_16571 < len(xs_1142) else None
            if _x_16595 is None:
                _x_16596 = val_16594
                _x_16597 = None
                _x_16598 = _alt_16589(_x_16596, _x_16597)
                return _x_16598
            else:
                val_16599 = _x_16595
                _x_16600 = _alt_16585(val_16594, val_16599)
                return _x_16600

# Lean: Corpus.Advanced.siftDown
def sift_down(__1145: Any, inst_16606: Any, xs_1146: list[Any], i_1147: int) -> list[Any]:
    _x_16607 = len(xs_1146)
    _x_16608 = left_child(i_1147)
    _x_16609 = right_child(i_1147)
    _x_16610 = _x_16607 <= _x_16608
    if _x_16610:
        return xs_1146
    else:
        _x_16612 = _x_16607 <= _x_16609
        def _jp_16678(_y_16645: int):
            def _f_16659(vi_1151: Any, vs_1152: Any):
                _x_16648 = inst_16606.ord_0
                _x_16649 = _x_16648(vs_1152, vi_1151)
                _x_16650 = -1
                _x_16651 = _x_16649 == _x_16650
                _x_16652 = True
                if _x_16651:
                    _x_16656 = swap_at(None, xs_1146, i_1147, _y_16645)
                    _x_16657 = sift_down(None, inst_16606, _x_16656, _y_16645)
                    return _x_16657
                else:
                    return xs_1146
            _alt_16660 = _f_16659
            def _f_16663(x_16661: Any | None, x_16662: Any | None):
                return xs_1146
            _alt_16664 = _f_16663
            _x_16665 = xs_1146[i_1147] if 0 <= i_1147 < len(xs_1146) else None
            if _x_16665 is None:
                _x_16666 = None
                _x_16667 = xs_1146[_y_16645] if 0 <= _y_16645 < len(xs_1146) else None
                _x_16668 = _alt_16664(_x_16666, _x_16667)
                return _x_16668
            else:
                val_16669 = _x_16665
                _x_16670 = xs_1146[_y_16645] if 0 <= _y_16645 < len(xs_1146) else None
                if _x_16670 is None:
                    _x_16671 = val_16669
                    _x_16672 = None
                    _x_16673 = _alt_16664(_x_16671, _x_16672)
                    return _x_16673
                else:
                    val_16674 = _x_16670
                    _x_16675 = _alt_16660(val_16669, val_16674)
                    return _x_16675
        if _x_16612:
            return _jp_16678(_x_16608)
        else:
            def _f_16625(vl: Any, vr: Any):
                _x_16616 = inst_16606.ord_0
                _x_16617 = _x_16616(vl, vr)
                _x_16618 = -1
                _x_16619 = _x_16617 == _x_16618
                _x_16620 = True
                if _x_16619:
                    return _x_16608
                else:
                    return _x_16609
            _alt_16626 = _f_16625
            def _jp_16686(_y_16683: Any, _y_16684: Any):
                _x_16685 = _alt_16626(_y_16683, _y_16684)
                return _jp_16678(_x_16685)
            def _f_16629(x_16627: Any | None, x_16628: Any | None):
                return _x_16608
            _alt_16630 = _f_16629
            def _jp_16682(_y_16679: Any | None, _y_16680: Any | None):
                _x_16681 = _alt_16630(_y_16679, _y_16680)
                return _jp_16678(_x_16681)
            _x_16631 = xs_1146[_x_16608] if 0 <= _x_16608 < len(xs_1146) else None
            if _x_16631 is None:
                _x_16632 = None
                _x_16633 = xs_1146[_x_16609] if 0 <= _x_16609 < len(xs_1146) else None
                return _jp_16682(_x_16632, _x_16633)
            else:
                val_16635 = _x_16631
                _x_16636 = xs_1146[_x_16609] if 0 <= _x_16609 < len(xs_1146) else None
                if _x_16636 is None:
                    _x_16637 = val_16635
                    _x_16638 = None
                    return _jp_16682(_x_16637, _x_16638)
                else:
                    val_16640 = _x_16636
                    return _jp_16686(val_16635, val_16640)

# Lean: Corpus.Advanced.Heap.insert
def advanced_heap_insert(__1153: Any, inst_16690: Any, h_1154: Any, x_1155: Any) -> Any:
    _x_16694 = h_1154.heap_0
    _x_16695 = []
    _x_16696 = [x_1155] + _x_16695
    _x_16697 = _x_16694 + _x_16696
    _x_16701 = len(_x_16697)
    _x_16702 = 1
    _x_16705 = _x_16701 - 1
    _x_16706 = sift_up(None, inst_16690, _x_16697, _x_16705)
    _x_16707 = Heap_mk(None, _x_16706)
    return _x_16707

# Lean: Corpus.Advanced.Heap.min
def advanced_heap_min(__1156: Any, h_1157: Any) -> Any | None:
    _x_16709 = h_1157.heap_0
    _x_16710 = (lambda xs: xs[0] if xs else None)(_x_16709)
    return _x_16710

# Lean: Corpus.Advanced.Heap.popMin
def pop_min(__1158: Any, inst_16712: Any, h_1159: Any) -> Any:
    def _f_16713():
        return h_1159
    _alt_16714 = _f_16713
    def _f_16718(head_16715: Any):
        _x_16716 = []
        _x_16717 = Heap_mk(None, _x_16716)
        return _x_16717
    _alt_16719 = _f_16718
    def _f_16740(head_16720: Any, rest_1161: list[Any]):
        def _f_16723():
            _x_16721 = []
            _x_16722 = Heap_mk(None, _x_16721)
            return _x_16722
        _alt_16724 = _f_16723
        def _f_16732(last: Any):
            _x_16725 = (lambda xs: xs[:-1])(rest_1161)
            _x_16726 = [last] + _x_16725
            _x_16727 = 0
            _x_16730 = sift_down(None, inst_16712, _x_16726, 0)
            _x_16731 = Heap_mk(None, _x_16730)
            return _x_16731
        _alt_16733 = _f_16732
        _x_16734 = (lambda xs: xs[-1] if xs else None)(rest_1161)
        if _x_16734 is None:
            _x_16736 = _alt_16724()
            return _x_16736
        else:
            val_16737 = _x_16734
            _x_16738 = _alt_16733(val_16737)
            return _x_16738
    _alt_16741 = _f_16740
    _x_16742 = h_1159.heap_0
    if len(_x_16742) == 0:
        _x_16744 = _alt_16714()
        return _x_16744
    else:
        head_16745 = _x_16742[0]
        tail_16746 = _x_16742[1:]
        if len(tail_16746) == 0:
            _x_16747 = _alt_16719(head_16745)
            return _x_16747
        else:
            head_16748 = tail_16746[0]
            tail_16749 = tail_16746[1:]
            _x_16750 = [head_16748] + tail_16749
            _x_16751 = _alt_16741(head_16745, _x_16750)
            return _x_16751

# Lean: Corpus.Advanced.Heap.ofList
def of_list(__1163: Any, inst_16755: Any, xs_1164: list[Any]) -> Any:
    def _f_16759(x1_16756: Any, x2_16757: Any):
        _x_16758 = advanced_heap_insert(None, inst_16755, x1_16756, x2_16757)
        return _x_16758
    _x_16760 = advanced_heap_empty(None)
    _x_16761 = functools.reduce(_f_16759, xs_1164, _x_16760)
    return _x_16761

# Lean: Corpus.Advanced.heapSort
def heap_sort(__1165: Any, inst_16763: Any, xs_1166: list[Any]) -> list[Any]:
    _x_16764 = of_list(None, inst_16763, xs_1166)
    _x_16765 = []
    _x_16769 = len(xs_1166)
    _x_16770 = 1
    _x_16773 = _x_16769 + 1
    _x_16774 = extract(None, inst_16763, _x_16764, _x_16765, _x_16773)
    return _x_16774

# Lean: Corpus.Advanced.UnionFind.empty
def advanced_union_find_empty() -> UnionFind:
    _x_16776 = []
    _x_16777 = UnionFind_mk(_x_16776, _x_16776)
    return _x_16777

# Lean: Corpus.Advanced.UnionFind.size
def advanced_union_find_size(uf: UnionFind) -> int:
    _x_16778 = uf.union_find_0
    _x_16779 = len(_x_16778)
    return _x_16779

# Lean: Corpus.Advanced.UnionFind.push
def advanced_union_find_push(uf_1167: UnionFind) -> UnionFind:
    _x_16781 = uf_1167.union_find_0
    _x_16782 = len(_x_16781)
    _x_16786 = []
    _x_16787 = [_x_16782] + _x_16786
    _x_16788 = _x_16781 + _x_16787
    _x_16789 = uf_1167.union_find_1
    _x_16790 = 0
    _x_16793 = [0] + _x_16786
    _x_16794 = _x_16789 + _x_16793
    _x_16795 = UnionFind_mk(_x_16788, _x_16794)
    return _x_16795

# Lean: Corpus.Advanced.UnionFind.ofSize
def of_size(n_1169: int) -> UnionFind:
    _x_16797 = list(range(n_1169))
    _x_16798 = 0
    _x_16801 = list_replicate(None, n_1169, 0)
    _x_16802 = UnionFind_mk(_x_16797, _x_16801)
    return _x_16802

# Lean: Corpus.Advanced.UnionFind.root
def root(uf_1170: UnionFind, i_1171: int) -> int:
    def _f_16804():
        return i_1171
    _alt_16805 = _f_16804
    def _f_16815(p_1173: int):
        _x_16808 = p_1173 == i_1171
        _x_16809 = True
        if _x_16808:
            return i_1171
        else:
            _x_16812 = root(uf_1170, p_1173)
            return _x_16812
    _alt_16816 = _f_16815
    _x_16817 = uf_1170.union_find_0
    _x_16818 = _x_16817[i_1171] if 0 <= i_1171 < len(_x_16817) else None
    if _x_16818 is None:
        _x_16820 = _alt_16805()
        return _x_16820
    else:
        val_16821 = _x_16818
        _x_16822 = _alt_16816(val_16821)
        return _x_16822

# Lean: Corpus.Advanced.UnionFind.equiv
def equiv(uf_1174: UnionFind, i_1175: int, j_1176: int) -> bool:
    _x_16827 = root(uf_1174, i_1175)
    _x_16828 = root(uf_1174, j_1176)
    _x_16829 = _x_16827 == _x_16828
    return _x_16829

# Lean: Corpus.Advanced.UnionFind.union
def union(uf_1177: UnionFind, i_1178: int, j_1179: int) -> UnionFind:
    _x_16831 = root(uf_1177, i_1178)
    _x_16832 = root(uf_1177, j_1179)
    _x_16835 = _x_16831 == _x_16832
    _x_16836 = True
    if _x_16835:
        return uf_1177
    else:
        def _f_16867(ranki: int, rankj: int):
            _x_16839 = ranki < rankj
            if _x_16839:
                _x_16862 = uf_1177.union_find_0
                _x_16863 = _x_16862[:_x_16831] + [_x_16832] + _x_16862[_x_16831+1:]
                _x_16864 = uf_1177.union_find_1
                _x_16865 = UnionFind_mk(_x_16863, _x_16864)
                return _x_16865
            else:
                _x_16841 = rankj < ranki
                if _x_16841:
                    _x_16856 = uf_1177.union_find_0
                    _x_16857 = _x_16856[:_x_16832] + [_x_16831] + _x_16856[_x_16832+1:]
                    _x_16858 = uf_1177.union_find_1
                    _x_16859 = UnionFind_mk(_x_16857, _x_16858)
                    return _x_16859
                else:
                    _x_16843 = uf_1177.union_find_0
                    _x_16844 = _x_16843[:_x_16832] + [_x_16831] + _x_16843[_x_16832+1:]
                    _x_16845 = uf_1177.union_find_1
                    _x_16849 = 1
                    _x_16852 = ranki + 1
                    _x_16853 = _x_16845[:_x_16831] + [_x_16852] + _x_16845[_x_16831+1:]
                    _x_16854 = UnionFind_mk(_x_16844, _x_16853)
                    return _x_16854
        _alt_16868 = _f_16867
        def _f_16871(x_16869: int | None, x_16870: int | None):
            return uf_1177
        _alt_16872 = _f_16871
        _x_16873 = uf_1177.union_find_1
        _x_16874 = _x_16873[_x_16831] if 0 <= _x_16831 < len(_x_16873) else None
        if _x_16874 is None:
            _x_16875 = None
            _x_16876 = _x_16873[_x_16832] if 0 <= _x_16832 < len(_x_16873) else None
            _x_16877 = _alt_16872(_x_16875, _x_16876)
            return _x_16877
        else:
            val_16878 = _x_16874
            _x_16879 = _x_16873[_x_16832] if 0 <= _x_16832 < len(_x_16873) else None
            if _x_16879 is None:
                _x_16880 = val_16878
                _x_16881 = None
                _x_16882 = _alt_16872(_x_16880, _x_16881)
                return _x_16882
            else:
                val_16883 = _x_16879
                _x_16884 = _alt_16868(val_16878, val_16883)
                return _x_16884

# Lean: Corpus.Advanced.UnionFind.numSets
def num_sets(uf_1180: UnionFind) -> int:
    def _f_16894(i_1181: int):
        _x_16892 = root(uf_1180, i_1181)
        _x_16893 = _x_16892 == i_1181
        return _x_16893
    _x_16895 = advanced_union_find_size(uf_1180)
    _x_16896 = list(range(_x_16895))
    _x_16897 = [x for x in _x_16896 if _f_16894(x)]
    _x_16898 = len(_x_16897)
    return _x_16898

# Lean: Corpus.Advanced.Graph.empty
def advanced_graph_empty() -> Graph:
    _x_16900 = 0
    _x_16903 = []
    _x_16904 = Graph_mk(0, _x_16903)
    return _x_16904

# Lean: Corpus.Advanced.Graph.addVertex
def advanced_graph_add_vertex(g_1182: Graph) -> Graph:
    _x_16908 = g_1182.advanced_graph_0
    _x_16909 = 1
    _x_16912 = _x_16908 + 1
    _x_16913 = g_1182.advanced_graph_1
    _x_16914 = Graph_mk(_x_16912, _x_16913)
    return _x_16914

# Lean: Corpus.Advanced.Graph.addEdge
def advanced_graph_add_edge(g_1183: Graph, u_1184: int, v_1185: int) -> Graph:
    _x_16916 = g_1183.advanced_graph_0
    _x_16917 = (u_1184, v_1185)
    _x_16918 = g_1183.advanced_graph_1
    _x_16919 = [_x_16917] + _x_16918
    _x_16920 = Graph_mk(_x_16916, _x_16919)
    return _x_16920

# Lean: Corpus.Advanced.Graph.neighbors
def advanced_graph_neighbors(g_1186: Graph, v_1187: int) -> list[int]:
    def _f_16945(x_16922: tuple[int, int]):
        def _f_16939(u_1188: int, w_1189: int):
            _x_16925 = u_1188 == v_1187
            _x_16926 = True
            if _x_16925:
                _x_16937 = w_1189
                return _x_16937
            else:
                _x_16929 = w_1189 == v_1187
                if _x_16929:
                    _x_16934 = u_1188
                    return _x_16934
                else:
                    _x_16932 = None
                    return _x_16932
        _alt_16940 = _f_16939
        match x_16922:
            case (fst_16941, snd_16942):
                _x_16943 = _alt_16940(fst_16941, snd_16942)
                return _x_16943
    _x_16946 = g_1186.advanced_graph_1
    _x_16947 = [y for x in _x_16946 if (y := _f_16945(x)) is not None]
    return _x_16947

# Lean: Corpus.Advanced.Graph.bfs
def bfs(g_1190: Graph, start_1191: int) -> list[int]:
    _x_16949 = []
    _x_16950 = [start_1191] + _x_16949
    _x_16954 = g_1190.advanced_graph_0
    _x_16955 = g_1190.advanced_graph_1
    _x_16956 = len(_x_16955)
    _x_16957 = _x_16954 + _x_16956
    _x_16958 = 1
    _x_16961 = _x_16957 + 1
    _x_16962 = bfs_loop(g_1190, _x_16950, _x_16949, _x_16961)
    return _x_16962

# Lean: Corpus.Advanced.Graph.dfs
def dfs(g_1192: Graph, start_1193: int) -> list[int]:
    _x_16964 = []
    _x_16965 = [start_1193] + _x_16964
    _x_16969 = g_1192.advanced_graph_0
    _x_16970 = g_1192.advanced_graph_1
    _x_16971 = len(_x_16970)
    _x_16972 = _x_16969 + _x_16971
    _x_16973 = 1
    _x_16976 = _x_16972 + 1
    _x_16977 = dfs_loop(g_1192, _x_16965, _x_16964, _x_16976)
    return _x_16977

# Lean: Corpus.Advanced.Graph.isConnected
def is_connected(g_1194: Graph) -> bool:
    _x_16981 = g_1194.advanced_graph_0
    _x_16982 = 0
    _x_16985 = _x_16981 == 0
    _x_16986 = True
    if _x_16985:
        return True
    else:
        _x_16989 = bfs(g_1194, 0)
        _x_16990 = len(_x_16989)
        _x_16991 = _x_16990 == _x_16981
        return _x_16991

# Lean: Corpus.Advanced.Graph.topoSort
def topo_sort(g_1196: Graph) -> list[int] | None:
    def _f_17004(v_1197: int):
        def _f_17000(x_16995: tuple[int, int]):
            _x_16998 = x_16995[1]
            _x_16999 = _x_16998 == v_1197
            return _x_16999
        _x_17001 = g_1196.advanced_graph_1
        _x_17002 = [x for x in _x_17001 if _f_17000(x)]
        _x_17003 = len(_x_17002)
        return _x_17003
    _x_17005 = g_1196.advanced_graph_0
    _x_17006 = list(range(_x_17005))
    _x_17007 = [_f_17004(x) for x in _x_17006]
    def _f_17028(v_1198: int):
        def _f_17008(x_1199: bool):
            return x_1199
        _alt_17009 = _f_17008
        def _f_17011():
            _x_17010 = False
            return False
        _alt_17012 = _f_17011
        def _f_17020(x_17013: int):
            _x_17016 = 0
            _x_17019 = x_17013 == 0
            return _x_17019
        _x_17021 = _x_17007[v_1198] if 0 <= v_1198 < len(_x_17007) else None
        _x_17022 = option_map(None, None, _f_17020, _x_17021)
        if _x_17022 is None:
            _x_17024 = _alt_17012()
            return _x_17024
        else:
            val_17025 = _x_17022
            _x_17026 = _alt_17009(val_17025)
            return _x_17026
    _x_17029 = [x for x in _x_17006 if _f_17028(x)]
    _x_17030 = []
    _x_17034 = 1
    _x_17037 = _x_17005 + 1
    _x_17038 = topo_sort_loop(g_1196, _x_17029, _x_17007, _x_17030, _x_17037)
    return _x_17038

# Lean: Corpus.Advanced.Graph.hasCycle
def has_cycle(g_1201: Graph) -> bool:
    _x_17040 = topo_sort(g_1201)
    _x_17041 = (lambda x: x is None)(_x_17040)
    return _x_17041

# Lean: Corpus.Advanced.Matrix.get
def advanced_matrix_get(m_1202: list[list[int]], i_1203: int, j_1204: int) -> int | None:
    def _f_17044():
        _x_17043 = None
        return _x_17043
    _alt_17045 = _f_17044
    def _f_17047(row_1206: list[int]):
        _x_17046 = row_1206[j_1204] if 0 <= j_1204 < len(row_1206) else None
        return _x_17046
    _alt_17048 = _f_17047
    _x_17049 = m_1202[i_1203] if 0 <= i_1203 < len(m_1202) else None
    if _x_17049 is None:
        _x_17051 = _alt_17045()
        return _x_17051
    else:
        val_17052 = _x_17049
        _x_17053 = _alt_17048(val_17052)
        return _x_17053

# Lean: Corpus.Advanced.Matrix.set
def advanced_matrix_set(m_1207: list[list[int]], i_1208: int, j_1209: int, v_1210: int) -> list[list[int]]:
    def _f_17086(x_17056: tuple[int, list[int]]):
        def _f_17080(idx_1211: int, row_1212: list[int]):
            _x_17059 = idx_1211 == i_1208
            _x_17060 = True
            if _x_17059:
                def _f_17076(x_17064: tuple[int, int]):
                    def _f_17070(jdx: int, val: int):
                        _x_17065 = jdx == j_1209
                        if _x_17065:
                            return v_1210
                        else:
                            return val
                    _alt_17071 = _f_17070
                    match x_17064:
                        case (fst_17072, snd_17073):
                            _x_17074 = _alt_17071(fst_17072, snd_17073)
                            return _x_17074
                _x_17077 = list(enumerate(row_1212))
                _x_17078 = [_f_17076(x) for x in _x_17077]
                return _x_17078
            else:
                return row_1212
        _alt_17081 = _f_17080
        match x_17056:
            case (fst_17082, snd_17083):
                _x_17084 = _alt_17081(fst_17082, snd_17083)
                return _x_17084
    _x_17087 = list(enumerate(m_1207))
    _x_17088 = [_f_17086(x) for x in _x_17087]
    return _x_17088

# Lean: Corpus.Advanced.Matrix.create
def advanced_matrix_create(n_1213: int, fill: int) -> list[list[int]]:
    _x_17090 = list_replicate(None, n_1213, fill)
    _x_17091 = list_replicate(None, n_1213, _x_17090)
    return _x_17091

# Lean: Corpus.Advanced.floydWarshall
def floyd_warshall(n_1214: int, edges: list[tuple[int, tuple[int, int]]]) -> list[list[int]]:
    _x_17093 = 1000000000
    _x_17096 = advanced_matrix_create(n_1214, 1000000000)
    def _f_17101(m_1216: list[list[int]], i_1217: int):
        _x_17097 = 0
        _x_17100 = advanced_matrix_set(m_1216, i_1217, i_1217, 0)
        return _x_17100
    _x_17102 = list(range(n_1214))
    _x_17103 = functools.reduce(_f_17101, _x_17102, _x_17096)
    def _f_17115(m_1218: list[list[int]], x_17104: tuple[int, tuple[int, int]]):
        def _f_17106(u_1219: int, v_1220: int, w_1221: int):
            _x_17105 = advanced_matrix_set(m_1218, u_1219, v_1220, w_1221)
            return _x_17105
        _alt_17107 = _f_17106
        match x_17104:
            case (fst_17108, snd_17109):
                match snd_17109:
                    case (fst_17110, snd_17111):
                        _x_17112 = _alt_17107(fst_17108, fst_17110, snd_17111)
                        return _x_17112
    _x_17116 = functools.reduce(_f_17115, edges, _x_17103)
    def _f_17159(dist: list[list[int]], k_1222: int):
        def _f_17157(d_1223: list[list[int]], i_1224: int):
            def _f_17155(d_: list[list[int]], j_1225: int):
                def _f_17126(dik: int, dkj: int, dij: int):
                    _x_17120 = dik + dkj
                    _x_17121 = _x_17120 < dij
                    if _x_17121:
                        _x_17124 = advanced_matrix_set(d_, i_1224, j_1225, _x_17120)
                        return _x_17124
                    else:
                        return d_
                _alt_17127 = _f_17126
                def _f_17131(x_17128: int | None, x_17129: int | None, x_17130: int | None):
                    return d_
                _alt_17132 = _f_17131
                _x_17133 = advanced_matrix_get(d_, i_1224, k_1222)
                if _x_17133 is None:
                    _x_17134 = None
                    _x_17135 = advanced_matrix_get(d_, k_1222, j_1225)
                    _x_17136 = advanced_matrix_get(d_, i_1224, j_1225)
                    _x_17137 = _alt_17132(_x_17134, _x_17135, _x_17136)
                    return _x_17137
                else:
                    val_17138 = _x_17133
                    _x_17139 = advanced_matrix_get(d_, k_1222, j_1225)
                    if _x_17139 is None:
                        _x_17140 = val_17138
                        _x_17141 = None
                        _x_17142 = advanced_matrix_get(d_, i_1224, j_1225)
                        _x_17143 = _alt_17132(_x_17140, _x_17141, _x_17142)
                        return _x_17143
                    else:
                        val_17144 = _x_17139
                        _x_17145 = advanced_matrix_get(d_, i_1224, j_1225)
                        if _x_17145 is None:
                            _x_17146 = val_17138
                            _x_17147 = val_17144
                            _x_17148 = None
                            _x_17149 = _alt_17132(_x_17146, _x_17147, _x_17148)
                            return _x_17149
                        else:
                            val_17150 = _x_17145
                            _x_17151 = _alt_17127(val_17138, val_17144, val_17150)
                            return _x_17151
            _x_17156 = functools.reduce(_f_17155, _x_17102, d_1223)
            return _x_17156
        _x_17158 = functools.reduce(_f_17157, _x_17102, dist)
        return _x_17158
    _x_17160 = functools.reduce(_f_17159, _x_17102, _x_17116)
    return _x_17160

# Lean: Corpus.NumberTheory.extGcd
def ext_gcd(a_1226: int, b_1227: int) -> tuple[int, tuple[int, int]]:
    _x_17164 = 0
    _x_17167 = b_1227 == 0
    _x_17168 = True
    if _x_17167:
        _x_17203 = 1
        _x_17208 = (1, a_1226)
        _x_17209 = (1, _x_17208)
        return _x_17209
    else:
        def _f_17188(x_1228: int, y_1229: int, g_1230: int):
            _x_17181 = cast(None, _x_17180, a_1226)
            _x_17182 = cast(None, _x_17180, b_1227)
            _x_17183 = _x_17181 // _x_17182
            _x_17184 = _x_17183 * y_1229
            _x_17185 = x_1228 - _x_17184
            _x_17186 = (_x_17185, g_1230)
            _x_17187 = (y_1229, _x_17186)
            return _x_17187
        _alt_17189 = _f_17188
        _x_17193 = a_1226 % b_1227
        _x_17194 = ext_gcd(b_1227, _x_17193)
        match _x_17194:
            case (fst_17195, snd_17196):
                match snd_17196:
                    case (fst_17197, snd_17198):
                        _x_17199 = _alt_17189(fst_17195, fst_17197, snd_17198)
                        return _x_17199

# Lean: Corpus.NumberTheory.modInverse
def mod_inverse(a_1231: int, m_1232: int) -> int | None:
    def _f_17238(x_1233: int, fst_17212: int, g_1234: int):
        _x_17215 = 1
        _x_17218 = g_1234 == 1
        _x_17219 = True
        if _x_17218:
            _x_17231 = cast(None, _x_17230, m_1232)
            _x_17232 = x_1233 % _x_17231
            _x_17233 = _x_17232 + _x_17231
            _x_17234 = _x_17233 % _x_17231
            _x_17235 = to_nat(_x_17234)
            _x_17236 = _x_17235
            return _x_17236
        else:
            _x_17222 = None
            return _x_17222
    _alt_17239 = _f_17238
    _x_17240 = ext_gcd(a_1231, m_1232)
    match _x_17240:
        case (fst_17241, snd_17242):
            match snd_17242:
                case (fst_17243, snd_17244):
                    _x_17245 = _alt_17239(fst_17241, fst_17243, snd_17244)
                    return _x_17245

# Lean: Corpus.NumberTheory.totient
def totient(n_1235: int) -> int:
    _x_17249 = 1
    _x_17252 = n_1235 <= 1
    if _x_17252:
        return n_1235
    else:
        _x_17254 = 0
        _x_17257 = count(n_1235, 1, 0)
        return _x_17257

# Lean: Corpus.NumberTheory.isPerfect
def is_perfect(n_1236: int) -> bool:
    _x_17261 = 2
    _x_17264 = n_1236 < 2
    if _x_17264:
        _x_17317 = False
        return False
    else:
        def _f_17307(acc_1237: int, i_1238: int):
            def _f_17267():
                _x_17266 = False
                return False
            _alt_17268 = _f_17267
            def _f_17279():
                _x_17274 = n_1236 % i_1238
                _x_17275 = 0
                _x_17278 = _x_17274 == 0
                return _x_17278
            _alt_17280 = _f_17279
            _x_17281 = 0
            _x_17284 = 0 < i_1238
            def _jp_17300(_y_17290: bool):
                _x_17291 = True
                if _y_17290:
                    _x_17298 = acc_1237 + i_1238
                    return _x_17298
                else:
                    return acc_1237
            def _jp_17306():
                _x_17305 = _alt_17280()
                return _jp_17300(_x_17305)
            def _jp_17303():
                _x_17302 = _alt_17268()
                return _jp_17300(_x_17302)
            if _x_17284:
                return _jp_17306()
            else:
                return _jp_17303()
        _x_17308 = 0
        _x_17311 = list(range(n_1236))
        _x_17312 = functools.reduce(_f_17307, _x_17311, 0)
        _x_17315 = _x_17312 == n_1236
        return _x_17315

# Lean: Corpus.NumberTheory.isAbundant
def is_abundant(n_1241: int) -> bool:
    _x_17320 = 2
    _x_17323 = n_1241 < 2
    if _x_17323:
        _x_17375 = False
        return False
    else:
        def _f_17366(acc_1242: int, i_1243: int):
            def _f_17326():
                _x_17325 = False
                return False
            _alt_17327 = _f_17326
            def _f_17338():
                _x_17333 = n_1241 % i_1243
                _x_17334 = 0
                _x_17337 = _x_17333 == 0
                return _x_17337
            _alt_17339 = _f_17338
            _x_17340 = 0
            _x_17343 = 0 < i_1243
            def _jp_17359(_y_17349: bool):
                _x_17350 = True
                if _y_17349:
                    _x_17357 = acc_1242 + i_1243
                    return _x_17357
                else:
                    return acc_1242
            def _jp_17362():
                _x_17361 = _alt_17327()
                return _jp_17359(_x_17361)
            def _jp_17365():
                _x_17364 = _alt_17339()
                return _jp_17359(_x_17364)
            if _x_17343:
                return _jp_17365()
            else:
                return _jp_17362()
        _x_17367 = 0
        _x_17370 = list(range(n_1241))
        _x_17371 = functools.reduce(_f_17366, _x_17370, 0)
        _x_17372 = n_1241 < _x_17371
        return _x_17372

# Lean: Corpus.NumberTheory.isDeficient
def is_deficient(n_1247: int) -> bool:
    _x_17378 = 1
    _x_17381 = n_1247 < 1
    if _x_17381:
        _x_17433 = False
        return False
    else:
        def _f_17424(acc_1248: int, i_1249: int):
            def _f_17384():
                _x_17383 = False
                return False
            _alt_17385 = _f_17384
            def _f_17396():
                _x_17391 = n_1247 % i_1249
                _x_17392 = 0
                _x_17395 = _x_17391 == 0
                return _x_17395
            _alt_17397 = _f_17396
            _x_17398 = 0
            _x_17401 = 0 < i_1249
            def _jp_17417(_y_17407: bool):
                _x_17408 = True
                if _y_17407:
                    _x_17415 = acc_1248 + i_1249
                    return _x_17415
                else:
                    return acc_1248
            def _jp_17423():
                _x_17422 = _alt_17397()
                return _jp_17417(_x_17422)
            def _jp_17420():
                _x_17419 = _alt_17385()
                return _jp_17417(_x_17419)
            if _x_17401:
                return _jp_17423()
            else:
                return _jp_17420()
        _x_17425 = 0
        _x_17428 = list(range(n_1247))
        _x_17429 = functools.reduce(_f_17424, _x_17428, 0)
        _x_17430 = _x_17429 < n_1247
        return _x_17430

# Lean: Corpus.NumberTheory.collatzLength
def collatz_length(n_1253: int) -> int:
    _x_17436 = 1
    _x_17439 = n_1253 <= 1
    if _x_17439:
        _x_17478 = 0
        return 0
    else:
        _x_17449 = 2
        _x_17452 = n_1253 % 2
        _x_17453 = 0
        _x_17456 = _x_17452 == 0
        _x_17457 = True
        def _jp_17476(_y_17473: int):
            _x_17474 = collatz_length(_y_17473)
            _x_17475 = 1 + _x_17474
            return _x_17475
        if _x_17456:
            _x_17472 = n_1253 // 2
            return _jp_17476(_x_17472)
        else:
            _x_17463 = 3
            _x_17466 = 3 * n_1253
            _x_17467 = _x_17466 + 1
            return _jp_17476(_x_17467)

# Lean: Corpus.NumberTheory.isqrt
def isqrt(n_1254: int) -> int:
    _x_17485 = 0
    _x_17488 = n_1254 == 0
    _x_17489 = True
    if _x_17488:
        return 0
    else:
        _x_17492 = isqrt_go(n_1254, n_1254, n_1254)
        return _x_17492

# Lean: Corpus.NumberTheory.isPerfectSquare
def is_perfect_square(n_1255: int) -> bool:
    _x_17496 = isqrt(n_1255)
    _x_17502 = _x_17496 * _x_17496
    _x_17503 = _x_17502 == n_1255
    return _x_17503

# Lean: Corpus.NumberTheory.digitalRoot
def digital_root(n_1257: int) -> int:
    _x_17505 = 10
    _x_17508 = n_1257 < 10
    if _x_17508:
        return n_1257
    else:
        _x_17510 = digit_sum(n_1257)
        _x_17511 = digital_root(_x_17510)
        return _x_17511

# Lean: Corpus.NumberTheory.isHarshad
def is_harshad(n_1258: int) -> bool:
    _x_17517 = 0
    _x_17520 = n_1258 == 0
    _x_17521 = True
    if _x_17520:
        _x_17543 = False
        return False
    else:
        _x_17524 = digit_sum(n_1258)
        def _f_17526():
            _x_17525 = False
            return False
        _alt_17527 = _f_17526
        def _f_17533():
            _x_17531 = n_1258 % _x_17524
            _x_17532 = _x_17531 == 0
            return _x_17532
        _alt_17534 = _f_17533
        _x_17535 = 0 < _x_17524
        if _x_17535:
            _x_17540 = _alt_17534()
            return _x_17540
        else:
            _x_17538 = _alt_17527()
            return _x_17538

# Lean: Corpus.NumberTheory.hammingWeight
def hamming_weight(n_1262: int) -> int:
    _x_17548 = 0
    _x_17551 = n_1262 == 0
    _x_17552 = True
    if _x_17551:
        return 0
    else:
        _x_17561 = 2
        _x_17564 = n_1262 % 2
        _x_17568 = n_1262 // 2
        _x_17569 = hamming_weight(_x_17568)
        _x_17570 = _x_17564 + _x_17569
        return _x_17570

# Lean: Corpus.NumberTheory.josephus
def josephus(n_1263: int, k_1264: int) -> int:
    _x_17576 = 1
    _x_17579 = n_1263 == 1
    _x_17580 = True
    if _x_17579:
        _x_17597 = 0
        return 0
    else:
        _x_17592 = n_1263 - 1
        _x_17593 = josephus(_x_17592, k_1264)
        _x_17594 = _x_17593 + k_1264
        _x_17595 = _x_17594 % n_1263
        return _x_17595

# Lean: Corpus.Geometry.dist2D
def dist2d(p1_1265: Point2D, p2_1266: Point2D) -> float:
    _x_17605 = p2_1266.point2d_0
    _x_17606 = p1_1265.point2d_0
    _x_17607 = _x_17605 - _x_17606
    _x_17608 = p2_1266.point2d_1
    _x_17609 = p1_1265.point2d_1
    _x_17610 = _x_17608 - _x_17609
    _x_17617 = _x_17607 * _x_17607
    _x_17618 = _x_17610 * _x_17610
    _x_17619 = _x_17617 + _x_17618
    _x_17620 = sqrt(_x_17619)
    return _x_17620

# Lean: Corpus.Geometry.dist3D
def dist3d(p1_1267: Point3D, p2_1268: Point3D) -> float:
    _x_17625 = p2_1268.point3d_0
    _x_17626 = p1_1267.point3d_0
    _x_17627 = _x_17625 - _x_17626
    _x_17628 = p2_1268.point3d_1
    _x_17629 = p1_1267.point3d_1
    _x_17630 = _x_17628 - _x_17629
    _x_17631 = p2_1268.point3d_2
    _x_17632 = p1_1267.point3d_2
    _x_17633 = _x_17631 - _x_17632
    _x_17640 = _x_17627 * _x_17627
    _x_17641 = _x_17630 * _x_17630
    _x_17642 = _x_17640 + _x_17641
    _x_17643 = _x_17633 * _x_17633
    _x_17644 = _x_17642 + _x_17643
    _x_17645 = sqrt(_x_17644)
    return _x_17645

# Lean: Corpus.Geometry.manhattan2D
def manhattan2d(p1_1271: Point2D, p2_1272: Point2D) -> float:
    _x_17653 = p2_1272.point2d_0
    _x_17654 = p1_1271.point2d_0
    _x_17655 = _x_17653 - _x_17654
    _x_17656 = float_abs(_x_17655)
    _x_17657 = p2_1272.point2d_1
    _x_17658 = p1_1271.point2d_1
    _x_17659 = _x_17657 - _x_17658
    _x_17660 = float_abs(_x_17659)
    _x_17661 = _x_17656 + _x_17660
    return _x_17661

# Lean: Corpus.Geometry.chebyshev2D
def chebyshev2d(p1_1273: Point2D, p2_1274: Point2D) -> float:
    _x_17664 = max
    _x_17668 = p2_1274.point2d_0
    _x_17669 = p1_1273.point2d_0
    _x_17670 = _x_17668 - _x_17669
    _x_17671 = float_abs(_x_17670)
    _x_17672 = p2_1274.point2d_1
    _x_17673 = p1_1273.point2d_1
    _x_17674 = _x_17672 - _x_17673
    _x_17675 = float_abs(_x_17674)
    _x_17676 = _x_17664(_x_17671, _x_17675)
    return _x_17676

# Lean: Corpus.Geometry.midpoint2D
def midpoint2d(p1_1275: Point2D, p2_1276: Point2D) -> Point2D:
    _x_17684 = p1_1275.point2d_0
    _x_17685 = p2_1276.point2d_0
    _x_17686 = _x_17684 + _x_17685
    _x_17687 = 2
    _x_17690 = _x_17686 // 2
    _x_17691 = p1_1275.point2d_1
    _x_17692 = p2_1276.point2d_1
    _x_17693 = _x_17691 + _x_17692
    _x_17694 = _x_17693 // 2
    _x_17695 = Point2D_mk(_x_17690, _x_17694)
    return _x_17695

# Lean: Corpus.Geometry.midpoint3D
def midpoint3d(p1_1277: Point3D, p2_1278: Point3D) -> Point3D:
    _x_17703 = p1_1277.point3d_0
    _x_17704 = p2_1278.point3d_0
    _x_17705 = _x_17703 + _x_17704
    _x_17706 = 2
    _x_17709 = _x_17705 // 2
    _x_17710 = p1_1277.point3d_1
    _x_17711 = p2_1278.point3d_1
    _x_17712 = _x_17710 + _x_17711
    _x_17713 = _x_17712 // 2
    _x_17714 = p1_1277.point3d_2
    _x_17715 = p2_1278.point3d_2
    _x_17716 = _x_17714 + _x_17715
    _x_17717 = _x_17716 // 2
    _x_17718 = Point3D_mk(_x_17709, _x_17713, _x_17717)
    return _x_17718

# Lean: Corpus.Geometry.dot2D
def dot2d(p1_1279: Point2D, p2_1280: Point2D) -> float:
    _x_17726 = p1_1279.point2d_0
    _x_17727 = p2_1280.point2d_0
    _x_17728 = _x_17726 * _x_17727
    _x_17729 = p1_1279.point2d_1
    _x_17730 = p2_1280.point2d_1
    _x_17731 = _x_17729 * _x_17730
    _x_17732 = _x_17728 + _x_17731
    return _x_17732

# Lean: Corpus.Geometry.dot3D
def dot3d(p1_1281: Point3D, p2_1282: Point3D) -> float:
    _x_17740 = p1_1281.point3d_0
    _x_17741 = p2_1282.point3d_0
    _x_17742 = _x_17740 * _x_17741
    _x_17743 = p1_1281.point3d_1
    _x_17744 = p2_1282.point3d_1
    _x_17745 = _x_17743 * _x_17744
    _x_17746 = _x_17742 + _x_17745
    _x_17747 = p1_1281.point3d_2
    _x_17748 = p2_1282.point3d_2
    _x_17749 = _x_17747 * _x_17748
    _x_17750 = _x_17746 + _x_17749
    return _x_17750

# Lean: Corpus.Geometry.cross2D
def cross2d(p1_1283: Point2D, p2_1284: Point2D) -> float:
    _x_17758 = p1_1283.point2d_0
    _x_17759 = p2_1284.point2d_1
    _x_17760 = _x_17758 * _x_17759
    _x_17761 = p1_1283.point2d_1
    _x_17762 = p2_1284.point2d_0
    _x_17763 = _x_17761 * _x_17762
    _x_17764 = _x_17760 - _x_17763
    return _x_17764

# Lean: Corpus.Geometry.cross3D
def cross3d(p1_1285: Point3D, p2_1286: Point3D) -> Point3D:
    _x_17772 = p1_1285.point3d_1
    _x_17773 = p2_1286.point3d_2
    _x_17774 = _x_17772 * _x_17773
    _x_17775 = p1_1285.point3d_2
    _x_17776 = p2_1286.point3d_1
    _x_17777 = _x_17775 * _x_17776
    _x_17778 = _x_17774 - _x_17777
    _x_17779 = p2_1286.point3d_0
    _x_17780 = _x_17775 * _x_17779
    _x_17781 = p1_1285.point3d_0
    _x_17782 = _x_17781 * _x_17773
    _x_17783 = _x_17780 - _x_17782
    _x_17784 = _x_17781 * _x_17776
    _x_17785 = _x_17772 * _x_17779
    _x_17786 = _x_17784 - _x_17785
    _x_17787 = Point3D_mk(_x_17778, _x_17783, _x_17786)
    return _x_17787

# Lean: Corpus.Geometry.magnitude2D
def magnitude2d(p_1287: Point2D) -> float:
    _x_17795 = p_1287.point2d_0
    _x_17796 = _x_17795 * _x_17795
    _x_17797 = p_1287.point2d_1
    _x_17798 = _x_17797 * _x_17797
    _x_17799 = _x_17796 + _x_17798
    _x_17800 = sqrt(_x_17799)
    return _x_17800

# Lean: Corpus.Geometry.magnitude3D
def magnitude3d(p_1288: Point3D) -> float:
    _x_17808 = p_1288.point3d_0
    _x_17809 = _x_17808 * _x_17808
    _x_17810 = p_1288.point3d_1
    _x_17811 = _x_17810 * _x_17810
    _x_17812 = _x_17809 + _x_17811
    _x_17813 = p_1288.point3d_2
    _x_17814 = _x_17813 * _x_17813
    _x_17815 = _x_17812 + _x_17814
    _x_17816 = sqrt(_x_17815)
    return _x_17816

# Lean: Corpus.Geometry.normalize2D
def normalize2d(p_1289: Point2D) -> Point2D:
    _x_17818 = magnitude2d(p_1289)
    _x_17821 = 0
    _x_17824 = _x_17818 == 0
    _x_17825 = True
    if _x_17824:
        return p_1289
    else:
        _x_17831 = p_1289.point2d_0
        _x_17832 = _x_17831 // _x_17818
        _x_17833 = p_1289.point2d_1
        _x_17834 = _x_17833 // _x_17818
        _x_17835 = Point2D_mk(_x_17832, _x_17834)
        return _x_17835

# Lean: Corpus.Geometry.normalize3D
def normalize3d(p_1291: Point3D) -> Point3D:
    _x_17839 = magnitude3d(p_1291)
    _x_17842 = 0
    _x_17845 = _x_17839 == 0
    _x_17846 = True
    if _x_17845:
        return p_1291
    else:
        _x_17852 = p_1291.point3d_0
        _x_17853 = _x_17852 // _x_17839
        _x_17854 = p_1291.point3d_1
        _x_17855 = _x_17854 // _x_17839
        _x_17856 = p_1291.point3d_2
        _x_17857 = _x_17856 // _x_17839
        _x_17858 = Point3D_mk(_x_17853, _x_17855, _x_17857)
        return _x_17858

# Lean: Corpus.Geometry.triangleArea
def triangle_area(p1_1293: Point2D, p2_1294: Point2D, p3_1295: Point2D) -> float:
    _x_17871 = p2_1294.point2d_0
    _x_17872 = p1_1293.point2d_0
    _x_17873 = _x_17871 - _x_17872
    _x_17874 = p3_1295.point2d_1
    _x_17875 = p1_1293.point2d_1
    _x_17876 = _x_17874 - _x_17875
    _x_17877 = _x_17873 * _x_17876
    _x_17878 = p3_1295.point2d_0
    _x_17879 = _x_17878 - _x_17872
    _x_17880 = p2_1294.point2d_1
    _x_17881 = _x_17880 - _x_17875
    _x_17882 = _x_17879 * _x_17881
    _x_17883 = _x_17877 - _x_17882
    _x_17884 = float_abs(_x_17883)
    _x_17885 = 2
    _x_17888 = _x_17884 // 2
    return _x_17888

# Lean: Corpus.Geometry.pointInTriangle
def point_in_triangle(p_1296: Point2D, p1_1297: Point2D, p2_1298: Point2D, p3_1299: Point2D) -> bool:
    _x_17890 = sign(p_1296, p1_1297, p2_1298)
    _x_17891 = sign(p_1296, p2_1298, p3_1299)
    _x_17892 = sign(p_1296, p3_1299, p1_1297)
    def _f_17894():
        _x_17893 = True
        return True
    _alt_17895 = _f_17894
    def _f_17901():
        _x_17896 = 0
        _x_17899 = float_dec_lt(_x_17892, 0)
        return _x_17899
    _alt_17902 = _f_17901
    _alt_17903 = _f_17894
    def _f_17909():
        _x_17904 = 0
        _x_17907 = float_dec_lt(_x_17891, 0)
        return _x_17907
    _alt_17910 = _f_17909
    _x_17911 = 0
    _x_17914 = float_dec_lt(_x_17890, 0)
    def _jp_17987(_y_17920: bool):
        def _jp_17980(_y_17925: bool):
            _alt_17926 = _f_17894
            def _f_17929():
                _x_17927 = float_dec_lt(0, _x_17892)
                return _x_17927
            _alt_17930 = _f_17929
            _alt_17931 = _f_17894
            def _f_17934():
                _x_17932 = float_dec_lt(0, _x_17891)
                return _x_17932
            _alt_17935 = _f_17934
            _x_17936 = float_dec_lt(0, _x_17890)
            def _jp_17973(_y_17942: bool):
                def _jp_17966(_y_17947: bool):
                    def _f_17949():
                        _x_17948 = False
                        return False
                    _alt_17950 = _f_17949
                    def _f_17951():
                        return _y_17947
                    _alt_17952 = _f_17951
                    def _jp_17959(_y_17957: bool):
                        _x_17958 = not _y_17957
                        return _x_17958
                    def _jp_17965():
                        _x_17964 = _alt_17952()
                        return _jp_17959(_x_17964)
                    def _jp_17962():
                        _x_17961 = _alt_17950()
                        return _jp_17959(_x_17961)
                    if _y_17925:
                        return _jp_17965()
                    else:
                        return _jp_17962()
                def _jp_17969():
                    _x_17968 = _alt_17930()
                    return _jp_17966(_x_17968)
                def _jp_17972():
                    _x_17971 = _alt_17926()
                    return _jp_17966(_x_17971)
                if _y_17942:
                    return _jp_17972()
                else:
                    return _jp_17969()
            def _jp_17979():
                _x_17978 = _alt_17931()
                return _jp_17973(_x_17978)
            def _jp_17976():
                _x_17975 = _alt_17935()
                return _jp_17973(_x_17975)
            if _x_17936:
                return _jp_17979()
            else:
                return _jp_17976()
        def _jp_17983():
            _x_17982 = _alt_17902()
            return _jp_17980(_x_17982)
        def _jp_17986():
            _x_17985 = _alt_17895()
            return _jp_17980(_x_17985)
        if _y_17920:
            return _jp_17986()
        else:
            return _jp_17983()
    def _jp_17993():
        _x_17992 = _alt_17903()
        return _jp_17987(_x_17992)
    def _jp_17990():
        _x_17989 = _alt_17910()
        return _jp_17987(_x_17989)
    if _x_17914:
        return _jp_17993()
    else:
        return _jp_17990()

# Lean: Corpus.Geometry.circleArea
def circle_area(radius: float) -> float:
    _x_17999 = _x_17998.of_scientific_0
    _x_18000 = 314159265358979
    _x_18001 = True
    _x_18002 = 14
    _x_18003 = _x_17999(_x_18000, True, _x_18002)
    _x_18004 = _x_18003 * radius
    _x_18005 = _x_18004 * radius
    return _x_18005

# Lean: Corpus.Geometry.circleCircumference
def circle_circumference(radius_1307: float) -> float:
    _x_18010 = 2
    _x_18014 = _x_18013.of_scientific_0
    _x_18015 = 314159265358979
    _x_18016 = True
    _x_18017 = 14
    _x_18018 = _x_18014(_x_18015, True, _x_18017)
    _x_18019 = 2 * _x_18018
    _x_18020 = _x_18019 * radius_1307
    return _x_18020

# Lean: Corpus.Geometry.sphereVolume
def sphere_volume(radius_1308: float) -> float:
    _x_18028 = 4
    _x_18031 = 3
    _x_18034 = 4 // 3
    _x_18036 = _x_18035.of_scientific_0
    _x_18037 = 314159265358979
    _x_18038 = True
    _x_18039 = 14
    _x_18040 = _x_18036(_x_18037, True, _x_18039)
    _x_18041 = _x_18034 * _x_18040
    _x_18042 = _x_18041 * radius_1308
    _x_18043 = _x_18042 * radius_1308
    _x_18044 = _x_18043 * radius_1308
    return _x_18044

# Lean: Corpus.Geometry.sphereSurfaceArea
def sphere_surface_area(radius_1309: float) -> float:
    _x_18049 = 4
    _x_18053 = _x_18052.of_scientific_0
    _x_18054 = 314159265358979
    _x_18055 = True
    _x_18056 = 14
    _x_18057 = _x_18053(_x_18054, True, _x_18056)
    _x_18058 = 4 * _x_18057
    _x_18059 = _x_18058 * radius_1309
    _x_18060 = _x_18059 * radius_1309
    return _x_18060

# Lean: Corpus.Geometry.rectangleArea
def rectangle_area(width: float, height: float) -> float:
    _x_18065 = width * height
    return _x_18065

# Lean: Corpus.Geometry.rectanglePerimeter
def rectangle_perimeter(width_1310: float, height_1311: float) -> float:
    _x_18070 = 2
    _x_18076 = width_1310 + height_1311
    _x_18077 = 2 * _x_18076
    return _x_18077

# Lean: Corpus.Geometry.polygonArea
def polygon_area(vertices: list[Point2D]) -> float:
    def _f_18082():
        _x_18079 = 0
        return 0
    _alt_18083 = _f_18082
    def _f_18088(head_18084: Point2D):
        _x_18085 = 0
        return 0
    _alt_18089 = _f_18088
    def _f_18095(first_1313: Point2D, rest_1314: list[Point2D]):
        _x_18090 = 0
        _x_18093 = polygon_area_go(rest_1314, first_1313, first_1313, 0)
        _x_18094 = float_abs(_x_18093)
        return _x_18094
    _alt_18096 = _f_18095
    if len(vertices) == 0:
        _x_18098 = _alt_18083()
        return _x_18098
    else:
        head_18099 = vertices[0]
        tail_18100 = vertices[1:]
        if len(tail_18100) == 0:
            _x_18101 = _alt_18089(head_18099)
            return _x_18101
        else:
            head_18102 = tail_18100[0]
            tail_18103 = tail_18100[1:]
            _x_18104 = [head_18102] + tail_18103
            _x_18105 = _alt_18096(head_18099, _x_18104)
            return _x_18105

# Lean: Corpus.Geometry.isConvexPolygon
def is_convex_polygon(vertices_1315: list[Point2D]) -> bool:
    def _f_18110():
        _x_18109 = True
        return True
    _alt_18111 = _f_18110
    def _f_18114(head_18112: Point2D):
        _x_18113 = True
        return True
    _alt_18115 = _f_18114
    def _f_18119(head_18116: Point2D, head_18117: Point2D):
        _x_18118 = True
        return True
    _alt_18120 = _f_18119
    def _f_18123(first_1317: Point2D, second_1318: Point2D, rest_1319: list[Point2D]):
        _x_18121 = None
        _x_18122 = is_convex_polygon_check(first_1317, second_1318, first_1317, second_1318, rest_1319, _x_18121)
        return _x_18122
    _alt_18124 = _f_18123
    if len(vertices_1315) == 0:
        _x_18126 = _alt_18111()
        return _x_18126
    else:
        head_18127 = vertices_1315[0]
        tail_18128 = vertices_1315[1:]
        if len(tail_18128) == 0:
            _x_18129 = _alt_18115(head_18127)
            return _x_18129
        else:
            head_18130 = tail_18128[0]
            tail_18131 = tail_18128[1:]
            if len(tail_18131) == 0:
                _x_18132 = _alt_18120(head_18127, head_18130)
                return _x_18132
            else:
                head_18133 = tail_18131[0]
                tail_18134 = tail_18131[1:]
                _x_18135 = [head_18133] + tail_18134
                _x_18136 = _alt_18124(head_18127, head_18130, _x_18135)
                return _x_18136

# Lean: Corpus.Geometry.orientation
def orientation(p_1320: Point2D, q_1321: Point2D, r_1322: Point2D) -> int:
    _x_18147 = q_1321.point2d_1
    _x_18148 = p_1320.point2d_1
    _x_18149 = _x_18147 - _x_18148
    _x_18150 = r_1322.point2d_0
    _x_18151 = q_1321.point2d_0
    _x_18152 = _x_18150 - _x_18151
    _x_18153 = _x_18149 * _x_18152
    _x_18154 = p_1320.point2d_0
    _x_18155 = _x_18151 - _x_18154
    _x_18156 = r_1322.point2d_1
    _x_18157 = _x_18156 - _x_18147
    _x_18158 = _x_18155 * _x_18157
    _x_18159 = _x_18153 - _x_18158
    _x_18162 = 0
    _x_18165 = _x_18159 == 0
    _x_18166 = True
    if _x_18165:
        return 0
    else:
        _x_18169 = float_dec_lt(0, _x_18159)
        if _x_18169:
            _x_18175 = 1
            return 1
        else:
            _x_18171 = 2
            return 2

# Lean: Corpus.Geometry.segmentsIntersect
def segments_intersect(p1_1324: Point2D, q1: Point2D, p2_1325: Point2D, q2: Point2D) -> bool:
    _x_18184 = orientation(p1_1324, q1, p2_1325)
    _x_18185 = orientation(p1_1324, q1, q2)
    _x_18186 = orientation(p2_1325, q2, p1_1324)
    _x_18187 = orientation(p2_1325, q2, q1)
    def _f_18189():
        _x_18188 = True
        return True
    _alt_18190 = _f_18189
    def _f_18208():
        def _f_18192():
            _x_18191 = False
            return False
        _alt_18193 = _f_18192
        def _f_18195():
            _x_18194 = on_segment(p2_1325, q1, q2)
            return _x_18194
        _alt_18196 = _f_18195
        _x_18199 = 0
        _x_18202 = _x_18187 == 0
        if _x_18202:
            _x_18206 = _alt_18196()
            return _x_18206
        else:
            _x_18204 = _alt_18193()
            return _x_18204
    _alt_18209 = _f_18208
    _alt_18210 = _f_18189
    def _f_18228():
        def _f_18212():
            _x_18211 = False
            return False
        _alt_18213 = _f_18212
        def _f_18215():
            _x_18214 = on_segment(p2_1325, p1_1324, q2)
            return _x_18214
        _alt_18216 = _f_18215
        _x_18219 = 0
        _x_18222 = _x_18186 == 0
        if _x_18222:
            _x_18226 = _alt_18216()
            return _x_18226
        else:
            _x_18224 = _alt_18213()
            return _x_18224
    _alt_18229 = _f_18228
    _alt_18230 = _f_18189
    def _f_18248():
        def _f_18232():
            _x_18231 = False
            return False
        _alt_18233 = _f_18232
        def _f_18235():
            _x_18234 = on_segment(p1_1324, q2, q1)
            return _x_18234
        _alt_18236 = _f_18235
        _x_18239 = 0
        _x_18242 = _x_18185 == 0
        if _x_18242:
            _x_18246 = _alt_18236()
            return _x_18246
        else:
            _x_18244 = _alt_18233()
            return _x_18244
    _alt_18249 = _f_18248
    _alt_18250 = _f_18189
    def _f_18268():
        def _f_18252():
            _x_18251 = False
            return False
        _alt_18253 = _f_18252
        def _f_18255():
            _x_18254 = on_segment(p1_1324, p2_1325, q1)
            return _x_18254
        _alt_18256 = _f_18255
        _x_18259 = 0
        _x_18262 = _x_18184 == 0
        if _x_18262:
            _x_18266 = _alt_18256()
            return _x_18266
        else:
            _x_18264 = _alt_18253()
            return _x_18264
    _alt_18269 = _f_18268
    def _f_18271():
        _x_18270 = False
        return False
    _alt_18272 = _f_18271
    def _f_18275():
        _x_18274 = (lambda a, b: a != b)(_x_18187)
        return _x_18274
    _alt_18276 = _f_18275
    _x_18278 = (lambda a, b: a != b)(_x_18185)
    def _jp_18325(_y_18283: bool):
        def _jp_18318(_y_18288: bool):
            def _jp_18311(_y_18293: bool):
                def _jp_18304(_y_18298: bool):
                    if _y_18298:
                        _x_18302 = _alt_18190()
                        return _x_18302
                    else:
                        _x_18300 = _alt_18209()
                        return _x_18300
                def _jp_18307():
                    _x_18306 = _alt_18229()
                    return _jp_18304(_x_18306)
                def _jp_18310():
                    _x_18309 = _alt_18210()
                    return _jp_18304(_x_18309)
                if _y_18293:
                    return _jp_18310()
                else:
                    return _jp_18307()
            def _jp_18314():
                _x_18313 = _alt_18249()
                return _jp_18311(_x_18313)
            def _jp_18317():
                _x_18316 = _alt_18230()
                return _jp_18311(_x_18316)
            if _y_18288:
                return _jp_18317()
            else:
                return _jp_18314()
        def _jp_18321():
            _x_18320 = _alt_18269()
            return _jp_18318(_x_18320)
        def _jp_18324():
            _x_18323 = _alt_18250()
            return _jp_18318(_x_18323)
        if _y_18283:
            return _jp_18324()
        else:
            return _jp_18321()
    def _jp_18331():
        _x_18330 = _alt_18276()
        return _jp_18325(_x_18330)
    def _jp_18328():
        _x_18327 = _alt_18272()
        return _jp_18325(_x_18327)
    if _x_18278:
        return _jp_18331()
    else:
        return _jp_18328()

# Lean: Corpus.Geometry.rotate2D
def rotate2d(p_1341: Point2D, angle: float) -> Point2D:
    _x_18333 = cos(angle)
    _x_18334 = sin(angle)
    _x_18341 = p_1341.point2d_0
    _x_18342 = _x_18341 * _x_18333
    _x_18343 = p_1341.point2d_1
    _x_18344 = _x_18343 * _x_18334
    _x_18345 = _x_18342 - _x_18344
    _x_18349 = _x_18341 * _x_18334
    _x_18350 = _x_18343 * _x_18333
    _x_18351 = _x_18349 + _x_18350
    _x_18352 = Point2D_mk(_x_18345, _x_18351)
    return _x_18352

# Lean: Corpus.Geometry.scale2D
def scale2d(p_1344: Point2D, factor: float) -> Point2D:
    _x_18357 = p_1344.point2d_0
    _x_18358 = _x_18357 * factor
    _x_18359 = p_1344.point2d_1
    _x_18360 = _x_18359 * factor
    _x_18361 = Point2D_mk(_x_18358, _x_18360)
    return _x_18361

# Lean: Corpus.Geometry.translate2D
def translate2d(p_1345: Point2D, dx_1346: float, dy_1347: float) -> Point2D:
    _x_18366 = p_1345.point2d_0
    _x_18367 = _x_18366 + dx_1346
    _x_18368 = p_1345.point2d_1
    _x_18369 = _x_18368 + dy_1347
    _x_18370 = Point2D_mk(_x_18367, _x_18369)
    return _x_18370

# Lean: Corpus.Geometry.reflectX
def reflect_x(p_1348: Point2D) -> Point2D:
    _x_18372 = p_1348.point2d_0
    _x_18375 = p_1348.point2d_1
    _x_18376 = -_x_18375
    _x_18377 = Point2D_mk(_x_18372, _x_18376)
    return _x_18377

# Lean: Corpus.Geometry.reflectY
def reflect_y(p_1349: Point2D) -> Point2D:
    _x_18381 = p_1349.point2d_0
    _x_18382 = -_x_18381
    _x_18383 = p_1349.point2d_1
    _x_18384 = Point2D_mk(_x_18382, _x_18383)
    return _x_18384

# Lean: Corpus.Geometry.angleBetween
def angle_between(v1: Point2D, v2: Point2D) -> float:
    _x_18386 = dot2d(v1, v2)
    _x_18387 = magnitude2d(v1)
    _x_18388 = magnitude2d(v2)
    def _f_18390():
        _x_18389 = True
        return True
    _alt_18391 = _f_18390
    def _f_18398():
        _x_18394 = 0
        _x_18397 = _x_18388 == 0
        return _x_18397
    _alt_18399 = _f_18398
    _x_18402 = 0
    _x_18405 = _x_18387 == 0
    def _jp_18425(_y_18410: bool):
        _x_18411 = True
        if _y_18410:
            return 0
        else:
            _x_18420 = _x_18387 * _x_18388
            _x_18421 = _x_18386 // _x_18420
            _x_18422 = acos(_x_18421)
            return _x_18422
    def _jp_18428():
        _x_18427 = _alt_18399()
        return _jp_18425(_x_18427)
    def _jp_18431():
        _x_18430 = _alt_18391()
        return _jp_18425(_x_18430)
    if _x_18405:
        return _jp_18431()
    else:
        return _jp_18428()

# Lean: Corpus.Geometry.projectOntoLine
def project_onto_line(p_1352: Point2D, a_1353: Point2D, b_1354: Point2D) -> Point2D:
    _x_18436 = p_1352.point2d_0
    _x_18437 = a_1353.point2d_0
    _x_18438 = _x_18436 - _x_18437
    _x_18439 = p_1352.point2d_1
    _x_18440 = a_1353.point2d_1
    _x_18441 = _x_18439 - _x_18440
    _x_18442 = Point2D_mk(_x_18438, _x_18441)
    _x_18443 = b_1354.point2d_0
    _x_18444 = _x_18443 - _x_18437
    _x_18445 = b_1354.point2d_1
    _x_18446 = _x_18445 - _x_18440
    _x_18447 = Point2D_mk(_x_18444, _x_18446)
    _x_18451 = dot2d(_x_18442, _x_18447)
    _x_18452 = dot2d(_x_18447, _x_18447)
    _x_18453 = _x_18451 // _x_18452
    _x_18460 = _x_18447.point2d_0
    _x_18461 = _x_18453 * _x_18460
    _x_18462 = _x_18437 + _x_18461
    _x_18463 = _x_18447.point2d_1
    _x_18464 = _x_18453 * _x_18463
    _x_18465 = _x_18440 + _x_18464
    _x_18466 = Point2D_mk(_x_18462, _x_18465)
    return _x_18466

# Lean: Corpus.Geometry.distanceToLine
def distance_to_line(p_1356: Point2D, a_1357: Point2D, b_1358: Point2D) -> float:
    _x_18468 = project_onto_line(p_1356, a_1357, b_1358)
    _x_18469 = dist2d(p_1356, _x_18468)
    return _x_18469

# Lean: Corpus.Combinatorics.doubleFactorial
def double_factorial(n_1359: int) -> int:
    _x_18471 = 1
    _x_18474 = n_1359 <= 1
    if _x_18474:
        return 1
    else:
        _x_18482 = 2
        _x_18485 = n_1359 - 2
        _x_18486 = double_factorial(_x_18485)
        _x_18487 = n_1359 * _x_18486
        return _x_18487

# Lean: Corpus.Combinatorics.risingFactorial
def rising_factorial(x_1360: int, n_1361: int) -> int:
    _x_18491 = 0
    _x_18494 = 1
    _x_18497 = rising_factorial_go(x_1360, n_1361, 0, 1)
    return _x_18497

# Lean: Corpus.Combinatorics.fallingFactorial
def falling_factorial(x_1362: int, n_1363: int) -> int:
    _x_18499 = 0
    _x_18502 = 1
    _x_18505 = falling_factorial_go(x_1362, n_1363, 0, 1)
    return _x_18505

# Lean: Corpus.Combinatorics.multinomial
def multinomial(n_1364: int, ks: list[int]) -> int:
    def _f_18513(x1_18507: int, x2_18508: int):
        _x_18512 = x1_18507 + x2_18508
        return _x_18512
    _x_18514 = 0
    _x_18517 = functools.reduce(_f_18513, ks, 0)
    _x_18519 = (lambda a, b: a != b)(n_1364)
    _x_18520 = True
    if _x_18519:
        return 0
    else:
        _x_18523 = factorial(n_1364)
        def _f_18529(acc_1366: int, k_1367: int):
            _x_18527 = factorial(k_1367)
            _x_18528 = acc_1366 * _x_18527
            return _x_18528
        _x_18530 = 1
        _x_18533 = functools.reduce(_f_18529, ks, 1)
        _x_18537 = _x_18523 // _x_18533
        return _x_18537

# Lean: Corpus.Combinatorics.stirling1
def stirling1(n_1369: int, k_1370: int) -> int:
    _x_18543 = 0
    _x_18546 = k_1370 == 0
    _x_18547 = True
    if _x_18546:
        _x_18574 = n_1369 == 0
        if _x_18574:
            _x_18578 = 1
            return 1
        else:
            return 0
    else:
        _x_18550 = n_1369 == 0
        if _x_18550:
            return 0
        else:
            _x_18562 = 1
            _x_18565 = n_1369 - 1
            _x_18566 = stirling1(_x_18565, k_1370)
            _x_18567 = _x_18565 * _x_18566
            _x_18568 = k_1370 - 1
            _x_18569 = stirling1(_x_18565, _x_18568)
            _x_18570 = _x_18567 + _x_18569
            return _x_18570

# Lean: Corpus.Combinatorics.stirling2
def stirling2(n_1371: int, k_1372: int) -> int:
    _x_18586 = 0
    _x_18589 = k_1372 == 0
    _x_18590 = True
    if _x_18589:
        _x_18617 = n_1371 == 0
        if _x_18617:
            _x_18621 = 1
            return 1
        else:
            return 0
    else:
        _x_18593 = n_1371 == 0
        if _x_18593:
            return 0
        else:
            _x_18605 = 1
            _x_18608 = n_1371 - 1
            _x_18609 = stirling2(_x_18608, k_1372)
            _x_18610 = k_1372 * _x_18609
            _x_18611 = k_1372 - 1
            _x_18612 = stirling2(_x_18608, _x_18611)
            _x_18613 = _x_18610 + _x_18612
            return _x_18613

# Lean: Corpus.Combinatorics.bell
def bell(n_1373: int) -> int:
    _x_18627 = 0
    _x_18630 = bell_go(n_1373, 0, 0)
    return _x_18630

# Lean: Corpus.Combinatorics.catalan
def catalan(n_1374: int) -> int:
    _x_18638 = 2
    _x_18641 = 2 * n_1374
    _x_18642 = binomial(_x_18641, n_1374)
    _x_18646 = 1
    _x_18649 = n_1374 + 1
    _x_18650 = _x_18642 // _x_18649
    return _x_18650

# Lean: Corpus.Combinatorics.derangement
def derangement(n_1375: int) -> int:
    _x_18654 = 0
    _x_18657 = n_1375 == 0
    _x_18658 = True
    if _x_18657:
        _x_18688 = 1
        return 1
    else:
        _x_18661 = 1
        _x_18664 = n_1375 == 1
        if _x_18664:
            return 0
        else:
            _x_18673 = n_1375 - 1
            _x_18677 = derangement(_x_18673)
            _x_18678 = 2
            _x_18681 = n_1375 - 2
            _x_18682 = derangement(_x_18681)
            _x_18683 = _x_18677 + _x_18682
            _x_18684 = _x_18673 * _x_18683
            return _x_18684

# Lean: Corpus.Combinatorics.partitionCount
def partition_count(n_1376: int) -> int:
    _x_18693 = p(n_1376, n_1376)
    return _x_18693

# Lean: Corpus.Combinatorics.permutations
def permutations(__1377: Any, inst_18695: Any, xs_1378: list[Any]) -> list[list[Any]]:
    def _f_18699():
        _x_18696 = []
        _x_18697 = []
        _x_18698 = [_x_18696] + _x_18697
        return _x_18698
    _alt_18700 = _f_18699
    def _f_18705(x_1380: Any):
        _x_18701 = []
        _x_18702 = [x_1380] + _x_18701
        _x_18703 = []
        _x_18704 = [_x_18702] + _x_18703
        return _x_18704
    _alt_18706 = _f_18705
    def _f_18719(x_18707: list[Any]):
        def _f_18717(x_1381: Any):
            def _f_18710(x_18708: list[Any]):
                _x_18709 = [x_1381] + x_18708
                return _x_18709
            def _f_18713(x_18711: Any):
                _x_18712 = (lambda a, b: a != b)(x_1381)
                return _x_18712
            _x_18714 = [x for x in xs_1378 if _f_18713(x)]
            _x_18715 = permutations(None, inst_18695, _x_18714)
            _x_18716 = [_f_18710(x) for x in _x_18715]
            return _x_18716
        _x_18718 = [y for x in xs_1378 for y in _f_18717(x)]
        return _x_18718
    _alt_18720 = _f_18719
    if len(xs_1378) == 0:
        _x_18722 = _alt_18700()
        return _x_18722
    else:
        head_18723 = xs_1378[0]
        tail_18724 = xs_1378[1:]
        if len(tail_18724) == 0:
            _x_18725 = _alt_18706(head_18723)
            return _x_18725
        else:
            head_18726 = tail_18724[0]
            tail_18727 = tail_18724[1:]
            _x_18728 = [head_18726] + tail_18727
            _x_18729 = [head_18723] + _x_18728
            _x_18730 = _alt_18720(_x_18729)
            return _x_18730

# Lean: Corpus.Combinatorics.combinations
def combinations(__1382: Any, k_1383: int, xs_1384: list[Any]) -> list[list[Any]]:
    _x_18736 = 0
    _x_18739 = k_1383 == 0
    _x_18740 = True
    if _x_18739:
        _x_18772 = []
        _x_18773 = []
        _x_18774 = [_x_18772] + _x_18773
        return _x_18774
    else:
        def _f_18744():
            _x_18743 = []
            return _x_18743
        _alt_18745 = _f_18744
        def _f_18763(x_1386: Any, rest_1387: list[Any]):
            def _f_18751(x_18749: list[Any]):
                _x_18750 = [x_1386] + x_18749
                return _x_18750
            _x_18755 = 1
            _x_18758 = k_1383 - 1
            _x_18759 = combinations(None, _x_18758, rest_1387)
            _x_18760 = [_f_18751(x) for x in _x_18759]
            _x_18761 = combinations(None, k_1383, rest_1387)
            _x_18762 = _x_18760 + _x_18761
            return _x_18762
        _alt_18764 = _f_18763
        if len(xs_1384) == 0:
            _x_18766 = _alt_18745()
            return _x_18766
        else:
            head_18767 = xs_1384[0]
            tail_18768 = xs_1384[1:]
            _x_18769 = _alt_18764(head_18767, tail_18768)
            return _x_18769

# Lean: Corpus.Combinatorics.powerSet
def power_set(__1388: Any, xs_1389: list[Any]) -> list[list[Any]]:
    def _f_18780():
        _x_18777 = []
        _x_18778 = []
        _x_18779 = [_x_18777] + _x_18778
        return _x_18779
    _alt_18781 = _f_18780
    def _f_18791(x_1391: Any, rest_1392: list[Any]):
        _x_18782 = power_set(None, rest_1392)
        def _f_18788(x_18786: list[Any]):
            _x_18787 = [x_1391] + x_18786
            return _x_18787
        _x_18789 = [_f_18788(x) for x in _x_18782]
        _x_18790 = _x_18782 + _x_18789
        return _x_18790
    _alt_18792 = _f_18791
    if len(xs_1389) == 0:
        _x_18794 = _alt_18781()
        return _x_18794
    else:
        head_18795 = xs_1389[0]
        tail_18796 = xs_1389[1:]
        _x_18797 = _alt_18792(head_18795, tail_18796)
        return _x_18797

# Lean: Corpus.Combinatorics.countInversions
def count_inversions(xs_1393: list[int]) -> int:
    _x_18800 = count(xs_1393)
    return _x_18800

# Lean: Corpus.Combinatorics.isEvenPermutation
def is_even_permutation(xs_1394: list[int]) -> bool:
    _x_18807 = count_inversions(xs_1394)
    _x_18808 = 2
    _x_18811 = _x_18807 % 2
    _x_18812 = 0
    _x_18815 = _x_18811 == 0
    return _x_18815

# Lean: Corpus.Combinatorics.lehmerCode
def lehmer_code(perm_1395: list[int]) -> list[int]:
    _x_18817 = []
    _x_18818 = lehmer_code_go(perm_1395, _x_18817)
    return _x_18818

# Lean: Corpus.Combinatorics.fromLehmerCode
def from_lehmer_code(code_1396: list[int]) -> list[int]:
    _x_18820 = len(code_1396)
    _x_18821 = list(range(_x_18820))
    _x_18822 = []
    _x_18823 = from_lehmer_code_go(code_1396, _x_18821, _x_18822)
    return _x_18823

# Lean: Corpus.Combinatorics.nthPermutation
def nth_permutation(n_1398: int, k_1399: int) -> list[int]:
    _x_18825 = list(range(n_1398))
    _x_18826 = []
    _x_18827 = nth_permutation_go(k_1399, n_1398, _x_18825, _x_18826)
    return _x_18827

# Lean: Corpus.Combinatorics.permutationRank
def permutation_rank(perm_1400: list[int]) -> int:
    _x_18829 = lehmer_code(perm_1400)
    _x_18830 = len(_x_18829)
    _x_18831 = 0
    _x_18834 = permutation_rank_go(_x_18830, _x_18829, 0, 0)
    return _x_18834

# Lean: Corpus.Combinatorics.nextPermutation
def next_permutation(perm_1403: list[int]) -> list[int] | None:
    _x_18836 = list(perm_1403)
    _x_18837 = len(_x_18836)
    def _f_18839():
        _x_18838 = None
        return _x_18838
    _alt_18840 = _f_18839
    def _f_18853(i_1407: int):
        _x_18841 = find_j(_x_18836, i_1407, _x_18837)
        _x_18842 = swap_(None, _x_18836, i_1407, _x_18841)
        _x_18846 = 1
        _x_18849 = i_1407 + 1
        _x_18850 = reverse_from(_x_18842, _x_18849)
        _x_18851 = list(_x_18850)
        _x_18852 = _x_18851
        return _x_18852
    _alt_18854 = _f_18853
    _x_18858 = 1
    _x_18861 = _x_18837 - 1
    _x_18862 = find_i(_x_18836, _x_18861)
    if _x_18862 is None:
        _x_18864 = _alt_18840()
        return _x_18864
    else:
        val_18865 = _x_18862
        _x_18866 = _alt_18854(val_18865)
        return _x_18866

# Lean: Corpus.Combinatorics.prevPermutation
def prev_permutation(perm_1411: list[int]) -> list[int] | None:
    _x_18869 = list(perm_1411)
    _x_18870 = len(_x_18869)
    def _f_18872():
        _x_18871 = None
        return _x_18871
    _alt_18873 = _f_18872
    def _f_18886(i_1415: int):
        _x_18874 = find_j(_x_18869, i_1415, _x_18870)
        _x_18875 = swap_(None, _x_18869, i_1415, _x_18874)
        _x_18879 = 1
        _x_18882 = i_1415 + 1
        _x_18883 = reverse_from(_x_18875, _x_18882)
        _x_18884 = list(_x_18883)
        _x_18885 = _x_18884
        return _x_18885
    _alt_18887 = _f_18886
    _x_18891 = 1
    _x_18894 = _x_18870 - 1
    _x_18895 = find_i(_x_18869, _x_18894)
    if _x_18895 is None:
        _x_18897 = _alt_18873()
        return _x_18897
    else:
        val_18898 = _x_18895
        _x_18899 = _alt_18887(val_18898)
        return _x_18899

# Lean: Corpus.Combinatorics.compositions
def compositions(n_1419: int) -> list[list[int]]:
    _x_18904 = 0
    _x_18907 = n_1419 == 0
    _x_18908 = True
    if _x_18907:
        _x_18917 = []
        _x_18918 = []
        _x_18919 = [_x_18917] + _x_18918
        return _x_18919
    else:
        _x_18911 = 1
        _x_18914 = []
        _x_18915 = compositions_go(n_1419, 1, _x_18914)
        return _x_18915

# Lean: Corpus.Combinatorics.integerPartitions
def integer_partitions(n_1420: int) -> list[list[int]]:
    _x_18922 = integer_partitions_go(n_1420, n_1420)
    return _x_18922

# Lean: Corpus.Sequences.fibonacci
def sequences_fibonacci(n_1421: int) -> int:
    _x_18924 = 0
    _x_18927 = 1
    _x_18930 = sequences_fibonacci_go(n_1421, 0, 1)
    return _x_18930

# Lean: Corpus.Sequences.lucas
def lucas(n_1422: int) -> int:
    _x_18932 = 2
    _x_18935 = 1
    _x_18938 = lucas_go(n_1422, 2, 1)
    return _x_18938

# Lean: Corpus.Sequences.tribonacci
def tribonacci(n_1423: int) -> int:
    _x_18940 = 0
    _x_18943 = 1
    _x_18946 = tribonacci_go(n_1423, 0, 0, 1)
    return _x_18946

# Lean: Corpus.Sequences.pell
def pell(n_1424: int) -> int:
    _x_18948 = 0
    _x_18951 = 1
    _x_18954 = pell_go(n_1424, 0, 1)
    return _x_18954

# Lean: Corpus.Sequences.padovan
def padovan(n_1425: int) -> int:
    _x_18956 = 1
    _x_18959 = padovan_go(n_1425, 1, 1, 1)
    return _x_18959

# Lean: Corpus.Sequences.perrin
def perrin(n_1426: int) -> int:
    _x_18961 = 3
    _x_18964 = 0
    _x_18967 = 2
    _x_18970 = perrin_go(n_1426, 3, 0, 2)
    return _x_18970

# Lean: Corpus.Sequences.jacobsthal
def jacobsthal(n_1427: int) -> int:
    _x_18972 = 0
    _x_18975 = 1
    _x_18978 = jacobsthal_go(n_1427, 0, 1)
    return _x_18978

# Lean: Corpus.Sequences.motzkin
def motzkin(n_1428: int) -> int:
    _x_18982 = 0
    _x_18985 = n_1428 == 0
    _x_18986 = True
    if _x_18985:
        _x_19008 = 1
        return 1
    else:
        _x_18989 = 1
        _x_18992 = n_1428 == 1
        if _x_18992:
            return 1
        else:
            _x_19001 = n_1428 - 1
            _x_19002 = motzkin(_x_19001)
            _x_19003 = motzkin_go(n_1428, 0, 0)
            _x_19004 = _x_19002 + _x_19003
            return _x_19004

# Lean: Corpus.Sequences.narayana
def narayana(n_1429: int, k_1430: int) -> int:
    def _f_19014():
        _x_19013 = True
        return True
    _alt_19015 = _f_19014
    def _f_19018():
        _x_19016 = n_1429 < k_1430
        return _x_19016
    _alt_19019 = _f_19018
    _x_19022 = 0
    _x_19025 = k_1430 == 0
    def _jp_19053(_y_19030: bool):
        _x_19031 = True
        if _y_19030:
            return 0
        else:
            _x_19040 = binomial(n_1429, k_1430)
            _x_19044 = 1
            _x_19047 = k_1430 - 1
            _x_19048 = binomial(n_1429, _x_19047)
            _x_19049 = _x_19040 * _x_19048
            _x_19050 = _x_19049 // n_1429
            return _x_19050
    def _jp_19056():
        _x_19055 = _alt_19019()
        return _jp_19053(_x_19055)
    def _jp_19059():
        _x_19058 = _alt_19015()
        return _jp_19053(_x_19058)
    if _x_19025:
        return _jp_19059()
    else:
        return _jp_19056()

# Lean: Corpus.Sequences.triangular
def triangular(n_1433: int) -> int:
    _x_19070 = 1
    _x_19073 = n_1433 + 1
    _x_19074 = n_1433 * _x_19073
    _x_19075 = 2
    _x_19078 = _x_19074 // 2
    return _x_19078

# Lean: Corpus.Sequences.square
def square(n_1434: int) -> int:
    _x_19083 = n_1434 * n_1434
    return _x_19083

# Lean: Corpus.Sequences.pentagonal
def pentagonal(n_1435: int) -> int:
    _x_19094 = 3
    _x_19097 = 3 * n_1435
    _x_19098 = 1
    _x_19101 = _x_19097 - 1
    _x_19102 = n_1435 * _x_19101
    _x_19103 = 2
    _x_19106 = _x_19102 // 2
    return _x_19106

# Lean: Corpus.Sequences.hexagonal
def hexagonal(n_1436: int) -> int:
    _x_19114 = 2
    _x_19117 = 2 * n_1436
    _x_19118 = 1
    _x_19121 = _x_19117 - 1
    _x_19122 = n_1436 * _x_19121
    return _x_19122

# Lean: Corpus.Sequences.heptagonal
def heptagonal(n_1437: int) -> int:
    _x_19133 = 5
    _x_19136 = 5 * n_1437
    _x_19137 = 3
    _x_19140 = _x_19136 - 3
    _x_19141 = n_1437 * _x_19140
    _x_19142 = 2
    _x_19145 = _x_19141 // 2
    return _x_19145

# Lean: Corpus.Sequences.octagonal
def octagonal(n_1438: int) -> int:
    _x_19153 = 3
    _x_19156 = 3 * n_1438
    _x_19157 = 2
    _x_19160 = _x_19156 - 2
    _x_19161 = n_1438 * _x_19160
    return _x_19161

# Lean: Corpus.Sequences.kGonal
def k_gonal(k_1439: int, n_1440: int) -> int:
    _x_19172 = 2
    _x_19175 = k_1439 - 2
    _x_19176 = _x_19175 * n_1440
    _x_19177 = 4
    _x_19180 = k_1439 - 4
    _x_19181 = _x_19176 - _x_19180
    _x_19182 = n_1440 * _x_19181
    _x_19183 = _x_19182 // 2
    return _x_19183

# Lean: Corpus.Sequences.tetrahedral
def tetrahedral(n_1441: int) -> int:
    _x_19194 = 1
    _x_19197 = n_1441 + 1
    _x_19198 = n_1441 * _x_19197
    _x_19199 = 2
    _x_19202 = n_1441 + 2
    _x_19203 = _x_19198 * _x_19202
    _x_19204 = 6
    _x_19207 = _x_19203 // 6
    return _x_19207

# Lean: Corpus.Sequences.pyramidal
def pyramidal(n_1442: int) -> int:
    _x_19218 = 1
    _x_19221 = n_1442 + 1
    _x_19222 = n_1442 * _x_19221
    _x_19223 = 2
    _x_19226 = 2 * n_1442
    _x_19227 = _x_19226 + 1
    _x_19228 = _x_19222 * _x_19227
    _x_19229 = 6
    _x_19232 = _x_19228 // 6
    return _x_19232

# Lean: Corpus.Sequences.centeredTriangular
def centered_triangular(n_1443: int) -> int:
    _x_19243 = 3
    _x_19246 = 3 * n_1443
    _x_19247 = _x_19246 * n_1443
    _x_19248 = _x_19247 + _x_19246
    _x_19249 = 2
    _x_19252 = _x_19248 + 2
    _x_19253 = _x_19252 // 2
    return _x_19253

# Lean: Corpus.Sequences.centeredSquare
def centered_square(n_1444: int) -> int:
    _x_19261 = n_1444 * n_1444
    _x_19262 = 1
    _x_19265 = n_1444 + 1
    _x_19266 = _x_19265 * _x_19265
    _x_19267 = _x_19261 + _x_19266
    return _x_19267

# Lean: Corpus.Sequences.centeredHexagonal
def centered_hexagonal(n_1445: int) -> int:
    _x_19275 = 3
    _x_19278 = 3 * n_1445
    _x_19282 = 1
    _x_19285 = n_1445 - 1
    _x_19286 = _x_19278 * _x_19285
    _x_19287 = _x_19286 + 1
    return _x_19287

# Lean: Corpus.Sequences.starNumber
def star_number(n_1446: int) -> int:
    _x_19295 = 6
    _x_19298 = 6 * n_1446
    _x_19302 = 1
    _x_19305 = n_1446 - 1
    _x_19306 = _x_19298 * _x_19305
    _x_19307 = _x_19306 + 1
    return _x_19307

# Lean: Corpus.Sequences.pronic
def pronic(n_1447: int) -> int:
    _x_19315 = 1
    _x_19318 = n_1447 + 1
    _x_19319 = n_1447 * _x_19318
    return _x_19319

# Lean: Corpus.Sequences.cullen
def cullen(n_1448: int) -> int:
    _x_19331 = 2
    _x_19334 = 2 ** n_1448
    _x_19335 = n_1448 * _x_19334
    _x_19336 = 1
    _x_19339 = _x_19335 + 1
    return _x_19339

# Lean: Corpus.Sequences.woodall
def woodall(n_1449: int) -> int:
    _x_19351 = 2
    _x_19354 = 2 ** n_1449
    _x_19355 = n_1449 * _x_19354
    _x_19356 = 1
    _x_19359 = _x_19355 - 1
    return _x_19359

# Lean: Corpus.Sequences.mersenne
def mersenne(n_1450: int) -> int:
    _x_19368 = 2
    _x_19371 = 2 ** n_1450
    _x_19372 = 1
    _x_19375 = _x_19371 - 1
    return _x_19375

# Lean: Corpus.Sequences.fermat
def fermat(n_1451: int) -> int:
    _x_19384 = 2
    _x_19387 = 2 ** n_1451
    _x_19388 = 2 ** _x_19387
    _x_19389 = 1
    _x_19392 = _x_19388 + 1
    return _x_19392

# Lean: Corpus.Sequences.safeFromGermain
def safe_from_germain(p_1452: int) -> int:
    _x_19400 = 2
    _x_19403 = 2 * p_1452
    _x_19404 = 1
    _x_19407 = _x_19403 + 1
    return _x_19407

# Lean: Corpus.Sequences.repunit
def repunit(n_1453: int) -> int:
    _x_19409 = 0
    _x_19412 = repunit_go(n_1453, 0)
    return _x_19412

# Lean: Corpus.Sequences.lookAndSayNext
def look_and_say_next(xs_1454: list[int]) -> list[int]:
    def _f_19415():
        _x_19414 = []
        return _x_19414
    _alt_19416 = _f_19415
    def _f_19423(x_1456: int, rest_1457: list[int]):
        _x_19417 = 1
        _x_19420 = []
        _x_19421 = look_and_say_next_go(rest_1457, x_1456, 1, _x_19420)
        _x_19422 = list(reversed(_x_19421))
        return _x_19422
    _alt_19424 = _f_19423
    if len(xs_1454) == 0:
        _x_19426 = _alt_19416()
        return _x_19426
    else:
        head_19427 = xs_1454[0]
        tail_19428 = xs_1454[1:]
        _x_19429 = _alt_19424(head_19427, tail_19428)
        return _x_19429

# Lean: Corpus.Sequences.collatzSequence
def collatz_sequence(n_1458: int) -> list[int]:
    _x_19432 = 1
    _x_19435 = n_1458 <= 1
    if _x_19435:
        _x_19474 = []
        _x_19475 = [n_1458] + _x_19474
        return _x_19475
    else:
        _x_19442 = 2
        _x_19445 = n_1458 % 2
        _x_19446 = 0
        _x_19449 = _x_19445 == 0
        _x_19450 = True
        def _jp_19472(_y_19469: int):
            _x_19470 = collatz_sequence(_y_19469)
            _x_19471 = [n_1458] + _x_19470
            return _x_19471
        if _x_19449:
            _x_19468 = n_1458 // 2
            return _jp_19472(_x_19468)
        else:
            _x_19459 = 3
            _x_19462 = 3 * n_1458
            _x_19463 = _x_19462 + 1
            return _jp_19472(_x_19463)

# Lean: Corpus.Sequences.recaman
def recaman(n_1459: int) -> list[int]:
    _x_19478 = 1
    _x_19481 = 0
    _x_19484 = []
    _x_19485 = [0] + _x_19484
    _x_19486 = recaman_go(n_1459, 1, 0, _x_19485, _x_19485)
    return _x_19486

# Lean: Corpus.Sequences.sylvester
def sylvester(n_1460: int) -> int:
    _x_19490 = 0
    _x_19493 = n_1460 == 0
    _x_19494 = True
    if _x_19493:
        _x_19515 = 2
        return 2
    else:
        _x_19500 = 1
        _x_19503 = n_1460 - 1
        _x_19504 = sylvester(_x_19503)
        _x_19511 = _x_19504 * _x_19504
        _x_19512 = _x_19511 - _x_19504
        _x_19513 = _x_19512 + 1
        return _x_19513

# Lean: Corpus.Sequences.alcuin
def alcuin(n_1462: int) -> int:
    _x_19525 = 12
    _x_19528 = n_1462 % 12
    _x_19529 = 0
    _x_19532 = _x_19528 == 0
    _x_19533 = True
    if _x_19532:
        _x_19615 = n_1462 * n_1462
        _x_19616 = _x_19615 // 12
        return _x_19616
    else:
        def _f_19536():
            return True
        _alt_19537 = _f_19536
        def _f_19542():
            _x_19538 = 9
            _x_19541 = _x_19528 == 9
            return _x_19541
        _alt_19543 = _f_19542
        _x_19544 = 3
        _x_19547 = _x_19528 == 3
        def _jp_19601(_y_19552: bool):
            if _y_19552:
                _x_19597 = n_1462 * n_1462
                _x_19598 = _x_19597 - 3
                _x_19599 = _x_19598 // 12
                return _x_19599
            else:
                _x_19555 = 6
                _x_19558 = _x_19528 == 6
                if _x_19558:
                    _x_19583 = n_1462 * n_1462
                    _x_19584 = _x_19583 - 12
                    _x_19585 = _x_19584 // 12
                    return _x_19585
                else:
                    _x_19570 = n_1462 * n_1462
                    _x_19571 = _x_19570 + 3
                    _x_19572 = _x_19571 // 12
                    return _x_19572
        def _jp_19607():
            _x_19606 = _alt_19537()
            return _jp_19601(_x_19606)
        def _jp_19604():
            _x_19603 = _alt_19543()
            return _jp_19601(_x_19603)
        if _x_19547:
            return _jp_19607()
        else:
            return _jp_19604()

# Lean: Corpus.Sequences.firstNPrimes
def first_nprimes(n_1465: int) -> list[int]:
    _x_19619 = 2
    _x_19622 = []
    _x_19623 = first_nprimes_go(n_1465, 2, _x_19622)
    return _x_19623

# Lean: Corpus.Sequences.vanEck
def van_eck(n_1466: int) -> list[int]:
    _x_19625 = 1
    _x_19628 = 0
    _x_19631 = []
    _x_19632 = []
    _x_19633 = [0] + _x_19632
    _x_19634 = van_eck_go(n_1466, 1, 0, _x_19631, _x_19633)
    return _x_19634

# Lean: Corpus.Sorting.bubbleSort
def bubble_sort(xs_1467: list[int]) -> list[int]:
    _x_19636 = len(xs_1467)
    _x_19637 = list(xs_1467)
    _x_19638 = 0
    _x_19641 = outer(_x_19636, 0, _x_19637)
    _x_19642 = list(_x_19641)
    return _x_19642

# Lean: Corpus.Sorting.selectionSort
def selection_sort(xs_1470: list[int]) -> list[int]:
    _x_19644 = len(xs_1470)
    _x_19645 = list(xs_1470)
    _x_19646 = 0
    _x_19649 = selection_sort_go(_x_19644, 0, _x_19645)
    _x_19650 = list(_x_19649)
    return _x_19650

# Lean: Corpus.Sorting.countingSort
def counting_sort(xs_1473: list[int], max_val_1474: int) -> list[int]:
    def _f_19664(arr_1475: list[int], x_1476: int):
        _x_19655 = 0
        _x_19658 = get_d(None, arr_1475, x_1476, 0)
        _x_19659 = 1
        _x_19662 = _x_19658 + 1
        _x_19663 = set_(None, arr_1475, x_1476, _x_19662)
        return _x_19663
    _x_19668 = 1
    _x_19671 = max_val_1474 + 1
    _x_19672 = 0
    _x_19675 = mk_array(None, _x_19671, 0)
    _x_19676 = functools.reduce(_f_19664, xs_1473, _x_19675)
    _x_19677 = []
    _x_19678 = expand(max_val_1474, _x_19676, 0, _x_19677)
    return _x_19678

# Lean: Corpus.Sorting.radixSort
def radix_sort(xs_1478: list[int]) -> list[int]:
    _x_19681 = max
    _x_19682 = 0
    _x_19685 = functools.reduce(_x_19681, xs_1478, 0)
    _x_19686 = 1
    _x_19689 = radix_sort_go(_x_19685, 1, xs_1478)
    return _x_19689

# Lean: Corpus.Sorting.gnomeSort
def gnome_sort(xs_1480: list[int]) -> list[int]:
    _x_19691 = len(xs_1480)
    _x_19692 = list(xs_1480)
    _x_19693 = 0
    _x_19696 = gnome_sort_go(_x_19691, 0, _x_19692)
    _x_19697 = list(_x_19696)
    return _x_19697

# Lean: Corpus.Sorting.isSorted
def is_sorted(xs_1483: list[int]) -> bool:
    def _f_19700():
        _x_19699 = True
        return True
    _alt_19701 = _f_19700
    def _f_19704(head_19702: int):
        _x_19703 = True
        return True
    _alt_19705 = _f_19704
    def _f_19720(x_1485: int, y_1486: int, rest_1487: list[int]):
        def _f_19707():
            _x_19706 = False
            return False
        _alt_19708 = _f_19707
        def _f_19711():
            _x_19709 = [y_1486] + rest_1487
            _x_19710 = is_sorted(_x_19709)
            return _x_19710
        _alt_19712 = _f_19711
        _x_19713 = x_1485 <= y_1486
        if _x_19713:
            _x_19718 = _alt_19712()
            return _x_19718
        else:
            _x_19716 = _alt_19708()
            return _x_19716
    _alt_19721 = _f_19720
    if len(xs_1483) == 0:
        _x_19723 = _alt_19701()
        return _x_19723
    else:
        head_19724 = xs_1483[0]
        tail_19725 = xs_1483[1:]
        if len(tail_19725) == 0:
            _x_19726 = _alt_19705(head_19724)
            return _x_19726
        else:
            head_19727 = tail_19725[0]
            tail_19728 = tail_19725[1:]
            _x_19729 = _alt_19721(head_19724, head_19727, tail_19728)
            return _x_19729

# Lean: Corpus.Sorting.isSortedDesc
def is_sorted_desc(xs_1490: list[int]) -> bool:
    def _f_19734():
        _x_19733 = True
        return True
    _alt_19735 = _f_19734
    def _f_19738(head_19736: int):
        _x_19737 = True
        return True
    _alt_19739 = _f_19738
    def _f_19754(x_1492: int, y_1493: int, rest_1494: list[int]):
        def _f_19741():
            _x_19740 = False
            return False
        _alt_19742 = _f_19741
        def _f_19745():
            _x_19743 = [y_1493] + rest_1494
            _x_19744 = is_sorted_desc(_x_19743)
            return _x_19744
        _alt_19746 = _f_19745
        _x_19747 = y_1493 <= x_1492
        if _x_19747:
            _x_19752 = _alt_19746()
            return _x_19752
        else:
            _x_19750 = _alt_19742()
            return _x_19750
    _alt_19755 = _f_19754
    if len(xs_1490) == 0:
        _x_19757 = _alt_19735()
        return _x_19757
    else:
        head_19758 = xs_1490[0]
        tail_19759 = xs_1490[1:]
        if len(tail_19759) == 0:
            _x_19760 = _alt_19739(head_19758)
            return _x_19760
        else:
            head_19761 = tail_19759[0]
            tail_19762 = tail_19759[1:]
            _x_19763 = _alt_19755(head_19758, head_19761, tail_19762)
            return _x_19763

# Lean: Corpus.Sorting.findMin
def find_min(xs_1497: list[int]) -> int | None:
    def _f_19787(acc_1498: int | None, x_1499: int):
        def _f_19767():
            return x_1499
        _alt_19768 = _f_19767
        def _f_19772(m_1501: int):
            _x_19770 = min
            _x_19771 = _x_19770(m_1501, x_1499)
            return _x_19771
        _alt_19773 = _f_19772
        def _jp_19780(_y_19778: int):
            _x_19779 = _y_19778
            return _x_19779
        def _jp_19786(_y_19784: int):
            _x_19785 = _alt_19773(_y_19784)
            return _jp_19780(_x_19785)
        def _jp_19783():
            _x_19782 = _alt_19768()
            return _jp_19780(_x_19782)
        if acc_1498 is None:
            return _jp_19783()
        else:
            val_19776 = acc_1498
            return _jp_19786(val_19776)
    _x_19788 = None
    _x_19789 = functools.reduce(_f_19787, xs_1497, _x_19788)
    return _x_19789

# Lean: Corpus.Sorting.findMax
def find_max(xs_1502: list[int]) -> int | None:
    def _f_19811(acc_1503: int | None, x_1504: int):
        def _f_19791():
            return x_1504
        _alt_19792 = _f_19791
        def _f_19796(m_1506: int):
            _x_19794 = max
            _x_19795 = _x_19794(m_1506, x_1504)
            return _x_19795
        _alt_19797 = _f_19796
        def _jp_19804(_y_19802: int):
            _x_19803 = _y_19802
            return _x_19803
        def _jp_19810(_y_19808: int):
            _x_19809 = _alt_19797(_y_19808)
            return _jp_19804(_x_19809)
        def _jp_19807():
            _x_19806 = _alt_19792()
            return _jp_19804(_x_19806)
        if acc_1503 is None:
            return _jp_19807()
        else:
            val_19800 = acc_1503
            return _jp_19810(val_19800)
    _x_19812 = None
    _x_19813 = functools.reduce(_f_19811, xs_1502, _x_19812)
    return _x_19813

# Lean: Corpus.Sorting.kthSmallest
def kth_smallest(xs_1507: list[int], k_1508: int) -> int | None:
    _x_19815 = insertion_sort(xs_1507)
    _x_19816 = _x_19815[k_1508] if 0 <= k_1508 < len(_x_19815) else None
    return _x_19816

# Lean: Corpus.Sorting.kthLargest
def kth_largest(xs_1510: list[int], k_1511: int) -> int | None:
    _x_19818 = insertion_sort(xs_1510)
    _x_19819 = len(_x_19818)
    _x_19820 = _x_19819 <= k_1511
    if _x_19820:
        _x_19832 = None
        return _x_19832
    else:
        _x_19825 = 1
        _x_19828 = _x_19819 - 1
        _x_19829 = _x_19828 - k_1511
        _x_19830 = _x_19818[_x_19829] if 0 <= _x_19829 < len(_x_19818) else None
        return _x_19830

# Lean: Corpus.Sorting.median
def median(xs_1513: list[int]) -> int | None:
    _x_19835 = len(xs_1513) == 0
    _x_19836 = True
    if _x_19835:
        _x_19850 = None
        return _x_19850
    else:
        _x_19839 = insertion_sort(xs_1513)
        _x_19840 = len(_x_19839)
        _x_19844 = 2
        _x_19847 = _x_19840 // 2
        _x_19848 = _x_19839[_x_19847] if 0 <= _x_19847 < len(_x_19839) else None
        return _x_19848

# Lean: Corpus.Sorting.mode
def mode(xs_1516: list[int]) -> int | None:
    _x_19853 = None
    _x_19854 = 0
    _x_19857 = mode_go(xs_1516, _x_19853, 0)
    return _x_19857

# Lean: Corpus.Sorting.unique
def unique(xs_1517: list[int]) -> list[int]:
    _x_19859 = []
    _x_19860 = unique_go(xs_1517, _x_19859)
    return _x_19860

# Lean: Corpus.Sorting.removeDupsSorted
def remove_dups_sorted(xs_1518: list[int]) -> list[int]:
    def _f_19863():
        _x_19862 = []
        return _x_19862
    _alt_19864 = _f_19863
    def _f_19867(x_1520: int):
        _x_19865 = []
        _x_19866 = [x_1520] + _x_19865
        return _x_19866
    _alt_19868 = _f_19867
    def _f_19882(x_1521: int, y_1522: int, rest_1523: list[int]):
        _x_19871 = x_1521 == y_1522
        _x_19872 = True
        if _x_19871:
            _x_19879 = [y_1522] + rest_1523
            _x_19880 = remove_dups_sorted(_x_19879)
            return _x_19880
        else:
            _x_19875 = [y_1522] + rest_1523
            _x_19876 = remove_dups_sorted(_x_19875)
            _x_19877 = [x_1521] + _x_19876
            return _x_19877
    _alt_19883 = _f_19882
    if len(xs_1518) == 0:
        _x_19885 = _alt_19864()
        return _x_19885
    else:
        head_19886 = xs_1518[0]
        tail_19887 = xs_1518[1:]
        if len(tail_19887) == 0:
            _x_19888 = _alt_19868(head_19886)
            return _x_19888
        else:
            head_19889 = tail_19887[0]
            tail_19890 = tail_19887[1:]
            _x_19891 = _alt_19883(head_19886, head_19889, tail_19890)
            return _x_19891


