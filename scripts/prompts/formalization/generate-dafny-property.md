# Dafny Property Generation

Translate a single formally extracted property into a verified Dafny
declaration. You receive one property — its extract entry, proof index row,
and the stable foundation module it imports.

## Modeling approach

Functional throughout — datatypes, pure functions, no heap:
- Operations are pure functions: `function Op(s: State, ...): State`
- No `modifies`, no `twostate predicate`, no heap reasoning
- Transition invariants are regular predicates over two states
- Lemmas are ghost — verified but erased from compiled output
- Use `ghost predicate` when the body has unbounded quantifiers

## Module assignment

Decide which module this property belongs in based on its domain. Place the
output file in that module's directory.

{{module_registry}}

## ASN notation → Dafny

| ASN notation | Dafny equivalent |
|-------------|------------------|
| `(A x : P(x) : Q(x))` | `forall x :: P(x) ==> Q(x)` |
| `(E x : P(x) : Q(x))` | `exists x :: P(x) && Q(x)` |
| `x ∈ S` | `x in S` |
| `m.x` or `m(x)` | `m[x]` |
| `S ∪ T` | `S + T` (sets) |
| `S ∩ T` | `S * T` (sets) |
| `S ∩ T = ∅` | `S !! T` (disjoint) |
| `#S` or `\|S\|` | `\|S\|` |
| `f'` (primed, post-state) | `s'.field` |

Use the functions and predicates defined in the stable foundation for
domain-specific operations (ordering, arithmetic, etc.).

## Dafny reference

Study these verified patterns carefully. Dafny is not Boogie, Why3, or Coq.

```dafny
{{dafny_reference}}
```

## Stable foundation

The verified foundation module. Your output file lives in the same
directory. Start your file with:

```dafny
include "{{stable_root_filename}}"
```

Then import it with `import opened`. Do not redefine anything already
defined here.

```dafny
{{stable_root}}
```

## Property to translate

**Proof index row (translate this row only):**

{{index_row}}

**Full extract (definitions and all properties for context):**

{{extract_entry}}

{{#if alloy_model}}
## Alloy reference

One formalization of this property in Alloy. Use for understanding structure
and edge cases. The extract is authoritative; do not adopt Alloy idioms.

```alloy
{{alloy_model}}
```
{{/if}}

## Examples

Match the conventions of the foundation module.

### Predicate

```dafny
// ASN-label — DafnyName
ghost predicate SomeInvariant(x: T, y: T) {
  forall i :: 0 <= i < |x.components| ==> P(x, y, i)
}
```

### Lemma

```dafny
// ASN-label — DafnyName
lemma SomeDerivedProperty(a: T, b: T, c: T)
  requires Precondition(a)
  requires Precondition(b)
  ensures Postcondition(a, b, c)
{ }
```

### Operation function

```dafny
// OperationName
function SomeOperation(s: State, args: ...): (s': State)
  requires ValidState(s)
  requires OperationPrecondition(s, args)
  ensures ValidState(s')
  ensures OperationPostcondition(s, s', args)
{
  assume false; s  // body is future work
}
```

## Output

Reply with raw Dafny source code only. No markdown fences, no commentary,
no tool calls, no explanation — just the Dafny code starting with
`include` or `module`.

The code should contain one module with one declaration. The module imports
the foundation, includes the ASN label as a comment for traceability, and
contains only the declaration being translated (plus any helpers it needs
that aren't in the foundation).
