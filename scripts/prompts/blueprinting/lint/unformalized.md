# Unformalized Property Check

You are reviewing an ASN for properties that exist in the prose but are
not properly declared. A properly declared property has both:

1. A bold header: `**LABEL (PascalCaseName).**` or `**Definition (PascalCaseName).**`
2. A row in the property table

Read the entire ASN. Identify any content that defines, asserts, or
establishes a property — axioms, definitions, theorems, lemmas, design
requirements — that is missing either the bold header, the table entry,
or both.

Do NOT flag embedded sub-results within a property section (consequences,
case analyses, verification claims). Those are handled separately by
promote-inline.

## ASN Content

{{asn_content}}

## Output

For each unformalized property, write one finding:

```
LINE N | description of what the content establishes | what's missing (header, table entry, or both)
```

If everything is properly declared, write:

```
RESULT: CLEAN
```
