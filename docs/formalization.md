# Formalization — From ASN to Dafny

The formalization pipeline translates a converged ASN into a verified Dafny specification. Three steps, each building on the previous: classify properties into a proof index, extract formal statements, then generate Dafny per-property.

## How It Works

```
  ASN (converged)
       |
       v
[1] index         classify properties, assign proof labels
       |
       v
  proof index
       |
       v
[2] statements    extract formal statements from ASN prose
       |
       v
  statements file
       |
       v
[3] dafny         generate Dafny per-property (incremental)
       |
       v
  vault/3-modeling/dafny/ASN-NNNN/modeling-N/
       |
       v
[4] verify-dafny  three-tier verification loop
```

## Step 1: Proof Index

The proof index classifies each ASN property and assigns descriptive labels for use in Dafny. This is the bridge between the ASN's neutral labels (S0, PRE1, INS-F2) and the Dafny specification's descriptive names.

For each property, the index records:

| Field | Example | Purpose |
|-------|---------|---------|
| ASN Label | S0 | Original label in the ASN |
| Proof Label | VIGrounding | Descriptive PascalCase identifier for Dafny |
| Type | INV | Property classification (see below) |
| Construct | `predicate(State)` | Dafny construct to use |
| Notes | Transition invariant | Additional context |

### Property Types

| Type | Meaning | Dafny Construct |
|------|---------|-----------------|
| INV | State invariant | `predicate(State)` or `predicate(State, State)` for transitions |
| PRE | Precondition | `requires` clause on the operation function |
| POST | Postcondition | `ensures` clause on the operation function |
| FRAME | Frame condition | `ensures` clause specifying what does NOT change |
| LEMMA | Derived property | `lemma` — proved from other properties, erased at compile time |

### Re-run Stability

When re-run after an ASN revision, the existing proof index is fed back to the classification agent. Established labels and types are preserved. Only new or changed properties get new labels. Changes from the previous index are flagged in the output.

## Step 2: Statement Extraction

Extracts just the formal property statements from the ASN prose, indexed by the proof index. The ASN contains properties embedded in explanatory text — this step strips the narrative to produce a compact file suitable for Dafny generation.

The output lists each property with its proof label, type, and the precise formal statement from the ASN.

## Step 3: Dafny Generation

Translates the extracted statements into a Dafny module. Each run creates a new `modeling-N/` directory under `vault/3-modeling/dafny/ASN-NNNN/`. Verified files are manually promoted to `vault/proofs/` after review.

### Modeling Style: Functional Datatypes

The Dafny specification uses datatypes (immutable values), not classes. This is a deliberate modeling decision:

- **State is a value.** `datatype State = State(ispace: ..., poom: ..., ...)` — an immutable snapshot.
- **Operations are pure functions.** `function Insert(s: State, ...): (s': State)` — takes a state, returns a new state.
- **No heap.** No aliasing, no `reads this`, no `modifies` clauses, no dynamic frames.
- **Transition invariants are binary predicates.** `predicate IspaceImmutable(s: State, s': State)` — no `twostate` keyword needed.
- **Composition is natural.** `Delete(Insert(s, d, p, c), d, p2)` — function composition, not sequential method calls.

This matches the ASN's primed notation (`poom'(d)`, `ispace'`), which is a mathematical convention from Z/VDM/Event-B defining a relation over two values.

```dafny
datatype State = State(
  ispace: map<Addr, Content>,
  poom: map<DocId, map<Pos, Addr>>,
  links: set<Link>
)

predicate ValidState(s: State) {
  S0(s) && S2(s) && S3(s)
}

function Insert(s: State, d: DocId, p: Pos, c: seq<byte>): (s': State)
  requires ValidState(s) && PRE1(s, d) && PRE3(s, d, p)
  ensures ValidState(s')
  ensures IspaceImmutable(s, s')
  ensures s'.links == s.links  // frame
```

### Module Registry

`vault/3-modeling/modules.md` tracks the mapping from ASN numbers to Dafny module names, dependencies between modules, and generation status.

### Divergence and Failure Tracking

When the Dafny generation agent encounters a gap between the ASN property and what can be mechanically translated, it records a DIVERGENCE comment in the source. After generation, a review agent triages all divergences and verification failures:

- **Divergences** are classified as genuine spec issues (→ REVISE) or proof artifacts (→ SKIP)
- **Verification failures** are classified as spec issues (mathematical impossibility), proof limitations, or timeouts

Only findings classified as spec issues appear in the REVISE section. The review is written to `vault/2-review/` and the pipeline stops. You read the review and decide whether to run consult → revise manually.

## Artifacts

### Input

| Artifact | Location | Description |
|----------|----------|-------------|
| ASN | `vault/asns/ASN-NNNN-*.md` | Converged specification |
| Existing proof index | `vault/3-modeling/proof-index/ASN-NNNN-proof-index.md` | For re-run stability |
| Module registry | `vault/3-modeling/modules.md` | Module dependencies |

### Output

| Artifact | Location | Description |
|----------|----------|-------------|
| Proof index | `vault/3-modeling/proof-index/ASN-NNNN-proof-index.md` | Property classification table |
| Statements | `vault/3-modeling/formal-statements/ASN-NNNN-statements.md` | Extracted formal statements |
| Dafny modeling | `vault/3-modeling/dafny/ASN-NNNN/modeling-N/*.dfy` | Per-run staging output |
| Status | `vault/3-modeling/dafny/ASN-NNNN/modeling-N/STATUS.md` | Verification status, divergences, fix history |
| Dafny module (curated) | `vault/proofs/` | Manually promoted after review |

## CLI Reference

```bash
# Classify properties and assign proof labels
python scripts/model.py index 1

# Extract formal statements from ASN prose
python scripts/model.py statements 1

# Generate Dafny per-property (creates new modeling-N/ directory)
python scripts/model.py dafny 1

# Generate single property
python scripts/model.py dafny 1 --property TA4

# Add missing properties to an existing modeling run
python scripts/model.py dafny 1 --modeling 3

# Single property into existing run
python scripts/model.py dafny 1 --modeling 3 --property TA4

# Generate STATUS.md for an existing modeling directory
python scripts/model.py status 1
python scripts/model.py status 1 --modeling 1

# Fix unverified files with baby-steps
python scripts/model.py fix 1
python scripts/model.py fix 1 --property TA3

# Full formalization pipeline: index → statements → dafny → verify
python scripts/model.py verify-dafny 1 --full

# After verification, manually promote to vault/proofs/
cp vault/3-modeling/dafny/ASN-0001/modeling-1/*.dfy vault/proofs/ModuleName/
```

### Flags

| Flag | Description |
|------|-------------|
| `--property LABEL` | Process a single property only (dafny command) |
| `--modeling N` | Target existing modeling-N directory (skips already-generated properties) |
| `--no-alloy` | Skip injecting Alloy model as reference (included by default) |
| `--full` | Run complete pipeline: index → statements → generate → verify |

The `dafny` command generates, verifies, writes `STATUS.md`, and writes a review (for verified files with divergences) — then stops. Consult/revise is a separate manual step after reading the review.

### Additional Commands

| Command | Description |
|---------|-------------|
| `model.py status N` | Verify all .dfy files and write `STATUS.md` (no LLM generation) |
| `model.py fix N` | Fix unverified files with agentic baby-steps |
| `model.py fix N --property TA3` | Fix a single property |

## Path to Compiled Go

Dafny compiles datatypes to Go directly:

| Dafny | Go |
|-------|----|
| `datatype` | struct with functional update methods |
| `map<K,V>` | Dafny runtime persistent map (structure-sharing) |
| `function` | pure function |
| `lemma` | erased (proved at verification time only) |
| `requires`/`ensures` | runtime assertions (toggleable) |

The compiled Go serves as a verified reference implementation / test oracle. A thin stateful wrapper threads state:

```go
type Engine struct { state State }

func (e *Engine) Insert(d DocId, p Pos, c []byte) {
    e.state = Insert(e.state, d, p, c)
}
```

The verified pure function does the work; the wrapper provides a mutable API.

## Design Decisions

**Why three separate steps instead of one?** Each step produces an independently useful artifact. The proof index is used by Alloy checking and review. The statements file is a compact reference independent of Dafny syntax. Separating them allows re-running just the step that needs updating.

**Why functional datatypes?** The ASN is a specification, not an implementation. It describes WHAT relationship holds between pre-state and post-state, not HOW the transition is performed. Datatypes are neutral — they don't commit to mutability, heap allocation, or any particular implementation strategy.

**Why per-property generation?** Individual properties can be generated and verified independently. When one property needs revision, only that property's Dafny code is regenerated. This keeps iteration cycles fast.

**Why opus for index and dafny, sonnet for statements?** Property classification and Dafny generation require deep reasoning about formal semantics. Statement extraction is more structured — pulling formal text from known locations — and benefits from sonnet's speed.
