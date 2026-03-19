mod harness;

use std::rc::Rc;
use dafny_runtime::{int, seq, DafnyInt, Sequence};
use dafny_runtime::_System::nat;
use xanadu_oracle::TumblerAlgebra;
use xanadu_oracle::TumblerHierarchy;
use xanadu_oracle::TumblerAlgebra::Tumbler;

#[test]
fn tc_001_inc_with_k2_produces_correct_child_address() {
    let n = harness::tumbler(&[1]);
    let result = TumblerAlgebra::_default::AllocationInc(&n, &int!(2));
    assert_eq!(result, harness::tumbler(&[1, 0, 1]));
}

#[test]
fn tc_002_inc_with_k2_produces_length_n_plus_k() {
    let n = harness::tumbler(&[1]);
    let result = TumblerAlgebra::_default::AllocationInc(&n, &int!(2));
    assert_eq!(result.components().cardinality(), int!(3));
}

#[test]
fn tc_003_inc_with_k2_places_zero_separator_at_position_2() {
    let n = harness::tumbler(&[1]);
    let result = TumblerAlgebra::_default::AllocationInc(&n, &int!(2));
    assert_eq!(result.components().get(&int!(1)), int!(0));
}

#[test]
fn tc_004_inc_with_k2_places_one_at_final_position() {
    let n = harness::tumbler(&[1]);
    let result = TumblerAlgebra::_default::AllocationInc(&n, &int!(2));
    assert_eq!(result.components().get(&int!(2)), int!(1));
}

#[test]
fn tc_005_sig_identifies_last_nonzero_position() {
    let u1 = harness::tumbler(&[1, 0, 1]);
    // sig = 3 (1-based) → LastNonzero returns 0-based index 2
    assert_eq!(TumblerAlgebra::_default::LastNonzero(&u1), int!(2));
}

#[test]
fn tc_006_inc_with_k0_increments_at_sig_position() {
    let u1 = harness::tumbler(&[1, 0, 1]);
    let result = TumblerAlgebra::_default::AllocationInc(&u1, &int!(0));
    assert_eq!(result, harness::tumbler(&[1, 0, 2]));
}

#[test]
fn tc_007_inc_with_k0_preserves_length() {
    let u1 = harness::tumbler(&[1, 0, 1]);
    let result = TumblerAlgebra::_default::AllocationInc(&u1, &int!(0));
    assert_eq!(result.components().cardinality(), int!(3));
}

#[test]
fn tc_008_zeros_counts_interior_zero_components() {
    let u1 = harness::tumbler(&[1, 0, 1]);
    assert_eq!(TumblerHierarchy::_default::ZeroCount(u1.components()), int!(1));
}

#[test]
fn tc_009_zeros_count_for_depth2_address() {
    let d1 = harness::tumbler(&[1, 0, 1, 0, 1]);
    assert_eq!(TumblerHierarchy::_default::ZeroCount(d1.components()), int!(2));
}

#[test]
fn tc_010_inc_valid_allows_k2_when_zeros_0() {
    let n = harness::tumbler(&[1]);
    assert!(TumblerHierarchy::_default::ValidAddress(
        &TumblerAlgebra::_default::AllocationInc(&n, &int!(2))
    ));
}

#[test]
fn tc_011_inc_valid_blocks_k2_when_zeros_3() {
    let e1 = harness::tumbler(&[1, 0, 1, 0, 1, 0, 1]);
    assert!(!TumblerHierarchy::_default::ValidAddress(
        &TumblerAlgebra::_default::AllocationInc(&e1, &int!(2))
    ));
}

#[test]
fn tc_012_partition_independence_outputs_under_distinct_parents_are_unequal() {
    let d1 = harness::tumbler(&[1, 0, 1, 0, 1]);
    let d2 = harness::tumbler(&[1, 0, 2, 0, 1]);
    assert_ne!(d1, d2);
}

#[test]
fn tc_013_proper_prefix_gives_strict_order() {
    let n = harness::tumbler(&[1]);
    let u1 = harness::tumbler(&[1, 0, 1]);
    assert!(harness::tumbler_lt(&n, &u1));
}

#[test]
fn tc_014_position_wise_difference_gives_strict_order() {
    let u1 = harness::tumbler(&[1, 0, 1]);
    let u2 = harness::tumbler(&[1, 0, 2]);
    assert!(harness::tumbler_lt(&u1, &u2));
}

#[test]
fn tc_015_ordering_extends_to_children() {
    let d1 = harness::tumbler(&[1, 0, 1, 0, 1]);
    let d2 = harness::tumbler(&[1, 0, 2, 0, 1]);
    assert!(harness::tumbler_lt(&d1, &d2));
}

#[test]
fn tc_016_same_length_differing_addresses_are_non_nested() {
    let u1 = harness::tumbler(&[1, 0, 1]);
    let u2 = harness::tumbler(&[1, 0, 2]);
    assert!(!TumblerHierarchy::_default::SeqIsPrefix(u1.components(), u2.components()));
}

#[test]
fn tc_017_inc_with_k0_yields_strictly_greater_sibling() {
    let d1 = harness::tumbler(&[1, 0, 1, 0, 1]);
    let result = TumblerAlgebra::_default::AllocationInc(&d1, &int!(0));
    assert_eq!(result, harness::tumbler(&[1, 0, 1, 0, 2]));
}

#[test]
fn tc_018_t4_permits_k2_at_the_boundary_zeros_2() {
    let d1 = harness::tumbler(&[1, 0, 1, 0, 1]);
    assert!(TumblerHierarchy::_default::ValidAddress(
        &TumblerAlgebra::_default::AllocationInc(&d1, &int!(2))
    ));
}