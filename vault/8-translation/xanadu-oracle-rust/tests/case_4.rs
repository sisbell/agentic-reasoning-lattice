mod harness;

use std::rc::Rc;
use dafny_runtime::{int, seq, DafnyInt, Sequence};
use dafny_runtime::_System::nat;
use xanadu_oracle::TumblerAlgebra;
use xanadu_oracle::TumblerHierarchy;
use xanadu_oracle::TumblerAlgebra::Tumbler;

#[test]
fn tc_001_ta4_ordinal_round_trip_succeeds_when_preconditions_hold() {
    let o = harness::tumbler(&[2]);
    let w = harness::tumbler(&[3]);
    let result = TumblerAlgebra::_default::TumblerSubtract(
        &TumblerAlgebra::_default::TumblerAdd(&o, &w),
        &w,
    );
    assert_eq!(result, harness::tumbler(&[2]));
}

#[test]
fn tc_002_ta4_round_trip_returns_intermediate_result_when_zero_prefix_violated() {
    let a = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 2]);
    let w = harness::tumbler(&[0, 0, 0, 0, 0, 0, 0, 3]);
    let result = TumblerAlgebra::_default::TumblerSubtract(
        &TumblerAlgebra::_default::TumblerAdd(&a, &w),
        &w,
    );
    assert_eq!(result, harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]));
}

#[test]
fn tc_003_ta2_subtraction_precondition_holds_after_addition() {
    let r = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    let w = harness::tumbler(&[0, 0, 0, 0, 0, 0, 0, 3]);
    assert!(harness::tumbler_lt(&w, &r));
}

#[test]
fn tc_004_ta6_self_subtraction_yields_zero_sentinel() {
    let o = harness::tumbler(&[3]);
    let result = TumblerAlgebra::_default::TumblerSubtract(&o, &o);
    assert_eq!(result, harness::tumbler(&[0]));
}

#[test]
fn tc_005_ta6_zero_tumbler_strictly_less_than_positive_tumbler() {
    let z = harness::tumbler(&[0]);
    let p = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 1]);
    assert!(harness::tumbler_lt(&z, &p));
}