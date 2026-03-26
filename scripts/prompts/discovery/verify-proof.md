# Proof Verification

You are verifying a single property's proof in an Abstract Specification Note
(ASN) for the Xanadu hypertext system.

## Property to Verify

**Label**: {{label}}

### Property Section

{{property_section}}

### Dependencies

The following properties and definitions are referenced by this proof.
Use them as ground truth when checking the proof's reasoning.

{{dependency_sections}}

## Verification Checklist

1. **Precondition completeness** — Are all required inputs and conditions stated?
   What is assumed? Is anything missing?

2. **Case coverage** — Are all cases handled? Boundaries: empty inputs, zero values,
   equal operands, prefix pairs, maximum/minimum values. If the proof says "three
   cases arise," are there really only three?

3. **Postcondition establishment** — Does the proof actually establish what the
   property claims? Or does it say "by similar reasoning" or "follows similarly"
   without showing work?

4. **All conjuncts addressed** — If the property has multiple parts (a), (b), (c),
   is each one proved? Are any skipped?

5. **Dependency correctness** — Does the proof use the dependencies it claims?
   Are there dependencies used but not declared, or declared but not used?

## Output

If the proof is sound and complete:

```
RESULT: VERIFIED
```

If there is an issue:

```
RESULT: FOUND

**Problem**: [specific description of the gap, with concrete example if possible]
**Required**: [what would fix it]
```

Be specific. Cite the exact text that is wrong or missing. Construct a
counterexample if the proof misses a case.
