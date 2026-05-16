mod harness;

use std::rc::Rc;
use dafny_runtime::{int, seq, DafnyInt, Sequence};
use dafny_runtime::_System::nat;
use xanadu_oracle::TumblerAlgebra;
use xanadu_oracle::TumblerHierarchy;
use xanadu_oracle::TumblerAlgebra::Tumbler;

#[test]
fn tc_001_valid_element_address_accepted() {
    let addr = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    assert!(TumblerHierarchy::_default::ValidAddress(&addr));
}

#[test]
fn tc_002_four_zero_separators_rejected() {
    let addr = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 0]);
    assert!(!TumblerHierarchy::_default::ValidAddress(&addr));
}

#[test]
fn tc_003_adjacent_zeros_rejected() {
    let addr = harness::tumbler(&[1, 0, 0, 3]);
    assert!(!TumblerHierarchy::_default::ValidAddress(&addr));
}

#[test]
fn tc_004_leading_zero_rejected() {
    let addr = harness::tumbler(&[0, 1, 0, 3]);
    assert!(!TumblerHierarchy::_default::ValidAddress(&addr));
}

#[test]
fn tc_005_trailing_zero_rejected() {
    let addr = harness::tumbler(&[1, 0, 3, 0]);
    assert!(!TumblerHierarchy::_default::ValidAddress(&addr));
}

#[test]
fn tc_006_t3_holds_for_x1() {
    let addr = harness::tumbler(&[1, 0, 0, 3]);
    assert!(harness::t3_valid(&addr));
}

#[test]
fn tc_007_t3_holds_for_x2() {
    let addr = harness::tumbler(&[0, 1, 0, 3]);
    assert!(harness::t3_valid(&addr));
}

#[test]
fn tc_008_t3_holds_for_x3() {
    let addr = harness::tumbler(&[1, 0, 3, 0]);
    assert!(harness::t3_valid(&addr));
}

#[test]
fn tc_009_t3_holds_for_x4() {
    let addr = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 0]);
    assert!(harness::t3_valid(&addr));
}

#[test]
fn tc_010_t3_holds_for_v() {
    let addr = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    assert!(harness::t3_valid(&addr));
}