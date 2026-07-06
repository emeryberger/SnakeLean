/-
Main corpus test file - extracts all corpus functions to Python.
-/

import SnakeLean
import Corpus.Algorithms
import Corpus.DataStructures
import Corpus.Math
import Corpus.Functional
import Corpus.Strings
import Corpus.Games
import Corpus.Parsers

open Lean SnakeLean

-- Extract all algorithms
#eval show CoreM Unit from do
  let names := [
    -- Sorting
    `Corpus.Algorithms.insertionSort,
    `Corpus.Algorithms.merge,
    `Corpus.Algorithms.split,
    -- `Corpus.Algorithms.mergeSort,  -- partial

    -- Searching
    `Corpus.Algorithms.linearSearch,
    `Corpus.Algorithms.binarySearch,

    -- Numeric
    `Corpus.Algorithms.gcd,
    `Corpus.Algorithms.lcm,
    `Corpus.Algorithms.isPrime,
    `Corpus.Algorithms.primeFactors,
    `Corpus.Algorithms.fibonacci,
    `Corpus.Algorithms.power,

    -- List algorithms
    `Corpus.Algorithms.reverse,
    `Corpus.Algorithms.take,
    `Corpus.Algorithms.drop,
    `Corpus.Algorithms.filter,
    `Corpus.Algorithms.map,
    `Corpus.Algorithms.foldl,
    `Corpus.Algorithms.foldr,
    `Corpus.Algorithms.zip,
    `Corpus.Algorithms.unzip,
    `Corpus.Algorithms.concat,
    `Corpus.Algorithms.intersperse,
    `Corpus.Algorithms.span,
    `Corpus.Algorithms.partition,
    `Corpus.Algorithms.groupBy,

    -- String
    `Corpus.Algorithms.isPalindrome,
    `Corpus.Algorithms.countChar,
    `Corpus.Algorithms.replaceChar
  ]
  let code ← emitPythonForNames `Corpus.Algorithms names
  IO.println "# ==================== ALGORITHMS ===================="
  IO.println code

-- Extract math functions
#eval show CoreM Unit from do
  let names := [
    `Corpus.Math.abs,
    `Corpus.Math.sign,
    `Corpus.Math.min,
    `Corpus.Math.max,
    `Corpus.Math.clamp,
    `Corpus.Math.divMod,
    `Corpus.Math.pow,
    `Corpus.Math.fastPow,
    `Corpus.Math.modPow,
    `Corpus.Math.gcd,
    `Corpus.Math.lcm,
    `Corpus.Math.coprime,
    `Corpus.Math.isPrime,
    `Corpus.Math.primeFactors,
    `Corpus.Math.divisors,
    `Corpus.Math.numDivisors,
    `Corpus.Math.sumDivisors,
    `Corpus.Math.fibonacci,
    `Corpus.Math.lucas,
    `Corpus.Math.tribonacci,
    `Corpus.Math.factorial,
    `Corpus.Math.binomial,
    `Corpus.Math.catalan,
    `Corpus.Math.permutations,
    `Corpus.Math.triangularNumber,
    `Corpus.Math.squareNumber,
    `Corpus.Math.pentagonalNumber,
    `Corpus.Math.hexagonalNumber,
    `Corpus.Math.isTriangular,
    `Corpus.Math.isSquare,
    `Corpus.Math.digits,
    `Corpus.Math.fromDigits,
    `Corpus.Math.numDigits,
    `Corpus.Math.digitSum,
    `Corpus.Math.digitalRoot,
    `Corpus.Math.reverseDigits,
    `Corpus.Math.isPalindromeNum
  ]
  let code ← emitPythonForNames `Corpus.Math names
  IO.println "# ==================== MATH ===================="
  IO.println code

-- Extract functional programming constructs
#eval show CoreM Unit from do
  let names := [
    `Corpus.Functional.id,
    `Corpus.Functional.const,
    `Corpus.Functional.flip,
    `Corpus.Functional.compose,
    `Corpus.Functional.pipe,
    `Corpus.Functional.apply,
    `Corpus.Functional.curry,
    `Corpus.Functional.uncurry,
    `Corpus.Functional.Option.map,
    `Corpus.Functional.Option.bind,
    `Corpus.Functional.Option.filter,
    `Corpus.Functional.Option.getOrElse,
    `Corpus.Functional.Option.orElse,
    `Corpus.Functional.Option.zip,
    `Corpus.Functional.List.head?,
    `Corpus.Functional.List.tail?,
    `Corpus.Functional.List.last?,
    `Corpus.Functional.List.nth,
    `Corpus.Functional.List.updateAt,
    `Corpus.Functional.List.insertAt,
    `Corpus.Functional.List.removeAt,
    `Corpus.Functional.List.splitAt,
    `Corpus.Functional.List.takeWhile,
    `Corpus.Functional.List.dropWhile,
    `Corpus.Functional.List.replicate,
    `Corpus.Functional.List.scanl,
    `Corpus.Functional.List.interleave,
    `Corpus.Functional.Either.map,
    `Corpus.Functional.Either.mapLeft,
    `Corpus.Functional.Either.bind,
    `Corpus.Functional.Either.isLeft,
    `Corpus.Functional.Either.isRight
  ]
  let code ← emitPythonForNames `Corpus.Functional names
  IO.println "# ==================== FUNCTIONAL ===================="
  IO.println code

-- Extract string functions
#eval show CoreM Unit from do
  let names := [
    `Corpus.Strings.isEmpty,
    `Corpus.Strings.isNotEmpty,
    `Corpus.Strings.head,
    `Corpus.Strings.tail,
    `Corpus.Strings.last,
    `Corpus.Strings.init,
    `Corpus.Strings.take,
    `Corpus.Strings.drop,
    `Corpus.Strings.charAt,
    `Corpus.Strings.substring,
    `Corpus.Strings.slice,
    `Corpus.Strings.append,
    `Corpus.Strings.concat,
    `Corpus.Strings.intercalate,
    `Corpus.Strings.join,
    `Corpus.Strings.replicate,
    `Corpus.Strings.reverse,
    `Corpus.Strings.toUpper,
    `Corpus.Strings.toLower,
    `Corpus.Strings.capitalize,
    `Corpus.Strings.swapCase,
    `Corpus.Strings.trimLeft,
    `Corpus.Strings.trimRight,
    `Corpus.Strings.trim,
    `Corpus.Strings.padLeft,
    `Corpus.Strings.padRight,
    `Corpus.Strings.center,
    `Corpus.Strings.contains,
    `Corpus.Strings.indexOf,
    `Corpus.Strings.count,
    `Corpus.Strings.countChar,
    `Corpus.Strings.startsWith,
    `Corpus.Strings.endsWith,
    `Corpus.Strings.isPalindrome,
    `Corpus.Strings.isDigits,
    `Corpus.Strings.isAlpha,
    `Corpus.Strings.splitOn,
    `Corpus.Strings.lines,
    `Corpus.Strings.words,
    `Corpus.Strings.unlines,
    `Corpus.Strings.unwords,
    `Corpus.Strings.replace,
    `Corpus.Strings.replaceFirst,
    `Corpus.Strings.removePrefix,
    `Corpus.Strings.removeSuffix,
    `Corpus.Strings.toCharList,
    `Corpus.Strings.fromCharList,
    `Corpus.Strings.filterChars,
    `Corpus.Strings.mapChars,
    `Corpus.Strings.ord,
    `Corpus.Strings.chr,
    `Corpus.Strings.toAsciiCodes,
    `Corpus.Strings.fromAsciiCodes
  ]
  let code ← emitPythonForNames `Corpus.Strings names
  IO.println "# ==================== STRINGS ===================="
  IO.println code

-- Extract game functions
#eval show CoreM Unit from do
  let names := [
    `Corpus.Games.Player.other,
    `Corpus.Games.TicTacToe.empty,
    `Corpus.Games.TicTacToe.get,
    `Corpus.Games.TicTacToe.set,
    `Corpus.Games.TicTacToe.winner,
    `Corpus.Games.TicTacToe.isDraw,
    `Corpus.Games.TicTacToe.isOver,
    `Corpus.Games.TicTacToe.validMoves,
    `Corpus.Games.Nim.create,
    `Corpus.Games.Nim.take,
    `Corpus.Games.Nim.isOver,
    `Corpus.Games.Nim.nimSum,
    `Corpus.Games.Nim.isWinningPosition,
    `Corpus.Games.Card.value,
    `Corpus.Games.Card.isAce,
    `Corpus.Games.BlackjackHand.empty,
    `Corpus.Games.BlackjackHand.add,
    `Corpus.Games.BlackjackHand.hardValue,
    `Corpus.Games.BlackjackHand.numAces,
    `Corpus.Games.BlackjackHand.bestValue,
    `Corpus.Games.BlackjackHand.isBust,
    `Corpus.Games.BlackjackHand.isBlackjack,
    `Corpus.Games.roll,
    `Corpus.Games.rollDice,
    `Corpus.Games.sumDice,
    `Corpus.Games.yahtzeeScore,
    `Corpus.Games.RPS.beats,
    `Corpus.Games.RPS.compare,
    `Corpus.Games.RPS.fromNat,
    `Corpus.Games.isValidSudokuRow,
    `Corpus.Games.isValidSudokuGrid
  ]
  let code ← emitPythonForNames `Corpus.Games names
  IO.println "# ==================== GAMES ===================="
  IO.println code

-- Extract data structure functions
#eval show CoreM Unit from do
  let names := [
    `Corpus.DataStructures.Stack.empty,
    `Corpus.DataStructures.Stack.push,
    `Corpus.DataStructures.Stack.pop,
    `Corpus.DataStructures.Stack.peek,
    `Corpus.DataStructures.Stack.isEmpty,
    `Corpus.DataStructures.Stack.size,
    `Corpus.DataStructures.Queue.empty,
    `Corpus.DataStructures.Queue.enqueue,
    `Corpus.DataStructures.Queue.dequeue,
    `Corpus.DataStructures.Queue.isEmpty,
    `Corpus.DataStructures.Queue.size,
    `Corpus.DataStructures.BinaryTree.singleton,
    `Corpus.DataStructures.BinaryTree.size,
    `Corpus.DataStructures.BinaryTree.height,
    `Corpus.DataStructures.BinaryTree.inorder,
    `Corpus.DataStructures.BinaryTree.preorder,
    `Corpus.DataStructures.BinaryTree.postorder,
    `Corpus.DataStructures.BinaryTree.levelOrder,
    `Corpus.DataStructures.BinaryTree.mirror,
    `Corpus.DataStructures.BinaryTree.map,
    `Corpus.DataStructures.BinaryTree.fold,
    `Corpus.DataStructures.AssocList.empty,
    `Corpus.DataStructures.AssocList.insert,
    `Corpus.DataStructures.AssocList.lookup,
    `Corpus.DataStructures.AssocList.remove,
    `Corpus.DataStructures.AssocList.keys,
    `Corpus.DataStructures.AssocList.values,
    `Corpus.DataStructures.AssocList.size,
    `Corpus.DataStructures.Graph.empty,
    `Corpus.DataStructures.Graph.addVertex,
    `Corpus.DataStructures.Graph.addEdge,
    `Corpus.DataStructures.Graph.neighbors,
    `Corpus.DataStructures.Graph.degree,
    `Corpus.DataStructures.Graph.hasEdge,
    `Corpus.DataStructures.Trie.empty,
    `Corpus.DataStructures.Trie.insert,
    `Corpus.DataStructures.Trie.contains,
    `Corpus.DataStructures.Trie.hasPrefix
  ]
  let code ← emitPythonForNames `Corpus.DataStructures names
  IO.println "# ==================== DATA STRUCTURES ===================="
  IO.println code
