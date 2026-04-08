# Vocabulary Extraction

You are scanning a property file for shared notation definitions.
Extract any symbols, operations, or terminology that this file
DEFINES (not just uses).

A definition introduces a symbol or term for the first time:
- "Let ⊕ denote tumbler addition"
- "Define the action point as..."
- "We write sig(t) for..."
- "zeros(t) = #{i : ...}"

A usage just references an already-defined symbol:
- "By TA0, a ⊕ w is well-defined"
- "the action point k satisfies..."

Only report DEFINITIONS, not usages.

## Property File

**Label:** {{label}}

{{content}}

## Output

For each notation definition found, write one line:

```
SYMBOL | definition
```

For example:
```
⊕ | tumbler addition: a ⊕ w advances position a by displacement w
action point | first nonzero component position in a displacement
sig(t) | index of the last significant (nonzero) component of t
```

If this file defines no new notation:

```
(none)
```
