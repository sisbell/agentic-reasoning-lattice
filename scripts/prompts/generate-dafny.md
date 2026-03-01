# Dafny Specification Generation

You are translating formally extracted properties into a verified Dafny
specification module. The extract below contains definitions and properties
from an ASN, each with a Dafny name, type classification, and construct.
Your job is to produce correct, idiomatic Dafny code.

## Modeling approach

Use Dafny **datatypes** (functional style):
- State is an immutable value
- Operations are pure functions: `function Op(s: State, ...): State`
- No `modifies`, no `twostate predicate`, no heap reasoning
- Transition invariants are regular predicates: `predicate P(s: State, s': State)`
- Frame conditions are `ensures` clauses comparing input and output state
- Derived properties are `lemma` (ghost — verified but erased from compiled output)

## ASN notation → Dafny translation

| ASN notation | Dafny equivalent |
|-------------|------------------|
| `(A x : P(x) : Q(x))` | `forall x :: P(x) ==> Q(x)` |
| `(E x : P(x) : Q(x))` | `exists x :: P(x) && Q(x)` |
| `x ∈ dom.m` | `x in m` (for `map<K,V>`) |
| `m.x` or `m(x)` | `m[x]` |
| `x ∈ S` | `x in S` |
| `S ∪ T` | `S + T` (sets) |
| `S ∩ T` | `S * T` (sets) |
| `S ∩ T = ∅` | `S * T == {}` or `S !! T` (disjoint) |
| `#S` or `\|S\|` | `\|S\|` |
| `f'` (primed, post-state) | `s'.field` (compare `s.field` vs `s'.field`) |
| `poom(d)` | `s.poom[d]` |
| `poom'(d)` | `s'.poom[d]` |
| `ispace` | `s.ispace` |
| `dom.ispace` | `s.ispace.Keys` or use `in s.ispace` |

## Type definitions

Use these type aliases for clarity:

```dafny
type Addr = nat      // I-space address (tumbler, simplified to nat for now)
type Pos = nat       // V-space position
type DocId = nat     // document identifier
type Content = nat   // content value (byte)
type User = nat      // user/owner identifier
```

For Layer 1 (type/algebra) ASNs, define the primary datatype first:

```dafny
datatype Tumbler = Tumbler(components: seq<nat>)
```

For Layer 2 (state operation) ASNs, define the State datatype based on the
vocabulary and properties:

```dafny
datatype State = State(
  ispace: map<Addr, Content>,
  poom: map<DocId, map<Pos, Addr>>,
  spanindex: set<(Addr, DocId)>,
  links: set<Link>,
  owner: map<DocId, User>
)
```

Extend or adjust these types as needed by the properties.

## Vocabulary

{{vocabulary}}

## Extracted formal properties

{{extract}}

## Code generation rules

### Predicates (INV)

Translate each INV property to a `predicate` with the specified signature.
The body is the direct translation of the formal statement.

```dafny
predicate VIGrounding(s: State) {
  forall d, q :: d in s.poom && q in s.poom[d]
    ==> s.poom[d][q] in s.ispace
}
```

### Preconditions (PRE)

Translate each PRE to a `predicate` that can be used in `requires` clauses.

```dafny
predicate DocExists(s: State, d: DocId) {
  d in s.owner
}
```

### Postconditions and frame conditions (POST, FRAME)

Translate each POST/FRAME to a `predicate` over `(s: State, s': State, ...)`.
These are used in `ensures` clauses on the operation function.

```dafny
predicate OtherDocsUnchanged(s: State, s': State, d: DocId) {
  forall d' :: d' != d && d' in s.poom ==> d' in s'.poom && s'.poom[d'] == s.poom[d']
}
```

### Operation functions

If the extract contains an operation (INSERT, DELETE, etc.), generate the
function signature with all PRE as `requires` and all POST/FRAME/INV as
`ensures`. The body can use an `assume false; s` placeholder — the ensures
clauses ARE the specification. An executable body is a future step.

```dafny
function Insert(s: State, d: DocId, p: Pos, c: seq<Content>): (s': State)
  requires DocExists(s, d)
  requires IsOwner(s, d)
  requires PositionValid(s, d, p)
  requires ContentNonEmpty(c)
  ensures FreshAddresses(s, s', d, c)
  ensures ContentEstablished(s, s', c)
  // ... all POST, FRAME, INV ensures
{
  assume false; s  // specification only — body is future work
}
```

### Lemmas

Translate each LEMMA to a `lemma` declaration with appropriate requires
and ensures. Leave the proof body empty `{ }` — proofs are a future step.

```dafny
lemma DomainSize(s: State, s': State, d: DocId, p: Pos, c: seq<Content>)
  requires ValidState(s) && DocExists(s, d) && ...
  requires s' == Insert(s, d, p, c)
  ensures |s'.poom[d]| == |s.poom[d]| + |c|
{ }
```

### Definitions

Translate definitions to `function` declarations with executable bodies.

```dafny
function ActionPoint(w: seq<nat>): nat
  requires exists i :: 0 <= i < |w| && w[i] != 0
{
  var i :| 0 <= i < |w| && w[i] != 0 && forall j :: 0 <= j < i ==> w[j] == 0;
  i
}
```

### ValidState predicate

Generate a `ValidState` predicate that conjoins all single-state INV
predicates. This is used in requires/ensures for operations.

## Output format

Produce a single Dafny module. Structure:

```dafny
module ASN_NNNN {
  // Type aliases
  // Datatype definitions
  // Helper functions (from definitions)
  // Invariant predicates (INV)
  // ValidState
  // Precondition predicates (PRE)
  // Postcondition predicates (POST)
  // Frame condition predicates (FRAME)
  // Operation function(s)
  // Lemmas (LEMMA)
}
```

Use `//` comments to mark sections. Include a comment with the ASN label
before each predicate/lemma for traceability:

```dafny
// S0 — V→I Grounding
predicate VIGrounding(s: State) {
  ...
}
```

Output ONLY the raw Dafny code. Start directly with `module ASN_NNNN {`.
No markdown fences, no commentary before or after the code, no explanation.
