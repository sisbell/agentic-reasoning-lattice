# Modeling — From ASN to Dafny

The modeling pipeline translates a converged ASN into a verified Dafny specification. Three steps, each building on the previous: classify properties into a proof index, extract formal statements, then generate Dafny per-property.

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
[3] dafny         generate Dafny per-property, commit
       |
       v
  vault/4-modeling/dafny/ASN-NNNN/modeling-N/
       |
       v
[4] fix           fix unverified files iteratively
       |
       v
[5] status        re-verify, update STATUS.md, commit
       |
       v
[6] review        generate divergence review, commit
       |
       v
[7] verify-dafny  three-tier verification loop (full pipeline)
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

Translates the extracted statements into a Dafny module. Each run creates a new `modeling-N/` directory under `vault/4-modeling/dafny/ASN-NNNN/`. Verified files are manually promoted to `vault/proofs/` after review.

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

### Proof Imports

Each ASN's project model (`vault/project-model/ASN-NNNN/project.yaml`) has a `proof_imports` field listing the Dafny proof modules it needs. The Dafny generator reads all `.dfy` files from each listed module directory and injects their source into the generation prompt. Generated files use `import` statements; dfyconfig.toml handles resolution.

### Foundation ASNs

Foundation ASNs are identified by a `covers` field in their project model definition (`vault/project-model/ASN-NNNN/project.yaml`). Their formal statements are injected into every review, revise, and discovery prompt. Add a `covers` field after proofs are promoted to `vault/proofs/`. Foundation statements give downstream ASNs access to verified definitions without restating them.

### Divergence and Failure Tracking

When the Dafny generation agent encounters a gap between the ASN property and what can be mechanically translated, it records a DIVERGENCE comment in the source. The `dafny` command writes STATUS.md and commits — it does NOT auto-generate a review.

After fixing verification failures (`model.py fix N`) and updating status (`model.py status N`), you trigger the review manually (`model.py review N`). The review agent triages divergences from verified files:

- **Divergences** are classified as genuine spec issues (→ REVISE) or proof artifacts (→ SKIP)
- **Quality issues** are classified as over-proving, missing abstraction, or solver-fighting

Only findings classified as spec issues appear in the REVISE section. The review is written to `vault/2-review/` and committed. You read the review and act on the verdict.

### Review Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| **CONVERGED** | All divergences are proof artifacts, proofs are clean | Promote `.dfy` files to `vault/proofs/` |
| **SIMPLIFY** | No spec issues, but proofs need quality cleanup | Fix `.dfy` files, re-run `model.py review N` |
| **REVISE** | Dafny exposed a genuine spec issue | Fix the ASN via `revise.py N`, then re-run modeling |

A review with verdict REVISE may also contain QUALITY findings. Fix the ASN first (REVISE items change what gets proved), then address quality on the next modeling run.

#### CONVERGED

All divergences are proof artifacts (extra preconditions, helper lemmas, type coercions). The ASN is correct as stated. Promote verified `.dfy` files to `vault/proofs/`:

```bash
cp vault/4-modeling/dafny/ASN-NNNN/modeling-N/*.dfy vault/proofs/ModuleName/
python scripts/commit.py --proofs-only "promote ModuleName from modeling-N"
```

#### SIMPLIFY

No spec issues, but proofs have quality problems: duplicated helpers across files, over-proving (unnecessary assertions), missing abstraction, or fighting the solver. The review lists specific files and what to fix.

**This is a manual step.** There is no automated simplify command — read the review, make the changes by hand, verify with `dafny verify`, then re-run review to confirm.

```bash
# 1. Read the review findings and fix .dfy files manually
# 2. Verify each changed file: dafny verify <file>
# 3. Re-run review to confirm quality is clean
python scripts/model.py review N
# 4. Repeat until CONVERGED, then promote
```

#### REVISE

Dafny found a genuine spec problem — a property that's too strong, a missing precondition, or an ambiguity the proof exposed. The review describes the issue and proposes a fix.

```bash
# Revise the ASN from the Dafny review findings
python scripts/revise.py N
# Re-run the full modeling pipeline on the revised ASN
./run/remodel.sh N
```

## Artifacts

### Input

| Artifact | Location | Description |
|----------|----------|-------------|
| ASN | `vault/asns/ASN-NNNN-*.md` | Converged specification |
| Existing proof index | `vault/4-modeling/proof-index/ASN-NNNN-proof-index.md` | For re-run stability |
| Proof imports | `vault/project-model/ASN-NNNN/project.yaml` (proof_imports field) | Proof module dependencies per ASN |

### Output

| Artifact | Location | Description |
|----------|----------|-------------|
| Proof index | `vault/4-modeling/proof-index/ASN-NNNN-proof-index.md` | Property classification table |
| Statements | `vault/project-model/ASN-NNNN/formal-statements.md` | Extracted formal statements |
| Dafny modeling | `vault/4-modeling/dafny/ASN-NNNN/modeling-N/*.dfy` | Per-run staging output |
| Status | `vault/4-modeling/dafny/ASN-NNNN/modeling-N/STATUS.md` | Verification status, divergences, fix history |
| Dafny module (curated) | `vault/proofs/` | Manually promoted and committed (never auto-committed) |

## CLI Reference

```bash
# Classify properties and assign proof labels
# Extract formal statements from ASN prose
python scripts/export.py 1

python scripts/model.py index 1

# Generate Dafny per-property (creates new modeling-N/ directory)
python scripts/model.py dafny 1

# Generate single property
python scripts/model.py dafny 1 --property TA4

# Generate multiple specific properties
python scripts/model.py dafny 1 --property T1,T3,TA0

# Add missing properties to an existing modeling run
python scripts/model.py dafny 1 --modeling 3

# Single property into existing run
python scripts/model.py dafny 1 --modeling 3 --property TA4

# Generate STATUS.md and commit
python scripts/model.py status 1
python scripts/model.py status 1 --modeling 1

# Fix unverified files with baby-steps (no commit — iterate freely)
python scripts/model.py fix 1
python scripts/model.py fix 1 --property TA3

# Generate review of verified divergences and commit
python scripts/model.py review 1
python scripts/model.py review 1 --model sonnet

# Full modeling pipeline: index → statements → dafny → verify
python scripts/model.py verify-dafny 1 --full

# After verification, promote and commit with proofs-only mode
cp vault/4-modeling/dafny/ASN-0001/modeling-1/*.dfy vault/proofs/ModuleName/
python scripts/commit.py --proofs-only "promote ModuleName from modeling-1"
```

### Flags

| Flag | Description |
|------|-------------|
| `--property LABEL[,LABEL,...]` | Process specific properties, comma-separated (dafny, fix commands) |
| `--modeling N` | Target existing modeling-N directory (skips already-generated properties) |
| `--no-alloy` | Skip injecting Alloy model as reference (included by default) |
| `--full` | Run complete pipeline: index → statements → generate → verify |

The `dafny` command generates, verifies, writes `STATUS.md`, and commits. Review is a separate human-triggered step (`model.py review N`) after fixing failures and updating status.

### Additional Commands

| Command | Description |
|---------|-------------|
| `model.py status N` | Verify all .dfy files, write `STATUS.md`, commit |
| `model.py fix N` | Fix unverified files with agentic baby-steps (no commit) |
| `model.py fix N --property TA3` | Fix a single property |
| `model.py fix N --property T1,T3,TA0` | Fix multiple specific properties |
| `model.py review N` | Generate divergence review from verified files, commit |
| `model.py review N --model sonnet` | Use sonnet instead of opus for review |

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
