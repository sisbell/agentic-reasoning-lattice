//! Test harness for oracle-backed test cases.
//!
//! Provides helpers that bridge test-case notation to oracle types.
//! tumbler_lt / tumbler_le implement the lexicographic order defined
//! by the Dafny ghost predicate LessThan (TumblerAlgebra.dfy:170),
//! which is not compiled to Rust.

use std::rc::Rc;

use dafny_runtime::_System::nat;
use dafny_runtime::{int, seq, DafnyInt, Sequence};
use xanadu_oracle::TumblerAlgebra::Tumbler;

/// Construct a Tumbler from a slice of i64 components.
pub fn tumbler(cs: &[i64]) -> Rc<Tumbler> {
    let components: Sequence<nat> = cs
        .iter()
        .map(|&c| int!(c))
        .collect::<Vec<DafnyInt>>()
        .into_iter()
        .fold(seq![] as Sequence<nat>, |acc, v| {
            acc.concat(&seq![v])
        });
    Rc::new(Tumbler::Tumbler { components })
}

/// Lexicographic strict less-than per Dafny's LessThanAt.
///
/// Scan for the first index k where a[k] != b[k]:
///   - if a is exhausted before b (a shorter, all shared prefixes equal), true
///   - if such k exists and a[k] < b[k], true
///   - otherwise false
pub fn tumbler_lt(a: &Rc<Tumbler>, b: &Rc<Tumbler>) -> bool {
    let ac = a.components();
    let bc = b.components();
    let a_len = ac.cardinality();
    let b_len = bc.cardinality();
    let min_len = if a_len <= b_len { a_len.clone() } else { b_len.clone() };

    let mut i = int!(0);
    while i < min_len {
        let av = ac.get(&i);
        let bv = bc.get(&i);
        if av < bv {
            return true;
        }
        if av > bv {
            return false;
        }
        i = i + int!(1);
    }
    // All shared components equal — shorter is less
    a_len < b_len
}

/// Lexicographic less-than-or-equal.
pub fn tumbler_le(a: &Rc<Tumbler>, b: &Rc<Tumbler>) -> bool {
    a == b || tumbler_lt(a, b)
}

/// Compare a Dafny Sequence<nat> with a Rust slice for equality.
pub fn seq_eq(s: &Sequence<nat>, expected: &[i64]) -> bool {
    let len = s.cardinality();
    if len != int!(expected.len() as i64) {
        return false;
    }
    for (i, &e) in expected.iter().enumerate() {
        if s.get(&int!(i as i64)) != int!(e) {
            return false;
        }
    }
    true
}

/// T3 (canonical representation) — trivially true for Dafny datatypes.
pub fn t3_valid(_t: &Rc<Tumbler>) -> bool {
    true
}
