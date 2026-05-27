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
    def _f_13158(ys_0: list[int]):
        _x_13155 = list(reversed(acc))
        _x_13156 = _x_13155 + ys_0
        _x_13157 = (_x_13156, inv)
        return _x_13157
    _alt_13159 = _f_13158
    _alt_13160 = _f_13158
    def _f_13176(x: int, xs_: list[int], y: int, ys_: list[int]):
        _x_13161 = x <= y
        if _x_13161:
            _x_13172 = [y] + ys_
            _x_13173 = [x] + acc
            _x_13174 = merge_and_count_go(xs_, _x_13172, _x_13173, inv)
            return _x_13174
        else:
            _x_13163 = [x] + xs_
            _x_13164 = [y] + acc
            _x_13168 = len(xs)
            _x_13169 = inv + _x_13168
            _x_13170 = merge_and_count_go(_x_13163, ys_, _x_13164, _x_13169)
            return _x_13170
    _alt_13177 = _f_13176
    if len(xs) == 0:
        if len(ys) == 0:
            _x_13178 = []
            _x_13179 = _alt_13159(_x_13178)
            return _x_13179
        else:
            head_13180 = ys[0]
            tail_13181 = ys[1:]
            _x_13182 = [head_13180] + tail_13181
            _x_13183 = _alt_13159(_x_13182)
            return _x_13183
    else:
        head_13185 = xs[0]
        tail_13186 = xs[1:]
        if len(ys) == 0:
            _x_13187 = [head_13185] + tail_13186
            _x_13188 = _alt_13160(_x_13187)
            return _x_13188
        else:
            head_13189 = ys[0]
            tail_13190 = ys[1:]
            _x_13191 = _alt_13177(head_13185, tail_13186, head_13189, tail_13190)
            return _x_13191

# Lean: Corpus.Production.countInversions.mergeAndCount
def merge_and_count(xs_1: list[int], ys_2: list[int]) -> tuple[list[int], int]:
    _x_13195 = []
    _x_13196 = 0
    _x_13199 = merge_and_count_go(xs_1, ys_2, _x_13195, 0)
    return _x_13199

# Lean: Corpus.Production.countInversions.mergeCount
def merge_count(xs_3: list[int]) -> tuple[list[int], int]:
    _x_13201 = len(xs_3)
    _x_13202 = 1
    _x_13205 = _x_13201 <= 1
    if _x_13205:
        _x_13251 = 0
        _x_13254 = (xs_3, 0)
        return _x_13254
    else:
        _x_13210 = 2
        _x_13213 = _x_13201 // 2
        def _f_13241(left: list[int], right: list[int]):
            def _f_13234(sorted_l: list[int], inv_l: int):
                def _f_13227(sorted_r: list[int], inv_r: int):
                    def _f_13220(merged: list[int], inv_merge: int):
                        _x_13217 = inv_l + inv_r
                        _x_13218 = _x_13217 + inv_merge
                        _x_13219 = (merged, _x_13218)
                        return _x_13219
                    _alt_13221 = _f_13220
                    _x_13222 = merge_and_count(sorted_l, sorted_r)
                    match _x_13222:
                        case (fst_13223, snd_13224):
                            _x_13225 = _alt_13221(fst_13223, snd_13224)
                            return _x_13225
                _alt_13228 = _f_13227
                _x_13229 = merge_count(right)
                match _x_13229:
                    case (fst_13230, snd_13231):
                        _x_13232 = _alt_13228(fst_13230, snd_13231)
                        return _x_13232
            _alt_13235 = _f_13234
            _x_13236 = merge_count(left)
            match _x_13236:
                case (fst_13237, snd_13238):
                    _x_13239 = _alt_13235(fst_13237, snd_13238)
                    return _x_13239
        _alt_13242 = _f_13241
        _x_13243 = (lambda n, xs: xs[:n])(xs_3)
        _x_13244 = (lambda n, xs: xs[n:])(xs_3)
        _x_13245 = (_x_13243, _x_13244)
        match _x_13245:
            case (fst_13246, snd_13247):
                _x_13248 = _alt_13242(fst_13246, snd_13247)
                return _x_13248

# Lean: Corpus.Production.maxSubarraySum.kadane
def kadane(xs_4: list[int], current_max: int, global_max: int) -> int:
    def _f_13257():
        return global_max
    _alt_13258 = _f_13257
    def _f_13268(x_5: int, rest: list[int]):
        _x_13260 = max
        _x_13264 = current_max + x_5
        _x_13265 = _x_13260(x_5, _x_13264)
        _x_13266 = _x_13260(global_max, _x_13265)
        _x_13267 = kadane(rest, _x_13265, _x_13266)
        return _x_13267
    _alt_13269 = _f_13268
    if len(xs_4) == 0:
        _x_13271 = _alt_13258()
        return _x_13271
    else:
        head_13272 = xs_4[0]
        tail_13273 = xs_4[1:]
        _x_13274 = _alt_13269(head_13272, tail_13273)
        return _x_13274

# Lean: Corpus.Production.lis.fill
def fill(xs_6: list[int], n: int, i: int, dp: list[int], parent: list[int]) -> tuple[list[int], list[int]]:
    _x_13277 = n <= i
    if _x_13277:
        _x_13375 = (dp, parent)
        return _x_13375
    else:
        def _f_13282(xs_7: list[int], i_8: int):
            _x_13280 = len(xs_7)
            _x_13281 = i_8 < _x_13280
            return _x_13281
        _x_13284 = _x_13283.get_elem__2
        _x_13286 = _x_13284(_x_13285, xs_6, i)
        def _f_13297(max_len: int, max_j: int):
            _x_13290 = 1
            _x_13293 = i + 1
            _x_13294 = set_(None, dp, i, max_len)
            _x_13295 = set_(None, parent, i, max_j)
            _x_13296 = fill(xs_6, n, _x_13293, _x_13294, _x_13295)
            return _x_13296
        _alt_13298 = _f_13297
        def _f_13363(x_13299: tuple[int, int], j: int):
            def _f_13357(acc_9: int, pj: int):
                def _f_13301():
                    _x_13300 = False
                    return False
                _alt_13302 = _f_13301
                def _f_13319():
                    def _f_13309(xs_12: list[int], i_13: int):
                        _x_13307 = len(xs_12)
                        _x_13308 = i_13 < _x_13307
                        return _x_13308
                    _x_13311 = _x_13310.get_elem__2
                    _x_13312 = _x_13311(_x_13285, dp, j)
                    _x_13313 = 1
                    _x_13316 = _x_13312 + 1
                    _x_13317 = acc_9 < _x_13316
                    return _x_13317
                _alt_13320 = _f_13319
                _x_13321 = _x_13284(_x_13285, xs_6, j)
                _x_13322 = _x_13321 < _x_13286
                def _jp_13350(_y_13328: bool):
                    _x_13329 = True
                    if _y_13328:
                        def _f_13340(xs_14: list[int], i_15: int):
                            _x_13338 = len(xs_14)
                            _x_13339 = i_15 < _x_13338
                            return _x_13339
                        _x_13342 = _x_13341.get_elem__2
                        _x_13343 = _x_13342(_x_13285, dp, j)
                        _x_13344 = 1
                        _x_13347 = _x_13343 + 1
                        _x_13348 = (_x_13347, j)
                        return _x_13348
                    else:
                        _x_13332 = (acc_9, pj)
                        return _x_13332
                def _jp_13353():
                    _x_13352 = _alt_13302()
                    return _jp_13350(_x_13352)
                def _jp_13356():
                    _x_13355 = _alt_13320()
                    return _jp_13350(_x_13355)
                if _x_13322:
                    return _jp_13356()
                else:
                    return _jp_13353()
            _alt_13358 = _f_13357
            match x_13299:
                case (fst_13359, snd_13360):
                    _x_13361 = _alt_13358(fst_13359, snd_13360)
                    return _x_13361
        _x_13364 = 1
        _x_13367 = (1, n)
        _x_13368 = list(range(i))
        _x_13369 = functools.reduce(_f_13363, _x_13368, _x_13367)
        match _x_13369:
            case (fst_13370, snd_13371):
                _x_13372 = _alt_13298(fst_13370, snd_13371)
                return _x_13372

# Lean: Corpus.Production.lis.backtrack
def backtrack(xs_16: list[int], n_17: int, parent_: list[int], i_18: int, acc_19: list[int]) -> list[int]:
    _x_13378 = n_17 <= i_18
    if _x_13378:
        return acc_19
    else:
        def _f_13383(xs_20: list[int], i_21: int):
            _x_13381 = len(xs_20)
            _x_13382 = i_21 < _x_13381
            return _x_13382
        _x_13385 = _x_13384.get_elem__2
        _x_13387 = _x_13385(_x_13386, parent_, i_18)
        def _f_13391(xs_22: list[int], i_23: int):
            _x_13389 = len(xs_22)
            _x_13390 = i_23 < _x_13389
            return _x_13390
        _x_13393 = _x_13392.get_elem__2
        _x_13394 = _x_13393(_x_13386, xs_16, i_18)
        _x_13395 = [_x_13394] + acc_19
        _x_13396 = backtrack(xs_16, n_17, parent_, _x_13387, _x_13395)
        return _x_13396

# Lean: Corpus.Production.lisLength.fill
def fill(xs_24: list[int], n_25: int, i_26: int, dp_27: list[int]) -> list[int]:
    _x_13400 = n_25 <= i_26
    if _x_13400:
        return dp_27
    else:
        def _f_13405(xs_28: list[int], i_29: int):
            _x_13403 = len(xs_28)
            _x_13404 = i_29 < _x_13403
            return _x_13404
        _x_13407 = _x_13406.get_elem__2
        _x_13409 = _x_13407(_x_13408, xs_24, i_26)
        def _f_13432(acc_31: int, j_32: int):
            _x_13410 = _x_13407(_x_13408, xs_24, j_32)
            _x_13411 = _x_13410 < _x_13409
            if _x_13411:
                _x_13415 = max
                def _f_13422(xs_33: list[int], i_34: int):
                    _x_13420 = len(xs_33)
                    _x_13421 = i_34 < _x_13420
                    return _x_13421
                _x_13424 = _x_13423.get_elem__2
                _x_13425 = _x_13424(_x_13408, dp_27, j_32)
                _x_13426 = 1
                _x_13429 = _x_13425 + 1
                _x_13430 = _x_13415(acc_31, _x_13429)
                return _x_13430
            else:
                return acc_31
        _x_13433 = 1
        _x_13436 = list(range(i_26))
        _x_13437 = functools.reduce(_f_13432, _x_13436, 1)
        _x_13441 = i_26 + 1
        _x_13442 = set_(None, dp_27, i_26, _x_13437)
        _x_13443 = fill(xs_24, n_25, _x_13441, _x_13442)
        return _x_13443

# Lean: Corpus.Production.matrixChainOrder.fill
def fill(dims: list[int], n_35: int, inf: int, len: int, i_36: int, dp_37: list[int]) -> list[int]:
    _x_13447 = n_35 < len
    if _x_13447:
        return dp_37
    else:
        _x_13452 = i_36 + len
        _x_13453 = n_35 < _x_13452
        if _x_13453:
            _x_13520 = 1
            _x_13523 = len + 1
            _x_13524 = 0
            _x_13527 = fill(dims, n_35, inf, _x_13523, 0, dp_37)
            return _x_13527
        else:
            _x_13458 = 1
            _x_13461 = _x_13452 - 1
            _x_13465 = i_36 * n_35
            _x_13466 = _x_13465 + _x_13461
            _x_13469 = len == 1
            _x_13470 = True
            if _x_13469:
                _x_13512 = i_36 + 1
                _x_13513 = 0
                _x_13516 = set_(None, dp_37, _x_13466, 0)
                _x_13517 = fill(dims, n_35, inf, len, _x_13512, _x_13516)
                return _x_13517
            else:
                def _f_13504(acc_39: int, k_: int):
                    _x_13473 = i_36 + k_
                    def _f_13477(xs_40: list[int], i_41: int):
                        _x_13475 = len(xs_40)
                        _x_13476 = i_41 < _x_13475
                        return _x_13476
                    _x_13479 = _x_13478.get_elem__2
                    _x_13481 = _x_13465 + _x_13473
                    _x_13482 = _x_13479(_x_13480, dp_37, _x_13481)
                    _x_13483 = _x_13473 + 1
                    _x_13484 = _x_13483 * n_35
                    _x_13485 = _x_13484 + _x_13461
                    _x_13486 = _x_13479(_x_13480, dp_37, _x_13485)
                    _x_13487 = _x_13482 + _x_13486
                    def _f_13491(xs_42: list[int], i_43: int):
                        _x_13489 = len(xs_42)
                        _x_13490 = i_43 < _x_13489
                        return _x_13490
                    _x_13493 = _x_13492.get_elem__2
                    _x_13494 = _x_13493(_x_13480, dims, i_36)
                    _x_13495 = _x_13493(_x_13480, dims, _x_13483)
                    _x_13496 = _x_13494 * _x_13495
                    _x_13497 = _x_13461 + 1
                    _x_13498 = _x_13493(_x_13480, dims, _x_13497)
                    _x_13499 = _x_13496 * _x_13498
                    _x_13500 = _x_13487 + _x_13499
                    _x_13502 = min
                    _x_13503 = _x_13502(acc_39, _x_13500)
                    return _x_13503
                _x_13505 = len - 1
                _x_13506 = list(range(_x_13505))
                _x_13507 = functools.reduce(_f_13504, _x_13506, inf)
                _x_13508 = i_36 + 1
                _x_13509 = set_(None, dp_37, _x_13466, _x_13507)
                _x_13510 = fill(dims, n_35, inf, len, _x_13508, _x_13509)
                return _x_13510

# Lean: Corpus.Production.coinChange.fill
def fill(coins: list[int], amount: int, inf_44: int, a: int, dp_45: list[int]) -> list[int]:
    _x_13532 = amount < a
    if _x_13532:
        return dp_45
    else:
        def _f_13594(acc_46: int, c: int):
            def _f_13535():
                _x_13534 = False
                return False
            _alt_13536 = _f_13535
            def _f_13551():
                def _f_13540(xs_49: list[int], i_50: int):
                    _x_13538 = len(xs_49)
                    _x_13539 = i_50 < _x_13538
                    return _x_13539
                _x_13542 = _x_13541.get_elem__2
                _x_13547 = a - c
                _x_13548 = _x_13542(_x_13543, dp_45, _x_13547)
                _x_13549 = _x_13548 < inf_44
                return _x_13549
            _alt_13552 = _f_13551
            _x_13553 = c <= a
            def _jp_13587(_y_13559: bool):
                _x_13560 = True
                if _y_13559:
                    _x_13565 = min
                    def _f_13572(xs_51: list[int], i_52: int):
                        _x_13570 = len(xs_51)
                        _x_13571 = i_52 < _x_13570
                        return _x_13571
                    _x_13574 = _x_13573.get_elem__2
                    _x_13579 = a - c
                    _x_13580 = _x_13574(_x_13575, dp_45, _x_13579)
                    _x_13581 = 1
                    _x_13584 = _x_13580 + 1
                    _x_13585 = _x_13565(acc_46, _x_13584)
                    return _x_13585
                else:
                    return acc_46
            def _jp_13593():
                _x_13592 = _alt_13552()
                return _jp_13587(_x_13592)
            def _jp_13590():
                _x_13589 = _alt_13536()
                return _jp_13587(_x_13589)
            if _x_13553:
                return _jp_13593()
            else:
                return _jp_13590()
        _x_13595 = functools.reduce(_f_13594, coins, inf_44)
        _x_13599 = 1
        _x_13602 = a + 1
        _x_13603 = set_(None, dp_45, a, _x_13595)
        _x_13604 = fill(coins, amount, inf_44, _x_13602, _x_13603)
        return _x_13604

# Lean: Corpus.Production.knapsack01.fill
def fill(capacity: int, weights: list[int], values: list[int], n_53: int, i_54: int, w: int, dp_55: list[int]) -> list[int]:
    _x_13608 = n_53 < i_54
    if _x_13608:
        return dp_55
    else:
        _x_13610 = capacity < w
        if _x_13610:
            _x_13685 = 1
            _x_13688 = i_54 + 1
            _x_13689 = 0
            _x_13692 = fill(capacity, weights, values, n_53, _x_13688, 0, dp_55)
            return _x_13692
        else:
            _x_13618 = 1
            _x_13621 = capacity + 1
            _x_13622 = i_54 * _x_13621
            _x_13623 = _x_13622 + w
            _x_13626 = 0
            _x_13629 = i_54 == 0
            _x_13630 = True
            def _jp_13680(_y_13676: int):
                _x_13677 = w + 1
                _x_13678 = set_(None, dp_55, _x_13623, _y_13676)
                _x_13679 = fill(capacity, weights, values, n_53, i_54, _x_13677, _x_13678)
                return _x_13679
            if _x_13629:
                return _jp_13680(0)
            else:
                def _f_13636(xs_57: list[int], i_58: int):
                    _x_13634 = len(xs_57)
                    _x_13635 = i_58 < _x_13634
                    return _x_13635
                _x_13638 = _x_13637.get_elem__2
                _x_13643 = i_54 - 1
                _x_13644 = _x_13638(_x_13639, weights, _x_13643)
                _x_13645 = _x_13638(_x_13639, values, _x_13643)
                _x_13646 = w < _x_13644
                if _x_13646:
                    def _f_13668(xs_59: list[int], i_60: int):
                        _x_13666 = len(xs_59)
                        _x_13667 = i_60 < _x_13666
                        return _x_13667
                    _x_13670 = _x_13669.get_elem__2
                    _x_13671 = _x_13643 * _x_13621
                    _x_13672 = _x_13671 + w
                    _x_13673 = _x_13670(_x_13639, dp_55, _x_13672)
                    return _jp_13680(_x_13673)
                else:
                    _x_13649 = max
                    def _f_13653(xs_61: list[int], i_62: int):
                        _x_13651 = len(xs_61)
                        _x_13652 = i_62 < _x_13651
                        return _x_13652
                    _x_13655 = _x_13654.get_elem__2
                    _x_13656 = _x_13643 * _x_13621
                    _x_13657 = _x_13656 + w
                    _x_13658 = _x_13655(_x_13639, dp_55, _x_13657)
                    _x_13659 = w - _x_13644
                    _x_13660 = _x_13656 + _x_13659
                    _x_13661 = _x_13655(_x_13639, dp_55, _x_13660)
                    _x_13662 = _x_13661 + _x_13645
                    _x_13663 = _x_13649(_x_13658, _x_13662)
                    return _jp_13680(_x_13663)

# Lean: Corpus.Production.intervalScheduling.select
def select(remaining: list[tuple[int, int]], last_end: int, acc_63: list[tuple[int, int]]) -> list[tuple[int, int]]:
    def _f_13698():
        _x_13697 = list(reversed(acc_63))
        return _x_13697
    _alt_13699 = _f_13698
    def _f_13708(s: int, e: int, rest_65: list[tuple[int, int]]):
        _x_13700 = last_end <= s
        if _x_13700:
            _x_13704 = (s, e)
            _x_13705 = [_x_13704] + acc_63
            _x_13706 = select(rest_65, e, _x_13705)
            return _x_13706
        else:
            _x_13702 = select(rest_65, last_end, acc_63)
            return _x_13702
    _alt_13709 = _f_13708
    if len(remaining) == 0:
        _x_13711 = _alt_13699()
        return _x_13711
    else:
        head_13712 = remaining[0]
        tail_13713 = remaining[1:]
        match head_13712:
            case (fst_13714, snd_13715):
                _x_13716 = _alt_13709(fst_13714, snd_13715, tail_13713)
                return _x_13716

# Lean: Corpus.Production.editDistance.fill
def fill(xs_66: list[int], ys_67: list[int], m: int, n_68: int, i_69: int, j_70: int, dp_71: list[int]) -> list[int]:
    _x_13720 = m < i_69
    if _x_13720:
        return dp_71
    else:
        _x_13722 = n_68 < j_70
        if _x_13722:
            _x_13800 = 1
            _x_13803 = i_69 + 1
            _x_13804 = 0
            _x_13807 = fill(xs_66, ys_67, m, n_68, _x_13803, 0, dp_71)
            return _x_13807
        else:
            _x_13730 = 1
            _x_13733 = n_68 + 1
            _x_13734 = i_69 * _x_13733
            _x_13735 = _x_13734 + j_70
            _x_13738 = 0
            _x_13741 = i_69 == 0
            _x_13742 = True
            def _jp_13795(_y_13791: int):
                _x_13792 = j_70 + 1
                _x_13793 = set_(None, dp_71, _x_13735, _y_13791)
                _x_13794 = fill(xs_66, ys_67, m, n_68, i_69, _x_13792, _x_13793)
                return _x_13794
            if _x_13741:
                return _jp_13795(j_70)
            else:
                _x_13745 = j_70 == 0
                if _x_13745:
                    return _jp_13795(i_69)
                else:
                    def _f_13751(xs_74: list[int], i_75: int):
                        _x_13749 = len(xs_74)
                        _x_13750 = i_75 < _x_13749
                        return _x_13750
                    _x_13753 = _x_13752.get_elem__2
                    _x_13758 = i_69 - 1
                    _x_13759 = _x_13753(_x_13754, xs_66, _x_13758)
                    _x_13760 = j_70 - 1
                    _x_13761 = _x_13753(_x_13754, ys_67, _x_13760)
                    _x_13762 = _x_13759 == _x_13761
                    def _jp_13787(_y_13766: int):
                        _x_13768 = min
                        def _f_13772(xs_78: list[int], i_79: int):
                            _x_13770 = len(xs_78)
                            _x_13771 = i_79 < _x_13770
                            return _x_13771
                        _x_13774 = _x_13773.get_elem__2
                        _x_13775 = _x_13758 * _x_13733
                        _x_13776 = _x_13775 + j_70
                        _x_13777 = _x_13774(_x_13754, dp_71, _x_13776)
                        _x_13778 = _x_13777 + 1
                        _x_13779 = _x_13734 + _x_13760
                        _x_13780 = _x_13774(_x_13754, dp_71, _x_13779)
                        _x_13781 = _x_13780 + 1
                        _x_13782 = _x_13768(_x_13778, _x_13781)
                        _x_13783 = _x_13775 + _x_13760
                        _x_13784 = _x_13774(_x_13754, dp_71, _x_13783)
                        _x_13785 = _x_13784 + _y_13766
                        _x_13786 = _x_13768(_x_13782, _x_13785)
                        return _jp_13795(_x_13786)
                    if _x_13762:
                        return _jp_13787(0)
                    else:
                        return _jp_13787(1)

# Lean: Corpus.Production.lcs.backtrack
def backtrack(xs_80: list[int], ys_81: list[int], n_82: int, memo_: list[int], i_83: int, j_84: int, acc_85: list[int]) -> list[int]:
    def _f_13813():
        _x_13812 = True
        return True
    _alt_13814 = _f_13813
    def _f_13821():
        _x_13817 = 0
        _x_13820 = j_84 == 0
        return _x_13820
    _alt_13822 = _f_13821
    _x_13825 = 0
    _x_13828 = i_83 == 0
    def _jp_13888(_y_13833: bool):
        _x_13834 = True
        if _y_13833:
            return acc_85
        else:
            def _f_13840(xs_88: list[int], i_89: int):
                _x_13838 = len(xs_88)
                _x_13839 = i_89 < _x_13838
                return _x_13839
            _x_13842 = _x_13841.get_elem__2
            _x_13847 = 1
            _x_13850 = i_83 - 1
            _x_13851 = _x_13842(_x_13843, xs_80, _x_13850)
            _x_13852 = j_84 - 1
            _x_13853 = _x_13842(_x_13843, ys_81, _x_13852)
            _x_13854 = _x_13851 == _x_13853
            if _x_13854:
                _x_13883 = [_x_13851] + acc_85
                _x_13884 = backtrack(xs_80, ys_81, n_82, memo_, _x_13850, _x_13852, _x_13883)
                return _x_13884
            else:
                def _f_13860(xs_92: list[int], i_93: int):
                    _x_13858 = len(xs_92)
                    _x_13859 = i_93 < _x_13858
                    return _x_13859
                _x_13862 = _x_13861.get_elem__2
                _x_13869 = n_82 + 1
                _x_13870 = i_83 * _x_13869
                _x_13871 = _x_13870 + _x_13852
                _x_13872 = _x_13862(_x_13843, memo_, _x_13871)
                _x_13873 = _x_13850 * _x_13869
                _x_13874 = _x_13873 + j_84
                _x_13875 = _x_13862(_x_13843, memo_, _x_13874)
                _x_13876 = _x_13872 < _x_13875
                if _x_13876:
                    _x_13880 = backtrack(xs_80, ys_81, n_82, memo_, _x_13850, j_84, acc_85)
                    return _x_13880
                else:
                    _x_13878 = backtrack(xs_80, ys_81, n_82, memo_, i_83, _x_13852, acc_85)
                    return _x_13878
    def _jp_13891():
        _x_13890 = _alt_13822()
        return _jp_13888(_x_13890)
    def _jp_13894():
        _x_13893 = _alt_13814()
        return _jp_13888(_x_13893)
    if _x_13828:
        return _jp_13894()
    else:
        return _jp_13891()

# Lean: Corpus.Production.lcs.fill
def fill(xs_94: list[int], ys_95: list[int], m_96: int, n_97: int, i_98: int, j_99: int, memo: list[int]) -> list[int]:
    _x_13896 = m_96 < i_98
    if _x_13896:
        return memo
    else:
        _x_13898 = n_97 < j_99
        if _x_13898:
            _x_14000 = 1
            _x_14003 = i_98 + 1
            _x_14004 = 0
            _x_14007 = fill(xs_94, ys_95, m_96, n_97, _x_14003, 0, memo)
            return _x_14007
        else:
            _x_13906 = 1
            _x_13909 = n_97 + 1
            _x_13910 = i_98 * _x_13909
            _x_13911 = _x_13910 + j_99
            def _f_13913():
                _x_13912 = True
                return True
            _alt_13914 = _f_13913
            def _f_13921():
                _x_13917 = 0
                _x_13920 = j_99 == 0
                return _x_13920
            _alt_13922 = _f_13921
            _x_13925 = 0
            _x_13928 = i_98 == 0
            def _jp_13989(_y_13933: bool):
                _x_13934 = True
                if _y_13933:
                    _x_13985 = j_99 + 1
                    _x_13986 = set_(None, memo, _x_13911, 0)
                    _x_13987 = fill(xs_94, ys_95, m_96, n_97, i_98, _x_13985, _x_13986)
                    return _x_13987
                else:
                    def _f_13940(xs_103: list[int], i_104: int):
                        _x_13938 = len(xs_103)
                        _x_13939 = i_104 < _x_13938
                        return _x_13939
                    _x_13942 = _x_13941.get_elem__2
                    _x_13947 = i_98 - 1
                    _x_13948 = _x_13942(_x_13943, xs_94, _x_13947)
                    _x_13949 = j_99 - 1
                    _x_13950 = _x_13942(_x_13943, ys_95, _x_13949)
                    _x_13951 = _x_13948 == _x_13950
                    def _jp_13983(_y_13979: int):
                        _x_13980 = j_99 + 1
                        _x_13981 = set_(None, memo, _x_13911, _y_13979)
                        _x_13982 = fill(xs_94, ys_95, m_96, n_97, i_98, _x_13980, _x_13981)
                        return _x_13982
                    if _x_13951:
                        def _f_13972(xs_108: list[int], i_109: int):
                            _x_13970 = len(xs_108)
                            _x_13971 = i_109 < _x_13970
                            return _x_13971
                        _x_13974 = _x_13973.get_elem__2
                        _x_13975 = _x_13947 * _x_13909
                        _x_13976 = _x_13975 + _x_13949
                        _x_13977 = _x_13974(_x_13943, memo, _x_13976)
                        _x_13978 = _x_13977 + 1
                        return _jp_13983(_x_13978)
                    else:
                        _x_13955 = max
                        def _f_13959(xs_110: list[int], i_111: int):
                            _x_13957 = len(xs_110)
                            _x_13958 = i_111 < _x_13957
                            return _x_13958
                        _x_13961 = _x_13960.get_elem__2
                        _x_13962 = _x_13947 * _x_13909
                        _x_13963 = _x_13962 + j_99
                        _x_13964 = _x_13961(_x_13943, memo, _x_13963)
                        _x_13965 = _x_13910 + _x_13949
                        _x_13966 = _x_13961(_x_13943, memo, _x_13965)
                        _x_13967 = _x_13955(_x_13964, _x_13966)
                        return _jp_13983(_x_13967)
            def _jp_13995():
                _x_13994 = _alt_13914()
                return _jp_13989(_x_13994)
            def _jp_13992():
                _x_13991 = _alt_13922()
                return _jp_13989(_x_13991)
            if _x_13928:
                return _jp_13995()
            else:
                return _jp_13992()

# Lean: Corpus.Production.lcsLength.fill
def fill(xs_112: list[int], ys_113: list[int], m_114: int, n_115: int, i_116: int, j_117: int, memo_118: list[int]) -> list[int]:
    _x_14012 = m_114 < i_116
    if _x_14012:
        return memo_118
    else:
        _x_14014 = n_115 < j_117
        if _x_14014:
            _x_14116 = 1
            _x_14119 = i_116 + 1
            _x_14120 = 0
            _x_14123 = fill(xs_112, ys_113, m_114, n_115, _x_14119, 0, memo_118)
            return _x_14123
        else:
            _x_14022 = 1
            _x_14025 = n_115 + 1
            _x_14026 = i_116 * _x_14025
            _x_14027 = _x_14026 + j_117
            def _f_14029():
                _x_14028 = True
                return True
            _alt_14030 = _f_14029
            def _f_14037():
                _x_14033 = 0
                _x_14036 = j_117 == 0
                return _x_14036
            _alt_14038 = _f_14037
            _x_14041 = 0
            _x_14044 = i_116 == 0
            def _jp_14105(_y_14049: bool):
                _x_14050 = True
                if _y_14049:
                    _x_14101 = j_117 + 1
                    _x_14102 = set_(None, memo_118, _x_14027, 0)
                    _x_14103 = fill(xs_112, ys_113, m_114, n_115, i_116, _x_14101, _x_14102)
                    return _x_14103
                else:
                    def _f_14056(xs_122: list[int], i_123: int):
                        _x_14054 = len(xs_122)
                        _x_14055 = i_123 < _x_14054
                        return _x_14055
                    _x_14058 = _x_14057.get_elem__2
                    _x_14063 = i_116 - 1
                    _x_14064 = _x_14058(_x_14059, xs_112, _x_14063)
                    _x_14065 = j_117 - 1
                    _x_14066 = _x_14058(_x_14059, ys_113, _x_14065)
                    _x_14067 = _x_14064 == _x_14066
                    def _jp_14099(_y_14095: int):
                        _x_14096 = j_117 + 1
                        _x_14097 = set_(None, memo_118, _x_14027, _y_14095)
                        _x_14098 = fill(xs_112, ys_113, m_114, n_115, i_116, _x_14096, _x_14097)
                        return _x_14098
                    if _x_14067:
                        def _f_14088(xs_127: list[int], i_128: int):
                            _x_14086 = len(xs_127)
                            _x_14087 = i_128 < _x_14086
                            return _x_14087
                        _x_14090 = _x_14089.get_elem__2
                        _x_14091 = _x_14063 * _x_14025
                        _x_14092 = _x_14091 + _x_14065
                        _x_14093 = _x_14090(_x_14059, memo_118, _x_14092)
                        _x_14094 = _x_14093 + 1
                        return _jp_14099(_x_14094)
                    else:
                        _x_14071 = max
                        def _f_14075(xs_129: list[int], i_130: int):
                            _x_14073 = len(xs_129)
                            _x_14074 = i_130 < _x_14073
                            return _x_14074
                        _x_14077 = _x_14076.get_elem__2
                        _x_14078 = _x_14063 * _x_14025
                        _x_14079 = _x_14078 + j_117
                        _x_14080 = _x_14077(_x_14059, memo_118, _x_14079)
                        _x_14081 = _x_14026 + _x_14065
                        _x_14082 = _x_14077(_x_14059, memo_118, _x_14081)
                        _x_14083 = _x_14071(_x_14080, _x_14082)
                        return _jp_14099(_x_14083)
            def _jp_14111():
                _x_14110 = _alt_14030()
                return _jp_14105(_x_14110)
            def _jp_14108():
                _x_14107 = _alt_14038()
                return _jp_14105(_x_14107)
            if _x_14044:
                return _jp_14111()
            else:
                return _jp_14108()

# Lean: Corpus.Production.computeZArray.matchLength
def match_length(s_131: list[str], t: list[str], i_132: int, j_133: int) -> int:
    def _f_14129():
        _x_14128 = True
        return True
    _alt_14130 = _f_14129
    def _f_14134():
        _x_14131 = len(t)
        _x_14132 = _x_14131 <= j_133
        return _x_14132
    _alt_14135 = _f_14134
    _x_14136 = len(s_131)
    _x_14137 = _x_14136 <= i_132
    def _jp_14182(_y_14143: bool):
        _x_14144 = True
        if _y_14143:
            _x_14178 = 0
            return 0
        else:
            def _f_14153(xs_136: list[str], i_137: int):
                _x_14151 = len(xs_136)
                _x_14152 = i_137 < _x_14151
                return _x_14152
            _x_14155 = _x_14154.get_elem__2
            _x_14157 = _x_14155(_x_14156, s_131, i_132)
            _x_14158 = _x_14155(_x_14156, t, j_133)
            _x_14159 = _x_14157 == _x_14158
            if _x_14159:
                _x_14169 = 1
                _x_14172 = i_132 + 1
                _x_14173 = j_133 + 1
                _x_14174 = match_length(s_131, t, _x_14172, _x_14173)
                _x_14175 = 1 + _x_14174
                return _x_14175
            else:
                _x_14162 = 0
                return 0
    def _jp_14188():
        _x_14187 = _alt_14130()
        return _jp_14182(_x_14187)
    def _jp_14185():
        _x_14184 = _alt_14135()
        return _jp_14182(_x_14184)
    if _x_14137:
        return _jp_14188()
    else:
        return _jp_14185()

# Lean: Corpus.Production.computeZArray.compute
def compute(s_138: list[str], n_139: int, z: list[int], i_140: int, l: int, r: int) -> list[int]:
    _x_14190 = n_139 <= i_140
    if _x_14190:
        return z
    else:
        _x_14192 = r < i_140
        if _x_14192:
            _x_14229 = 0
            _x_14232 = match_length(s_138, s_138, i_140, 0)
            _x_14233 = set_(None, z, i_140, _x_14232)
            _x_14234 = 0 < _x_14232
            if _x_14234:
                _x_14248 = 1
                _x_14251 = i_140 + 1
                _x_14255 = i_140 + _x_14232
                _x_14256 = _x_14255 - 1
                _x_14257 = compute(s_138, n_139, _x_14233, _x_14251, i_140, _x_14256)
                return _x_14257
            else:
                _x_14239 = 1
                _x_14242 = i_140 + 1
                _x_14243 = compute(s_138, n_139, _x_14233, _x_14242, l, r)
                return _x_14243
        else:
            _x_14197 = i_140 - l
            def _f_14201(xs_143: list[int], i_144: int):
                _x_14199 = len(xs_143)
                _x_14200 = i_144 < _x_14199
                return _x_14200
            _x_14203 = _x_14202.get_elem__2
            _x_14205 = _x_14203(_x_14204, z, _x_14197)
            _x_14209 = r - i_140
            _x_14210 = 1
            _x_14213 = _x_14209 + 1
            _x_14214 = _x_14205 < _x_14213
            if _x_14214:
                _x_14224 = set_(None, z, i_140, _x_14205)
                _x_14225 = i_140 + 1
                _x_14226 = compute(s_138, n_139, _x_14224, _x_14225, l, r)
                return _x_14226
            else:
                _x_14216 = r + 1
                _x_14217 = match_length(s_138, s_138, _x_14216, _x_14213)
                _x_14218 = _x_14213 + _x_14217
                _x_14219 = set_(None, z, i_140, _x_14218)
                _x_14220 = i_140 + 1
                _x_14221 = r + _x_14217
                _x_14222 = compute(s_138, n_139, _x_14219, _x_14220, i_140, _x_14221)
                return _x_14222

# Lean: Corpus.Production.naiveStringMatchAll.checkMatch
def check_match(t_147: list[str], p: list[str], i_148: int, j_149: int) -> bool:
    _x_14263 = len(p)
    _x_14264 = _x_14263 <= j_149
    if _x_14264:
        _x_14295 = True
        return True
    else:
        def _f_14272(xs_150: list[str], i_151: int):
            _x_14270 = len(xs_150)
            _x_14271 = i_151 < _x_14270
            return _x_14271
        _x_14274 = _x_14273.get_elem__2
        _x_14279 = i_148 + j_149
        _x_14280 = _x_14274(_x_14275, t_147, _x_14279)
        _x_14281 = _x_14274(_x_14275, p, j_149)
        _x_14282 = _x_14280 == _x_14281
        _x_14283 = True
        if _x_14282:
            _x_14288 = 1
            _x_14291 = j_149 + 1
            _x_14292 = check_match(t_147, p, i_148, _x_14291)
            return _x_14292
        else:
            _x_14286 = False
            return False

# Lean: Corpus.Production.naiveStringMatchAll.search
def search(t_152: list[str], p_153: list[str], n_154: int, m_155: int, i_156: int, acc_157: list[int]) -> list[int]:
    _x_14301 = n_154 - m_155
    _x_14302 = _x_14301 < i_156
    if _x_14302:
        _x_14331 = list(reversed(acc_157))
        return _x_14331
    else:
        _x_14304 = 0
        _x_14307 = check_match(t_152, p_153, i_156, 0)
        _x_14308 = True
        if _x_14307:
            _x_14323 = 1
            _x_14326 = i_156 + 1
            _x_14327 = [i_156] + acc_157
            _x_14328 = search(t_152, p_153, n_154, m_155, _x_14326, _x_14327)
            return _x_14328
        else:
            _x_14314 = 1
            _x_14317 = i_156 + 1
            _x_14318 = search(t_152, p_153, n_154, m_155, _x_14317, acc_157)
            return _x_14318

# Lean: Corpus.Production.naiveStringMatch.checkMatch
def check_match(t_158: list[str], p_159: list[str], i_160: int, j_161: int) -> bool:
    _x_14334 = len(p_159)
    _x_14335 = _x_14334 <= j_161
    if _x_14335:
        _x_14366 = True
        return True
    else:
        def _f_14343(xs_162: list[str], i_163: int):
            _x_14341 = len(xs_162)
            _x_14342 = i_163 < _x_14341
            return _x_14342
        _x_14345 = _x_14344.get_elem__2
        _x_14350 = i_160 + j_161
        _x_14351 = _x_14345(_x_14346, t_158, _x_14350)
        _x_14352 = _x_14345(_x_14346, p_159, j_161)
        _x_14353 = _x_14351 == _x_14352
        _x_14354 = True
        if _x_14353:
            _x_14359 = 1
            _x_14362 = j_161 + 1
            _x_14363 = check_match(t_158, p_159, i_160, _x_14362)
            return _x_14363
        else:
            _x_14357 = False
            return False

# Lean: Corpus.Production.naiveStringMatch.search
def search(t_164: list[str], p_165: list[str], n_166: int, m_167: int, i_168: int) -> int | None:
    _x_14372 = n_166 - m_167
    _x_14373 = _x_14372 < i_168
    if _x_14373:
        _x_14394 = None
        return _x_14394
    else:
        _x_14375 = 0
        _x_14378 = check_match(t_164, p_165, i_168, 0)
        _x_14379 = True
        if _x_14378:
            _x_14391 = i_168
            return _x_14391
        else:
            _x_14385 = 1
            _x_14388 = i_168 + 1
            _x_14389 = search(t_164, p_165, n_166, m_167, _x_14388)
            return _x_14389

# Lean: Corpus.Production.lomutoPartition.go
def lomuto_partition_go(hi: int, pivot: int, arr: list[int], i_169: int, j_170: int) -> tuple[list[int], int]:
    _x_14397 = hi <= j_170
    if _x_14397:
        _x_14430 = swap_(None, arr, i_169, hi)
        _x_14431 = (_x_14430, i_169)
        return _x_14431
    else:
        def _f_14402(xs_171: list[int], i_172: int):
            _x_14400 = len(xs_171)
            _x_14401 = i_172 < _x_14400
            return _x_14401
        _x_14404 = _x_14403.get_elem__2
        _x_14406 = _x_14404(_x_14405, arr, j_170)
        _x_14407 = _x_14406 < pivot
        if _x_14407:
            _x_14418 = swap_(None, arr, i_169, j_170)
            _x_14422 = 1
            _x_14425 = i_169 + 1
            _x_14426 = j_170 + 1
            _x_14427 = lomuto_partition_go(hi, pivot, _x_14418, _x_14425, _x_14426)
            return _x_14427
        else:
            _x_14412 = 1
            _x_14415 = j_170 + 1
            _x_14416 = lomuto_partition_go(hi, pivot, arr, i_169, _x_14415)
            return _x_14416

# Lean: Corpus.Production.UnionFind.ofSize.build
def of_size_build(n_174: int, i_175: int, nodes: list[UFNode]) -> list[UFNode]:
    _x_14434 = n_174 <= i_175
    if _x_14434:
        return nodes
    else:
        _x_14439 = 1
        _x_14442 = i_175 + 1
        _x_14443 = 0
        _x_14446 = UFNode_mk(i_175, 0)
        _x_14447 = array_push(None, nodes, _x_14446)
        _x_14448 = of_size_build(n_174, _x_14442, _x_14447)
        return _x_14448

# Lean: Corpus.Sorting.unique.go
def unique_go(xs_176: list[int], seen: list[int]) -> list[int]:
    def _f_14453():
        _x_14452 = list(reversed(seen))
        return _x_14452
    _alt_14454 = _f_14453
    def _f_14465(x_178: int, rest_179: list[int]):
        _x_14456 = x_178 in seen
        _x_14457 = True
        if _x_14456:
            _x_14463 = unique_go(rest_179, seen)
            return _x_14463
        else:
            _x_14460 = [x_178] + seen
            _x_14461 = unique_go(rest_179, _x_14460)
            return _x_14461
    _alt_14466 = _f_14465
    if len(xs_176) == 0:
        _x_14468 = _alt_14454()
        return _x_14468
    else:
        head_14469 = xs_176[0]
        tail_14470 = xs_176[1:]
        _x_14471 = _alt_14466(head_14469, tail_14470)
        return _x_14471

# Lean: Corpus.Sorting.mode.count
def count(x_180: int, xs_181: list[int]) -> int:
    def _f_14489(acc_182: int, y_183: int):
        _x_14476 = y_183 == x_180
        _x_14477 = True
        if _x_14476:
            _x_14484 = 1
            _x_14487 = acc_182 + 1
            return _x_14487
        else:
            return acc_182
    _x_14490 = 0
    _x_14493 = functools.reduce(_f_14489, xs_181, 0)
    return _x_14493

# Lean: Corpus.Sorting.mode.go
def mode_go(xs_184: list[int], best: int | None, best_count: int) -> int | None:
    def _f_14495():
        return best
    _alt_14496 = _f_14495
    def _f_14505(x_186: int, rest_187: list[int]):
        _x_14497 = count(x_186, xs_184)
        _x_14498 = best_count < _x_14497
        if _x_14498:
            _x_14502 = x_186
            _x_14503 = mode_go(rest_187, _x_14502, _x_14497)
            return _x_14503
        else:
            _x_14500 = mode_go(rest_187, best, best_count)
            return _x_14500
    _alt_14506 = _f_14505
    if len(xs_184) == 0:
        _x_14508 = _alt_14496()
        return _x_14508
    else:
        head_14509 = xs_184[0]
        tail_14510 = xs_184[1:]
        _x_14511 = _alt_14506(head_14509, tail_14510)
        return _x_14511

# Lean: Corpus.Sorting.gnomeSort.go
def gnome_sort_go(n_189: int, pos: int, arr_190: list[int]) -> list[int]:
    _x_14514 = n_189 <= pos
    if _x_14514:
        return arr_190
    else:
        def _f_14517():
            _x_14516 = True
            return True
        _alt_14518 = _f_14517
        def _f_14537():
            def _f_14522(xs_193: list[int], i_194: int):
                _x_14520 = len(xs_193)
                _x_14521 = i_194 < _x_14520
                return _x_14521
            _x_14524 = _x_14523.get_elem__2
            _x_14529 = 1
            _x_14532 = pos - 1
            _x_14533 = _x_14524(_x_14525, arr_190, _x_14532)
            _x_14534 = _x_14524(_x_14525, arr_190, pos)
            _x_14535 = _x_14533 <= _x_14534
            return _x_14535
        _alt_14538 = _f_14537
        _x_14541 = 0
        _x_14544 = pos == 0
        def _jp_14572(_y_14549: bool):
            _x_14550 = True
            if _y_14549:
                _x_14566 = 1
                _x_14569 = pos + 1
                _x_14570 = gnome_sort_go(n_189, _x_14569, arr_190)
                return _x_14570
            else:
                _x_14556 = 1
                _x_14559 = pos - 1
                _x_14560 = swap_(None, arr_190, pos, _x_14559)
                _x_14561 = gnome_sort_go(n_189, _x_14559, _x_14560)
                return _x_14561
        def _jp_14578():
            _x_14577 = _alt_14518()
            return _jp_14572(_x_14577)
        def _jp_14575():
            _x_14574 = _alt_14538()
            return _jp_14572(_x_14574)
        if _x_14544:
            return _jp_14578()
        else:
            return _jp_14575()

# Lean: Corpus.Sorting.radixSort.go
def radix_sort_go(max_val: int, exp: int, xs_195: list[int]) -> list[int]:
    _x_14582 = max_val < exp
    if _x_14582:
        return xs_195
    else:
        def _f_14599(arr_196: list[list[int]], x_197: int):
            _x_14590 = x_197 // exp
            _x_14591 = 10
            _x_14594 = _x_14590 % 10
            def _f_14597(x_14595: list[int]):
                _x_14596 = [x_197] + x_14595
                return _x_14596
            _x_14598 = modify(None, arr_196, _x_14594, _f_14597)
            return _x_14598
        _x_14600 = 10
        _x_14603 = []
        _x_14604 = mk_array(None, 10, _x_14603)
        _x_14605 = functools.reduce(_f_14599, xs_195, _x_14604)
        def _f_14611(acc_198: list[int], bucket: list[int]):
            _x_14609 = list(reversed(bucket))
            _x_14610 = acc_198 + _x_14609
            return _x_14610
        _x_14612 = 0
        _x_14615 = len(_x_14605)
        _x_14616 = array_foldl(None, None, _f_14611, _x_14603, _x_14605, 0, _x_14615)
        _x_14620 = exp * 10
        _x_14621 = radix_sort_go(max_val, _x_14620, _x_14616)
        return _x_14621

# Lean: Corpus.Sorting.countingSort.expand
def expand(max_val_199: int, counts: list[int], i_200: int, acc_201: list[int]) -> list[int]:
    _x_14625 = max_val_199 < i_200
    if _x_14625:
        return acc_201
    else:
        _x_14630 = 1
        _x_14633 = i_200 + 1
        _x_14637 = 0
        _x_14640 = get_d(None, counts, i_200, 0)
        _x_14641 = list_replicate(None, _x_14640, i_200)
        _x_14642 = acc_201 + _x_14641
        _x_14643 = expand(max_val_199, counts, _x_14633, _x_14642)
        return _x_14643

# Lean: Corpus.Sorting.selectionSort.go.findMin
def find_min(n_202: int, arr_203: list[int], j_204: int, min_idx: int) -> int:
    _x_14647 = n_202 <= j_204
    if _x_14647:
        return min_idx
    else:
        _x_14652 = 1
        _x_14655 = j_204 + 1
        def _f_14659(xs_205: list[int], i_206: int):
            _x_14657 = len(xs_205)
            _x_14658 = i_206 < _x_14657
            return _x_14658
        _x_14661 = _x_14660.get_elem__2
        _x_14663 = _x_14661(_x_14662, arr_203, j_204)
        _x_14664 = _x_14661(_x_14662, arr_203, min_idx)
        _x_14665 = _x_14663 < _x_14664
        def _jp_14670(_y_14668: int):
            _x_14669 = find_min(n_202, arr_203, _x_14655, _y_14668)
            return _x_14669
        if _x_14665:
            return _jp_14670(j_204)
        else:
            return _jp_14670(min_idx)

# Lean: Corpus.Sorting.selectionSort.go
def selection_sort_go(n_207: int, i_208: int, arr_209: list[int]) -> list[int]:
    _x_14674 = n_207 <= i_208
    if _x_14674:
        return arr_209
    else:
        _x_14676 = find_min(n_207, arr_209, i_208, i_208)
        _x_14680 = 1
        _x_14683 = i_208 + 1
        _x_14684 = swap_(None, arr_209, i_208, _x_14676)
        _x_14685 = selection_sort_go(n_207, _x_14683, _x_14684)
        return _x_14685

# Lean: Corpus.Sorting.bubbleSort.outer.inner
def outer_inner(n_211: int, i_212: int, j_213: int, arr_214: list[int]) -> list[int]:
    _x_14692 = n_211 - i_212
    _x_14693 = 1
    _x_14696 = _x_14692 - 1
    _x_14697 = _x_14696 <= j_213
    if _x_14697:
        return arr_214
    else:
        def _f_14702(xs_215: list[int], i_216: int):
            _x_14700 = len(xs_215)
            _x_14701 = i_216 < _x_14700
            return _x_14701
        _x_14704 = _x_14703.get_elem__2
        _x_14709 = j_213 + 1
        _x_14710 = _x_14704(_x_14705, arr_214, _x_14709)
        _x_14711 = _x_14704(_x_14705, arr_214, j_213)
        _x_14712 = _x_14710 < _x_14711
        def _jp_14718(_y_14716: list[int]):
            _x_14717 = outer_inner(n_211, i_212, _x_14709, _y_14716)
            return _x_14717
        if _x_14712:
            _x_14715 = swap_(None, arr_214, j_213, _x_14709)
            return _jp_14718(_x_14715)
        else:
            return _jp_14718(arr_214)

# Lean: Corpus.Sorting.bubbleSort.outer
def outer(n_218: int, i_219: int, arr_220: list[int]) -> list[int]:
    _x_14722 = n_218 <= i_219
    if _x_14722:
        return arr_220
    else:
        _x_14727 = 1
        _x_14730 = i_219 + 1
        _x_14731 = 0
        _x_14734 = outer_inner(n_218, i_219, 0, arr_220)
        _x_14735 = outer(n_218, _x_14730, _x_14734)
        return _x_14735

# Lean: Corpus.Sequences.vanEck.go
def van_eck_go(n_221: int, i_222: int, prev: int, last_seen: list[tuple[int, int]], acc_223: list[int]) -> list[int]:
    _x_14739 = n_221 < i_222
    if _x_14739:
        _x_14800 = list(reversed(acc_223))
        return _x_14800
    else:
        def _f_14744():
            _x_14741 = 0
            return 0
        _alt_14745 = _f_14744
        def _f_14755(fst_14746: int, idx_225: int):
            _x_14750 = 1
            _x_14753 = i_222 - 1
            _x_14754 = _x_14753 - idx_225
            return _x_14754
        _alt_14756 = _f_14755
        def _f_14761(p_226: tuple[int, int]):
            _x_14759 = p_226[0]
            _x_14760 = _x_14759 == prev
            return _x_14760
        _x_14762 = next((x for x in last_seen if _f_14761(x)), None)
        def _jp_14791(_y_14770: int):
            _x_14774 = 1
            _x_14777 = i_222 - 1
            _x_14778 = (prev, _x_14777)
            def _f_14782(p_227: tuple[int, int]):
                _x_14780 = p_227[0]
                _x_14781 = (lambda a, b: a != b)(prev)
                return _x_14781
            _x_14783 = [x for x in last_seen if _f_14782(x)]
            _x_14784 = [_x_14778] + _x_14783
            _x_14788 = i_222 + 1
            _x_14789 = [_y_14770] + acc_223
            _x_14790 = van_eck_go(n_221, _x_14788, _y_14770, _x_14784, _x_14789)
            return _x_14790
        def _jp_14798(_y_14795: int, _y_14796: int):
            _x_14797 = _alt_14756(_y_14795, _y_14796)
            return _jp_14791(_x_14797)
        def _jp_14794():
            _x_14793 = _alt_14745()
            return _jp_14791(_x_14793)
        if _x_14762 is None:
            return _jp_14794()
        else:
            val_14765 = _x_14762
            match val_14765:
                case (fst_14766, snd_14767):
                    return _jp_14798(fst_14766, snd_14767)

# Lean: Corpus.Sequences.firstNPrimes.isPrime.check
def first_nprimes_is_prime_check(n_228: int, d: int) -> bool:
    _x_14806 = d * d
    _x_14807 = n_228 < _x_14806
    if _x_14807:
        _x_14834 = True
        return True
    else:
        _x_14814 = n_228 % d
        _x_14815 = 0
        _x_14818 = _x_14814 == 0
        _x_14819 = True
        if _x_14818:
            _x_14831 = False
            return False
        else:
            _x_14825 = 1
            _x_14828 = d + 1
            _x_14829 = first_nprimes_is_prime_check(n_228, _x_14828)
            return _x_14829

# Lean: Corpus.Sequences.firstNPrimes.isPrime
def first_nprimes_is_prime(n_229: int) -> bool:
    _x_14837 = 2
    _x_14840 = n_229 < 2
    if _x_14840:
        _x_14844 = False
        return False
    else:
        _x_14842 = first_nprimes_is_prime_check(n_229, 2)
        return _x_14842

# Lean: Corpus.Sequences.firstNPrimes.go
def first_nprimes_go(n_230: int, candidate: int, found: list[int]) -> list[int]:
    _x_14847 = len(found)
    _x_14848 = n_230 <= _x_14847
    if _x_14848:
        _x_14874 = list(reversed(found))
        return _x_14874
    else:
        _x_14850 = first_nprimes_is_prime(candidate)
        _x_14851 = True
        if _x_14850:
            _x_14866 = 1
            _x_14869 = candidate + 1
            _x_14870 = [candidate] + found
            _x_14871 = first_nprimes_go(n_230, _x_14869, _x_14870)
            return _x_14871
        else:
            _x_14857 = 1
            _x_14860 = candidate + 1
            _x_14861 = first_nprimes_go(n_230, _x_14860, found)
            return _x_14861

# Lean: Corpus.Sequences.recaman.go
def recaman_go(n_231: int, i_232: int, prev_233: int, seen_234: list[int], acc_235: list[int]) -> list[int]:
    _x_14877 = n_231 < i_232
    if _x_14877:
        _x_14929 = list(reversed(acc_235))
        return _x_14929
    else:
        _x_14882 = prev_233 - i_232
        def _f_14884():
            _x_14883 = False
            return False
        _alt_14885 = _f_14884
        def _f_14889():
            _x_14887 = _x_14882 in seen_234
            _x_14888 = not _x_14887
            return _x_14888
        _alt_14890 = _f_14889
        _x_14891 = 0
        _x_14894 = 0 < _x_14882
        def _jp_14921(_y_14900: bool):
            _x_14901 = True
            def _jp_14920(_y_14909: int):
                _x_14913 = 1
                _x_14916 = i_232 + 1
                _x_14917 = [_y_14909] + seen_234
                _x_14918 = [_y_14909] + acc_235
                _x_14919 = recaman_go(n_231, _x_14916, _y_14909, _x_14917, _x_14918)
                return _x_14919
            if _y_14900:
                return _jp_14920(_x_14882)
            else:
                _x_14907 = prev_233 + i_232
                return _jp_14920(_x_14907)
        def _jp_14927():
            _x_14926 = _alt_14890()
            return _jp_14921(_x_14926)
        def _jp_14924():
            _x_14923 = _alt_14885()
            return _jp_14921(_x_14923)
        if _x_14894:
            return _jp_14927()
        else:
            return _jp_14924()

# Lean: Corpus.Sequences.lookAndSayNext.go
def look_and_say_next_go(xs_240: list[int], curr: int, count: int, acc_241: list[int]) -> list[int]:
    def _f_14940():
        _x_14935 = []
        _x_14936 = [curr] + _x_14935
        _x_14937 = [count] + _x_14936
        _x_14938 = acc_241 + _x_14937
        _x_14939 = list(reversed(_x_14938))
        return _x_14939
    _alt_14941 = _f_14940
    def _f_14964(x_243: int, rest_244: list[int]):
        _x_14944 = x_243 == curr
        _x_14945 = True
        if _x_14944:
            _x_14958 = 1
            _x_14961 = count + 1
            _x_14962 = look_and_say_next_go(rest_244, curr, _x_14961, acc_241)
            return _x_14962
        else:
            _x_14948 = 1
            _x_14951 = [count] + acc_241
            _x_14952 = [curr] + _x_14951
            _x_14953 = look_and_say_next_go(rest_244, x_243, 1, _x_14952)
            return _x_14953
    _alt_14965 = _f_14964
    if len(xs_240) == 0:
        _x_14967 = _alt_14941()
        return _x_14967
    else:
        head_14968 = xs_240[0]
        tail_14969 = xs_240[1:]
        _x_14970 = _alt_14965(head_14968, tail_14969)
        return _x_14970

# Lean: Corpus.Sequences.repunit.go
def repunit_go(n_245: int, acc_246: int) -> int:
    _x_14975 = 0
    _x_14978 = n_245 == 0
    _x_14979 = True
    if _x_14978:
        return acc_246
    else:
        _x_14985 = 1
        _x_14988 = n_245 - 1
        _x_14995 = 10
        _x_14998 = acc_246 * 10
        _x_14999 = _x_14998 + 1
        _x_15000 = repunit_go(_x_14988, _x_14999)
        return _x_15000

# Lean: Corpus.Sequences.narayana.binomial.go
def binomial_go(n_247: int, k_248: int, i_249: int, acc_250: int) -> int:
    _x_15006 = i_249 == k_248
    _x_15007 = True
    if _x_15006:
        return acc_250
    else:
        _x_15013 = 1
        _x_15016 = i_249 + 1
        _x_15026 = n_247 - i_249
        _x_15027 = acc_250 * _x_15026
        _x_15028 = _x_15027 // _x_15016
        _x_15029 = binomial_go(n_247, k_248, _x_15016, _x_15028)
        return _x_15029

# Lean: Corpus.Sequences.narayana.binomial
def binomial(n_251: int, k_252: int) -> int:
    _x_15033 = n_251 < k_252
    if _x_15033:
        _x_15052 = 0
        return 0
    else:
        _x_15038 = n_251 - k_252
        _x_15039 = _x_15038 < k_252
        def _jp_15050(_y_15042: int):
            _x_15043 = 0
            _x_15046 = 1
            _x_15049 = binomial_go(n_251, _y_15042, 0, 1)
            return _x_15049
        if _x_15039:
            return _jp_15050(_x_15038)
        else:
            return _jp_15050(k_252)

# Lean: Corpus.Sequences.motzkin.go
def motzkin_go(n_254: int, k_255: int, acc_256: int) -> int:
    _x_15062 = 1
    _x_15065 = n_254 + 1
    _x_15066 = k_255 == _x_15065
    _x_15067 = True
    if _x_15066:
        return acc_256
    else:
        _x_15070 = k_255 + 1
        _x_15074 = motzkin(k_255)
        _x_15078 = n_254 - 1
        _x_15079 = _x_15078 - k_255
        _x_15080 = motzkin(_x_15079)
        _x_15081 = _x_15074 * _x_15080
        _x_15082 = acc_256 + _x_15081
        _x_15083 = motzkin_go(n_254, _x_15070, _x_15082)
        return _x_15083

# Lean: Corpus.Sequences.jacobsthal.go
def jacobsthal_go(n_257: int, a_258: int, b: int) -> int:
    _x_15089 = 0
    _x_15092 = n_257 == 0
    _x_15093 = True
    if _x_15092:
        return a_258
    else:
        _x_15099 = 1
        _x_15102 = n_257 - 1
        _x_15109 = 2
        _x_15112 = 2 * a_258
        _x_15113 = b + _x_15112
        _x_15114 = jacobsthal_go(_x_15102, b, _x_15113)
        return _x_15114

# Lean: Corpus.Sequences.perrin.go
def perrin_go(n_259: int, a_260: int, b_261: int, c_262: int) -> int:
    _x_15120 = 0
    _x_15123 = n_259 == 0
    _x_15124 = True
    if _x_15123:
        return a_260
    else:
        _x_15130 = 1
        _x_15133 = n_259 - 1
        _x_15137 = a_260 + b_261
        _x_15138 = perrin_go(_x_15133, b_261, c_262, _x_15137)
        return _x_15138

# Lean: Corpus.Sequences.padovan.go
def padovan_go(n_263: int, a_264: int, b_265: int, c_266: int) -> int:
    _x_15144 = 0
    _x_15147 = n_263 == 0
    _x_15148 = True
    if _x_15147:
        return a_264
    else:
        _x_15154 = 1
        _x_15157 = n_263 - 1
        _x_15161 = a_264 + b_265
        _x_15162 = padovan_go(_x_15157, b_265, c_266, _x_15161)
        return _x_15162

# Lean: Corpus.Sequences.pell.go
def pell_go(n_267: int, a_268: int, b_269: int) -> int:
    _x_15168 = 0
    _x_15171 = n_267 == 0
    _x_15172 = True
    if _x_15171:
        return a_268
    else:
        _x_15178 = 1
        _x_15181 = n_267 - 1
        _x_15188 = 2
        _x_15191 = 2 * b_269
        _x_15192 = _x_15191 + a_268
        _x_15193 = pell_go(_x_15181, b_269, _x_15192)
        return _x_15193

# Lean: Corpus.Sequences.tribonacci.go
def tribonacci_go(n_270: int, a_271: int, b_272: int, c_273: int) -> int:
    _x_15199 = 0
    _x_15202 = n_270 == 0
    _x_15203 = True
    if _x_15202:
        return a_271
    else:
        _x_15209 = 1
        _x_15212 = n_270 - 1
        _x_15216 = a_271 + b_272
        _x_15217 = _x_15216 + c_273
        _x_15218 = tribonacci_go(_x_15212, b_272, c_273, _x_15217)
        return _x_15218

# Lean: Corpus.Sequences.lucas.go
def lucas_go(n_274: int, a_275: int, b_276: int) -> int:
    _x_15224 = 0
    _x_15227 = n_274 == 0
    _x_15228 = True
    if _x_15227:
        return a_275
    else:
        _x_15234 = 1
        _x_15237 = n_274 - 1
        _x_15241 = a_275 + b_276
        _x_15242 = lucas_go(_x_15237, b_276, _x_15241)
        return _x_15242

# Lean: Corpus.Sequences.fibonacci.go
def sequences_fibonacci_go(n_277: int, a_278: int, b_279: int) -> int:
    _x_15248 = 0
    _x_15251 = n_277 == 0
    _x_15252 = True
    if _x_15251:
        return a_278
    else:
        _x_15258 = 1
        _x_15261 = n_277 - 1
        _x_15265 = a_278 + b_279
        _x_15266 = sequences_fibonacci_go(_x_15261, b_279, _x_15265)
        return _x_15266

# Lean: Corpus.Combinatorics.integerPartitions.go
def integer_partitions_go(n_280: int, max: int) -> list[list[int]]:
    _x_15272 = 0
    _x_15275 = n_280 == 0
    _x_15276 = True
    if _x_15275:
        _x_15304 = []
        _x_15305 = []
        _x_15306 = [_x_15304] + _x_15305
        return _x_15306
    else:
        _x_15279 = max == 0
        if _x_15279:
            _x_15301 = []
            return _x_15301
        else:
            def _f_15284(x_15282: list[int]):
                _x_15283 = [max] + x_15282
                return _x_15283
            _x_15288 = n_280 - max
            _x_15289 = integer_partitions_go(_x_15288, max)
            _x_15290 = [_f_15284(x) for x in _x_15289]
            _x_15291 = 1
            _x_15294 = max - 1
            _x_15295 = integer_partitions_go(n_280, _x_15294)
            _x_15299 = _x_15290 + _x_15295
            return _x_15299

# Lean: Corpus.Combinatorics.compositions.go
def compositions_go(n_281: int, k_282: int, acc_283: list[list[int]]) -> list[list[int]]:
    _x_15309 = n_281 < k_282
    if _x_15309:
        return acc_283
    else:
        _x_15314 = 1
        _x_15317 = k_282 + 1
        def _f_15323(x_15321: list[int]):
            _x_15322 = [k_282] + x_15321
            return _x_15322
        _x_15327 = n_281 - k_282
        _x_15328 = compositions(_x_15327)
        _x_15329 = [_f_15323(x) for x in _x_15328]
        _x_15330 = acc_283 + _x_15329
        _x_15331 = compositions_go(n_281, _x_15317, _x_15330)
        return _x_15331

# Lean: Corpus.Combinatorics.prevPermutation.findI
def find_i(arr_284: list[int], i_285: int) -> int | None:
    _x_15337 = 0
    _x_15340 = i_285 == 0
    _x_15341 = True
    if _x_15340:
        _x_15367 = None
        return _x_15367
    else:
        def _f_15347(xs_286: list[int], i_287: int):
            _x_15345 = len(xs_286)
            _x_15346 = i_287 < _x_15345
            return _x_15346
        _x_15349 = _x_15348.get_elem__2
        _x_15351 = _x_15349(_x_15350, arr_284, i_285)
        _x_15355 = 1
        _x_15358 = i_285 - 1
        _x_15359 = _x_15349(_x_15350, arr_284, _x_15358)
        _x_15360 = _x_15351 < _x_15359
        if _x_15360:
            _x_15364 = _x_15358
            return _x_15364
        else:
            _x_15362 = find_i(arr_284, _x_15358)
            return _x_15362

# Lean: Corpus.Combinatorics.prevPermutation.reverseFrom.go
def reverse_from_go(arr_288: list[int], l_289: int, r_290: int) -> list[int]:
    _x_15370 = r_290 <= l_289
    if _x_15370:
        return arr_288
    else:
        _x_15372 = swap_(None, arr_288, l_289, r_290)
        _x_15376 = 1
        _x_15379 = l_289 + 1
        _x_15383 = r_290 - 1
        _x_15384 = reverse_from_go(_x_15372, _x_15379, _x_15383)
        return _x_15384

# Lean: Corpus.Combinatorics.prevPermutation.reverseFrom
def reverse_from(arr_291: list[int], start: int) -> list[int]:
    _x_15391 = len(arr_291)
    _x_15392 = 1
    _x_15395 = _x_15391 - 1
    _x_15396 = reverse_from_go(arr_291, start, _x_15395)
    return _x_15396

# Lean: Corpus.Combinatorics.prevPermutation.findJ
def find_j(arr_292: list[int], i_293: int, j_294: int) -> int:
    _x_15403 = 1
    _x_15406 = i_293 + 1
    _x_15407 = j_294 == _x_15406
    _x_15408 = True
    if _x_15407:
        return j_294
    else:
        def _f_15414(xs_295: list[int], i_296: int):
            _x_15412 = len(xs_295)
            _x_15413 = i_296 < _x_15412
            return _x_15413
        _x_15416 = _x_15415.get_elem__2
        _x_15421 = j_294 - 1
        _x_15422 = _x_15416(_x_15417, arr_292, _x_15421)
        _x_15423 = _x_15416(_x_15417, arr_292, i_293)
        _x_15424 = _x_15422 < _x_15423
        if _x_15424:
            return _x_15421
        else:
            _x_15426 = find_j(arr_292, i_293, _x_15421)
            return _x_15426

# Lean: Corpus.Combinatorics.nextPermutation.findI
def find_i(arr_297: list[int], i_298: int) -> int | None:
    _x_15434 = 0
    _x_15437 = i_298 == 0
    _x_15438 = True
    if _x_15437:
        _x_15464 = None
        return _x_15464
    else:
        def _f_15444(xs_299: list[int], i_300: int):
            _x_15442 = len(xs_299)
            _x_15443 = i_300 < _x_15442
            return _x_15443
        _x_15446 = _x_15445.get_elem__2
        _x_15451 = 1
        _x_15454 = i_298 - 1
        _x_15455 = _x_15446(_x_15447, arr_297, _x_15454)
        _x_15456 = _x_15446(_x_15447, arr_297, i_298)
        _x_15457 = _x_15455 < _x_15456
        if _x_15457:
            _x_15461 = _x_15454
            return _x_15461
        else:
            _x_15459 = find_i(arr_297, _x_15454)
            return _x_15459

# Lean: Corpus.Combinatorics.nextPermutation.reverseFrom.go
def reverse_from_go(arr_301: list[int], l_302: int, r_303: int) -> list[int]:
    _x_15467 = r_303 <= l_302
    if _x_15467:
        return arr_301
    else:
        _x_15469 = swap_(None, arr_301, l_302, r_303)
        _x_15473 = 1
        _x_15476 = l_302 + 1
        _x_15480 = r_303 - 1
        _x_15481 = reverse_from_go(_x_15469, _x_15476, _x_15480)
        return _x_15481

# Lean: Corpus.Combinatorics.nextPermutation.reverseFrom
def reverse_from(arr_304: list[int], start_305: int) -> list[int]:
    _x_15488 = len(arr_304)
    _x_15489 = 1
    _x_15492 = _x_15488 - 1
    _x_15493 = reverse_from_go(arr_304, start_305, _x_15492)
    return _x_15493

# Lean: Corpus.Combinatorics.nextPermutation.findJ
def find_j(arr_306: list[int], i_307: int, j_308: int) -> int:
    _x_15500 = 1
    _x_15503 = i_307 + 1
    _x_15504 = j_308 == _x_15503
    _x_15505 = True
    if _x_15504:
        return j_308
    else:
        def _f_15511(xs_309: list[int], i_310: int):
            _x_15509 = len(xs_309)
            _x_15510 = i_310 < _x_15509
            return _x_15510
        _x_15513 = _x_15512.get_elem__2
        _x_15515 = _x_15513(_x_15514, arr_306, i_307)
        _x_15519 = j_308 - 1
        _x_15520 = _x_15513(_x_15514, arr_306, _x_15519)
        _x_15521 = _x_15515 < _x_15520
        if _x_15521:
            return _x_15519
        else:
            _x_15523 = find_j(arr_306, i_307, _x_15519)
            return _x_15523

# Lean: Corpus.Combinatorics.permutationRank.go
def permutation_rank_go(n_311: int, code: list[int], pos_312: int, acc_313: int) -> int:
    def _f_15529():
        return acc_313
    _alt_15530 = _f_15529
    def _f_15550(c_315: int, rest_316: list[int]):
        _x_15534 = 1
        _x_15537 = pos_312 + 1
        _x_15544 = n_311 - pos_312
        _x_15545 = _x_15544 - 1
        _x_15546 = factorial(_x_15545)
        _x_15547 = c_315 * _x_15546
        _x_15548 = acc_313 + _x_15547
        _x_15549 = permutation_rank_go(n_311, rest_316, _x_15537, _x_15548)
        return _x_15549
    _alt_15551 = _f_15550
    if len(code) == 0:
        _x_15553 = _alt_15530()
        return _x_15553
    else:
        head_15554 = code[0]
        tail_15555 = code[1:]
        _x_15556 = _alt_15551(head_15554, tail_15555)
        return _x_15556

# Lean: Corpus.Combinatorics.nthPermutation.go
def nth_permutation_go(k_317: int, n_318: int, available: list[int], acc_319: list[int]) -> list[int]:
    def _f_15560():
        _x_15559 = list(reversed(acc_319))
        return _x_15559
    _alt_15561 = _f_15560
    def _f_15591(x_15562: list[int]):
        _x_15566 = len(available)
        _x_15567 = 1
        _x_15570 = _x_15566 - 1
        _x_15571 = factorial(_x_15570)
        _x_15575 = k_317 // _x_15571
        _x_15576 = 0
        _x_15579 = get_d(None, available, _x_15575, 0)
        _x_15583 = k_317 % _x_15571
        def _f_15587(x_15584: int):
            _x_15586 = (lambda a, b: a != b)(_x_15579)
            return _x_15586
        _x_15588 = [x for x in available if _f_15587(x)]
        _x_15589 = [_x_15579] + acc_319
        _x_15590 = nth_permutation_go(_x_15583, n_318, _x_15588, _x_15589)
        return _x_15590
    _alt_15592 = _f_15591
    if len(available) == 0:
        _x_15594 = _alt_15561()
        return _x_15594
    else:
        head_15595 = available[0]
        tail_15596 = available[1:]
        _x_15597 = [head_15595] + tail_15596
        _x_15598 = _alt_15592(_x_15597)
        return _x_15598

# Lean: Corpus.Combinatorics.fromLehmerCode.go
def from_lehmer_code_go(code_322: list[int], available_323: list[int], acc_324: list[int]) -> list[int]:
    def _f_15602():
        _x_15601 = list(reversed(acc_324))
        return _x_15601
    _alt_15603 = _f_15602
    def _f_15615(c_326: int, rest_327: list[int]):
        _x_15604 = 0
        _x_15607 = get_d(None, available_323, c_326, 0)
        def _f_15611(x_15608: int):
            _x_15610 = (lambda a, b: a != b)(_x_15607)
            return _x_15610
        _x_15612 = [x for x in available_323 if _f_15611(x)]
        _x_15613 = [_x_15607] + acc_324
        _x_15614 = from_lehmer_code_go(rest_327, _x_15612, _x_15613)
        return _x_15614
    _alt_15616 = _f_15615
    if len(code_322) == 0:
        _x_15618 = _alt_15603()
        return _x_15618
    else:
        head_15619 = code_322[0]
        tail_15620 = code_322[1:]
        _x_15621 = _alt_15616(head_15619, tail_15620)
        return _x_15621

# Lean: Corpus.Combinatorics.lehmerCode.go
def lehmer_code_go(perm: list[int], acc_329: list[int]) -> list[int]:
    def _f_15625():
        _x_15624 = list(reversed(acc_329))
        return _x_15624
    _alt_15626 = _f_15625
    def _f_15645(x_331: int, rest_332: list[int]):
        def _f_15638(acc_333: int, y_334: int):
            _x_15627 = y_334 < x_331
            if _x_15627:
                _x_15633 = 1
                _x_15636 = acc_333 + 1
                return _x_15636
            else:
                return acc_333
        _x_15639 = 0
        _x_15642 = functools.reduce(_f_15638, rest_332, 0)
        _x_15643 = [_x_15642] + acc_329
        _x_15644 = lehmer_code_go(rest_332, _x_15643)
        return _x_15644
    _alt_15646 = _f_15645
    if len(perm) == 0:
        _x_15648 = _alt_15626()
        return _x_15648
    else:
        head_15649 = perm[0]
        tail_15650 = perm[1:]
        _x_15651 = _alt_15646(head_15649, tail_15650)
        return _x_15651

# Lean: Corpus.Combinatorics.countInversions.count
def count(xs_336: list[int]) -> int:
    def _f_15657():
        _x_15654 = 0
        return 0
    _alt_15658 = _f_15657
    def _f_15677(x_338: int, rest_339: list[int]):
        def _f_15670(acc_340: int, y_341: int):
            _x_15662 = y_341 < x_338
            if _x_15662:
                _x_15665 = 1
                _x_15668 = acc_340 + 1
                return _x_15668
            else:
                return acc_340
        _x_15671 = 0
        _x_15674 = functools.reduce(_f_15670, rest_339, 0)
        _x_15675 = count(rest_339)
        _x_15676 = _x_15674 + _x_15675
        return _x_15676
    _alt_15678 = _f_15677
    if len(xs_336) == 0:
        _x_15680 = _alt_15658()
        return _x_15680
    else:
        head_15681 = xs_336[0]
        tail_15682 = xs_336[1:]
        _x_15683 = _alt_15678(head_15681, tail_15682)
        return _x_15683

# Lean: Corpus.Combinatorics.partitionCount.p
def p(n_342: int, k_343: int) -> int:
    _x_15688 = 0
    _x_15691 = n_342 == 0
    _x_15692 = True
    if _x_15691:
        _x_15720 = 1
        return 1
    else:
        _x_15695 = k_343 == 0
        if _x_15695:
            return 0
        else:
            _x_15698 = n_342 < k_343
            if _x_15698:
                _x_15715 = p(n_342, n_342)
                return _x_15715
            else:
                _x_15706 = n_342 - k_343
                _x_15707 = p(_x_15706, k_343)
                _x_15708 = 1
                _x_15711 = k_343 - 1
                _x_15712 = p(n_342, _x_15711)
                _x_15713 = _x_15707 + _x_15712
                return _x_15713

# Lean: Corpus.Combinatorics.bell.go
def bell_go(n_344: int, i_345: int, acc_346: int) -> int:
    _x_15730 = 1
    _x_15733 = n_344 + 1
    _x_15734 = i_345 == _x_15733
    _x_15735 = True
    if _x_15734:
        return acc_346
    else:
        _x_15738 = i_345 + 1
        _x_15739 = stirling2(n_344, i_345)
        _x_15740 = acc_346 + _x_15739
        _x_15741 = bell_go(n_344, _x_15738, _x_15740)
        return _x_15741

# Lean: Corpus.Combinatorics.fallingFactorial.go
def falling_factorial_go(x_347: int, n_348: int, i_349: int, acc_350: int) -> int:
    _x_15747 = i_349 == n_348
    _x_15748 = True
    if _x_15747:
        return acc_350
    else:
        _x_15754 = 1
        _x_15757 = i_349 + 1
        _x_15764 = x_347 - i_349
        _x_15765 = acc_350 * _x_15764
        _x_15766 = falling_factorial_go(x_347, n_348, _x_15757, _x_15765)
        return _x_15766

# Lean: Corpus.Combinatorics.risingFactorial.go
def rising_factorial_go(x_351: int, n_352: int, i_353: int, acc_354: int) -> int:
    _x_15772 = i_353 == n_352
    _x_15773 = True
    if _x_15772:
        return acc_354
    else:
        _x_15779 = 1
        _x_15782 = i_353 + 1
        _x_15786 = x_351 + i_353
        _x_15787 = acc_354 * _x_15786
        _x_15788 = rising_factorial_go(x_351, n_352, _x_15782, _x_15787)
        return _x_15788

# Lean: Corpus.Geometry.segmentsIntersect.onSegment
def on_segment(p_355: Point2D, q: Point2D, r_356: Point2D) -> bool:
    def _f_15793():
        _x_15792 = False
        return False
    _alt_15794 = _f_15793
    def _f_15803():
        _x_15796 = min
        _x_15797 = p_355.point2d_1
        _x_15798 = r_356.point2d_1
        _x_15799 = _x_15796(_x_15797, _x_15798)
        _x_15800 = q.point2d_1
        _x_15801 = float_dec_le(_x_15799, _x_15800)
        return _x_15801
    _alt_15804 = _f_15803
    _alt_15805 = _f_15793
    def _f_15814():
        _x_15806 = q.point2d_1
        _x_15808 = max
        _x_15809 = p_355.point2d_1
        _x_15810 = r_356.point2d_1
        _x_15811 = _x_15808(_x_15809, _x_15810)
        _x_15812 = float_dec_le(_x_15806, _x_15811)
        return _x_15812
    _alt_15815 = _f_15814
    _alt_15816 = _f_15793
    def _f_15825():
        _x_15818 = min
        _x_15819 = p_355.point2d_0
        _x_15820 = r_356.point2d_0
        _x_15821 = _x_15818(_x_15819, _x_15820)
        _x_15822 = q.point2d_0
        _x_15823 = float_dec_le(_x_15821, _x_15822)
        return _x_15823
    _alt_15826 = _f_15825
    _x_15827 = q.point2d_0
    _x_15829 = max
    _x_15830 = p_355.point2d_0
    _x_15831 = r_356.point2d_0
    _x_15832 = _x_15829(_x_15830, _x_15831)
    _x_15833 = float_dec_le(_x_15827, _x_15832)
    def _jp_15857(_y_15839: bool):
        def _jp_15850(_y_15844: bool):
            if _y_15844:
                _x_15848 = _alt_15804()
                return _x_15848
            else:
                _x_15846 = _alt_15794()
                return _x_15846
        def _jp_15856():
            _x_15855 = _alt_15815()
            return _jp_15850(_x_15855)
        def _jp_15853():
            _x_15852 = _alt_15805()
            return _jp_15850(_x_15852)
        if _y_15839:
            return _jp_15856()
        else:
            return _jp_15853()
    def _jp_15863():
        _x_15862 = _alt_15826()
        return _jp_15857(_x_15862)
    def _jp_15860():
        _x_15859 = _alt_15816()
        return _jp_15857(_x_15859)
    if _x_15833:
        return _jp_15863()
    else:
        return _jp_15860()

# Lean: Corpus.Geometry.isConvexPolygon.checkSign
def check_sign(c_361: float, sign: bool | None) -> bool:
    def _f_15866():
        _x_15865 = True
        return True
    _alt_15867 = _f_15866
    def _f_15891(s_363: bool):
        _alt_15868 = _f_15866
        def _f_15878():
            _x_15872 = 0
            _x_15875 = float_dec_lt(0, c_361)
            _x_15877 = _x_15875 == s_363
            return _x_15877
        _alt_15879 = _f_15878
        _x_15882 = 0
        _x_15885 = c_361 == 0
        if _x_15885:
            _x_15889 = _alt_15868()
            return _x_15889
        else:
            _x_15887 = _alt_15879()
            return _x_15887
    _alt_15892 = _f_15891
    if sign is None:
        _x_15894 = _alt_15867()
        return _x_15894
    else:
        val_15895 = sign
        _x_15896 = _alt_15892(val_15895)
        return _x_15896

# Lean: Corpus.Geometry.isConvexPolygon.sub
def sub(a_365: Point2D, b_366: Point2D) -> Point2D:
    _x_15902 = a_365.point2d_0
    _x_15903 = b_366.point2d_0
    _x_15904 = _x_15902 - _x_15903
    _x_15905 = a_365.point2d_1
    _x_15906 = b_366.point2d_1
    _x_15907 = _x_15905 - _x_15906
    _x_15908 = Point2D_mk(_x_15904, _x_15907)
    return _x_15908

# Lean: Corpus.Geometry.isConvexPolygon.check
def is_convex_polygon_check(first: Point2D, second: Point2D, prev2: Point2D, prev1: Point2D, vs: list[Point2D], sign_367: bool | None) -> bool:
    def _f_15927():
        _x_15910 = sub(prev1, prev2)
        _x_15911 = sub(first, prev1)
        _x_15912 = cross2d(_x_15910, _x_15911)
        _x_15913 = sub(second, first)
        _x_15914 = cross2d(_x_15911, _x_15913)
        def _f_15916():
            _x_15915 = False
            return False
        _alt_15917 = _f_15916
        def _f_15919():
            _x_15918 = check_sign(_x_15914, sign_367)
            return _x_15918
        _alt_15920 = _f_15919
        _x_15921 = check_sign(_x_15912, sign_367)
        if _x_15921:
            _x_15925 = _alt_15920()
            return _x_15925
        else:
            _x_15923 = _alt_15917()
            return _x_15923
    _alt_15928 = _f_15927
    def _f_15959(v: Point2D, rest_: list[Point2D]):
        _x_15929 = sub(prev1, prev2)
        _x_15930 = sub(v, prev1)
        _x_15931 = cross2d(_x_15929, _x_15930)
        def _f_15933():
            _x_15932 = False
            return False
        _alt_15934 = _f_15933
        def _f_15951():
            _x_15937 = 0
            _x_15940 = _x_15931 == 0
            _x_15941 = True
            def _jp_15950(_y_15948: bool | None):
                _x_15949 = is_convex_polygon_check(first, second, prev1, v, rest_, _y_15948)
                return _x_15949
            if _x_15940:
                return _jp_15950(sign_367)
            else:
                _x_15944 = float_dec_lt(0, _x_15931)
                _x_15946 = _x_15944
                return _jp_15950(_x_15946)
        _alt_15952 = _f_15951
        _x_15953 = check_sign(_x_15931, sign_367)
        if _x_15953:
            _x_15957 = _alt_15952()
            return _x_15957
        else:
            _x_15955 = _alt_15934()
            return _x_15955
    _alt_15960 = _f_15959
    if len(vs) == 0:
        _x_15962 = _alt_15928()
        return _x_15962
    else:
        head_15963 = vs[0]
        tail_15964 = vs[1:]
        _x_15965 = _alt_15960(head_15963, tail_15964)
        return _x_15965

# Lean: Corpus.Geometry.polygonArea.go
def polygon_area_go(vs_374: list[Point2D], first_375: Point2D, prev_376: Point2D, acc_377: float) -> float:
    def _f_15980():
        _x_15974 = cross2d(prev_376, first_375)
        _x_15975 = acc_377 + _x_15974
        _x_15976 = 2
        _x_15979 = _x_15975 // 2
        return _x_15979
    _alt_15981 = _f_15980
    def _f_15988(v_379: Point2D, rest_380: list[Point2D]):
        _x_15985 = cross2d(prev_376, v_379)
        _x_15986 = acc_377 + _x_15985
        _x_15987 = polygon_area_go(rest_380, first_375, v_379, _x_15986)
        return _x_15987
    _alt_15989 = _f_15988
    if len(vs_374) == 0:
        _x_15991 = _alt_15981()
        return _x_15991
    else:
        head_15992 = vs_374[0]
        tail_15993 = vs_374[1:]
        _x_15994 = _alt_15989(head_15992, tail_15993)
        return _x_15994

# Lean: Corpus.Geometry.pointInTriangle.sign
def sign(p1: Point2D, p2: Point2D, p3: Point2D) -> float:
    _x_16003 = p1.point2d_0
    _x_16004 = p3.point2d_0
    _x_16005 = _x_16003 - _x_16004
    _x_16006 = p2.point2d_1
    _x_16007 = p3.point2d_1
    _x_16008 = _x_16006 - _x_16007
    _x_16009 = _x_16005 * _x_16008
    _x_16010 = p2.point2d_0
    _x_16011 = _x_16010 - _x_16004
    _x_16012 = p1.point2d_1
    _x_16013 = _x_16012 - _x_16007
    _x_16014 = _x_16011 * _x_16013
    _x_16015 = _x_16009 - _x_16014
    return _x_16015

# Lean: Corpus.NumberTheory.isHarshad.digitSum
def digit_sum(n_381: int) -> int:
    _x_16019 = 0
    _x_16022 = n_381 == 0
    _x_16023 = True
    if _x_16022:
        return 0
    else:
        _x_16032 = 10
        _x_16035 = n_381 % 10
        _x_16039 = n_381 // 10
        _x_16040 = digit_sum(_x_16039)
        _x_16041 = _x_16035 + _x_16040
        return _x_16041

# Lean: Corpus.NumberTheory.digitalRoot.digitSum
def digit_sum(n_382: int) -> int:
    _x_16047 = 0
    _x_16050 = n_382 == 0
    _x_16051 = True
    if _x_16050:
        return 0
    else:
        _x_16060 = 10
        _x_16063 = n_382 % 10
        _x_16067 = n_382 // 10
        _x_16068 = digit_sum(_x_16067)
        _x_16069 = _x_16063 + _x_16068
        return _x_16069

# Lean: Corpus.NumberTheory.isqrt.go
def isqrt_go(n_383: int, x_384: int, fuel: int) -> int:
    def _f_16073():
        return x_384
    _alt_16074 = _f_16073
    def _f_16092(fuel_: int):
        _x_16081 = n_383 // x_384
        _x_16082 = x_384 + _x_16081
        _x_16083 = 2
        _x_16086 = _x_16082 // 2
        _x_16087 = x_384 <= _x_16086
        if _x_16087:
            return x_384
        else:
            _x_16089 = isqrt_go(n_383, _x_16086, fuel_)
            return _x_16089
    _alt_16093 = _f_16092
    if fuel == 0:
        _x_16095 = _alt_16074()
        return _x_16095
    else:
        n_16096 = fuel - 1
        _x_16097 = _alt_16093(n_16096)
        return _x_16097

# Lean: Corpus.NumberTheory.totient.gcd
def totient_gcd(a_387: int, b_388: int) -> int:
    _x_16102 = 0
    _x_16105 = b_388 == 0
    _x_16106 = True
    if _x_16105:
        return a_387
    else:
        _x_16112 = a_387 % b_388
        _x_16113 = totient_gcd(b_388, _x_16112)
        return _x_16113

# Lean: Corpus.NumberTheory.totient.count
def count(n_389: int, i_390: int, acc_391: int) -> int:
    _x_16119 = i_390 == n_389
    _x_16120 = True
    if _x_16119:
        return acc_391
    else:
        _x_16123 = totient_gcd(i_390, n_389)
        _x_16124 = 1
        _x_16127 = _x_16123 == 1
        if _x_16127:
            _x_16139 = i_390 + 1
            _x_16140 = acc_391 + 1
            _x_16141 = count(n_389, _x_16139, _x_16140)
            return _x_16141
        else:
            _x_16133 = i_390 + 1
            _x_16134 = count(n_389, _x_16133, acc_391)
            return _x_16134

# Lean: Corpus.Advanced.Graph.topoSort.loop
def topo_sort_loop(g: Graph, queue: list[int], in_deg: list[int], result: list[int], fuel_392: int) -> list[int] | None:
    def _f_16147():
        _x_16146 = None
        return _x_16146
    _alt_16148 = _f_16147
    def _f_16239(fuel__394: int):
        def _f_16162():
            _x_16151 = len(result)
            _x_16152 = g.advanced_graph_0
            _x_16153 = _x_16151 == _x_16152
            _x_16154 = True
            if _x_16153:
                _x_16159 = list(reversed(result))
                _x_16160 = _x_16159
                return _x_16160
            else:
                _x_16157 = None
                return _x_16157
        _alt_16163 = _f_16162
        def _f_16231(v_396: int, rest_397: list[int]):
            _x_16164 = [v_396] + result
            def _f_16170(x_16165: tuple[int, int]):
                _x_16168 = x_16165[0]
                _x_16169 = _x_16168 == v_396
                return _x_16169
            _x_16171 = g.advanced_graph_1
            _x_16172 = [x for x in _x_16171 if _f_16170(x)]
            def _f_16174(new_in_deg: list[int], new_queue: list[int]):
                _x_16173 = topo_sort_loop(g, new_queue, new_in_deg, _x_16164, fuel__394)
                return _x_16173
            _alt_16175 = _f_16174
            def _f_16224(x_16176: tuple[list[int], list[int]], x_16177: tuple[int, int]):
                def _f_16218(deg: list[int], q_398: list[int]):
                    def _f_16212(fst_16178: int, w_399: int):
                        def _f_16201(d_400: int):
                            _x_16182 = 1
                            _x_16185 = d_400 - 1
                            _x_16186 = deg[:w_399] + [_x_16185] + deg[w_399+1:]
                            _x_16189 = 0
                            _x_16192 = _x_16185 == 0
                            _x_16193 = True
                            if _x_16192:
                                _x_16198 = [w_399] + q_398
                                _x_16199 = (_x_16186, _x_16198)
                                return _x_16199
                            else:
                                _x_16196 = (_x_16186, q_398)
                                return _x_16196
                        _alt_16202 = _f_16201
                        def _f_16204():
                            _x_16203 = (deg, q_398)
                            return _x_16203
                        _alt_16205 = _f_16204
                        _x_16206 = deg[w_399] if 0 <= w_399 < len(deg) else None
                        if _x_16206 is None:
                            _x_16208 = _alt_16205()
                            return _x_16208
                        else:
                            val_16209 = _x_16206
                            _x_16210 = _alt_16202(val_16209)
                            return _x_16210
                    _alt_16213 = _f_16212
                    match x_16177:
                        case (fst_16214, snd_16215):
                            _x_16216 = _alt_16213(fst_16214, snd_16215)
                            return _x_16216
                _alt_16219 = _f_16218
                match x_16176:
                    case (fst_16220, snd_16221):
                        _x_16222 = _alt_16219(fst_16220, snd_16221)
                        return _x_16222
            _x_16225 = (in_deg, rest_397)
            _x_16226 = functools.reduce(_f_16224, _x_16172, _x_16225)
            match _x_16226:
                case (fst_16227, snd_16228):
                    _x_16229 = _alt_16175(fst_16227, snd_16228)
                    return _x_16229
        _alt_16232 = _f_16231
        if len(queue) == 0:
            _x_16234 = _alt_16163()
            return _x_16234
        else:
            head_16235 = queue[0]
            tail_16236 = queue[1:]
            _x_16237 = _alt_16232(head_16235, tail_16236)
            return _x_16237
    _alt_16240 = _f_16239
    if fuel_392 == 0:
        _x_16242 = _alt_16148()
        return _x_16242
    else:
        n_16243 = fuel_392 - 1
        _x_16244 = _alt_16240(n_16243)
        return _x_16244

# Lean: Corpus.Advanced.Graph.dfs.loop
def dfs_loop(g_402: Graph, stack: list[int], visited: list[int], fuel_403: int) -> list[int]:
    def _f_16248():
        _x_16247 = list(reversed(visited))
        return _x_16247
    _alt_16249 = _f_16248
    def _f_16279(fuel__405: int):
        _alt_16250 = _f_16248
        def _f_16271(v_406: int, rest_407: list[int]):
            _x_16252 = v_406 in visited
            _x_16253 = True
            if _x_16252:
                _x_16269 = dfs_loop(g_402, rest_407, visited, fuel__405)
                return _x_16269
            else:
                _x_16256 = [v_406] + visited
                def _f_16260(x_16257: int):
                    _x_16258 = x_16257 in _x_16256
                    _x_16259 = not _x_16258
                    return _x_16259
                _x_16261 = advanced_graph_neighbors(g_402, v_406)
                _x_16262 = [x for x in _x_16261 if _f_16260(x)]
                _x_16266 = _x_16262 + rest_407
                _x_16267 = dfs_loop(g_402, _x_16266, _x_16256, fuel__405)
                return _x_16267
        _alt_16272 = _f_16271
        if len(stack) == 0:
            _x_16274 = _alt_16250()
            return _x_16274
        else:
            head_16275 = stack[0]
            tail_16276 = stack[1:]
            _x_16277 = _alt_16272(head_16275, tail_16276)
            return _x_16277
    _alt_16280 = _f_16279
    if fuel_403 == 0:
        _x_16282 = _alt_16249()
        return _x_16282
    else:
        n_16283 = fuel_403 - 1
        _x_16284 = _alt_16280(n_16283)
        return _x_16284

# Lean: Corpus.Advanced.Graph.bfs.loop
def bfs_loop(g_408: Graph, queue_409: list[int], visited_410: list[int], fuel_411: int) -> list[int]:
    def _f_16288():
        _x_16287 = list(reversed(visited_410))
        return _x_16287
    _alt_16289 = _f_16288
    def _f_16319(fuel__413: int):
        _alt_16290 = _f_16288
        def _f_16311(v_414: int, rest_415: list[int]):
            _x_16292 = v_414 in visited_410
            _x_16293 = True
            if _x_16292:
                _x_16309 = bfs_loop(g_408, rest_415, visited_410, fuel__413)
                return _x_16309
            else:
                _x_16296 = [v_414] + visited_410
                def _f_16300(x_16297: int):
                    _x_16298 = x_16297 in _x_16296
                    _x_16299 = not _x_16298
                    return _x_16299
                _x_16301 = advanced_graph_neighbors(g_408, v_414)
                _x_16302 = [x for x in _x_16301 if _f_16300(x)]
                _x_16306 = rest_415 + _x_16302
                _x_16307 = bfs_loop(g_408, _x_16306, _x_16296, fuel__413)
                return _x_16307
        _alt_16312 = _f_16311
        if len(queue_409) == 0:
            _x_16314 = _alt_16290()
            return _x_16314
        else:
            head_16315 = queue_409[0]
            tail_16316 = queue_409[1:]
            _x_16317 = _alt_16312(head_16315, tail_16316)
            return _x_16317
    _alt_16320 = _f_16319
    if fuel_411 == 0:
        _x_16322 = _alt_16289()
        return _x_16322
    else:
        n_16323 = fuel_411 - 1
        _x_16324 = _alt_16320(n_16323)
        return _x_16324

# Lean: Corpus.Advanced.heapSort.extract
def extract(__418: Any, inst_16327: Any, h: Any, acc_419: list[Any], fuel_420: int) -> list[Any]:
    def _f_16329():
        _x_16328 = list(reversed(acc_419))
        return _x_16328
    _alt_16330 = _f_16329
    def _f_16343(fuel__422: int):
        _alt_16331 = _f_16329
        def _f_16335(x_423: Any):
            _x_16332 = pop_min(None, inst_16327, h)
            _x_16333 = [x_423] + acc_419
            _x_16334 = extract(None, inst_16327, _x_16332, _x_16333, fuel__422)
            return _x_16334
        _alt_16336 = _f_16335
        _x_16337 = advanced_heap_min(None, h)
        if _x_16337 is None:
            _x_16339 = _alt_16331()
            return _x_16339
        else:
            val_16340 = _x_16337
            _x_16341 = _alt_16336(val_16340)
            return _x_16341
    _alt_16344 = _f_16343
    if fuel_420 == 0:
        _x_16346 = _alt_16330()
        return _x_16346
    else:
        n_16347 = fuel_420 - 1
        _x_16348 = _alt_16344(n_16347)
        return _x_16348

# Lean: Corpus.DataStructures.Trie.hasPrefix.go
def has_prefix_go(t_424: Trie, chars: list[str]) -> bool:
    def _f_16353(x_16351: Trie):
        _x_16352 = True
        return True
    _alt_16354 = _f_16353
    def _f_16385(a_16355: bool, children: list[tuple[str, Trie]], c_425: str, cs: list[str]):
        def _f_16358(fst_16356: str, child: Trie):
            _x_16357 = has_prefix_go(child, cs)
            return _x_16357
        _alt_16359 = _f_16358
        def _f_16361():
            _x_16360 = False
            return False
        _alt_16362 = _f_16361
        def _f_16375(x_16363: tuple[str, Trie]):
            def _f_16369(ch: str, snd_16364: Trie):
                _x_16368 = ch == c_425
                return _x_16368
            _alt_16370 = _f_16369
            match x_16363:
                case (fst_16371, snd_16372):
                    _x_16373 = _alt_16370(fst_16371, snd_16372)
                    return _x_16373
        _x_16376 = next((x for x in children if _f_16375(x)), None)
        if _x_16376 is None:
            _x_16378 = _alt_16362()
            return _x_16378
        else:
            val_16379 = _x_16376
            match val_16379:
                case (fst_16380, snd_16381):
                    _x_16382 = _alt_16359(fst_16380, snd_16381)
                    return _x_16382
    _alt_16386 = _f_16385
    match t_424:
        case Trie_node(a_16387, a_16388):
            if len(chars) == 0:
                _x_16389 = Trie_node(a_16387, a_16388)
                _x_16390 = _alt_16354(_x_16389)
                return _x_16390
            else:
                head_16391 = chars[0]
                tail_16392 = chars[1:]
                _x_16393 = _alt_16386(a_16387, a_16388, head_16391, tail_16392)
                return _x_16393

# Lean: Corpus.DataStructures.Trie.contains.go
def trie_contains_go(t_427: Trie, chars_428: list[str]) -> bool:
    def _f_16398(is_end: bool, a_16397: list[tuple[str, Trie]]):
        return is_end
    _alt_16399 = _f_16398
    def _f_16430(a_16400: bool, children_429: list[tuple[str, Trie]], c_430: str, cs_431: list[str]):
        def _f_16403(fst_16401: str, child_432: Trie):
            _x_16402 = trie_contains_go(child_432, cs_431)
            return _x_16402
        _alt_16404 = _f_16403
        def _f_16406():
            _x_16405 = False
            return False
        _alt_16407 = _f_16406
        def _f_16420(x_16408: tuple[str, Trie]):
            def _f_16414(ch_434: str, snd_16409: Trie):
                _x_16413 = ch_434 == c_430
                return _x_16413
            _alt_16415 = _f_16414
            match x_16408:
                case (fst_16416, snd_16417):
                    _x_16418 = _alt_16415(fst_16416, snd_16417)
                    return _x_16418
        _x_16421 = next((x for x in children_429 if _f_16420(x)), None)
        if _x_16421 is None:
            _x_16423 = _alt_16407()
            return _x_16423
        else:
            val_16424 = _x_16421
            match val_16424:
                case (fst_16425, snd_16426):
                    _x_16427 = _alt_16404(fst_16425, snd_16426)
                    return _x_16427
    _alt_16431 = _f_16430
    match t_427:
        case Trie_node(a_16432, a_16433):
            if len(chars_428) == 0:
                _x_16434 = _alt_16399(a_16432, a_16433)
                return _x_16434
            else:
                head_16435 = chars_428[0]
                tail_16436 = chars_428[1:]
                _x_16437 = _alt_16431(a_16432, a_16433, head_16435, tail_16436)
                return _x_16437

# Lean: Corpus.DataStructures.Trie.insert.go
def trie_insert_go(t_435: Trie, chars_436: list[str]) -> Trie:
    def _f_16443(is_end_437: bool, children_438: list[tuple[str, Trie]]):
        _x_16441 = True
        _x_16442 = Trie_node(True, children_438)
        return _x_16442
    _alt_16444 = _f_16443
    def _f_16506(is_end_439: bool, children_440: list[tuple[str, Trie]], c_441: str, cs_442: list[str]):
        def _f_16467(fst_16445: str, child_443: Trie):
            def _f_16465(x_16446: tuple[str, Trie]):
                def _f_16459(ch_444: str, t_: Trie):
                    _x_16450 = ch_444 == c_441
                    _x_16451 = True
                    if _x_16450:
                        _x_16456 = trie_insert_go(t_, cs_442)
                        _x_16457 = (ch_444, _x_16456)
                        return _x_16457
                    else:
                        _x_16454 = (ch_444, t_)
                        return _x_16454
                _alt_16460 = _f_16459
                match x_16446:
                    case (fst_16461, snd_16462):
                        _x_16463 = _alt_16460(fst_16461, snd_16462)
                        return _x_16463
            _x_16466 = [_f_16465(x) for x in children_440]
            return _x_16466
        _alt_16468 = _f_16467
        def _f_16473():
            _x_16469 = trie_empty()
            _x_16470 = trie_insert_go(_x_16469, cs_442)
            _x_16471 = (c_441, _x_16470)
            _x_16472 = [_x_16471] + children_440
            return _x_16472
        _alt_16474 = _f_16473
        def _f_16487(x_16475: tuple[str, Trie]):
            def _f_16481(ch_446: str, snd_16476: Trie):
                _x_16480 = ch_446 == c_441
                return _x_16480
            _alt_16482 = _f_16481
            match x_16475:
                case (fst_16483, snd_16484):
                    _x_16485 = _alt_16482(fst_16483, snd_16484)
                    return _x_16485
        _x_16488 = next((x for x in children_440 if _f_16487(x)), None)
        def _jp_16498(_y_16496: list[tuple[str, Trie]]):
            _x_16497 = Trie_node(is_end_439, _y_16496)
            return _x_16497
        def _jp_16501():
            _x_16500 = _alt_16474()
            return _jp_16498(_x_16500)
        def _jp_16505(_y_16502: str, _y_16503: Trie):
            _x_16504 = _alt_16468(_y_16502, _y_16503)
            return _jp_16498(_x_16504)
        if _x_16488 is None:
            return _jp_16501()
        else:
            val_16491 = _x_16488
            match val_16491:
                case (fst_16492, snd_16493):
                    return _jp_16505(fst_16492, snd_16493)
    _alt_16507 = _f_16506
    match t_435:
        case Trie_node(a_16508, a_16509):
            if len(chars_436) == 0:
                _x_16510 = _alt_16444(a_16508, a_16509)
                return _x_16510
            else:
                head_16511 = chars_436[0]
                tail_16512 = chars_436[1:]
                _x_16513 = _alt_16507(a_16508, a_16509, head_16511, tail_16512)
                return _x_16513

# Lean: Corpus.DataStructures.BinaryTree.levelOrder.go
def level_order_go(__447: Any, queue_448: list[Any], acc_449: list[Any], fuel_450: int) -> list[Any]:
    def _f_16518():
        _x_16517 = list(reversed(acc_449))
        return _x_16517
    _alt_16519 = _f_16518
    def _f_16546(fuel__452: int):
        _alt_16520 = _f_16518
        def _f_16522(rest_453: list[Any]):
            _x_16521 = level_order_go(None, rest_453, acc_449, fuel__452)
            return _x_16521
        _alt_16523 = _f_16522
        def _f_16533(v_454: Any, l_455: Any, r_456: Any, rest_457: list[Any]):
            _x_16527 = []
            _x_16528 = [r_456] + _x_16527
            _x_16529 = [l_455] + _x_16528
            _x_16530 = rest_457 + _x_16529
            _x_16531 = [v_454] + acc_449
            _x_16532 = level_order_go(None, _x_16530, _x_16531, fuel__452)
            return _x_16532
        _alt_16534 = _f_16533
        if len(queue_448) == 0:
            _x_16536 = _alt_16520()
            return _x_16536
        else:
            head_16537 = queue_448[0]
            tail_16538 = queue_448[1:]
            match head_16537:
                case BinaryTree_empty():
                    _x_16539 = _alt_16523(tail_16538)
                    return _x_16539
                case BinaryTree_node(a_16540, a_16541, a_16542):
                    _x_16543 = _alt_16534(a_16540, a_16541, a_16542, tail_16538)
                    return _x_16543
    _alt_16547 = _f_16546
    if fuel_450 == 0:
        _x_16549 = _alt_16519()
        return _x_16549
    else:
        n_16550 = fuel_450 - 1
        _x_16551 = _alt_16547(n_16550)
        return _x_16551

# Lean: Corpus.Games.rollDice.go
def roll_dice_go(sides: int, n_458: int, seed: int, acc_459: list[int]) -> tuple[list[int], int]:
    def _f_16556():
        _x_16554 = list(reversed(acc_459))
        _x_16555 = (_x_16554, seed)
        return _x_16555
    _alt_16557 = _f_16556
    def _f_16594(n_: int):
        _x_16567 = 1103515245
        _x_16570 = seed * 1103515245
        _x_16571 = 12345
        _x_16574 = _x_16570 + 12345
        _x_16579 = 2
        _x_16582 = 31
        _x_16585 = 2 ** 31
        _x_16586 = _x_16574 % _x_16585
        _x_16587 = _x_16586 % sides
        _x_16588 = 1
        _x_16591 = _x_16587 + 1
        _x_16592 = [_x_16591] + acc_459
        _x_16593 = roll_dice_go(sides, n_, _x_16586, _x_16592)
        return _x_16593
    _alt_16595 = _f_16594
    if n_458 == 0:
        _x_16597 = _alt_16557()
        return _x_16597
    else:
        n_16598 = n_458 - 1
        _x_16599 = _alt_16595(n_16598)
        return _x_16599

# Lean: Corpus.Games.BlackjackHand.bestValue.adjust
def best_value_adjust(value_461: int, aces: int) -> int:
    def _f_16602():
        return value_461
    _alt_16603 = _f_16602
    def _f_16619(aces_: int):
        _x_16604 = 21
        _x_16607 = value_461 <= 21
        if _x_16607:
            return value_461
        else:
            _x_16612 = 10
            _x_16615 = value_461 - 10
            _x_16616 = best_value_adjust(_x_16615, aces_)
            return _x_16616
    _alt_16620 = _f_16619
    if aces == 0:
        _x_16622 = _alt_16603()
        return _x_16622
    else:
        n_16623 = aces - 1
        _x_16624 = _alt_16620(n_16623)
        return _x_16624

# Lean: Corpus.Strings.words.go
def words_go(chars_463: list[str], current: list[str], acc_464: list[str]) -> list[str]:
    def _f_16638():
        _x_16627 = len(current) == 0
        _x_16628 = True
        if _x_16627:
            _x_16636 = list(reversed(acc_464))
            return _x_16636
        else:
            _x_16631 = list(reversed(current))
            _x_16632 = ''.join(_x_16631)
            _x_16633 = [_x_16632] + acc_464
            _x_16634 = list(reversed(_x_16633))
            return _x_16634
    _alt_16639 = _f_16638
    def _f_16665(c_466: str, cs_467: list[str]):
        _x_16643 = 32
        _x_16644 = chr(_x_16643)
        _x_16645 = c_466 == _x_16644
        _x_16646 = True
        if _x_16645:
            _x_16652 = len(current) == 0
            if _x_16652:
                _x_16661 = []
                _x_16662 = words_go(cs_467, _x_16661, acc_464)
                return _x_16662
            else:
                _x_16655 = []
                _x_16656 = list(reversed(current))
                _x_16657 = ''.join(_x_16656)
                _x_16658 = [_x_16657] + acc_464
                _x_16659 = words_go(cs_467, _x_16655, _x_16658)
                return _x_16659
        else:
            _x_16649 = [c_466] + current
            _x_16650 = words_go(cs_467, _x_16649, acc_464)
            return _x_16650
    _alt_16666 = _f_16665
    if len(chars_463) == 0:
        _x_16668 = _alt_16639()
        return _x_16668
    else:
        head_16669 = chars_463[0]
        tail_16670 = chars_463[1:]
        _x_16671 = _alt_16666(head_16669, tail_16670)
        return _x_16671

# Lean: Corpus.Strings.splitOn.go
def split_on_go(sep: str, chars_468: list[str], current_469: list[str], acc_470: list[str]) -> list[str]:
    def _f_16678():
        _x_16674 = list(reversed(current_469))
        _x_16675 = ''.join(_x_16674)
        _x_16676 = [_x_16675] + acc_470
        _x_16677 = list(reversed(_x_16676))
        return _x_16677
    _alt_16679 = _f_16678
    def _f_16707(cs_472: list[str]):
        _x_16680 = ''.join(cs_472)
        _x_16681 = starts_with(_x_16680, sep)
        _x_16682 = True
        if _x_16681:
            _x_16699 = len(sep)
            _x_16700 = (lambda n, xs: xs[n:])(cs_472)
            _x_16701 = []
            _x_16702 = list(reversed(current_469))
            _x_16703 = ''.join(_x_16702)
            _x_16704 = [_x_16703] + acc_470
            _x_16705 = split_on_go(sep, _x_16700, _x_16701, _x_16704)
            return _x_16705
        else:
            def _f_16687(c_473: str, cs_: list[str]):
                _x_16685 = [c_473] + current_469
                _x_16686 = split_on_go(sep, cs_, _x_16685, acc_470)
                return _x_16686
            _alt_16688 = _f_16687
            def _f_16690():
                _x_16689 = list(reversed(acc_470))
                return _x_16689
            _alt_16691 = _f_16690
            if len(cs_472) == 0:
                _x_16693 = _alt_16691()
                return _x_16693
            else:
                head_16694 = cs_472[0]
                tail_16695 = cs_472[1:]
                _x_16696 = _alt_16688(head_16694, tail_16695)
                return _x_16696
    _alt_16708 = _f_16707
    if len(chars_468) == 0:
        _x_16710 = _alt_16679()
        return _x_16710
    else:
        head_16711 = chars_468[0]
        tail_16712 = chars_468[1:]
        _x_16713 = [head_16711] + tail_16712
        _x_16714 = _alt_16708(_x_16713)
        return _x_16714

# Lean: Corpus.Strings.count.go
def count_go(sub: str, chars_475: list[str], cnt: int) -> int:
    def _f_16717():
        return cnt
    _alt_16718 = _f_16717
    def _f_16736(c_477: str, cs_478: list[str]):
        _x_16719 = [c_477] + cs_478
        _x_16720 = ''.join(_x_16719)
        _x_16721 = starts_with(_x_16720, sub)
        _x_16722 = True
        if _x_16721:
            _x_16730 = 1
            _x_16733 = cnt + 1
            _x_16734 = count_go(sub, cs_478, _x_16733)
            return _x_16734
        else:
            _x_16725 = count_go(sub, cs_478, cnt)
            return _x_16725
    _alt_16737 = _f_16736
    if len(chars_475) == 0:
        _x_16739 = _alt_16718()
        return _x_16739
    else:
        head_16740 = chars_475[0]
        tail_16741 = chars_475[1:]
        _x_16742 = _alt_16737(head_16740, tail_16741)
        return _x_16742

# Lean: Corpus.Strings.indexOf.go
def index_of_go(sub_479: str, chars_480: list[str], idx_481: int) -> int | None:
    def _f_16759():
        _x_16747 = len(sub_479)
        _x_16748 = 0
        _x_16751 = _x_16747 == 0
        _x_16752 = True
        if _x_16751:
            _x_16757 = idx_481
            return _x_16757
        else:
            _x_16755 = None
            return _x_16755
    _alt_16760 = _f_16759
    def _f_16778(c_483: str, cs_484: list[str]):
        _x_16761 = [c_483] + cs_484
        _x_16762 = ''.join(_x_16761)
        _x_16763 = starts_with(_x_16762, sub_479)
        _x_16764 = True
        if _x_16763:
            _x_16776 = idx_481
            return _x_16776
        else:
            _x_16770 = 1
            _x_16773 = idx_481 + 1
            _x_16774 = index_of_go(sub_479, cs_484, _x_16773)
            return _x_16774
    _alt_16779 = _f_16778
    if len(chars_480) == 0:
        _x_16781 = _alt_16760()
        return _x_16781
    else:
        head_16782 = chars_480[0]
        tail_16783 = chars_480[1:]
        _x_16784 = _alt_16779(head_16782, tail_16783)
        return _x_16784

# Lean: Corpus.Strings.contains.go
def strings_contains_go(sub_485: str, chars_486: list[str]) -> bool:
    def _f_16794():
        _x_16789 = len(sub_485)
        _x_16790 = 0
        _x_16793 = _x_16789 == 0
        return _x_16793
    _alt_16795 = _f_16794
    def _f_16805(c_488: str, cs_489: list[str]):
        _x_16796 = [c_488] + cs_489
        _x_16797 = ''.join(_x_16796)
        _x_16798 = starts_with(_x_16797, sub_485)
        _x_16799 = True
        if _x_16798:
            return True
        else:
            _x_16802 = strings_contains_go(sub_485, cs_489)
            return _x_16802
    _alt_16806 = _f_16805
    if len(chars_486) == 0:
        _x_16808 = _alt_16795()
        return _x_16808
    else:
        head_16809 = chars_486[0]
        tail_16810 = chars_486[1:]
        _x_16811 = _alt_16806(head_16809, tail_16810)
        return _x_16811

# Lean: Corpus.Strings.replicate.go
def strings_replicate_go(s_490: str, n_491: int, acc_492: str) -> str:
    def _f_16814():
        return acc_492
    _alt_16815 = _f_16814
    def _f_16821(n__494: int):
        _x_16819 = acc_492 + s_490
        _x_16820 = strings_replicate_go(s_490, n__494, _x_16819)
        return _x_16820
    _alt_16822 = _f_16821
    if n_491 == 0:
        _x_16824 = _alt_16815()
        return _x_16824
    else:
        n_16825 = n_491 - 1
        _x_16826 = _alt_16822(n_16825)
        return _x_16826

# Lean: Corpus.Math.digitalRoot.go
def digital_root_go(n_495: int, fuel_496: int) -> int:
    def _f_16829():
        return n_495
    _alt_16830 = _f_16829
    def _f_16840(fuel__498: int):
        _x_16831 = 10
        _x_16834 = digit_sum(n_495, 10)
        _x_16835 = _x_16834 < 10
        if _x_16835:
            return _x_16834
        else:
            _x_16837 = digital_root_go(_x_16834, fuel__498)
            return _x_16837
    _alt_16841 = _f_16840
    if fuel_496 == 0:
        _x_16843 = _alt_16830()
        return _x_16843
    else:
        n_16844 = fuel_496 - 1
        _x_16845 = _alt_16841(n_16844)
        return _x_16845

# Lean: Corpus.Math.digits.go
def digits_go(base: int, n_500: int, acc_501: list[int]) -> list[int]:
    _x_16850 = 0
    _x_16853 = n_500 == 0
    _x_16854 = True
    if _x_16853:
        _x_16868 = len(acc_501) == 0
        if _x_16868:
            _x_16872 = []
            _x_16873 = [0] + _x_16872
            return _x_16873
        else:
            return acc_501
    else:
        _x_16860 = n_500 // base
        _x_16864 = n_500 % base
        _x_16865 = [_x_16864] + acc_501
        _x_16866 = digits_go(base, _x_16860, _x_16865)
        return _x_16866

# Lean: Corpus.Math.isqrt.go
def isqrt_go(n_502: int, x_503: int, fuel_504: int) -> int:
    def _f_16877():
        return x_503
    _alt_16878 = _f_16877
    def _f_16896(fuel__506: int):
        _x_16885 = n_502 // x_503
        _x_16886 = x_503 + _x_16885
        _x_16887 = 2
        _x_16890 = _x_16886 // 2
        _x_16891 = x_503 <= _x_16890
        if _x_16891:
            return x_503
        else:
            _x_16893 = isqrt_go(n_502, _x_16890, fuel__506)
            return _x_16893
    _alt_16897 = _f_16896
    if fuel_504 == 0:
        _x_16899 = _alt_16878()
        return _x_16899
    else:
        n_16900 = fuel_504 - 1
        _x_16901 = _alt_16897(n_16900)
        return _x_16901

# Lean: Corpus.Math.binomial.go
def binomial_go(n_507: int, k_508: int, num: int, den: int, i_509: int) -> int:
    _x_16904 = k_508 < i_509
    if _x_16904:
        _x_16928 = num // den
        return _x_16928
    else:
        _x_16915 = n_507 - i_509
        _x_16916 = 1
        _x_16919 = _x_16915 + 1
        _x_16920 = num * _x_16919
        _x_16921 = den * i_509
        _x_16922 = i_509 + 1
        _x_16923 = binomial_go(n_507, k_508, _x_16920, _x_16921, _x_16922)
        return _x_16923

# Lean: Corpus.Math.tribonacci.go
def tribonacci_go(a_510: int, b_511: int, c_512: int, k_513: int) -> int:
    def _f_16931():
        return a_510
    _alt_16932 = _f_16931
    def _f_16939(k__515: int):
        _x_16936 = a_510 + b_511
        _x_16937 = _x_16936 + c_512
        _x_16938 = tribonacci_go(b_511, c_512, _x_16937, k__515)
        return _x_16938
    _alt_16940 = _f_16939
    if k_513 == 0:
        _x_16942 = _alt_16932()
        return _x_16942
    else:
        n_16943 = k_513 - 1
        _x_16944 = _alt_16940(n_16943)
        return _x_16944

# Lean: Corpus.Math.lucas.go
def lucas_go(a_516: int, b_517: int, k_518: int) -> int:
    def _f_16947():
        return a_516
    _alt_16948 = _f_16947
    def _f_16954(k__520: int):
        _x_16952 = a_516 + b_517
        _x_16953 = lucas_go(b_517, _x_16952, k__520)
        return _x_16953
    _alt_16955 = _f_16954
    if k_518 == 0:
        _x_16957 = _alt_16948()
        return _x_16957
    else:
        n_16958 = k_518 - 1
        _x_16959 = _alt_16955(n_16958)
        return _x_16959

# Lean: Corpus.Math.fibonacci.go
def math_fibonacci_go(a_521: int, b_522: int, k_523: int) -> int:
    def _f_16962():
        return a_521
    _alt_16963 = _f_16962
    def _f_16969(k__525: int):
        _x_16967 = a_521 + b_522
        _x_16968 = math_fibonacci_go(b_522, _x_16967, k__525)
        return _x_16968
    _alt_16970 = _f_16969
    if k_523 == 0:
        _x_16972 = _alt_16963()
        return _x_16972
    else:
        n_16973 = k_523 - 1
        _x_16974 = _alt_16970(n_16973)
        return _x_16974

# Lean: Corpus.Math.divisors.go
def divisors_go(n_526: int, d_527: int, acc_528: list[int]) -> list[int]:
    _x_16980 = d_527 * d_527
    _x_16981 = n_526 < _x_16980
    if _x_16981:
        return acc_528
    else:
        _x_16988 = n_526 % d_527
        _x_16989 = 0
        _x_16992 = _x_16988 == 0
        _x_16993 = True
        if _x_16992:
            _x_17005 = _x_16980 == n_526
            if _x_17005:
                _x_17026 = 1
                _x_17029 = d_527 + 1
                _x_17030 = [d_527] + acc_528
                _x_17031 = divisors_go(n_526, _x_17029, _x_17030)
                return _x_17031
            else:
                _x_17011 = 1
                _x_17014 = d_527 + 1
                _x_17018 = n_526 // d_527
                _x_17019 = [_x_17018] + acc_528
                _x_17020 = [d_527] + _x_17019
                _x_17021 = divisors_go(n_526, _x_17014, _x_17020)
                return _x_17021
        else:
            _x_16999 = 1
            _x_17002 = d_527 + 1
            _x_17003 = divisors_go(n_526, _x_17002, acc_528)
            return _x_17003

# Lean: Corpus.Math.primeFactors.go
def math_prime_factors_go(n_529: int, d_530: int, acc_531: list[int], fuel_532: int) -> list[int]:
    def _f_17038():
        _x_17037 = list(reversed(acc_531))
        return _x_17037
    _alt_17039 = _f_17038
    def _f_17084(fuel__534: int):
        _x_17040 = 1
        _x_17043 = n_529 <= 1
        if _x_17043:
            _x_17082 = list(reversed(acc_531))
            return _x_17082
        else:
            _x_17048 = d_530 * d_530
            _x_17049 = n_529 < _x_17048
            if _x_17049:
                _x_17078 = [n_529] + acc_531
                _x_17079 = list(reversed(_x_17078))
                return _x_17079
            else:
                _x_17056 = n_529 % d_530
                _x_17057 = 0
                _x_17060 = _x_17056 == 0
                _x_17061 = True
                if _x_17060:
                    _x_17073 = n_529 // d_530
                    _x_17074 = [d_530] + acc_531
                    _x_17075 = math_prime_factors_go(_x_17073, d_530, _x_17074, fuel__534)
                    return _x_17075
                else:
                    _x_17067 = d_530 + 1
                    _x_17068 = math_prime_factors_go(n_529, _x_17067, acc_531, fuel__534)
                    return _x_17068
    _alt_17085 = _f_17084
    if fuel_532 == 0:
        _x_17087 = _alt_17039()
        return _x_17087
    else:
        n_17088 = fuel_532 - 1
        _x_17089 = _alt_17085(n_17088)
        return _x_17089

# Lean: Corpus.Math.isPrime.check
def math_is_prime_check(n_535: int, d_536: int, fuel_537: int) -> bool:
    def _f_17093():
        _x_17092 = True
        return True
    _alt_17094 = _f_17093
    def _f_17128(fuel__539: int):
        _x_17098 = d_536 * d_536
        _x_17099 = n_535 < _x_17098
        if _x_17099:
            _x_17126 = True
            return True
        else:
            _x_17106 = n_535 % d_536
            _x_17107 = 0
            _x_17110 = _x_17106 == 0
            _x_17111 = True
            if _x_17110:
                _x_17123 = False
                return False
            else:
                _x_17117 = 1
                _x_17120 = d_536 + 1
                _x_17121 = math_is_prime_check(n_535, _x_17120, fuel__539)
                return _x_17121
    _alt_17129 = _f_17128
    if fuel_537 == 0:
        _x_17131 = _alt_17094()
        return _x_17131
    else:
        n_17132 = fuel_537 - 1
        _x_17133 = _alt_17129(n_17132)
        return _x_17133

# Lean: Corpus.Math.modPow.go
def mod_pow_go(m_540: int, b_541: int, e_542: int, acc_543: int) -> int:
    def _f_17140():
        _x_17139 = acc_543 % m_540
        return _x_17139
    _alt_17141 = _f_17140
    def _f_17183(x_17142: int):
        _x_17148 = 2
        _x_17151 = e_542 % 2
        _x_17152 = 0
        _x_17155 = _x_17151 == 0
        _x_17156 = True
        if _x_17155:
            _x_17175 = b_541 * b_541
            _x_17176 = _x_17175 % m_540
            _x_17180 = e_542 // 2
            _x_17181 = mod_pow_go(m_540, _x_17176, _x_17180, acc_543)
            return _x_17181
        else:
            _x_17162 = b_541 * b_541
            _x_17163 = _x_17162 % m_540
            _x_17167 = e_542 // 2
            _x_17168 = acc_543 * b_541
            _x_17169 = _x_17168 % m_540
            _x_17170 = mod_pow_go(m_540, _x_17163, _x_17167, _x_17169)
            return _x_17170
    _alt_17184 = _f_17183
    _x_17185 = 0
    if e_542:
        _x_17189 = _alt_17184(e_542)
        return _x_17189
    else:
        _x_17191 = _alt_17141()
        return _x_17191

# Lean: Corpus.Math.fastPow.go
def fast_pow_go(b_545: int, e_546: int, acc_547: int) -> int:
    def _f_17194():
        return acc_547
    _alt_17195 = _f_17194
    def _f_17234(x_17196: int):
        _x_17202 = 2
        _x_17205 = e_546 % 2
        _x_17206 = 0
        _x_17209 = _x_17205 == 0
        _x_17210 = True
        if _x_17209:
            _x_17227 = b_545 * b_545
            _x_17231 = e_546 // 2
            _x_17232 = fast_pow_go(_x_17227, _x_17231, acc_547)
            return _x_17232
        else:
            _x_17216 = b_545 * b_545
            _x_17220 = e_546 // 2
            _x_17221 = acc_547 * b_545
            _x_17222 = fast_pow_go(_x_17216, _x_17220, _x_17221)
            return _x_17222
    _alt_17235 = _f_17234
    _x_17236 = 0
    if e_546:
        _x_17240 = _alt_17235(e_546)
        return _x_17240
    else:
        _x_17242 = _alt_17195()
        return _x_17242

# Lean: Corpus.Algorithms.reverse.go
def algorithms_reverse_go(__549: Any, xs_550: list[Any], acc_551: list[Any]) -> list[Any]:
    def _f_17245():
        return acc_551
    _alt_17246 = _f_17245
    def _f_17249(x_553: Any, xs__554: list[Any]):
        _x_17247 = [x_553] + acc_551
        _x_17248 = algorithms_reverse_go(None, xs__554, _x_17247)
        return _x_17248
    _alt_17250 = _f_17249
    if len(xs_550) == 0:
        _x_17252 = _alt_17246()
        return _x_17252
    else:
        head_17253 = xs_550[0]
        tail_17254 = xs_550[1:]
        _x_17255 = _alt_17250(head_17253, tail_17254)
        return _x_17255

# Lean: Corpus.Algorithms.power.go
def power_go(b_555: int, e_556: int, acc_557: int) -> int:
    def _f_17258():
        return acc_557
    _alt_17259 = _f_17258
    def _f_17298(x_17260: int):
        _x_17266 = 2
        _x_17269 = e_556 % 2
        _x_17270 = 0
        _x_17273 = _x_17269 == 0
        _x_17274 = True
        if _x_17273:
            _x_17291 = b_555 * b_555
            _x_17295 = e_556 // 2
            _x_17296 = power_go(_x_17291, _x_17295, acc_557)
            return _x_17296
        else:
            _x_17280 = b_555 * b_555
            _x_17284 = e_556 // 2
            _x_17285 = acc_557 * b_555
            _x_17286 = power_go(_x_17280, _x_17284, _x_17285)
            return _x_17286
    _alt_17299 = _f_17298
    _x_17300 = 0
    if e_556:
        _x_17304 = _alt_17299(e_556)
        return _x_17304
    else:
        _x_17306 = _alt_17259()
        return _x_17306

# Lean: Corpus.Algorithms.fibonacci.go
def algorithms_fibonacci_go(a_559: int, b_560: int, k_561: int) -> int:
    def _f_17309():
        return a_559
    _alt_17310 = _f_17309
    def _f_17316(k__563: int):
        _x_17314 = a_559 + b_560
        _x_17315 = algorithms_fibonacci_go(b_560, _x_17314, k__563)
        return _x_17315
    _alt_17317 = _f_17316
    if k_561 == 0:
        _x_17319 = _alt_17310()
        return _x_17319
    else:
        n_17320 = k_561 - 1
        _x_17321 = _alt_17317(n_17320)
        return _x_17321

# Lean: Corpus.Algorithms.primeFactors.go
def algorithms_prime_factors_go(n_564: int, d_565: int, acc_566: list[int], fuel_567: int) -> list[int]:
    def _f_17325():
        _x_17324 = list(reversed(acc_566))
        return _x_17324
    _alt_17326 = _f_17325
    def _f_17371(fuel__569: int):
        _x_17327 = 1
        _x_17330 = n_564 <= 1
        if _x_17330:
            _x_17369 = list(reversed(acc_566))
            return _x_17369
        else:
            _x_17335 = d_565 * d_565
            _x_17336 = n_564 < _x_17335
            if _x_17336:
                _x_17365 = [n_564] + acc_566
                _x_17366 = list(reversed(_x_17365))
                return _x_17366
            else:
                _x_17343 = n_564 % d_565
                _x_17344 = 0
                _x_17347 = _x_17343 == 0
                _x_17348 = True
                if _x_17347:
                    _x_17360 = n_564 // d_565
                    _x_17361 = [d_565] + acc_566
                    _x_17362 = algorithms_prime_factors_go(_x_17360, d_565, _x_17361, fuel__569)
                    return _x_17362
                else:
                    _x_17354 = d_565 + 1
                    _x_17355 = algorithms_prime_factors_go(n_564, _x_17354, acc_566, fuel__569)
                    return _x_17355
    _alt_17372 = _f_17371
    if fuel_567 == 0:
        _x_17374 = _alt_17326()
        return _x_17374
    else:
        n_17375 = fuel_567 - 1
        _x_17376 = _alt_17372(n_17375)
        return _x_17376

# Lean: Corpus.Algorithms.isPrime.check
def algorithms_is_prime_check(n_570: int, d_571: int, fuel_572: int) -> bool:
    def _f_17380():
        _x_17379 = True
        return True
    _alt_17381 = _f_17380
    def _f_17415(fuel__574: int):
        _x_17385 = d_571 * d_571
        _x_17386 = n_570 < _x_17385
        if _x_17386:
            _x_17413 = True
            return True
        else:
            _x_17393 = n_570 % d_571
            _x_17394 = 0
            _x_17397 = _x_17393 == 0
            _x_17398 = True
            if _x_17397:
                _x_17410 = False
                return False
            else:
                _x_17404 = 1
                _x_17407 = d_571 + 1
                _x_17408 = algorithms_is_prime_check(n_570, _x_17407, fuel__574)
                return _x_17408
    _alt_17416 = _f_17415
    if fuel_572 == 0:
        _x_17418 = _alt_17381()
        return _x_17418
    else:
        n_17419 = fuel_572 - 1
        _x_17420 = _alt_17416(n_17419)
        return _x_17420

# Lean: Corpus.Algorithms.binarySearch.go
def binary_search_go(arr_575: list[int], target: int, lo: int, hi_576: int, fuel_577: int) -> int | None:
    def _f_17424():
        _x_17423 = None
        return _x_17423
    _alt_17425 = _f_17424
    def _f_17480(fuel__579: int):
        _x_17426 = hi_576 <= lo
        if _x_17426:
            _x_17478 = None
            return _x_17478
        else:
            _x_17437 = hi_576 - lo
            _x_17438 = 2
            _x_17441 = _x_17437 // 2
            _x_17442 = lo + _x_17441
            _alt_17443 = _f_17424
            def _f_17463(v_581: int):
                _x_17446 = v_581 == target
                _x_17447 = True
                if _x_17446:
                    _x_17461 = _x_17442
                    return _x_17461
                else:
                    _x_17450 = v_581 < target
                    if _x_17450:
                        _x_17454 = 1
                        _x_17457 = _x_17442 + 1
                        _x_17458 = binary_search_go(arr_575, target, _x_17457, hi_576, fuel__579)
                        return _x_17458
                    else:
                        _x_17452 = binary_search_go(arr_575, target, lo, _x_17442, fuel__579)
                        return _x_17452
            _alt_17464 = _f_17463
            def _f_17468(xs_582: list[int], i_583: int):
                _x_17466 = len(xs_582)
                _x_17467 = i_583 < _x_17466
                return _x_17467
            _x_17470 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_17471 = _x_17470(arr_575, _x_17442)
            if _x_17471 is None:
                _x_17473 = _alt_17443()
                return _x_17473
            else:
                val_17474 = _x_17471
                _x_17475 = _alt_17464(val_17474)
                return _x_17475
    _alt_17481 = _f_17480
    if fuel_577 == 0:
        _x_17483 = _alt_17425()
        return _x_17483
    else:
        n_17484 = fuel_577 - 1
        _x_17485 = _alt_17481(n_17484)
        return _x_17485

# Lean: Corpus.Algorithms.linearSearch.go
def linear_search_go(target_584: int, xs_585: list[int], idx_586: int) -> int | None:
    def _f_17489():
        _x_17488 = None
        return _x_17488
    _alt_17490 = _f_17489
    def _f_17508(x_588: int, xs__589: list[int]):
        _x_17493 = x_588 == target_584
        _x_17494 = True
        if _x_17493:
            _x_17506 = idx_586
            return _x_17506
        else:
            _x_17500 = 1
            _x_17503 = idx_586 + 1
            _x_17504 = linear_search_go(target_584, xs__589, _x_17503)
            return _x_17504
    _alt_17509 = _f_17508
    if len(xs_585) == 0:
        _x_17511 = _alt_17490()
        return _x_17511
    else:
        head_17512 = xs_585[0]
        tail_17513 = xs_585[1:]
        _x_17514 = _alt_17509(head_17512, tail_17513)
        return _x_17514

# Lean: Corpus.Algorithms.insertionSort.insert
def insertion_sort_insert(x_590: int, sorted_591: list[int]) -> list[int]:
    def _f_17519():
        _x_17517 = []
        _x_17518 = [x_590] + _x_17517
        return _x_17518
    _alt_17520 = _f_17519
    def _f_17529(y_593: int, ys_594: list[int]):
        _x_17521 = x_590 <= y_593
        if _x_17521:
            _x_17526 = [y_593] + ys_594
            _x_17527 = [x_590] + _x_17526
            return _x_17527
        else:
            _x_17523 = insertion_sort_insert(x_590, ys_594)
            _x_17524 = [y_593] + _x_17523
            return _x_17524
    _alt_17530 = _f_17529
    if len(sorted_591) == 0:
        _x_17532 = _alt_17520()
        return _x_17532
    else:
        head_17533 = sorted_591[0]
        tail_17534 = sorted_591[1:]
        _x_17535 = _alt_17530(head_17533, tail_17534)
        return _x_17535

# Lean: Corpus.Algorithms.insertionSort.sort
def insertion_sort_sort(unsorted: list[int], acc_595: list[int]) -> list[int]:
    def _f_17538():
        return acc_595
    _alt_17539 = _f_17538
    def _f_17542(x_597: int, xs_598: list[int]):
        _x_17540 = insertion_sort_insert(x_597, acc_595)
        _x_17541 = insertion_sort_sort(xs_598, _x_17540)
        return _x_17541
    _alt_17543 = _f_17542
    if len(unsorted) == 0:
        _x_17545 = _alt_17539()
        return _x_17545
    else:
        head_17546 = unsorted[0]
        tail_17547 = unsorted[1:]
        _x_17548 = _alt_17543(head_17546, tail_17547)
        return _x_17548

# Lean: Corpus.Algorithms.insertionSort
def insertion_sort(xs_599: list[int]) -> list[int]:
    _x_17551 = []
    _x_17552 = insertion_sort_sort(xs_599, _x_17551)
    return _x_17552

# Lean: Corpus.Algorithms.merge
def algorithms_merge(xs_600: list[int], ys_601: list[int]) -> list[int]:
    def _f_17554(ys_602: list[int]):
        return ys_602
    _alt_17555 = _f_17554
    _alt_17556 = _f_17554
    def _f_17567(x_603: int, xs__604: list[int], y_605: int, ys__606: list[int]):
        _x_17557 = x_603 <= y_605
        if _x_17557:
            _x_17563 = [y_605] + ys__606
            _x_17564 = algorithms_merge(xs__604, _x_17563)
            _x_17565 = [x_603] + _x_17564
            return _x_17565
        else:
            _x_17559 = [x_603] + xs__604
            _x_17560 = algorithms_merge(_x_17559, ys__606)
            _x_17561 = [y_605] + _x_17560
            return _x_17561
    _alt_17568 = _f_17567
    if len(xs_600) == 0:
        if len(ys_601) == 0:
            _x_17569 = []
            _x_17570 = _alt_17555(_x_17569)
            return _x_17570
        else:
            head_17571 = ys_601[0]
            tail_17572 = ys_601[1:]
            _x_17573 = [head_17571] + tail_17572
            _x_17574 = _alt_17555(_x_17573)
            return _x_17574
    else:
        head_17576 = xs_600[0]
        tail_17577 = xs_600[1:]
        if len(ys_601) == 0:
            _x_17578 = [head_17576] + tail_17577
            _x_17579 = _alt_17556(_x_17578)
            return _x_17579
        else:
            head_17580 = ys_601[0]
            tail_17581 = ys_601[1:]
            _x_17582 = _alt_17568(head_17576, tail_17577, head_17580, tail_17581)
            return _x_17582

# Lean: Corpus.Algorithms.split
def algorithms_split(xs_607: list[int]) -> tuple[list[int], list[int]]:
    def _f_17588():
        _x_17586 = []
        _x_17587 = (_x_17586, _x_17586)
        return _x_17587
    _alt_17589 = _f_17588
    def _f_17593(x_609: int):
        _x_17590 = []
        _x_17591 = [x_609] + _x_17590
        _x_17592 = (_x_17591, _x_17590)
        return _x_17592
    _alt_17594 = _f_17593
    def _f_17605(x_610: int, y_611: int, rest_612: list[int]):
        def _f_17598(l_613: list[int], r_614: list[int]):
            _x_17595 = [x_610] + l_613
            _x_17596 = [y_611] + r_614
            _x_17597 = (_x_17595, _x_17596)
            return _x_17597
        _alt_17599 = _f_17598
        _x_17600 = algorithms_split(rest_612)
        match _x_17600:
            case (fst_17601, snd_17602):
                _x_17603 = _alt_17599(fst_17601, snd_17602)
                return _x_17603
    _alt_17606 = _f_17605
    if len(xs_607) == 0:
        _x_17608 = _alt_17589()
        return _x_17608
    else:
        head_17609 = xs_607[0]
        tail_17610 = xs_607[1:]
        if len(tail_17610) == 0:
            _x_17611 = _alt_17594(head_17609)
            return _x_17611
        else:
            head_17612 = tail_17610[0]
            tail_17613 = tail_17610[1:]
            _x_17614 = _alt_17606(head_17609, head_17612, tail_17613)
            return _x_17614

# Lean: Corpus.Algorithms.mergeSort
def merge_sort(xs_615: list[int]) -> list[int]:
    def _f_17619():
        _x_17618 = []
        return _x_17618
    _alt_17620 = _f_17619
    def _f_17623(x_617: int):
        _x_17621 = []
        _x_17622 = [x_617] + _x_17621
        return _x_17622
    _alt_17624 = _f_17623
    def _f_17636(x_17625: list[int]):
        def _f_17629(l_618: list[int], r_619: list[int]):
            _x_17626 = merge_sort(l_618)
            _x_17627 = merge_sort(r_619)
            _x_17628 = algorithms_merge(_x_17626, _x_17627)
            return _x_17628
        _alt_17630 = _f_17629
        _x_17631 = algorithms_split(xs_615)
        match _x_17631:
            case (fst_17632, snd_17633):
                _x_17634 = _alt_17630(fst_17632, snd_17633)
                return _x_17634
    _alt_17637 = _f_17636
    if len(xs_615) == 0:
        _x_17639 = _alt_17620()
        return _x_17639
    else:
        head_17640 = xs_615[0]
        tail_17641 = xs_615[1:]
        if len(tail_17641) == 0:
            _x_17642 = _alt_17624(head_17640)
            return _x_17642
        else:
            head_17643 = tail_17641[0]
            tail_17644 = tail_17641[1:]
            _x_17645 = [head_17643] + tail_17644
            _x_17646 = [head_17640] + _x_17645
            _x_17647 = _alt_17637(_x_17646)
            return _x_17647

# Lean: Corpus.Algorithms.linearSearch
def linear_search(xs_620: list[int], target_621: int) -> int | None:
    _x_17651 = 0
    _x_17654 = linear_search_go(target_621, xs_620, 0)
    return _x_17654

# Lean: Corpus.Algorithms.binarySearch
def binary_search(arr_622: list[int], target_623: int) -> int | None:
    _x_17656 = 0
    _x_17659 = len(arr_622)
    _x_17660 = binary_search_go(arr_622, target_623, 0, _x_17659, _x_17659)
    return _x_17660

# Lean: Corpus.Algorithms.gcd
def algorithms_gcd(a_624: int, b_625: int) -> int:
    _x_17664 = 0
    _x_17667 = b_625 == 0
    _x_17668 = True
    if _x_17667:
        return a_624
    else:
        _x_17674 = a_624 % b_625
        _x_17675 = algorithms_gcd(b_625, _x_17674)
        return _x_17675

# Lean: Corpus.Algorithms.lcm
def algorithms_lcm(a_626: int, b_627: int) -> int:
    def _f_17680():
        _x_17679 = True
        return True
    _alt_17681 = _f_17680
    def _f_17688():
        _x_17684 = 0
        _x_17687 = b_627 == 0
        return _x_17687
    _alt_17689 = _f_17688
    _x_17692 = 0
    _x_17695 = a_626 == 0
    def _jp_17715(_y_17700: bool):
        _x_17701 = True
        if _y_17700:
            return 0
        else:
            _x_17710 = algorithms_gcd(a_626, b_627)
            _x_17711 = a_626 // _x_17710
            _x_17712 = _x_17711 * b_627
            return _x_17712
    def _jp_17718():
        _x_17717 = _alt_17689()
        return _jp_17715(_x_17717)
    def _jp_17721():
        _x_17720 = _alt_17681()
        return _jp_17715(_x_17720)
    if _x_17695:
        return _jp_17721()
    else:
        return _jp_17718()

# Lean: Corpus.Algorithms.isPrime
def algorithms_is_prime(n_630: int) -> bool:
    _x_17723 = 2
    _x_17726 = n_630 < 2
    if _x_17726:
        _x_17730 = False
        return False
    else:
        _x_17728 = algorithms_is_prime_check(n_630, 2, n_630)
        return _x_17728

# Lean: Corpus.Algorithms.primeFactors
def algorithms_prime_factors(n_631: int) -> list[int]:
    _x_17733 = 2
    _x_17736 = []
    _x_17737 = algorithms_prime_factors_go(n_631, 2, _x_17736, n_631)
    return _x_17737

# Lean: Corpus.Algorithms.fibonacci
def algorithms_fibonacci(n_632: int) -> int:
    _x_17739 = 0
    _x_17742 = 1
    _x_17745 = algorithms_fibonacci_go(0, 1, n_632)
    return _x_17745

# Lean: Corpus.Algorithms.power
def power(base_633: int, exp_634: int) -> int:
    _x_17747 = 1
    _x_17750 = power_go(base_633, exp_634, 1)
    return _x_17750

# Lean: Corpus.Algorithms.reverse
def algorithms_reverse(__635: Any, xs_636: list[Any]) -> list[Any]:
    _x_17752 = []
    _x_17753 = algorithms_reverse_go(None, xs_636, _x_17752)
    return _x_17753

# Lean: Corpus.Algorithms.take
def algorithms_take(__637: Any, n_638: int, xs_639: list[Any]) -> list[Any]:
    def _f_17757(x_17755: list[Any]):
        _x_17756 = []
        return _x_17756
    _alt_17758 = _f_17757
    def _f_17761(x_17759: int):
        _x_17760 = []
        return _x_17760
    _alt_17762 = _f_17761
    def _f_17765(n__640: int, x_641: Any, xs__642: list[Any]):
        _x_17763 = algorithms_take(None, n__640, xs__642)
        _x_17764 = [x_641] + _x_17763
        return _x_17764
    _alt_17766 = _f_17765
    if n_638 == 0:
        if len(xs_639) == 0:
            _x_17767 = []
            _x_17768 = _alt_17758(_x_17767)
            return _x_17768
        else:
            head_17769 = xs_639[0]
            tail_17770 = xs_639[1:]
            _x_17771 = [head_17769] + tail_17770
            _x_17772 = _alt_17758(_x_17771)
            return _x_17772
    else:
        n_17774 = n_638 - 1
        if len(xs_639) == 0:
            _x_17775 = n_17774 + 1
            _x_17776 = _alt_17762(_x_17775)
            return _x_17776
        else:
            head_17777 = xs_639[0]
            tail_17778 = xs_639[1:]
            _x_17779 = _alt_17766(n_17774, head_17777, tail_17778)
            return _x_17779

# Lean: Corpus.Algorithms.drop
def algorithms_drop(__643: Any, n_644: int, xs_645: list[Any]) -> list[Any]:
    def _f_17783(xs_646: list[Any]):
        return xs_646
    _alt_17784 = _f_17783
    def _f_17787(x_17785: int):
        _x_17786 = []
        return _x_17786
    _alt_17788 = _f_17787
    def _f_17791(n__647: int, head_17789: Any, xs__648: list[Any]):
        _x_17790 = algorithms_drop(None, n__647, xs__648)
        return _x_17790
    _alt_17792 = _f_17791
    if n_644 == 0:
        if len(xs_645) == 0:
            _x_17793 = []
            _x_17794 = _alt_17784(_x_17793)
            return _x_17794
        else:
            head_17795 = xs_645[0]
            tail_17796 = xs_645[1:]
            _x_17797 = [head_17795] + tail_17796
            _x_17798 = _alt_17784(_x_17797)
            return _x_17798
    else:
        n_17800 = n_644 - 1
        if len(xs_645) == 0:
            _x_17801 = n_17800 + 1
            _x_17802 = _alt_17788(_x_17801)
            return _x_17802
        else:
            head_17803 = xs_645[0]
            tail_17804 = xs_645[1:]
            _x_17805 = _alt_17792(n_17800, head_17803, tail_17804)
            return _x_17805

# Lean: Corpus.Algorithms.filter
def algorithms_filter(__649: Any, p_650: Callable[[Any], bool], xs_651: list[Any]) -> list[Any]:
    def _f_17810():
        _x_17809 = []
        return _x_17809
    _alt_17811 = _f_17810
    def _f_17821(x_653: Any, xs__654: list[Any]):
        _x_17812 = p_650(x_653)
        _x_17813 = True
        if _x_17812:
            _x_17818 = algorithms_filter(None, p_650, xs__654)
            _x_17819 = [x_653] + _x_17818
            return _x_17819
        else:
            _x_17816 = algorithms_filter(None, p_650, xs__654)
            return _x_17816
    _alt_17822 = _f_17821
    if len(xs_651) == 0:
        _x_17824 = _alt_17811()
        return _x_17824
    else:
        head_17825 = xs_651[0]
        tail_17826 = xs_651[1:]
        _x_17827 = _alt_17822(head_17825, tail_17826)
        return _x_17827

# Lean: Corpus.Algorithms.map
def algorithms_map(__655: Any, __656: Any, f: Callable[[Any], Any], xs_657: list[Any]) -> list[Any]:
    def _f_17831():
        _x_17830 = []
        return _x_17830
    _alt_17832 = _f_17831
    def _f_17836(x_659: Any, xs__660: list[Any]):
        _x_17833 = f(x_659)
        _x_17834 = algorithms_map(None, None, f, xs__660)
        _x_17835 = [_x_17833] + _x_17834
        return _x_17835
    _alt_17837 = _f_17836
    if len(xs_657) == 0:
        _x_17839 = _alt_17832()
        return _x_17839
    else:
        head_17840 = xs_657[0]
        tail_17841 = xs_657[1:]
        _x_17842 = _alt_17837(head_17840, tail_17841)
        return _x_17842

# Lean: Corpus.Algorithms.foldl
def algorithms_foldl(__661: Any, __662: Any, f_663: Callable[[Any, Any], Any], init: Any, xs_664: list[Any]) -> Any:
    def _f_17845():
        return init
    _alt_17846 = _f_17845
    def _f_17849(x_666: Any, xs__667: list[Any]):
        _x_17847 = f_663(init, x_666)
        _x_17848 = algorithms_foldl(None, None, f_663, _x_17847, xs__667)
        return _x_17848
    _alt_17850 = _f_17849
    if len(xs_664) == 0:
        _x_17852 = _alt_17846()
        return _x_17852
    else:
        head_17853 = xs_664[0]
        tail_17854 = xs_664[1:]
        _x_17855 = _alt_17850(head_17853, tail_17854)
        return _x_17855

# Lean: Corpus.Algorithms.foldr
def algorithms_foldr(__668: Any, __669: Any, f_670: Callable[[Any, Any], Any], init_671: Any, xs_672: list[Any]) -> Any:
    def _f_17858():
        return init_671
    _alt_17859 = _f_17858
    def _f_17862(x_674: Any, xs__675: list[Any]):
        _x_17860 = algorithms_foldr(None, None, f_670, init_671, xs__675)
        _x_17861 = f_670(x_674, _x_17860)
        return _x_17861
    _alt_17863 = _f_17862
    if len(xs_672) == 0:
        _x_17865 = _alt_17859()
        return _x_17865
    else:
        head_17866 = xs_672[0]
        tail_17867 = xs_672[1:]
        _x_17868 = _alt_17863(head_17866, tail_17867)
        return _x_17868

# Lean: Corpus.Algorithms.zip
def algorithms_zip(__676: Any, __677: Any, xs_678: list[Any], ys_679: list[Any]) -> list[tuple[Any, Any]]:
    def _f_17873(x_17871: list[Any]):
        _x_17872 = []
        return _x_17872
    _alt_17874 = _f_17873
    def _f_17877(x_17875: list[Any]):
        _x_17876 = []
        return _x_17876
    _alt_17878 = _f_17877
    def _f_17882(x_680: Any, xs__681: list[Any], y_682: Any, ys__683: list[Any]):
        _x_17879 = (x_680, y_682)
        _x_17880 = algorithms_zip(None, None, xs__681, ys__683)
        _x_17881 = [_x_17879] + _x_17880
        return _x_17881
    _alt_17883 = _f_17882
    if len(xs_678) == 0:
        if len(ys_679) == 0:
            _x_17884 = []
            _x_17885 = _alt_17874(_x_17884)
            return _x_17885
        else:
            head_17886 = ys_679[0]
            tail_17887 = ys_679[1:]
            _x_17888 = [head_17886] + tail_17887
            _x_17889 = _alt_17874(_x_17888)
            return _x_17889
    else:
        head_17891 = xs_678[0]
        tail_17892 = xs_678[1:]
        if len(ys_679) == 0:
            _x_17893 = [head_17891] + tail_17892
            _x_17894 = _alt_17878(_x_17893)
            return _x_17894
        else:
            head_17895 = ys_679[0]
            tail_17896 = ys_679[1:]
            _x_17897 = _alt_17883(head_17891, tail_17892, head_17895, tail_17896)
            return _x_17897

# Lean: Corpus.Algorithms.unzip
def unzip(__684: Any, __685: Any, xys: list[tuple[Any, Any]]) -> tuple[list[Any], list[Any]]:
    def _f_17904():
        _x_17901 = []
        _x_17902 = []
        _x_17903 = (_x_17901, _x_17902)
        return _x_17903
    _alt_17905 = _f_17904
    def _f_17916(x_687: Any, y_688: Any, rest_689: list[tuple[Any, Any]]):
        def _f_17909(xs_690: list[Any], ys_691: list[Any]):
            _x_17906 = [x_687] + xs_690
            _x_17907 = [y_688] + ys_691
            _x_17908 = (_x_17906, _x_17907)
            return _x_17908
        _alt_17910 = _f_17909
        _x_17911 = unzip(None, None, rest_689)
        match _x_17911:
            case (fst_17912, snd_17913):
                _x_17914 = _alt_17910(fst_17912, snd_17913)
                return _x_17914
    _alt_17917 = _f_17916
    if len(xys) == 0:
        _x_17919 = _alt_17905()
        return _x_17919
    else:
        head_17920 = xys[0]
        tail_17921 = xys[1:]
        match head_17920:
            case (fst_17922, snd_17923):
                _x_17924 = _alt_17917(fst_17922, snd_17923, tail_17921)
                return _x_17924

# Lean: Corpus.Algorithms.concat
def algorithms_concat(__692: Any, xss: list[list[Any]]) -> list[Any]:
    def _f_17929():
        _x_17928 = []
        return _x_17928
    _alt_17930 = _f_17929
    def _f_17936(xs_694: list[Any], xss_: list[list[Any]]):
        _x_17934 = algorithms_concat(None, xss_)
        _x_17935 = xs_694 + _x_17934
        return _x_17935
    _alt_17937 = _f_17936
    if len(xss) == 0:
        _x_17939 = _alt_17930()
        return _x_17939
    else:
        head_17940 = xss[0]
        tail_17941 = xss[1:]
        _x_17942 = _alt_17937(head_17940, tail_17941)
        return _x_17942

# Lean: Corpus.Algorithms.intersperse
def intersperse(__695: Any, sep_696: Any, xs_697: list[Any]) -> list[Any]:
    def _f_17946():
        _x_17945 = []
        return _x_17945
    _alt_17947 = _f_17946
    def _f_17950(x_699: Any):
        _x_17948 = []
        _x_17949 = [x_699] + _x_17948
        return _x_17949
    _alt_17951 = _f_17950
    def _f_17955(x_700: Any, xs__701: list[Any]):
        _x_17952 = intersperse(None, sep_696, xs__701)
        _x_17953 = [sep_696] + _x_17952
        _x_17954 = [x_700] + _x_17953
        return _x_17954
    _alt_17956 = _f_17955
    if len(xs_697) == 0:
        _x_17958 = _alt_17947()
        return _x_17958
    else:
        head_17959 = xs_697[0]
        tail_17960 = xs_697[1:]
        if len(tail_17960) == 0:
            _x_17961 = _alt_17951(head_17959)
            return _x_17961
        else:
            head_17962 = tail_17960[0]
            tail_17963 = tail_17960[1:]
            _x_17964 = [head_17962] + tail_17963
            _x_17965 = _alt_17956(head_17959, _x_17964)
            return _x_17965

# Lean: Corpus.Algorithms.span
def span(__702: Any, p_703: Callable[[Any], bool], xs_704: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_17971():
        _x_17969 = []
        _x_17970 = (_x_17969, _x_17969)
        return _x_17970
    _alt_17972 = _f_17971
    def _f_17990(x_706: Any, xs__707: list[Any]):
        _x_17973 = p_703(x_706)
        _x_17974 = True
        if _x_17973:
            def _f_17982(ys_708: list[Any], zs: list[Any]):
                _x_17980 = [x_706] + ys_708
                _x_17981 = (_x_17980, zs)
                return _x_17981
            _alt_17983 = _f_17982
            _x_17984 = span(None, p_703, xs__707)
            match _x_17984:
                case (fst_17985, snd_17986):
                    _x_17987 = _alt_17983(fst_17985, snd_17986)
                    return _x_17987
        else:
            _x_17977 = []
            _x_17978 = (_x_17977, xs_704)
            return _x_17978
    _alt_17991 = _f_17990
    if len(xs_704) == 0:
        _x_17993 = _alt_17972()
        return _x_17993
    else:
        head_17994 = xs_704[0]
        tail_17995 = xs_704[1:]
        _x_17996 = _alt_17991(head_17994, tail_17995)
        return _x_17996

# Lean: Corpus.Algorithms.partition
def partition(__709: Any, p_710: Callable[[Any], bool], xs_711: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_18001():
        _x_17999 = []
        _x_18000 = (_x_17999, _x_17999)
        return _x_18000
    _alt_18002 = _f_18001
    def _f_18020(x_713: Any, xs__714: list[Any]):
        def _f_18013(yes: list[Any], no: list[Any]):
            _x_18003 = p_710(x_713)
            _x_18004 = True
            if _x_18003:
                _x_18010 = [x_713] + yes
                _x_18011 = (_x_18010, no)
                return _x_18011
            else:
                _x_18007 = [x_713] + no
                _x_18008 = (yes, _x_18007)
                return _x_18008
        _alt_18014 = _f_18013
        _x_18015 = partition(None, p_710, xs__714)
        match _x_18015:
            case (fst_18016, snd_18017):
                _x_18018 = _alt_18014(fst_18016, snd_18017)
                return _x_18018
    _alt_18021 = _f_18020
    if len(xs_711) == 0:
        _x_18023 = _alt_18002()
        return _x_18023
    else:
        head_18024 = xs_711[0]
        tail_18025 = xs_711[1:]
        _x_18026 = _alt_18021(head_18024, tail_18025)
        return _x_18026

# Lean: Corpus.Algorithms.groupBy
def group_by(__715: Any, eq: Callable[[Any, Any], bool], xs_716: list[Any]) -> list[list[Any]]:
    def _f_18030():
        _x_18029 = []
        return _x_18029
    _alt_18031 = _f_18030
    def _f_18043(x_718: Any, xs__719: list[Any]):
        def _f_18035(same: list[Any], rest_720: list[Any]):
            _x_18032 = [x_718] + same
            _x_18033 = group_by(None, eq, rest_720)
            _x_18034 = [_x_18032] + _x_18033
            return _x_18034
        _alt_18036 = _f_18035
        _x_18037 = eq(x_718)
        _x_18038 = span(None, _x_18037, xs__719)
        match _x_18038:
            case (fst_18039, snd_18040):
                _x_18041 = _alt_18036(fst_18039, snd_18040)
                return _x_18041
    _alt_18044 = _f_18043
    if len(xs_716) == 0:
        _x_18046 = _alt_18031()
        return _x_18046
    else:
        head_18047 = xs_716[0]
        tail_18048 = xs_716[1:]
        _x_18049 = _alt_18044(head_18047, tail_18048)
        return _x_18049

# Lean: Corpus.Algorithms.isPalindrome
def algorithms_is_palindrome(s_721: str) -> bool:
    _x_18052 = list(s_721)
    _x_18057 = list(reversed(_x_18052))
    _x_18058 = _x_18052 == _x_18057
    return _x_18058

# Lean: Corpus.Algorithms.countChar
def algorithms_count_char(c_723: str, s_724: str) -> int:
    def _f_18076(acc_725: int, x_726: str):
        _x_18063 = x_726 == c_723
        _x_18064 = True
        if _x_18063:
            _x_18071 = 1
            _x_18074 = acc_725 + 1
            return _x_18074
        else:
            return acc_725
    _x_18077 = 0
    _x_18080 = list(s_724)
    _x_18081 = functools.reduce(_f_18076, _x_18080, 0)
    return _x_18081

# Lean: Corpus.Algorithms.replaceChar
def replace_char(old: str, new: str, s_727: str) -> str:
    def _f_18092(c_728: str):
        _x_18086 = c_728 == old
        _x_18087 = True
        if _x_18086:
            return new
        else:
            return c_728
    _x_18093 = list(s_727)
    _x_18094 = [_f_18092(x) for x in _x_18093]
    _x_18095 = ''.join(_x_18094)
    return _x_18095

# Lean: Corpus.Math.abs
def math_abs(x_729: int) -> int:
    _x_18097 = 0
    _x_18100 = x_729 < 0
    if _x_18100:
        _x_18105 = -x_729
        return _x_18105
    else:
        return x_729

# Lean: Corpus.Math.sign
def sign(x_730: int) -> int:
    _x_18108 = 0
    _x_18111 = x_730 < 0
    if _x_18111:
        _x_18123 = 1
        _x_18126 = -1
        return _x_18126
    else:
        _x_18113 = 0 < x_730
        if _x_18113:
            _x_18116 = 1
            return 1
        else:
            return 0

# Lean: Corpus.Math.min
def math_min(a_731: int, b_732: int) -> int:
    _x_18129 = a_731 <= b_732
    if _x_18129:
        return a_731
    else:
        return b_732

# Lean: Corpus.Math.max
def math_max(a_733: int, b_734: int) -> int:
    _x_18134 = b_734 <= a_733
    if _x_18134:
        return a_733
    else:
        return b_734

# Lean: Corpus.Math.clamp
def clamp(lo_735: int, hi_736: int, x_737: int) -> int:
    _x_18139 = math_max(lo_735, x_737)
    _x_18140 = math_min(hi_736, _x_18139)
    return _x_18140

# Lean: Corpus.Math.divMod
def div_mod(a_738: int, b_739: int) -> tuple[int, int]:
    _x_18145 = a_738 // b_739
    _x_18149 = a_738 % b_739
    _x_18150 = (_x_18145, _x_18149)
    return _x_18150

# Lean: Corpus.Math.pow
def pow(base_740: int, exp_741: int) -> int:
    def _f_18155():
        _x_18152 = 1
        return 1
    _alt_18156 = _f_18155
    def _f_18162(n_743: int):
        _x_18160 = pow(base_740, n_743)
        _x_18161 = base_740 * _x_18160
        return _x_18161
    _alt_18163 = _f_18162
    if exp_741 == 0:
        _x_18165 = _alt_18156()
        return _x_18165
    else:
        n_18166 = exp_741 - 1
        _x_18167 = _alt_18163(n_18166)
        return _x_18167

# Lean: Corpus.Math.fastPow
def fast_pow(base_744: int, exp_745: int) -> int:
    _x_18170 = 1
    _x_18173 = fast_pow_go(base_744, exp_745, 1)
    return _x_18173

# Lean: Corpus.Math.modPow
def mod_pow(base_746: int, exp_747: int, m_748: int) -> int:
    _x_18178 = base_746 % m_748
    _x_18179 = 1
    _x_18182 = mod_pow_go(m_748, _x_18178, exp_747, 1)
    return _x_18182

# Lean: Corpus.Math.gcd
def math_gcd(a_749: int, b_750: int) -> int:
    _x_18186 = 0
    _x_18189 = b_750 == 0
    _x_18190 = True
    if _x_18189:
        return a_749
    else:
        _x_18196 = a_749 % b_750
        _x_18197 = math_gcd(b_750, _x_18196)
        return _x_18197

# Lean: Corpus.Math.lcm
def math_lcm(a_751: int, b_752: int) -> int:
    def _f_18202():
        _x_18201 = True
        return True
    _alt_18203 = _f_18202
    def _f_18210():
        _x_18206 = 0
        _x_18209 = b_752 == 0
        return _x_18209
    _alt_18211 = _f_18210
    _x_18214 = 0
    _x_18217 = a_751 == 0
    def _jp_18237(_y_18222: bool):
        _x_18223 = True
        if _y_18222:
            return 0
        else:
            _x_18232 = math_gcd(a_751, b_752)
            _x_18233 = a_751 // _x_18232
            _x_18234 = _x_18233 * b_752
            return _x_18234
    def _jp_18243():
        _x_18242 = _alt_18203()
        return _jp_18237(_x_18242)
    def _jp_18240():
        _x_18239 = _alt_18211()
        return _jp_18237(_x_18239)
    if _x_18217:
        return _jp_18243()
    else:
        return _jp_18240()

# Lean: Corpus.Math.coprime
def coprime(a_755: int, b_756: int) -> bool:
    _x_18247 = math_gcd(a_755, b_756)
    _x_18248 = 1
    _x_18251 = _x_18247 == 1
    return _x_18251

# Lean: Corpus.Math.isPrime
def math_is_prime(n_757: int) -> bool:
    _x_18253 = 2
    _x_18256 = n_757 < 2
    if _x_18256:
        _x_18260 = False
        return False
    else:
        _x_18258 = math_is_prime_check(n_757, 2, n_757)
        return _x_18258

# Lean: Corpus.Math.primeFactors
def math_prime_factors(n_758: int) -> list[int]:
    _x_18263 = 2
    _x_18266 = []
    _x_18267 = math_prime_factors_go(n_758, 2, _x_18266, n_758)
    return _x_18267

# Lean: Corpus.Math.divisors
def divisors(n_759: int) -> list[int]:
    _x_18269 = 1
    _x_18272 = []
    _x_18273 = divisors_go(n_759, 1, _x_18272)
    _x_18274 = list(reversed(_x_18273))
    return _x_18274

# Lean: Corpus.Math.numDivisors
def num_divisors(n_760: int) -> int:
    _x_18276 = divisors(n_760)
    _x_18277 = len(_x_18276)
    return _x_18277

# Lean: Corpus.Math.sumDivisors
def sum_divisors(n_761: int) -> int:
    def _f_18285(x1_18279: int, x2_18280: int):
        _x_18284 = x1_18279 + x2_18280
        return _x_18284
    _x_18286 = 0
    _x_18289 = divisors(n_761)
    _x_18290 = functools.reduce(_f_18285, _x_18289, 0)
    return _x_18290

# Lean: Corpus.Math.fibonacci
def math_fibonacci(n_762: int) -> int:
    _x_18292 = 0
    _x_18295 = 1
    _x_18298 = math_fibonacci_go(0, 1, n_762)
    return _x_18298

# Lean: Corpus.Math.lucas
def lucas(n_763: int) -> int:
    _x_18300 = 2
    _x_18303 = 1
    _x_18306 = lucas_go(2, 1, n_763)
    return _x_18306

# Lean: Corpus.Math.tribonacci
def tribonacci(n_764: int) -> int:
    _x_18308 = 0
    _x_18311 = 1
    _x_18314 = tribonacci_go(0, 0, 1, n_764)
    return _x_18314

# Lean: Corpus.Math.factorial
def factorial(n_765: int) -> int:
    def _f_18319():
        _x_18316 = 1
        return 1
    _alt_18320 = _f_18319
    def _f_18333(n__767: int):
        _x_18327 = 1
        _x_18330 = n__767 + 1
        _x_18331 = factorial(n__767)
        _x_18332 = _x_18330 * _x_18331
        return _x_18332
    _alt_18334 = _f_18333
    if n_765 == 0:
        _x_18336 = _alt_18320()
        return _x_18336
    else:
        n_18337 = n_765 - 1
        _x_18338 = _alt_18334(n_18337)
        return _x_18338

# Lean: Corpus.Math.binomial
def binomial(n_768: int, k_769: int) -> int:
    _x_18341 = n_768 < k_769
    if _x_18341:
        _x_18348 = 0
        return 0
    else:
        _x_18343 = 1
        _x_18346 = binomial_go(n_768, k_769, 1, 1, 1)
        return _x_18346

# Lean: Corpus.Math.catalan
def catalan(n_770: int) -> int:
    _x_18359 = 2
    _x_18362 = 2 * n_770
    _x_18363 = binomial(_x_18362, n_770)
    _x_18367 = 1
    _x_18370 = n_770 + 1
    _x_18371 = _x_18363 // _x_18370
    return _x_18371

# Lean: Corpus.Math.permutations
def permutations(n_771: int, k_772: int) -> int:
    _x_18373 = n_771 < k_772
    if _x_18373:
        _x_18386 = 0
        return 0
    else:
        _x_18378 = factorial(n_771)
        _x_18382 = n_771 - k_772
        _x_18383 = factorial(_x_18382)
        _x_18384 = _x_18378 // _x_18383
        return _x_18384

# Lean: Corpus.Math.triangularNumber
def triangular_number(n_773: int) -> int:
    _x_18400 = 1
    _x_18403 = n_773 + 1
    _x_18404 = n_773 * _x_18403
    _x_18405 = 2
    _x_18408 = _x_18404 // 2
    return _x_18408

# Lean: Corpus.Math.squareNumber
def square_number(n_774: int) -> int:
    _x_18413 = n_774 * n_774
    return _x_18413

# Lean: Corpus.Math.pentagonalNumber
def pentagonal_number(n_775: int) -> int:
    _x_18424 = 3
    _x_18427 = 3 * n_775
    _x_18428 = 1
    _x_18431 = _x_18427 - 1
    _x_18432 = n_775 * _x_18431
    _x_18433 = 2
    _x_18436 = _x_18432 // 2
    return _x_18436

# Lean: Corpus.Math.hexagonalNumber
def hexagonal_number(n_776: int) -> int:
    _x_18444 = 2
    _x_18447 = 2 * n_776
    _x_18448 = 1
    _x_18451 = _x_18447 - 1
    _x_18452 = n_776 * _x_18451
    return _x_18452

# Lean: Corpus.Math.isTriangular
def is_triangular(n_777: int) -> bool:
    _x_18466 = 8
    _x_18469 = 8 * n_777
    _x_18470 = 1
    _x_18473 = _x_18469 + 1
    _x_18474 = isqrt(_x_18473)
    _x_18475 = _x_18474 - 1
    _x_18476 = 2
    _x_18479 = _x_18475 // 2
    _x_18482 = _x_18479 + 1
    _x_18483 = _x_18479 * _x_18482
    _x_18484 = _x_18483 // 2
    _x_18485 = _x_18484 == n_777
    return _x_18485

# Lean: Corpus.Math.isSquare
def is_square(n_779: int) -> bool:
    _x_18487 = isqrt(n_779)
    _x_18493 = _x_18487 * _x_18487
    _x_18494 = _x_18493 == n_779
    return _x_18494

# Lean: Corpus.Math.isqrt
def isqrt(n_781: int) -> int:
    _x_18498 = 0
    _x_18501 = n_781 == 0
    _x_18502 = True
    if _x_18501:
        return 0
    else:
        _x_18505 = isqrt_go(n_781, n_781, n_781)
        return _x_18505

# Lean: Corpus.Math.digits
def digits(n_782: int, base_783: int) -> list[int]:
    _x_18509 = 2
    _x_18512 = base_783 < 2
    if _x_18512:
        _x_18517 = []
        return _x_18517
    else:
        _x_18514 = []
        _x_18515 = digits_go(base_783, n_782, _x_18514)
        return _x_18515

# Lean: Corpus.Math.fromDigits
def from_digits(ds: list[int], base_784: int) -> int:
    def _f_18528(acc_785: int, d_786: int):
        _x_18526 = acc_785 * base_784
        _x_18527 = _x_18526 + d_786
        return _x_18527
    _x_18529 = 0
    _x_18532 = functools.reduce(_f_18528, ds, 0)
    return _x_18532

# Lean: Corpus.Math.numDigits
def num_digits(n_787: int, base_788: int) -> int:
    _x_18534 = digits(n_787, base_788)
    _x_18535 = len(_x_18534)
    return _x_18535

# Lean: Corpus.Math.numDigits10
def num_digits10(n_789: int) -> int:
    _x_18537 = 10
    _x_18540 = num_digits(n_789, 10)
    return _x_18540

# Lean: Corpus.Math.digitSum
def digit_sum(n_790: int, base_791: int) -> int:
    def _f_18548(x1_18542: int, x2_18543: int):
        _x_18547 = x1_18542 + x2_18543
        return _x_18547
    _x_18549 = 0
    _x_18552 = digits(n_790, base_791)
    _x_18553 = functools.reduce(_f_18548, _x_18552, 0)
    return _x_18553

# Lean: Corpus.Math.digitSum10
def digit_sum10(n_792: int) -> int:
    _x_18555 = 10
    _x_18558 = digit_sum(n_792, 10)
    return _x_18558

# Lean: Corpus.Math.digitalRoot
def digital_root(n_793: int) -> int:
    _x_18560 = 100
    _x_18563 = digital_root_go(n_793, 100)
    return _x_18563

# Lean: Corpus.Math.reverseDigits
def reverse_digits(n_794: int) -> int:
    _x_18565 = 10
    _x_18568 = digits(n_794, 10)
    _x_18569 = list(reversed(_x_18568))
    _x_18570 = from_digits(_x_18569, 10)
    return _x_18570

# Lean: Corpus.Math.isPalindromeNum
def is_palindrome_num(n_795: int) -> bool:
    _x_18574 = reverse_digits(n_795)
    _x_18575 = n_795 == _x_18574
    return _x_18575

# Lean: Corpus.Math.isEven
def is_even(n_796: int) -> bool:
    _x_18582 = 2
    _x_18585 = n_796 % 2
    _x_18586 = 0
    _x_18589 = _x_18585 == 0
    return _x_18589

# Lean: Corpus.Math.isOdd
def is_odd(n_797: int) -> bool:
    _x_18596 = 2
    _x_18599 = n_797 % 2
    _x_18600 = 1
    _x_18603 = _x_18599 == 1
    return _x_18603

# Lean: Corpus.Functional.id
def functional_id(__798: Any, x_799: Any) -> Any:
    return x_799

# Lean: Corpus.Functional.const
def functional_const(__800: Any, __801: Any, x_802: Any, y_803: Any) -> Any:
    return x_802

# Lean: Corpus.Functional.flip
def functional_flip(__804: Any, __805: Any, __806: Any, f_807: Callable[[Any, Any], Any], y_808: Any, x_809: Any) -> Any:
    _x_18607 = f_807(x_809, y_808)
    return _x_18607

# Lean: Corpus.Functional.compose
def functional_compose(__810: Any, __811: Any, __812: Any, f_813: Callable[[Any], Any], g_814: Callable[[Any], Any], x_815: Any) -> Any:
    _x_18609 = g_814(x_815)
    _x_18610 = f_813(_x_18609)
    return _x_18610

# Lean: Corpus.Functional.pipe
def pipe(__816: Any, __817: Any, x_818: Any, f_819: Callable[[Any], Any]) -> Any:
    _x_18612 = f_819(x_818)
    return _x_18612

# Lean: Corpus.Functional.apply
def functional_apply(__820: Any, __821: Any, f_822: Callable[[Any], Any], x_823: Any) -> Any:
    _x_18614 = f_822(x_823)
    return _x_18614

# Lean: Corpus.Functional.curry
def curry(__824: Any, __825: Any, __826: Any, f_827: Callable[[tuple[Any, Any]], Any], x_828: Any, y_829: Any) -> Any:
    _x_18616 = (x_828, y_829)
    _x_18617 = f_827(_x_18616)
    return _x_18617

# Lean: Corpus.Functional.uncurry
def uncurry(__830: Any, __831: Any, __832: Any, f_833: Callable[[Any, Any], Any], p_834: tuple[Any, Any]) -> Any:
    _x_18619 = p_834[0]
    _x_18620 = p_834[1]
    _x_18621 = f_833(_x_18619, _x_18620)
    return _x_18621

# Lean: Corpus.Functional.Option.map
def option_map(__835: Any, __836: Any, f_837: Callable[[Any], Any], x_18623: Any | None) -> Any | None:
    def _f_18625():
        _x_18624 = None
        return _x_18624
    _alt_18626 = _f_18625
    def _f_18629(x_839: Any):
        _x_18627 = f_837(x_839)
        _x_18628 = _x_18627
        return _x_18628
    _alt_18630 = _f_18629
    if x_18623 is None:
        _x_18632 = _alt_18626()
        return _x_18632
    else:
        val_18633 = x_18623
        _x_18634 = _alt_18630(val_18633)
        return _x_18634

# Lean: Corpus.Functional.Option.bind
def option_bind(__840: Any, __841: Any, x_842: Any | None, f_843: Callable[[Any], Any | None]) -> Any | None:
    def _f_18638():
        _x_18637 = None
        return _x_18637
    _alt_18639 = _f_18638
    def _f_18641(a_845: Any):
        _x_18640 = f_843(a_845)
        return _x_18640
    _alt_18642 = _f_18641
    if x_842 is None:
        _x_18644 = _alt_18639()
        return _x_18644
    else:
        val_18645 = x_842
        _x_18646 = _alt_18642(val_18645)
        return _x_18646

# Lean: Corpus.Functional.Option.filter
def option_filter(__846: Any, p_847: Callable[[Any], bool], x_18649: Any | None) -> Any | None:
    def _f_18651():
        _x_18650 = None
        return _x_18650
    _alt_18652 = _f_18651
    def _f_18661(x_849: Any):
        _x_18653 = p_847(x_849)
        _x_18654 = True
        if _x_18653:
            _x_18659 = x_849
            return _x_18659
        else:
            _x_18657 = None
            return _x_18657
    _alt_18662 = _f_18661
    if x_18649 is None:
        _x_18664 = _alt_18652()
        return _x_18664
    else:
        val_18665 = x_18649
        _x_18666 = _alt_18662(val_18665)
        return _x_18666

# Lean: Corpus.Functional.Option.getOrElse
def get_or_else(__850: Any, x_851: Any | None, default: Any) -> Any:
    def _f_18669():
        return default
    _alt_18670 = _f_18669
    def _f_18671(a_853: Any):
        return a_853
    _alt_18672 = _f_18671
    if x_851 is None:
        _x_18674 = _alt_18670()
        return _x_18674
    else:
        val_18675 = x_851
        _x_18676 = _alt_18672(val_18675)
        return _x_18676

# Lean: Corpus.Functional.Option.orElse
def or_else(__854: Any, x_855: Any | None, y_856: Any | None) -> Any | None:
    def _f_18680(a_857: Any):
        _x_18679 = a_857
        return _x_18679
    _alt_18681 = _f_18680
    def _f_18682():
        return y_856
    _alt_18683 = _f_18682
    if x_855 is None:
        _x_18685 = _alt_18683()
        return _x_18685
    else:
        val_18686 = x_855
        _x_18687 = _alt_18681(val_18686)
        return _x_18687

# Lean: Corpus.Functional.Option.zip
def option_zip(__859: Any, __860: Any, x_861: Any | None, y_862: Any | None) -> tuple[Any, Any] | None:
    def _f_18692(a_863: Any, b_864: Any):
        _x_18690 = (a_863, b_864)
        _x_18691 = _x_18690
        return _x_18691
    _alt_18693 = _f_18692
    def _f_18697(x_18694: Any | None, x_18695: Any | None):
        _x_18696 = None
        return _x_18696
    _alt_18698 = _f_18697
    if x_861 is None:
        _x_18699 = None
        _x_18700 = _alt_18698(_x_18699, y_862)
        return _x_18700
    else:
        val_18701 = x_861
        if y_862 is None:
            _x_18702 = val_18701
            _x_18703 = None
            _x_18704 = _alt_18698(_x_18702, _x_18703)
            return _x_18704
        else:
            val_18705 = y_862
            _x_18706 = _alt_18693(val_18701, val_18705)
            return _x_18706

# Lean: Corpus.Functional.List.head?
def head_(__865: Any, xs_866: list[Any]) -> Any | None:
    def _f_18711():
        _x_18710 = None
        return _x_18710
    _alt_18712 = _f_18711
    def _f_18715(x_868: Any, tail_18713: list[Any]):
        _x_18714 = x_868
        return _x_18714
    _alt_18716 = _f_18715
    if len(xs_866) == 0:
        _x_18718 = _alt_18712()
        return _x_18718
    else:
        head_18719 = xs_866[0]
        tail_18720 = xs_866[1:]
        _x_18721 = _alt_18716(head_18719, tail_18720)
        return _x_18721

# Lean: Corpus.Functional.List.tail?
def tail_(__869: Any, xs_870: list[Any]) -> list[Any] | None:
    def _f_18725():
        _x_18724 = None
        return _x_18724
    _alt_18726 = _f_18725
    def _f_18729(head_18727: Any, xs__872: list[Any]):
        _x_18728 = xs__872
        return _x_18728
    _alt_18730 = _f_18729
    if len(xs_870) == 0:
        _x_18732 = _alt_18726()
        return _x_18732
    else:
        head_18733 = xs_870[0]
        tail_18734 = xs_870[1:]
        _x_18735 = _alt_18730(head_18733, tail_18734)
        return _x_18735

# Lean: Corpus.Functional.List.last?
def last_(__873: Any, xs_874: list[Any]) -> Any | None:
    def _f_18739():
        _x_18738 = None
        return _x_18738
    _alt_18740 = _f_18739
    def _f_18742(x_876: Any):
        _x_18741 = x_876
        return _x_18741
    _alt_18743 = _f_18742
    def _f_18746(head_18744: Any, xs__877: list[Any]):
        _x_18745 = last_(None, xs__877)
        return _x_18745
    _alt_18747 = _f_18746
    if len(xs_874) == 0:
        _x_18749 = _alt_18740()
        return _x_18749
    else:
        head_18750 = xs_874[0]
        tail_18751 = xs_874[1:]
        if len(tail_18751) == 0:
            _x_18752 = _alt_18743(head_18750)
            return _x_18752
        else:
            head_18753 = tail_18751[0]
            tail_18754 = tail_18751[1:]
            _x_18755 = [head_18753] + tail_18754
            _x_18756 = _alt_18747(head_18750, _x_18755)
            return _x_18756

# Lean: Corpus.Functional.List.nth
def nth(__878: Any, xs_879: list[Any], n_880: int) -> Any | None:
    def _f_18762(x_18760: int):
        _x_18761 = None
        return _x_18761
    _alt_18763 = _f_18762
    def _f_18766(x_881: Any, tail_18764: list[Any]):
        _x_18765 = x_881
        return _x_18765
    _alt_18767 = _f_18766
    def _f_18770(head_18768: Any, xs__882: list[Any], n__883: int):
        _x_18769 = nth(None, xs__882, n__883)
        return _x_18769
    _alt_18771 = _f_18770
    if len(xs_879) == 0:
        _x_18772 = _alt_18763(n_880)
        return _x_18772
    else:
        head_18773 = xs_879[0]
        tail_18774 = xs_879[1:]
        if n_880 == 0:
            _x_18775 = _alt_18767(head_18773, tail_18774)
            return _x_18775
        else:
            n_18776 = n_880 - 1
            _x_18777 = _alt_18771(head_18773, tail_18774, n_18776)
            return _x_18777

# Lean: Corpus.Functional.List.updateAt
def update_at(__884: Any, xs_885: list[Any], n_886: int, f_887: Callable[[Any], Any]) -> list[Any]:
    def _f_18783(x_18781: int):
        _x_18782 = []
        return _x_18782
    _alt_18784 = _f_18783
    def _f_18787(x_888: Any, xs__889: list[Any]):
        _x_18785 = f_887(x_888)
        _x_18786 = [_x_18785] + xs__889
        return _x_18786
    _alt_18788 = _f_18787
    def _f_18791(x_890: Any, xs__891: list[Any], n__892: int):
        _x_18789 = update_at(None, xs__891, n__892, f_887)
        _x_18790 = [x_890] + _x_18789
        return _x_18790
    _alt_18792 = _f_18791
    if len(xs_885) == 0:
        _x_18793 = _alt_18784(n_886)
        return _x_18793
    else:
        head_18794 = xs_885[0]
        tail_18795 = xs_885[1:]
        if n_886 == 0:
            _x_18796 = _alt_18788(head_18794, tail_18795)
            return _x_18796
        else:
            n_18797 = n_886 - 1
            _x_18798 = _alt_18792(head_18794, tail_18795, n_18797)
            return _x_18798

# Lean: Corpus.Functional.List.insertAt
def insert_at(__893: Any, xs_894: list[Any], n_895: int, x_896: Any) -> list[Any]:
    def _f_18803(xs_897: list[Any]):
        _x_18802 = [x_896] + xs_897
        return _x_18802
    _alt_18804 = _f_18803
    def _f_18808(x_18805: int):
        _x_18806 = []
        _x_18807 = [x_896] + _x_18806
        return _x_18807
    _alt_18809 = _f_18808
    def _f_18812(y_898: Any, ys_899: list[Any], n__900: int):
        _x_18810 = insert_at(None, ys_899, n__900, x_896)
        _x_18811 = [y_898] + _x_18810
        return _x_18811
    _alt_18813 = _f_18812
    if len(xs_894) == 0:
        _x_18814 = 0
        if n_895:
            _x_18818 = _alt_18809(n_895)
            return _x_18818
        else:
            _x_18819 = []
            _x_18820 = _alt_18804(_x_18819)
            return _x_18820
    else:
        head_18822 = xs_894[0]
        tail_18823 = xs_894[1:]
        if n_895 == 0:
            _x_18824 = [head_18822] + tail_18823
            _x_18825 = _alt_18804(_x_18824)
            return _x_18825
        else:
            n_18826 = n_895 - 1
            _x_18827 = _alt_18813(head_18822, tail_18823, n_18826)
            return _x_18827

# Lean: Corpus.Functional.List.removeAt
def remove_at(__901: Any, xs_902: list[Any], n_903: int) -> list[Any]:
    def _f_18833(x_18831: int):
        _x_18832 = []
        return _x_18832
    _alt_18834 = _f_18833
    def _f_18836(head_18835: Any, xs__904: list[Any]):
        return xs__904
    _alt_18837 = _f_18836
    def _f_18840(x_905: Any, xs__906: list[Any], n__907: int):
        _x_18838 = remove_at(None, xs__906, n__907)
        _x_18839 = [x_905] + _x_18838
        return _x_18839
    _alt_18841 = _f_18840
    if len(xs_902) == 0:
        _x_18842 = _alt_18834(n_903)
        return _x_18842
    else:
        head_18843 = xs_902[0]
        tail_18844 = xs_902[1:]
        if n_903 == 0:
            _x_18845 = _alt_18837(head_18843, tail_18844)
            return _x_18845
        else:
            n_18846 = n_903 - 1
            _x_18847 = _alt_18841(head_18843, tail_18844, n_18846)
            return _x_18847

# Lean: Corpus.Functional.List.splitAt
def split_at(__908: Any, n_909: int, xs_910: list[Any]) -> tuple[list[Any], list[Any]]:
    def _f_18853(xs_911: list[Any]):
        _x_18851 = []
        _x_18852 = (_x_18851, xs_911)
        return _x_18852
    _alt_18854 = _f_18853
    def _f_18858(x_18855: int):
        _x_18856 = []
        _x_18857 = (_x_18856, _x_18856)
        return _x_18857
    _alt_18859 = _f_18858
    def _f_18869(n__912: int, x_913: Any, xs__914: list[Any]):
        def _f_18862(l_915: list[Any], r_916: list[Any]):
            _x_18860 = [x_913] + l_915
            _x_18861 = (_x_18860, r_916)
            return _x_18861
        _alt_18863 = _f_18862
        _x_18864 = split_at(None, n__912, xs__914)
        match _x_18864:
            case (fst_18865, snd_18866):
                _x_18867 = _alt_18863(fst_18865, snd_18866)
                return _x_18867
    _alt_18870 = _f_18869
    if n_909 == 0:
        if len(xs_910) == 0:
            _x_18871 = []
            _x_18872 = _alt_18854(_x_18871)
            return _x_18872
        else:
            head_18873 = xs_910[0]
            tail_18874 = xs_910[1:]
            _x_18875 = [head_18873] + tail_18874
            _x_18876 = _alt_18854(_x_18875)
            return _x_18876
    else:
        n_18878 = n_909 - 1
        if len(xs_910) == 0:
            _x_18879 = n_18878 + 1
            _x_18880 = _alt_18859(_x_18879)
            return _x_18880
        else:
            head_18881 = xs_910[0]
            tail_18882 = xs_910[1:]
            _x_18883 = _alt_18870(n_18878, head_18881, tail_18882)
            return _x_18883

# Lean: Corpus.Functional.List.takeWhile
def take_while(__917: Any, p_918: Callable[[Any], bool], xs_919: list[Any]) -> list[Any]:
    def _f_18888():
        _x_18887 = []
        return _x_18887
    _alt_18889 = _f_18888
    def _f_18899(x_921: Any, xs__922: list[Any]):
        _x_18890 = p_918(x_921)
        _x_18891 = True
        if _x_18890:
            _x_18896 = take_while(None, p_918, xs__922)
            _x_18897 = [x_921] + _x_18896
            return _x_18897
        else:
            _x_18894 = []
            return _x_18894
    _alt_18900 = _f_18899
    if len(xs_919) == 0:
        _x_18902 = _alt_18889()
        return _x_18902
    else:
        head_18903 = xs_919[0]
        tail_18904 = xs_919[1:]
        _x_18905 = _alt_18900(head_18903, tail_18904)
        return _x_18905

# Lean: Corpus.Functional.List.dropWhile
def drop_while(__923: Any, p_924: Callable[[Any], bool], xs_925: list[Any]) -> list[Any]:
    def _f_18909():
        _x_18908 = []
        return _x_18908
    _alt_18910 = _f_18909
    def _f_18919(x_927: Any, xs__928: list[Any]):
        _x_18911 = p_924(x_927)
        _x_18912 = True
        if _x_18911:
            _x_18917 = drop_while(None, p_924, xs__928)
            return _x_18917
        else:
            _x_18915 = [x_927] + xs__928
            return _x_18915
    _alt_18920 = _f_18919
    if len(xs_925) == 0:
        _x_18922 = _alt_18910()
        return _x_18922
    else:
        head_18923 = xs_925[0]
        tail_18924 = xs_925[1:]
        _x_18925 = _alt_18920(head_18923, tail_18924)
        return _x_18925

# Lean: Corpus.Functional.List.replicate
def list_replicate(__929: Any, n_930: int, x_931: Any) -> list[Any]:
    def _f_18929():
        _x_18928 = []
        return _x_18928
    _alt_18930 = _f_18929
    def _f_18933(n__933: int):
        _x_18931 = list_replicate(None, n__933, x_931)
        _x_18932 = [x_931] + _x_18931
        return _x_18932
    _alt_18934 = _f_18933
    if n_930 == 0:
        _x_18936 = _alt_18930()
        return _x_18936
    else:
        n_18937 = n_930 - 1
        _x_18938 = _alt_18934(n_18937)
        return _x_18938

# Lean: Corpus.Functional.List.scanl
def scanl(__934: Any, __935: Any, f_936: Callable[[Any, Any], Any], init_937: Any, xs_938: list[Any]) -> list[Any]:
    def _f_18942():
        _x_18941 = []
        return _x_18941
    _alt_18943 = _f_18942
    def _f_18946(x_940: Any, xs__941: list[Any]):
        _x_18944 = f_936(init_937, x_940)
        _x_18945 = scanl(None, None, f_936, _x_18944, xs__941)
        return _x_18945
    _alt_18947 = _f_18946
    def _jp_18955(_y_18953: list[Any]):
        _x_18954 = [init_937] + _y_18953
        return _x_18954
    def _jp_18958():
        _x_18957 = _alt_18943()
        return _jp_18955(_x_18957)
    def _jp_18962(_y_18959: Any, _y_18960: list[Any]):
        _x_18961 = _alt_18947(_y_18959, _y_18960)
        return _jp_18955(_x_18961)
    if len(xs_938) == 0:
        return _jp_18958()
    else:
        head_18950 = xs_938[0]
        tail_18951 = xs_938[1:]
        return _jp_18962(head_18950, tail_18951)

# Lean: Corpus.Functional.List.interleave
def interleave(__942: Any, xs_943: list[Any], ys_944: list[Any]) -> list[Any]:
    def _f_18964(ys_945: list[Any]):
        return ys_945
    _alt_18965 = _f_18964
    _alt_18966 = _f_18964
    def _f_18970(x_946: Any, xs__947: list[Any], y_948: Any, ys__949: list[Any]):
        _x_18967 = interleave(None, xs__947, ys__949)
        _x_18968 = [y_948] + _x_18967
        _x_18969 = [x_946] + _x_18968
        return _x_18969
    _alt_18971 = _f_18970
    if len(xs_943) == 0:
        if len(ys_944) == 0:
            _x_18972 = []
            _x_18973 = _alt_18965(_x_18972)
            return _x_18973
        else:
            head_18974 = ys_944[0]
            tail_18975 = ys_944[1:]
            _x_18976 = [head_18974] + tail_18975
            _x_18977 = _alt_18965(_x_18976)
            return _x_18977
    else:
        head_18979 = xs_943[0]
        tail_18980 = xs_943[1:]
        if len(ys_944) == 0:
            _x_18981 = [head_18979] + tail_18980
            _x_18982 = _alt_18966(_x_18981)
            return _x_18982
        else:
            head_18983 = ys_944[0]
            tail_18984 = ys_944[1:]
            _x_18985 = _alt_18971(head_18979, tail_18980, head_18983, tail_18984)
            return _x_18985

# Lean: Corpus.Functional.Either.map
def either_map(__950: Any, __951: Any, __952: Any, f_953: Callable[[Any], Any], x_18989: Any) -> Any:
    def _f_18991(a_954: Any):
        _x_18990 = left(None, None, a_954)
        return _x_18990
    _alt_18992 = _f_18991
    def _f_18995(b_955: Any):
        _x_18993 = f_953(b_955)
        _x_18994 = right(None, None, _x_18993)
        return _x_18994
    _alt_18996 = _f_18995
    match x_18989:
        case left(a_18997):
            _x_18998 = _alt_18992(a_18997)
            return _x_18998
        case right(a_18999):
            _x_19000 = _alt_18996(a_18999)
            return _x_19000

# Lean: Corpus.Functional.Either.mapLeft
def map_left(__956: Any, __957: Any, __958: Any, f_959: Callable[[Any], Any], x_19003: Any) -> Any:
    def _f_19006(a_960: Any):
        _x_19004 = f_959(a_960)
        _x_19005 = left(None, None, _x_19004)
        return _x_19005
    _alt_19007 = _f_19006
    def _f_19009(b_961: Any):
        _x_19008 = right(None, None, b_961)
        return _x_19008
    _alt_19010 = _f_19009
    match x_19003:
        case left(a_19011):
            _x_19012 = _alt_19007(a_19011)
            return _x_19012
        case right(a_19013):
            _x_19014 = _alt_19010(a_19013)
            return _x_19014

# Lean: Corpus.Functional.Either.bind
def either_bind(__962: Any, __963: Any, __964: Any, x_965: Any, f_966: Callable[[Any], Any]) -> Any:
    def _f_19018(a_967: Any):
        _x_19017 = left(None, None, a_967)
        return _x_19017
    _alt_19019 = _f_19018
    def _f_19021(b_968: Any):
        _x_19020 = f_966(b_968)
        return _x_19020
    _alt_19022 = _f_19021
    match x_965:
        case left(a_19023):
            _x_19024 = _alt_19019(a_19023)
            return _x_19024
        case right(a_19025):
            _x_19026 = _alt_19022(a_19025)
            return _x_19026

# Lean: Corpus.Functional.Either.isLeft
def is_left(__969: Any, __970: Any, x_19029: Any) -> bool:
    def _f_19032(a_19030: Any):
        _x_19031 = True
        return True
    _alt_19033 = _f_19032
    def _f_19036(a_19034: Any):
        _x_19035 = False
        return False
    _alt_19037 = _f_19036
    match x_19029:
        case left(a_19038):
            _x_19039 = _alt_19033(a_19038)
            return _x_19039
        case right(a_19040):
            _x_19041 = _alt_19037(a_19040)
            return _x_19041

# Lean: Corpus.Functional.Either.isRight
def is_right(__971: Any, __972: Any, x_19044: Any) -> bool:
    def _f_19047(a_19045: Any):
        _x_19046 = False
        return False
    _alt_19048 = _f_19047
    def _f_19051(a_19049: Any):
        _x_19050 = True
        return True
    _alt_19052 = _f_19051
    match x_19044:
        case left(a_19053):
            _x_19054 = _alt_19048(a_19053)
            return _x_19054
        case right(a_19055):
            _x_19056 = _alt_19052(a_19055)
            return _x_19056

# Lean: Corpus.Strings.isEmpty
def strings_is_empty(s_973: str) -> bool:
    _x_19061 = len(s_973)
    _x_19062 = 0
    _x_19065 = _x_19061 == 0
    return _x_19065

# Lean: Corpus.Strings.isNotEmpty
def is_not_empty(s_974: str) -> bool:
    _x_19067 = 0
    _x_19070 = len(s_974)
    _x_19071 = 0 < _x_19070
    return _x_19071

# Lean: Corpus.Strings.head
def head(s_975: str) -> str | None:
    _x_19074 = list(s_975)
    _x_19075 = (lambda xs: xs[0] if xs else None)(_x_19074)
    return _x_19075

# Lean: Corpus.Strings.tail
def tail(s_976: str) -> str:
    def _f_19078():
        _x_19077 = ""
        return _x_19077
    _alt_19079 = _f_19078
    def _f_19082(head_19080: str, cs_978: list[str]):
        _x_19081 = ''.join(cs_978)
        return _x_19081
    _alt_19083 = _f_19082
    _x_19084 = list(s_976)
    if len(_x_19084) == 0:
        _x_19086 = _alt_19079()
        return _x_19086
    else:
        head_19087 = _x_19084[0]
        tail_19088 = _x_19084[1:]
        _x_19089 = _alt_19083(head_19087, tail_19088)
        return _x_19089

# Lean: Corpus.Strings.last
def last(s_979: str) -> str | None:
    _x_19092 = list(s_979)
    _x_19093 = (lambda xs: xs[-1] if xs else None)(_x_19092)
    return _x_19093

# Lean: Corpus.Strings.init
def init(s_980: str) -> str:
    _x_19095 = list(s_980)
    _x_19096 = (lambda xs: xs[:-1])(_x_19095)
    _x_19097 = ''.join(_x_19096)
    return _x_19097

# Lean: Corpus.Strings.take
def strings_take(n_981: int, s_982: str) -> str:
    _x_19099 = list(s_982)
    _x_19100 = (lambda n, xs: xs[:n])(_x_19099)
    _x_19101 = ''.join(_x_19100)
    return _x_19101

# Lean: Corpus.Strings.drop
def strings_drop(n_983: int, s_984: str) -> str:
    _x_19103 = list(s_984)
    _x_19104 = (lambda n, xs: xs[n:])(_x_19103)
    _x_19105 = ''.join(_x_19104)
    return _x_19105

# Lean: Corpus.Strings.charAt
def char_at(s_985: str, i_986: int) -> str | None:
    def _f_19110(xs_987: list[str], i_988: int):
        _x_19108 = len(xs_987)
        _x_19109 = i_988 < _x_19108
        return _x_19109
    _x_19112 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_19113 = list(s_985)
    _x_19114 = _x_19112(_x_19113, i_986)
    return _x_19114

# Lean: Corpus.Strings.substring
def substring(s_989: str, start_990: int, len_991: int) -> str:
    _x_19116 = list(s_989)
    _x_19117 = (lambda n, xs: xs[n:])(_x_19116)
    _x_19118 = (lambda n, xs: xs[:n])(_x_19117)
    _x_19119 = ''.join(_x_19118)
    return _x_19119

# Lean: Corpus.Strings.slice
def slice(s_992: str, start_993: int, stop: int) -> str:
    _x_19124 = stop - start_993
    _x_19125 = substring(s_992, start_993, _x_19124)
    return _x_19125

# Lean: Corpus.Strings.append
def append(s1: str, s2: str) -> str:
    _x_19130 = s1 + s2
    return _x_19130

# Lean: Corpus.Strings.concat
def strings_concat(ss: list[str]) -> str:
    def _f_19138(x1_19132: str, x2_19133: str):
        _x_19137 = x1_19132 + x2_19133
        return _x_19137
    _x_19139 = ""
    _x_19140 = functools.reduce(_f_19138, ss, _x_19139)
    return _x_19140

# Lean: Corpus.Strings.intercalate
def intercalate(sep_994: str, ss_995: list[str]) -> str:
    def _f_19143():
        _x_19142 = ""
        return _x_19142
    _alt_19144 = _f_19143
    def _f_19145(s_997: str):
        return s_997
    _alt_19146 = _f_19145
    def _f_19153(s_998: str, rest_999: list[str]):
        _x_19150 = s_998 + sep_994
        _x_19151 = intercalate(sep_994, rest_999)
        _x_19152 = _x_19150 + _x_19151
        return _x_19152
    _alt_19154 = _f_19153
    if len(ss_995) == 0:
        _x_19156 = _alt_19144()
        return _x_19156
    else:
        head_19157 = ss_995[0]
        tail_19158 = ss_995[1:]
        if len(tail_19158) == 0:
            _x_19159 = _alt_19146(head_19157)
            return _x_19159
        else:
            head_19160 = tail_19158[0]
            tail_19161 = tail_19158[1:]
            _x_19162 = [head_19160] + tail_19161
            _x_19163 = _alt_19154(head_19157, _x_19162)
            return _x_19163

# Lean: Corpus.Strings.join
def join(ss_1000: list[str]) -> str:
    _x_19167 = strings_concat(ss_1000)
    return _x_19167

# Lean: Corpus.Strings.replicate
def strings_replicate(n_1001: int, s_1002: str) -> str:
    _x_19169 = ""
    _x_19170 = strings_replicate_go(s_1002, n_1001, _x_19169)
    return _x_19170

# Lean: Corpus.Strings.reverse
def strings_reverse(s_1003: str) -> str:
    _x_19172 = list(s_1003)
    _x_19173 = list(reversed(_x_19172))
    _x_19174 = ''.join(_x_19173)
    return _x_19174

# Lean: Corpus.Strings.toUpper
def to_upper(s_1004: str) -> str:
    _x_19176 = (lambda c: c.upper())
    _x_19177 = list(s_1004)
    _x_19178 = [_x_19176(x) for x in _x_19177]
    _x_19179 = ''.join(_x_19178)
    return _x_19179

# Lean: Corpus.Strings.toLower
def to_lower(s_1005: str) -> str:
    _x_19181 = (lambda c: c.lower())
    _x_19182 = list(s_1005)
    _x_19183 = [_x_19181(x) for x in _x_19182]
    _x_19184 = ''.join(_x_19183)
    return _x_19184

# Lean: Corpus.Strings.capitalize
def capitalize(s_1006: str) -> str:
    def _f_19187():
        _x_19186 = ""
        return _x_19186
    _alt_19188 = _f_19187
    def _f_19192(c_1008: str, cs_1009: list[str]):
        _x_19189 = (lambda c: c.upper())(c_1008)
        _x_19190 = [_x_19189] + cs_1009
        _x_19191 = ''.join(_x_19190)
        return _x_19191
    _alt_19193 = _f_19192
    _x_19194 = list(s_1006)
    if len(_x_19194) == 0:
        _x_19196 = _alt_19188()
        return _x_19196
    else:
        head_19197 = _x_19194[0]
        tail_19198 = _x_19194[1:]
        _x_19199 = _alt_19193(head_19197, tail_19198)
        return _x_19199

# Lean: Corpus.Strings.swapCase
def swap_case(s_1010: str) -> str:
    def _f_19215(c_1011: str):
        _x_19202 = (lambda c: c.isupper())(c_1011)
        _x_19203 = True
        if _x_19202:
            _x_19213 = (lambda c: c.lower())(c_1011)
            return _x_19213
        else:
            _x_19206 = (lambda c: c.islower())(c_1011)
            if _x_19206:
                _x_19210 = (lambda c: c.upper())(c_1011)
                return _x_19210
            else:
                return c_1011
    _x_19216 = list(s_1010)
    _x_19217 = [_f_19215(x) for x in _x_19216]
    _x_19218 = ''.join(_x_19217)
    return _x_19218

# Lean: Corpus.Strings.trimLeft
def trim_left(s_1012: str) -> str:
    def _f_19227(x_19220: str):
        _x_19224 = 32
        _x_19225 = chr(_x_19224)
        _x_19226 = x_19220 == _x_19225
        return _x_19226
    _x_19228 = list(s_1012)
    _x_19229 = drop_while(None, _f_19227, _x_19228)
    _x_19230 = ''.join(_x_19229)
    return _x_19230

# Lean: Corpus.Strings.trimRight
def trim_right(s_1013: str) -> str:
    def _f_19239(x_19232: str):
        _x_19236 = 32
        _x_19237 = chr(_x_19236)
        _x_19238 = x_19232 == _x_19237
        return _x_19238
    _x_19240 = list(s_1013)
    _x_19241 = list(reversed(_x_19240))
    _x_19242 = drop_while(None, _f_19239, _x_19241)
    _x_19243 = list(reversed(_x_19242))
    _x_19244 = ''.join(_x_19243)
    return _x_19244

# Lean: Corpus.Strings.trim
def trim(s_1014: str) -> str:
    _x_19246 = trim_left(s_1014)
    _x_19247 = trim_right(_x_19246)
    return _x_19247

# Lean: Corpus.Strings.padLeft
def pad_left(n_1015: int, c_1016: str, s_1017: str) -> str:
    _x_19249 = len(s_1017)
    _x_19250 = n_1015 <= _x_19249
    if _x_19250:
        return s_1017
    else:
        _x_19258 = n_1015 - _x_19249
        _x_19259 = list_replicate(None, _x_19258, c_1016)
        _x_19260 = ''.join(_x_19259)
        _x_19261 = _x_19260 + s_1017
        return _x_19261

# Lean: Corpus.Strings.padRight
def pad_right(n_1018: int, c_1019: str, s_1020: str) -> str:
    _x_19265 = len(s_1020)
    _x_19266 = n_1018 <= _x_19265
    if _x_19266:
        return s_1020
    else:
        _x_19274 = n_1018 - _x_19265
        _x_19275 = list_replicate(None, _x_19274, c_1019)
        _x_19276 = ''.join(_x_19275)
        _x_19277 = s_1020 + _x_19276
        return _x_19277

# Lean: Corpus.Strings.center
def center(n_1021: int, c_1022: str, s_1023: str) -> str:
    _x_19281 = len(s_1023)
    _x_19282 = n_1021 <= _x_19281
    if _x_19282:
        return s_1023
    else:
        _x_19287 = n_1021 - _x_19281
        _x_19291 = 2
        _x_19294 = _x_19287 // 2
        _x_19295 = _x_19287 - _x_19294
        _x_19299 = list_replicate(None, _x_19294, c_1022)
        _x_19300 = ''.join(_x_19299)
        _x_19301 = _x_19300 + s_1023
        _x_19302 = list_replicate(None, _x_19295, c_1022)
        _x_19303 = ''.join(_x_19302)
        _x_19304 = _x_19301 + _x_19303
        return _x_19304

# Lean: Corpus.Strings.contains
def strings_contains(s_1024: str, sub_1025: str) -> bool:
    _x_19308 = list(s_1024)
    _x_19309 = strings_contains_go(sub_1025, _x_19308)
    return _x_19309

# Lean: Corpus.Strings.indexOf
def index_of(s_1026: str, sub_1027: str) -> int | None:
    _x_19311 = list(s_1026)
    _x_19312 = 0
    _x_19315 = index_of_go(sub_1027, _x_19311, 0)
    return _x_19315

# Lean: Corpus.Strings.count
def count(s_1028: str, sub_1029: str) -> int:
    _x_19317 = list(s_1028)
    _x_19318 = 0
    _x_19321 = count_go(sub_1029, _x_19317, 0)
    return _x_19321

# Lean: Corpus.Strings.countChar
def strings_count_char(c_1030: str, s_1031: str) -> int:
    def _f_19339(acc_1032: int, x_1033: str):
        _x_19326 = x_1033 == c_1030
        _x_19327 = True
        if _x_19326:
            _x_19334 = 1
            _x_19337 = acc_1032 + 1
            return _x_19337
        else:
            return acc_1032
    _x_19340 = 0
    _x_19343 = list(s_1031)
    _x_19344 = functools.reduce(_f_19339, _x_19343, 0)
    return _x_19344

# Lean: Corpus.Strings.startsWith
def starts_with(s_1034: str, pfx: str) -> bool:
    _x_19350 = len(pfx)
    _x_19351 = list(s_1034)
    _x_19352 = (lambda n, xs: xs[:n])(_x_19351)
    _x_19353 = list(pfx)
    _x_19354 = _x_19352 == _x_19353
    return _x_19354

# Lean: Corpus.Strings.endsWith
def ends_with(s_1035: str, suffix: str) -> bool:
    _x_19360 = len(suffix)
    _x_19361 = list(s_1035)
    _x_19362 = list(reversed(_x_19361))
    _x_19363 = (lambda n, xs: xs[:n])(_x_19362)
    _x_19364 = list(suffix)
    _x_19365 = list(reversed(_x_19364))
    _x_19366 = _x_19363 == _x_19365
    return _x_19366

# Lean: Corpus.Strings.isPalindrome
def strings_is_palindrome(s_1036: str) -> bool:
    _x_19368 = (lambda c: c.lower())
    def _f_19381(c_1037: str):
        def _f_19370():
            _x_19369 = True
            return True
        _alt_19371 = _f_19370
        def _f_19373():
            _x_19372 = str.isdigit(c_1037)
            return _x_19372
        _alt_19374 = _f_19373
        _x_19375 = str.isalpha(c_1037)
        if _x_19375:
            _x_19379 = _alt_19371()
            return _x_19379
        else:
            _x_19377 = _alt_19374()
            return _x_19377
    _x_19382 = list(s_1036)
    _x_19383 = [x for x in _x_19382 if _f_19381(x)]
    _x_19384 = [_x_19368(x) for x in _x_19383]
    _x_19389 = list(reversed(_x_19384))
    _x_19390 = _x_19384 == _x_19389
    return _x_19390

# Lean: Corpus.Strings.isDigits
def is_digits(s_1041: str) -> bool:
    def _f_19393():
        _x_19392 = False
        return False
    _alt_19394 = _f_19393
    def _f_19398():
        _x_19395 = list(s_1041)
        _x_19396 = str.isdigit
        _x_19397 = all(_x_19396(x) for x in _x_19395)
        return _x_19397
    _alt_19399 = _f_19398
    _x_19400 = len(s_1041) == 0
    _x_19401 = not _x_19400
    if _x_19401:
        _x_19405 = _alt_19399()
        return _x_19405
    else:
        _x_19403 = _alt_19394()
        return _x_19403

# Lean: Corpus.Strings.isAlpha
def is_alpha(s_1044: str) -> bool:
    def _f_19409():
        _x_19408 = False
        return False
    _alt_19410 = _f_19409
    def _f_19414():
        _x_19411 = list(s_1044)
        _x_19412 = str.isalpha
        _x_19413 = all(_x_19412(x) for x in _x_19411)
        return _x_19413
    _alt_19415 = _f_19414
    _x_19416 = len(s_1044) == 0
    _x_19417 = not _x_19416
    if _x_19417:
        _x_19421 = _alt_19415()
        return _x_19421
    else:
        _x_19419 = _alt_19410()
        return _x_19419

# Lean: Corpus.Strings.splitOn
def split_on(s_1047: str, sep_1048: str) -> list[str]:
    _x_19424 = len(sep_1048) == 0
    _x_19425 = True
    if _x_19424:
        _x_19433 = []
        _x_19434 = [s_1047] + _x_19433
        return _x_19434
    else:
        _x_19428 = list(s_1047)
        _x_19429 = []
        _x_19430 = []
        _x_19431 = split_on_go(sep_1048, _x_19428, _x_19429, _x_19430)
        return _x_19431

# Lean: Corpus.Strings.lines
def lines(s_1049: str) -> list[str]:
    _x_19437 = "\n"
    _x_19438 = split_on(s_1049, _x_19437)
    return _x_19438

# Lean: Corpus.Strings.words
def words(s_1050: str) -> list[str]:
    _x_19440 = list(s_1050)
    _x_19441 = []
    _x_19442 = []
    _x_19443 = words_go(_x_19440, _x_19441, _x_19442)
    return _x_19443

# Lean: Corpus.Strings.unlines
def unlines(ss_1051: list[str]) -> str:
    _x_19445 = "\n"
    _x_19446 = intercalate(_x_19445, ss_1051)
    return _x_19446

# Lean: Corpus.Strings.unwords
def unwords(ss_1052: list[str]) -> str:
    _x_19448 = " "
    _x_19449 = intercalate(_x_19448, ss_1052)
    return _x_19449

# Lean: Corpus.Strings.replace
def replace(s_1053: str, old_1054: str, new_1055: str) -> str:
    _x_19451 = split_on(s_1053, old_1054)
    _x_19452 = intercalate(new_1055, _x_19451)
    return _x_19452

# Lean: Corpus.Strings.replaceFirst
def replace_first(s_1056: str, old_1057: str, new_1058: str) -> str:
    def _f_19454():
        return s_1056
    _alt_19455 = _f_19454
    def _f_19468(i_1060: int):
        _x_19459 = strings_take(i_1060, s_1056)
        _x_19460 = _x_19459 + new_1058
        _x_19464 = len(old_1057)
        _x_19465 = i_1060 + _x_19464
        _x_19466 = strings_drop(_x_19465, s_1056)
        _x_19467 = _x_19460 + _x_19466
        return _x_19467
    _alt_19469 = _f_19468
    _x_19470 = index_of(s_1056, old_1057)
    if _x_19470 is None:
        _x_19472 = _alt_19455()
        return _x_19472
    else:
        val_19473 = _x_19470
        _x_19474 = _alt_19469(val_19473)
        return _x_19474

# Lean: Corpus.Strings.removePrefix
def remove_prefix(pfx_1061: str, s_1062: str) -> str:
    _x_19477 = starts_with(s_1062, pfx_1061)
    _x_19478 = True
    if _x_19477:
        _x_19482 = len(pfx_1061)
        _x_19483 = strings_drop(_x_19482, s_1062)
        return _x_19483
    else:
        return s_1062

# Lean: Corpus.Strings.removeSuffix
def remove_suffix(suffix_1063: str, s_1064: str) -> str:
    _x_19486 = ends_with(s_1064, suffix_1063)
    _x_19487 = True
    if _x_19486:
        _x_19494 = len(s_1064)
        _x_19495 = len(suffix_1063)
        _x_19496 = _x_19494 - _x_19495
        _x_19497 = strings_take(_x_19496, s_1064)
        return _x_19497
    else:
        return s_1064

# Lean: Corpus.Strings.toCharList
def to_char_list(s_1065: str) -> list[str]:
    _x_19500 = list(s_1065)
    return _x_19500

# Lean: Corpus.Strings.fromCharList
def from_char_list(cs_1066: list[str]) -> str:
    _x_19502 = ''.join(cs_1066)
    return _x_19502

# Lean: Corpus.Strings.filterChars
def filter_chars(p_1067: Callable[[str], bool], s_1068: str) -> str:
    _x_19504 = list(s_1068)
    _x_19505 = [x for x in _x_19504 if p_1067(x)]
    _x_19506 = ''.join(_x_19505)
    return _x_19506

# Lean: Corpus.Strings.mapChars
def map_chars(f_1069: Callable[[str], str], s_1070: str) -> str:
    _x_19508 = list(s_1070)
    _x_19509 = [f_1069(x) for x in _x_19508]
    _x_19510 = ''.join(_x_19509)
    return _x_19510

# Lean: Corpus.Strings.ord
def strings_ord(c_1071: str) -> int:
    _x_19512 = ord(c_1071)
    return _x_19512

# Lean: Corpus.Strings.chr
def strings_chr(n_1072: int) -> str:
    _x_19514 = chr(n_1072)
    return _x_19514

# Lean: Corpus.Strings.toAsciiCodes
def to_ascii_codes(s_1073: str) -> list[int]:
    _x_19516 = ord
    _x_19517 = list(s_1073)
    _x_19518 = [_x_19516(x) for x in _x_19517]
    return _x_19518

# Lean: Corpus.Strings.fromAsciiCodes
def from_ascii_codes(ns: list[int]) -> str:
    _x_19520 = chr
    _x_19521 = [_x_19520(x) for x in ns]
    _x_19522 = ''.join(_x_19521)
    return _x_19522

# Lean: Corpus.Games.Player.other
def other(x_19524: Player) -> Player:
    def _f_19526():
        _x_19525 = O()
        return _x_19525
    _alt_19527 = _f_19526
    def _f_19529():
        _x_19528 = X()
        return _x_19528
    _alt_19530 = _f_19529
    match x_19524:
        case X():
            _x_19532 = _alt_19527()
            return _x_19532
        case O():
            _x_19534 = _alt_19530()
            return _x_19534

# Lean: Corpus.Games.TicTacToe.empty
def tic_tac_toe_empty() -> TicTacToe:
    _x_19537 = 9
    _x_19540 = None
    _x_19541 = list_replicate(None, 9, _x_19540)
    _x_19542 = X()
    _x_19543 = TicTacToe_mk(_x_19541, _x_19542)
    return _x_19543

# Lean: Corpus.Games.TicTacToe.get
def tic_tac_toe_get(g_1076: TicTacToe, row: int, col: int) -> Player | None:
    def _f_19544(p_1077: Player | None):
        return p_1077
    _alt_19545 = _f_19544
    def _f_19547():
        _x_19546 = None
        return _x_19546
    _alt_19548 = _f_19547
    def _f_19552(xs_1079: list[Player | None], i_1080: int):
        _x_19550 = len(xs_1079)
        _x_19551 = i_1080 < _x_19550
        return _x_19551
    _x_19554 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_19555 = g_1076.tic_tac_toe_0
    _x_19562 = 3
    _x_19565 = row * 3
    _x_19566 = _x_19565 + col
    _x_19567 = _x_19554(_x_19555, _x_19566)
    if _x_19567 is None:
        _x_19569 = _alt_19548()
        return _x_19569
    else:
        val_19570 = _x_19567
        _x_19571 = _alt_19545(val_19570)
        return _x_19571

# Lean: Corpus.Games.TicTacToe.set
def tic_tac_toe_set(g_1081: TicTacToe, row_1082: int, col_1083: int) -> TicTacToe | None:
    _x_19580 = 3
    _x_19583 = row_1082 * 3
    _x_19584 = _x_19583 + col_1083
    _x_19585 = 9
    _x_19588 = 9 <= _x_19584
    if _x_19588:
        _x_19623 = None
        return _x_19623
    else:
        def _f_19597():
            _x_19590 = g_1081.tic_tac_toe_0
            _x_19591 = g_1081.tic_tac_toe_1
            _x_19592 = _x_19591
            _x_19593 = _x_19590[:_x_19584] + [_x_19592] + _x_19590[_x_19584+1:]
            _x_19594 = other(_x_19591)
            _x_19595 = TicTacToe_mk(_x_19593, _x_19594)
            _x_19596 = _x_19595
            return _x_19596
        _alt_19598 = _f_19597
        def _f_19601(x_19599: Player | None | None):
            _x_19600 = None
            return _x_19600
        _alt_19602 = _f_19601
        def _f_19606(xs_1086: list[Player | None], i_1087: int):
            _x_19604 = len(xs_1086)
            _x_19605 = i_1087 < _x_19604
            return _x_19605
        _x_19608 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
        _x_19609 = g_1081.tic_tac_toe_0
        _x_19610 = _x_19608(_x_19609, _x_19584)
        if _x_19610 is None:
            _x_19611 = None
            _x_19612 = _alt_19602(_x_19611)
            return _x_19612
        else:
            val_19613 = _x_19610
            if val_19613 is None:
                _x_19615 = _alt_19598()
                return _x_19615
            else:
                val_19616 = val_19613
                _x_19617 = val_19616
                _x_19618 = _x_19617
                _x_19619 = _alt_19602(_x_19618)
                return _x_19619

# Lean: Corpus.Games.TicTacToe.checkLine
def check_line(g_1088: TicTacToe, i1: int, i2: int, i3: int) -> Player | None:
    def _f_19656(p1_1089: Player, p2_1090: Player, p3_1091: Player):
        def _f_19627():
            _x_19626 = False
            return False
        _alt_19628 = _f_19627
        def _f_19632():
            _x_19631 = p2_1090 == p3_1091
            return _x_19631
        _alt_19633 = _f_19632
        _x_19636 = p1_1089 == p2_1090
        def _jp_19649(_y_19641: bool):
            _x_19642 = True
            if _y_19641:
                _x_19647 = p1_1089
                return _x_19647
            else:
                _x_19645 = None
                return _x_19645
        def _jp_19652():
            _x_19651 = _alt_19628()
            return _jp_19649(_x_19651)
        def _jp_19655():
            _x_19654 = _alt_19633()
            return _jp_19649(_x_19654)
        if _x_19636:
            return _jp_19655()
        else:
            return _jp_19652()
    _alt_19657 = _f_19656
    def _f_19662(x_19658: Player | None | None, x_19659: Player | None | None, x_19660: Player | None | None):
        _x_19661 = None
        return _x_19661
    _alt_19663 = _f_19662
    def _f_19667(xs_1094: list[Player | None], i_1095: int):
        _x_19665 = len(xs_1094)
        _x_19666 = i_1095 < _x_19665
        return _x_19666
    _x_19669 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_19670 = g_1088.tic_tac_toe_0
    _x_19671 = _x_19669(_x_19670, i1)
    if _x_19671 is None:
        _x_19672 = None
        _x_19673 = _x_19669(_x_19670, i2)
        _x_19674 = _x_19669(_x_19670, i3)
        _x_19675 = _alt_19663(_x_19672, _x_19673, _x_19674)
        return _x_19675
    else:
        val_19676 = _x_19671
        if val_19676 is None:
            _x_19677 = None
            _x_19678 = _x_19677
            _x_19679 = _x_19669(_x_19670, i2)
            _x_19680 = _x_19669(_x_19670, i3)
            _x_19681 = _alt_19663(_x_19678, _x_19679, _x_19680)
            return _x_19681
        else:
            val_19682 = val_19676
            _x_19683 = _x_19669(_x_19670, i2)
            if _x_19683 is None:
                _x_19684 = val_19682
                _x_19685 = _x_19684
                _x_19686 = None
                _x_19687 = _x_19669(_x_19670, i3)
                _x_19688 = _alt_19663(_x_19685, _x_19686, _x_19687)
                return _x_19688
            else:
                val_19689 = _x_19683
                if val_19689 is None:
                    _x_19690 = val_19682
                    _x_19691 = _x_19690
                    _x_19692 = None
                    _x_19693 = _x_19692
                    _x_19694 = _x_19669(_x_19670, i3)
                    _x_19695 = _alt_19663(_x_19691, _x_19693, _x_19694)
                    return _x_19695
                else:
                    val_19696 = val_19689
                    _x_19697 = _x_19669(_x_19670, i3)
                    if _x_19697 is None:
                        _x_19698 = val_19682
                        _x_19699 = _x_19698
                        _x_19700 = val_19696
                        _x_19701 = _x_19700
                        _x_19702 = None
                        _x_19703 = _alt_19663(_x_19699, _x_19701, _x_19702)
                        return _x_19703
                    else:
                        val_19704 = _x_19697
                        if val_19704 is None:
                            _x_19705 = val_19682
                            _x_19706 = _x_19705
                            _x_19707 = val_19696
                            _x_19708 = _x_19707
                            _x_19709 = None
                            _x_19710 = _x_19709
                            _x_19711 = _alt_19663(_x_19706, _x_19708, _x_19710)
                            return _x_19711
                        else:
                            val_19712 = val_19704
                            _x_19713 = _alt_19657(val_19682, val_19696, val_19712)
                            return _x_19713

# Lean: Corpus.Games.TicTacToe.winner
def winner(g_1096: TicTacToe) -> Player | None:
    _x_19721 = 0
    _x_19724 = 1
    _x_19727 = 2
    _x_19730 = (1, 2)
    _x_19731 = (0, _x_19730)
    _x_19732 = 3
    _x_19735 = 4
    _x_19738 = 5
    _x_19741 = (4, 5)
    _x_19742 = (3, _x_19741)
    _x_19743 = 6
    _x_19746 = 7
    _x_19749 = 8
    _x_19752 = (7, 8)
    _x_19753 = (6, _x_19752)
    _x_19754 = (3, 6)
    _x_19755 = (0, _x_19754)
    _x_19756 = (4, 7)
    _x_19757 = (1, _x_19756)
    _x_19758 = (5, 8)
    _x_19759 = (2, _x_19758)
    _x_19760 = (4, 8)
    _x_19761 = (0, _x_19760)
    _x_19762 = (4, 6)
    _x_19763 = (2, _x_19762)
    _x_19764 = []
    _x_19765 = [_x_19763] + _x_19764
    _x_19766 = [_x_19761] + _x_19765
    _x_19767 = [_x_19759] + _x_19766
    _x_19768 = [_x_19757] + _x_19767
    _x_19769 = [_x_19755] + _x_19768
    _x_19770 = [_x_19753] + _x_19769
    _x_19771 = [_x_19742] + _x_19770
    _x_19772 = [_x_19731] + _x_19771
    def _f_19784(x_19773: tuple[int, tuple[int, int]]):
        def _f_19775(i1_1097: int, i2_1098: int, i3_1099: int):
            _x_19774 = check_line(g_1096, i1_1097, i2_1098, i3_1099)
            return _x_19774
        _alt_19776 = _f_19775
        match x_19773:
            case (fst_19777, snd_19778):
                match snd_19778:
                    case (fst_19779, snd_19780):
                        _x_19781 = _alt_19776(fst_19777, fst_19779, snd_19780)
                        return _x_19781
    _x_19785 = next((y for x in _x_19772 if (y := _f_19784(x)) is not None), None)
    return _x_19785

# Lean: Corpus.Games.TicTacToe.isDraw
def is_draw(g_1100: TicTacToe) -> bool:
    def _f_19788():
        _x_19787 = False
        return False
    _alt_19789 = _f_19788
    def _f_19793():
        _x_19790 = g_1100.tic_tac_toe_0
        _x_19791 = (lambda x: x is not None)(None)
        _x_19792 = all(_x_19791(x) for x in _x_19790)
        return _x_19792
    _alt_19794 = _f_19793
    _x_19795 = winner(g_1100)
    _x_19796 = (lambda x: x is None)(_x_19795)
    if _x_19796:
        _x_19800 = _alt_19794()
        return _x_19800
    else:
        _x_19798 = _alt_19789()
        return _x_19798

# Lean: Corpus.Games.TicTacToe.isOver
def tic_tac_toe_is_over(g_1103: TicTacToe) -> bool:
    def _f_19804():
        _x_19803 = True
        return True
    _alt_19805 = _f_19804
    def _f_19807():
        _x_19806 = is_draw(g_1103)
        return _x_19806
    _alt_19808 = _f_19807
    _x_19809 = winner(g_1103)
    _x_19810 = (lambda x: x is not None)(_x_19809)
    if _x_19810:
        _x_19814 = _alt_19805()
        return _x_19814
    else:
        _x_19812 = _alt_19808()
        return _x_19812

# Lean: Corpus.Games.TicTacToe.validMoves
def valid_moves(g_1106: TicTacToe) -> list[tuple[int, int]]:
    _x_19817 = tic_tac_toe_is_over(g_1106)
    _x_19818 = True
    if _x_19817:
        _x_19866 = []
        return _x_19866
    else:
        def _f_19859(i_1107: int):
            def _f_19834():
                _x_19824 = 3
                _x_19827 = i_1107 // 3
                _x_19831 = i_1107 % 3
                _x_19832 = (_x_19827, _x_19831)
                _x_19833 = _x_19832
                return _x_19833
            _alt_19835 = _f_19834
            def _f_19838(x_19836: Player | None | None):
                _x_19837 = None
                return _x_19837
            _alt_19839 = _f_19838
            def _f_19843(xs_1109: list[Player | None], i_1110: int):
                _x_19841 = len(xs_1109)
                _x_19842 = i_1110 < _x_19841
                return _x_19842
            _x_19845 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_19846 = g_1106.tic_tac_toe_0
            _x_19847 = _x_19845(_x_19846, i_1107)
            if _x_19847 is None:
                _x_19848 = None
                _x_19849 = _alt_19839(_x_19848)
                return _x_19849
            else:
                val_19850 = _x_19847
                if val_19850 is None:
                    _x_19852 = _alt_19835()
                    return _x_19852
                else:
                    val_19853 = val_19850
                    _x_19854 = val_19853
                    _x_19855 = _x_19854
                    _x_19856 = _alt_19839(_x_19855)
                    return _x_19856
        _x_19860 = 9
        _x_19863 = list(range(9))
        _x_19864 = [y for x in _x_19863 if (y := _f_19859(x)) is not None]
        return _x_19864

# Lean: Corpus.Games.Nim.create
def nim_create(sizes: list[int]) -> Nim:
    _x_19869 = Nim_mk(sizes)
    return _x_19869

# Lean: Corpus.Games.Nim.take
def nim_take(g_1111: Nim, pile: int, count_1112: int) -> Nim | None:
    def _f_19909(n_1113: int):
        def _f_19872():
            _x_19871 = False
            return False
        _alt_19873 = _f_19872
        def _f_19876():
            _x_19874 = count_1112 <= n_1113
            return _x_19874
        _alt_19877 = _f_19876
        _x_19878 = 0
        _x_19881 = 0 < count_1112
        def _jp_19902(_y_19887: bool):
            _x_19888 = True
            if _y_19887:
                _x_19893 = g_1111.nim_0
                _x_19897 = n_1113 - count_1112
                _x_19898 = _x_19893[:pile] + [_x_19897] + _x_19893[pile+1:]
                _x_19899 = Nim_mk(_x_19898)
                _x_19900 = _x_19899
                return _x_19900
            else:
                _x_19891 = None
                return _x_19891
        def _jp_19905():
            _x_19904 = _alt_19873()
            return _jp_19902(_x_19904)
        def _jp_19908():
            _x_19907 = _alt_19877()
            return _jp_19902(_x_19907)
        if _x_19881:
            return _jp_19908()
        else:
            return _jp_19905()
    _alt_19910 = _f_19909
    def _f_19912():
        _x_19911 = None
        return _x_19911
    _alt_19913 = _f_19912
    def _f_19917(xs_1117: list[int], i_1118: int):
        _x_19915 = len(xs_1117)
        _x_19916 = i_1118 < _x_19915
        return _x_19916
    _x_19919 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
    _x_19920 = g_1111.nim_0
    _x_19921 = _x_19919(_x_19920, pile)
    if _x_19921 is None:
        _x_19923 = _alt_19913()
        return _x_19923
    else:
        val_19924 = _x_19921
        _x_19925 = _alt_19910(val_19924)
        return _x_19925

# Lean: Corpus.Games.Nim.isOver
def nim_is_over(g_1119: Nim) -> bool:
    _x_19928 = g_1119.nim_0
    def _f_19936(x_19929: int):
        _x_19932 = 0
        _x_19935 = x_19929 == 0
        return _x_19935
    _x_19937 = all(_f_19936(x) for x in _x_19928)
    return _x_19937

# Lean: Corpus.Games.Nim.nimSum
def nim_sum(g_1120: Nim) -> int:
    _x_19939 = (lambda a, b: a ^ b)
    _x_19940 = 0
    _x_19943 = g_1120.nim_0
    _x_19944 = functools.reduce(_x_19939, _x_19943, 0)
    return _x_19944

# Lean: Corpus.Games.Nim.isWinningPosition
def is_winning_position(g_1121: Nim) -> bool:
    _x_19947 = nim_sum(g_1121)
    _x_19948 = 0
    _x_19951 = (lambda a, b: a != b)(0)
    return _x_19951

# Lean: Corpus.Games.Card.value
def value(c_1122: Card) -> int:
    def _f_19956():
        _x_19953 = 11
        return 11
    _alt_19957 = _f_19956
    def _f_19961():
        _x_19958 = 2
        return 2
    _alt_19962 = _f_19961
    def _f_19966():
        _x_19963 = 3
        return 3
    _alt_19967 = _f_19966
    def _f_19971():
        _x_19968 = 4
        return 4
    _alt_19972 = _f_19971
    def _f_19976():
        _x_19973 = 5
        return 5
    _alt_19977 = _f_19976
    def _f_19981():
        _x_19978 = 6
        return 6
    _alt_19982 = _f_19981
    def _f_19986():
        _x_19983 = 7
        return 7
    _alt_19987 = _f_19986
    def _f_19991():
        _x_19988 = 8
        return 8
    _alt_19992 = _f_19991
    def _f_19996():
        _x_19993 = 9
        return 9
    _alt_19997 = _f_19996
    def _f_20001():
        _x_19998 = 10
        return 10
    _alt_20002 = _f_20001
    _alt_20003 = _f_20001
    _alt_20004 = _f_20001
    _alt_20005 = _f_20001
    _x_20006 = c_1122.card_0
    match _x_20006:
        case ace():
            _x_20008 = _alt_19957()
            return _x_20008
        case two():
            _x_20010 = _alt_19962()
            return _x_20010
        case three():
            _x_20012 = _alt_19967()
            return _x_20012
        case four():
            _x_20014 = _alt_19972()
            return _x_20014
        case five():
            _x_20016 = _alt_19977()
            return _x_20016
        case six():
            _x_20018 = _alt_19982()
            return _x_20018
        case seven():
            _x_20020 = _alt_19987()
            return _x_20020
        case eight():
            _x_20022 = _alt_19992()
            return _x_20022
        case nine():
            _x_20024 = _alt_19997()
            return _x_20024
        case ten():
            _x_20026 = _alt_20002()
            return _x_20026
        case jack():
            _x_20028 = _alt_20003()
            return _x_20028
        case queen():
            _x_20030 = _alt_20004()
            return _x_20030
        case king():
            _x_20032 = _alt_20005()
            return _x_20032

# Lean: Corpus.Games.Card.isAce
def is_ace(c_1133: Card) -> bool:
    _x_20037 = c_1133.card_0
    _x_20038 = ace()
    _x_20039 = _x_20037 == _x_20038
    return _x_20039

# Lean: Corpus.Games.BlackjackHand.empty
def blackjack_hand_empty() -> BlackjackHand:
    _x_20041 = []
    _x_20042 = BlackjackHand_mk(_x_20041)
    return _x_20042

# Lean: Corpus.Games.BlackjackHand.add
def add(h_1134: BlackjackHand, c_1135: Card) -> BlackjackHand:
    _x_20043 = h_1134.blackjack_hand_0
    _x_20044 = [c_1135] + _x_20043
    _x_20045 = BlackjackHand_mk(_x_20044)
    return _x_20045

# Lean: Corpus.Games.BlackjackHand.hardValue
def hard_value(h_1136: BlackjackHand) -> int:
    def _f_20052(acc_1137: int, c_1138: Card):
        _x_20050 = value(c_1138)
        _x_20051 = acc_1137 + _x_20050
        return _x_20051
    _x_20053 = 0
    _x_20056 = h_1136.blackjack_hand_0
    _x_20057 = functools.reduce(_f_20052, _x_20056, 0)
    return _x_20057

# Lean: Corpus.Games.BlackjackHand.numAces
def num_aces(h_1139: BlackjackHand) -> int:
    _x_20059 = is_ace()
    _x_20060 = h_1139.blackjack_hand_0
    _x_20061 = [x for x in _x_20060 if _x_20059(x)]
    _x_20062 = len(_x_20061)
    return _x_20062

# Lean: Corpus.Games.BlackjackHand.bestValue
def best_value(h_1140: BlackjackHand) -> int:
    _x_20064 = hard_value(h_1140)
    _x_20065 = num_aces(h_1140)
    _x_20066 = best_value_adjust(_x_20064, _x_20065)
    return _x_20066

# Lean: Corpus.Games.BlackjackHand.isBust
def is_bust(h_1141: BlackjackHand) -> bool:
    _x_20068 = 21
    _x_20071 = best_value(h_1141)
    _x_20072 = 21 < _x_20071
    return _x_20072

# Lean: Corpus.Games.BlackjackHand.isBlackjack
def is_blackjack(h_1142: BlackjackHand) -> bool:
    def _f_20076():
        _x_20075 = False
        return False
    _alt_20077 = _f_20076
    def _f_20085():
        _x_20080 = best_value(h_1142)
        _x_20081 = 21
        _x_20084 = _x_20080 == 21
        return _x_20084
    _alt_20086 = _f_20085
    _x_20089 = h_1142.blackjack_hand_0
    _x_20090 = len(_x_20089)
    _x_20091 = 2
    _x_20094 = _x_20090 == 2
    if _x_20094:
        _x_20098 = _alt_20086()
        return _x_20098
    else:
        _x_20096 = _alt_20077()
        return _x_20096

# Lean: Corpus.Games.roll
def roll(sides_1145: int, seed_1146: int) -> int:
    _x_20110 = 1103515245
    _x_20113 = seed_1146 * 1103515245
    _x_20114 = 12345
    _x_20117 = _x_20113 + 12345
    _x_20122 = 2
    _x_20125 = 31
    _x_20128 = 2 ** 31
    _x_20129 = _x_20117 % _x_20128
    _x_20130 = _x_20129 % sides_1145
    _x_20131 = 1
    _x_20134 = _x_20130 + 1
    return _x_20134

# Lean: Corpus.Games.rollDice
def roll_dice(num_dice: int, sides_1147: int, seed_1148: int) -> tuple[list[int], int]:
    _x_20136 = []
    _x_20137 = roll_dice_go(sides_1147, num_dice, seed_1148, _x_20136)
    return _x_20137

# Lean: Corpus.Games.sumDice
def sum_dice(dice: list[int]) -> int:
    def _f_20145(x1_20139: int, x2_20140: int):
        _x_20144 = x1_20139 + x2_20140
        return _x_20144
    _x_20146 = 0
    _x_20149 = functools.reduce(_f_20145, dice, 0)
    return _x_20149

# Lean: Corpus.Games.yahtzeeScore
def yahtzee_score(dice_1149: list[int]) -> int:
    _x_20152 = len(dice_1149)
    _x_20153 = 5
    _x_20156 = (lambda a, b: a != b)(5)
    _x_20157 = True
    if _x_20156:
        _x_20301 = 0
        return 0
    else:
        _x_20160 = list(dice_1149)
        def _f_20165(x1_20161: int, x2_20162: int):
            _x_20163 = x1_20161 < x2_20162
            return _x_20163
        _x_20166 = 0
        _x_20172 = len(_x_20160)
        _x_20173 = 1
        _x_20176 = _x_20172 - 1
        _x_20177 = sorted(0, key=functools.cmp_to_key(lambda a, b: -1 if _x_20176(a, b) else 1))
        _x_20178 = list(_x_20177)
        def _f_20189(n_1151: int):
            def _f_20186(x_20179: int):
                _x_20184 = n_1151 + 1
                _x_20185 = x_20179 == _x_20184
                return _x_20185
            _x_20187 = [x for x in dice_1149 if _f_20186(x)]
            _x_20188 = len(_x_20187)
            return _x_20188
        _x_20190 = 6
        _x_20193 = list(range(6))
        _x_20194 = [_f_20189(x) for x in _x_20193]
        _x_20196 = max
        _x_20197 = functools.reduce(_x_20196, _x_20194, 0)
        def _f_20204(x1_20198: int, x2_20199: int):
            _x_20203 = x1_20198 + x2_20199
            return _x_20203
        _x_20205 = functools.reduce(_f_20204, dice_1149, 0)
        _x_20207 = _x_20197 == 5
        if _x_20207:
            _x_20296 = 50
            return 50
        else:
            def _f_20210():
                return True
            _alt_20211 = _f_20210
            def _f_20230():
                _x_20214 = 2
                _x_20217 = 3
                _x_20220 = 4
                _x_20223 = []
                _x_20224 = [6] + _x_20223
                _x_20225 = [5] + _x_20224
                _x_20226 = [4] + _x_20225
                _x_20227 = [3] + _x_20226
                _x_20228 = [2] + _x_20227
                _x_20229 = _x_20178 == _x_20228
                return _x_20229
            _alt_20231 = _f_20230
            _x_20234 = 2
            _x_20237 = 3
            _x_20240 = 4
            _x_20243 = []
            _x_20244 = [5] + _x_20243
            _x_20245 = [4] + _x_20244
            _x_20246 = [3] + _x_20245
            _x_20247 = [2] + _x_20246
            _x_20248 = [1] + _x_20247
            _x_20249 = _x_20178 == _x_20248
            def _jp_20288(_y_20254: bool):
                if _y_20254:
                    _x_20284 = 40
                    return 40
                else:
                    def _f_20258():
                        _x_20257 = False
                        return False
                    _alt_20259 = _f_20258
                    def _f_20261():
                        _x_20260 = 2 in _x_20194
                        return _x_20260
                    _alt_20262 = _f_20261
                    _x_20263 = 3 in _x_20194
                    def _jp_20276(_y_20268: bool):
                        if _y_20268:
                            _x_20272 = 25
                            return 25
                        else:
                            return _x_20205
                    def _jp_20279():
                        _x_20278 = _alt_20259()
                        return _jp_20276(_x_20278)
                    def _jp_20282():
                        _x_20281 = _alt_20262()
                        return _jp_20276(_x_20281)
                    if _x_20263:
                        return _jp_20282()
                    else:
                        return _jp_20279()
            def _jp_20294():
                _x_20293 = _alt_20211()
                return _jp_20288(_x_20293)
            def _jp_20291():
                _x_20290 = _alt_20231()
                return _jp_20288(_x_20290)
            if _x_20249:
                return _jp_20294()
            else:
                return _jp_20291()

# Lean: Corpus.Games.RPS.beats
def beats(x_20306: RPS, x_20307: RPS) -> bool:
    def _f_20309():
        _x_20308 = True
        return True
    _alt_20310 = _f_20309
    _alt_20311 = _f_20309
    _alt_20312 = _f_20309
    def _f_20316(x_20313: RPS, x_20314: RPS):
        _x_20315 = False
        return False
    _alt_20317 = _f_20316
    match x_20306:
        case rock():
            match x_20307:
                case rock():
                    _x_20318 = rock()
                    _x_20319 = _alt_20317(_x_20318, _x_20318)
                    return _x_20319
                case paper():
                    _x_20320 = rock()
                    _x_20321 = paper()
                    _x_20322 = _alt_20317(_x_20320, _x_20321)
                    return _x_20322
                case scissors():
                    _x_20324 = _alt_20310()
                    return _x_20324
        case paper():
            match x_20307:
                case rock():
                    _x_20327 = _alt_20311()
                    return _x_20327
                case paper():
                    _x_20328 = paper()
                    _x_20329 = _alt_20317(_x_20328, _x_20328)
                    return _x_20329
                case scissors():
                    _x_20330 = paper()
                    _x_20331 = scissors()
                    _x_20332 = _alt_20317(_x_20330, _x_20331)
                    return _x_20332
        case scissors():
            match x_20307:
                case rock():
                    _x_20334 = scissors()
                    _x_20335 = rock()
                    _x_20336 = _alt_20317(_x_20334, _x_20335)
                    return _x_20336
                case paper():
                    _x_20338 = _alt_20312()
                    return _x_20338
                case scissors():
                    _x_20339 = scissors()
                    _x_20340 = _alt_20317(_x_20339, _x_20339)
                    return _x_20340

# Lean: Corpus.Games.RPS.compare
def compare(a_1158: RPS, b_1159: RPS) -> int:
    _x_20346 = a_1158 == b_1159
    _x_20347 = True
    if _x_20346:
        _x_20365 = 0
        return 0
    else:
        _x_20350 = beats(a_1158, b_1159)
        if _x_20350:
            _x_20360 = 1
            return 1
        else:
            _x_20355 = 1
            _x_20358 = -1
            return _x_20358

# Lean: Corpus.Games.RPS.fromNat
def from_nat(x_20370: int) -> RPS | None:
    def _f_20373():
        _x_20371 = rock()
        _x_20372 = _x_20371
        return _x_20372
    _alt_20374 = _f_20373
    def _f_20377():
        _x_20375 = paper()
        _x_20376 = _x_20375
        return _x_20376
    _alt_20378 = _f_20377
    def _f_20381():
        _x_20379 = scissors()
        _x_20380 = _x_20379
        return _x_20380
    _alt_20382 = _f_20381
    def _f_20385(x_20383: int):
        _x_20384 = None
        return _x_20384
    _alt_20386 = _f_20385
    _x_20387 = 0
    if x_20370:
        _x_20391 = 1
        if x_20370:
            _x_20395 = 2
            if x_20370:
                _x_20399 = _alt_20386(x_20370)
                return _x_20399
            else:
                def _f_20402(h_1: Any, h_2: Any):
                    _x_20401 = _alt_20382()
                    return _x_20401
                _x_20403 = _f_20402(None, None)
                return _x_20403
        else:
            def _f_20407(h_1_1163: Any):
                _x_20406 = _alt_20378()
                return _x_20406
            _x_20408 = _f_20407(None)
            return _x_20408
    else:
        _x_20411 = _alt_20374()
        return _x_20411

# Lean: Corpus.Games.isValidSudokuRow
def is_valid_sudoku_row(row_1164: list[int]) -> bool:
    def _f_20420(x_20414: int):
        _x_20416 = 0
        _x_20419 = (lambda a, b: a != b)(0)
        return _x_20419
    _x_20421 = [x for x in row_1164 if _f_20420(x)]
    _x_20424 = len(_x_20421)
    _x_20425 = list(dict.fromkeys(_x_20421))
    _x_20426 = len(_x_20425)
    _x_20427 = _x_20424 == _x_20426
    return _x_20427

# Lean: Corpus.Games.isValidSudokuGrid
def is_valid_sudoku_grid(grid: list[list[int]]) -> bool:
    _x_20429 = is_valid_sudoku_row()
    _x_20430 = all(_x_20429(x) for x in grid)
    def _f_20440(c_1165: int):
        def _f_20438(row_1166: list[int]):
            def _f_20434(xs_1167: list[int], i_1168: int):
                _x_20432 = len(xs_1167)
                _x_20433 = i_1168 < _x_20432
                return _x_20433
            _x_20436 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
            _x_20437 = _x_20436(row_1166, c_1165)
            return _x_20437
        _x_20439 = [y for x in grid if (y := _f_20438(x)) is not None]
        return _x_20439
    _x_20441 = 9
    _x_20444 = list(range(9))
    _x_20445 = [_f_20440(x) for x in _x_20444]
    _x_20446 = all(_x_20429(x) for x in _x_20445)
    _x_20447 = 3
    _x_20450 = list(range(3))
    def _f_20497(br: int):
        def _f_20495(bc: int):
            def _f_20493(r_1169: int):
                def _f_20491(c_1170: int):
                    def _f_20466(row_1171: list[int]):
                        def _f_20454(xs_1172: list[int], i_1173: int):
                            _x_20452 = len(xs_1172)
                            _x_20453 = i_1173 < _x_20452
                            return _x_20453
                        _x_20456 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                        _x_20463 = bc * 3
                        _x_20464 = _x_20463 + c_1170
                        _x_20465 = _x_20456(row_1171, _x_20464)
                        return _x_20465
                    _alt_20467 = _f_20466
                    def _f_20469():
                        _x_20468 = None
                        return _x_20468
                    _alt_20470 = _f_20469
                    def _f_20474(xs_1175: list[list[int]], i_1176: int):
                        _x_20472 = len(xs_1175)
                        _x_20473 = i_1176 < _x_20472
                        return _x_20473
                    _x_20476 = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)
                    _x_20483 = br * 3
                    _x_20484 = _x_20483 + r_1169
                    _x_20485 = _x_20476(grid, _x_20484)
                    if _x_20485 is None:
                        _x_20487 = _alt_20470()
                        return _x_20487
                    else:
                        val_20488 = _x_20485
                        _x_20489 = _alt_20467(val_20488)
                        return _x_20489
                _x_20492 = [y for x in _x_20450 if (y := _f_20491(x)) is not None]
                return _x_20492
            _x_20494 = [y for x in _x_20450 for y in _f_20493(x)]
            return _x_20494
        _x_20496 = [_f_20495(x) for x in _x_20450]
        return _x_20496
    _x_20498 = [y for x in _x_20450 for y in _f_20497(x)]
    _x_20499 = all(_x_20429(x) for x in _x_20498)
    def _f_20501():
        _x_20500 = False
        return False
    _alt_20502 = _f_20501
    def _f_20503():
        return _x_20499
    _alt_20504 = _f_20503
    _alt_20505 = _f_20501
    def _f_20506():
        return _x_20446
    _alt_20507 = _f_20506
    def _jp_20518(_y_20512: bool):
        if _y_20512:
            _x_20516 = _alt_20504()
            return _x_20516
        else:
            _x_20514 = _alt_20502()
            return _x_20514
    def _jp_20521():
        _x_20520 = _alt_20505()
        return _jp_20518(_x_20520)
    def _jp_20524():
        _x_20523 = _alt_20507()
        return _jp_20518(_x_20523)
    if _x_20430:
        return _jp_20524()
    else:
        return _jp_20521()

# Lean: Corpus.DataStructures.Stack.empty
def stack_empty(__1180: Any) -> Any:
    _x_20526 = []
    _x_20527 = Stack_mk(None, _x_20526)
    return _x_20527

# Lean: Corpus.DataStructures.Stack.push
def stack_push(__1181: Any, s_1182: Any, x_1183: Any) -> Any:
    _x_20529 = s_1182.stack_0
    _x_20530 = [x_1183] + _x_20529
    _x_20531 = Stack_mk(None, _x_20530)
    return _x_20531

# Lean: Corpus.DataStructures.Stack.pop
def pop(__1184: Any, s_1185: Any) -> tuple[Any, Any] | None:
    def _f_20534():
        _x_20533 = None
        return _x_20533
    _alt_20535 = _f_20534
    def _f_20539(x_1187: Any, xs_1188: list[Any]):
        _x_20536 = Stack_mk(None, xs_1188)
        _x_20537 = (x_1187, _x_20536)
        _x_20538 = _x_20537
        return _x_20538
    _alt_20540 = _f_20539
    _x_20541 = s_1185.stack_0
    if len(_x_20541) == 0:
        _x_20543 = _alt_20535()
        return _x_20543
    else:
        head_20544 = _x_20541[0]
        tail_20545 = _x_20541[1:]
        _x_20546 = _alt_20540(head_20544, tail_20545)
        return _x_20546

# Lean: Corpus.DataStructures.Stack.peek
def peek(__1189: Any, s_1190: Any) -> Any | None:
    _x_20549 = s_1190.stack_0
    _x_20550 = (lambda xs: xs[0] if xs else None)(_x_20549)
    return _x_20550

# Lean: Corpus.DataStructures.Stack.isEmpty
def stack_is_empty(__1191: Any, s_1192: Any) -> bool:
    _x_20552 = s_1192.stack_0
    _x_20553 = len(_x_20552) == 0
    return _x_20553

# Lean: Corpus.DataStructures.Stack.size
def stack_size(__1193: Any, s_1194: Any) -> int:
    _x_20555 = s_1194.stack_0
    _x_20556 = len(_x_20555)
    return _x_20556

# Lean: Corpus.DataStructures.Queue.empty
def queue_empty(__1195: Any) -> Any:
    _x_20558 = []
    _x_20559 = Queue_mk(None, _x_20558, _x_20558)
    return _x_20559

# Lean: Corpus.DataStructures.Queue.enqueue
def enqueue(__1196: Any, q_1197: Any, x_1198: Any) -> Any:
    _x_20561 = q_1197.queue_0
    _x_20562 = q_1197.queue_1
    _x_20563 = [x_1198] + _x_20562
    _x_20564 = Queue_mk(None, _x_20561, _x_20563)
    return _x_20564

# Lean: Corpus.DataStructures.Queue.dequeue
def dequeue(__1199: Any, q_1200: Any) -> tuple[Any, Any] | None:
    def _f_20570(x_1201: Any, xs_1202: list[Any]):
        _x_20566 = q_1200.queue_1
        _x_20567 = Queue_mk(None, xs_1202, _x_20566)
        _x_20568 = (x_1201, _x_20567)
        _x_20569 = _x_20568
        return _x_20569
    _alt_20571 = _f_20570
    def _f_20589():
        def _f_20573():
            _x_20572 = None
            return _x_20572
        _alt_20574 = _f_20573
        def _f_20579(x_1205: Any, xs_1206: list[Any]):
            _x_20575 = []
            _x_20576 = Queue_mk(None, xs_1206, _x_20575)
            _x_20577 = (x_1205, _x_20576)
            _x_20578 = _x_20577
            return _x_20578
        _alt_20580 = _f_20579
        _x_20581 = q_1200.queue_1
        _x_20582 = list(reversed(_x_20581))
        if len(_x_20582) == 0:
            _x_20584 = _alt_20574()
            return _x_20584
        else:
            head_20585 = _x_20582[0]
            tail_20586 = _x_20582[1:]
            _x_20587 = _alt_20580(head_20585, tail_20586)
            return _x_20587
    _alt_20590 = _f_20589
    _x_20591 = q_1200.queue_0
    if len(_x_20591) == 0:
        _x_20593 = _alt_20590()
        return _x_20593
    else:
        head_20594 = _x_20591[0]
        tail_20595 = _x_20591[1:]
        _x_20596 = _alt_20571(head_20594, tail_20595)
        return _x_20596

# Lean: Corpus.DataStructures.Queue.isEmpty
def queue_is_empty(__1207: Any, q_1208: Any) -> bool:
    def _f_20600():
        _x_20599 = False
        return False
    _alt_20601 = _f_20600
    def _f_20604():
        _x_20602 = q_1208.queue_1
        _x_20603 = len(_x_20602) == 0
        return _x_20603
    _alt_20605 = _f_20604
    _x_20606 = q_1208.queue_0
    _x_20607 = len(_x_20606) == 0
    if _x_20607:
        _x_20611 = _alt_20605()
        return _x_20611
    else:
        _x_20609 = _alt_20601()
        return _x_20609

# Lean: Corpus.DataStructures.Queue.size
def queue_size(__1211: Any, q_1212: Any) -> int:
    _x_20617 = q_1212.queue_0
    _x_20618 = len(_x_20617)
    _x_20619 = q_1212.queue_1
    _x_20620 = len(_x_20619)
    _x_20621 = _x_20618 + _x_20620
    return _x_20621

# Lean: Corpus.DataStructures.BinaryTree.singleton
def singleton(__1213: Any, x_1214: Any) -> Any:
    _x_20623 = BinaryTree_empty(None)
    _x_20624 = BinaryTree_node(None, x_1214, _x_20623, _x_20623)
    return _x_20624

# Lean: Corpus.DataStructures.BinaryTree.size
def binary_tree_size(__1215: Any, t_1216: Any) -> int:
    def _f_20629():
        _x_20626 = 0
        return 0
    _alt_20630 = _f_20629
    def _f_20642(a_20631: Any, l_1218: Any, r_1219: Any):
        _x_20635 = 1
        _x_20638 = binary_tree_size(None, l_1218)
        _x_20639 = 1 + _x_20638
        _x_20640 = binary_tree_size(None, r_1219)
        _x_20641 = _x_20639 + _x_20640
        return _x_20641
    _alt_20643 = _f_20642
    match t_1216:
        case BinaryTree_empty():
            _x_20645 = _alt_20630()
            return _x_20645
        case BinaryTree_node(a_20646, a_20647, a_20648):
            _x_20649 = _alt_20643(a_20646, a_20647, a_20648)
            return _x_20649

# Lean: Corpus.DataStructures.BinaryTree.height
def height(__1220: Any, t_1221: Any) -> int:
    def _f_20655():
        _x_20652 = 0
        return 0
    _alt_20656 = _f_20655
    def _f_20670(a_20657: Any, l_1223: Any, r_1224: Any):
        _x_20661 = 1
        _x_20665 = max
        _x_20666 = height(None, l_1223)
        _x_20667 = height(None, r_1224)
        _x_20668 = _x_20665(_x_20666, _x_20667)
        _x_20669 = 1 + _x_20668
        return _x_20669
    _alt_20671 = _f_20670
    match t_1221:
        case BinaryTree_empty():
            _x_20673 = _alt_20656()
            return _x_20673
        case BinaryTree_node(a_20674, a_20675, a_20676):
            _x_20677 = _alt_20671(a_20674, a_20675, a_20676)
            return _x_20677

# Lean: Corpus.DataStructures.BinaryTree.inorder
def inorder(__1225: Any, t_1226: Any) -> list[Any]:
    def _f_20681():
        _x_20680 = []
        return _x_20680
    _alt_20682 = _f_20681
    def _f_20692(v_1228: Any, l_1229: Any, r_1230: Any):
        _x_20686 = inorder(None, l_1229)
        _x_20687 = []
        _x_20688 = [v_1228] + _x_20687
        _x_20689 = _x_20686 + _x_20688
        _x_20690 = inorder(None, r_1230)
        _x_20691 = _x_20689 + _x_20690
        return _x_20691
    _alt_20693 = _f_20692
    match t_1226:
        case BinaryTree_empty():
            _x_20695 = _alt_20682()
            return _x_20695
        case BinaryTree_node(a_20696, a_20697, a_20698):
            _x_20699 = _alt_20693(a_20696, a_20697, a_20698)
            return _x_20699

# Lean: Corpus.DataStructures.BinaryTree.preorder
def preorder(__1231: Any, t_1232: Any) -> list[Any]:
    def _f_20703():
        _x_20702 = []
        return _x_20702
    _alt_20704 = _f_20703
    def _f_20714(v_1234: Any, l_1235: Any, r_1236: Any):
        _x_20708 = []
        _x_20709 = [v_1234] + _x_20708
        _x_20710 = preorder(None, l_1235)
        _x_20711 = _x_20709 + _x_20710
        _x_20712 = preorder(None, r_1236)
        _x_20713 = _x_20711 + _x_20712
        return _x_20713
    _alt_20715 = _f_20714
    match t_1232:
        case BinaryTree_empty():
            _x_20717 = _alt_20704()
            return _x_20717
        case BinaryTree_node(a_20718, a_20719, a_20720):
            _x_20721 = _alt_20715(a_20718, a_20719, a_20720)
            return _x_20721

# Lean: Corpus.DataStructures.BinaryTree.postorder
def postorder(__1237: Any, t_1238: Any) -> list[Any]:
    def _f_20725():
        _x_20724 = []
        return _x_20724
    _alt_20726 = _f_20725
    def _f_20736(v_1240: Any, l_1241: Any, r_1242: Any):
        _x_20730 = postorder(None, l_1241)
        _x_20731 = postorder(None, r_1242)
        _x_20732 = _x_20730 + _x_20731
        _x_20733 = []
        _x_20734 = [v_1240] + _x_20733
        _x_20735 = _x_20732 + _x_20734
        return _x_20735
    _alt_20737 = _f_20736
    match t_1238:
        case BinaryTree_empty():
            _x_20739 = _alt_20726()
            return _x_20739
        case BinaryTree_node(a_20740, a_20741, a_20742):
            _x_20743 = _alt_20737(a_20740, a_20741, a_20742)
            return _x_20743

# Lean: Corpus.DataStructures.BinaryTree.levelOrder
def level_order(__1243: Any, t_1244: Any) -> list[Any]:
    _x_20746 = []
    _x_20747 = [t_1244] + _x_20746
    _x_20748 = []
    _x_20749 = 10000
    _x_20752 = level_order_go(None, _x_20747, _x_20748, 10000)
    return _x_20752

# Lean: Corpus.DataStructures.BinaryTree.mirror
def mirror(__1245: Any, t_1246: Any) -> Any:
    def _f_20755():
        _x_20754 = BinaryTree_empty(None)
        return _x_20754
    _alt_20756 = _f_20755
    def _f_20760(v_1248: Any, l_1249: Any, r_1250: Any):
        _x_20757 = mirror(None, r_1250)
        _x_20758 = mirror(None, l_1249)
        _x_20759 = BinaryTree_node(None, v_1248, _x_20757, _x_20758)
        return _x_20759
    _alt_20761 = _f_20760
    match t_1246:
        case BinaryTree_empty():
            _x_20763 = _alt_20756()
            return _x_20763
        case BinaryTree_node(a_20764, a_20765, a_20766):
            _x_20767 = _alt_20761(a_20764, a_20765, a_20766)
            return _x_20767

# Lean: Corpus.DataStructures.BinaryTree.map
def binary_tree_map(__1251: Any, __1252: Any, f_1253: Callable[[Any], Any], t_1254: Any) -> Any:
    def _f_20771():
        _x_20770 = BinaryTree_empty(None)
        return _x_20770
    _alt_20772 = _f_20771
    def _f_20777(v_1256: Any, l_1257: Any, r_1258: Any):
        _x_20773 = f_1253(v_1256)
        _x_20774 = binary_tree_map(None, None, f_1253, l_1257)
        _x_20775 = binary_tree_map(None, None, f_1253, r_1258)
        _x_20776 = BinaryTree_node(None, _x_20773, _x_20774, _x_20775)
        return _x_20776
    _alt_20778 = _f_20777
    match t_1254:
        case BinaryTree_empty():
            _x_20780 = _alt_20772()
            return _x_20780
        case BinaryTree_node(a_20781, a_20782, a_20783):
            _x_20784 = _alt_20778(a_20781, a_20782, a_20783)
            return _x_20784

# Lean: Corpus.DataStructures.BinaryTree.fold
def binary_tree_fold(__1259: Any, __1260: Any, f_1261: Callable[[Any, Any], Any], init_1262: Any, t_1263: Any) -> Any:
    def _f_20787():
        return init_1262
    _alt_20788 = _f_20787
    def _f_20792(v_1265: Any, l_1266: Any, r_1267: Any):
        _x_20789 = binary_tree_fold(None, None, f_1261, init_1262, l_1266)
        _x_20790 = f_1261(_x_20789, v_1265)
        _x_20791 = binary_tree_fold(None, None, f_1261, _x_20790, r_1267)
        return _x_20791
    _alt_20793 = _f_20792
    match t_1263:
        case BinaryTree_empty():
            _x_20795 = _alt_20788()
            return _x_20795
        case BinaryTree_node(a_20796, a_20797, a_20798):
            _x_20799 = _alt_20793(a_20796, a_20797, a_20798)
            return _x_20799

# Lean: Corpus.DataStructures.AssocList.empty
def assoc_list_empty(__1268: Any, __1269: Any) -> list[tuple[Any, Any]]:
    _x_20802 = []
    return _x_20802

# Lean: Corpus.DataStructures.AssocList.insert
def assoc_list_insert(__1270: Any, __1271: Any, inst_20804: Any, m_1272: list[tuple[Any, Any]], k_1273: Any, v_1274: Any) -> list[tuple[Any, Any]]:
    _x_20805 = (k_1273, v_1274)
    def _f_20815(x_20806: tuple[Any, Any]):
        def _f_20809(k__1275: Any, snd_20807: Any):
            _x_20808 = (lambda a, b: a != b)(k_1273)
            return _x_20808
        _alt_20810 = _f_20809
        match x_20806:
            case (fst_20811, snd_20812):
                _x_20813 = _alt_20810(fst_20811, snd_20812)
                return _x_20813
    _x_20816 = [x for x in m_1272 if _f_20815(x)]
    _x_20817 = [_x_20805] + _x_20816
    return _x_20817

# Lean: Corpus.DataStructures.AssocList.lookup
def lookup(__1276: Any, __1277: Any, inst_20819: Any, m_1278: list[tuple[Any, Any]], k_1279: Any) -> Any | None:
    def _f_20821():
        _x_20820 = None
        return _x_20820
    _alt_20822 = _f_20821
    def _f_20832(k__1281: Any, v_1282: Any, rest_1283: list[tuple[Any, Any]]):
        _x_20823 = inst_20819.beq_0
        _x_20824 = _x_20823(k_1279, k__1281)
        _x_20825 = True
        if _x_20824:
            _x_20830 = v_1282
            return _x_20830
        else:
            _x_20828 = lookup(None, None, inst_20819, k_1279, rest_1283)
            return _x_20828
    _alt_20833 = _f_20832
    if len(m_1278) == 0:
        _x_20835 = _alt_20822()
        return _x_20835
    else:
        head_20836 = m_1278[0]
        tail_20837 = m_1278[1:]
        match head_20836:
            case (fst_20838, snd_20839):
                _x_20840 = _alt_20833(fst_20838, snd_20839, tail_20837)
                return _x_20840

# Lean: Corpus.DataStructures.AssocList.remove
def remove(__1284: Any, __1285: Any, inst_20844: Any, m_1286: list[tuple[Any, Any]], k_1287: Any) -> list[tuple[Any, Any]]:
    def _f_20854(x_20845: tuple[Any, Any]):
        def _f_20848(k__1288: Any, snd_20846: Any):
            _x_20847 = (lambda a, b: a != b)(k_1287)
            return _x_20847
        _alt_20849 = _f_20848
        match x_20845:
            case (fst_20850, snd_20851):
                _x_20852 = _alt_20849(fst_20850, snd_20851)
                return _x_20852
    _x_20855 = [x for x in m_1286 if _f_20854(x)]
    return _x_20855

# Lean: Corpus.DataStructures.AssocList.keys
def keys(__1289: Any, __1290: Any, m_1291: list[tuple[Any, Any]]) -> list[Any]:
    def _f_20858(self: tuple[Any, Any]):
        _x_20857 = self[0]
        return _x_20857
    _x_20859 = [_f_20858(x) for x in m_1291]
    return _x_20859

# Lean: Corpus.DataStructures.AssocList.values
def values(__1292: Any, __1293: Any, m_1294: list[tuple[Any, Any]]) -> list[Any]:
    def _f_20862(self_1295: tuple[Any, Any]):
        _x_20861 = self_1295[1]
        return _x_20861
    _x_20863 = [_f_20862(x) for x in m_1294]
    return _x_20863

# Lean: Corpus.DataStructures.AssocList.size
def assoc_list_size(__1296: Any, __1297: Any, m_1298: list[tuple[Any, Any]]) -> int:
    _x_20865 = len(m_1298)
    return _x_20865

# Lean: Corpus.DataStructures.Graph.empty
def data_structures_graph_empty(__1299: Any) -> Any:
    _x_20867 = []
    _x_20868 = []
    _x_20869 = Graph_mk(None, _x_20867, _x_20868)
    return _x_20869

# Lean: Corpus.DataStructures.Graph.addVertex
def data_structures_graph_add_vertex(__1300: Any, inst_20871: Any, g_1301: Any, v_1302: Any) -> Any:
    _x_20872 = g_1301.data_structures_graph_0
    _x_20873 = v_1302 in _x_20872
    _x_20874 = True
    if _x_20873:
        return g_1301
    else:
        _x_20877 = [v_1302] + _x_20872
        _x_20878 = g_1301.data_structures_graph_1
        _x_20879 = Graph_mk(None, _x_20877, _x_20878)
        return _x_20879

# Lean: Corpus.DataStructures.Graph.addEdge
def data_structures_graph_add_edge(__1303: Any, inst_20883: Any, g_1304: Any, u: Any, v_1305: Any) -> Any:
    _x_20884 = data_structures_graph_add_vertex(None, inst_20883, g_1304, u)
    _x_20885 = data_structures_graph_add_vertex(None, inst_20883, _x_20884, v_1305)
    _x_20886 = _x_20885.data_structures_graph_0
    _x_20887 = (u, v_1305)
    _x_20888 = _x_20885.data_structures_graph_1
    _x_20889 = [_x_20887] + _x_20888
    _x_20890 = Graph_mk(None, _x_20886, _x_20889)
    return _x_20890

# Lean: Corpus.DataStructures.Graph.neighbors
def data_structures_graph_neighbors(__1306: Any, inst_20892: Any, g_1307: Any, v_1308: Any) -> list[Any]:
    def _f_20915(x_20893: tuple[Any, Any]):
        def _f_20909(u_1309: Any, w_1310: Any):
            _x_20894 = inst_20892.beq_0
            _x_20895 = _x_20894(u_1309, v_1308)
            _x_20896 = True
            if _x_20895:
                _x_20907 = w_1310
                return _x_20907
            else:
                _x_20899 = _x_20894(w_1310, v_1308)
                if _x_20899:
                    _x_20904 = u_1309
                    return _x_20904
                else:
                    _x_20902 = None
                    return _x_20902
        _alt_20910 = _f_20909
        match x_20893:
            case (fst_20911, snd_20912):
                _x_20913 = _alt_20910(fst_20911, snd_20912)
                return _x_20913
    _x_20916 = g_1307.data_structures_graph_1
    _x_20917 = [y for x in _x_20916 if (y := _f_20915(x)) is not None]
    return _x_20917

# Lean: Corpus.DataStructures.Graph.degree
def degree(__1311: Any, inst_20919: Any, g_1312: Any, v_1313: Any) -> int:
    _x_20920 = data_structures_graph_neighbors(None, inst_20919, g_1312, v_1313)
    _x_20921 = len(_x_20920)
    return _x_20921

# Lean: Corpus.DataStructures.Graph.hasEdge
def has_edge(__1314: Any, inst_20923: Any, g_1315: Any, u_1316: Any, v_1317: Any) -> bool:
    _x_20924 = g_1315.data_structures_graph_1
    def _f_20977(x_20925: tuple[Any, Any]):
        def _f_20971(a_1318: Any, b_1319: Any):
            def _f_20927():
                _x_20926 = True
                return True
            _alt_20928 = _f_20927
            def _f_20943():
                def _f_20930():
                    _x_20929 = False
                    return False
                _alt_20931 = _f_20930
                def _f_20934():
                    _x_20932 = inst_20923.beq_0
                    _x_20933 = _x_20932(b_1319, u_1316)
                    return _x_20933
                _alt_20935 = _f_20934
                _x_20936 = inst_20923.beq_0
                _x_20937 = _x_20936(a_1318, v_1317)
                if _x_20937:
                    _x_20941 = _alt_20935()
                    return _x_20941
                else:
                    _x_20939 = _alt_20931()
                    return _x_20939
            _alt_20944 = _f_20943
            def _f_20946():
                _x_20945 = False
                return False
            _alt_20947 = _f_20946
            def _f_20950():
                _x_20948 = inst_20923.beq_0
                _x_20949 = _x_20948(b_1319, v_1317)
                return _x_20949
            _alt_20951 = _f_20950
            _x_20952 = inst_20923.beq_0
            _x_20953 = _x_20952(a_1318, u_1316)
            def _jp_20964(_y_20958: bool):
                if _y_20958:
                    _x_20962 = _alt_20928()
                    return _x_20962
                else:
                    _x_20960 = _alt_20944()
                    return _x_20960
            def _jp_20967():
                _x_20966 = _alt_20947()
                return _jp_20964(_x_20966)
            def _jp_20970():
                _x_20969 = _alt_20951()
                return _jp_20964(_x_20969)
            if _x_20953:
                return _jp_20970()
            else:
                return _jp_20967()
        _alt_20972 = _f_20971
        match x_20925:
            case (fst_20973, snd_20974):
                _x_20975 = _alt_20972(fst_20973, snd_20974)
                return _x_20975
    _x_20978 = any(_f_20977(x) for x in _x_20924)
    return _x_20978

# Lean: Corpus.DataStructures.Trie.empty
def trie_empty() -> Trie:
    _x_20980 = False
    _x_20981 = []
    _x_20982 = Trie_node(False, _x_20981)
    return _x_20982

# Lean: Corpus.DataStructures.Trie.insert
def trie_insert(t_1326: Trie, s_1327: str) -> Trie:
    _x_20983 = list(s_1327)
    _x_20984 = trie_insert_go(t_1326, _x_20983)
    return _x_20984

# Lean: Corpus.DataStructures.Trie.contains
def trie_contains(t_1328: Trie, s_1329: str) -> bool:
    _x_20986 = list(s_1329)
    _x_20987 = trie_contains_go(t_1328, _x_20986)
    return _x_20987

# Lean: Corpus.DataStructures.Trie.hasPrefix
def has_prefix(t_1330: Trie, pfx_1331: str) -> bool:
    _x_20989 = list(pfx_1331)
    _x_20990 = has_prefix_go(t_1330, _x_20989)
    return _x_20990

# Lean: Corpus.Advanced.Heap.empty
def advanced_heap_empty(__1332: Any) -> Any:
    _x_20992 = []
    _x_20993 = Heap_mk(None, _x_20992)
    return _x_20993

# Lean: Corpus.Advanced.Heap.isEmpty
def advanced_heap_is_empty(__1333: Any, h_1334: Any) -> bool:
    _x_20995 = h_1334.heap_0
    _x_20996 = len(_x_20995) == 0
    return _x_20996

# Lean: Corpus.Advanced.Heap.size
def advanced_heap_size(__1335: Any, h_1336: Any) -> int:
    _x_20998 = h_1336.heap_0
    _x_20999 = len(_x_20998)
    return _x_20999

# Lean: Corpus.Advanced.parent
def parent(i_1337: int) -> int:
    _x_21007 = 1
    _x_21010 = i_1337 - 1
    _x_21011 = 2
    _x_21014 = _x_21010 // 2
    return _x_21014

# Lean: Corpus.Advanced.leftChild
def left_child(i_1338: int) -> int:
    _x_21022 = 2
    _x_21025 = 2 * i_1338
    _x_21026 = 1
    _x_21029 = _x_21025 + 1
    return _x_21029

# Lean: Corpus.Advanced.rightChild
def right_child(i_1339: int) -> int:
    _x_21037 = 2
    _x_21040 = 2 * i_1339
    _x_21041 = _x_21040 + 2
    return _x_21041

# Lean: Corpus.Advanced.swapAt
def swap_at(__1340: Any, xs_1341: list[Any], i_1342: int, j_1343: int) -> list[Any]:
    def _f_21045(a_1344: Any, b_1345: Any):
        _x_21043 = xs_1341[:i_1342] + [b_1345] + xs_1341[i_1342+1:]
        _x_21044 = _x_21043[:j_1343] + [a_1344] + _x_21043[j_1343+1:]
        return _x_21044
    _alt_21046 = _f_21045
    def _f_21049(x_21047: Any | None, x_21048: Any | None):
        return xs_1341
    _alt_21050 = _f_21049
    _x_21051 = xs_1341[i_1342] if 0 <= i_1342 < len(xs_1341) else None
    if _x_21051 is None:
        _x_21052 = None
        _x_21053 = xs_1341[j_1343] if 0 <= j_1343 < len(xs_1341) else None
        _x_21054 = _alt_21050(_x_21052, _x_21053)
        return _x_21054
    else:
        val_21055 = _x_21051
        _x_21056 = xs_1341[j_1343] if 0 <= j_1343 < len(xs_1341) else None
        if _x_21056 is None:
            _x_21057 = val_21055
            _x_21058 = None
            _x_21059 = _alt_21050(_x_21057, _x_21058)
            return _x_21059
        else:
            val_21060 = _x_21056
            _x_21061 = _alt_21046(val_21055, val_21060)
            return _x_21061

# Lean: Corpus.Advanced.siftUp
def sift_up(__1346: Any, inst_21065: Any, xs_1347: list[Any], i_1348: int) -> list[Any]:
    _x_21068 = 0
    _x_21071 = i_1348 == 0
    _x_21072 = True
    if _x_21071:
        return xs_1347
    else:
        _x_21075 = parent(i_1348)
        def _f_21088(vi_1350: Any, vp: Any):
            _x_21078 = inst_21065.ord_0
            _x_21079 = _x_21078(vi_1350, vp)
            _x_21080 = -1
            _x_21081 = _x_21079 == _x_21080
            if _x_21081:
                _x_21085 = swap_at(None, xs_1347, i_1348, _x_21075)
                _x_21086 = sift_up(None, inst_21065, _x_21085, _x_21075)
                return _x_21086
            else:
                return xs_1347
        _alt_21089 = _f_21088
        def _f_21092(x_21090: Any | None, x_21091: Any | None):
            return xs_1347
        _alt_21093 = _f_21092
        _x_21094 = xs_1347[i_1348] if 0 <= i_1348 < len(xs_1347) else None
        if _x_21094 is None:
            _x_21095 = None
            _x_21096 = xs_1347[_x_21075] if 0 <= _x_21075 < len(xs_1347) else None
            _x_21097 = _alt_21093(_x_21095, _x_21096)
            return _x_21097
        else:
            val_21098 = _x_21094
            _x_21099 = xs_1347[_x_21075] if 0 <= _x_21075 < len(xs_1347) else None
            if _x_21099 is None:
                _x_21100 = val_21098
                _x_21101 = None
                _x_21102 = _alt_21093(_x_21100, _x_21101)
                return _x_21102
            else:
                val_21103 = _x_21099
                _x_21104 = _alt_21089(val_21098, val_21103)
                return _x_21104

# Lean: Corpus.Advanced.siftDown
def sift_down(__1351: Any, inst_21110: Any, xs_1352: list[Any], i_1353: int) -> list[Any]:
    _x_21111 = len(xs_1352)
    _x_21112 = left_child(i_1353)
    _x_21113 = right_child(i_1353)
    _x_21114 = _x_21111 <= _x_21112
    if _x_21114:
        return xs_1352
    else:
        _x_21116 = _x_21111 <= _x_21113
        def _jp_21182(_y_21149: int):
            def _f_21163(vi_1357: Any, vs_1358: Any):
                _x_21152 = inst_21110.ord_0
                _x_21153 = _x_21152(vs_1358, vi_1357)
                _x_21154 = -1
                _x_21155 = _x_21153 == _x_21154
                _x_21156 = True
                if _x_21155:
                    _x_21160 = swap_at(None, xs_1352, i_1353, _y_21149)
                    _x_21161 = sift_down(None, inst_21110, _x_21160, _y_21149)
                    return _x_21161
                else:
                    return xs_1352
            _alt_21164 = _f_21163
            def _f_21167(x_21165: Any | None, x_21166: Any | None):
                return xs_1352
            _alt_21168 = _f_21167
            _x_21169 = xs_1352[i_1353] if 0 <= i_1353 < len(xs_1352) else None
            if _x_21169 is None:
                _x_21170 = None
                _x_21171 = xs_1352[_y_21149] if 0 <= _y_21149 < len(xs_1352) else None
                _x_21172 = _alt_21168(_x_21170, _x_21171)
                return _x_21172
            else:
                val_21173 = _x_21169
                _x_21174 = xs_1352[_y_21149] if 0 <= _y_21149 < len(xs_1352) else None
                if _x_21174 is None:
                    _x_21175 = val_21173
                    _x_21176 = None
                    _x_21177 = _alt_21168(_x_21175, _x_21176)
                    return _x_21177
                else:
                    val_21178 = _x_21174
                    _x_21179 = _alt_21164(val_21173, val_21178)
                    return _x_21179
        if _x_21116:
            return _jp_21182(_x_21112)
        else:
            def _f_21129(vl: Any, vr: Any):
                _x_21120 = inst_21110.ord_0
                _x_21121 = _x_21120(vl, vr)
                _x_21122 = -1
                _x_21123 = _x_21121 == _x_21122
                _x_21124 = True
                if _x_21123:
                    return _x_21112
                else:
                    return _x_21113
            _alt_21130 = _f_21129
            def _jp_21190(_y_21187: Any, _y_21188: Any):
                _x_21189 = _alt_21130(_y_21187, _y_21188)
                return _jp_21182(_x_21189)
            def _f_21133(x_21131: Any | None, x_21132: Any | None):
                return _x_21112
            _alt_21134 = _f_21133
            def _jp_21186(_y_21183: Any | None, _y_21184: Any | None):
                _x_21185 = _alt_21134(_y_21183, _y_21184)
                return _jp_21182(_x_21185)
            _x_21135 = xs_1352[_x_21112] if 0 <= _x_21112 < len(xs_1352) else None
            if _x_21135 is None:
                _x_21136 = None
                _x_21137 = xs_1352[_x_21113] if 0 <= _x_21113 < len(xs_1352) else None
                return _jp_21186(_x_21136, _x_21137)
            else:
                val_21139 = _x_21135
                _x_21140 = xs_1352[_x_21113] if 0 <= _x_21113 < len(xs_1352) else None
                if _x_21140 is None:
                    _x_21141 = val_21139
                    _x_21142 = None
                    return _jp_21186(_x_21141, _x_21142)
                else:
                    val_21144 = _x_21140
                    return _jp_21190(val_21139, val_21144)

# Lean: Corpus.Advanced.Heap.insert
def advanced_heap_insert(__1359: Any, inst_21194: Any, h_1360: Any, x_1361: Any) -> Any:
    _x_21198 = h_1360.heap_0
    _x_21199 = []
    _x_21200 = [x_1361] + _x_21199
    _x_21201 = _x_21198 + _x_21200
    _x_21205 = len(_x_21201)
    _x_21206 = 1
    _x_21209 = _x_21205 - 1
    _x_21210 = sift_up(None, inst_21194, _x_21201, _x_21209)
    _x_21211 = Heap_mk(None, _x_21210)
    return _x_21211

# Lean: Corpus.Advanced.Heap.min
def advanced_heap_min(__1362: Any, h_1363: Any) -> Any | None:
    _x_21213 = h_1363.heap_0
    _x_21214 = (lambda xs: xs[0] if xs else None)(_x_21213)
    return _x_21214

# Lean: Corpus.Advanced.Heap.popMin
def pop_min(__1364: Any, inst_21216: Any, h_1365: Any) -> Any:
    def _f_21217():
        return h_1365
    _alt_21218 = _f_21217
    def _f_21222(head_21219: Any):
        _x_21220 = []
        _x_21221 = Heap_mk(None, _x_21220)
        return _x_21221
    _alt_21223 = _f_21222
    def _f_21244(head_21224: Any, rest_1367: list[Any]):
        def _f_21227():
            _x_21225 = []
            _x_21226 = Heap_mk(None, _x_21225)
            return _x_21226
        _alt_21228 = _f_21227
        def _f_21236(last: Any):
            _x_21229 = (lambda xs: xs[:-1])(rest_1367)
            _x_21230 = [last] + _x_21229
            _x_21231 = 0
            _x_21234 = sift_down(None, inst_21216, _x_21230, 0)
            _x_21235 = Heap_mk(None, _x_21234)
            return _x_21235
        _alt_21237 = _f_21236
        _x_21238 = (lambda xs: xs[-1] if xs else None)(rest_1367)
        if _x_21238 is None:
            _x_21240 = _alt_21228()
            return _x_21240
        else:
            val_21241 = _x_21238
            _x_21242 = _alt_21237(val_21241)
            return _x_21242
    _alt_21245 = _f_21244
    _x_21246 = h_1365.heap_0
    if len(_x_21246) == 0:
        _x_21248 = _alt_21218()
        return _x_21248
    else:
        head_21249 = _x_21246[0]
        tail_21250 = _x_21246[1:]
        if len(tail_21250) == 0:
            _x_21251 = _alt_21223(head_21249)
            return _x_21251
        else:
            head_21252 = tail_21250[0]
            tail_21253 = tail_21250[1:]
            _x_21254 = [head_21252] + tail_21253
            _x_21255 = _alt_21245(head_21249, _x_21254)
            return _x_21255

# Lean: Corpus.Advanced.Heap.ofList
def of_list(__1369: Any, inst_21259: Any, xs_1370: list[Any]) -> Any:
    def _f_21263(x1_21260: Any, x2_21261: Any):
        _x_21262 = advanced_heap_insert(None, inst_21259, x1_21260, x2_21261)
        return _x_21262
    _x_21264 = advanced_heap_empty(None)
    _x_21265 = functools.reduce(_f_21263, xs_1370, _x_21264)
    return _x_21265

# Lean: Corpus.Advanced.heapSort
def heap_sort(__1371: Any, inst_21267: Any, xs_1372: list[Any]) -> list[Any]:
    _x_21268 = of_list(None, inst_21267, xs_1372)
    _x_21269 = []
    _x_21273 = len(xs_1372)
    _x_21274 = 1
    _x_21277 = _x_21273 + 1
    _x_21278 = extract(None, inst_21267, _x_21268, _x_21269, _x_21277)
    return _x_21278

# Lean: Corpus.Advanced.UnionFind.empty
def advanced_union_find_empty() -> UnionFind:
    _x_21280 = []
    _x_21281 = UnionFind_mk(_x_21280, _x_21280)
    return _x_21281

# Lean: Corpus.Advanced.UnionFind.size
def advanced_union_find_size(uf: UnionFind) -> int:
    _x_21282 = uf.union_find_0
    _x_21283 = len(_x_21282)
    return _x_21283

# Lean: Corpus.Advanced.UnionFind.push
def advanced_union_find_push(uf_1373: UnionFind) -> UnionFind:
    _x_21285 = uf_1373.union_find_0
    _x_21286 = len(_x_21285)
    _x_21290 = []
    _x_21291 = [_x_21286] + _x_21290
    _x_21292 = _x_21285 + _x_21291
    _x_21293 = uf_1373.union_find_1
    _x_21294 = 0
    _x_21297 = [0] + _x_21290
    _x_21298 = _x_21293 + _x_21297
    _x_21299 = UnionFind_mk(_x_21292, _x_21298)
    return _x_21299

# Lean: Corpus.Advanced.UnionFind.ofSize
def of_size(n_1375: int) -> UnionFind:
    _x_21301 = list(range(n_1375))
    _x_21302 = 0
    _x_21305 = list_replicate(None, n_1375, 0)
    _x_21306 = UnionFind_mk(_x_21301, _x_21305)
    return _x_21306

# Lean: Corpus.Advanced.UnionFind.root
def root(uf_1376: UnionFind, i_1377: int) -> int:
    def _f_21308():
        return i_1377
    _alt_21309 = _f_21308
    def _f_21319(p_1379: int):
        _x_21312 = p_1379 == i_1377
        _x_21313 = True
        if _x_21312:
            return i_1377
        else:
            _x_21316 = root(uf_1376, p_1379)
            return _x_21316
    _alt_21320 = _f_21319
    _x_21321 = uf_1376.union_find_0
    _x_21322 = _x_21321[i_1377] if 0 <= i_1377 < len(_x_21321) else None
    if _x_21322 is None:
        _x_21324 = _alt_21309()
        return _x_21324
    else:
        val_21325 = _x_21322
        _x_21326 = _alt_21320(val_21325)
        return _x_21326

# Lean: Corpus.Advanced.UnionFind.equiv
def equiv(uf_1380: UnionFind, i_1381: int, j_1382: int) -> bool:
    _x_21331 = root(uf_1380, i_1381)
    _x_21332 = root(uf_1380, j_1382)
    _x_21333 = _x_21331 == _x_21332
    return _x_21333

# Lean: Corpus.Advanced.UnionFind.union
def union(uf_1383: UnionFind, i_1384: int, j_1385: int) -> UnionFind:
    _x_21335 = root(uf_1383, i_1384)
    _x_21336 = root(uf_1383, j_1385)
    _x_21339 = _x_21335 == _x_21336
    _x_21340 = True
    if _x_21339:
        return uf_1383
    else:
        def _f_21371(ranki: int, rankj: int):
            _x_21343 = ranki < rankj
            if _x_21343:
                _x_21366 = uf_1383.union_find_0
                _x_21367 = _x_21366[:_x_21335] + [_x_21336] + _x_21366[_x_21335+1:]
                _x_21368 = uf_1383.union_find_1
                _x_21369 = UnionFind_mk(_x_21367, _x_21368)
                return _x_21369
            else:
                _x_21345 = rankj < ranki
                if _x_21345:
                    _x_21360 = uf_1383.union_find_0
                    _x_21361 = _x_21360[:_x_21336] + [_x_21335] + _x_21360[_x_21336+1:]
                    _x_21362 = uf_1383.union_find_1
                    _x_21363 = UnionFind_mk(_x_21361, _x_21362)
                    return _x_21363
                else:
                    _x_21347 = uf_1383.union_find_0
                    _x_21348 = _x_21347[:_x_21336] + [_x_21335] + _x_21347[_x_21336+1:]
                    _x_21349 = uf_1383.union_find_1
                    _x_21353 = 1
                    _x_21356 = ranki + 1
                    _x_21357 = _x_21349[:_x_21335] + [_x_21356] + _x_21349[_x_21335+1:]
                    _x_21358 = UnionFind_mk(_x_21348, _x_21357)
                    return _x_21358
        _alt_21372 = _f_21371
        def _f_21375(x_21373: int | None, x_21374: int | None):
            return uf_1383
        _alt_21376 = _f_21375
        _x_21377 = uf_1383.union_find_1
        _x_21378 = _x_21377[_x_21335] if 0 <= _x_21335 < len(_x_21377) else None
        if _x_21378 is None:
            _x_21379 = None
            _x_21380 = _x_21377[_x_21336] if 0 <= _x_21336 < len(_x_21377) else None
            _x_21381 = _alt_21376(_x_21379, _x_21380)
            return _x_21381
        else:
            val_21382 = _x_21378
            _x_21383 = _x_21377[_x_21336] if 0 <= _x_21336 < len(_x_21377) else None
            if _x_21383 is None:
                _x_21384 = val_21382
                _x_21385 = None
                _x_21386 = _alt_21376(_x_21384, _x_21385)
                return _x_21386
            else:
                val_21387 = _x_21383
                _x_21388 = _alt_21372(val_21382, val_21387)
                return _x_21388

# Lean: Corpus.Advanced.UnionFind.numSets
def num_sets(uf_1386: UnionFind) -> int:
    def _f_21398(i_1387: int):
        _x_21396 = root(uf_1386, i_1387)
        _x_21397 = _x_21396 == i_1387
        return _x_21397
    _x_21399 = advanced_union_find_size(uf_1386)
    _x_21400 = list(range(_x_21399))
    _x_21401 = [x for x in _x_21400 if _f_21398(x)]
    _x_21402 = len(_x_21401)
    return _x_21402

# Lean: Corpus.Advanced.Graph.empty
def advanced_graph_empty() -> Graph:
    _x_21404 = 0
    _x_21407 = []
    _x_21408 = Graph_mk(0, _x_21407)
    return _x_21408

# Lean: Corpus.Advanced.Graph.addVertex
def advanced_graph_add_vertex(g_1388: Graph) -> Graph:
    _x_21412 = g_1388.advanced_graph_0
    _x_21413 = 1
    _x_21416 = _x_21412 + 1
    _x_21417 = g_1388.advanced_graph_1
    _x_21418 = Graph_mk(_x_21416, _x_21417)
    return _x_21418

# Lean: Corpus.Advanced.Graph.addEdge
def advanced_graph_add_edge(g_1389: Graph, u_1390: int, v_1391: int) -> Graph:
    _x_21420 = g_1389.advanced_graph_0
    _x_21421 = (u_1390, v_1391)
    _x_21422 = g_1389.advanced_graph_1
    _x_21423 = [_x_21421] + _x_21422
    _x_21424 = Graph_mk(_x_21420, _x_21423)
    return _x_21424

# Lean: Corpus.Advanced.Graph.neighbors
def advanced_graph_neighbors(g_1392: Graph, v_1393: int) -> list[int]:
    def _f_21449(x_21426: tuple[int, int]):
        def _f_21443(u_1394: int, w_1395: int):
            _x_21429 = u_1394 == v_1393
            _x_21430 = True
            if _x_21429:
                _x_21441 = w_1395
                return _x_21441
            else:
                _x_21433 = w_1395 == v_1393
                if _x_21433:
                    _x_21438 = u_1394
                    return _x_21438
                else:
                    _x_21436 = None
                    return _x_21436
        _alt_21444 = _f_21443
        match x_21426:
            case (fst_21445, snd_21446):
                _x_21447 = _alt_21444(fst_21445, snd_21446)
                return _x_21447
    _x_21450 = g_1392.advanced_graph_1
    _x_21451 = [y for x in _x_21450 if (y := _f_21449(x)) is not None]
    return _x_21451

# Lean: Corpus.Advanced.Graph.bfs
def bfs(g_1396: Graph, start_1397: int) -> list[int]:
    _x_21453 = []
    _x_21454 = [start_1397] + _x_21453
    _x_21458 = g_1396.advanced_graph_0
    _x_21459 = g_1396.advanced_graph_1
    _x_21460 = len(_x_21459)
    _x_21461 = _x_21458 + _x_21460
    _x_21462 = 1
    _x_21465 = _x_21461 + 1
    _x_21466 = bfs_loop(g_1396, _x_21454, _x_21453, _x_21465)
    return _x_21466

# Lean: Corpus.Advanced.Graph.dfs
def dfs(g_1398: Graph, start_1399: int) -> list[int]:
    _x_21468 = []
    _x_21469 = [start_1399] + _x_21468
    _x_21473 = g_1398.advanced_graph_0
    _x_21474 = g_1398.advanced_graph_1
    _x_21475 = len(_x_21474)
    _x_21476 = _x_21473 + _x_21475
    _x_21477 = 1
    _x_21480 = _x_21476 + 1
    _x_21481 = dfs_loop(g_1398, _x_21469, _x_21468, _x_21480)
    return _x_21481

# Lean: Corpus.Advanced.Graph.isConnected
def is_connected(g_1400: Graph) -> bool:
    _x_21485 = g_1400.advanced_graph_0
    _x_21486 = 0
    _x_21489 = _x_21485 == 0
    _x_21490 = True
    if _x_21489:
        return True
    else:
        _x_21493 = bfs(g_1400, 0)
        _x_21494 = len(_x_21493)
        _x_21495 = _x_21494 == _x_21485
        return _x_21495

# Lean: Corpus.Advanced.Graph.topoSort
def topo_sort(g_1402: Graph) -> list[int] | None:
    def _f_21508(v_1403: int):
        def _f_21504(x_21499: tuple[int, int]):
            _x_21502 = x_21499[1]
            _x_21503 = _x_21502 == v_1403
            return _x_21503
        _x_21505 = g_1402.advanced_graph_1
        _x_21506 = [x for x in _x_21505 if _f_21504(x)]
        _x_21507 = len(_x_21506)
        return _x_21507
    _x_21509 = g_1402.advanced_graph_0
    _x_21510 = list(range(_x_21509))
    _x_21511 = [_f_21508(x) for x in _x_21510]
    def _f_21532(v_1404: int):
        def _f_21512(x_1405: bool):
            return x_1405
        _alt_21513 = _f_21512
        def _f_21515():
            _x_21514 = False
            return False
        _alt_21516 = _f_21515
        def _f_21524(x_21517: int):
            _x_21520 = 0
            _x_21523 = x_21517 == 0
            return _x_21523
        _x_21525 = _x_21511[v_1404] if 0 <= v_1404 < len(_x_21511) else None
        _x_21526 = option_map(None, None, _f_21524, _x_21525)
        if _x_21526 is None:
            _x_21528 = _alt_21516()
            return _x_21528
        else:
            val_21529 = _x_21526
            _x_21530 = _alt_21513(val_21529)
            return _x_21530
    _x_21533 = [x for x in _x_21510 if _f_21532(x)]
    _x_21534 = []
    _x_21538 = 1
    _x_21541 = _x_21509 + 1
    _x_21542 = topo_sort_loop(g_1402, _x_21533, _x_21511, _x_21534, _x_21541)
    return _x_21542

# Lean: Corpus.Advanced.Graph.hasCycle
def has_cycle(g_1407: Graph) -> bool:
    _x_21544 = topo_sort(g_1407)
    _x_21545 = (lambda x: x is None)(_x_21544)
    return _x_21545

# Lean: Corpus.Advanced.Matrix.get
def advanced_matrix_get(m_1408: list[list[int]], i_1409: int, j_1410: int) -> int | None:
    def _f_21548():
        _x_21547 = None
        return _x_21547
    _alt_21549 = _f_21548
    def _f_21551(row_1412: list[int]):
        _x_21550 = row_1412[j_1410] if 0 <= j_1410 < len(row_1412) else None
        return _x_21550
    _alt_21552 = _f_21551
    _x_21553 = m_1408[i_1409] if 0 <= i_1409 < len(m_1408) else None
    if _x_21553 is None:
        _x_21555 = _alt_21549()
        return _x_21555
    else:
        val_21556 = _x_21553
        _x_21557 = _alt_21552(val_21556)
        return _x_21557

# Lean: Corpus.Advanced.Matrix.set
def advanced_matrix_set(m_1413: list[list[int]], i_1414: int, j_1415: int, v_1416: int) -> list[list[int]]:
    def _f_21590(x_21560: tuple[int, list[int]]):
        def _f_21584(idx_1417: int, row_1418: list[int]):
            _x_21563 = idx_1417 == i_1414
            _x_21564 = True
            if _x_21563:
                def _f_21580(x_21568: tuple[int, int]):
                    def _f_21574(jdx: int, val_1419: int):
                        _x_21569 = jdx == j_1415
                        if _x_21569:
                            return v_1416
                        else:
                            return val_1419
                    _alt_21575 = _f_21574
                    match x_21568:
                        case (fst_21576, snd_21577):
                            _x_21578 = _alt_21575(fst_21576, snd_21577)
                            return _x_21578
                _x_21581 = list(enumerate(row_1418))
                _x_21582 = [_f_21580(x) for x in _x_21581]
                return _x_21582
            else:
                return row_1418
        _alt_21585 = _f_21584
        match x_21560:
            case (fst_21586, snd_21587):
                _x_21588 = _alt_21585(fst_21586, snd_21587)
                return _x_21588
    _x_21591 = list(enumerate(m_1413))
    _x_21592 = [_f_21590(x) for x in _x_21591]
    return _x_21592

# Lean: Corpus.Advanced.Matrix.create
def advanced_matrix_create(n_1420: int, fill: int) -> list[list[int]]:
    _x_21594 = list_replicate(None, n_1420, fill)
    _x_21595 = list_replicate(None, n_1420, _x_21594)
    return _x_21595

# Lean: Corpus.Advanced.floydWarshall
def floyd_warshall(n_1421: int, edges: list[tuple[int, tuple[int, int]]]) -> list[list[int]]:
    _x_21597 = 1000000000
    _x_21600 = advanced_matrix_create(n_1421, 1000000000)
    def _f_21605(m_1424: list[list[int]], i_1425: int):
        _x_21601 = 0
        _x_21604 = advanced_matrix_set(m_1424, i_1425, i_1425, 0)
        return _x_21604
    _x_21606 = list(range(n_1421))
    _x_21607 = functools.reduce(_f_21605, _x_21606, _x_21600)
    def _f_21619(m_1426: list[list[int]], x_21608: tuple[int, tuple[int, int]]):
        def _f_21610(u_1427: int, v_1428: int, w_1429: int):
            _x_21609 = advanced_matrix_set(m_1426, u_1427, v_1428, w_1429)
            return _x_21609
        _alt_21611 = _f_21610
        match x_21608:
            case (fst_21612, snd_21613):
                match snd_21613:
                    case (fst_21614, snd_21615):
                        _x_21616 = _alt_21611(fst_21612, fst_21614, snd_21615)
                        return _x_21616
    _x_21620 = functools.reduce(_f_21619, edges, _x_21607)
    def _f_21663(dist: list[list[int]], k_1430: int):
        def _f_21661(d_1431: list[list[int]], i_1432: int):
            def _f_21659(d_: list[list[int]], j_1433: int):
                def _f_21630(dik: int, dkj: int, dij: int):
                    _x_21624 = dik + dkj
                    _x_21625 = _x_21624 < dij
                    if _x_21625:
                        _x_21628 = advanced_matrix_set(d_, i_1432, j_1433, _x_21624)
                        return _x_21628
                    else:
                        return d_
                _alt_21631 = _f_21630
                def _f_21635(x_21632: int | None, x_21633: int | None, x_21634: int | None):
                    return d_
                _alt_21636 = _f_21635
                _x_21637 = advanced_matrix_get(d_, i_1432, k_1430)
                if _x_21637 is None:
                    _x_21638 = None
                    _x_21639 = advanced_matrix_get(d_, k_1430, j_1433)
                    _x_21640 = advanced_matrix_get(d_, i_1432, j_1433)
                    _x_21641 = _alt_21636(_x_21638, _x_21639, _x_21640)
                    return _x_21641
                else:
                    val_21642 = _x_21637
                    _x_21643 = advanced_matrix_get(d_, k_1430, j_1433)
                    if _x_21643 is None:
                        _x_21644 = val_21642
                        _x_21645 = None
                        _x_21646 = advanced_matrix_get(d_, i_1432, j_1433)
                        _x_21647 = _alt_21636(_x_21644, _x_21645, _x_21646)
                        return _x_21647
                    else:
                        val_21648 = _x_21643
                        _x_21649 = advanced_matrix_get(d_, i_1432, j_1433)
                        if _x_21649 is None:
                            _x_21650 = val_21642
                            _x_21651 = val_21648
                            _x_21652 = None
                            _x_21653 = _alt_21636(_x_21650, _x_21651, _x_21652)
                            return _x_21653
                        else:
                            val_21654 = _x_21649
                            _x_21655 = _alt_21631(val_21642, val_21648, val_21654)
                            return _x_21655
            _x_21660 = functools.reduce(_f_21659, _x_21606, d_1431)
            return _x_21660
        _x_21662 = functools.reduce(_f_21661, _x_21606, dist)
        return _x_21662
    _x_21664 = functools.reduce(_f_21663, _x_21606, _x_21620)
    return _x_21664

# Lean: Corpus.NumberTheory.extGcd
def ext_gcd(a_1434: int, b_1435: int) -> tuple[int, tuple[int, int]]:
    _x_21668 = 0
    _x_21671 = b_1435 == 0
    _x_21672 = True
    if _x_21671:
        _x_21707 = 1
        _x_21712 = (1, a_1434)
        _x_21713 = (1, _x_21712)
        return _x_21713
    else:
        def _f_21692(x_1436: int, y_1437: int, g_1438: int):
            _x_21685 = cast(None, _x_21684, a_1434)
            _x_21686 = cast(None, _x_21684, b_1435)
            _x_21687 = _x_21685 // _x_21686
            _x_21688 = _x_21687 * y_1437
            _x_21689 = x_1436 - _x_21688
            _x_21690 = (_x_21689, g_1438)
            _x_21691 = (y_1437, _x_21690)
            return _x_21691
        _alt_21693 = _f_21692
        _x_21697 = a_1434 % b_1435
        _x_21698 = ext_gcd(b_1435, _x_21697)
        match _x_21698:
            case (fst_21699, snd_21700):
                match snd_21700:
                    case (fst_21701, snd_21702):
                        _x_21703 = _alt_21693(fst_21699, fst_21701, snd_21702)
                        return _x_21703

# Lean: Corpus.NumberTheory.modInverse
def mod_inverse(a_1439: int, m_1440: int) -> int | None:
    def _f_21742(x_1441: int, fst_21716: int, g_1442: int):
        _x_21719 = 1
        _x_21722 = g_1442 == 1
        _x_21723 = True
        if _x_21722:
            _x_21735 = cast(None, _x_21734, m_1440)
            _x_21736 = x_1441 % _x_21735
            _x_21737 = _x_21736 + _x_21735
            _x_21738 = _x_21737 % _x_21735
            _x_21739 = to_nat(_x_21738)
            _x_21740 = _x_21739
            return _x_21740
        else:
            _x_21726 = None
            return _x_21726
    _alt_21743 = _f_21742
    _x_21744 = ext_gcd(a_1439, m_1440)
    match _x_21744:
        case (fst_21745, snd_21746):
            match snd_21746:
                case (fst_21747, snd_21748):
                    _x_21749 = _alt_21743(fst_21745, fst_21747, snd_21748)
                    return _x_21749

# Lean: Corpus.NumberTheory.totient
def totient(n_1443: int) -> int:
    _x_21753 = 1
    _x_21756 = n_1443 <= 1
    if _x_21756:
        return n_1443
    else:
        _x_21758 = 0
        _x_21761 = count(n_1443, 1, 0)
        return _x_21761

# Lean: Corpus.NumberTheory.isPerfect
def is_perfect(n_1444: int) -> bool:
    _x_21765 = 2
    _x_21768 = n_1444 < 2
    if _x_21768:
        _x_21821 = False
        return False
    else:
        def _f_21811(acc_1445: int, i_1446: int):
            def _f_21771():
                _x_21770 = False
                return False
            _alt_21772 = _f_21771
            def _f_21783():
                _x_21778 = n_1444 % i_1446
                _x_21779 = 0
                _x_21782 = _x_21778 == 0
                return _x_21782
            _alt_21784 = _f_21783
            _x_21785 = 0
            _x_21788 = 0 < i_1446
            def _jp_21804(_y_21794: bool):
                _x_21795 = True
                if _y_21794:
                    _x_21802 = acc_1445 + i_1446
                    return _x_21802
                else:
                    return acc_1445
            def _jp_21807():
                _x_21806 = _alt_21772()
                return _jp_21804(_x_21806)
            def _jp_21810():
                _x_21809 = _alt_21784()
                return _jp_21804(_x_21809)
            if _x_21788:
                return _jp_21810()
            else:
                return _jp_21807()
        _x_21812 = 0
        _x_21815 = list(range(n_1444))
        _x_21816 = functools.reduce(_f_21811, _x_21815, 0)
        _x_21819 = _x_21816 == n_1444
        return _x_21819

# Lean: Corpus.NumberTheory.isAbundant
def is_abundant(n_1449: int) -> bool:
    _x_21824 = 2
    _x_21827 = n_1449 < 2
    if _x_21827:
        _x_21879 = False
        return False
    else:
        def _f_21870(acc_1450: int, i_1451: int):
            def _f_21830():
                _x_21829 = False
                return False
            _alt_21831 = _f_21830
            def _f_21842():
                _x_21837 = n_1449 % i_1451
                _x_21838 = 0
                _x_21841 = _x_21837 == 0
                return _x_21841
            _alt_21843 = _f_21842
            _x_21844 = 0
            _x_21847 = 0 < i_1451
            def _jp_21863(_y_21853: bool):
                _x_21854 = True
                if _y_21853:
                    _x_21861 = acc_1450 + i_1451
                    return _x_21861
                else:
                    return acc_1450
            def _jp_21869():
                _x_21868 = _alt_21843()
                return _jp_21863(_x_21868)
            def _jp_21866():
                _x_21865 = _alt_21831()
                return _jp_21863(_x_21865)
            if _x_21847:
                return _jp_21869()
            else:
                return _jp_21866()
        _x_21871 = 0
        _x_21874 = list(range(n_1449))
        _x_21875 = functools.reduce(_f_21870, _x_21874, 0)
        _x_21876 = n_1449 < _x_21875
        return _x_21876

# Lean: Corpus.NumberTheory.isDeficient
def is_deficient(n_1455: int) -> bool:
    _x_21882 = 1
    _x_21885 = n_1455 < 1
    if _x_21885:
        _x_21937 = False
        return False
    else:
        def _f_21928(acc_1456: int, i_1457: int):
            def _f_21888():
                _x_21887 = False
                return False
            _alt_21889 = _f_21888
            def _f_21900():
                _x_21895 = n_1455 % i_1457
                _x_21896 = 0
                _x_21899 = _x_21895 == 0
                return _x_21899
            _alt_21901 = _f_21900
            _x_21902 = 0
            _x_21905 = 0 < i_1457
            def _jp_21921(_y_21911: bool):
                _x_21912 = True
                if _y_21911:
                    _x_21919 = acc_1456 + i_1457
                    return _x_21919
                else:
                    return acc_1456
            def _jp_21927():
                _x_21926 = _alt_21901()
                return _jp_21921(_x_21926)
            def _jp_21924():
                _x_21923 = _alt_21889()
                return _jp_21921(_x_21923)
            if _x_21905:
                return _jp_21927()
            else:
                return _jp_21924()
        _x_21929 = 0
        _x_21932 = list(range(n_1455))
        _x_21933 = functools.reduce(_f_21928, _x_21932, 0)
        _x_21934 = _x_21933 < n_1455
        return _x_21934

# Lean: Corpus.NumberTheory.collatzLength
def collatz_length(n_1461: int) -> int:
    _x_21940 = 1
    _x_21943 = n_1461 <= 1
    if _x_21943:
        _x_21982 = 0
        return 0
    else:
        _x_21953 = 2
        _x_21956 = n_1461 % 2
        _x_21957 = 0
        _x_21960 = _x_21956 == 0
        _x_21961 = True
        def _jp_21980(_y_21977: int):
            _x_21978 = collatz_length(_y_21977)
            _x_21979 = 1 + _x_21978
            return _x_21979
        if _x_21960:
            _x_21976 = n_1461 // 2
            return _jp_21980(_x_21976)
        else:
            _x_21967 = 3
            _x_21970 = 3 * n_1461
            _x_21971 = _x_21970 + 1
            return _jp_21980(_x_21971)

# Lean: Corpus.NumberTheory.isqrt
def isqrt(n_1462: int) -> int:
    _x_21989 = 0
    _x_21992 = n_1462 == 0
    _x_21993 = True
    if _x_21992:
        return 0
    else:
        _x_21996 = isqrt_go(n_1462, n_1462, n_1462)
        return _x_21996

# Lean: Corpus.NumberTheory.isPerfectSquare
def is_perfect_square(n_1463: int) -> bool:
    _x_22000 = isqrt(n_1463)
    _x_22006 = _x_22000 * _x_22000
    _x_22007 = _x_22006 == n_1463
    return _x_22007

# Lean: Corpus.NumberTheory.digitalRoot
def digital_root(n_1465: int) -> int:
    _x_22009 = 10
    _x_22012 = n_1465 < 10
    if _x_22012:
        return n_1465
    else:
        _x_22014 = digit_sum(n_1465)
        _x_22015 = digital_root(_x_22014)
        return _x_22015

# Lean: Corpus.NumberTheory.isHarshad
def is_harshad(n_1466: int) -> bool:
    _x_22021 = 0
    _x_22024 = n_1466 == 0
    _x_22025 = True
    if _x_22024:
        _x_22047 = False
        return False
    else:
        _x_22028 = digit_sum(n_1466)
        def _f_22030():
            _x_22029 = False
            return False
        _alt_22031 = _f_22030
        def _f_22037():
            _x_22035 = n_1466 % _x_22028
            _x_22036 = _x_22035 == 0
            return _x_22036
        _alt_22038 = _f_22037
        _x_22039 = 0 < _x_22028
        if _x_22039:
            _x_22044 = _alt_22038()
            return _x_22044
        else:
            _x_22042 = _alt_22031()
            return _x_22042

# Lean: Corpus.NumberTheory.hammingWeight
def hamming_weight(n_1470: int) -> int:
    _x_22052 = 0
    _x_22055 = n_1470 == 0
    _x_22056 = True
    if _x_22055:
        return 0
    else:
        _x_22065 = 2
        _x_22068 = n_1470 % 2
        _x_22072 = n_1470 // 2
        _x_22073 = hamming_weight(_x_22072)
        _x_22074 = _x_22068 + _x_22073
        return _x_22074

# Lean: Corpus.NumberTheory.josephus
def josephus(n_1471: int, k_1472: int) -> int:
    _x_22080 = 1
    _x_22083 = n_1471 == 1
    _x_22084 = True
    if _x_22083:
        _x_22101 = 0
        return 0
    else:
        _x_22096 = n_1471 - 1
        _x_22097 = josephus(_x_22096, k_1472)
        _x_22098 = _x_22097 + k_1472
        _x_22099 = _x_22098 % n_1471
        return _x_22099

# Lean: Corpus.Geometry.dist2D
def dist2d(p1_1473: Point2D, p2_1474: Point2D) -> float:
    _x_22109 = p2_1474.point2d_0
    _x_22110 = p1_1473.point2d_0
    _x_22111 = _x_22109 - _x_22110
    _x_22112 = p2_1474.point2d_1
    _x_22113 = p1_1473.point2d_1
    _x_22114 = _x_22112 - _x_22113
    _x_22121 = _x_22111 * _x_22111
    _x_22122 = _x_22114 * _x_22114
    _x_22123 = _x_22121 + _x_22122
    _x_22124 = sqrt(_x_22123)
    return _x_22124

# Lean: Corpus.Geometry.dist3D
def dist3d(p1_1475: Point3D, p2_1476: Point3D) -> float:
    _x_22129 = p2_1476.point3d_0
    _x_22130 = p1_1475.point3d_0
    _x_22131 = _x_22129 - _x_22130
    _x_22132 = p2_1476.point3d_1
    _x_22133 = p1_1475.point3d_1
    _x_22134 = _x_22132 - _x_22133
    _x_22135 = p2_1476.point3d_2
    _x_22136 = p1_1475.point3d_2
    _x_22137 = _x_22135 - _x_22136
    _x_22144 = _x_22131 * _x_22131
    _x_22145 = _x_22134 * _x_22134
    _x_22146 = _x_22144 + _x_22145
    _x_22147 = _x_22137 * _x_22137
    _x_22148 = _x_22146 + _x_22147
    _x_22149 = sqrt(_x_22148)
    return _x_22149

# Lean: Corpus.Geometry.manhattan2D
def manhattan2d(p1_1479: Point2D, p2_1480: Point2D) -> float:
    _x_22157 = p2_1480.point2d_0
    _x_22158 = p1_1479.point2d_0
    _x_22159 = _x_22157 - _x_22158
    _x_22160 = float_abs(_x_22159)
    _x_22161 = p2_1480.point2d_1
    _x_22162 = p1_1479.point2d_1
    _x_22163 = _x_22161 - _x_22162
    _x_22164 = float_abs(_x_22163)
    _x_22165 = _x_22160 + _x_22164
    return _x_22165

# Lean: Corpus.Geometry.chebyshev2D
def chebyshev2d(p1_1481: Point2D, p2_1482: Point2D) -> float:
    _x_22168 = max
    _x_22172 = p2_1482.point2d_0
    _x_22173 = p1_1481.point2d_0
    _x_22174 = _x_22172 - _x_22173
    _x_22175 = float_abs(_x_22174)
    _x_22176 = p2_1482.point2d_1
    _x_22177 = p1_1481.point2d_1
    _x_22178 = _x_22176 - _x_22177
    _x_22179 = float_abs(_x_22178)
    _x_22180 = _x_22168(_x_22175, _x_22179)
    return _x_22180

# Lean: Corpus.Geometry.midpoint2D
def midpoint2d(p1_1483: Point2D, p2_1484: Point2D) -> Point2D:
    _x_22188 = p1_1483.point2d_0
    _x_22189 = p2_1484.point2d_0
    _x_22190 = _x_22188 + _x_22189
    _x_22191 = 2
    _x_22194 = _x_22190 // 2
    _x_22195 = p1_1483.point2d_1
    _x_22196 = p2_1484.point2d_1
    _x_22197 = _x_22195 + _x_22196
    _x_22198 = _x_22197 // 2
    _x_22199 = Point2D_mk(_x_22194, _x_22198)
    return _x_22199

# Lean: Corpus.Geometry.midpoint3D
def midpoint3d(p1_1485: Point3D, p2_1486: Point3D) -> Point3D:
    _x_22207 = p1_1485.point3d_0
    _x_22208 = p2_1486.point3d_0
    _x_22209 = _x_22207 + _x_22208
    _x_22210 = 2
    _x_22213 = _x_22209 // 2
    _x_22214 = p1_1485.point3d_1
    _x_22215 = p2_1486.point3d_1
    _x_22216 = _x_22214 + _x_22215
    _x_22217 = _x_22216 // 2
    _x_22218 = p1_1485.point3d_2
    _x_22219 = p2_1486.point3d_2
    _x_22220 = _x_22218 + _x_22219
    _x_22221 = _x_22220 // 2
    _x_22222 = Point3D_mk(_x_22213, _x_22217, _x_22221)
    return _x_22222

# Lean: Corpus.Geometry.dot2D
def dot2d(p1_1487: Point2D, p2_1488: Point2D) -> float:
    _x_22230 = p1_1487.point2d_0
    _x_22231 = p2_1488.point2d_0
    _x_22232 = _x_22230 * _x_22231
    _x_22233 = p1_1487.point2d_1
    _x_22234 = p2_1488.point2d_1
    _x_22235 = _x_22233 * _x_22234
    _x_22236 = _x_22232 + _x_22235
    return _x_22236

# Lean: Corpus.Geometry.dot3D
def dot3d(p1_1489: Point3D, p2_1490: Point3D) -> float:
    _x_22244 = p1_1489.point3d_0
    _x_22245 = p2_1490.point3d_0
    _x_22246 = _x_22244 * _x_22245
    _x_22247 = p1_1489.point3d_1
    _x_22248 = p2_1490.point3d_1
    _x_22249 = _x_22247 * _x_22248
    _x_22250 = _x_22246 + _x_22249
    _x_22251 = p1_1489.point3d_2
    _x_22252 = p2_1490.point3d_2
    _x_22253 = _x_22251 * _x_22252
    _x_22254 = _x_22250 + _x_22253
    return _x_22254

# Lean: Corpus.Geometry.cross2D
def cross2d(p1_1491: Point2D, p2_1492: Point2D) -> float:
    _x_22262 = p1_1491.point2d_0
    _x_22263 = p2_1492.point2d_1
    _x_22264 = _x_22262 * _x_22263
    _x_22265 = p1_1491.point2d_1
    _x_22266 = p2_1492.point2d_0
    _x_22267 = _x_22265 * _x_22266
    _x_22268 = _x_22264 - _x_22267
    return _x_22268

# Lean: Corpus.Geometry.cross3D
def cross3d(p1_1493: Point3D, p2_1494: Point3D) -> Point3D:
    _x_22276 = p1_1493.point3d_1
    _x_22277 = p2_1494.point3d_2
    _x_22278 = _x_22276 * _x_22277
    _x_22279 = p1_1493.point3d_2
    _x_22280 = p2_1494.point3d_1
    _x_22281 = _x_22279 * _x_22280
    _x_22282 = _x_22278 - _x_22281
    _x_22283 = p2_1494.point3d_0
    _x_22284 = _x_22279 * _x_22283
    _x_22285 = p1_1493.point3d_0
    _x_22286 = _x_22285 * _x_22277
    _x_22287 = _x_22284 - _x_22286
    _x_22288 = _x_22285 * _x_22280
    _x_22289 = _x_22276 * _x_22283
    _x_22290 = _x_22288 - _x_22289
    _x_22291 = Point3D_mk(_x_22282, _x_22287, _x_22290)
    return _x_22291

# Lean: Corpus.Geometry.magnitude2D
def magnitude2d(p_1495: Point2D) -> float:
    _x_22299 = p_1495.point2d_0
    _x_22300 = _x_22299 * _x_22299
    _x_22301 = p_1495.point2d_1
    _x_22302 = _x_22301 * _x_22301
    _x_22303 = _x_22300 + _x_22302
    _x_22304 = sqrt(_x_22303)
    return _x_22304

# Lean: Corpus.Geometry.magnitude3D
def magnitude3d(p_1496: Point3D) -> float:
    _x_22312 = p_1496.point3d_0
    _x_22313 = _x_22312 * _x_22312
    _x_22314 = p_1496.point3d_1
    _x_22315 = _x_22314 * _x_22314
    _x_22316 = _x_22313 + _x_22315
    _x_22317 = p_1496.point3d_2
    _x_22318 = _x_22317 * _x_22317
    _x_22319 = _x_22316 + _x_22318
    _x_22320 = sqrt(_x_22319)
    return _x_22320

# Lean: Corpus.Geometry.normalize2D
def normalize2d(p_1497: Point2D) -> Point2D:
    _x_22322 = magnitude2d(p_1497)
    _x_22325 = 0
    _x_22328 = _x_22322 == 0
    _x_22329 = True
    if _x_22328:
        return p_1497
    else:
        _x_22335 = p_1497.point2d_0
        _x_22336 = _x_22335 // _x_22322
        _x_22337 = p_1497.point2d_1
        _x_22338 = _x_22337 // _x_22322
        _x_22339 = Point2D_mk(_x_22336, _x_22338)
        return _x_22339

# Lean: Corpus.Geometry.normalize3D
def normalize3d(p_1499: Point3D) -> Point3D:
    _x_22343 = magnitude3d(p_1499)
    _x_22346 = 0
    _x_22349 = _x_22343 == 0
    _x_22350 = True
    if _x_22349:
        return p_1499
    else:
        _x_22356 = p_1499.point3d_0
        _x_22357 = _x_22356 // _x_22343
        _x_22358 = p_1499.point3d_1
        _x_22359 = _x_22358 // _x_22343
        _x_22360 = p_1499.point3d_2
        _x_22361 = _x_22360 // _x_22343
        _x_22362 = Point3D_mk(_x_22357, _x_22359, _x_22361)
        return _x_22362

# Lean: Corpus.Geometry.triangleArea
def triangle_area(p1_1501: Point2D, p2_1502: Point2D, p3_1503: Point2D) -> float:
    _x_22375 = p2_1502.point2d_0
    _x_22376 = p1_1501.point2d_0
    _x_22377 = _x_22375 - _x_22376
    _x_22378 = p3_1503.point2d_1
    _x_22379 = p1_1501.point2d_1
    _x_22380 = _x_22378 - _x_22379
    _x_22381 = _x_22377 * _x_22380
    _x_22382 = p3_1503.point2d_0
    _x_22383 = _x_22382 - _x_22376
    _x_22384 = p2_1502.point2d_1
    _x_22385 = _x_22384 - _x_22379
    _x_22386 = _x_22383 * _x_22385
    _x_22387 = _x_22381 - _x_22386
    _x_22388 = float_abs(_x_22387)
    _x_22389 = 2
    _x_22392 = _x_22388 // 2
    return _x_22392

# Lean: Corpus.Geometry.pointInTriangle
def point_in_triangle(p_1504: Point2D, p1_1505: Point2D, p2_1506: Point2D, p3_1507: Point2D) -> bool:
    _x_22394 = sign(p_1504, p1_1505, p2_1506)
    _x_22395 = sign(p_1504, p2_1506, p3_1507)
    _x_22396 = sign(p_1504, p3_1507, p1_1505)
    def _f_22398():
        _x_22397 = True
        return True
    _alt_22399 = _f_22398
    def _f_22405():
        _x_22400 = 0
        _x_22403 = float_dec_lt(_x_22396, 0)
        return _x_22403
    _alt_22406 = _f_22405
    _alt_22407 = _f_22398
    def _f_22413():
        _x_22408 = 0
        _x_22411 = float_dec_lt(_x_22395, 0)
        return _x_22411
    _alt_22414 = _f_22413
    _x_22415 = 0
    _x_22418 = float_dec_lt(_x_22394, 0)
    def _jp_22491(_y_22424: bool):
        def _jp_22484(_y_22429: bool):
            _alt_22430 = _f_22398
            def _f_22433():
                _x_22431 = float_dec_lt(0, _x_22396)
                return _x_22431
            _alt_22434 = _f_22433
            _alt_22435 = _f_22398
            def _f_22438():
                _x_22436 = float_dec_lt(0, _x_22395)
                return _x_22436
            _alt_22439 = _f_22438
            _x_22440 = float_dec_lt(0, _x_22394)
            def _jp_22477(_y_22446: bool):
                def _jp_22470(_y_22451: bool):
                    def _f_22453():
                        _x_22452 = False
                        return False
                    _alt_22454 = _f_22453
                    def _f_22455():
                        return _y_22451
                    _alt_22456 = _f_22455
                    def _jp_22463(_y_22461: bool):
                        _x_22462 = not _y_22461
                        return _x_22462
                    def _jp_22466():
                        _x_22465 = _alt_22454()
                        return _jp_22463(_x_22465)
                    def _jp_22469():
                        _x_22468 = _alt_22456()
                        return _jp_22463(_x_22468)
                    if _y_22429:
                        return _jp_22469()
                    else:
                        return _jp_22466()
                def _jp_22473():
                    _x_22472 = _alt_22434()
                    return _jp_22470(_x_22472)
                def _jp_22476():
                    _x_22475 = _alt_22430()
                    return _jp_22470(_x_22475)
                if _y_22446:
                    return _jp_22476()
                else:
                    return _jp_22473()
            def _jp_22480():
                _x_22479 = _alt_22439()
                return _jp_22477(_x_22479)
            def _jp_22483():
                _x_22482 = _alt_22435()
                return _jp_22477(_x_22482)
            if _x_22440:
                return _jp_22483()
            else:
                return _jp_22480()
        def _jp_22490():
            _x_22489 = _alt_22399()
            return _jp_22484(_x_22489)
        def _jp_22487():
            _x_22486 = _alt_22406()
            return _jp_22484(_x_22486)
        if _y_22424:
            return _jp_22490()
        else:
            return _jp_22487()
    def _jp_22497():
        _x_22496 = _alt_22407()
        return _jp_22491(_x_22496)
    def _jp_22494():
        _x_22493 = _alt_22414()
        return _jp_22491(_x_22493)
    if _x_22418:
        return _jp_22497()
    else:
        return _jp_22494()

# Lean: Corpus.Geometry.circleArea
def circle_area(radius: float) -> float:
    _x_22503 = _x_22502.of_scientific_0
    _x_22504 = 314159265358979
    _x_22505 = True
    _x_22506 = 14
    _x_22507 = _x_22503(_x_22504, True, _x_22506)
    _x_22508 = _x_22507 * radius
    _x_22509 = _x_22508 * radius
    return _x_22509

# Lean: Corpus.Geometry.circleCircumference
def circle_circumference(radius_1515: float) -> float:
    _x_22514 = 2
    _x_22518 = _x_22517.of_scientific_0
    _x_22519 = 314159265358979
    _x_22520 = True
    _x_22521 = 14
    _x_22522 = _x_22518(_x_22519, True, _x_22521)
    _x_22523 = 2 * _x_22522
    _x_22524 = _x_22523 * radius_1515
    return _x_22524

# Lean: Corpus.Geometry.sphereVolume
def sphere_volume(radius_1516: float) -> float:
    _x_22532 = 4
    _x_22535 = 3
    _x_22538 = 4 // 3
    _x_22540 = _x_22539.of_scientific_0
    _x_22541 = 314159265358979
    _x_22542 = True
    _x_22543 = 14
    _x_22544 = _x_22540(_x_22541, True, _x_22543)
    _x_22545 = _x_22538 * _x_22544
    _x_22546 = _x_22545 * radius_1516
    _x_22547 = _x_22546 * radius_1516
    _x_22548 = _x_22547 * radius_1516
    return _x_22548

# Lean: Corpus.Geometry.sphereSurfaceArea
def sphere_surface_area(radius_1517: float) -> float:
    _x_22553 = 4
    _x_22557 = _x_22556.of_scientific_0
    _x_22558 = 314159265358979
    _x_22559 = True
    _x_22560 = 14
    _x_22561 = _x_22557(_x_22558, True, _x_22560)
    _x_22562 = 4 * _x_22561
    _x_22563 = _x_22562 * radius_1517
    _x_22564 = _x_22563 * radius_1517
    return _x_22564

# Lean: Corpus.Geometry.rectangleArea
def rectangle_area(width: float, height: float) -> float:
    _x_22569 = width * height
    return _x_22569

# Lean: Corpus.Geometry.rectanglePerimeter
def rectangle_perimeter(width_1518: float, height_1519: float) -> float:
    _x_22574 = 2
    _x_22580 = width_1518 + height_1519
    _x_22581 = 2 * _x_22580
    return _x_22581

# Lean: Corpus.Geometry.polygonArea
def polygon_area(vertices: list[Point2D]) -> float:
    def _f_22586():
        _x_22583 = 0
        return 0
    _alt_22587 = _f_22586
    def _f_22592(head_22588: Point2D):
        _x_22589 = 0
        return 0
    _alt_22593 = _f_22592
    def _f_22599(first_1521: Point2D, rest_1522: list[Point2D]):
        _x_22594 = 0
        _x_22597 = polygon_area_go(rest_1522, first_1521, first_1521, 0)
        _x_22598 = float_abs(_x_22597)
        return _x_22598
    _alt_22600 = _f_22599
    if len(vertices) == 0:
        _x_22602 = _alt_22587()
        return _x_22602
    else:
        head_22603 = vertices[0]
        tail_22604 = vertices[1:]
        if len(tail_22604) == 0:
            _x_22605 = _alt_22593(head_22603)
            return _x_22605
        else:
            head_22606 = tail_22604[0]
            tail_22607 = tail_22604[1:]
            _x_22608 = [head_22606] + tail_22607
            _x_22609 = _alt_22600(head_22603, _x_22608)
            return _x_22609

# Lean: Corpus.Geometry.isConvexPolygon
def is_convex_polygon(vertices_1523: list[Point2D]) -> bool:
    def _f_22614():
        _x_22613 = True
        return True
    _alt_22615 = _f_22614
    def _f_22618(head_22616: Point2D):
        _x_22617 = True
        return True
    _alt_22619 = _f_22618
    def _f_22623(head_22620: Point2D, head_22621: Point2D):
        _x_22622 = True
        return True
    _alt_22624 = _f_22623
    def _f_22627(first_1525: Point2D, second_1526: Point2D, rest_1527: list[Point2D]):
        _x_22625 = None
        _x_22626 = is_convex_polygon_check(first_1525, second_1526, first_1525, second_1526, rest_1527, _x_22625)
        return _x_22626
    _alt_22628 = _f_22627
    if len(vertices_1523) == 0:
        _x_22630 = _alt_22615()
        return _x_22630
    else:
        head_22631 = vertices_1523[0]
        tail_22632 = vertices_1523[1:]
        if len(tail_22632) == 0:
            _x_22633 = _alt_22619(head_22631)
            return _x_22633
        else:
            head_22634 = tail_22632[0]
            tail_22635 = tail_22632[1:]
            if len(tail_22635) == 0:
                _x_22636 = _alt_22624(head_22631, head_22634)
                return _x_22636
            else:
                head_22637 = tail_22635[0]
                tail_22638 = tail_22635[1:]
                _x_22639 = [head_22637] + tail_22638
                _x_22640 = _alt_22628(head_22631, head_22634, _x_22639)
                return _x_22640

# Lean: Corpus.Geometry.orientation
def orientation(p_1528: Point2D, q_1529: Point2D, r_1530: Point2D) -> int:
    _x_22651 = q_1529.point2d_1
    _x_22652 = p_1528.point2d_1
    _x_22653 = _x_22651 - _x_22652
    _x_22654 = r_1530.point2d_0
    _x_22655 = q_1529.point2d_0
    _x_22656 = _x_22654 - _x_22655
    _x_22657 = _x_22653 * _x_22656
    _x_22658 = p_1528.point2d_0
    _x_22659 = _x_22655 - _x_22658
    _x_22660 = r_1530.point2d_1
    _x_22661 = _x_22660 - _x_22651
    _x_22662 = _x_22659 * _x_22661
    _x_22663 = _x_22657 - _x_22662
    _x_22666 = 0
    _x_22669 = _x_22663 == 0
    _x_22670 = True
    if _x_22669:
        return 0
    else:
        _x_22673 = float_dec_lt(0, _x_22663)
        if _x_22673:
            _x_22679 = 1
            return 1
        else:
            _x_22675 = 2
            return 2

# Lean: Corpus.Geometry.segmentsIntersect
def segments_intersect(p1_1532: Point2D, q1: Point2D, p2_1533: Point2D, q2: Point2D) -> bool:
    _x_22688 = orientation(p1_1532, q1, p2_1533)
    _x_22689 = orientation(p1_1532, q1, q2)
    _x_22690 = orientation(p2_1533, q2, p1_1532)
    _x_22691 = orientation(p2_1533, q2, q1)
    def _f_22693():
        _x_22692 = True
        return True
    _alt_22694 = _f_22693
    def _f_22712():
        def _f_22696():
            _x_22695 = False
            return False
        _alt_22697 = _f_22696
        def _f_22699():
            _x_22698 = on_segment(p2_1533, q1, q2)
            return _x_22698
        _alt_22700 = _f_22699
        _x_22703 = 0
        _x_22706 = _x_22691 == 0
        if _x_22706:
            _x_22710 = _alt_22700()
            return _x_22710
        else:
            _x_22708 = _alt_22697()
            return _x_22708
    _alt_22713 = _f_22712
    _alt_22714 = _f_22693
    def _f_22732():
        def _f_22716():
            _x_22715 = False
            return False
        _alt_22717 = _f_22716
        def _f_22719():
            _x_22718 = on_segment(p2_1533, p1_1532, q2)
            return _x_22718
        _alt_22720 = _f_22719
        _x_22723 = 0
        _x_22726 = _x_22690 == 0
        if _x_22726:
            _x_22730 = _alt_22720()
            return _x_22730
        else:
            _x_22728 = _alt_22717()
            return _x_22728
    _alt_22733 = _f_22732
    _alt_22734 = _f_22693
    def _f_22752():
        def _f_22736():
            _x_22735 = False
            return False
        _alt_22737 = _f_22736
        def _f_22739():
            _x_22738 = on_segment(p1_1532, q2, q1)
            return _x_22738
        _alt_22740 = _f_22739
        _x_22743 = 0
        _x_22746 = _x_22689 == 0
        if _x_22746:
            _x_22750 = _alt_22740()
            return _x_22750
        else:
            _x_22748 = _alt_22737()
            return _x_22748
    _alt_22753 = _f_22752
    _alt_22754 = _f_22693
    def _f_22772():
        def _f_22756():
            _x_22755 = False
            return False
        _alt_22757 = _f_22756
        def _f_22759():
            _x_22758 = on_segment(p1_1532, p2_1533, q1)
            return _x_22758
        _alt_22760 = _f_22759
        _x_22763 = 0
        _x_22766 = _x_22688 == 0
        if _x_22766:
            _x_22770 = _alt_22760()
            return _x_22770
        else:
            _x_22768 = _alt_22757()
            return _x_22768
    _alt_22773 = _f_22772
    def _f_22775():
        _x_22774 = False
        return False
    _alt_22776 = _f_22775
    def _f_22779():
        _x_22778 = (lambda a, b: a != b)(_x_22691)
        return _x_22778
    _alt_22780 = _f_22779
    _x_22782 = (lambda a, b: a != b)(_x_22689)
    def _jp_22829(_y_22787: bool):
        def _jp_22822(_y_22792: bool):
            def _jp_22815(_y_22797: bool):
                def _jp_22808(_y_22802: bool):
                    if _y_22802:
                        _x_22806 = _alt_22694()
                        return _x_22806
                    else:
                        _x_22804 = _alt_22713()
                        return _x_22804
                def _jp_22811():
                    _x_22810 = _alt_22733()
                    return _jp_22808(_x_22810)
                def _jp_22814():
                    _x_22813 = _alt_22714()
                    return _jp_22808(_x_22813)
                if _y_22797:
                    return _jp_22814()
                else:
                    return _jp_22811()
            def _jp_22818():
                _x_22817 = _alt_22753()
                return _jp_22815(_x_22817)
            def _jp_22821():
                _x_22820 = _alt_22734()
                return _jp_22815(_x_22820)
            if _y_22792:
                return _jp_22821()
            else:
                return _jp_22818()
        def _jp_22828():
            _x_22827 = _alt_22754()
            return _jp_22822(_x_22827)
        def _jp_22825():
            _x_22824 = _alt_22773()
            return _jp_22822(_x_22824)
        if _y_22787:
            return _jp_22828()
        else:
            return _jp_22825()
    def _jp_22835():
        _x_22834 = _alt_22780()
        return _jp_22829(_x_22834)
    def _jp_22832():
        _x_22831 = _alt_22776()
        return _jp_22829(_x_22831)
    if _x_22782:
        return _jp_22835()
    else:
        return _jp_22832()

# Lean: Corpus.Geometry.rotate2D
def rotate2d(p_1549: Point2D, angle: float) -> Point2D:
    _x_22837 = cos(angle)
    _x_22838 = sin(angle)
    _x_22845 = p_1549.point2d_0
    _x_22846 = _x_22845 * _x_22837
    _x_22847 = p_1549.point2d_1
    _x_22848 = _x_22847 * _x_22838
    _x_22849 = _x_22846 - _x_22848
    _x_22853 = _x_22845 * _x_22838
    _x_22854 = _x_22847 * _x_22837
    _x_22855 = _x_22853 + _x_22854
    _x_22856 = Point2D_mk(_x_22849, _x_22855)
    return _x_22856

# Lean: Corpus.Geometry.scale2D
def scale2d(p_1552: Point2D, factor: float) -> Point2D:
    _x_22861 = p_1552.point2d_0
    _x_22862 = _x_22861 * factor
    _x_22863 = p_1552.point2d_1
    _x_22864 = _x_22863 * factor
    _x_22865 = Point2D_mk(_x_22862, _x_22864)
    return _x_22865

# Lean: Corpus.Geometry.translate2D
def translate2d(p_1553: Point2D, dx_1554: float, dy_1555: float) -> Point2D:
    _x_22870 = p_1553.point2d_0
    _x_22871 = _x_22870 + dx_1554
    _x_22872 = p_1553.point2d_1
    _x_22873 = _x_22872 + dy_1555
    _x_22874 = Point2D_mk(_x_22871, _x_22873)
    return _x_22874

# Lean: Corpus.Geometry.reflectX
def reflect_x(p_1556: Point2D) -> Point2D:
    _x_22876 = p_1556.point2d_0
    _x_22879 = p_1556.point2d_1
    _x_22880 = -_x_22879
    _x_22881 = Point2D_mk(_x_22876, _x_22880)
    return _x_22881

# Lean: Corpus.Geometry.reflectY
def reflect_y(p_1557: Point2D) -> Point2D:
    _x_22885 = p_1557.point2d_0
    _x_22886 = -_x_22885
    _x_22887 = p_1557.point2d_1
    _x_22888 = Point2D_mk(_x_22886, _x_22887)
    return _x_22888

# Lean: Corpus.Geometry.angleBetween
def angle_between(v1: Point2D, v2: Point2D) -> float:
    _x_22890 = dot2d(v1, v2)
    _x_22891 = magnitude2d(v1)
    _x_22892 = magnitude2d(v2)
    def _f_22894():
        _x_22893 = True
        return True
    _alt_22895 = _f_22894
    def _f_22902():
        _x_22898 = 0
        _x_22901 = _x_22892 == 0
        return _x_22901
    _alt_22903 = _f_22902
    _x_22906 = 0
    _x_22909 = _x_22891 == 0
    def _jp_22929(_y_22914: bool):
        _x_22915 = True
        if _y_22914:
            return 0
        else:
            _x_22924 = _x_22891 * _x_22892
            _x_22925 = _x_22890 // _x_22924
            _x_22926 = acos(_x_22925)
            return _x_22926
    def _jp_22932():
        _x_22931 = _alt_22903()
        return _jp_22929(_x_22931)
    def _jp_22935():
        _x_22934 = _alt_22895()
        return _jp_22929(_x_22934)
    if _x_22909:
        return _jp_22935()
    else:
        return _jp_22932()

# Lean: Corpus.Geometry.projectOntoLine
def project_onto_line(p_1560: Point2D, a_1561: Point2D, b_1562: Point2D) -> Point2D:
    _x_22940 = p_1560.point2d_0
    _x_22941 = a_1561.point2d_0
    _x_22942 = _x_22940 - _x_22941
    _x_22943 = p_1560.point2d_1
    _x_22944 = a_1561.point2d_1
    _x_22945 = _x_22943 - _x_22944
    _x_22946 = Point2D_mk(_x_22942, _x_22945)
    _x_22947 = b_1562.point2d_0
    _x_22948 = _x_22947 - _x_22941
    _x_22949 = b_1562.point2d_1
    _x_22950 = _x_22949 - _x_22944
    _x_22951 = Point2D_mk(_x_22948, _x_22950)
    _x_22955 = dot2d(_x_22946, _x_22951)
    _x_22956 = dot2d(_x_22951, _x_22951)
    _x_22957 = _x_22955 // _x_22956
    _x_22964 = _x_22951.point2d_0
    _x_22965 = _x_22957 * _x_22964
    _x_22966 = _x_22941 + _x_22965
    _x_22967 = _x_22951.point2d_1
    _x_22968 = _x_22957 * _x_22967
    _x_22969 = _x_22944 + _x_22968
    _x_22970 = Point2D_mk(_x_22966, _x_22969)
    return _x_22970

# Lean: Corpus.Geometry.distanceToLine
def distance_to_line(p_1564: Point2D, a_1565: Point2D, b_1566: Point2D) -> float:
    _x_22972 = project_onto_line(p_1564, a_1565, b_1566)
    _x_22973 = dist2d(p_1564, _x_22972)
    return _x_22973

# Lean: Corpus.Combinatorics.doubleFactorial
def double_factorial(n_1567: int) -> int:
    _x_22975 = 1
    _x_22978 = n_1567 <= 1
    if _x_22978:
        return 1
    else:
        _x_22986 = 2
        _x_22989 = n_1567 - 2
        _x_22990 = double_factorial(_x_22989)
        _x_22991 = n_1567 * _x_22990
        return _x_22991

# Lean: Corpus.Combinatorics.risingFactorial
def rising_factorial(x_1568: int, n_1569: int) -> int:
    _x_22995 = 0
    _x_22998 = 1
    _x_23001 = rising_factorial_go(x_1568, n_1569, 0, 1)
    return _x_23001

# Lean: Corpus.Combinatorics.fallingFactorial
def falling_factorial(x_1570: int, n_1571: int) -> int:
    _x_23003 = 0
    _x_23006 = 1
    _x_23009 = falling_factorial_go(x_1570, n_1571, 0, 1)
    return _x_23009

# Lean: Corpus.Combinatorics.multinomial
def multinomial(n_1572: int, ks: list[int]) -> int:
    def _f_23017(x1_23011: int, x2_23012: int):
        _x_23016 = x1_23011 + x2_23012
        return _x_23016
    _x_23018 = 0
    _x_23021 = functools.reduce(_f_23017, ks, 0)
    _x_23023 = (lambda a, b: a != b)(n_1572)
    _x_23024 = True
    if _x_23023:
        return 0
    else:
        _x_23027 = factorial(n_1572)
        def _f_23033(acc_1574: int, k_1575: int):
            _x_23031 = factorial(k_1575)
            _x_23032 = acc_1574 * _x_23031
            return _x_23032
        _x_23034 = 1
        _x_23037 = functools.reduce(_f_23033, ks, 1)
        _x_23041 = _x_23027 // _x_23037
        return _x_23041

# Lean: Corpus.Combinatorics.stirling1
def stirling1(n_1577: int, k_1578: int) -> int:
    _x_23047 = 0
    _x_23050 = k_1578 == 0
    _x_23051 = True
    if _x_23050:
        _x_23078 = n_1577 == 0
        if _x_23078:
            _x_23082 = 1
            return 1
        else:
            return 0
    else:
        _x_23054 = n_1577 == 0
        if _x_23054:
            return 0
        else:
            _x_23066 = 1
            _x_23069 = n_1577 - 1
            _x_23070 = stirling1(_x_23069, k_1578)
            _x_23071 = _x_23069 * _x_23070
            _x_23072 = k_1578 - 1
            _x_23073 = stirling1(_x_23069, _x_23072)
            _x_23074 = _x_23071 + _x_23073
            return _x_23074

# Lean: Corpus.Combinatorics.stirling2
def stirling2(n_1579: int, k_1580: int) -> int:
    _x_23090 = 0
    _x_23093 = k_1580 == 0
    _x_23094 = True
    if _x_23093:
        _x_23121 = n_1579 == 0
        if _x_23121:
            _x_23125 = 1
            return 1
        else:
            return 0
    else:
        _x_23097 = n_1579 == 0
        if _x_23097:
            return 0
        else:
            _x_23109 = 1
            _x_23112 = n_1579 - 1
            _x_23113 = stirling2(_x_23112, k_1580)
            _x_23114 = k_1580 * _x_23113
            _x_23115 = k_1580 - 1
            _x_23116 = stirling2(_x_23112, _x_23115)
            _x_23117 = _x_23114 + _x_23116
            return _x_23117

# Lean: Corpus.Combinatorics.bell
def bell(n_1581: int) -> int:
    _x_23131 = 0
    _x_23134 = bell_go(n_1581, 0, 0)
    return _x_23134

# Lean: Corpus.Combinatorics.catalan
def catalan(n_1582: int) -> int:
    _x_23142 = 2
    _x_23145 = 2 * n_1582
    _x_23146 = binomial(_x_23145, n_1582)
    _x_23150 = 1
    _x_23153 = n_1582 + 1
    _x_23154 = _x_23146 // _x_23153
    return _x_23154

# Lean: Corpus.Combinatorics.derangement
def derangement(n_1583: int) -> int:
    _x_23158 = 0
    _x_23161 = n_1583 == 0
    _x_23162 = True
    if _x_23161:
        _x_23192 = 1
        return 1
    else:
        _x_23165 = 1
        _x_23168 = n_1583 == 1
        if _x_23168:
            return 0
        else:
            _x_23177 = n_1583 - 1
            _x_23181 = derangement(_x_23177)
            _x_23182 = 2
            _x_23185 = n_1583 - 2
            _x_23186 = derangement(_x_23185)
            _x_23187 = _x_23181 + _x_23186
            _x_23188 = _x_23177 * _x_23187
            return _x_23188

# Lean: Corpus.Combinatorics.partitionCount
def partition_count(n_1584: int) -> int:
    _x_23197 = p(n_1584, n_1584)
    return _x_23197

# Lean: Corpus.Combinatorics.permutations
def permutations(__1585: Any, inst_23199: Any, xs_1586: list[Any]) -> list[list[Any]]:
    def _f_23203():
        _x_23200 = []
        _x_23201 = []
        _x_23202 = [_x_23200] + _x_23201
        return _x_23202
    _alt_23204 = _f_23203
    def _f_23209(x_1588: Any):
        _x_23205 = []
        _x_23206 = [x_1588] + _x_23205
        _x_23207 = []
        _x_23208 = [_x_23206] + _x_23207
        return _x_23208
    _alt_23210 = _f_23209
    def _f_23223(x_23211: list[Any]):
        def _f_23221(x_1589: Any):
            def _f_23214(x_23212: list[Any]):
                _x_23213 = [x_1589] + x_23212
                return _x_23213
            def _f_23217(x_23215: Any):
                _x_23216 = (lambda a, b: a != b)(x_1589)
                return _x_23216
            _x_23218 = [x for x in xs_1586 if _f_23217(x)]
            _x_23219 = permutations(None, inst_23199, _x_23218)
            _x_23220 = [_f_23214(x) for x in _x_23219]
            return _x_23220
        _x_23222 = [y for x in xs_1586 for y in _f_23221(x)]
        return _x_23222
    _alt_23224 = _f_23223
    if len(xs_1586) == 0:
        _x_23226 = _alt_23204()
        return _x_23226
    else:
        head_23227 = xs_1586[0]
        tail_23228 = xs_1586[1:]
        if len(tail_23228) == 0:
            _x_23229 = _alt_23210(head_23227)
            return _x_23229
        else:
            head_23230 = tail_23228[0]
            tail_23231 = tail_23228[1:]
            _x_23232 = [head_23230] + tail_23231
            _x_23233 = [head_23227] + _x_23232
            _x_23234 = _alt_23224(_x_23233)
            return _x_23234

# Lean: Corpus.Combinatorics.combinations
def combinations(__1590: Any, k_1591: int, xs_1592: list[Any]) -> list[list[Any]]:
    _x_23240 = 0
    _x_23243 = k_1591 == 0
    _x_23244 = True
    if _x_23243:
        _x_23276 = []
        _x_23277 = []
        _x_23278 = [_x_23276] + _x_23277
        return _x_23278
    else:
        def _f_23248():
            _x_23247 = []
            return _x_23247
        _alt_23249 = _f_23248
        def _f_23267(x_1594: Any, rest_1595: list[Any]):
            def _f_23255(x_23253: list[Any]):
                _x_23254 = [x_1594] + x_23253
                return _x_23254
            _x_23259 = 1
            _x_23262 = k_1591 - 1
            _x_23263 = combinations(None, _x_23262, rest_1595)
            _x_23264 = [_f_23255(x) for x in _x_23263]
            _x_23265 = combinations(None, k_1591, rest_1595)
            _x_23266 = _x_23264 + _x_23265
            return _x_23266
        _alt_23268 = _f_23267
        if len(xs_1592) == 0:
            _x_23270 = _alt_23249()
            return _x_23270
        else:
            head_23271 = xs_1592[0]
            tail_23272 = xs_1592[1:]
            _x_23273 = _alt_23268(head_23271, tail_23272)
            return _x_23273

# Lean: Corpus.Combinatorics.powerSet
def power_set(__1596: Any, xs_1597: list[Any]) -> list[list[Any]]:
    def _f_23284():
        _x_23281 = []
        _x_23282 = []
        _x_23283 = [_x_23281] + _x_23282
        return _x_23283
    _alt_23285 = _f_23284
    def _f_23295(x_1599: Any, rest_1600: list[Any]):
        _x_23286 = power_set(None, rest_1600)
        def _f_23292(x_23290: list[Any]):
            _x_23291 = [x_1599] + x_23290
            return _x_23291
        _x_23293 = [_f_23292(x) for x in _x_23286]
        _x_23294 = _x_23286 + _x_23293
        return _x_23294
    _alt_23296 = _f_23295
    if len(xs_1597) == 0:
        _x_23298 = _alt_23285()
        return _x_23298
    else:
        head_23299 = xs_1597[0]
        tail_23300 = xs_1597[1:]
        _x_23301 = _alt_23296(head_23299, tail_23300)
        return _x_23301

# Lean: Corpus.Combinatorics.countInversions
def count_inversions(xs_1601: list[int]) -> int:
    _x_23304 = count(xs_1601)
    return _x_23304

# Lean: Corpus.Combinatorics.isEvenPermutation
def is_even_permutation(xs_1602: list[int]) -> bool:
    _x_23311 = count_inversions(xs_1602)
    _x_23312 = 2
    _x_23315 = _x_23311 % 2
    _x_23316 = 0
    _x_23319 = _x_23315 == 0
    return _x_23319

# Lean: Corpus.Combinatorics.lehmerCode
def lehmer_code(perm_1603: list[int]) -> list[int]:
    _x_23321 = []
    _x_23322 = lehmer_code_go(perm_1603, _x_23321)
    return _x_23322

# Lean: Corpus.Combinatorics.fromLehmerCode
def from_lehmer_code(code_1604: list[int]) -> list[int]:
    _x_23324 = len(code_1604)
    _x_23325 = list(range(_x_23324))
    _x_23326 = []
    _x_23327 = from_lehmer_code_go(code_1604, _x_23325, _x_23326)
    return _x_23327

# Lean: Corpus.Combinatorics.nthPermutation
def nth_permutation(n_1606: int, k_1607: int) -> list[int]:
    _x_23329 = list(range(n_1606))
    _x_23330 = []
    _x_23331 = nth_permutation_go(k_1607, n_1606, _x_23329, _x_23330)
    return _x_23331

# Lean: Corpus.Combinatorics.permutationRank
def permutation_rank(perm_1608: list[int]) -> int:
    _x_23333 = lehmer_code(perm_1608)
    _x_23334 = len(_x_23333)
    _x_23335 = 0
    _x_23338 = permutation_rank_go(_x_23334, _x_23333, 0, 0)
    return _x_23338

# Lean: Corpus.Combinatorics.nextPermutation
def next_permutation(perm_1611: list[int]) -> list[int] | None:
    _x_23340 = list(perm_1611)
    _x_23341 = len(_x_23340)
    def _f_23343():
        _x_23342 = None
        return _x_23342
    _alt_23344 = _f_23343
    def _f_23357(i_1615: int):
        _x_23345 = find_j(_x_23340, i_1615, _x_23341)
        _x_23346 = swap_(None, _x_23340, i_1615, _x_23345)
        _x_23350 = 1
        _x_23353 = i_1615 + 1
        _x_23354 = reverse_from(_x_23346, _x_23353)
        _x_23355 = list(_x_23354)
        _x_23356 = _x_23355
        return _x_23356
    _alt_23358 = _f_23357
    _x_23362 = 1
    _x_23365 = _x_23341 - 1
    _x_23366 = find_i(_x_23340, _x_23365)
    if _x_23366 is None:
        _x_23368 = _alt_23344()
        return _x_23368
    else:
        val_23369 = _x_23366
        _x_23370 = _alt_23358(val_23369)
        return _x_23370

# Lean: Corpus.Combinatorics.prevPermutation
def prev_permutation(perm_1619: list[int]) -> list[int] | None:
    _x_23373 = list(perm_1619)
    _x_23374 = len(_x_23373)
    def _f_23376():
        _x_23375 = None
        return _x_23375
    _alt_23377 = _f_23376
    def _f_23390(i_1623: int):
        _x_23378 = find_j(_x_23373, i_1623, _x_23374)
        _x_23379 = swap_(None, _x_23373, i_1623, _x_23378)
        _x_23383 = 1
        _x_23386 = i_1623 + 1
        _x_23387 = reverse_from(_x_23379, _x_23386)
        _x_23388 = list(_x_23387)
        _x_23389 = _x_23388
        return _x_23389
    _alt_23391 = _f_23390
    _x_23395 = 1
    _x_23398 = _x_23374 - 1
    _x_23399 = find_i(_x_23373, _x_23398)
    if _x_23399 is None:
        _x_23401 = _alt_23377()
        return _x_23401
    else:
        val_23402 = _x_23399
        _x_23403 = _alt_23391(val_23402)
        return _x_23403

# Lean: Corpus.Combinatorics.compositions
def compositions(n_1627: int) -> list[list[int]]:
    _x_23408 = 0
    _x_23411 = n_1627 == 0
    _x_23412 = True
    if _x_23411:
        _x_23421 = []
        _x_23422 = []
        _x_23423 = [_x_23421] + _x_23422
        return _x_23423
    else:
        _x_23415 = 1
        _x_23418 = []
        _x_23419 = compositions_go(n_1627, 1, _x_23418)
        return _x_23419

# Lean: Corpus.Combinatorics.integerPartitions
def integer_partitions(n_1628: int) -> list[list[int]]:
    _x_23426 = integer_partitions_go(n_1628, n_1628)
    return _x_23426

# Lean: Corpus.Sequences.fibonacci
def sequences_fibonacci(n_1629: int) -> int:
    _x_23428 = 0
    _x_23431 = 1
    _x_23434 = sequences_fibonacci_go(n_1629, 0, 1)
    return _x_23434

# Lean: Corpus.Sequences.lucas
def lucas(n_1630: int) -> int:
    _x_23436 = 2
    _x_23439 = 1
    _x_23442 = lucas_go(n_1630, 2, 1)
    return _x_23442

# Lean: Corpus.Sequences.tribonacci
def tribonacci(n_1631: int) -> int:
    _x_23444 = 0
    _x_23447 = 1
    _x_23450 = tribonacci_go(n_1631, 0, 0, 1)
    return _x_23450

# Lean: Corpus.Sequences.pell
def pell(n_1632: int) -> int:
    _x_23452 = 0
    _x_23455 = 1
    _x_23458 = pell_go(n_1632, 0, 1)
    return _x_23458

# Lean: Corpus.Sequences.padovan
def padovan(n_1633: int) -> int:
    _x_23460 = 1
    _x_23463 = padovan_go(n_1633, 1, 1, 1)
    return _x_23463

# Lean: Corpus.Sequences.perrin
def perrin(n_1634: int) -> int:
    _x_23465 = 3
    _x_23468 = 0
    _x_23471 = 2
    _x_23474 = perrin_go(n_1634, 3, 0, 2)
    return _x_23474

# Lean: Corpus.Sequences.jacobsthal
def jacobsthal(n_1635: int) -> int:
    _x_23476 = 0
    _x_23479 = 1
    _x_23482 = jacobsthal_go(n_1635, 0, 1)
    return _x_23482

# Lean: Corpus.Sequences.motzkin
def motzkin(n_1636: int) -> int:
    _x_23486 = 0
    _x_23489 = n_1636 == 0
    _x_23490 = True
    if _x_23489:
        _x_23512 = 1
        return 1
    else:
        _x_23493 = 1
        _x_23496 = n_1636 == 1
        if _x_23496:
            return 1
        else:
            _x_23505 = n_1636 - 1
            _x_23506 = motzkin(_x_23505)
            _x_23507 = motzkin_go(n_1636, 0, 0)
            _x_23508 = _x_23506 + _x_23507
            return _x_23508

# Lean: Corpus.Sequences.narayana
def narayana(n_1637: int, k_1638: int) -> int:
    def _f_23518():
        _x_23517 = True
        return True
    _alt_23519 = _f_23518
    def _f_23522():
        _x_23520 = n_1637 < k_1638
        return _x_23520
    _alt_23523 = _f_23522
    _x_23526 = 0
    _x_23529 = k_1638 == 0
    def _jp_23557(_y_23534: bool):
        _x_23535 = True
        if _y_23534:
            return 0
        else:
            _x_23544 = binomial(n_1637, k_1638)
            _x_23548 = 1
            _x_23551 = k_1638 - 1
            _x_23552 = binomial(n_1637, _x_23551)
            _x_23553 = _x_23544 * _x_23552
            _x_23554 = _x_23553 // n_1637
            return _x_23554
    def _jp_23560():
        _x_23559 = _alt_23523()
        return _jp_23557(_x_23559)
    def _jp_23563():
        _x_23562 = _alt_23519()
        return _jp_23557(_x_23562)
    if _x_23529:
        return _jp_23563()
    else:
        return _jp_23560()

# Lean: Corpus.Sequences.triangular
def triangular(n_1641: int) -> int:
    _x_23574 = 1
    _x_23577 = n_1641 + 1
    _x_23578 = n_1641 * _x_23577
    _x_23579 = 2
    _x_23582 = _x_23578 // 2
    return _x_23582

# Lean: Corpus.Sequences.square
def square(n_1642: int) -> int:
    _x_23587 = n_1642 * n_1642
    return _x_23587

# Lean: Corpus.Sequences.pentagonal
def pentagonal(n_1643: int) -> int:
    _x_23598 = 3
    _x_23601 = 3 * n_1643
    _x_23602 = 1
    _x_23605 = _x_23601 - 1
    _x_23606 = n_1643 * _x_23605
    _x_23607 = 2
    _x_23610 = _x_23606 // 2
    return _x_23610

# Lean: Corpus.Sequences.hexagonal
def hexagonal(n_1644: int) -> int:
    _x_23618 = 2
    _x_23621 = 2 * n_1644
    _x_23622 = 1
    _x_23625 = _x_23621 - 1
    _x_23626 = n_1644 * _x_23625
    return _x_23626

# Lean: Corpus.Sequences.heptagonal
def heptagonal(n_1645: int) -> int:
    _x_23637 = 5
    _x_23640 = 5 * n_1645
    _x_23641 = 3
    _x_23644 = _x_23640 - 3
    _x_23645 = n_1645 * _x_23644
    _x_23646 = 2
    _x_23649 = _x_23645 // 2
    return _x_23649

# Lean: Corpus.Sequences.octagonal
def octagonal(n_1646: int) -> int:
    _x_23657 = 3
    _x_23660 = 3 * n_1646
    _x_23661 = 2
    _x_23664 = _x_23660 - 2
    _x_23665 = n_1646 * _x_23664
    return _x_23665

# Lean: Corpus.Sequences.kGonal
def k_gonal(k_1647: int, n_1648: int) -> int:
    _x_23676 = 2
    _x_23679 = k_1647 - 2
    _x_23680 = _x_23679 * n_1648
    _x_23681 = 4
    _x_23684 = k_1647 - 4
    _x_23685 = _x_23680 - _x_23684
    _x_23686 = n_1648 * _x_23685
    _x_23687 = _x_23686 // 2
    return _x_23687

# Lean: Corpus.Sequences.tetrahedral
def tetrahedral(n_1649: int) -> int:
    _x_23698 = 1
    _x_23701 = n_1649 + 1
    _x_23702 = n_1649 * _x_23701
    _x_23703 = 2
    _x_23706 = n_1649 + 2
    _x_23707 = _x_23702 * _x_23706
    _x_23708 = 6
    _x_23711 = _x_23707 // 6
    return _x_23711

# Lean: Corpus.Sequences.pyramidal
def pyramidal(n_1650: int) -> int:
    _x_23722 = 1
    _x_23725 = n_1650 + 1
    _x_23726 = n_1650 * _x_23725
    _x_23727 = 2
    _x_23730 = 2 * n_1650
    _x_23731 = _x_23730 + 1
    _x_23732 = _x_23726 * _x_23731
    _x_23733 = 6
    _x_23736 = _x_23732 // 6
    return _x_23736

# Lean: Corpus.Sequences.centeredTriangular
def centered_triangular(n_1651: int) -> int:
    _x_23747 = 3
    _x_23750 = 3 * n_1651
    _x_23751 = _x_23750 * n_1651
    _x_23752 = _x_23751 + _x_23750
    _x_23753 = 2
    _x_23756 = _x_23752 + 2
    _x_23757 = _x_23756 // 2
    return _x_23757

# Lean: Corpus.Sequences.centeredSquare
def centered_square(n_1652: int) -> int:
    _x_23765 = n_1652 * n_1652
    _x_23766 = 1
    _x_23769 = n_1652 + 1
    _x_23770 = _x_23769 * _x_23769
    _x_23771 = _x_23765 + _x_23770
    return _x_23771

# Lean: Corpus.Sequences.centeredHexagonal
def centered_hexagonal(n_1653: int) -> int:
    _x_23779 = 3
    _x_23782 = 3 * n_1653
    _x_23786 = 1
    _x_23789 = n_1653 - 1
    _x_23790 = _x_23782 * _x_23789
    _x_23791 = _x_23790 + 1
    return _x_23791

# Lean: Corpus.Sequences.starNumber
def star_number(n_1654: int) -> int:
    _x_23799 = 6
    _x_23802 = 6 * n_1654
    _x_23806 = 1
    _x_23809 = n_1654 - 1
    _x_23810 = _x_23802 * _x_23809
    _x_23811 = _x_23810 + 1
    return _x_23811

# Lean: Corpus.Sequences.pronic
def pronic(n_1655: int) -> int:
    _x_23819 = 1
    _x_23822 = n_1655 + 1
    _x_23823 = n_1655 * _x_23822
    return _x_23823

# Lean: Corpus.Sequences.cullen
def cullen(n_1656: int) -> int:
    _x_23835 = 2
    _x_23838 = 2 ** n_1656
    _x_23839 = n_1656 * _x_23838
    _x_23840 = 1
    _x_23843 = _x_23839 + 1
    return _x_23843

# Lean: Corpus.Sequences.woodall
def woodall(n_1657: int) -> int:
    _x_23855 = 2
    _x_23858 = 2 ** n_1657
    _x_23859 = n_1657 * _x_23858
    _x_23860 = 1
    _x_23863 = _x_23859 - 1
    return _x_23863

# Lean: Corpus.Sequences.mersenne
def mersenne(n_1658: int) -> int:
    _x_23872 = 2
    _x_23875 = 2 ** n_1658
    _x_23876 = 1
    _x_23879 = _x_23875 - 1
    return _x_23879

# Lean: Corpus.Sequences.fermat
def fermat(n_1659: int) -> int:
    _x_23888 = 2
    _x_23891 = 2 ** n_1659
    _x_23892 = 2 ** _x_23891
    _x_23893 = 1
    _x_23896 = _x_23892 + 1
    return _x_23896

# Lean: Corpus.Sequences.safeFromGermain
def safe_from_germain(p_1660: int) -> int:
    _x_23904 = 2
    _x_23907 = 2 * p_1660
    _x_23908 = 1
    _x_23911 = _x_23907 + 1
    return _x_23911

# Lean: Corpus.Sequences.repunit
def repunit(n_1661: int) -> int:
    _x_23913 = 0
    _x_23916 = repunit_go(n_1661, 0)
    return _x_23916

# Lean: Corpus.Sequences.lookAndSayNext
def look_and_say_next(xs_1662: list[int]) -> list[int]:
    def _f_23919():
        _x_23918 = []
        return _x_23918
    _alt_23920 = _f_23919
    def _f_23927(x_1664: int, rest_1665: list[int]):
        _x_23921 = 1
        _x_23924 = []
        _x_23925 = look_and_say_next_go(rest_1665, x_1664, 1, _x_23924)
        _x_23926 = list(reversed(_x_23925))
        return _x_23926
    _alt_23928 = _f_23927
    if len(xs_1662) == 0:
        _x_23930 = _alt_23920()
        return _x_23930
    else:
        head_23931 = xs_1662[0]
        tail_23932 = xs_1662[1:]
        _x_23933 = _alt_23928(head_23931, tail_23932)
        return _x_23933

# Lean: Corpus.Sequences.collatzSequence
def collatz_sequence(n_1666: int) -> list[int]:
    _x_23936 = 1
    _x_23939 = n_1666 <= 1
    if _x_23939:
        _x_23978 = []
        _x_23979 = [n_1666] + _x_23978
        return _x_23979
    else:
        _x_23946 = 2
        _x_23949 = n_1666 % 2
        _x_23950 = 0
        _x_23953 = _x_23949 == 0
        _x_23954 = True
        def _jp_23976(_y_23973: int):
            _x_23974 = collatz_sequence(_y_23973)
            _x_23975 = [n_1666] + _x_23974
            return _x_23975
        if _x_23953:
            _x_23972 = n_1666 // 2
            return _jp_23976(_x_23972)
        else:
            _x_23963 = 3
            _x_23966 = 3 * n_1666
            _x_23967 = _x_23966 + 1
            return _jp_23976(_x_23967)

# Lean: Corpus.Sequences.recaman
def recaman(n_1667: int) -> list[int]:
    _x_23982 = 1
    _x_23985 = 0
    _x_23988 = []
    _x_23989 = [0] + _x_23988
    _x_23990 = recaman_go(n_1667, 1, 0, _x_23989, _x_23989)
    return _x_23990

# Lean: Corpus.Sequences.sylvester
def sylvester(n_1668: int) -> int:
    _x_23994 = 0
    _x_23997 = n_1668 == 0
    _x_23998 = True
    if _x_23997:
        _x_24019 = 2
        return 2
    else:
        _x_24004 = 1
        _x_24007 = n_1668 - 1
        _x_24008 = sylvester(_x_24007)
        _x_24015 = _x_24008 * _x_24008
        _x_24016 = _x_24015 - _x_24008
        _x_24017 = _x_24016 + 1
        return _x_24017

# Lean: Corpus.Sequences.alcuin
def alcuin(n_1670: int) -> int:
    _x_24029 = 12
    _x_24032 = n_1670 % 12
    _x_24033 = 0
    _x_24036 = _x_24032 == 0
    _x_24037 = True
    if _x_24036:
        _x_24119 = n_1670 * n_1670
        _x_24120 = _x_24119 // 12
        return _x_24120
    else:
        def _f_24040():
            return True
        _alt_24041 = _f_24040
        def _f_24046():
            _x_24042 = 9
            _x_24045 = _x_24032 == 9
            return _x_24045
        _alt_24047 = _f_24046
        _x_24048 = 3
        _x_24051 = _x_24032 == 3
        def _jp_24105(_y_24056: bool):
            if _y_24056:
                _x_24101 = n_1670 * n_1670
                _x_24102 = _x_24101 - 3
                _x_24103 = _x_24102 // 12
                return _x_24103
            else:
                _x_24059 = 6
                _x_24062 = _x_24032 == 6
                if _x_24062:
                    _x_24087 = n_1670 * n_1670
                    _x_24088 = _x_24087 - 12
                    _x_24089 = _x_24088 // 12
                    return _x_24089
                else:
                    _x_24074 = n_1670 * n_1670
                    _x_24075 = _x_24074 + 3
                    _x_24076 = _x_24075 // 12
                    return _x_24076
        def _jp_24108():
            _x_24107 = _alt_24047()
            return _jp_24105(_x_24107)
        def _jp_24111():
            _x_24110 = _alt_24041()
            return _jp_24105(_x_24110)
        if _x_24051:
            return _jp_24111()
        else:
            return _jp_24108()

# Lean: Corpus.Sequences.firstNPrimes
def first_nprimes(n_1673: int) -> list[int]:
    _x_24123 = 2
    _x_24126 = []
    _x_24127 = first_nprimes_go(n_1673, 2, _x_24126)
    return _x_24127

# Lean: Corpus.Sequences.vanEck
def van_eck(n_1674: int) -> list[int]:
    _x_24129 = 1
    _x_24132 = 0
    _x_24135 = []
    _x_24136 = []
    _x_24137 = [0] + _x_24136
    _x_24138 = van_eck_go(n_1674, 1, 0, _x_24135, _x_24137)
    return _x_24138

# Lean: Corpus.Sorting.bubbleSort
def bubble_sort(xs_1675: list[int]) -> list[int]:
    _x_24140 = len(xs_1675)
    _x_24141 = list(xs_1675)
    _x_24142 = 0
    _x_24145 = outer(_x_24140, 0, _x_24141)
    _x_24146 = list(_x_24145)
    return _x_24146

# Lean: Corpus.Sorting.selectionSort
def selection_sort(xs_1678: list[int]) -> list[int]:
    _x_24148 = len(xs_1678)
    _x_24149 = list(xs_1678)
    _x_24150 = 0
    _x_24153 = selection_sort_go(_x_24148, 0, _x_24149)
    _x_24154 = list(_x_24153)
    return _x_24154

# Lean: Corpus.Sorting.countingSort
def counting_sort(xs_1681: list[int], max_val_1682: int) -> list[int]:
    def _f_24168(arr_1683: list[int], x_1684: int):
        _x_24159 = 0
        _x_24162 = get_d(None, arr_1683, x_1684, 0)
        _x_24163 = 1
        _x_24166 = _x_24162 + 1
        _x_24167 = set_(None, arr_1683, x_1684, _x_24166)
        return _x_24167
    _x_24172 = 1
    _x_24175 = max_val_1682 + 1
    _x_24176 = 0
    _x_24179 = mk_array(None, _x_24175, 0)
    _x_24180 = functools.reduce(_f_24168, xs_1681, _x_24179)
    _x_24181 = []
    _x_24182 = expand(max_val_1682, _x_24180, 0, _x_24181)
    return _x_24182

# Lean: Corpus.Sorting.radixSort
def radix_sort(xs_1686: list[int]) -> list[int]:
    _x_24185 = max
    _x_24186 = 0
    _x_24189 = functools.reduce(_x_24185, xs_1686, 0)
    _x_24190 = 1
    _x_24193 = radix_sort_go(_x_24189, 1, xs_1686)
    return _x_24193

# Lean: Corpus.Sorting.gnomeSort
def gnome_sort(xs_1688: list[int]) -> list[int]:
    _x_24195 = len(xs_1688)
    _x_24196 = list(xs_1688)
    _x_24197 = 0
    _x_24200 = gnome_sort_go(_x_24195, 0, _x_24196)
    _x_24201 = list(_x_24200)
    return _x_24201

# Lean: Corpus.Sorting.isSorted
def is_sorted(xs_1691: list[int]) -> bool:
    def _f_24204():
        _x_24203 = True
        return True
    _alt_24205 = _f_24204
    def _f_24208(head_24206: int):
        _x_24207 = True
        return True
    _alt_24209 = _f_24208
    def _f_24224(x_1693: int, y_1694: int, rest_1695: list[int]):
        def _f_24211():
            _x_24210 = False
            return False
        _alt_24212 = _f_24211
        def _f_24215():
            _x_24213 = [y_1694] + rest_1695
            _x_24214 = is_sorted(_x_24213)
            return _x_24214
        _alt_24216 = _f_24215
        _x_24217 = x_1693 <= y_1694
        if _x_24217:
            _x_24222 = _alt_24216()
            return _x_24222
        else:
            _x_24220 = _alt_24212()
            return _x_24220
    _alt_24225 = _f_24224
    if len(xs_1691) == 0:
        _x_24227 = _alt_24205()
        return _x_24227
    else:
        head_24228 = xs_1691[0]
        tail_24229 = xs_1691[1:]
        if len(tail_24229) == 0:
            _x_24230 = _alt_24209(head_24228)
            return _x_24230
        else:
            head_24231 = tail_24229[0]
            tail_24232 = tail_24229[1:]
            _x_24233 = _alt_24225(head_24228, head_24231, tail_24232)
            return _x_24233

# Lean: Corpus.Sorting.isSortedDesc
def is_sorted_desc(xs_1698: list[int]) -> bool:
    def _f_24238():
        _x_24237 = True
        return True
    _alt_24239 = _f_24238
    def _f_24242(head_24240: int):
        _x_24241 = True
        return True
    _alt_24243 = _f_24242
    def _f_24258(x_1700: int, y_1701: int, rest_1702: list[int]):
        def _f_24245():
            _x_24244 = False
            return False
        _alt_24246 = _f_24245
        def _f_24249():
            _x_24247 = [y_1701] + rest_1702
            _x_24248 = is_sorted_desc(_x_24247)
            return _x_24248
        _alt_24250 = _f_24249
        _x_24251 = y_1701 <= x_1700
        if _x_24251:
            _x_24256 = _alt_24250()
            return _x_24256
        else:
            _x_24254 = _alt_24246()
            return _x_24254
    _alt_24259 = _f_24258
    if len(xs_1698) == 0:
        _x_24261 = _alt_24239()
        return _x_24261
    else:
        head_24262 = xs_1698[0]
        tail_24263 = xs_1698[1:]
        if len(tail_24263) == 0:
            _x_24264 = _alt_24243(head_24262)
            return _x_24264
        else:
            head_24265 = tail_24263[0]
            tail_24266 = tail_24263[1:]
            _x_24267 = _alt_24259(head_24262, head_24265, tail_24266)
            return _x_24267

# Lean: Corpus.Sorting.findMin
def find_min(xs_1705: list[int]) -> int | None:
    def _f_24291(acc_1706: int | None, x_1707: int):
        def _f_24271():
            return x_1707
        _alt_24272 = _f_24271
        def _f_24276(m_1709: int):
            _x_24274 = min
            _x_24275 = _x_24274(m_1709, x_1707)
            return _x_24275
        _alt_24277 = _f_24276
        def _jp_24284(_y_24282: int):
            _x_24283 = _y_24282
            return _x_24283
        def _jp_24287():
            _x_24286 = _alt_24272()
            return _jp_24284(_x_24286)
        def _jp_24290(_y_24288: int):
            _x_24289 = _alt_24277(_y_24288)
            return _jp_24284(_x_24289)
        if acc_1706 is None:
            return _jp_24287()
        else:
            val_24280 = acc_1706
            return _jp_24290(val_24280)
    _x_24292 = None
    _x_24293 = functools.reduce(_f_24291, xs_1705, _x_24292)
    return _x_24293

# Lean: Corpus.Sorting.findMax
def find_max(xs_1710: list[int]) -> int | None:
    def _f_24315(acc_1711: int | None, x_1712: int):
        def _f_24295():
            return x_1712
        _alt_24296 = _f_24295
        def _f_24300(m_1714: int):
            _x_24298 = max
            _x_24299 = _x_24298(m_1714, x_1712)
            return _x_24299
        _alt_24301 = _f_24300
        def _jp_24308(_y_24306: int):
            _x_24307 = _y_24306
            return _x_24307
        def _jp_24314(_y_24312: int):
            _x_24313 = _alt_24301(_y_24312)
            return _jp_24308(_x_24313)
        def _jp_24311():
            _x_24310 = _alt_24296()
            return _jp_24308(_x_24310)
        if acc_1711 is None:
            return _jp_24311()
        else:
            val_24304 = acc_1711
            return _jp_24314(val_24304)
    _x_24316 = None
    _x_24317 = functools.reduce(_f_24315, xs_1710, _x_24316)
    return _x_24317

# Lean: Corpus.Sorting.kthSmallest
def kth_smallest(xs_1715: list[int], k_1716: int) -> int | None:
    _x_24319 = insertion_sort(xs_1715)
    _x_24320 = _x_24319[k_1716] if 0 <= k_1716 < len(_x_24319) else None
    return _x_24320

# Lean: Corpus.Sorting.kthLargest
def kth_largest(xs_1718: list[int], k_1719: int) -> int | None:
    _x_24322 = insertion_sort(xs_1718)
    _x_24323 = len(_x_24322)
    _x_24324 = _x_24323 <= k_1719
    if _x_24324:
        _x_24336 = None
        return _x_24336
    else:
        _x_24329 = 1
        _x_24332 = _x_24323 - 1
        _x_24333 = _x_24332 - k_1719
        _x_24334 = _x_24322[_x_24333] if 0 <= _x_24333 < len(_x_24322) else None
        return _x_24334

# Lean: Corpus.Sorting.median
def median(xs_1721: list[int]) -> int | None:
    _x_24339 = len(xs_1721) == 0
    _x_24340 = True
    if _x_24339:
        _x_24354 = None
        return _x_24354
    else:
        _x_24343 = insertion_sort(xs_1721)
        _x_24344 = len(_x_24343)
        _x_24348 = 2
        _x_24351 = _x_24344 // 2
        _x_24352 = _x_24343[_x_24351] if 0 <= _x_24351 < len(_x_24343) else None
        return _x_24352

# Lean: Corpus.Sorting.mode
def mode(xs_1724: list[int]) -> int | None:
    _x_24357 = None
    _x_24358 = 0
    _x_24361 = mode_go(xs_1724, _x_24357, 0)
    return _x_24361

# Lean: Corpus.Sorting.unique
def unique(xs_1725: list[int]) -> list[int]:
    _x_24363 = []
    _x_24364 = unique_go(xs_1725, _x_24363)
    return _x_24364

# Lean: Corpus.Sorting.removeDupsSorted
def remove_dups_sorted(xs_1726: list[int]) -> list[int]:
    def _f_24367():
        _x_24366 = []
        return _x_24366
    _alt_24368 = _f_24367
    def _f_24371(x_1728: int):
        _x_24369 = []
        _x_24370 = [x_1728] + _x_24369
        return _x_24370
    _alt_24372 = _f_24371
    def _f_24386(x_1729: int, y_1730: int, rest_1731: list[int]):
        _x_24375 = x_1729 == y_1730
        _x_24376 = True
        if _x_24375:
            _x_24383 = [y_1730] + rest_1731
            _x_24384 = remove_dups_sorted(_x_24383)
            return _x_24384
        else:
            _x_24379 = [y_1730] + rest_1731
            _x_24380 = remove_dups_sorted(_x_24379)
            _x_24381 = [x_1729] + _x_24380
            return _x_24381
    _alt_24387 = _f_24386
    if len(xs_1726) == 0:
        _x_24389 = _alt_24368()
        return _x_24389
    else:
        head_24390 = xs_1726[0]
        tail_24391 = xs_1726[1:]
        if len(tail_24391) == 0:
            _x_24392 = _alt_24372(head_24390)
            return _x_24392
        else:
            head_24393 = tail_24391[0]
            tail_24394 = tail_24391[1:]
            _x_24395 = _alt_24387(head_24390, head_24393, tail_24394)
            return _x_24395

# Lean: Corpus.Production.RBTree.singleton
def singleton(__1732: Any, x_1733: Any) -> Any:
    _x_24399 = red()
    _x_24400 = RBTree_empty(None)
    _x_24401 = RBTree_node(None, _x_24399, _x_24400, x_1733, _x_24400)
    return _x_24401

# Lean: Corpus.Production.RBTree.member
def member(__1734: Any, inst_24403: Any, x_1735: Any, x_24404: Any) -> bool:
    def _f_24406():
        _x_24405 = False
        return False
    _alt_24407 = _f_24406
    def _f_24427(a_24408: Color, l_1737: Any, y_1738: Any, r_1739: Any):
        def _f_24410():
            _x_24409 = member(None, inst_24403, x_1735, l_1737)
            return _x_24409
        _alt_24411 = _f_24410
        def _f_24413():
            _x_24412 = True
            return True
        _alt_24414 = _f_24413
        def _f_24416():
            _x_24415 = member(None, inst_24403, x_1735, r_1739)
            return _x_24415
        _alt_24417 = _f_24416
        _x_24418 = inst_24403.ord_0
        _x_24419 = _x_24418(x_1735, y_1738)
        match _x_24419:
            case lt():
                _x_24421 = _alt_24411()
                return _x_24421
            case eq():
                _x_24423 = _alt_24414()
                return _x_24423
            case gt():
                _x_24425 = _alt_24417()
                return _x_24425
    _alt_24428 = _f_24427
    match x_24404:
        case RBTree_empty():
            _x_24430 = _alt_24407()
            return _x_24430
        case RBTree_node(a_24431, a_24432, a_24433, a_24434):
            _x_24435 = _alt_24428(a_24431, a_24432, a_24433, a_24434)
            return _x_24435

# Lean: Corpus.Production.RBTree.balance
def balance(__1743: Any, x_24438: Color, x_24439: Any, x_24440: Any, x_24441: Any) -> Any:
    def _f_24447(a_1744: Any, x_1745: Any, b_1746: Any, y_1747: Any, c_1748: Any, z_1749: Any, d_1750: Any):
        _x_24442 = red()
        _x_24443 = black()
        _x_24444 = RBTree_node(None, _x_24443, a_1744, x_1745, b_1746)
        _x_24445 = RBTree_node(None, _x_24443, c_1748, z_1749, d_1750)
        _x_24446 = RBTree_node(None, _x_24442, _x_24444, y_1747, _x_24445)
        return _x_24446
    _alt_24448 = _f_24447
    _alt_24449 = _f_24447
    _alt_24450 = _f_24447
    _alt_24451 = _f_24447
    def _f_24453(c_1751: Color, l_1752: Any, x_1753: Any, r_1754: Any):
        _x_24452 = RBTree_node(None, c_1751, l_1752, x_1753, r_1754)
        return _x_24452
    _alt_24454 = _f_24453
    match x_24438:
        case red():
            _x_24455 = red()
            _x_24456 = _alt_24454(_x_24455, x_24439, x_24440, x_24441)
            return _x_24456
        case black():
            match x_24439:
                case RBTree_empty():
                    match x_24441:
                        case RBTree_empty():
                            _x_24457 = black()
                            _x_24458 = RBTree_empty(None)
                            _x_24459 = _alt_24454(_x_24457, _x_24458, x_24440, _x_24458)
                            return _x_24459
                        case RBTree_node(a_24460, a_24461, a_24462, a_24463):
                            match a_24460:
                                case red():
                                    match a_24461:
                                        case RBTree_empty():
                                            match a_24463:
                                                case RBTree_empty():
                                                    _x_24464 = black()
                                                    _x_24465 = RBTree_empty(None)
                                                    _x_24466 = red()
                                                    _x_24467 = RBTree_node(None, _x_24466, _x_24465, a_24462, _x_24465)
                                                    _x_24468 = _alt_24454(_x_24464, _x_24465, x_24440, _x_24467)
                                                    return _x_24468
                                                case RBTree_node(a_24469, a_24470, a_24471, a_24472):
                                                    match a_24469:
                                                        case red():
                                                            _x_24473 = RBTree_empty(None)
                                                            _x_24474 = _alt_24451(_x_24473, x_24440, _x_24473, a_24462, a_24470, a_24471, a_24472)
                                                            return _x_24474
                                                        case black():
                                                            _x_24475 = black()
                                                            _x_24476 = RBTree_empty(None)
                                                            _x_24477 = red()
                                                            _x_24478 = RBTree_node(None, _x_24475, a_24470, a_24471, a_24472)
                                                            _x_24479 = RBTree_node(None, _x_24477, _x_24476, a_24462, _x_24478)
                                                            _x_24480 = _alt_24454(_x_24475, _x_24476, x_24440, _x_24479)
                                                            return _x_24480
                                        case RBTree_node(a_24483, a_24484, a_24485, a_24486):
                                            match a_24483:
                                                case red():
                                                    match a_24463:
                                                        case RBTree_empty():
                                                            _x_24487 = RBTree_empty(None)
                                                            _x_24488 = _alt_24450(_x_24487, x_24440, a_24484, a_24485, a_24486, a_24462, _x_24487)
                                                            return _x_24488
                                                        case RBTree_node(a_24489, a_24490, a_24491, a_24492):
                                                            match a_24489:
                                                                case red():
                                                                    _x_24493 = RBTree_empty(None)
                                                                    _x_24494 = red()
                                                                    _x_24495 = RBTree_node(None, _x_24494, a_24490, a_24491, a_24492)
                                                                    _x_24496 = _alt_24450(_x_24493, x_24440, a_24484, a_24485, a_24486, a_24462, _x_24495)
                                                                    return _x_24496
                                                                case black():
                                                                    _x_24497 = RBTree_empty(None)
                                                                    _x_24498 = black()
                                                                    _x_24499 = RBTree_node(None, _x_24498, a_24490, a_24491, a_24492)
                                                                    _x_24500 = _alt_24450(_x_24497, x_24440, a_24484, a_24485, a_24486, a_24462, _x_24499)
                                                                    return _x_24500
                                                case black():
                                                    match a_24463:
                                                        case RBTree_empty():
                                                            _x_24503 = black()
                                                            _x_24504 = RBTree_empty(None)
                                                            _x_24505 = red()
                                                            _x_24506 = RBTree_node(None, _x_24503, a_24484, a_24485, a_24486)
                                                            _x_24507 = RBTree_node(None, _x_24505, _x_24506, a_24462, _x_24504)
                                                            _x_24508 = _alt_24454(_x_24503, _x_24504, x_24440, _x_24507)
                                                            return _x_24508
                                                        case RBTree_node(a_24509, a_24510, a_24511, a_24512):
                                                            match a_24509:
                                                                case red():
                                                                    _x_24513 = RBTree_empty(None)
                                                                    _x_24514 = black()
                                                                    _x_24515 = RBTree_node(None, _x_24514, a_24484, a_24485, a_24486)
                                                                    _x_24516 = _alt_24451(_x_24513, x_24440, _x_24515, a_24462, a_24510, a_24511, a_24512)
                                                                    return _x_24516
                                                                case black():
                                                                    _x_24517 = black()
                                                                    _x_24518 = RBTree_empty(None)
                                                                    _x_24519 = red()
                                                                    _x_24520 = RBTree_node(None, _x_24517, a_24484, a_24485, a_24486)
                                                                    _x_24521 = RBTree_node(None, _x_24517, a_24510, a_24511, a_24512)
                                                                    _x_24522 = RBTree_node(None, _x_24519, _x_24520, a_24462, _x_24521)
                                                                    _x_24523 = _alt_24454(_x_24517, _x_24518, x_24440, _x_24522)
                                                                    return _x_24523
                                case black():
                                    _x_24528 = black()
                                    _x_24529 = RBTree_empty(None)
                                    _x_24530 = RBTree_node(None, _x_24528, a_24461, a_24462, a_24463)
                                    _x_24531 = _alt_24454(_x_24528, _x_24529, x_24440, _x_24530)
                                    return _x_24531
                case RBTree_node(a_24534, a_24535, a_24536, a_24537):
                    match a_24534:
                        case red():
                            match a_24535:
                                case RBTree_empty():
                                    match a_24537:
                                        case RBTree_empty():
                                            match x_24441:
                                                case RBTree_empty():
                                                    _x_24538 = black()
                                                    _x_24539 = red()
                                                    _x_24540 = RBTree_empty(None)
                                                    _x_24541 = RBTree_node(None, _x_24539, _x_24540, a_24536, _x_24540)
                                                    _x_24542 = _alt_24454(_x_24538, _x_24541, x_24440, _x_24540)
                                                    return _x_24542
                                                case RBTree_node(a_24543, a_24544, a_24545, a_24546):
                                                    match a_24543:
                                                        case red():
                                                            match a_24544:
                                                                case RBTree_empty():
                                                                    match a_24546:
                                                                        case RBTree_empty():
                                                                            _x_24547 = black()
                                                                            _x_24548 = red()
                                                                            _x_24549 = RBTree_empty(None)
                                                                            _x_24550 = RBTree_node(None, _x_24548, _x_24549, a_24536, _x_24549)
                                                                            _x_24551 = RBTree_node(None, _x_24548, _x_24549, a_24545, _x_24549)
                                                                            _x_24552 = _alt_24454(_x_24547, _x_24550, x_24440, _x_24551)
                                                                            return _x_24552
                                                                        case RBTree_node(a_24553, a_24554, a_24555, a_24556):
                                                                            match a_24553:
                                                                                case red():
                                                                                    _x_24557 = red()
                                                                                    _x_24558 = RBTree_empty(None)
                                                                                    _x_24559 = RBTree_node(None, _x_24557, _x_24558, a_24536, _x_24558)
                                                                                    _x_24560 = _alt_24451(_x_24559, x_24440, _x_24558, a_24545, a_24554, a_24555, a_24556)
                                                                                    return _x_24560
                                                                                case black():
                                                                                    _x_24561 = black()
                                                                                    _x_24562 = red()
                                                                                    _x_24563 = RBTree_empty(None)
                                                                                    _x_24564 = RBTree_node(None, _x_24562, _x_24563, a_24536, _x_24563)
                                                                                    _x_24565 = RBTree_node(None, _x_24561, a_24554, a_24555, a_24556)
                                                                                    _x_24566 = RBTree_node(None, _x_24562, _x_24563, a_24545, _x_24565)
                                                                                    _x_24567 = _alt_24454(_x_24561, _x_24564, x_24440, _x_24566)
                                                                                    return _x_24567
                                                                case RBTree_node(a_24570, a_24571, a_24572, a_24573):
                                                                    match a_24570:
                                                                        case red():
                                                                            match a_24546:
                                                                                case RBTree_empty():
                                                                                    _x_24574 = red()
                                                                                    _x_24575 = RBTree_empty(None)
                                                                                    _x_24576 = RBTree_node(None, _x_24574, _x_24575, a_24536, _x_24575)
                                                                                    _x_24577 = _alt_24450(_x_24576, x_24440, a_24571, a_24572, a_24573, a_24545, _x_24575)
                                                                                    return _x_24577
                                                                                case RBTree_node(a_24578, a_24579, a_24580, a_24581):
                                                                                    match a_24578:
                                                                                        case red():
                                                                                            _x_24582 = red()
                                                                                            _x_24583 = RBTree_empty(None)
                                                                                            _x_24584 = RBTree_node(None, _x_24582, _x_24583, a_24536, _x_24583)
                                                                                            _x_24585 = RBTree_node(None, _x_24582, a_24579, a_24580, a_24581)
                                                                                            _x_24586 = _alt_24450(_x_24584, x_24440, a_24571, a_24572, a_24573, a_24545, _x_24585)
                                                                                            return _x_24586
                                                                                        case black():
                                                                                            _x_24587 = red()
                                                                                            _x_24588 = RBTree_empty(None)
                                                                                            _x_24589 = RBTree_node(None, _x_24587, _x_24588, a_24536, _x_24588)
                                                                                            _x_24590 = black()
                                                                                            _x_24591 = RBTree_node(None, _x_24590, a_24579, a_24580, a_24581)
                                                                                            _x_24592 = _alt_24450(_x_24589, x_24440, a_24571, a_24572, a_24573, a_24545, _x_24591)
                                                                                            return _x_24592
                                                                        case black():
                                                                            match a_24546:
                                                                                case RBTree_empty():
                                                                                    _x_24595 = black()
                                                                                    _x_24596 = red()
                                                                                    _x_24597 = RBTree_empty(None)
                                                                                    _x_24598 = RBTree_node(None, _x_24596, _x_24597, a_24536, _x_24597)
                                                                                    _x_24599 = RBTree_node(None, _x_24595, a_24571, a_24572, a_24573)
                                                                                    _x_24600 = RBTree_node(None, _x_24596, _x_24599, a_24545, _x_24597)
                                                                                    _x_24601 = _alt_24454(_x_24595, _x_24598, x_24440, _x_24600)
                                                                                    return _x_24601
                                                                                case RBTree_node(a_24602, a_24603, a_24604, a_24605):
                                                                                    match a_24602:
                                                                                        case red():
                                                                                            _x_24606 = red()
                                                                                            _x_24607 = RBTree_empty(None)
                                                                                            _x_24608 = RBTree_node(None, _x_24606, _x_24607, a_24536, _x_24607)
                                                                                            _x_24609 = black()
                                                                                            _x_24610 = RBTree_node(None, _x_24609, a_24571, a_24572, a_24573)
                                                                                            _x_24611 = _alt_24451(_x_24608, x_24440, _x_24610, a_24545, a_24603, a_24604, a_24605)
                                                                                            return _x_24611
                                                                                        case black():
                                                                                            _x_24612 = black()
                                                                                            _x_24613 = red()
                                                                                            _x_24614 = RBTree_empty(None)
                                                                                            _x_24615 = RBTree_node(None, _x_24613, _x_24614, a_24536, _x_24614)
                                                                                            _x_24616 = RBTree_node(None, _x_24612, a_24571, a_24572, a_24573)
                                                                                            _x_24617 = RBTree_node(None, _x_24612, a_24603, a_24604, a_24605)
                                                                                            _x_24618 = RBTree_node(None, _x_24613, _x_24616, a_24545, _x_24617)
                                                                                            _x_24619 = _alt_24454(_x_24612, _x_24615, x_24440, _x_24618)
                                                                                            return _x_24619
                                                        case black():
                                                            _x_24624 = black()
                                                            _x_24625 = red()
                                                            _x_24626 = RBTree_empty(None)
                                                            _x_24627 = RBTree_node(None, _x_24625, _x_24626, a_24536, _x_24626)
                                                            _x_24628 = RBTree_node(None, _x_24624, a_24544, a_24545, a_24546)
                                                            _x_24629 = _alt_24454(_x_24624, _x_24627, x_24440, _x_24628)
                                                            return _x_24629
                                        case RBTree_node(a_24632, a_24633, a_24634, a_24635):
                                            match a_24632:
                                                case red():
                                                    match x_24441:
                                                        case RBTree_empty():
                                                            _x_24636 = RBTree_empty(None)
                                                            _x_24637 = _alt_24449(_x_24636, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24636)
                                                            return _x_24637
                                                        case RBTree_node(a_24638, a_24639, a_24640, a_24641):
                                                            match a_24638:
                                                                case red():
                                                                    match a_24639:
                                                                        case RBTree_empty():
                                                                            match a_24641:
                                                                                case RBTree_empty():
                                                                                    _x_24642 = RBTree_empty(None)
                                                                                    _x_24643 = red()
                                                                                    _x_24644 = RBTree_node(None, _x_24643, _x_24642, a_24640, _x_24642)
                                                                                    _x_24645 = _alt_24449(_x_24642, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24644)
                                                                                    return _x_24645
                                                                                case RBTree_node(a_24646, a_24647, a_24648, a_24649):
                                                                                    match a_24646:
                                                                                        case red():
                                                                                            _x_24650 = RBTree_empty(None)
                                                                                            _x_24651 = red()
                                                                                            _x_24652 = RBTree_node(None, _x_24651, a_24647, a_24648, a_24649)
                                                                                            _x_24653 = RBTree_node(None, _x_24651, _x_24650, a_24640, _x_24652)
                                                                                            _x_24654 = _alt_24449(_x_24650, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24653)
                                                                                            return _x_24654
                                                                                        case black():
                                                                                            _x_24655 = RBTree_empty(None)
                                                                                            _x_24656 = red()
                                                                                            _x_24657 = black()
                                                                                            _x_24658 = RBTree_node(None, _x_24657, a_24647, a_24648, a_24649)
                                                                                            _x_24659 = RBTree_node(None, _x_24656, _x_24655, a_24640, _x_24658)
                                                                                            _x_24660 = _alt_24449(_x_24655, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24659)
                                                                                            return _x_24660
                                                                        case RBTree_node(a_24663, a_24664, a_24665, a_24666):
                                                                            match a_24663:
                                                                                case red():
                                                                                    match a_24641:
                                                                                        case RBTree_empty():
                                                                                            _x_24667 = RBTree_empty(None)
                                                                                            _x_24668 = red()
                                                                                            _x_24669 = RBTree_node(None, _x_24668, a_24664, a_24665, a_24666)
                                                                                            _x_24670 = RBTree_node(None, _x_24668, _x_24669, a_24640, _x_24667)
                                                                                            _x_24671 = _alt_24449(_x_24667, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24670)
                                                                                            return _x_24671
                                                                                        case RBTree_node(a_24672, a_24673, a_24674, a_24675):
                                                                                            match a_24672:
                                                                                                case red():
                                                                                                    _x_24676 = RBTree_empty(None)
                                                                                                    _x_24677 = red()
                                                                                                    _x_24678 = RBTree_node(None, _x_24677, a_24664, a_24665, a_24666)
                                                                                                    _x_24679 = RBTree_node(None, _x_24677, a_24673, a_24674, a_24675)
                                                                                                    _x_24680 = RBTree_node(None, _x_24677, _x_24678, a_24640, _x_24679)
                                                                                                    _x_24681 = _alt_24449(_x_24676, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24680)
                                                                                                    return _x_24681
                                                                                                case black():
                                                                                                    _x_24682 = RBTree_empty(None)
                                                                                                    _x_24683 = red()
                                                                                                    _x_24684 = RBTree_node(None, _x_24683, a_24664, a_24665, a_24666)
                                                                                                    _x_24685 = black()
                                                                                                    _x_24686 = RBTree_node(None, _x_24685, a_24673, a_24674, a_24675)
                                                                                                    _x_24687 = RBTree_node(None, _x_24683, _x_24684, a_24640, _x_24686)
                                                                                                    _x_24688 = _alt_24449(_x_24682, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24687)
                                                                                                    return _x_24688
                                                                                case black():
                                                                                    match a_24641:
                                                                                        case RBTree_empty():
                                                                                            _x_24691 = RBTree_empty(None)
                                                                                            _x_24692 = red()
                                                                                            _x_24693 = black()
                                                                                            _x_24694 = RBTree_node(None, _x_24693, a_24664, a_24665, a_24666)
                                                                                            _x_24695 = RBTree_node(None, _x_24692, _x_24694, a_24640, _x_24691)
                                                                                            _x_24696 = _alt_24449(_x_24691, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24695)
                                                                                            return _x_24696
                                                                                        case RBTree_node(a_24697, a_24698, a_24699, a_24700):
                                                                                            match a_24697:
                                                                                                case red():
                                                                                                    _x_24701 = RBTree_empty(None)
                                                                                                    _x_24702 = red()
                                                                                                    _x_24703 = black()
                                                                                                    _x_24704 = RBTree_node(None, _x_24703, a_24664, a_24665, a_24666)
                                                                                                    _x_24705 = RBTree_node(None, _x_24702, a_24698, a_24699, a_24700)
                                                                                                    _x_24706 = RBTree_node(None, _x_24702, _x_24704, a_24640, _x_24705)
                                                                                                    _x_24707 = _alt_24449(_x_24701, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24706)
                                                                                                    return _x_24707
                                                                                                case black():
                                                                                                    _x_24708 = RBTree_empty(None)
                                                                                                    _x_24709 = red()
                                                                                                    _x_24710 = black()
                                                                                                    _x_24711 = RBTree_node(None, _x_24710, a_24664, a_24665, a_24666)
                                                                                                    _x_24712 = RBTree_node(None, _x_24710, a_24698, a_24699, a_24700)
                                                                                                    _x_24713 = RBTree_node(None, _x_24709, _x_24711, a_24640, _x_24712)
                                                                                                    _x_24714 = _alt_24449(_x_24708, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24713)
                                                                                                    return _x_24714
                                                                case black():
                                                                    _x_24719 = RBTree_empty(None)
                                                                    _x_24720 = black()
                                                                    _x_24721 = RBTree_node(None, _x_24720, a_24639, a_24640, a_24641)
                                                                    _x_24722 = _alt_24449(_x_24719, a_24536, a_24633, a_24634, a_24635, x_24440, _x_24721)
                                                                    return _x_24722
                                                case black():
                                                    match x_24441:
                                                        case RBTree_empty():
                                                            _x_24725 = black()
                                                            _x_24726 = red()
                                                            _x_24727 = RBTree_empty(None)
                                                            _x_24728 = RBTree_node(None, _x_24725, a_24633, a_24634, a_24635)
                                                            _x_24729 = RBTree_node(None, _x_24726, _x_24727, a_24536, _x_24728)
                                                            _x_24730 = _alt_24454(_x_24725, _x_24729, x_24440, _x_24727)
                                                            return _x_24730
                                                        case RBTree_node(a_24731, a_24732, a_24733, a_24734):
                                                            match a_24731:
                                                                case red():
                                                                    match a_24732:
                                                                        case RBTree_empty():
                                                                            match a_24734:
                                                                                case RBTree_empty():
                                                                                    _x_24735 = black()
                                                                                    _x_24736 = red()
                                                                                    _x_24737 = RBTree_empty(None)
                                                                                    _x_24738 = RBTree_node(None, _x_24735, a_24633, a_24634, a_24635)
                                                                                    _x_24739 = RBTree_node(None, _x_24736, _x_24737, a_24536, _x_24738)
                                                                                    _x_24740 = RBTree_node(None, _x_24736, _x_24737, a_24733, _x_24737)
                                                                                    _x_24741 = _alt_24454(_x_24735, _x_24739, x_24440, _x_24740)
                                                                                    return _x_24741
                                                                                case RBTree_node(a_24742, a_24743, a_24744, a_24745):
                                                                                    match a_24742:
                                                                                        case red():
                                                                                            _x_24746 = red()
                                                                                            _x_24747 = RBTree_empty(None)
                                                                                            _x_24748 = black()
                                                                                            _x_24749 = RBTree_node(None, _x_24748, a_24633, a_24634, a_24635)
                                                                                            _x_24750 = RBTree_node(None, _x_24746, _x_24747, a_24536, _x_24749)
                                                                                            _x_24751 = _alt_24451(_x_24750, x_24440, _x_24747, a_24733, a_24743, a_24744, a_24745)
                                                                                            return _x_24751
                                                                                        case black():
                                                                                            _x_24752 = black()
                                                                                            _x_24753 = red()
                                                                                            _x_24754 = RBTree_empty(None)
                                                                                            _x_24755 = RBTree_node(None, _x_24752, a_24633, a_24634, a_24635)
                                                                                            _x_24756 = RBTree_node(None, _x_24753, _x_24754, a_24536, _x_24755)
                                                                                            _x_24757 = RBTree_node(None, _x_24752, a_24743, a_24744, a_24745)
                                                                                            _x_24758 = RBTree_node(None, _x_24753, _x_24754, a_24733, _x_24757)
                                                                                            _x_24759 = _alt_24454(_x_24752, _x_24756, x_24440, _x_24758)
                                                                                            return _x_24759
                                                                        case RBTree_node(a_24762, a_24763, a_24764, a_24765):
                                                                            match a_24762:
                                                                                case red():
                                                                                    match a_24734:
                                                                                        case RBTree_empty():
                                                                                            _x_24766 = red()
                                                                                            _x_24767 = RBTree_empty(None)
                                                                                            _x_24768 = black()
                                                                                            _x_24769 = RBTree_node(None, _x_24768, a_24633, a_24634, a_24635)
                                                                                            _x_24770 = RBTree_node(None, _x_24766, _x_24767, a_24536, _x_24769)
                                                                                            _x_24771 = _alt_24450(_x_24770, x_24440, a_24763, a_24764, a_24765, a_24733, _x_24767)
                                                                                            return _x_24771
                                                                                        case RBTree_node(a_24772, a_24773, a_24774, a_24775):
                                                                                            match a_24772:
                                                                                                case red():
                                                                                                    _x_24776 = red()
                                                                                                    _x_24777 = RBTree_empty(None)
                                                                                                    _x_24778 = black()
                                                                                                    _x_24779 = RBTree_node(None, _x_24778, a_24633, a_24634, a_24635)
                                                                                                    _x_24780 = RBTree_node(None, _x_24776, _x_24777, a_24536, _x_24779)
                                                                                                    _x_24781 = RBTree_node(None, _x_24776, a_24773, a_24774, a_24775)
                                                                                                    _x_24782 = _alt_24450(_x_24780, x_24440, a_24763, a_24764, a_24765, a_24733, _x_24781)
                                                                                                    return _x_24782
                                                                                                case black():
                                                                                                    _x_24783 = red()
                                                                                                    _x_24784 = RBTree_empty(None)
                                                                                                    _x_24785 = black()
                                                                                                    _x_24786 = RBTree_node(None, _x_24785, a_24633, a_24634, a_24635)
                                                                                                    _x_24787 = RBTree_node(None, _x_24783, _x_24784, a_24536, _x_24786)
                                                                                                    _x_24788 = RBTree_node(None, _x_24785, a_24773, a_24774, a_24775)
                                                                                                    _x_24789 = _alt_24450(_x_24787, x_24440, a_24763, a_24764, a_24765, a_24733, _x_24788)
                                                                                                    return _x_24789
                                                                                case black():
                                                                                    match a_24734:
                                                                                        case RBTree_empty():
                                                                                            _x_24792 = black()
                                                                                            _x_24793 = red()
                                                                                            _x_24794 = RBTree_empty(None)
                                                                                            _x_24795 = RBTree_node(None, _x_24792, a_24633, a_24634, a_24635)
                                                                                            _x_24796 = RBTree_node(None, _x_24793, _x_24794, a_24536, _x_24795)
                                                                                            _x_24797 = RBTree_node(None, _x_24792, a_24763, a_24764, a_24765)
                                                                                            _x_24798 = RBTree_node(None, _x_24793, _x_24797, a_24733, _x_24794)
                                                                                            _x_24799 = _alt_24454(_x_24792, _x_24796, x_24440, _x_24798)
                                                                                            return _x_24799
                                                                                        case RBTree_node(a_24800, a_24801, a_24802, a_24803):
                                                                                            match a_24800:
                                                                                                case red():
                                                                                                    _x_24804 = red()
                                                                                                    _x_24805 = RBTree_empty(None)
                                                                                                    _x_24806 = black()
                                                                                                    _x_24807 = RBTree_node(None, _x_24806, a_24633, a_24634, a_24635)
                                                                                                    _x_24808 = RBTree_node(None, _x_24804, _x_24805, a_24536, _x_24807)
                                                                                                    _x_24809 = RBTree_node(None, _x_24806, a_24763, a_24764, a_24765)
                                                                                                    _x_24810 = _alt_24451(_x_24808, x_24440, _x_24809, a_24733, a_24801, a_24802, a_24803)
                                                                                                    return _x_24810
                                                                                                case black():
                                                                                                    _x_24811 = black()
                                                                                                    _x_24812 = red()
                                                                                                    _x_24813 = RBTree_empty(None)
                                                                                                    _x_24814 = RBTree_node(None, _x_24811, a_24633, a_24634, a_24635)
                                                                                                    _x_24815 = RBTree_node(None, _x_24812, _x_24813, a_24536, _x_24814)
                                                                                                    _x_24816 = RBTree_node(None, _x_24811, a_24763, a_24764, a_24765)
                                                                                                    _x_24817 = RBTree_node(None, _x_24811, a_24801, a_24802, a_24803)
                                                                                                    _x_24818 = RBTree_node(None, _x_24812, _x_24816, a_24733, _x_24817)
                                                                                                    _x_24819 = _alt_24454(_x_24811, _x_24815, x_24440, _x_24818)
                                                                                                    return _x_24819
                                                                case black():
                                                                    _x_24824 = black()
                                                                    _x_24825 = red()
                                                                    _x_24826 = RBTree_empty(None)
                                                                    _x_24827 = RBTree_node(None, _x_24824, a_24633, a_24634, a_24635)
                                                                    _x_24828 = RBTree_node(None, _x_24825, _x_24826, a_24536, _x_24827)
                                                                    _x_24829 = RBTree_node(None, _x_24824, a_24732, a_24733, a_24734)
                                                                    _x_24830 = _alt_24454(_x_24824, _x_24828, x_24440, _x_24829)
                                                                    return _x_24830
                                case RBTree_node(a_24835, a_24836, a_24837, a_24838):
                                    match a_24835:
                                        case red():
                                            match a_24537:
                                                case RBTree_empty():
                                                    match x_24441:
                                                        case RBTree_empty():
                                                            _x_24839 = RBTree_empty(None)
                                                            _x_24840 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24839, x_24440, _x_24839)
                                                            return _x_24840
                                                        case RBTree_node(a_24841, a_24842, a_24843, a_24844):
                                                            match a_24841:
                                                                case red():
                                                                    match a_24842:
                                                                        case RBTree_empty():
                                                                            match a_24844:
                                                                                case RBTree_empty():
                                                                                    _x_24845 = RBTree_empty(None)
                                                                                    _x_24846 = red()
                                                                                    _x_24847 = RBTree_node(None, _x_24846, _x_24845, a_24843, _x_24845)
                                                                                    _x_24848 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24845, x_24440, _x_24847)
                                                                                    return _x_24848
                                                                                case RBTree_node(a_24849, a_24850, a_24851, a_24852):
                                                                                    match a_24849:
                                                                                        case red():
                                                                                            _x_24853 = RBTree_empty(None)
                                                                                            _x_24854 = red()
                                                                                            _x_24855 = RBTree_node(None, _x_24854, a_24850, a_24851, a_24852)
                                                                                            _x_24856 = RBTree_node(None, _x_24854, _x_24853, a_24843, _x_24855)
                                                                                            _x_24857 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24853, x_24440, _x_24856)
                                                                                            return _x_24857
                                                                                        case black():
                                                                                            _x_24858 = RBTree_empty(None)
                                                                                            _x_24859 = red()
                                                                                            _x_24860 = black()
                                                                                            _x_24861 = RBTree_node(None, _x_24860, a_24850, a_24851, a_24852)
                                                                                            _x_24862 = RBTree_node(None, _x_24859, _x_24858, a_24843, _x_24861)
                                                                                            _x_24863 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24858, x_24440, _x_24862)
                                                                                            return _x_24863
                                                                        case RBTree_node(a_24866, a_24867, a_24868, a_24869):
                                                                            match a_24866:
                                                                                case red():
                                                                                    match a_24844:
                                                                                        case RBTree_empty():
                                                                                            _x_24870 = RBTree_empty(None)
                                                                                            _x_24871 = red()
                                                                                            _x_24872 = RBTree_node(None, _x_24871, a_24867, a_24868, a_24869)
                                                                                            _x_24873 = RBTree_node(None, _x_24871, _x_24872, a_24843, _x_24870)
                                                                                            _x_24874 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24870, x_24440, _x_24873)
                                                                                            return _x_24874
                                                                                        case RBTree_node(a_24875, a_24876, a_24877, a_24878):
                                                                                            match a_24875:
                                                                                                case red():
                                                                                                    _x_24879 = RBTree_empty(None)
                                                                                                    _x_24880 = red()
                                                                                                    _x_24881 = RBTree_node(None, _x_24880, a_24867, a_24868, a_24869)
                                                                                                    _x_24882 = RBTree_node(None, _x_24880, a_24876, a_24877, a_24878)
                                                                                                    _x_24883 = RBTree_node(None, _x_24880, _x_24881, a_24843, _x_24882)
                                                                                                    _x_24884 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24879, x_24440, _x_24883)
                                                                                                    return _x_24884
                                                                                                case black():
                                                                                                    _x_24885 = RBTree_empty(None)
                                                                                                    _x_24886 = red()
                                                                                                    _x_24887 = RBTree_node(None, _x_24886, a_24867, a_24868, a_24869)
                                                                                                    _x_24888 = black()
                                                                                                    _x_24889 = RBTree_node(None, _x_24888, a_24876, a_24877, a_24878)
                                                                                                    _x_24890 = RBTree_node(None, _x_24886, _x_24887, a_24843, _x_24889)
                                                                                                    _x_24891 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24885, x_24440, _x_24890)
                                                                                                    return _x_24891
                                                                                case black():
                                                                                    match a_24844:
                                                                                        case RBTree_empty():
                                                                                            _x_24894 = RBTree_empty(None)
                                                                                            _x_24895 = red()
                                                                                            _x_24896 = black()
                                                                                            _x_24897 = RBTree_node(None, _x_24896, a_24867, a_24868, a_24869)
                                                                                            _x_24898 = RBTree_node(None, _x_24895, _x_24897, a_24843, _x_24894)
                                                                                            _x_24899 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24894, x_24440, _x_24898)
                                                                                            return _x_24899
                                                                                        case RBTree_node(a_24900, a_24901, a_24902, a_24903):
                                                                                            match a_24900:
                                                                                                case red():
                                                                                                    _x_24904 = RBTree_empty(None)
                                                                                                    _x_24905 = red()
                                                                                                    _x_24906 = black()
                                                                                                    _x_24907 = RBTree_node(None, _x_24906, a_24867, a_24868, a_24869)
                                                                                                    _x_24908 = RBTree_node(None, _x_24905, a_24901, a_24902, a_24903)
                                                                                                    _x_24909 = RBTree_node(None, _x_24905, _x_24907, a_24843, _x_24908)
                                                                                                    _x_24910 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24904, x_24440, _x_24909)
                                                                                                    return _x_24910
                                                                                                case black():
                                                                                                    _x_24911 = RBTree_empty(None)
                                                                                                    _x_24912 = red()
                                                                                                    _x_24913 = black()
                                                                                                    _x_24914 = RBTree_node(None, _x_24913, a_24867, a_24868, a_24869)
                                                                                                    _x_24915 = RBTree_node(None, _x_24913, a_24901, a_24902, a_24903)
                                                                                                    _x_24916 = RBTree_node(None, _x_24912, _x_24914, a_24843, _x_24915)
                                                                                                    _x_24917 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24911, x_24440, _x_24916)
                                                                                                    return _x_24917
                                                                case black():
                                                                    _x_24922 = RBTree_empty(None)
                                                                    _x_24923 = black()
                                                                    _x_24924 = RBTree_node(None, _x_24923, a_24842, a_24843, a_24844)
                                                                    _x_24925 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24922, x_24440, _x_24924)
                                                                    return _x_24925
                                                case RBTree_node(a_24928, a_24929, a_24930, a_24931):
                                                    match a_24928:
                                                        case red():
                                                            match x_24441:
                                                                case RBTree_empty():
                                                                    _x_24932 = red()
                                                                    _x_24933 = RBTree_node(None, _x_24932, a_24929, a_24930, a_24931)
                                                                    _x_24934 = RBTree_empty(None)
                                                                    _x_24935 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24933, x_24440, _x_24934)
                                                                    return _x_24935
                                                                case RBTree_node(a_24936, a_24937, a_24938, a_24939):
                                                                    match a_24936:
                                                                        case red():
                                                                            match a_24937:
                                                                                case RBTree_empty():
                                                                                    match a_24939:
                                                                                        case RBTree_empty():
                                                                                            _x_24940 = red()
                                                                                            _x_24941 = RBTree_node(None, _x_24940, a_24929, a_24930, a_24931)
                                                                                            _x_24942 = RBTree_empty(None)
                                                                                            _x_24943 = RBTree_node(None, _x_24940, _x_24942, a_24938, _x_24942)
                                                                                            _x_24944 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24941, x_24440, _x_24943)
                                                                                            return _x_24944
                                                                                        case RBTree_node(a_24945, a_24946, a_24947, a_24948):
                                                                                            match a_24945:
                                                                                                case red():
                                                                                                    _x_24949 = red()
                                                                                                    _x_24950 = RBTree_node(None, _x_24949, a_24929, a_24930, a_24931)
                                                                                                    _x_24951 = RBTree_empty(None)
                                                                                                    _x_24952 = RBTree_node(None, _x_24949, a_24946, a_24947, a_24948)
                                                                                                    _x_24953 = RBTree_node(None, _x_24949, _x_24951, a_24938, _x_24952)
                                                                                                    _x_24954 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24950, x_24440, _x_24953)
                                                                                                    return _x_24954
                                                                                                case black():
                                                                                                    _x_24955 = red()
                                                                                                    _x_24956 = RBTree_node(None, _x_24955, a_24929, a_24930, a_24931)
                                                                                                    _x_24957 = RBTree_empty(None)
                                                                                                    _x_24958 = black()
                                                                                                    _x_24959 = RBTree_node(None, _x_24958, a_24946, a_24947, a_24948)
                                                                                                    _x_24960 = RBTree_node(None, _x_24955, _x_24957, a_24938, _x_24959)
                                                                                                    _x_24961 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24956, x_24440, _x_24960)
                                                                                                    return _x_24961
                                                                                case RBTree_node(a_24964, a_24965, a_24966, a_24967):
                                                                                    match a_24964:
                                                                                        case red():
                                                                                            match a_24939:
                                                                                                case RBTree_empty():
                                                                                                    _x_24968 = red()
                                                                                                    _x_24969 = RBTree_node(None, _x_24968, a_24929, a_24930, a_24931)
                                                                                                    _x_24970 = RBTree_node(None, _x_24968, a_24965, a_24966, a_24967)
                                                                                                    _x_24971 = RBTree_empty(None)
                                                                                                    _x_24972 = RBTree_node(None, _x_24968, _x_24970, a_24938, _x_24971)
                                                                                                    _x_24973 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24969, x_24440, _x_24972)
                                                                                                    return _x_24973
                                                                                                case RBTree_node(a_24974, a_24975, a_24976, a_24977):
                                                                                                    match a_24974:
                                                                                                        case red():
                                                                                                            _x_24978 = red()
                                                                                                            _x_24979 = RBTree_node(None, _x_24978, a_24929, a_24930, a_24931)
                                                                                                            _x_24980 = RBTree_node(None, _x_24978, a_24965, a_24966, a_24967)
                                                                                                            _x_24981 = RBTree_node(None, _x_24978, a_24975, a_24976, a_24977)
                                                                                                            _x_24982 = RBTree_node(None, _x_24978, _x_24980, a_24938, _x_24981)
                                                                                                            _x_24983 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24979, x_24440, _x_24982)
                                                                                                            return _x_24983
                                                                                                        case black():
                                                                                                            _x_24984 = red()
                                                                                                            _x_24985 = RBTree_node(None, _x_24984, a_24929, a_24930, a_24931)
                                                                                                            _x_24986 = RBTree_node(None, _x_24984, a_24965, a_24966, a_24967)
                                                                                                            _x_24987 = black()
                                                                                                            _x_24988 = RBTree_node(None, _x_24987, a_24975, a_24976, a_24977)
                                                                                                            _x_24989 = RBTree_node(None, _x_24984, _x_24986, a_24938, _x_24988)
                                                                                                            _x_24990 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24985, x_24440, _x_24989)
                                                                                                            return _x_24990
                                                                                        case black():
                                                                                            match a_24939:
                                                                                                case RBTree_empty():
                                                                                                    _x_24993 = red()
                                                                                                    _x_24994 = RBTree_node(None, _x_24993, a_24929, a_24930, a_24931)
                                                                                                    _x_24995 = black()
                                                                                                    _x_24996 = RBTree_node(None, _x_24995, a_24965, a_24966, a_24967)
                                                                                                    _x_24997 = RBTree_empty(None)
                                                                                                    _x_24998 = RBTree_node(None, _x_24993, _x_24996, a_24938, _x_24997)
                                                                                                    _x_24999 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_24994, x_24440, _x_24998)
                                                                                                    return _x_24999
                                                                                                case RBTree_node(a_25000, a_25001, a_25002, a_25003):
                                                                                                    match a_25000:
                                                                                                        case red():
                                                                                                            _x_25004 = red()
                                                                                                            _x_25005 = RBTree_node(None, _x_25004, a_24929, a_24930, a_24931)
                                                                                                            _x_25006 = black()
                                                                                                            _x_25007 = RBTree_node(None, _x_25006, a_24965, a_24966, a_24967)
                                                                                                            _x_25008 = RBTree_node(None, _x_25004, a_25001, a_25002, a_25003)
                                                                                                            _x_25009 = RBTree_node(None, _x_25004, _x_25007, a_24938, _x_25008)
                                                                                                            _x_25010 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25005, x_24440, _x_25009)
                                                                                                            return _x_25010
                                                                                                        case black():
                                                                                                            _x_25011 = red()
                                                                                                            _x_25012 = RBTree_node(None, _x_25011, a_24929, a_24930, a_24931)
                                                                                                            _x_25013 = black()
                                                                                                            _x_25014 = RBTree_node(None, _x_25013, a_24965, a_24966, a_24967)
                                                                                                            _x_25015 = RBTree_node(None, _x_25013, a_25001, a_25002, a_25003)
                                                                                                            _x_25016 = RBTree_node(None, _x_25011, _x_25014, a_24938, _x_25015)
                                                                                                            _x_25017 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25012, x_24440, _x_25016)
                                                                                                            return _x_25017
                                                                        case black():
                                                                            _x_25022 = red()
                                                                            _x_25023 = RBTree_node(None, _x_25022, a_24929, a_24930, a_24931)
                                                                            _x_25024 = black()
                                                                            _x_25025 = RBTree_node(None, _x_25024, a_24937, a_24938, a_24939)
                                                                            _x_25026 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25023, x_24440, _x_25025)
                                                                            return _x_25026
                                                        case black():
                                                            match x_24441:
                                                                case RBTree_empty():
                                                                    _x_25029 = black()
                                                                    _x_25030 = RBTree_node(None, _x_25029, a_24929, a_24930, a_24931)
                                                                    _x_25031 = RBTree_empty(None)
                                                                    _x_25032 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25030, x_24440, _x_25031)
                                                                    return _x_25032
                                                                case RBTree_node(a_25033, a_25034, a_25035, a_25036):
                                                                    match a_25033:
                                                                        case red():
                                                                            match a_25034:
                                                                                case RBTree_empty():
                                                                                    match a_25036:
                                                                                        case RBTree_empty():
                                                                                            _x_25037 = black()
                                                                                            _x_25038 = RBTree_node(None, _x_25037, a_24929, a_24930, a_24931)
                                                                                            _x_25039 = red()
                                                                                            _x_25040 = RBTree_empty(None)
                                                                                            _x_25041 = RBTree_node(None, _x_25039, _x_25040, a_25035, _x_25040)
                                                                                            _x_25042 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25038, x_24440, _x_25041)
                                                                                            return _x_25042
                                                                                        case RBTree_node(a_25043, a_25044, a_25045, a_25046):
                                                                                            match a_25043:
                                                                                                case red():
                                                                                                    _x_25047 = black()
                                                                                                    _x_25048 = RBTree_node(None, _x_25047, a_24929, a_24930, a_24931)
                                                                                                    _x_25049 = red()
                                                                                                    _x_25050 = RBTree_empty(None)
                                                                                                    _x_25051 = RBTree_node(None, _x_25049, a_25044, a_25045, a_25046)
                                                                                                    _x_25052 = RBTree_node(None, _x_25049, _x_25050, a_25035, _x_25051)
                                                                                                    _x_25053 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25048, x_24440, _x_25052)
                                                                                                    return _x_25053
                                                                                                case black():
                                                                                                    _x_25054 = black()
                                                                                                    _x_25055 = RBTree_node(None, _x_25054, a_24929, a_24930, a_24931)
                                                                                                    _x_25056 = red()
                                                                                                    _x_25057 = RBTree_empty(None)
                                                                                                    _x_25058 = RBTree_node(None, _x_25054, a_25044, a_25045, a_25046)
                                                                                                    _x_25059 = RBTree_node(None, _x_25056, _x_25057, a_25035, _x_25058)
                                                                                                    _x_25060 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25055, x_24440, _x_25059)
                                                                                                    return _x_25060
                                                                                case RBTree_node(a_25063, a_25064, a_25065, a_25066):
                                                                                    match a_25063:
                                                                                        case red():
                                                                                            match a_25036:
                                                                                                case RBTree_empty():
                                                                                                    _x_25067 = black()
                                                                                                    _x_25068 = RBTree_node(None, _x_25067, a_24929, a_24930, a_24931)
                                                                                                    _x_25069 = red()
                                                                                                    _x_25070 = RBTree_node(None, _x_25069, a_25064, a_25065, a_25066)
                                                                                                    _x_25071 = RBTree_empty(None)
                                                                                                    _x_25072 = RBTree_node(None, _x_25069, _x_25070, a_25035, _x_25071)
                                                                                                    _x_25073 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25068, x_24440, _x_25072)
                                                                                                    return _x_25073
                                                                                                case RBTree_node(a_25074, a_25075, a_25076, a_25077):
                                                                                                    match a_25074:
                                                                                                        case red():
                                                                                                            _x_25078 = black()
                                                                                                            _x_25079 = RBTree_node(None, _x_25078, a_24929, a_24930, a_24931)
                                                                                                            _x_25080 = red()
                                                                                                            _x_25081 = RBTree_node(None, _x_25080, a_25064, a_25065, a_25066)
                                                                                                            _x_25082 = RBTree_node(None, _x_25080, a_25075, a_25076, a_25077)
                                                                                                            _x_25083 = RBTree_node(None, _x_25080, _x_25081, a_25035, _x_25082)
                                                                                                            _x_25084 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25079, x_24440, _x_25083)
                                                                                                            return _x_25084
                                                                                                        case black():
                                                                                                            _x_25085 = black()
                                                                                                            _x_25086 = RBTree_node(None, _x_25085, a_24929, a_24930, a_24931)
                                                                                                            _x_25087 = red()
                                                                                                            _x_25088 = RBTree_node(None, _x_25087, a_25064, a_25065, a_25066)
                                                                                                            _x_25089 = RBTree_node(None, _x_25085, a_25075, a_25076, a_25077)
                                                                                                            _x_25090 = RBTree_node(None, _x_25087, _x_25088, a_25035, _x_25089)
                                                                                                            _x_25091 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25086, x_24440, _x_25090)
                                                                                                            return _x_25091
                                                                                        case black():
                                                                                            match a_25036:
                                                                                                case RBTree_empty():
                                                                                                    _x_25094 = black()
                                                                                                    _x_25095 = RBTree_node(None, _x_25094, a_24929, a_24930, a_24931)
                                                                                                    _x_25096 = red()
                                                                                                    _x_25097 = RBTree_node(None, _x_25094, a_25064, a_25065, a_25066)
                                                                                                    _x_25098 = RBTree_empty(None)
                                                                                                    _x_25099 = RBTree_node(None, _x_25096, _x_25097, a_25035, _x_25098)
                                                                                                    _x_25100 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25095, x_24440, _x_25099)
                                                                                                    return _x_25100
                                                                                                case RBTree_node(a_25101, a_25102, a_25103, a_25104):
                                                                                                    match a_25101:
                                                                                                        case red():
                                                                                                            _x_25105 = black()
                                                                                                            _x_25106 = RBTree_node(None, _x_25105, a_24929, a_24930, a_24931)
                                                                                                            _x_25107 = red()
                                                                                                            _x_25108 = RBTree_node(None, _x_25105, a_25064, a_25065, a_25066)
                                                                                                            _x_25109 = RBTree_node(None, _x_25107, a_25102, a_25103, a_25104)
                                                                                                            _x_25110 = RBTree_node(None, _x_25107, _x_25108, a_25035, _x_25109)
                                                                                                            _x_25111 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25106, x_24440, _x_25110)
                                                                                                            return _x_25111
                                                                                                        case black():
                                                                                                            _x_25112 = black()
                                                                                                            _x_25113 = RBTree_node(None, _x_25112, a_24929, a_24930, a_24931)
                                                                                                            _x_25114 = red()
                                                                                                            _x_25115 = RBTree_node(None, _x_25112, a_25064, a_25065, a_25066)
                                                                                                            _x_25116 = RBTree_node(None, _x_25112, a_25102, a_25103, a_25104)
                                                                                                            _x_25117 = RBTree_node(None, _x_25114, _x_25115, a_25035, _x_25116)
                                                                                                            _x_25118 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25113, x_24440, _x_25117)
                                                                                                            return _x_25118
                                                                        case black():
                                                                            _x_25123 = black()
                                                                            _x_25124 = RBTree_node(None, _x_25123, a_24929, a_24930, a_24931)
                                                                            _x_25125 = RBTree_node(None, _x_25123, a_25034, a_25035, a_25036)
                                                                            _x_25126 = _alt_24448(a_24836, a_24837, a_24838, a_24536, _x_25124, x_24440, _x_25125)
                                                                            return _x_25126
                                        case black():
                                            match a_24537:
                                                case RBTree_empty():
                                                    match x_24441:
                                                        case RBTree_empty():
                                                            _x_25131 = black()
                                                            _x_25132 = red()
                                                            _x_25133 = RBTree_node(None, _x_25131, a_24836, a_24837, a_24838)
                                                            _x_25134 = RBTree_empty(None)
                                                            _x_25135 = RBTree_node(None, _x_25132, _x_25133, a_24536, _x_25134)
                                                            _x_25136 = _alt_24454(_x_25131, _x_25135, x_24440, _x_25134)
                                                            return _x_25136
                                                        case RBTree_node(a_25137, a_25138, a_25139, a_25140):
                                                            match a_25137:
                                                                case red():
                                                                    match a_25138:
                                                                        case RBTree_empty():
                                                                            match a_25140:
                                                                                case RBTree_empty():
                                                                                    _x_25141 = black()
                                                                                    _x_25142 = red()
                                                                                    _x_25143 = RBTree_node(None, _x_25141, a_24836, a_24837, a_24838)
                                                                                    _x_25144 = RBTree_empty(None)
                                                                                    _x_25145 = RBTree_node(None, _x_25142, _x_25143, a_24536, _x_25144)
                                                                                    _x_25146 = RBTree_node(None, _x_25142, _x_25144, a_25139, _x_25144)
                                                                                    _x_25147 = _alt_24454(_x_25141, _x_25145, x_24440, _x_25146)
                                                                                    return _x_25147
                                                                                case RBTree_node(a_25148, a_25149, a_25150, a_25151):
                                                                                    match a_25148:
                                                                                        case red():
                                                                                            _x_25152 = red()
                                                                                            _x_25153 = black()
                                                                                            _x_25154 = RBTree_node(None, _x_25153, a_24836, a_24837, a_24838)
                                                                                            _x_25155 = RBTree_empty(None)
                                                                                            _x_25156 = RBTree_node(None, _x_25152, _x_25154, a_24536, _x_25155)
                                                                                            _x_25157 = _alt_24451(_x_25156, x_24440, _x_25155, a_25139, a_25149, a_25150, a_25151)
                                                                                            return _x_25157
                                                                                        case black():
                                                                                            _x_25158 = black()
                                                                                            _x_25159 = red()
                                                                                            _x_25160 = RBTree_node(None, _x_25158, a_24836, a_24837, a_24838)
                                                                                            _x_25161 = RBTree_empty(None)
                                                                                            _x_25162 = RBTree_node(None, _x_25159, _x_25160, a_24536, _x_25161)
                                                                                            _x_25163 = RBTree_node(None, _x_25158, a_25149, a_25150, a_25151)
                                                                                            _x_25164 = RBTree_node(None, _x_25159, _x_25161, a_25139, _x_25163)
                                                                                            _x_25165 = _alt_24454(_x_25158, _x_25162, x_24440, _x_25164)
                                                                                            return _x_25165
                                                                        case RBTree_node(a_25168, a_25169, a_25170, a_25171):
                                                                            match a_25168:
                                                                                case red():
                                                                                    match a_25140:
                                                                                        case RBTree_empty():
                                                                                            _x_25172 = red()
                                                                                            _x_25173 = black()
                                                                                            _x_25174 = RBTree_node(None, _x_25173, a_24836, a_24837, a_24838)
                                                                                            _x_25175 = RBTree_empty(None)
                                                                                            _x_25176 = RBTree_node(None, _x_25172, _x_25174, a_24536, _x_25175)
                                                                                            _x_25177 = _alt_24450(_x_25176, x_24440, a_25169, a_25170, a_25171, a_25139, _x_25175)
                                                                                            return _x_25177
                                                                                        case RBTree_node(a_25178, a_25179, a_25180, a_25181):
                                                                                            match a_25178:
                                                                                                case red():
                                                                                                    _x_25182 = red()
                                                                                                    _x_25183 = black()
                                                                                                    _x_25184 = RBTree_node(None, _x_25183, a_24836, a_24837, a_24838)
                                                                                                    _x_25185 = RBTree_empty(None)
                                                                                                    _x_25186 = RBTree_node(None, _x_25182, _x_25184, a_24536, _x_25185)
                                                                                                    _x_25187 = RBTree_node(None, _x_25182, a_25179, a_25180, a_25181)
                                                                                                    _x_25188 = _alt_24450(_x_25186, x_24440, a_25169, a_25170, a_25171, a_25139, _x_25187)
                                                                                                    return _x_25188
                                                                                                case black():
                                                                                                    _x_25189 = red()
                                                                                                    _x_25190 = black()
                                                                                                    _x_25191 = RBTree_node(None, _x_25190, a_24836, a_24837, a_24838)
                                                                                                    _x_25192 = RBTree_empty(None)
                                                                                                    _x_25193 = RBTree_node(None, _x_25189, _x_25191, a_24536, _x_25192)
                                                                                                    _x_25194 = RBTree_node(None, _x_25190, a_25179, a_25180, a_25181)
                                                                                                    _x_25195 = _alt_24450(_x_25193, x_24440, a_25169, a_25170, a_25171, a_25139, _x_25194)
                                                                                                    return _x_25195
                                                                                case black():
                                                                                    match a_25140:
                                                                                        case RBTree_empty():
                                                                                            _x_25198 = black()
                                                                                            _x_25199 = red()
                                                                                            _x_25200 = RBTree_node(None, _x_25198, a_24836, a_24837, a_24838)
                                                                                            _x_25201 = RBTree_empty(None)
                                                                                            _x_25202 = RBTree_node(None, _x_25199, _x_25200, a_24536, _x_25201)
                                                                                            _x_25203 = RBTree_node(None, _x_25198, a_25169, a_25170, a_25171)
                                                                                            _x_25204 = RBTree_node(None, _x_25199, _x_25203, a_25139, _x_25201)
                                                                                            _x_25205 = _alt_24454(_x_25198, _x_25202, x_24440, _x_25204)
                                                                                            return _x_25205
                                                                                        case RBTree_node(a_25206, a_25207, a_25208, a_25209):
                                                                                            match a_25206:
                                                                                                case red():
                                                                                                    _x_25210 = red()
                                                                                                    _x_25211 = black()
                                                                                                    _x_25212 = RBTree_node(None, _x_25211, a_24836, a_24837, a_24838)
                                                                                                    _x_25213 = RBTree_empty(None)
                                                                                                    _x_25214 = RBTree_node(None, _x_25210, _x_25212, a_24536, _x_25213)
                                                                                                    _x_25215 = RBTree_node(None, _x_25211, a_25169, a_25170, a_25171)
                                                                                                    _x_25216 = _alt_24451(_x_25214, x_24440, _x_25215, a_25139, a_25207, a_25208, a_25209)
                                                                                                    return _x_25216
                                                                                                case black():
                                                                                                    _x_25217 = black()
                                                                                                    _x_25218 = red()
                                                                                                    _x_25219 = RBTree_node(None, _x_25217, a_24836, a_24837, a_24838)
                                                                                                    _x_25220 = RBTree_empty(None)
                                                                                                    _x_25221 = RBTree_node(None, _x_25218, _x_25219, a_24536, _x_25220)
                                                                                                    _x_25222 = RBTree_node(None, _x_25217, a_25169, a_25170, a_25171)
                                                                                                    _x_25223 = RBTree_node(None, _x_25217, a_25207, a_25208, a_25209)
                                                                                                    _x_25224 = RBTree_node(None, _x_25218, _x_25222, a_25139, _x_25223)
                                                                                                    _x_25225 = _alt_24454(_x_25217, _x_25221, x_24440, _x_25224)
                                                                                                    return _x_25225
                                                                case black():
                                                                    _x_25230 = black()
                                                                    _x_25231 = red()
                                                                    _x_25232 = RBTree_node(None, _x_25230, a_24836, a_24837, a_24838)
                                                                    _x_25233 = RBTree_empty(None)
                                                                    _x_25234 = RBTree_node(None, _x_25231, _x_25232, a_24536, _x_25233)
                                                                    _x_25235 = RBTree_node(None, _x_25230, a_25138, a_25139, a_25140)
                                                                    _x_25236 = _alt_24454(_x_25230, _x_25234, x_24440, _x_25235)
                                                                    return _x_25236
                                                case RBTree_node(a_25239, a_25240, a_25241, a_25242):
                                                    match a_25239:
                                                        case red():
                                                            match x_24441:
                                                                case RBTree_empty():
                                                                    _x_25243 = black()
                                                                    _x_25244 = RBTree_node(None, _x_25243, a_24836, a_24837, a_24838)
                                                                    _x_25245 = RBTree_empty(None)
                                                                    _x_25246 = _alt_24449(_x_25244, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25245)
                                                                    return _x_25246
                                                                case RBTree_node(a_25247, a_25248, a_25249, a_25250):
                                                                    match a_25247:
                                                                        case red():
                                                                            match a_25248:
                                                                                case RBTree_empty():
                                                                                    match a_25250:
                                                                                        case RBTree_empty():
                                                                                            _x_25251 = black()
                                                                                            _x_25252 = RBTree_node(None, _x_25251, a_24836, a_24837, a_24838)
                                                                                            _x_25253 = red()
                                                                                            _x_25254 = RBTree_empty(None)
                                                                                            _x_25255 = RBTree_node(None, _x_25253, _x_25254, a_25249, _x_25254)
                                                                                            _x_25256 = _alt_24449(_x_25252, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25255)
                                                                                            return _x_25256
                                                                                        case RBTree_node(a_25257, a_25258, a_25259, a_25260):
                                                                                            match a_25257:
                                                                                                case red():
                                                                                                    _x_25261 = black()
                                                                                                    _x_25262 = RBTree_node(None, _x_25261, a_24836, a_24837, a_24838)
                                                                                                    _x_25263 = red()
                                                                                                    _x_25264 = RBTree_empty(None)
                                                                                                    _x_25265 = RBTree_node(None, _x_25263, a_25258, a_25259, a_25260)
                                                                                                    _x_25266 = RBTree_node(None, _x_25263, _x_25264, a_25249, _x_25265)
                                                                                                    _x_25267 = _alt_24449(_x_25262, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25266)
                                                                                                    return _x_25267
                                                                                                case black():
                                                                                                    _x_25268 = black()
                                                                                                    _x_25269 = RBTree_node(None, _x_25268, a_24836, a_24837, a_24838)
                                                                                                    _x_25270 = red()
                                                                                                    _x_25271 = RBTree_empty(None)
                                                                                                    _x_25272 = RBTree_node(None, _x_25268, a_25258, a_25259, a_25260)
                                                                                                    _x_25273 = RBTree_node(None, _x_25270, _x_25271, a_25249, _x_25272)
                                                                                                    _x_25274 = _alt_24449(_x_25269, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25273)
                                                                                                    return _x_25274
                                                                                case RBTree_node(a_25277, a_25278, a_25279, a_25280):
                                                                                    match a_25277:
                                                                                        case red():
                                                                                            match a_25250:
                                                                                                case RBTree_empty():
                                                                                                    _x_25281 = black()
                                                                                                    _x_25282 = RBTree_node(None, _x_25281, a_24836, a_24837, a_24838)
                                                                                                    _x_25283 = red()
                                                                                                    _x_25284 = RBTree_node(None, _x_25283, a_25278, a_25279, a_25280)
                                                                                                    _x_25285 = RBTree_empty(None)
                                                                                                    _x_25286 = RBTree_node(None, _x_25283, _x_25284, a_25249, _x_25285)
                                                                                                    _x_25287 = _alt_24449(_x_25282, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25286)
                                                                                                    return _x_25287
                                                                                                case RBTree_node(a_25288, a_25289, a_25290, a_25291):
                                                                                                    match a_25288:
                                                                                                        case red():
                                                                                                            _x_25292 = black()
                                                                                                            _x_25293 = RBTree_node(None, _x_25292, a_24836, a_24837, a_24838)
                                                                                                            _x_25294 = red()
                                                                                                            _x_25295 = RBTree_node(None, _x_25294, a_25278, a_25279, a_25280)
                                                                                                            _x_25296 = RBTree_node(None, _x_25294, a_25289, a_25290, a_25291)
                                                                                                            _x_25297 = RBTree_node(None, _x_25294, _x_25295, a_25249, _x_25296)
                                                                                                            _x_25298 = _alt_24449(_x_25293, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25297)
                                                                                                            return _x_25298
                                                                                                        case black():
                                                                                                            _x_25299 = black()
                                                                                                            _x_25300 = RBTree_node(None, _x_25299, a_24836, a_24837, a_24838)
                                                                                                            _x_25301 = red()
                                                                                                            _x_25302 = RBTree_node(None, _x_25301, a_25278, a_25279, a_25280)
                                                                                                            _x_25303 = RBTree_node(None, _x_25299, a_25289, a_25290, a_25291)
                                                                                                            _x_25304 = RBTree_node(None, _x_25301, _x_25302, a_25249, _x_25303)
                                                                                                            _x_25305 = _alt_24449(_x_25300, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25304)
                                                                                                            return _x_25305
                                                                                        case black():
                                                                                            match a_25250:
                                                                                                case RBTree_empty():
                                                                                                    _x_25308 = black()
                                                                                                    _x_25309 = RBTree_node(None, _x_25308, a_24836, a_24837, a_24838)
                                                                                                    _x_25310 = red()
                                                                                                    _x_25311 = RBTree_node(None, _x_25308, a_25278, a_25279, a_25280)
                                                                                                    _x_25312 = RBTree_empty(None)
                                                                                                    _x_25313 = RBTree_node(None, _x_25310, _x_25311, a_25249, _x_25312)
                                                                                                    _x_25314 = _alt_24449(_x_25309, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25313)
                                                                                                    return _x_25314
                                                                                                case RBTree_node(a_25315, a_25316, a_25317, a_25318):
                                                                                                    match a_25315:
                                                                                                        case red():
                                                                                                            _x_25319 = black()
                                                                                                            _x_25320 = RBTree_node(None, _x_25319, a_24836, a_24837, a_24838)
                                                                                                            _x_25321 = red()
                                                                                                            _x_25322 = RBTree_node(None, _x_25319, a_25278, a_25279, a_25280)
                                                                                                            _x_25323 = RBTree_node(None, _x_25321, a_25316, a_25317, a_25318)
                                                                                                            _x_25324 = RBTree_node(None, _x_25321, _x_25322, a_25249, _x_25323)
                                                                                                            _x_25325 = _alt_24449(_x_25320, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25324)
                                                                                                            return _x_25325
                                                                                                        case black():
                                                                                                            _x_25326 = black()
                                                                                                            _x_25327 = RBTree_node(None, _x_25326, a_24836, a_24837, a_24838)
                                                                                                            _x_25328 = red()
                                                                                                            _x_25329 = RBTree_node(None, _x_25326, a_25278, a_25279, a_25280)
                                                                                                            _x_25330 = RBTree_node(None, _x_25326, a_25316, a_25317, a_25318)
                                                                                                            _x_25331 = RBTree_node(None, _x_25328, _x_25329, a_25249, _x_25330)
                                                                                                            _x_25332 = _alt_24449(_x_25327, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25331)
                                                                                                            return _x_25332
                                                                        case black():
                                                                            _x_25337 = black()
                                                                            _x_25338 = RBTree_node(None, _x_25337, a_24836, a_24837, a_24838)
                                                                            _x_25339 = RBTree_node(None, _x_25337, a_25248, a_25249, a_25250)
                                                                            _x_25340 = _alt_24449(_x_25338, a_24536, a_25240, a_25241, a_25242, x_24440, _x_25339)
                                                                            return _x_25340
                                                        case black():
                                                            match x_24441:
                                                                case RBTree_empty():
                                                                    _x_25343 = black()
                                                                    _x_25344 = red()
                                                                    _x_25345 = RBTree_node(None, _x_25343, a_24836, a_24837, a_24838)
                                                                    _x_25346 = RBTree_node(None, _x_25343, a_25240, a_25241, a_25242)
                                                                    _x_25347 = RBTree_node(None, _x_25344, _x_25345, a_24536, _x_25346)
                                                                    _x_25348 = RBTree_empty(None)
                                                                    _x_25349 = _alt_24454(_x_25343, _x_25347, x_24440, _x_25348)
                                                                    return _x_25349
                                                                case RBTree_node(a_25350, a_25351, a_25352, a_25353):
                                                                    match a_25350:
                                                                        case red():
                                                                            match a_25351:
                                                                                case RBTree_empty():
                                                                                    match a_25353:
                                                                                        case RBTree_empty():
                                                                                            _x_25354 = black()
                                                                                            _x_25355 = red()
                                                                                            _x_25356 = RBTree_node(None, _x_25354, a_24836, a_24837, a_24838)
                                                                                            _x_25357 = RBTree_node(None, _x_25354, a_25240, a_25241, a_25242)
                                                                                            _x_25358 = RBTree_node(None, _x_25355, _x_25356, a_24536, _x_25357)
                                                                                            _x_25359 = RBTree_empty(None)
                                                                                            _x_25360 = RBTree_node(None, _x_25355, _x_25359, a_25352, _x_25359)
                                                                                            _x_25361 = _alt_24454(_x_25354, _x_25358, x_24440, _x_25360)
                                                                                            return _x_25361
                                                                                        case RBTree_node(a_25362, a_25363, a_25364, a_25365):
                                                                                            match a_25362:
                                                                                                case red():
                                                                                                    _x_25366 = red()
                                                                                                    _x_25367 = black()
                                                                                                    _x_25368 = RBTree_node(None, _x_25367, a_24836, a_24837, a_24838)
                                                                                                    _x_25369 = RBTree_node(None, _x_25367, a_25240, a_25241, a_25242)
                                                                                                    _x_25370 = RBTree_node(None, _x_25366, _x_25368, a_24536, _x_25369)
                                                                                                    _x_25371 = RBTree_empty(None)
                                                                                                    _x_25372 = _alt_24451(_x_25370, x_24440, _x_25371, a_25352, a_25363, a_25364, a_25365)
                                                                                                    return _x_25372
                                                                                                case black():
                                                                                                    _x_25373 = black()
                                                                                                    _x_25374 = red()
                                                                                                    _x_25375 = RBTree_node(None, _x_25373, a_24836, a_24837, a_24838)
                                                                                                    _x_25376 = RBTree_node(None, _x_25373, a_25240, a_25241, a_25242)
                                                                                                    _x_25377 = RBTree_node(None, _x_25374, _x_25375, a_24536, _x_25376)
                                                                                                    _x_25378 = RBTree_empty(None)
                                                                                                    _x_25379 = RBTree_node(None, _x_25373, a_25363, a_25364, a_25365)
                                                                                                    _x_25380 = RBTree_node(None, _x_25374, _x_25378, a_25352, _x_25379)
                                                                                                    _x_25381 = _alt_24454(_x_25373, _x_25377, x_24440, _x_25380)
                                                                                                    return _x_25381
                                                                                case RBTree_node(a_25384, a_25385, a_25386, a_25387):
                                                                                    match a_25384:
                                                                                        case red():
                                                                                            match a_25353:
                                                                                                case RBTree_empty():
                                                                                                    _x_25388 = red()
                                                                                                    _x_25389 = black()
                                                                                                    _x_25390 = RBTree_node(None, _x_25389, a_24836, a_24837, a_24838)
                                                                                                    _x_25391 = RBTree_node(None, _x_25389, a_25240, a_25241, a_25242)
                                                                                                    _x_25392 = RBTree_node(None, _x_25388, _x_25390, a_24536, _x_25391)
                                                                                                    _x_25393 = RBTree_empty(None)
                                                                                                    _x_25394 = _alt_24450(_x_25392, x_24440, a_25385, a_25386, a_25387, a_25352, _x_25393)
                                                                                                    return _x_25394
                                                                                                case RBTree_node(a_25395, a_25396, a_25397, a_25398):
                                                                                                    match a_25395:
                                                                                                        case red():
                                                                                                            _x_25399 = red()
                                                                                                            _x_25400 = black()
                                                                                                            _x_25401 = RBTree_node(None, _x_25400, a_24836, a_24837, a_24838)
                                                                                                            _x_25402 = RBTree_node(None, _x_25400, a_25240, a_25241, a_25242)
                                                                                                            _x_25403 = RBTree_node(None, _x_25399, _x_25401, a_24536, _x_25402)
                                                                                                            _x_25404 = RBTree_node(None, _x_25399, a_25396, a_25397, a_25398)
                                                                                                            _x_25405 = _alt_24450(_x_25403, x_24440, a_25385, a_25386, a_25387, a_25352, _x_25404)
                                                                                                            return _x_25405
                                                                                                        case black():
                                                                                                            _x_25406 = red()
                                                                                                            _x_25407 = black()
                                                                                                            _x_25408 = RBTree_node(None, _x_25407, a_24836, a_24837, a_24838)
                                                                                                            _x_25409 = RBTree_node(None, _x_25407, a_25240, a_25241, a_25242)
                                                                                                            _x_25410 = RBTree_node(None, _x_25406, _x_25408, a_24536, _x_25409)
                                                                                                            _x_25411 = RBTree_node(None, _x_25407, a_25396, a_25397, a_25398)
                                                                                                            _x_25412 = _alt_24450(_x_25410, x_24440, a_25385, a_25386, a_25387, a_25352, _x_25411)
                                                                                                            return _x_25412
                                                                                        case black():
                                                                                            match a_25353:
                                                                                                case RBTree_empty():
                                                                                                    _x_25415 = black()
                                                                                                    _x_25416 = red()
                                                                                                    _x_25417 = RBTree_node(None, _x_25415, a_24836, a_24837, a_24838)
                                                                                                    _x_25418 = RBTree_node(None, _x_25415, a_25240, a_25241, a_25242)
                                                                                                    _x_25419 = RBTree_node(None, _x_25416, _x_25417, a_24536, _x_25418)
                                                                                                    _x_25420 = RBTree_node(None, _x_25415, a_25385, a_25386, a_25387)
                                                                                                    _x_25421 = RBTree_empty(None)
                                                                                                    _x_25422 = RBTree_node(None, _x_25416, _x_25420, a_25352, _x_25421)
                                                                                                    _x_25423 = _alt_24454(_x_25415, _x_25419, x_24440, _x_25422)
                                                                                                    return _x_25423
                                                                                                case RBTree_node(a_25424, a_25425, a_25426, a_25427):
                                                                                                    match a_25424:
                                                                                                        case red():
                                                                                                            _x_25428 = red()
                                                                                                            _x_25429 = black()
                                                                                                            _x_25430 = RBTree_node(None, _x_25429, a_24836, a_24837, a_24838)
                                                                                                            _x_25431 = RBTree_node(None, _x_25429, a_25240, a_25241, a_25242)
                                                                                                            _x_25432 = RBTree_node(None, _x_25428, _x_25430, a_24536, _x_25431)
                                                                                                            _x_25433 = RBTree_node(None, _x_25429, a_25385, a_25386, a_25387)
                                                                                                            _x_25434 = _alt_24451(_x_25432, x_24440, _x_25433, a_25352, a_25425, a_25426, a_25427)
                                                                                                            return _x_25434
                                                                                                        case black():
                                                                                                            _x_25435 = black()
                                                                                                            _x_25436 = red()
                                                                                                            _x_25437 = RBTree_node(None, _x_25435, a_24836, a_24837, a_24838)
                                                                                                            _x_25438 = RBTree_node(None, _x_25435, a_25240, a_25241, a_25242)
                                                                                                            _x_25439 = RBTree_node(None, _x_25436, _x_25437, a_24536, _x_25438)
                                                                                                            _x_25440 = RBTree_node(None, _x_25435, a_25385, a_25386, a_25387)
                                                                                                            _x_25441 = RBTree_node(None, _x_25435, a_25425, a_25426, a_25427)
                                                                                                            _x_25442 = RBTree_node(None, _x_25436, _x_25440, a_25352, _x_25441)
                                                                                                            _x_25443 = _alt_24454(_x_25435, _x_25439, x_24440, _x_25442)
                                                                                                            return _x_25443
                                                                        case black():
                                                                            _x_25448 = black()
                                                                            _x_25449 = red()
                                                                            _x_25450 = RBTree_node(None, _x_25448, a_24836, a_24837, a_24838)
                                                                            _x_25451 = RBTree_node(None, _x_25448, a_25240, a_25241, a_25242)
                                                                            _x_25452 = RBTree_node(None, _x_25449, _x_25450, a_24536, _x_25451)
                                                                            _x_25453 = RBTree_node(None, _x_25448, a_25351, a_25352, a_25353)
                                                                            _x_25454 = _alt_24454(_x_25448, _x_25452, x_24440, _x_25453)
                                                                            return _x_25454
                        case black():
                            match x_24441:
                                case RBTree_empty():
                                    _x_25461 = black()
                                    _x_25462 = RBTree_node(None, _x_25461, a_24535, a_24536, a_24537)
                                    _x_25463 = RBTree_empty(None)
                                    _x_25464 = _alt_24454(_x_25461, _x_25462, x_24440, _x_25463)
                                    return _x_25464
                                case RBTree_node(a_25465, a_25466, a_25467, a_25468):
                                    match a_25465:
                                        case red():
                                            match a_25466:
                                                case RBTree_empty():
                                                    match a_25468:
                                                        case RBTree_empty():
                                                            _x_25469 = black()
                                                            _x_25470 = RBTree_node(None, _x_25469, a_24535, a_24536, a_24537)
                                                            _x_25471 = red()
                                                            _x_25472 = RBTree_empty(None)
                                                            _x_25473 = RBTree_node(None, _x_25471, _x_25472, a_25467, _x_25472)
                                                            _x_25474 = _alt_24454(_x_25469, _x_25470, x_24440, _x_25473)
                                                            return _x_25474
                                                        case RBTree_node(a_25475, a_25476, a_25477, a_25478):
                                                            match a_25475:
                                                                case red():
                                                                    _x_25479 = black()
                                                                    _x_25480 = RBTree_node(None, _x_25479, a_24535, a_24536, a_24537)
                                                                    _x_25481 = RBTree_empty(None)
                                                                    _x_25482 = _alt_24451(_x_25480, x_24440, _x_25481, a_25467, a_25476, a_25477, a_25478)
                                                                    return _x_25482
                                                                case black():
                                                                    _x_25483 = black()
                                                                    _x_25484 = RBTree_node(None, _x_25483, a_24535, a_24536, a_24537)
                                                                    _x_25485 = red()
                                                                    _x_25486 = RBTree_empty(None)
                                                                    _x_25487 = RBTree_node(None, _x_25483, a_25476, a_25477, a_25478)
                                                                    _x_25488 = RBTree_node(None, _x_25485, _x_25486, a_25467, _x_25487)
                                                                    _x_25489 = _alt_24454(_x_25483, _x_25484, x_24440, _x_25488)
                                                                    return _x_25489
                                                case RBTree_node(a_25492, a_25493, a_25494, a_25495):
                                                    match a_25492:
                                                        case red():
                                                            match a_25468:
                                                                case RBTree_empty():
                                                                    _x_25496 = black()
                                                                    _x_25497 = RBTree_node(None, _x_25496, a_24535, a_24536, a_24537)
                                                                    _x_25498 = RBTree_empty(None)
                                                                    _x_25499 = _alt_24450(_x_25497, x_24440, a_25493, a_25494, a_25495, a_25467, _x_25498)
                                                                    return _x_25499
                                                                case RBTree_node(a_25500, a_25501, a_25502, a_25503):
                                                                    match a_25500:
                                                                        case red():
                                                                            _x_25504 = black()
                                                                            _x_25505 = RBTree_node(None, _x_25504, a_24535, a_24536, a_24537)
                                                                            _x_25506 = red()
                                                                            _x_25507 = RBTree_node(None, _x_25506, a_25501, a_25502, a_25503)
                                                                            _x_25508 = _alt_24450(_x_25505, x_24440, a_25493, a_25494, a_25495, a_25467, _x_25507)
                                                                            return _x_25508
                                                                        case black():
                                                                            _x_25509 = black()
                                                                            _x_25510 = RBTree_node(None, _x_25509, a_24535, a_24536, a_24537)
                                                                            _x_25511 = RBTree_node(None, _x_25509, a_25501, a_25502, a_25503)
                                                                            _x_25512 = _alt_24450(_x_25510, x_24440, a_25493, a_25494, a_25495, a_25467, _x_25511)
                                                                            return _x_25512
                                                        case black():
                                                            match a_25468:
                                                                case RBTree_empty():
                                                                    _x_25515 = black()
                                                                    _x_25516 = RBTree_node(None, _x_25515, a_24535, a_24536, a_24537)
                                                                    _x_25517 = red()
                                                                    _x_25518 = RBTree_node(None, _x_25515, a_25493, a_25494, a_25495)
                                                                    _x_25519 = RBTree_empty(None)
                                                                    _x_25520 = RBTree_node(None, _x_25517, _x_25518, a_25467, _x_25519)
                                                                    _x_25521 = _alt_24454(_x_25515, _x_25516, x_24440, _x_25520)
                                                                    return _x_25521
                                                                case RBTree_node(a_25522, a_25523, a_25524, a_25525):
                                                                    match a_25522:
                                                                        case red():
                                                                            _x_25526 = black()
                                                                            _x_25527 = RBTree_node(None, _x_25526, a_24535, a_24536, a_24537)
                                                                            _x_25528 = RBTree_node(None, _x_25526, a_25493, a_25494, a_25495)
                                                                            _x_25529 = _alt_24451(_x_25527, x_24440, _x_25528, a_25467, a_25523, a_25524, a_25525)
                                                                            return _x_25529
                                                                        case black():
                                                                            _x_25530 = black()
                                                                            _x_25531 = RBTree_node(None, _x_25530, a_24535, a_24536, a_24537)
                                                                            _x_25532 = red()
                                                                            _x_25533 = RBTree_node(None, _x_25530, a_25493, a_25494, a_25495)
                                                                            _x_25534 = RBTree_node(None, _x_25530, a_25523, a_25524, a_25525)
                                                                            _x_25535 = RBTree_node(None, _x_25532, _x_25533, a_25467, _x_25534)
                                                                            _x_25536 = _alt_24454(_x_25530, _x_25531, x_24440, _x_25535)
                                                                            return _x_25536
                                        case black():
                                            _x_25541 = black()
                                            _x_25542 = RBTree_node(None, _x_25541, a_24535, a_24536, a_24537)
                                            _x_25543 = RBTree_node(None, _x_25541, a_25466, a_25467, a_25468)
                                            _x_25544 = _alt_24454(_x_25541, _x_25542, x_24440, _x_25543)
                                            return _x_25544

# Lean: Corpus.Production.RBTree.insertAux
def insert_aux(__1755: Any, inst_25551: Any, x_1756: Any, x_25552: Any) -> Any:
    def _f_25556():
        _x_25553 = red()
        _x_25554 = RBTree_empty(None)
        _x_25555 = RBTree_node(None, _x_25553, _x_25554, x_1756, _x_25554)
        return _x_25555
    _alt_25557 = _f_25556
    def _f_25578(c_1758: Color, l_1759: Any, y_1760: Any, r_1761: Any):
        def _f_25560():
            _x_25558 = insert_aux(None, inst_25551, x_1756, l_1759)
            _x_25559 = balance(None, c_1758, _x_25558, y_1760, r_1761)
            return _x_25559
        _alt_25561 = _f_25560
        def _f_25563():
            _x_25562 = RBTree_node(None, c_1758, l_1759, y_1760, r_1761)
            return _x_25562
        _alt_25564 = _f_25563
        def _f_25567():
            _x_25565 = insert_aux(None, inst_25551, x_1756, r_1761)
            _x_25566 = balance(None, c_1758, l_1759, y_1760, _x_25565)
            return _x_25566
        _alt_25568 = _f_25567
        _x_25569 = inst_25551.ord_0
        _x_25570 = _x_25569(x_1756, y_1760)
        match _x_25570:
            case lt():
                _x_25572 = _alt_25561()
                return _x_25572
            case eq():
                _x_25574 = _alt_25564()
                return _x_25574
            case gt():
                _x_25576 = _alt_25568()
                return _x_25576
    _alt_25579 = _f_25578
    match x_25552:
        case RBTree_empty():
            _x_25581 = _alt_25557()
            return _x_25581
        case RBTree_node(a_25582, a_25583, a_25584, a_25585):
            _x_25586 = _alt_25579(a_25582, a_25583, a_25584, a_25585)
            return _x_25586

# Lean: Corpus.Production.RBTree.makeBlack
def make_black(__1765: Any, x_25589: Any) -> Any:
    def _f_25593(a_25590: Color, l_1766: Any, x_1767: Any, r_1768: Any):
        _x_25591 = black()
        _x_25592 = RBTree_node(None, _x_25591, l_1766, x_1767, r_1768)
        return _x_25592
    _alt_25594 = _f_25593
    def _f_25595(t_1769: Any):
        return t_1769
    _alt_25596 = _f_25595
    match x_25589:
        case RBTree_empty():
            _x_25597 = RBTree_empty(None)
            _x_25598 = _alt_25596(_x_25597)
            return _x_25598
        case RBTree_node(a_25599, a_25600, a_25601, a_25602):
            _x_25603 = _alt_25594(a_25599, a_25600, a_25601, a_25602)
            return _x_25603

# Lean: Corpus.Production.RBTree.insert
def rbtree_insert(__1770: Any, inst_25606: Any, x_1771: Any, t_1772: Any) -> Any:
    _x_25607 = insert_aux(None, inst_25606, x_1771, t_1772)
    _x_25608 = make_black(None, _x_25607)
    return _x_25608

# Lean: Corpus.Production.RBTree.toList
def to_list(__1773: Any, x_25610: Any) -> list[Any]:
    def _f_25612():
        _x_25611 = []
        return _x_25611
    _alt_25613 = _f_25612
    def _f_25624(a_25614: Color, l_1775: Any, x_1776: Any, r_1777: Any):
        _x_25618 = list(l_1775)
        _x_25619 = []
        _x_25620 = [x_1776] + _x_25619
        _x_25621 = _x_25618 + _x_25620
        _x_25622 = list(r_1777)
        _x_25623 = _x_25621 + _x_25622
        return _x_25623
    _alt_25625 = _f_25624
    match x_25610:
        case RBTree_empty():
            _x_25627 = _alt_25613()
            return _x_25627
        case RBTree_node(a_25628, a_25629, a_25630, a_25631):
            _x_25632 = _alt_25625(a_25628, a_25629, a_25630, a_25631)
            return _x_25632

# Lean: Corpus.Production.RBTree.fromList
def from_list(__1778: Any, inst_25635: Any, xs_1779: list[Any]) -> Any:
    def _f_25637(t_1780: Any, x_1781: Any):
        _x_25636 = rbtree_insert(None, inst_25635, x_1781, t_1780)
        return _x_25636
    _x_25638 = RBTree_empty(None)
    _x_25639 = functools.reduce(_f_25637, xs_1779, _x_25638)
    return _x_25639

# Lean: Corpus.Production.RBTree.size
def rbtree_size(__1782: Any, x_25641: Any) -> int:
    def _f_25645():
        _x_25642 = 0
        return 0
    _alt_25646 = _f_25645
    def _f_25659(a_25647: Color, l_1784: Any, a_25648: Any, r_1785: Any):
        _x_25652 = 1
        _x_25655 = rbtree_size(None, l_1784)
        _x_25656 = 1 + _x_25655
        _x_25657 = rbtree_size(None, r_1785)
        _x_25658 = _x_25656 + _x_25657
        return _x_25658
    _alt_25660 = _f_25659
    match x_25641:
        case RBTree_empty():
            _x_25662 = _alt_25646()
            return _x_25662
        case RBTree_node(a_25663, a_25664, a_25665, a_25666):
            _x_25667 = _alt_25660(a_25663, a_25664, a_25665, a_25666)
            return _x_25667

# Lean: Corpus.Production.RBTree.height
def height(__1786: Any, x_25670: Any) -> int:
    def _f_25674():
        _x_25671 = 0
        return 0
    _alt_25675 = _f_25674
    def _f_25690(a_25676: Color, l_1788: Any, a_25677: Any, r_1789: Any):
        _x_25681 = 1
        _x_25685 = max
        _x_25686 = height(None, l_1788)
        _x_25687 = height(None, r_1789)
        _x_25688 = _x_25685(_x_25686, _x_25687)
        _x_25689 = 1 + _x_25688
        return _x_25689
    _alt_25691 = _f_25690
    match x_25670:
        case RBTree_empty():
            _x_25693 = _alt_25675()
            return _x_25693
        case RBTree_node(a_25694, a_25695, a_25696, a_25697):
            _x_25698 = _alt_25691(a_25694, a_25695, a_25696, a_25697)
            return _x_25698

# Lean: Corpus.Production.RBTree.blackHeight
def black_height(__1790: Any, x_25701: Any) -> int:
    def _f_25705():
        _x_25702 = 1
        return 1
    _alt_25706 = _f_25705
    def _f_25730(c_1792: Color, l_1793: Any, a_25707: Any, a_25708: Any):
        _x_25714 = black()
        _x_25715 = c_1792 == _x_25714
        _x_25716 = True
        def _jp_25729(_y_25726: int):
            _x_25727 = black_height(None, l_1793)
            _x_25728 = _y_25726 + _x_25727
            return _x_25728
        if _x_25715:
            _x_25723 = 1
            return _jp_25729(1)
        else:
            _x_25719 = 0
            return _jp_25729(0)
    _alt_25731 = _f_25730
    match x_25701:
        case RBTree_empty():
            _x_25733 = _alt_25706()
            return _x_25733
        case RBTree_node(a_25734, a_25735, a_25736, a_25737):
            _x_25738 = _alt_25731(a_25734, a_25735, a_25736, a_25737)
            return _x_25738

# Lean: Corpus.Production.UnionFind.empty
def production_union_find_empty() -> UnionFind:
    _x_25741 = []
    _x_25742 = list(_x_25741)
    _x_25743 = UnionFind_mk(_x_25742)
    return _x_25743

# Lean: Corpus.Production.UnionFind.size
def production_union_find_size(uf_1794: UnionFind) -> int:
    _x_25744 = uf_1794.union_find_0
    _x_25745 = len(_x_25744)
    return _x_25745

# Lean: Corpus.Production.UnionFind.push
def production_union_find_push(uf_1795: UnionFind) -> UnionFind:
    _x_25747 = uf_1795.union_find_0
    _x_25748 = len(_x_25747)
    _x_25749 = 0
    _x_25752 = UFNode_mk(_x_25748, 0)
    _x_25753 = array_push(None, _x_25747, _x_25752)
    _x_25754 = UnionFind_mk(_x_25753)
    return _x_25754

# Lean: Corpus.Production.UnionFind.findWithPath
def find_with_path(nodes_1796: list[UFNode], x_1797: int) -> int:
    _x_25756 = len(nodes_1796)
    _x_25757 = x_1797 < _x_25756
    if _x_25757:
        _x_25759 = (lambda xs, i: 0 <= i < len(xs))
        _x_25760 = _x_25759(nodes_1796, x_1797, None)
        _x_25761 = _x_25760.ufnode_0
        _x_25764 = _x_25761 == x_1797
        _x_25765 = True
        if _x_25764:
            return x_1797
        else:
            _x_25768 = find_with_path(nodes_1796, _x_25761)
            return _x_25768
    else:
        return x_1797

# Lean: Corpus.Production.UnionFind.findRoot
def find_root(uf_1799: UnionFind, x_1800: int) -> int:
    _x_25773 = uf_1799.union_find_0
    _x_25774 = find_with_path(_x_25773, x_1800)
    return _x_25774

# Lean: Corpus.Production.UnionFind.connected
def connected(uf_1801: UnionFind, x_1802: int, y_1803: int) -> bool:
    _x_25778 = find_root(uf_1801, x_1802)
    _x_25779 = find_root(uf_1801, y_1803)
    _x_25780 = _x_25778 == _x_25779
    return _x_25780

# Lean: Corpus.Production.UnionFind.union
def union(uf_1804: UnionFind, x_1805: int, y_1806: int) -> UnionFind:
    _x_25782 = find_root(uf_1804, x_1805)
    _x_25783 = find_root(uf_1804, y_1806)
    _x_25786 = _x_25782 == _x_25783
    _x_25787 = True
    if _x_25786:
        return uf_1804
    else:
        _x_25790 = uf_1804.union_find_0
        _x_25791 = len(_x_25790)
        _x_25792 = _x_25782 < _x_25791
        if _x_25792:
            _x_25793 = _x_25783 < _x_25791
            if _x_25793:
                _x_25795 = (lambda xs, i: 0 <= i < len(xs))
                _x_25796 = _x_25795(_x_25790, _x_25782, None)
                _x_25797 = _x_25796.ufnode_1
                _x_25798 = _x_25795(_x_25790, _x_25783, None)
                _x_25799 = _x_25798.ufnode_1
                _x_25800 = _x_25797 < _x_25799
                if _x_25800:
                    _x_25822 = UFNode_mk(_x_25783, _x_25797)
                    _x_25823 = set_(None, _x_25790, _x_25782, _x_25822)
                    _x_25824 = UnionFind_mk(_x_25823)
                    return _x_25824
                else:
                    _x_25802 = _x_25799 < _x_25797
                    if _x_25802:
                        _x_25817 = UFNode_mk(_x_25782, _x_25799)
                        _x_25818 = set_(None, _x_25790, _x_25783, _x_25817)
                        _x_25819 = UnionFind_mk(_x_25818)
                        return _x_25819
                    else:
                        _x_25804 = UFNode_mk(_x_25782, _x_25799)
                        _x_25805 = set_(None, _x_25790, _x_25783, _x_25804)
                        _x_25809 = 1
                        _x_25812 = _x_25797 + 1
                        _x_25813 = UFNode_mk(_x_25782, _x_25812)
                        _x_25814 = set_(None, _x_25805, _x_25782, _x_25813)
                        _x_25815 = UnionFind_mk(_x_25814)
                        return _x_25815
            else:
                return uf_1804
        else:
            return uf_1804

# Lean: Corpus.Production.UnionFind.numComponents
def num_components(uf_1807: UnionFind) -> int:
    def _f_25843(i_1808: int):
        _x_25831 = uf_1807.union_find_0
        _x_25832 = len(_x_25831)
        _x_25833 = i_1808 < _x_25832
        if _x_25833:
            _x_25838 = (lambda xs, i: 0 <= i < len(xs))
            _x_25839 = _x_25838(_x_25831, i_1808, None)
            _x_25840 = _x_25839.ufnode_0
            _x_25841 = _x_25840 == i_1808
            return _x_25841
        else:
            _x_25834 = False
            return False
    _x_25844 = uf_1807.union_find_0
    _x_25845 = len(_x_25844)
    _x_25846 = list(range(_x_25845))
    _x_25847 = [x for x in _x_25846 if _f_25843(x)]
    _x_25848 = len(_x_25847)
    return _x_25848

# Lean: Corpus.Production.UnionFind.ofSize
def of_size(n_1810: int) -> UnionFind:
    _x_25850 = 0
    _x_25853 = []
    _x_25854 = list(_x_25853)
    _x_25855 = of_size_build(n_1810, 0, _x_25854)
    _x_25856 = UnionFind_mk(_x_25855)
    return _x_25856

# Lean: Corpus.Production.lomutoPartition
def lomuto_partition(arr_1811: list[int], lo_1812: int, hi_1813: int) -> tuple[list[int], int]:
    _x_25858 = hi_1813 <= lo_1812
    if _x_25858:
        _x_25870 = (arr_1811, lo_1812)
        return _x_25870
    else:
        def _f_25863(xs_1814: list[int], i_1815: int):
            _x_25861 = len(xs_1814)
            _x_25862 = i_1815 < _x_25861
            return _x_25862
        _x_25865 = _x_25864.get_elem__2
        _x_25867 = _x_25865(_x_25866, arr_1811, hi_1813)
        _x_25868 = lomuto_partition_go(hi_1813, _x_25867, arr_1811, lo_1812, lo_1812)
        return _x_25868

# Lean: Corpus.Production.quicksortAux
def quicksort_aux(arr_1817: list[int], lo_1818: int, hi_1819: int) -> list[int]:
    _x_25873 = hi_1819 <= lo_1818
    if _x_25873:
        return arr_1817
    else:
        def _f_25903(arr__1820: list[int], p_1821: int):
            _x_25875 = 0
            _x_25878 = 0 < p_1821
            def _jp_25902(_y_25889: list[int]):
                _x_25893 = 1
                _x_25896 = p_1821 + 1
                _x_25897 = _x_25896 < hi_1819
                if _x_25897:
                    _x_25900 = quicksort_aux(_y_25889, _x_25896, hi_1819)
                    return _x_25900
                else:
                    return _y_25889
            if _x_25878:
                _x_25884 = 1
                _x_25887 = p_1821 - 1
                _x_25888 = quicksort_aux(arr__1820, lo_1818, _x_25887)
                return _jp_25902(_x_25888)
            else:
                return _jp_25902(arr__1820)
        _alt_25904 = _f_25903
        _x_25905 = lomuto_partition(arr_1817, lo_1818, hi_1819)
        match _x_25905:
            case (fst_25906, snd_25907):
                _x_25908 = _alt_25904(fst_25906, snd_25907)
                return _x_25908

# Lean: Corpus.Production.quicksort
def quicksort(arr_1822: list[int]) -> list[int]:
    _x_25913 = len(arr_1822)
    _x_25914 = 1
    _x_25917 = _x_25913 <= 1
    if _x_25917:
        return arr_1822
    else:
        _x_25919 = 0
        _x_25925 = _x_25913 - 1
        _x_25926 = quicksort_aux(arr_1822, 0, _x_25925)
        return _x_25926

# Lean: Corpus.Production.naiveStringMatch
def naive_string_match(text: str, pattern: str) -> int | None:
    _x_25930 = list(text)
    _x_25931 = list(pattern)
    _x_25932 = len(_x_25930)
    _x_25933 = len(_x_25931)
    _x_25936 = 0
    _x_25939 = _x_25933 == 0
    _x_25940 = True
    if _x_25939:
        _x_25950 = 0
        return _x_25950
    else:
        _x_25943 = _x_25932 < _x_25933
        if _x_25943:
            _x_25947 = None
            return _x_25947
        else:
            _x_25945 = search(_x_25930, _x_25931, _x_25932, _x_25933, 0)
            return _x_25945

# Lean: Corpus.Production.naiveStringMatchAll
def naive_string_match_all(text_1827: str, pattern_1828: str) -> list[int]:
    _x_25953 = list(text_1827)
    _x_25954 = list(pattern_1828)
    _x_25955 = len(_x_25953)
    _x_25956 = len(_x_25954)
    _x_25959 = 0
    _x_25962 = _x_25956 == 0
    _x_25963 = True
    if _x_25962:
        _x_25977 = 1
        _x_25980 = _x_25955 + 1
        _x_25981 = list(range(_x_25980))
        return _x_25981
    else:
        _x_25966 = _x_25955 < _x_25956
        if _x_25966:
            _x_25971 = []
            return _x_25971
        else:
            _x_25968 = []
            _x_25969 = search(_x_25953, _x_25954, _x_25955, _x_25956, 0, _x_25968)
            return _x_25969

# Lean: Corpus.Production.computeZArray
def compute_zarray(s_1833: list[str]) -> list[int]:
    _x_25984 = len(s_1833)
    _x_25987 = 0
    _x_25990 = _x_25984 == 0
    _x_25991 = True
    if _x_25990:
        _x_26001 = []
        _x_26002 = list(_x_26001)
        return _x_26002
    else:
        _x_25994 = mk_array(None, _x_25984, 0)
        _x_25995 = set_(None, _x_25994, 0, _x_25984)
        _x_25996 = 1
        _x_25999 = compute(s_1833, _x_25984, _x_25995, 1, 0, 0)
        return _x_25999

# Lean: Corpus.Production.lcsLength
def lcs_length(xs_1837: list[int], ys_1838: list[int]) -> int:
    _x_26005 = len(xs_1837)
    _x_26006 = len(ys_1838)
    _x_26013 = 1
    _x_26016 = _x_26005 + 1
    _x_26017 = _x_26006 + 1
    _x_26018 = _x_26016 * _x_26017
    _x_26019 = 0
    _x_26022 = mk_array(None, _x_26018, 0)
    _x_26023 = fill(xs_1837, ys_1838, _x_26005, _x_26006, 0, 0, _x_26022)
    def _f_26027(xs_1843: list[int], i_1844: int):
        _x_26025 = len(xs_1843)
        _x_26026 = i_1844 < _x_26025
        return _x_26026
    _x_26029 = _x_26028.get_elem__2
    _x_26031 = _x_26005 * _x_26017
    _x_26032 = _x_26031 + _x_26006
    _x_26033 = _x_26029(_x_26030, _x_26023, _x_26032)
    return _x_26033

# Lean: Corpus.Production.lcs
def lcs(xs_1845: list[int], ys_1846: list[int]) -> list[int]:
    _x_26035 = len(xs_1845)
    _x_26036 = len(ys_1846)
    _x_26043 = 1
    _x_26046 = _x_26035 + 1
    _x_26047 = _x_26036 + 1
    _x_26048 = _x_26046 * _x_26047
    _x_26049 = 0
    _x_26052 = mk_array(None, _x_26048, 0)
    _x_26053 = fill(xs_1845, ys_1846, _x_26035, _x_26036, 0, 0, _x_26052)
    _x_26054 = []
    _x_26055 = backtrack(xs_1845, ys_1846, _x_26036, _x_26053, _x_26035, _x_26036, _x_26054)
    return _x_26055

# Lean: Corpus.Production.editDistance
def edit_distance(xs_1851: list[int], ys_1852: list[int]) -> int:
    _x_26057 = len(xs_1851)
    _x_26058 = len(ys_1852)
    _x_26065 = 1
    _x_26068 = _x_26057 + 1
    _x_26069 = _x_26058 + 1
    _x_26070 = _x_26068 * _x_26069
    _x_26071 = 0
    _x_26074 = mk_array(None, _x_26070, 0)
    _x_26075 = fill(xs_1851, ys_1852, _x_26057, _x_26058, 0, 0, _x_26074)
    def _f_26079(xs_1856: list[int], i_1857: int):
        _x_26077 = len(xs_1856)
        _x_26078 = i_1857 < _x_26077
        return _x_26078
    _x_26081 = _x_26080.get_elem__2
    _x_26083 = _x_26057 * _x_26069
    _x_26084 = _x_26083 + _x_26058
    _x_26085 = _x_26081(_x_26082, _x_26075, _x_26084)
    return _x_26085

# Lean: Corpus.Production.intervalScheduling
def interval_scheduling(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    _x_26087 = list(intervals)
    def _f_26092(a_1858: tuple[int, int], b_1859: tuple[int, int]):
        _x_26088 = a_1858[1]
        _x_26089 = b_1859[1]
        _x_26090 = _x_26088 < _x_26089
        return _x_26090
    _x_26093 = 0
    _x_26099 = len(_x_26087)
    _x_26100 = 1
    _x_26103 = _x_26099 - 1
    _x_26104 = sorted(0, key=functools.cmp_to_key(lambda a, b: -1 if _x_26103(a, b) else 1))
    _x_26105 = list(_x_26104)
    _x_26106 = []
    _x_26107 = select(_x_26105, 0, _x_26106)
    return _x_26107

# Lean: Corpus.Production.knapsack01
def knapsack01(capacity_1861: int, weights_1862: list[int], values_1863: list[int]) -> int:
    _x_26109 = len(weights_1862)
    _x_26116 = 1
    _x_26119 = _x_26109 + 1
    _x_26120 = capacity_1861 + 1
    _x_26121 = _x_26119 * _x_26120
    _x_26122 = 0
    _x_26125 = mk_array(None, _x_26121, 0)
    _x_26126 = fill(capacity_1861, weights_1862, values_1863, _x_26109, 0, 0, _x_26125)
    def _f_26130(xs_1867: list[int], i_1868: int):
        _x_26128 = len(xs_1867)
        _x_26129 = i_1868 < _x_26128
        return _x_26129
    _x_26132 = _x_26131.get_elem__2
    _x_26134 = _x_26109 * _x_26120
    _x_26135 = _x_26134 + capacity_1861
    _x_26136 = _x_26132(_x_26133, _x_26126, _x_26135)
    return _x_26136

# Lean: Corpus.Production.coinChange
def coin_change(coins_1869: list[int], amount_1870: int) -> int | None:
    _x_26141 = 1
    _x_26144 = amount_1870 + 1
    _x_26145 = mk_array(None, _x_26144, _x_26144)
    _x_26146 = 0
    _x_26149 = set_(None, _x_26145, 0, 0)
    _x_26150 = fill(coins_1869, amount_1870, _x_26144, 1, _x_26149)
    def _f_26154(xs_1875: list[int], i_1876: int):
        _x_26152 = len(xs_1875)
        _x_26153 = i_1876 < _x_26152
        return _x_26153
    _x_26156 = _x_26155.get_elem__2
    _x_26158 = _x_26156(_x_26157, _x_26150, amount_1870)
    _x_26159 = _x_26144 <= _x_26158
    if _x_26159:
        _x_26163 = None
        return _x_26163
    else:
        _x_26161 = _x_26158
        return _x_26161

# Lean: Corpus.Production.matrixChainOrder
def matrix_chain_order(dims_1877: list[int]) -> int:
    _x_26169 = len(dims_1877)
    _x_26170 = 1
    _x_26173 = _x_26169 - 1
    _x_26174 = _x_26173 <= 1
    if _x_26174:
        _x_26198 = 0
        return 0
    else:
        _x_26176 = 1000000000
        _x_26182 = _x_26173 * _x_26173
        _x_26183 = mk_array(None, _x_26182, 1000000000)
        _x_26184 = 0
        _x_26187 = fill(dims_1877, _x_26173, 1000000000, 1, 0, _x_26183)
        def _f_26191(xs_1882: list[int], i_1883: int):
            _x_26189 = len(xs_1882)
            _x_26190 = i_1883 < _x_26189
            return _x_26190
        _x_26193 = _x_26192.get_elem__2
        _x_26195 = _x_26173 - 1
        _x_26196 = _x_26193(_x_26194, _x_26187, _x_26195)
        return _x_26196

# Lean: Corpus.Production.lisLength
def lis_length(xs_1884: list[int]) -> int:
    _x_26203 = len(xs_1884)
    _x_26206 = 0
    _x_26209 = _x_26203 == 0
    _x_26210 = True
    if _x_26209:
        return 0
    else:
        _x_26213 = 1
        _x_26216 = mk_array(None, _x_26203, 1)
        _x_26217 = fill(xs_1884, _x_26203, 0, _x_26216)
        _x_26219 = max
        _x_26220 = len(_x_26217)
        _x_26221 = array_foldl(None, None, _x_26219, 0, _x_26217, 0, _x_26220)
        return _x_26221

# Lean: Corpus.Production.lis
def lis(xs_1888: list[int]) -> list[int]:
    _x_26225 = len(xs_1888)
    _x_26228 = 0
    _x_26231 = _x_26225 == 0
    _x_26232 = True
    if _x_26231:
        _x_26282 = []
        return _x_26282
    else:
        _x_26235 = 1
        _x_26238 = mk_array(None, _x_26225, 1)
        _x_26239 = mk_array(None, _x_26225, _x_26225)
        def _f_26274(dp__1892: list[int], parent__1893: list[int]):
            def _f_26243(fst_26240: int, max_idx: int):
                _x_26241 = []
                _x_26242 = backtrack(xs_1888, _x_26225, parent__1893, max_idx, _x_26241)
                return _x_26242
            _alt_26244 = _f_26243
            def _f_26266(x_26245: tuple[int, int], i_1894: int):
                def _f_26260(max_val_1895: int, max_i: int):
                    def _f_26249(xs_1896: list[int], i_1897: int):
                        _x_26247 = len(xs_1896)
                        _x_26248 = i_1897 < _x_26247
                        return _x_26248
                    _x_26251 = _x_26250.get_elem__2
                    _x_26253 = _x_26251(_x_26252, dp__1892, i_1894)
                    _x_26254 = max_val_1895 < _x_26253
                    if _x_26254:
                        _x_26258 = (_x_26253, i_1894)
                        return _x_26258
                    else:
                        _x_26256 = (max_val_1895, max_i)
                        return _x_26256
                _alt_26261 = _f_26260
                match x_26245:
                    case (fst_26262, snd_26263):
                        _x_26264 = _alt_26261(fst_26262, snd_26263)
                        return _x_26264
            _x_26267 = (0, 0)
            _x_26268 = list(range(_x_26225))
            _x_26269 = functools.reduce(_f_26266, _x_26268, _x_26267)
            match _x_26269:
                case (fst_26270, snd_26271):
                    _x_26272 = _alt_26244(fst_26270, snd_26271)
                    return _x_26272
        _alt_26275 = _f_26274
        _x_26276 = fill(xs_1888, _x_26225, 0, _x_26238, _x_26239)
        match _x_26276:
            case (fst_26277, snd_26278):
                _x_26279 = _alt_26275(fst_26277, snd_26278)
                return _x_26279

# Lean: Corpus.Production.maxSubarraySum
def max_subarray_sum(xs_1898: list[int]) -> int:
    def _f_26288():
        _x_26285 = 0
        return 0
    _alt_26289 = _f_26288
    def _f_26291(x_1900: int, rest_1901: list[int]):
        _x_26290 = kadane(rest_1901, x_1900, x_1900)
        return _x_26290
    _alt_26292 = _f_26291
    if len(xs_1898) == 0:
        _x_26294 = _alt_26289()
        return _x_26294
    else:
        head_26295 = xs_1898[0]
        tail_26296 = xs_1898[1:]
        _x_26297 = _alt_26292(head_26295, tail_26296)
        return _x_26297

# Lean: Corpus.Production.countInversions
def count_inversions(xs_1902: list[int]) -> int:
    _x_26300 = merge_count(xs_1902)
    _x_26301 = _x_26300[1]
    return _x_26301


