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

## Definitions

If a label's prose header starts with `**Definition`, classify it as DEFINITION.
Do NOT classify any other label as DEFINITION — only labels whose prose header
literally begins with the word "Definition". A property that defines an operation
(like an increment function) but uses a property-style header (`**LABEL (Name).**`)
is NOT a definition — classify it by what it claims (INV, LEMMA, PRE, etc.).

## Types

For all non-definition labels, choose from:

| Type | Meaning | How to recognize |
|------|---------|------------------|
| INV | Invariant | Must hold in every reachable state. "For every state transition..." |
| LEMMA | Lemma | Derived result used by other properties. Proved from prior claims. |
| THEOREM | Theorem | Major derived result. Key conclusion of a proof chain. |
| PRE | Precondition | Must hold before an operation. "Requires...", "Given..." |
| POST | Postcondition | Guaranteed after an operation. "Ensures...", "After..." |
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
OrdinalDisplacement: DEFINITION
TA5: INV
```

Output ONLY the label-type lines. No explanations, no commentary.
