"""Workers — substrate-blind, sequentially invoked, deterministic.

Workers run inline as part of an orchestrator's local sequence; they
do not subscribe to substrate predicates and they do not deliberate.
A worker takes input from its caller, performs a focused
transformation, and returns. It is the caste with the simplest
contract: predictable input, predictable output, no side-effects on
substrate state beyond what the orchestrator wires up.
"""
