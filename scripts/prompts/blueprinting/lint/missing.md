# Missing Dependency Check

You are checking whether a property references any undeclared properties.

## Declared Labels

These labels exist in the property table:

{{declared_labels}}

## Property File

**Label:** {{label}}

{{content}}

## Task

Read the property. Identify any labels cited as dependencies in the
proof, derivation, or formal contract that are NOT in the declared
labels list above.

A citation is a reference like "by T0", "from T3", "per TA5",
"using TumblerAdd" — where the label is used as a justification
or dependency, not just mentioned in passing.

## Output

For each missing label, write one line:

```
MISSING: LABEL — context where it's referenced
```

If all referenced labels are declared:

```
RESULT: CLEAN
```
