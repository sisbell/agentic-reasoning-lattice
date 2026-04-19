# Alloy Syntax Quick Reference

Distilled from Appendix B of *Software Abstractions* (Daniel Jackson).

## Declarations

```
sig S { f: expr }                     -- signature with field
abstract sig S {}                     -- abstract (no atoms unless extended)
sig A extends B { f: expr }           -- type signature (subtype of B)
sig A in B { f: expr }               -- subset signature (subset of B)
lone sig S {}                         -- at most one atom
one sig S {}                          -- exactly one atom

fact name { expr }                    -- named axiom
pred name[args] { expr }             -- predicate (boolean-valued)
fun name[args]: returnType { expr }  -- function (relation-valued)
assert name { expr }                  -- assertion (intended theorem)

check name for N                      -- check assertion within scope N
check name for N but M Sig            -- scope N, override Sig to M
run name for N                        -- search for instance within scope N
run name for N but exactly 2 State    -- exactly 2 atoms of State
```

## Scope Syntax

```
for N                                 -- default scope N for all top-level sigs
for N but M Sig                       -- override: M atoms of Sig
for N but M Sig, K seq               -- also limit seq length to K
for N but exactly M Sig              -- exactly M atoms of Sig
for N but B Int                       -- Int bitwidth B (must capitalize Int)
```

`but` is required before type-specific overrides. `Int` must be capitalized.

## Field Multiplicity in Declarations

```
f: E                                  -- f is a scalar (default: one E)
f: set E                              -- f is a set (any number of E)
f: lone E                             -- f is optional (zero or one E)
f: some E                             -- f is nonempty (one or more E)
f: A -> B                             -- f is a general relation
f: A -> lone B                        -- f is a partial function A->B
f: A -> one B                         -- f is a total function A->B
f: A one -> one B                     -- f is a bijection A<->B
```

## Operators by Precedence (tightest first)

| Precedence | Operators | Category |
|---|---|---|
| 1 (tightest) | `~` `^` `*` | unary: transpose, transitive closure, reflexive-transitive closure |
| 2 | `.` | dot join (relational join) |
| 3 | `[]` | box join: `a.b[c]` = `(a.b)[c]` |
| 4 | `<:` `:>` | domain restriction, range restriction |
| 5 | `->` | arrow product (Cartesian) |
| 6 | `&` | intersection |
| 7 | `++` | relational override |
| 8 | `#` | cardinality |
| 9 | `+` `-` | union, difference |
| 10 | `no` `some` `lone` `one` `set` | multiplicity/quantifier expressions |
| 11 | `!` `not` | comparison negation |
| 12 | `in` `=` `<` `>` `=<` `>=` | comparison |
| 13 | `&&` `and` | conjunction |
| 14 | `=>` `implies` `else` | implication (right-associative) |
| 15 | `<=>` `iff` | bi-implication |
| 16 | `\|\|` `or` | disjunction |
| 17 (loosest) | `let` `all` `no` `some` `lone` `one` `sum` | let-binding, quantification |

## Invocation Syntax

```
pred p[a, b, c] { ... }
fun f[a, b]: T { ... }

-- Invocation uses SQUARE brackets (not round):
p[x, y, z]                           -- predicate call
f[x, y]                              -- function call

-- Receiver (dot) syntax — first arg before the dot:
x.p[y, z]                            -- same as p[x, y, z]
x.f[y]                               -- same as f[x, y]

-- Box join is function application:
f[x]                                 -- equivalent to x.f
```

Declarations use `(round)` or `[square]` brackets. Invocations use only `[square]`.

## Relational Constants and Special Names

```
none                                  -- empty set (no tuples)
univ                                  -- universal set (all atoms)
iden                                  -- identity relation (binary: atom->atom)
this                                  -- current atom in sig facts
@f                                    -- field f without implicit dereference
```

`iden in r` means r is reflexive. `univ` and `iden` range over all atoms in scope.

## Relational Operator Semantics

```
~e                                    -- transpose (reverse tuples)
^e                                    -- transitive closure (e must be binary)
*e                                    -- reflexive-transitive closure = ^e + iden
e1 . e2                               -- join: match last col of e1 with first of e2
e2 [e1]                               -- box join: same as e1.e2
e1 -> e2                              -- Cartesian product
e2 <: e1                              -- domain restriction: tuples in e1 starting with e2
e1 :> e2                              -- range restriction: tuples in e1 ending with e2
e1 ++ e2                              -- override: e2, plus e1 tuples not sharing first col with e2
e1 & e2                               -- intersection (same-arity required)
e1 + e2                               -- union (same-arity required)
e1 - e2                               -- difference (same-arity required)
#e                                    -- cardinality (integer)
```

Comprehension (set builder): `{x1: E1, x2: E2 | F}` — tuples x1->x2->... where F holds. Bounding expressions must be unary (sets). No multiplicity keywords in comprehension decls (except `disj`).

## Integer Expressions

```
-- Int scope is BITWIDTH, not count. "4 Int" = 4 bits = values -8..+7
-- Arithmetic uses built-in functions (box/dot invocation):
plus[a, b]    or  a.plus[b]          -- addition
minus[a, b]   or  a.minus[b]         -- subtraction
mul[a, b]     or  a.mul[b]           -- multiplication
div[a, b]     or  a.div[b]           -- integer division
rem[a, b]     or  a.rem[b]           -- remainder

#e                                    -- cardinality (number of tuples)
sum x: E | intExpr                    -- distributed sum over bindings
```

Integer overflow is silent — if a result exceeds the bitwidth, the instance is discarded. Use sufficient Int bitwidth (e.g., `5 Int` for values -16..+15).

## Boolean Expressions and Quantifiers

```
-- Comparison:
e1 in e2                              -- subset
e1 = e2                               -- equality (extensional)
e1 != e2                              -- parses as !(e1 = e2) — see pitfalls
i < j                                 -- integer less-than
i > j                                 -- integer greater-than
i =< j                               -- less-than-or-equal (NOT <=)
i >= j                                -- greater-than-or-equal

-- Negated comparison: "e1 not in e2" = "not (e1 in e2)"

-- Logical connectives:
F and G       or  F && G
F or G        or  F || G
F implies G   or  F => G
F iff G       or  F <=> G
not F         or  !F
F implies G else H                    -- conditional

-- Quantified formulas:
all  x: E | F                         -- for all bindings of x in E
some x: E | F                         -- exists a binding
no   x: E | F                         -- no binding satisfies F
lone x: E | F                         -- at most one binding
one  x: E | F                         -- exactly one binding

-- Multi-variable: "all x: A, y: B | F" (y may reference x)
-- Bar is optional: "all x: A { F }" is the same as "all x: A | F"

-- Multiplicity expressions (no quantifier body):
no   e                                -- e is empty
some e                                -- e is nonempty
lone e                                -- e has at most one tuple
one  e                                -- e has exactly one tuple
```

## Let Expressions

```
let v = e | F                         -- bind v to expression e in F
let v1 = e1, v2 = e2 | F             -- multiple bindings (no recursion)
```

## Block Syntax

```
{ F  G  H }                           -- implicit conjunction: F and G and H
{ }                                   -- empty block = true
```

A block is a sequence of constraints, implicitly conjoined.

## Reserved Keywords

```
abstract  all    and   as      assert  but    check  disj
else      exactly extends  fact  for    fun    iden   iff
implies   in     Int   let     lone   module no     none
not       one    open  or      pred   run    set    sig
some      sum    univ
```

## Multi-character Tokens

These are single tokens: `=>` `>=` `=<` `->` `<:` `:>` `++` `&&` `||` `--` `//` `/*` `*/`

Negated comparison operators (`!=`, `!in`) are **NOT** single tokens. They are parsed as `!` followed by `=` or `in`.

## Common Pitfalls

1. **Negated operators**: `!=` is not a token. Write `not (a = b)` or ensure whitespace: `a ! = b`. Same for `!in` — write `not (a in b)`.
2. **Hyphen in identifiers**: `-` is the set-difference operator, not valid in identifiers. Use underscores: `my_name` not `my-name`.
3. **Right-associative implication**: `p => q => r` parses as `p => (q => r)`, not `(p => q) => r`.
4. **Dot binds tighter than box**: `a.b[c]` = `(a.b)[c]`, not `a.(b[c])`.
5. **Boolean vs relational ops**: Boolean operators (`&&`, `||`, `not`) apply to constraints/formulas. Relational operators (`&`, `+`, `~`) apply to expressions. Cannot mix.
6. **Int capitalization**: In scope declarations, always write `Int` (capitalized). `int` is not a keyword.
7. **else binds to nearest implies**: `p => q => r else s` parses as `p => (q => r else s)`.
8. **Default field multiplicity is one**: `f: E` constrains f to exactly one E. Use `f: set E` for a set, `f: lone E` for optional.
9. **Signature facts are implicitly quantified**: `sig S { ... } { F }` means `fact { all this: S | F }`.
10. **No return keyword**: Functions use `{ expr }` — the body IS the return value.
11. **Less-than-or-equal is `=<` not `<=`**: Written unconventionally to avoid confusion with `<=` (arrow). Greater-than-or-equal is `>=`.
12. **Int scope is bitwidth, not count**: `for 5 but 4 Int` means 4 bits (range -8..+7), not 4 integers. Default bitwidth is 4 (range -8..+7). Use `5 Int` or `6 Int` for larger ranges.
13. **Arithmetic uses function syntax**: Write `plus[a,b]` not `a + b` for integer addition. `+` is set union, not arithmetic.
14. **Invocations use square brackets only**: `pred p(x, y)` for declaration, but `p[x, y]` for invocation. Round brackets in invocations are a syntax error.
15. **Closure operators require binary relations**: `^r` and `*r` require r to be binary (arity 2). Applying to non-binary relations is a type error.
16. **`disj` is both keyword and built-in predicate**: In declarations `disj x, y: S` means x != y. As a predicate `disj[A, B, C]` checks mutual disjointness.
17. **No recursive functions/predicates**: Recursive invocations are not supported.
18. **Avoid single-quote `'` in identifiers**: Although the spec allows quotes in identifiers, the Alloy CLI parser chokes on primed names like `s'` in quantifier declarations (`some s': State | ...`). Use suffixed names instead: `s2`, `sPrime`, `sPost`. This applies to all quantified variables, comprehension variables, and let bindings. Predicate/function parameter declarations (e.g., `pred foo[s, s2: State]`) are safe with any legal name.

## Reference Model

```alloy
-- Reference Alloy model: demonstrates idiomatic patterns
-- (sig, pred, fun, assert, check, run)

-- Domain types
sig Key {}
sig Value {}

-- State with relations
sig State {
  store: Key -> lone Value,   -- partial function
  active: set Key             -- set-valued field
}

-- State invariant
pred wellFormed[s: State] {
  -- every key with a value is active
  all k: Key | some s.store[k] implies k in s.active
}

-- Operation: two-state predicate with pre/post
pred Add[s, sPost: State, k: Key, v: Value] {
  -- precondition: key is not already active
  k not in s.active

  -- postcondition: key maps to value
  sPost.store[k] = v
  k in sPost.active

  -- frame: everything else unchanged
  all k2: Key - k | sPost.store[k2] = s.store[k2]
  sPost.active = s.active + k
}

-- Derived property: count of active keys
fun activeCount[s: State]: Int {
  #s.active
}

-- Property: Add preserves well-formedness
assert AddPreservesWF {
  all s, sPost: State, k: Key, v: Value |
    (wellFormed[s] and Add[s, sPost, k, v]) implies wellFormed[sPost]
}

-- Property: Add does not remove existing keys
assert AddMonotonic {
  all s, sPost: State, k: Key, v: Value |
    (Add[s, sPost, k, v]) implies s.active in sPost.active
}

-- Non-vacuity: can we find a valid Add?
run FindAdd {
  some s, sPost: State, k: Key, v: Value |
    wellFormed[s] and Add[s, sPost, k, v]
} for 4 but exactly 2 State

check AddPreservesWF for 5 but exactly 2 State
check AddMonotonic for 5 but exactly 2 State
```
