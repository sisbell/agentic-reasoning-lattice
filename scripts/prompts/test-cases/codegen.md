# Generate Rust #[test] from Test Case

You translate a markdown test case file into a Rust `#[test]` module. You are given the oracle API (Dafny-generated Rust) and a test harness. Your job is to map each test case's abstract operations to the correct oracle function calls and harness helpers.

## How to read the oracle API

The oracle is generated from Dafny. Key patterns:

- **Modules**: `pub mod TumblerAlgebra { ... }`, `pub mod TumblerHierarchy { ... }`, etc.
- **Functions**: `pub fn FunctionName(arg: &Type, ...) -> ReturnType` inside `impl _default { ... }`
- **Call syntax**: `ModuleName::_default::FunctionName(&arg1, &arg2)`
- **Types**: `Rc<Tumbler>` is the tumbler type. `nat` is `DafnyInt`. `Sequence<nat>` is a Dafny sequence.
- **Integer literals**: use `int!(N)` macro for DafnyInt values
- **Sequences**: `Sequence::cardinality()` for length, `.get(&int!(i))` for 0-based access
- **Tumbler fields**: `.components()` returns `&Sequence<nat>`
- **Equality**: Dafny datatypes implement `PartialEq`/`Eq`, so `==` works

## How to read the harness

The harness provides helpers for things the oracle doesn't expose directly. Read the harness source to see what's available — construction helpers, comparison functions, gap-fillers for ghost predicates.

## Indexing

Test cases use **1-based** component indices. The oracle uses **0-based** Dafny sequences. When a test case references position N of a tumbler, use index N-1. This applies to:
- `at(t, k)` → `t.components().get(&int!(k - 1))`
- `sig(t) = N` → `LastNonzero` returns 0-based index, compare with `int!(N - 1)`

## Worked Example

Given this test case:

```markdown
## TC-001: proper prefix orders before its extension
**Property:** T1 case (ii)
**Given:**
p = [1, 0, 3]
d = [1, 0, 3, 0, 2]
**Assert:** `compare(p, d) == Less`
```

Looking at the harness, `tumbler_lt` implements lexicographic ordering. Emit:

```rust
#[test]
fn tc_001_proper_prefix_orders_before_its_extension() {
    let p = harness::tumbler(&[1, 0, 3]);
    let d = harness::tumbler(&[1, 0, 3, 0, 2]);
    assert!(harness::tumbler_lt(&p, &d));
}
```

## Mapping strategy

1. **Given** variables that look like `x = [1, 0, 3]` → `let x = harness::tumbler(&[1, 0, 3]);`
2. **Assert** operations → scan the oracle API for a matching function name and the harness for helpers. Match by name similarity (e.g., `add` → `TumblerAdd`, `zeros` → `ZeroCount`, `subtract` → `TumblerSubtract`).
3. **Comparisons** (`compare`, `lt`, `le`, `ordLt`, `ordLe`) → use the harness ordering functions.
4. **Validity checks** (`t3`, `t4`, `inc_valid`) → use harness helpers or oracle `ValidAddress`.
5. **Result equality** → compare with `harness::tumbler(&[...])` for tumbler results, `int!(N)` for integer results.
6. **Composite assertions** like `inc_valid(t, k) = true` → compute the operation and check the result: `ValidAddress(&AllocationInc(&t, &int!(k)))`.

## Output Format

Emit a complete Rust file. Include all potentially needed imports — unused imports are harmless:

```rust
mod harness;

use std::rc::Rc;
use dafny_runtime::{int, seq, DafnyInt, Sequence};
use dafny_runtime::_System::nat;
use xanadu_oracle::TumblerAlgebra;
use xanadu_oracle::TumblerHierarchy;
use xanadu_oracle::TumblerAlgebra::Tumbler;

// ... #[test] functions ...
```

Add `use` lines for any other oracle modules you call.

Rules:
- One `#[test]` function per `## TC-NNN` section
- Function name: `tc_NNN_{snake_case_short_name}` (from the TC heading)
- Skip the `## Skipped` section entirely — do not generate tests for skipped items
- Do not add `#[should_panic]` or `#[ignore]`
- Do not add helper functions — use the harness module
- Emit raw Rust — no markdown fences wrapping the output

**No simulated tool calls** — Do not attempt to read, fetch, or reference any files. You have everything you need in this prompt. Do not output XML tool-call markup.

## Oracle API

The following is the public API of the oracle (function signatures extracted from the compiled Dafny output):

```rust
{{ORACLE_API}}
```

## Harness

```rust
{{HARNESS}}
```

## Test Case

{{TEST_CASE}}
