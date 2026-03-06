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

The verified foundation module. Start your file with:

```dafny
include "{{stable_root_filename}}"
```

This relative path resolves from your output file's location to the
foundation module in `vault/proofs/`.

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

## Proof strategy

The proof serves the spec. A good proof is one you can read in 30 seconds
and see WHY the property holds. Apply these principles:

**Trust the solver first.** Write the signature (requires/ensures), leave
the body empty `{ }`, and verify. Dafny's solver handles most obligations
automatically. Only add proof body when verification fails. An empty body
that verifies is the best proof.

**Bridge lemmas over inline assertions.** When the solver needs help,
factor out a named lemma that states the intermediate fact. Call the lemma
where needed. Inline `assert` chains that walk the solver through every
step are a sign of fighting the solver — step back and find the right
decomposition.

**Compositional structure.** If a proof has two independent parts (e.g.,
"CompareRec true implies LessThan" and "CompareRec false implies not
LessThan"), write two separate lemmas. Each should be independently
readable.

**Constructive helpers.** When a property involves existentials, introduce
a function that constructs the witness. This makes the proof obvious and
gives downstream consumers a computable witness.

**Sparse proof bodies.** In recursive/inductive proofs, handle only the
non-trivial cases. Empty branches (`else if ... { }`) tell the reader
"the solver handles this case" — which is more informative than explicit
assertions restating what the solver already knows.

**When verification fails, diagnose before reacting.** If adding an
assertion fixes it, ask: is there a simpler structural change (a helper
function, a stronger precondition on the recursive call, a different
decomposition) that makes the assertion unnecessary?

## Examples

These are verified examples showing the target quality. Study the proof
density — most proof bodies are nearly empty because the structure does
the work.

### Lemma — trust the solver

```dafny
// Irreflexivity follows directly from LessThan's definition
lemma Irreflexive(a: Tumbler)
  ensures !LexicographicOrder(a, a)
{ }

// Transitivity — the solver handles seq reasoning
lemma Transitive(a: Tumbler, b: Tumbler, c: Tumbler)
  requires LexicographicOrder(a, b)
  requires LexicographicOrder(b, c)
  ensures LexicographicOrder(a, c)
{ }

// Asymmetry — one composition, not case analysis
lemma Asymmetric(a: Tumbler, b: Tumbler)
  requires LexicographicOrder(a, b)
  ensures !LexicographicOrder(b, a)
{
  if LexicographicOrder(b, a) {
    Transitive(a, b, a);
    Irreflexive(a);
  }
}
```

### Recursive proof — sparse branches

```dafny
// Only the non-trivial case needs a body. The solver handles base cases.
lemma CompareTrue(a: seq<nat>, b: seq<nat>, i: nat)
  requires i <= |a| && i <= |b|
  requires CompareRec(a, b, i)
  requires forall j :: 0 <= j < i ==> a[j] == b[j]
  ensures LessThan(Tumbler(a), Tumbler(b))
  decreases |a| + |b| - 2 * i
{
  if i == |a| {
    // witness k = i; solver handles
  } else if i < |a| && i < |b| && a[i] < b[i] {
    // witness k = i; solver handles
  } else {
    CompareTrue(a, b, i + 1);
  }
}
```

### Constructive witness

```dafny
// Helper function constructs the witness — proof becomes trivial
function WithComponent(t: Tumbler, i: nat, v: nat): Tumbler
  requires 0 <= i < |t.components|
  ensures |WithComponent(t, i, v).components| == |t.components|
  ensures WithComponent(t, i, v).components[i] == v
  ensures forall j :: 0 <= j < |t.components| && j != i ==>
            WithComponent(t, i, v).components[j] == t.components[j]
{
  Tumbler(t.components[..i] + [v] + t.components[i+1..])
}

// Bridge: existential form for downstream consumers
lemma UnboundedComponentsExistential(t: Tumbler, i: nat, M: nat)
  requires 0 <= i < |t.components|
  ensures exists t': Tumbler ::
    |t'.components| == |t.components| &&
    t'.components[i] > M &&
    (forall j :: 0 <= j < |t.components| && j != i ==>
       t'.components[j] == t.components[j])
{
  var t' := WithComponent(t, i, M + 1);
}
```

### Compositional — one lemma call does the work

```dafny
// Cross-allocator ordering follows from pairwise PrefixOrderingExtension
lemma PartitionMonotonicity(
  p1: Tumbler, p2: Tumbler,
  stream1: seq<Tumbler>, stream2: seq<Tumbler>
)
  requires LessThan(p1, p2)
  requires NonNesting(p1, p2)
  requires AllExtend(stream1, p1) && AllExtend(stream2, p2)
  ensures forall i, j :: 0 <= i < |stream1| && 0 <= j < |stream2|
            ==> LessThan(stream1[i], stream2[j])
{
  forall i, j | 0 <= i < |stream1| && 0 <= j < |stream2|
    ensures LessThan(stream1[i], stream2[j])
  {
    PrefixOrderingExtension(p1, p2, stream1[i], stream2[j]);
  }
}
```

### Operation function

```dafny
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
