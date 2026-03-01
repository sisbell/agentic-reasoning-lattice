# Property Refinement

You are refining an ASN (Abstract Specification Note) that has reached review
maturity. Your task is to classify each property, assign a Dafny-ready name,
and produce a property mapping table.

This is a mechanical structuring task, not an analytical one. The hard reasoning
was done during review. You are making the structure explicit for Dafny
translation.

## Dafny modeling context

The specification uses Dafny **datatypes** (functional style). State is an
immutable value. Operations are pure functions from state to state:

```dafny
datatype State = State(ispace: map<Addr, Content>, poom: ..., ...)

// Invariant — named as adjective/descriptive predicate
predicate VIGrounding(s: State) { ... }
predicate IspaceImmutable(s: State, s': State) { ... }   // transition invariant
predicate PoomInjective(s: State) { ... }

function Insert(s: State, d: DocId, p: Pos, c: seq<byte>): (s': State)
  // Preconditions — named so "requires X" reads naturally
  requires DocExists(s, d)
  requires IsOwner(s, d, user)
  requires PositionValid(s, d, p)
  // Postconditions
  ensures FreshAddresses(s, s', d, c)
  ensures ContentPlacement(s', d, p, c)
  // Frame conditions — named for what's preserved
  ensures OtherDocsUnchanged(s, s', d)
  ensures LinksPreserved(s, s')
  // Invariant preservation
  ensures VIGrounding(s')
  ensures PoomInjective(s')
  ensures IspaceImmutable(s, s')

// Derived property — proved, not compiled
lemma InsertDomainSize(s: State, d: DocId, p: Pos, c: seq<byte>)
  ensures |Insert(s, d, p, c).poom[d]| == |s.poom[d]| + |c|
```

This means:
- No `modifies` clauses (no heap, no mutation)
- No `twostate predicate` (no heap). Transition invariants are regular
  `predicate` with signature `(State, State) -> bool`
- Frame conditions are `ensures` clauses comparing input and output state
- Derived properties and proofs are `lemma` (ghost — verified but not compiled)

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
| PRE  | Precondition | `requires` | Must hold before the operation executes |
| POST | Postcondition | `ensures` | Describes what the operation establishes |
| FRAME | Frame condition | `ensures` | States what the operation does NOT change |
| INV  | State invariant (single-state) | `predicate(State)` | Must hold in every reachable state |
| INV  | State invariant (transition) | `predicate(State, State)` | Relates pre-state to post-state (e.g., immutability, monotonicity) |
| LEMMA | Derived property | `lemma` | Follows logically from other properties; not independently assumed |

Classification rules:
- A property that says "for all operations" or "in every state" is INV
- A property that references both unprimed and primed state (or "never changes",
  "never loses", "append-only") is INV with construct `predicate(State, State)`
- A property that is explicitly derived/proved from others is LEMMA
- A property labeled as a "frame condition" in the ASN is FRAME
- A postcondition that describes what changes is POST; one that describes
  what doesn't change is FRAME
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
- For predicates, prefer adjective form: `PoomInjective`, `PositionsDense`
- For preconditions, prefer verb/noun form: `DocExists`, `IsOwner`, `PositionValid`
- For postconditions, prefer noun form: `FreshAddresses`, `ContentPlacement`
- For frame conditions, describe what's preserved: `OtherDocsUnchanged`, `LinksPreserved`

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
