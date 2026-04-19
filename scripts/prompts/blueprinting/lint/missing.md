# Missing Dependency Check

You are checking whether a claim references any undeclared claims.

## Declared Labels

These labels exist in the claim table:

{{declared_labels}}

## Claim File

**Label:** {{label}}

{{content}}

## Task

Read the claim. Identify any labels cited as dependencies in the
proof, derivation, or formal contract that are NOT in the declared
labels list above.

A citation is a reference like "by T0", "from T3", "per TA5",
"using TumblerAdd" — where the label is used as a justification
or dependency, not just mentioned in passing.

Labels must match exactly as written. A reference to one label is not
satisfied by a different label that happens to share a prefix or look
similar. Each distinct label is its own claim.

## Output

For each missing label, write one line:

```
MISSING: LABEL — context where it's referenced
```

If all referenced labels are declared:

```
RESULT: CLEAN
```
