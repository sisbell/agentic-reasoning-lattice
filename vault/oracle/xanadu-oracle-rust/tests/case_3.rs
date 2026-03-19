mod harness;

use std::rc::Rc;
use dafny_runtime::{int, seq, DafnyInt, Sequence};
use dafny_runtime::_System::nat;
use xanadu_oracle::TumblerAlgebra;
use xanadu_oracle::TumblerHierarchy;
use xanadu_oracle::TumblerAlgebra::Tumbler;

#[test]
fn tc_001_ta0_deep_weight_operation_is_well_defined() {
    let a      = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let b      = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    let w_deep = harness::tumbler(&[0, 0, 0, 0, 0, 0, 0, 3]);
    assert!(w_deep.components().cardinality() <= a.components().cardinality());
    assert!(w_deep.components().cardinality() <= b.components().cardinality());
}

#[test]
fn tc_002_ta0_shallow_weight_operation_is_well_defined() {
    let a         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let b         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    let w_shallow = harness::tumbler(&[3]);
    assert!(w_shallow.components().cardinality() <= a.components().cardinality());
    assert!(w_shallow.components().cardinality() <= b.components().cardinality());
}

#[test]
fn tc_003_ta_strict_deep_addition_strictly_increases_a() {
    let a      = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let w_deep = harness::tumbler(&[0, 0, 0, 0, 0, 0, 0, 3]);
    let result = TumblerAlgebra::_default::TumblerAdd(&a, &w_deep);
    assert!(harness::tumbler_lt(&a, &result));
}

#[test]
fn tc_004_ta_strict_shallow_addition_strictly_increases_a() {
    let a         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let w_shallow = harness::tumbler(&[3]);
    let result    = TumblerAlgebra::_default::TumblerAdd(&a, &w_shallow);
    assert!(harness::tumbler_lt(&a, &result));
}

#[test]
fn tc_005_ta1_strict_k_equals_divergence_preserves_strict_order() {
    let a      = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let b      = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    let w_deep = harness::tumbler(&[0, 0, 0, 0, 0, 0, 0, 3]);
    let add_a  = TumblerAlgebra::_default::TumblerAdd(&a, &w_deep);
    let add_b  = TumblerAlgebra::_default::TumblerAdd(&b, &w_deep);
    assert!(harness::tumbler_lt(&add_a, &add_b));
}

#[test]
fn tc_006_ta1_weak_k_lt_divergence_satisfies_weak_order() {
    let a         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let b         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    let w_shallow = harness::tumbler(&[3]);
    let add_a     = TumblerAlgebra::_default::TumblerAdd(&a, &w_shallow);
    let add_b     = TumblerAlgebra::_default::TumblerAdd(&b, &w_shallow);
    assert!(harness::tumbler_le(&add_a, &add_b));
}

#[test]
fn tc_007_ta1_strict_negative_k_lt_divergence_collapses_to_equality() {
    let a         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let b         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    let w_shallow = harness::tumbler(&[3]);
    let add_a     = TumblerAlgebra::_default::TumblerAdd(&a, &w_shallow);
    let add_b     = TumblerAlgebra::_default::TumblerAdd(&b, &w_shallow);
    assert_eq!(add_a, add_b);
}

#[test]
fn tc_008_result_length_identity_deep() {
    let a      = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let w_deep = harness::tumbler(&[0, 0, 0, 0, 0, 0, 0, 3]);
    let result = TumblerAlgebra::_default::TumblerAdd(&a, &w_deep);
    assert_eq!(result.components().cardinality(), w_deep.components().cardinality());
}

#[test]
fn tc_009_result_length_identity_shallow() {
    let a         = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let w_shallow = harness::tumbler(&[3]);
    let result    = TumblerAlgebra::_default::TumblerAdd(&a, &w_shallow);
    assert_eq!(result.components().cardinality(), w_shallow.components().cardinality());
}