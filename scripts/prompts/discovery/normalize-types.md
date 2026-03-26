# Property Type Classification

You are classifying properties in an Abstract Specification Note (ASN) for
the Xanadu hypertext system. Each property in the property table needs a
type annotation.

## ASN Content

{{asn_content}}

## Task

The ASN contains a property table (headed `| Label | Statement | Status |`).
For each label in the table, determine the property's type from its definition
and usage in the ASN body.

## Types

| Type | Meaning | How to recognize |
|------|---------|------------------|
| INV | Invariant | Must hold in every reachable state. "For every state transition..." |
| LEMMA | Lemma | Derived result used by other properties. Proved from prior claims. |
| THEOREM | Theorem | Major derived result. Key conclusion of a proof chain. |
| PRE | Precondition | Must hold before an operation. "Requires...", "Given..." |
| POST | Postcondition | Guaranteed after an operation. "Ensures...", "After..." |
| DEF | Definition | Defines a concept, function, or structure. Not a claim — a construction. |
| FRAME | Frame condition | What does NOT change. "...is unchanged", "...is preserved" |
| META | Meta-property | About the specification itself, not the system. |

## Output format

Output one line per property label, in table order:

```
LABEL: TYPE
```

Example:
```
S0: INV
S1: LEMMA
ValidInsertionPosition: DEF
```

Output ONLY the label-type lines. No explanations, no commentary.
