#!/usr/bin/env python3

'''
The following is a simplified model checker for a specific problem. The aim is
to help readers understand how a model checker like Rumur works. It is written
in Python for readability, however the Rumur implementation is generated C code
optimised for both memory usage and execution speed. If you have read and
understood the following file, you will be in a position to start reading and
understanding ../rumur/resources/header.c.
'''

import sys
from typing import List, Optional, Set

class State(object):

  def __init__(self, initial_value: int = 5, size: int = 6, previous: Optional['State'] = None):

    # the state of our model; an array initialized with an initial value and size
         self.size = size
         self.arr = [5] * size

    # a pointer to the previous state, for the purpose of generating counter
    # example traces
         self.previous = previous

  def duplicate(self) -> 'State':
    'create a new State that will be a successor of this one'
    return State(self.arr, self.size, self)

  # make objects of this type storable in a set
  def __hash__(self) -> int:
    return Sum(self) #TODO Need to revise this 

def Sum(s: State) -> int:
  sum = 0
  for i in range(0, s.size):
      sum += s.arr[i]
  return sum

# an invariant we will claim, that the sum is never negative
def invariant(s: State) -> bool:
  return sum(s.arr) > 0


def decrement(s: State, index) -> None:
  val = s.arr[index]
  if(val >= 1):
      s.arr[index] = s.arr[index] - 1

# two rules and their accompanying guards
def dec__guard(s: State, index) -> bool:
  return s.arr[index] > 0

def dec__rule(s: State, index) -> None:
  decrement(s, index)
  if(index + 1 < s.size):
      if(s.arr[index + 1] > 0):
         decrement(s, index + 1)

# a start state that initially sets our value to 0
def start(s: State) -> None:
    for i in range(0, s.size):
      s.arr[i] = 5


def print_cex(s: State) -> None:
  'print a counter example trace ending at the given state'

  if s.previous is not None:
    print_cex(s.previous)

  # Print the value of this state. In a real world model checker like Rumur, you
  # would typically also print the transition rule that connected this state to
  # the previous to aid debugging.
  print(f' value == {s.value}')


def main() -> int:

  # A queue of states to be expanded and explored. Checking is done when this
  # queue is exhausted.
  pending: List[State] = []

  # A set of states we have already encountered. We use this to deduplicate
  # paths during exploration and avoid repeatedly checking the same states.
  seen: Set[State] = set()

  # we start with just our starting state in the queue
  s = State()
  start(s)
  pending.append(s)

  while len(pending) > 0:

    index = [0,1,2,3,4,5]
    # take the next state off the queue to be expanded
    n = pending.pop(0)
    
    # try each rule on it to generate new states
    for i in index:
        if dec__guard(n, i):
          e = n.duplicate()
          dec__rule(e, i)
      
        # Here is where symmetry reduction steps would usually take place in a
        # real model checker. These are used to further deduplicate states and
        # reduce the state space. For the purposes of this example, we omit such
        # optimisations.

        # Have we seen this new state before? If so, we can discard it as a
        # duplicate.
        if e in seen:
            continue

        # Does the state violate our invariant?
        if not invariant(e):
          print('counter example trace:')
          print_cex(e)
          return -1

        # note that we have seen this state for future checks
        seen.add(e)

        # add it to our queue and proceed
        pending.append(e)


  print('checking complete')

  return 0

if __name__ == '__main__':
  sys.exit(main())
