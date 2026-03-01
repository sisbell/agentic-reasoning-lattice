# Property Refinement

You are refining an ASN (Abstract Specification Note) that has reached review
maturity. Your task is to classify each property, assign a Dafny-ready name,
and produce a property mapping table.

This is a mechanical structuring task, not an analytical one. The hard reasoning
was done during review. You are making the structure explicit for Dafny
translation.

## Dafny modeling context

The specification uses Dafny **datatypes** (functional style). No `modifies`
clauses (no heap), no `twostate predicate`. Derived properties are `lemma`
(ghost — verified but not compiled).

ASNs fall into two layers. Determine which applies and use the matching pattern.

### Layer 1 — Type/algebra ASNs

Define a datatype and algebraic operations on it. Properties are about the
type itself and its operations:

```dafny
datatype Tumbler = Tumbler(components: seq<nat>)

// Type-level invariant — constraint on valid values
predicate ValidTumbler(t: Tumbler) { ... }
predicate PositiveComponents(t: Tumbler) { ... }

// Relation definition — ordering, containment, etc.
predicate LessThan(a: Tumbler, b: Tumbler) { ... }
predicate IsPrefix(a: Tumbler, b: Tumbler) { ... }

// Algebraic operation with pre/postconditions
function Add(a: Tumbler, w: Tumbler): (r: Tumbler)
  requires WellDefinedAddition(a, w)             // precondition
  ensures StrictIncrease(a, w, r)                // algebraic law
  ensures OrderPreservation(a, w, r)             // algebraic law

// Algebraic law — derived from operation definitions
lemma SubtractionPreservesOrder(a: Tumbler, b: Tumbler, w: Tumbler)
  requires LessThan(a, b) && a >= w && b >= w
  ensures LessThan(Subtract(a, w), Subtract(b, w))
```

### Layer 2 — State operation ASNs

Define operations that transform system state. Properties are preconditions,
postconditions, frame conditions, and state invariants:

```dafny
datatype State = State(ispace: map<Addr, Content>, poom: ..., ...)

// State invariant — named as adjective/descriptive predicate
predicate VIGrounding(s: State) { ... }
predicate PoomInjective(s: State) { ... }

// Transition invariant — regular predicate over two states
predicate IspaceImmutable(s: State, s': State) { ... }

function Insert(s: State, d: DocId, p: Pos, c: seq<byte>): (s': State)
  requires DocExists(s, d)                       // precondition
  requires IsOwner(s, d, user)
  ensures FreshAddresses(s, s', d, c)            // postcondition
  ensures ContentPlacement(s', d, p, c)
  ensures OtherDocsUnchanged(s, s', d)           // frame condition
  ensures LinksPreserved(s, s')
  ensures VIGrounding(s')                        // invariant preservation
  ensures IspaceImmutable(s, s')

// Derived property — proved, not compiled
lemma InsertDomainSize(s: State, d: DocId, p: Pos, c: seq<byte>)
  ensures |Insert(s, d, p, c).poom[d]| == |s.poom[d]| + |c|
```

## Input

### ASN Content

{{asn_content}}

### Shared Vocabulary

{{vocabulary}}

### Existing Mapping (if any)

{{existing_mapping}}

## Your Task

Produce a **property mapping table** — one row per formal property in the ASN.

### Step 1: Identify every formal property

Scan the ASN for every labeled formal property (bold label followed by a formal
statement). Properties have forms like:

- **S0 (V→I Grounding).** `formal statement`
- **PRE1 (Document existence).** `d ∈ dom.owner`
- **INS-F2 (Document isolation).** `(A d' : d' ≠ d : poom'(d') = poom(d'))`

### Step 2: Classify each property

| Type | Meaning | Dafny construct | How to recognize |
|------|---------|-----------------|------------------|
| INV  | Invariant (single-value) | `predicate(T)` or `predicate(State)` | Must hold for all valid values or in every reachable state |
| INV  | Invariant (relational) | `predicate(T, T)` or `predicate(State, State)` | Relates two values or two states (e.g., ordering, immutability, monotonicity) |
| PRE  | Precondition | `requires` | Must hold before the operation executes |
| POST | Postcondition | `ensures` | Describes what the operation establishes (algebraic law or state change) |
| FRAME | Frame condition | `ensures` | States what the operation does NOT change |
| LEMMA | Derived property | `lemma` | Follows logically from other properties; not independently assumed |

The type parameter in the Construct column reflects the domain — use the
actual type name (`Tumbler`, `State`, etc.), not a generic placeholder.

Classification rules:
- A property that says "for all operations", "in every state", or constrains
  all valid values of a type is INV
- A property that references both unprimed and primed state (or "never changes",
  "never loses", "append-only") is INV with a two-argument construct
- A relational property between two values of the same type (ordering,
  comparison, prefix relation) is INV with a two-argument construct
- A property that is explicitly derived/proved from others is LEMMA
  (includes corollaries and theorems)
- A property labeled as a "frame condition" in the ASN is FRAME
- A postcondition that describes what changes is POST; one that describes
  what doesn't change is FRAME
- Preconditions on algebraic operations (well-definedness) are PRE,
  same as preconditions on state operations
- System-level axioms (like append-only storage) are INV

### Step 3: Assign Dafny names

For each property, create a descriptive Dafny identifier from its **name**
(not its label). The name is the parenthesized text after the label:

- **S0 (V→I Grounding)** → `VIGrounding`
- **PRE1 (Document existence)** → `DocExists`
- **INS-F2 (Document isolation)** → `OtherDocsUnchanged`
- **INS-D1 (Domain size)** → `DomainSize`

Naming conventions:
- PascalCase (Dafny convention for predicates, lemmas, functions)
- Descriptive — the name should make sense in `requires DocExists(s, d)`
- Concise — aim for 1-3 words
- For invariants/predicates, prefer adjective form: `PoomInjective`, `PositionsDense`,
  `ValidTumbler`, `CanonicalRepresentation`
- For preconditions, prefer verb/noun form: `DocExists`, `IsOwner`,
  `WellDefinedAddition`
- For postconditions, prefer noun form: `FreshAddresses`, `ContentPlacement`,
  `OrderPreservation`, `StrictIncrease`
- For frame conditions, describe what's preserved: `OtherDocsUnchanged`, `LinksPreserved`
- For relational predicates, describe the relation: `LexicographicOrder`,
  `IntrinsicComparison`, `AddressPermanence`

If an existing mapping is provided, preserve Dafny names for properties that
haven't changed. Only generate new names for new or significantly changed
properties.

### Step 4: Add notes for special cases

Use the Notes column to flag:
- `derived from X` — for LEMMA properties, what they're derived from
- `split from X` — if a property was split during review
- `reclassified from TYPE` — if a review changed a property's nature
- `transition` — for INV properties with signature `(State, State)`
- Leave blank for straightforward mappings

## Output format

Produce ONLY a markdown document with a title and the mapping table. No other
content, no commentary, no preamble.

Type/algebra example:
```
# ASN-NNNN Property Mapping

| ASN Label | Dafny Name | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| T1 | LexicographicOrder | INV | predicate(Tumbler, Tumbler) | defines total order |
| T4 | HierarchicalParsing | INV | predicate(Tumbler) | structural constraint |
| T5 | ContiguousSubtrees | LEMMA | lemma | derived from T1 |
| T8 | AddressPermanence | INV | predicate(State, State) | transition |
| TA0 | WellDefinedAddition | PRE | requires | |
| TA1 | OrderPreservation | POST | ensures | algebraic law |
```

State operation example:
```
# ASN-NNNN Property Mapping

| ASN Label | Dafny Name | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| S0 | VIGrounding | INV | predicate(State) | |
| S1 | IspaceImmutable | INV | predicate(State, State) | transition |
| PRE1 | DocExists | PRE | requires | |
| INS1 | FreshAddresses | POST | ensures | |
| INS-F1 | IspaceUpperBound | FRAME | ensures | |
| INS-D1 | DomainSize | LEMMA | lemma | derived from INS3, INS4 |
```

Start directly with `# ASN-NNNN Property Mapping`.
