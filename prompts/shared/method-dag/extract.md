# Method Dependency Extraction

You are extracting the **method-call dependency graph** from one converged
module design. The output drives a topological bucketing of contract
derivation: a method's contract is composed from the contracts of the methods
it calls, so we must know, for every public method, which other methods it
invokes.

Read the design. For each **public method** (the items in the Public interface —
the transact-driving ops, the pure composable steps, the reads, the fold, the
accessor methods), list the **other methods it calls** in its algorithm /
internal-design body.

## Module under analysis

{{module_id}}

## The design

{{design}}

## What counts as an edge

An edge `A → B` means method `A`'s body **invokes** method `B` (so `A`'s
contract is composed from `B`'s). Capture:

- **Cross-module calls** — e.g. `stg.working().m3().mint_content(doc)` ⇒ edge to
  `M3::mint_content`; `M4::stage_write(...)` ⇒ `M4::stage_write`; `m5.resolve(...)`
  ⇒ `M5::resolve`; `M1::shift(...)`/`inc`/`checked_inc`/`validate` ⇒ `M1::shift` etc.
- **Intra-module calls** — a method in this module calling another method in this
  module (a query it checks against, a helper it reuses).

Do **not** capture: field/slice access (`stg.working().m5()` is an accessor, not
a domain method — skip it unless a *named* method is then called on it), type
references, or M2 kernel primitives (`transact`, `snapshot`, `push` — these are
the substrate, not contract-bearing domain methods).

## Labels

Module-qualify every method as **`Mx::method_name`**. Determine the owning module
from the design's notation:
- `m3.` / `M3::` / `…m3().foo` ⇒ `M3::foo`
- `M1::` pure-algebra calls ⇒ `M1::name`
- a method defined in THIS design (no module prefix) ⇒ `{{module_id}}::name`

Use the exact method name as written (e.g. `mint_content`, `stage_write`,
`is_registered_document`, `resolve`, `apply_m5`).

## Output

Output ONLY valid YAML — no fences, no commentary:

```
module: {{module_id}}
methods:
  - label: {{module_id}}::<method>
    calls: [Mx::<callee>, My::<callee>, ...]   # [] if it calls no domain method
  - label: {{module_id}}::<method>
    calls: [...]
```

List every public method of this module, even leaves (`calls: []`). Include a
callee in `calls` even if it lives in another module — the driver resolves the
full cross-module graph.
