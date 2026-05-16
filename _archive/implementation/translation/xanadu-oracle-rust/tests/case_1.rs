mod harness;

use std::rc::Rc;
use dafny_runtime::{int, seq, DafnyInt, Sequence};
use dafny_runtime::_System::nat;
use xanadu_oracle::TumblerAlgebra;
use xanadu_oracle::TumblerHierarchy;
use xanadu_oracle::TumblerAlgebra::Tumbler;

#[test]
fn tc_001_proper_prefix_orders_before_its_extension_user_document() {
    let p = harness::tumbler(&[1, 0, 3]);
    let d = harness::tumbler(&[1, 0, 3, 0, 2]);
    assert!(harness::tumbler_lt(&p, &d));
}

#[test]
fn tc_002_proper_prefix_orders_before_its_extension_document_element() {
    let d  = harness::tumbler(&[1, 0, 3, 0, 2]);
    let e1 = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 1]);
    assert!(harness::tumbler_lt(&d, &e1));
}

#[test]
fn tc_003_divergence_at_final_component_determines_order() {
    let e1 = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 1]);
    let e2 = harness::tumbler(&[1, 0, 3, 0, 2, 0, 1, 5]);
    assert!(harness::tumbler_lt(&e1, &e2));
}
