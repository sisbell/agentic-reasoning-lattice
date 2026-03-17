# ASN-0045: Tumbler Fields

*2026-03-17*

The tumbler hierarchy (T4, ASN-0034) defines four field levels separated by zero components. We name the levels.

## Hierarchy Level Definitions

A tumbler's zero count determines which level of the hierarchy it identifies:

**E.node** — A *node* is a valid tumbler with zeros(t) = 0.

**E.account** — An *account* is a valid tumbler with zeros(t) = 1.

**E.document** — A *document* is a valid tumbler with zeros(t) = 2.

**E.element** — An *element* is a valid tumbler with zeros(t) = 3.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| E.node | Node: ValidAddress(t) ∧ zeros(t) = 0 | introduced |
| E.account | Account: ValidAddress(t) ∧ zeros(t) = 1 | introduced |
| E.document | Document: ValidAddress(t) ∧ zeros(t) = 2 | introduced |
| E.element | Element: ValidAddress(t) ∧ zeros(t) = 3 | introduced |
