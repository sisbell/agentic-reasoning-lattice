#![allow(warnings, unconditional_panic)]
#![allow(nonstandard_style)]
#![cfg_attr(any(), rustfmt::skip)]

pub mod _module {
    
}
/// vault/proofs/TumblerBaptism/BaptismBranching.dfy(3,1)
pub mod BaptismBranching {
    
}
/// vault/proofs/TumblerBaptism/BaptismGhost.dfy(11,1)
pub mod BaptismGhost {
    pub use ::dafny_runtime::Set;
    pub use ::std::rc::Rc;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::std::fmt::Debug;
    pub use ::std::fmt::Formatter;
    pub use ::std::fmt::Result;
    pub use ::dafny_runtime::DafnyPrint;
    pub use ::std::cmp::PartialEq;
    pub use ::std::cmp::Eq;
    pub use ::std::hash::Hash;
    pub use ::std::hash::Hasher;
    pub use ::std::convert::AsRef;

    /// vault/proofs/TumblerBaptism/BaptismGhost.dfy(14,3)
    #[derive(Clone)]
    pub enum ContentState {
        ContentState {
            baptized: Set<Rc<Tumbler>>,
            occupied: Set<Rc<Tumbler>>
        }
    }

    impl ContentState {
        /// Returns a borrow of the field baptized
        pub fn baptized(&self) -> &Set<Rc<Tumbler>> {
            match self {
                ContentState::ContentState{baptized, occupied, } => baptized,
            }
        }
        /// Returns a borrow of the field occupied
        pub fn occupied(&self) -> &Set<Rc<Tumbler>> {
            match self {
                ContentState::ContentState{baptized, occupied, } => occupied,
            }
        }
    }

    impl Debug
        for ContentState {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for ContentState {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                ContentState::ContentState{baptized, occupied, } => {
                    write!(_formatter, "BaptismGhost.ContentState.ContentState(")?;
                    DafnyPrint::fmt_print(baptized, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(occupied, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for ContentState {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (ContentState::ContentState{baptized, occupied, }, ContentState::ContentState{baptized: _2_baptized, occupied: _2_occupied, }) => {
                    baptized == _2_baptized && occupied == _2_occupied
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for ContentState {}

    impl Hash
        for ContentState {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                ContentState::ContentState{baptized, occupied, } => {
                    Hash::hash(baptized, _state);
                    Hash::hash(occupied, _state)
                },
            }
        }
    }

    impl AsRef<ContentState>
        for ContentState {
        fn as_ref(&self) -> &Self {
            self
        }
    }
}
/// vault/proofs/TumblerBaptism/BaptismRegistry.dfy(3,1)
pub mod BaptismRegistry {
    pub use ::std::rc::Rc;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::_System::nat;
    pub use ::std::fmt::Debug;
    pub use ::std::fmt::Formatter;
    pub use ::std::fmt::Result;
    pub use ::dafny_runtime::DafnyPrint;
    pub use ::std::cmp::PartialEq;
    pub use ::std::cmp::Eq;
    pub use ::std::hash::Hash;
    pub use ::std::hash::Hasher;
    pub use ::std::convert::AsRef;
    pub use ::dafny_runtime::Set;
    pub use ::dafny_runtime::DafnyType;

    /// vault/proofs/TumblerBaptism/BaptismRegistry.dfy(82,3)
    #[derive(Clone)]
    pub enum Namespace {
        Namespace {
            parent: Rc<Tumbler>,
            depth: nat
        }
    }

    impl Namespace {
        /// Returns a borrow of the field parent
        pub fn parent(&self) -> &Rc<Tumbler> {
            match self {
                Namespace::Namespace{parent, depth, } => parent,
            }
        }
        /// Returns a borrow of the field depth
        pub fn depth(&self) -> &nat {
            match self {
                Namespace::Namespace{parent, depth, } => depth,
            }
        }
    }

    impl Debug
        for Namespace {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for Namespace {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                Namespace::Namespace{parent, depth, } => {
                    write!(_formatter, "BaptismRegistry.Namespace.Namespace(")?;
                    DafnyPrint::fmt_print(parent, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(depth, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for Namespace {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (Namespace::Namespace{parent, depth, }, Namespace::Namespace{parent: _2_parent, depth: _2_depth, }) => {
                    parent == _2_parent && depth == _2_depth
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for Namespace {}

    impl Hash
        for Namespace {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                Namespace::Namespace{parent, depth, } => {
                    Hash::hash(parent, _state);
                    Hash::hash(depth, _state)
                },
            }
        }
    }

    impl AsRef<Namespace>
        for Namespace {
        fn as_ref(&self) -> &Self {
            self
        }
    }

    /// vault/proofs/TumblerBaptism/BaptismRegistry.dfy(84,3)
    #[derive(Clone)]
    pub enum BaptismEvent {
        BaptismEvent {
            ns: Rc<Namespace>,
            readRegistry: Set<Rc<Tumbler>>,
            commitRegistry: Set<Rc<Tumbler>>
        }
    }

    impl BaptismEvent {
        /// Returns a borrow of the field ns
        pub fn ns(&self) -> &Rc<Namespace> {
            match self {
                BaptismEvent::BaptismEvent{ns, readRegistry, commitRegistry, } => ns,
            }
        }
        /// Returns a borrow of the field readRegistry
        pub fn readRegistry(&self) -> &Set<Rc<Tumbler>> {
            match self {
                BaptismEvent::BaptismEvent{ns, readRegistry, commitRegistry, } => readRegistry,
            }
        }
        /// Returns a borrow of the field commitRegistry
        pub fn commitRegistry(&self) -> &Set<Rc<Tumbler>> {
            match self {
                BaptismEvent::BaptismEvent{ns, readRegistry, commitRegistry, } => commitRegistry,
            }
        }
    }

    impl Debug
        for BaptismEvent {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for BaptismEvent {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                BaptismEvent::BaptismEvent{ns, readRegistry, commitRegistry, } => {
                    write!(_formatter, "BaptismRegistry.BaptismEvent.BaptismEvent(")?;
                    DafnyPrint::fmt_print(ns, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(readRegistry, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(commitRegistry, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for BaptismEvent {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (BaptismEvent::BaptismEvent{ns, readRegistry, commitRegistry, }, BaptismEvent::BaptismEvent{ns: _2_ns, readRegistry: _2_readRegistry, commitRegistry: _2_commitRegistry, }) => {
                    ns == _2_ns && readRegistry == _2_readRegistry && commitRegistry == _2_commitRegistry
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for BaptismEvent {}

    impl Hash
        for BaptismEvent {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                BaptismEvent::BaptismEvent{ns, readRegistry, commitRegistry, } => {
                    Hash::hash(ns, _state);
                    Hash::hash(readRegistry, _state);
                    Hash::hash(commitRegistry, _state)
                },
            }
        }
    }

    impl AsRef<BaptismEvent>
        for BaptismEvent {
        fn as_ref(&self) -> &Self {
            self
        }
    }

    /// vault/proofs/TumblerBaptism/BaptismRegistry.dfy(222,3)
    #[derive(Clone)]
    pub enum SystemState<R: DafnyType> {
        SystemState {
            B: Set<Rc<Tumbler>>,
            rest: R
        }
    }

    impl<R: DafnyType> SystemState<R> {
        /// Returns a borrow of the field B
        pub fn B(&self) -> &Set<Rc<Tumbler>> {
            match self {
                SystemState::SystemState{B, rest, } => B,
            }
        }
        /// Returns a borrow of the field rest
        pub fn rest(&self) -> &R {
            match self {
                SystemState::SystemState{B, rest, } => rest,
            }
        }
    }

    impl<R: DafnyType> Debug
        for SystemState<R> {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl<R: DafnyType> DafnyPrint
        for SystemState<R> {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                SystemState::SystemState{B, rest, } => {
                    write!(_formatter, "BaptismRegistry.SystemState.SystemState(")?;
                    DafnyPrint::fmt_print(B, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(rest, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl<R: DafnyType + Eq + Hash> PartialEq
        for SystemState<R> {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (SystemState::SystemState{B, rest, }, SystemState::SystemState{B: _2_B, rest: _2_rest, }) => {
                    B == _2_B && rest == _2_rest
                },
                _ => {
                    false
                },
            }
        }
    }

    impl<R: DafnyType + Eq + Hash> Eq
        for SystemState<R> {}

    impl<R: DafnyType + Hash> Hash
        for SystemState<R> {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                SystemState::SystemState{B, rest, } => {
                    Hash::hash(B, _state);
                    Hash::hash(rest, _state)
                },
            }
        }
    }

    impl<R: DafnyType> AsRef<SystemState<R>>
        for SystemState<R> {
        fn as_ref(&self) -> &Self {
            self
        }
    }
}
/// vault/proofs/TumblerOwnership/OwnershipDelegation.dfy(6,1)
pub mod OwnershipDelegation {
    pub use ::std::rc::Rc;
    pub use crate::TumblerOwnership::State;
    pub use crate::TumblerOwnership::Principal;
    pub use ::dafny_runtime::set;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TumblerOwnership/OwnershipDelegation.dfy(13,3)
        pub fn Delegate(s: &Rc<State>, delegator: &Rc<Principal>, delegate: &Rc<Principal>) -> Rc<State> {
            Rc::new(State::State {
                    principals: s.principals().merge(&set!{delegate.clone()}),
                    alloc: s.alloc().clone()
                })
        }
    }
}
/// vault/proofs/TumblerOwnership/OwnershipExclusivity.dfy(7,1)
pub mod OwnershipExclusivity {
    
}
/// vault/proofs/TumblerOwnership/OwnershipFork.dfy(6,1)
pub mod OwnershipFork {
    pub use ::std::rc::Rc;
    pub use crate::TumblerOwnership::State;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::set;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TumblerOwnership/OwnershipFork.dfy(19,3)
        pub fn Fork(s: &Rc<State>, alt: &Rc<Tumbler>) -> Rc<State> {
            Rc::new(State::State {
                    principals: s.principals().clone(),
                    alloc: s.alloc().merge(&set!{alt.clone()})
                })
        }
    }
}
/// vault/proofs/TumblerOwnership/OwnershipPermanence.dfy(7,1)
pub mod OwnershipPermanence {
    
}
/// vault/proofs/TumblerOwnership/OwnershipProvenance.dfy(6,1)
pub mod OwnershipProvenance {
    
}
/// vault/proofs/TumblerAlgebra/TumblerAddition.dfy(3,1)
pub mod TumblerAddition {
    
}
/// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(3,1)
pub mod TumblerAlgebra {
    pub use ::dafny_runtime::_System::nat;
    pub use ::dafny_runtime::Sequence;
    pub use ::std::rc::Rc;
    pub use ::dafny_runtime::DafnyInt;
    pub use ::dafny_runtime::int;
    pub use ::dafny_runtime::integer_range;
    pub use ::dafny_runtime::Zero;
    pub use ::dafny_runtime::seq;
    pub use ::std::fmt::Debug;
    pub use ::std::fmt::Formatter;
    pub use ::std::fmt::Result;
    pub use ::dafny_runtime::DafnyPrint;
    pub use ::std::cmp::PartialEq;
    pub use ::std::cmp::Eq;
    pub use ::std::hash::Hash;
    pub use ::std::hash::Hasher;
    pub use ::std::convert::AsRef;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(16,3)
        pub fn Max(a: &nat, b: &nat) -> nat {
            if a.clone() >= b.clone() {
                a.clone()
            } else {
                b.clone()
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(21,3)
        pub fn Pad(s: &Sequence<nat>, n: &nat) -> Sequence<nat> {
            s.concat(&({
                    let _initializer = {
                            Rc::new(move |i: &DafnyInt| -> DafnyInt{
            int!(0)
        }) as Rc<dyn ::std::ops::Fn(&_) -> _>
                        };
                    integer_range(Zero::zero(), n.clone() - s.cardinality()).map(move |i| _initializer(&i)).collect::<Sequence<_>>()
                }))
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(31,3)
        pub fn Zeros(n: &nat) -> Sequence<nat> {
            {
                let _initializer = {
                        Rc::new(move |i: &DafnyInt| -> DafnyInt{
            int!(0)
        }) as Rc<dyn ::std::ops::Fn(&_) -> _>
                    };
                integer_range(Zero::zero(), n.clone()).map(move |i| _initializer(&i)).collect::<Sequence<_>>()
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(50,3)
        pub fn ActionPoint(w: &Rc<Tumbler>) -> nat {
            _default::ActionPointRec(w.components(), &int!(0))
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(59,3)
        pub fn ActionPointRec(s: &Sequence<nat>, i: &nat) -> nat {
            let mut _r0 = s.clone();
            let mut _r1 = i.clone();
            'TAIL_CALL_START: loop {
                let s = _r0;
                let i = _r1;
                if s.get(&i) != int!(0) {
                    return i.clone();
                } else {
                    let mut _in0: Sequence<nat> = s.clone();
                    let mut _in1: DafnyInt = i.clone() + int!(1);
                    _r0 = _in0.clone();
                    _r1 = _in1.clone();
                    continue 'TAIL_CALL_START;
                }
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(75,3)
        pub fn LastNonzeroRec(s: &Sequence<nat>, i: &nat) -> nat {
            let mut _r0 = s.clone();
            let mut _r1 = i.clone();
            'TAIL_CALL_START: loop {
                let s = _r0;
                let i = _r1;
                if s.get(&(i.clone() - int!(1))) != int!(0) {
                    return i.clone() - int!(1);
                } else {
                    let mut _in0: Sequence<nat> = s.clone();
                    let mut _in1: DafnyInt = i.clone() - int!(1);
                    _r0 = _in0.clone();
                    _r1 = _in1.clone();
                    continue 'TAIL_CALL_START;
                }
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(87,3)
        pub fn LastNonzero(t: &Rc<Tumbler>) -> nat {
            _default::LastNonzeroRec(t.components(), &t.components().cardinality())
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(112,3)
        pub fn FindZero(s: &Sequence<nat>, start: &nat) -> nat {
            let mut _r0 = s.clone();
            let mut _r1 = start.clone();
            'TAIL_CALL_START: loop {
                let s = _r0;
                let start = _r1;
                if start.clone() == s.cardinality() {
                    return s.cardinality();
                } else {
                    if s.get(&start) == int!(0) {
                        return start.clone();
                    } else {
                        let mut _in0: Sequence<nat> = s.clone();
                        let mut _in1: DafnyInt = start.clone() + int!(1);
                        _r0 = _in0.clone();
                        _r1 = _in1.clone();
                        continue 'TAIL_CALL_START;
                    }
                }
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(128,3)
        pub fn FirstDiff(a: &Sequence<nat>, b: &Sequence<nat>) -> nat {
            _default::FirstDiffRec(a, b, &int!(0))
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(138,3)
        pub fn FirstDiffRec(a: &Sequence<nat>, b: &Sequence<nat>, i: &nat) -> nat {
            let mut _r0 = a.clone();
            let mut _r1 = b.clone();
            let mut _r2 = i.clone();
            'TAIL_CALL_START: loop {
                let a = _r0;
                let b = _r1;
                let i = _r2;
                if a.get(&i) != b.get(&i) {
                    return i.clone();
                } else {
                    let mut _in0: Sequence<nat> = a.clone();
                    let mut _in1: Sequence<nat> = b.clone();
                    let mut _in2: DafnyInt = i.clone() + int!(1);
                    _r0 = _in0.clone();
                    _r1 = _in1.clone();
                    _r2 = _in2.clone();
                    continue 'TAIL_CALL_START;
                }
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(203,3)
        pub fn TumblerAdd(a: &Rc<Tumbler>, w: &Rc<Tumbler>) -> Rc<Tumbler> {
            let mut k: nat = _default::ActionPoint(w);
            Rc::new(Tumbler::Tumbler {
                    components: a.components().take(&k).concat(&seq![a.components().get(&k) + w.components().get(&k)]).concat(&w.components().drop(&(k.clone() + int!(1))))
                })
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(222,3)
        pub fn AllocationInc(t: &Rc<Tumbler>, k: &nat) -> Rc<Tumbler> {
            if k.clone() == int!(0) {
                let mut s: nat = _default::LastNonzero(t);
                Rc::new(Tumbler::Tumbler {
                        components: t.components().take(&s).concat(&seq![t.components().get(&s) + int!(1)]).concat(&t.components().drop(&(s.clone() + int!(1))))
                    })
            } else {
                Rc::new(Tumbler::Tumbler {
                        components: t.components().concat(&_default::Zeros(&(k.clone() - int!(1)))).concat(&seq![int!(1)])
                    })
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(276,3)
        pub fn TumblerSubtract(a: &Rc<Tumbler>, w: &Rc<Tumbler>) -> Rc<Tumbler> {
            let mut len: nat = _default::Max(&a.components().cardinality(), &w.components().cardinality());
            let mut pa: Sequence<nat> = _default::Pad(a.components(), &len);
            let mut pw: Sequence<nat> = _default::Pad(w.components(), &len);
            if pa.clone() == pw.clone() {
                Rc::new(Tumbler::Tumbler {
                        components: _default::Zeros(&len)
                    })
            } else {
                let mut k: nat = _default::FirstDiff(&pa, &pw);
                Rc::new(Tumbler::Tumbler {
                        components: _default::Zeros(&k).concat(&seq![pa.get(&k) - pw.get(&k)]).concat(&pa.drop(&(k.clone() + int!(1))))
                    })
            }
        }
    }

    /// vault/proofs/TumblerAlgebra/TumblerAlgebra.dfy(6,3)
    #[derive(Clone)]
    pub enum Tumbler {
        Tumbler {
            components: Sequence<nat>
        }
    }

    impl Tumbler {
        /// Returns a borrow of the field components
        pub fn components(&self) -> &Sequence<nat> {
            match self {
                Tumbler::Tumbler{components, } => components,
            }
        }
    }

    impl Debug
        for Tumbler {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for Tumbler {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                Tumbler::Tumbler{components, } => {
                    write!(_formatter, "TumblerAlgebra.Tumbler.Tumbler(")?;
                    DafnyPrint::fmt_print(components, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for Tumbler {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (Tumbler::Tumbler{components, }, Tumbler::Tumbler{components: _2_components, }) => {
                    components == _2_components
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for Tumbler {}

    impl Hash
        for Tumbler {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                Tumbler::Tumbler{components, } => {
                    Hash::hash(components, _state)
                },
            }
        }
    }

    impl AsRef<Tumbler>
        for Tumbler {
        fn as_ref(&self) -> &Self {
            self
        }
    }
}
/// vault/proofs/TumblerAlgebra/TumblerAllocation.dfy(2,1)
pub mod TumblerAllocation {
    
}
/// vault/proofs/TumblerBaptism/TumblerBaptism.dfy(4,1)
pub mod TumblerBaptism {
    pub use ::std::rc::Rc;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::_System::nat;
    pub use ::dafny_runtime::int;
    pub use ::dafny_runtime::seq;
    pub use ::dafny_runtime::Set;
    pub use ::std::fmt::Debug;
    pub use ::std::fmt::Formatter;
    pub use ::std::fmt::Result;
    pub use ::dafny_runtime::DafnyPrint;
    pub use ::std::cmp::PartialEq;
    pub use ::std::cmp::Eq;
    pub use ::std::hash::Hash;
    pub use ::std::hash::Hasher;
    pub use ::std::convert::AsRef;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TumblerBaptism/TumblerBaptism.dfy(12,3)
        pub fn StreamElement(p: &Rc<Tumbler>, d: &nat, n: &nat) -> Rc<Tumbler> {
            Rc::new(Tumbler::Tumbler {
                    components: p.components().concat(&crate::TumblerAlgebra::_default::Zeros(&(d.clone() - int!(1)))).concat(&seq![n.clone()])
                })
        }
    }

    /// vault/proofs/TumblerBaptism/TumblerBaptism.dfy(63,3)
    #[derive(Clone)]
    pub enum BaptismState {
        BaptismState {
            B: Set<Rc<Tumbler>>
        }
    }

    impl BaptismState {
        /// Returns a borrow of the field B
        pub fn B(&self) -> &Set<Rc<Tumbler>> {
            match self {
                BaptismState::BaptismState{B, } => B,
            }
        }
    }

    impl Debug
        for BaptismState {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for BaptismState {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                BaptismState::BaptismState{B, } => {
                    write!(_formatter, "TumblerBaptism.BaptismState.BaptismState(")?;
                    DafnyPrint::fmt_print(B, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for BaptismState {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (BaptismState::BaptismState{B, }, BaptismState::BaptismState{B: _2_B, }) => {
                    B == _2_B
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for BaptismState {}

    impl Hash
        for BaptismState {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                BaptismState::BaptismState{B, } => {
                    Hash::hash(B, _state)
                },
            }
        }
    }

    impl AsRef<BaptismState>
        for BaptismState {
        fn as_ref(&self) -> &Self {
            self
        }
    }
}
/// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(2,1)
pub mod TumblerHierarchy {
    pub use ::dafny_runtime::Sequence;
    pub use ::dafny_runtime::_System::nat;
    pub use ::dafny_runtime::int;
    pub use ::dafny_runtime::integer_range;
    pub use ::std::rc::Rc;
    pub use ::dafny_runtime::DafnyInt;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::seq;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(9,3)
        pub fn ZeroCount(s: &Sequence<nat>) -> nat {
            let mut _accumulator: nat = int!(0);
            let mut _r0 = s.clone();
            'TAIL_CALL_START: loop {
                let s = _r0;
                if s.cardinality() == int!(0) {
                    return int!(0) + _accumulator.clone();
                } else {
                    _accumulator = _accumulator.clone() + (if s.get(&int!(0)) == int!(0) {
                                int!(1)
                            } else {
                                int!(0)
                            });
                    let mut _in0: Sequence<nat> = s.drop(&int!(1));
                    _r0 = _in0.clone();
                    continue 'TAIL_CALL_START;
                }
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(16,3)
        pub fn NoAdjacentZeros(s: &Sequence<nat>) -> bool {
            integer_range(int!(0), s.cardinality() - int!(1)).all(({
                    let mut s = s.clone();
                    Rc::new(move |__forall_var_0: DafnyInt| -> bool{
            let mut i: DafnyInt = __forall_var_0.clone();
            !(int!(0) <= i.clone() && i.clone() < s.cardinality() - int!(1)) || !(s.get(&i) == int!(0) && s.get(&(i.clone() + int!(1))) == int!(0))
        }) as Rc<dyn ::std::ops::Fn(_) -> _>
                }).as_ref())
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(20,3)
        pub fn ValidAddress(t: &Rc<Tumbler>) -> bool {
            t.components().cardinality() >= int!(1) && _default::ZeroCount(t.components()) <= int!(3) && t.components().get(&int!(0)) != int!(0) && t.components().get(&(t.components().cardinality() - int!(1))) != int!(0) && _default::NoAdjacentZeros(t.components())
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(44,3)
        pub fn NodeField(t: &Rc<Tumbler>) -> Sequence<nat> {
            let mut z: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &int!(0));
            t.components().take(&z)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(49,3)
        pub fn UserField(t: &Rc<Tumbler>) -> Sequence<nat> {
            let mut z0: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &int!(0));
            if z0.clone() >= t.components().cardinality() {
                seq![] as Sequence<nat>
            } else {
                let mut z1: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &(z0.clone() + int!(1)));
                t.components().slice(&(z0.clone() + int!(1)), &z1)
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(57,3)
        pub fn DocField(t: &Rc<Tumbler>) -> Sequence<nat> {
            let mut z0: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &int!(0));
            if z0.clone() >= t.components().cardinality() {
                seq![] as Sequence<nat>
            } else {
                let mut z1: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &(z0.clone() + int!(1)));
                if z1.clone() >= t.components().cardinality() {
                    seq![] as Sequence<nat>
                } else {
                    let mut z2: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &(z1.clone() + int!(1)));
                    t.components().slice(&(z1.clone() + int!(1)), &z2)
                }
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(68,3)
        pub fn SameNode(a: &Rc<Tumbler>, b: &Rc<Tumbler>) -> bool {
            _default::NodeField(a) == _default::NodeField(b)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(72,3)
        pub fn SameNodeUser(a: &Rc<Tumbler>, b: &Rc<Tumbler>) -> bool {
            _default::NodeField(a) == _default::NodeField(b) && _default::UserField(a) == _default::UserField(b)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(76,3)
        pub fn SameNodeUserDoc(a: &Rc<Tumbler>, b: &Rc<Tumbler>) -> bool {
            _default::NodeField(a) == _default::NodeField(b) && _default::UserField(a) == _default::UserField(b) && _default::DocField(a) == _default::DocField(b)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(80,3)
        pub fn SeqIsPrefix(a: &Sequence<nat>, b: &Sequence<nat>) -> bool {
            a.cardinality() <= b.cardinality() && a.clone() == b.take(&a.cardinality())
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(84,3)
        pub fn DocFieldIsPrefix(a: &Rc<Tumbler>, b: &Rc<Tumbler>) -> bool {
            _default::SeqIsPrefix(&_default::DocField(a), &_default::DocField(b))
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(118,3)
        pub fn E1Pos(t: &Rc<Tumbler>) -> nat {
            let mut z0: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &int!(0));
            if z0.clone() >= t.components().cardinality() {
                t.components().cardinality() + int!(1)
            } else {
                let mut z1: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &(z0.clone() + int!(1)));
                if z1.clone() >= t.components().cardinality() {
                    t.components().cardinality() + int!(1)
                } else {
                    let mut z2: nat = crate::TumblerAlgebra::_default::FindZero(t.components(), &(z1.clone() + int!(1)));
                    z2.clone() + int!(1)
                }
            }
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(129,3)
        pub fn HasElementField(t: &Rc<Tumbler>) -> bool {
            _default::E1Pos(t) < t.components().cardinality()
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(133,3)
        pub fn E1(t: &Rc<Tumbler>) -> nat {
            t.components().get(&_default::E1Pos(t))
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(166,3)
        pub fn NodeAddress(t: &Rc<Tumbler>) -> bool {
            _default::ValidAddress(t) && _default::ZeroCount(t.components()) == int!(0)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(170,3)
        pub fn AccountAddress(t: &Rc<Tumbler>) -> bool {
            _default::ValidAddress(t) && _default::ZeroCount(t.components()) == int!(1)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(174,3)
        pub fn DocumentAddress(t: &Rc<Tumbler>) -> bool {
            _default::ValidAddress(t) && _default::ZeroCount(t.components()) == int!(2)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(178,3)
        pub fn ElementAddress(t: &Rc<Tumbler>) -> bool {
            _default::ValidAddress(t) && _default::ZeroCount(t.components()) == int!(3)
        }
        /// vault/proofs/TumblerAlgebra/TumblerHierarchy.dfy(182,3)
        pub fn Root() -> Rc<Tumbler> {
            Rc::new(Tumbler::Tumbler {
                    components: seq![int!(1)]
                })
        }
    }
}
/// vault/proofs/TumblerAlgebra/TumblerOrder.dfy(2,1)
pub mod TumblerOrder {
    pub use ::std::rc::Rc;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::_System::nat;
    pub use ::dafny_runtime::seq;
    pub use ::dafny_runtime::int;
    pub use ::dafny_runtime::DafnyInt;
    pub use ::dafny_runtime::integer_range;
    pub use ::dafny_runtime::Zero;
    pub use ::dafny_runtime::Sequence;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TumblerAlgebra/TumblerOrder.dfy(9,3)
        pub fn WithComponent(t: &Rc<Tumbler>, i: &nat, v: &nat) -> Rc<Tumbler> {
            Rc::new(Tumbler::Tumbler {
                    components: t.components().take(i).concat(&seq![v.clone()]).concat(&t.components().drop(&(i.clone() + int!(1))))
                })
        }
        /// vault/proofs/TumblerAlgebra/TumblerOrder.dfy(34,3)
        pub fn TumblerOfLength(n: &nat) -> Rc<Tumbler> {
            Rc::new(Tumbler::Tumbler {
                    components: {
                            let _initializer = {
                                    Rc::new(move |_v0: &DafnyInt| -> DafnyInt{
            int!(1)
        }) as Rc<dyn ::std::ops::Fn(&_) -> _>
                                };
                            integer_range(Zero::zero(), n.clone()).map(move |i| _initializer(&i)).collect::<Sequence<_>>()
                        }
                })
        }
    }
}
/// vault/proofs/TumblerOwnership/TumblerOwnership.dfy(6,1)
pub mod TumblerOwnership {
    pub use ::std::rc::Rc;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::_System::nat;
    pub use ::dafny_runtime::int;
    pub use ::std::fmt::Debug;
    pub use ::std::fmt::Formatter;
    pub use ::std::fmt::Result;
    pub use ::dafny_runtime::DafnyPrint;
    pub use ::std::cmp::PartialEq;
    pub use ::std::cmp::Eq;
    pub use ::std::hash::Hash;
    pub use ::std::hash::Hasher;
    pub use ::std::convert::AsRef;
    pub use ::dafny_runtime::Set;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TumblerOwnership/TumblerOwnership.dfy(51,3)
        pub fn Acct(a: &Rc<Tumbler>) -> Rc<Tumbler> {
            let mut z0: nat = crate::TumblerAlgebra::_default::FindZero(a.components(), &int!(0));
            if z0.clone() >= a.components().cardinality() {
                a.clone()
            } else {
                let mut z1: nat = crate::TumblerAlgebra::_default::FindZero(a.components(), &(z0.clone() + int!(1)));
                Rc::new(Tumbler::Tumbler {
                        components: a.components().take(&z1)
                    })
            }
        }
    }

    /// vault/proofs/TumblerOwnership/TumblerOwnership.dfy(11,3)
    #[derive(Clone)]
    pub enum Principal {
        Principal {
            prefix: Rc<Tumbler>
        }
    }

    impl Principal {
        /// Returns a borrow of the field prefix
        pub fn prefix(&self) -> &Rc<Tumbler> {
            match self {
                Principal::Principal{prefix, } => prefix,
            }
        }
    }

    impl Debug
        for Principal {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for Principal {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                Principal::Principal{prefix, } => {
                    write!(_formatter, "TumblerOwnership.Principal.Principal(")?;
                    DafnyPrint::fmt_print(prefix, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for Principal {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (Principal::Principal{prefix, }, Principal::Principal{prefix: _2_prefix, }) => {
                    prefix == _2_prefix
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for Principal {}

    impl Hash
        for Principal {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                Principal::Principal{prefix, } => {
                    Hash::hash(prefix, _state)
                },
            }
        }
    }

    impl AsRef<Principal>
        for Principal {
        fn as_ref(&self) -> &Self {
            self
        }
    }

    /// vault/proofs/TumblerOwnership/TumblerOwnership.dfy(14,3)
    #[derive(Clone)]
    pub enum State {
        State {
            principals: Set<Rc<Principal>>,
            alloc: Set<Rc<Tumbler>>
        }
    }

    impl State {
        /// Returns a borrow of the field principals
        pub fn principals(&self) -> &Set<Rc<Principal>> {
            match self {
                State::State{principals, alloc, } => principals,
            }
        }
        /// Returns a borrow of the field alloc
        pub fn alloc(&self) -> &Set<Rc<Tumbler>> {
            match self {
                State::State{principals, alloc, } => alloc,
            }
        }
    }

    impl Debug
        for State {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for State {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                State::State{principals, alloc, } => {
                    write!(_formatter, "TumblerOwnership.State.State(")?;
                    DafnyPrint::fmt_print(principals, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(alloc, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for State {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (State::State{principals, alloc, }, State::State{principals: _2_principals, alloc: _2_alloc, }) => {
                    principals == _2_principals && alloc == _2_alloc
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for State {}

    impl Hash
        for State {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                State::State{principals, alloc, } => {
                    Hash::hash(principals, _state);
                    Hash::hash(alloc, _state)
                },
            }
        }
    }

    impl AsRef<State>
        for State {
        fn as_ref(&self) -> &Self {
            self
        }
    }

    /// vault/proofs/TumblerOwnership/TumblerOwnership.dfy(92,3)
    #[derive(Clone)]
    pub enum Session {
        Session {
            account: Rc<Tumbler>,
            principal: Rc<Principal>
        }
    }

    impl Session {
        /// Returns a borrow of the field account
        pub fn account(&self) -> &Rc<Tumbler> {
            match self {
                Session::Session{account, principal, } => account,
            }
        }
        /// Returns a borrow of the field principal
        pub fn principal(&self) -> &Rc<Principal> {
            match self {
                Session::Session{account, principal, } => principal,
            }
        }
    }

    impl Debug
        for Session {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for Session {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                Session::Session{account, principal, } => {
                    write!(_formatter, "TumblerOwnership.Session.Session(")?;
                    DafnyPrint::fmt_print(account, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(principal, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for Session {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (Session::Session{account, principal, }, Session::Session{account: _2_account, principal: _2_principal, }) => {
                    account == _2_account && principal == _2_principal
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for Session {}

    impl Hash
        for Session {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                Session::Session{account, principal, } => {
                    Hash::hash(account, _state);
                    Hash::hash(principal, _state)
                },
            }
        }
    }

    impl AsRef<Session>
        for Session {
        fn as_ref(&self) -> &Self {
            self
        }
    }
}
/// vault/proofs/TumblerAlgebra/TumblerSubtraction.dfy(2,1)
pub mod TumblerSubtraction {
    
}
/// vault/proofs/TwoSpace/TwoSpace.dfy(3,1)
pub mod TwoSpace {
    pub use ::std::rc::Rc;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::int;
    pub use ::dafny_runtime::Map;
    pub use ::dafny_runtime::Sequence;
    pub use ::dafny_runtime::_System::nat;
    pub use ::dafny_runtime::Set;
    pub use ::std::fmt::Debug;
    pub use ::std::fmt::Formatter;
    pub use ::std::fmt::Result;
    pub use ::dafny_runtime::DafnyPrint;
    pub use ::std::cmp::PartialEq;
    pub use ::std::cmp::Eq;
    pub use ::std::hash::Hash;
    pub use ::std::hash::Hasher;
    pub use ::std::convert::AsRef;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TwoSpace/TwoSpace.dfy(53,3)
        pub fn Origin(a: &Rc<Tumbler>) -> Rc<Tumbler> {
            Rc::new(Tumbler::Tumbler {
                    components: a.components().take(&(crate::TumblerHierarchy::_default::E1Pos(a) - int!(1)))
                })
        }
    }

    /// vault/proofs/TwoSpace/TwoSpace.dfy(18,3)
    #[derive(Clone)]
    pub enum TwoSpaceState {
        TwoSpaceState {
            C: Map<Rc<Tumbler>, Sequence<nat>>,
            M: Map<Rc<Tumbler>, Map<Rc<Tumbler>, Rc<Tumbler>>>,
            documents: Set<Rc<Tumbler>>
        }
    }

    impl TwoSpaceState {
        /// Returns a borrow of the field C
        pub fn C(&self) -> &Map<Rc<Tumbler>, Sequence<nat>> {
            match self {
                TwoSpaceState::TwoSpaceState{C, M, documents, } => C,
            }
        }
        /// Returns a borrow of the field M
        pub fn M(&self) -> &Map<Rc<Tumbler>, Map<Rc<Tumbler>, Rc<Tumbler>>> {
            match self {
                TwoSpaceState::TwoSpaceState{C, M, documents, } => M,
            }
        }
        /// Returns a borrow of the field documents
        pub fn documents(&self) -> &Set<Rc<Tumbler>> {
            match self {
                TwoSpaceState::TwoSpaceState{C, M, documents, } => documents,
            }
        }
    }

    impl Debug
        for TwoSpaceState {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for TwoSpaceState {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                TwoSpaceState::TwoSpaceState{C, M, documents, } => {
                    write!(_formatter, "TwoSpace.TwoSpaceState.TwoSpaceState(")?;
                    DafnyPrint::fmt_print(C, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(M, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(documents, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for TwoSpaceState {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (TwoSpaceState::TwoSpaceState{C, M, documents, }, TwoSpaceState::TwoSpaceState{C: _2_C, M: _2_M, documents: _2_documents, }) => {
                    C == _2_C && M == _2_M && documents == _2_documents
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for TwoSpaceState {}

    impl Hash
        for TwoSpaceState {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                TwoSpaceState::TwoSpaceState{C, M, documents, } => {
                    Hash::hash(C, _state);
                    Hash::hash(M, _state);
                    Hash::hash(documents, _state)
                },
            }
        }
    }

    impl AsRef<TwoSpaceState>
        for TwoSpaceState {
        fn as_ref(&self) -> &Self {
            self
        }
    }
}
/// vault/proofs/TwoSpace/TwoSpaceArrangement.dfy(2,1)
pub mod TwoSpaceArrangement {
    pub use ::std::rc::Rc;
    pub use crate::TumblerAlgebra::Tumbler;
    pub use ::dafny_runtime::_System::nat;
    pub use ::dafny_runtime::Map;
    pub use ::dafny_runtime::MapBuilder;
    pub use ::dafny_runtime::integer_range;
    pub use ::dafny_runtime::int;
    pub use ::dafny_runtime::DafnyInt;
    pub use ::dafny_runtime::seq;
    pub use ::std::fmt::Debug;
    pub use ::std::fmt::Formatter;
    pub use ::std::fmt::Result;
    pub use ::dafny_runtime::DafnyPrint;
    pub use ::std::cmp::PartialEq;
    pub use ::std::cmp::Eq;
    pub use ::std::hash::Hash;
    pub use ::std::hash::Hasher;
    pub use ::std::convert::AsRef;

    pub struct _default {}

    impl _default {
        /// vault/proofs/TwoSpace/TwoSpaceArrangement.dfy(26,3)
        pub fn WitnessArrangement(a: &Rc<Tumbler>, N: &nat, subspace: &nat) -> Map<Rc<Tumbler>, Rc<Tumbler>> {
            (&({
                let mut N = N.clone();
                let mut a = a.clone();
                let mut subspace = subspace.clone();
                Rc::new(move || -> Map<Rc<Tumbler>, Rc<Tumbler>>{
            let mut _coll0: MapBuilder<Rc<Tumbler>, Rc<Tumbler>> = MapBuilder::<Rc<Tumbler>, Rc<Tumbler>>::new();
            for __compr_0 in integer_range(int!(0), N.clone() + int!(1)) {
                let mut k: DafnyInt = __compr_0.clone();
                if int!(0) <= k.clone() && k.clone() < N.clone() + int!(1) {
                    _coll0.add(&Rc::new(Tumbler::Tumbler {
                                components: seq![subspace.clone(), k.clone() + int!(1)]
                            }), &a)
                }
            }
            _coll0.build()
        }) as Rc<dyn ::std::ops::Fn() -> _>
            }))()
        }
        /// vault/proofs/TwoSpace/TwoSpaceArrangement.dfy(82,3)
        pub fn OrdinalOffset(t: &Rc<Tumbler>, k: &nat) -> Rc<Tumbler> {
            Rc::new(Tumbler::Tumbler {
                    components: t.components().take(&(t.components().cardinality() - int!(1))).concat(&seq![t.components().get(&(t.components().cardinality() - int!(1))) + k.clone()])
                })
        }
    }

    /// vault/proofs/TwoSpace/TwoSpaceArrangement.dfy(89,3)
    #[derive(Clone)]
    pub enum Run {
        Run {
            vpos: Rc<Tumbler>,
            iaddr: Rc<Tumbler>,
            length: nat
        }
    }

    impl Run {
        /// Returns a borrow of the field vpos
        pub fn vpos(&self) -> &Rc<Tumbler> {
            match self {
                Run::Run{vpos, iaddr, length, } => vpos,
            }
        }
        /// Returns a borrow of the field iaddr
        pub fn iaddr(&self) -> &Rc<Tumbler> {
            match self {
                Run::Run{vpos, iaddr, length, } => iaddr,
            }
        }
        /// Returns a borrow of the field length
        pub fn length(&self) -> &nat {
            match self {
                Run::Run{vpos, iaddr, length, } => length,
            }
        }
    }

    impl Debug
        for Run {
        fn fmt(&self, f: &mut Formatter) -> Result {
            DafnyPrint::fmt_print(self, f, true)
        }
    }

    impl DafnyPrint
        for Run {
        fn fmt_print(&self, _formatter: &mut Formatter, _in_seq: bool) -> std::fmt::Result {
            match self {
                Run::Run{vpos, iaddr, length, } => {
                    write!(_formatter, "TwoSpaceArrangement.Run.Run(")?;
                    DafnyPrint::fmt_print(vpos, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(iaddr, _formatter, false)?;
                    write!(_formatter, ", ")?;
                    DafnyPrint::fmt_print(length, _formatter, false)?;
                    write!(_formatter, ")")?;
                    Ok(())
                },
            }
        }
    }

    impl PartialEq
        for Run {
        fn eq(&self, other: &Self) -> bool {
            match (
                    self,
                    other
                ) {
                (Run::Run{vpos, iaddr, length, }, Run::Run{vpos: _2_vpos, iaddr: _2_iaddr, length: _2_length, }) => {
                    vpos == _2_vpos && iaddr == _2_iaddr && length == _2_length
                },
                _ => {
                    false
                },
            }
        }
    }

    impl Eq
        for Run {}

    impl Hash
        for Run {
        fn hash<_H: Hasher>(&self, _state: &mut _H) {
            match self {
                Run::Run{vpos, iaddr, length, } => {
                    Hash::hash(vpos, _state);
                    Hash::hash(iaddr, _state);
                    Hash::hash(length, _state)
                },
            }
        }
    }

    impl AsRef<Run>
        for Run {
        fn as_ref(&self) -> &Self {
            self
        }
    }
}
/// vault/proofs/TwoSpace/TwoSpaceContent.dfy(2,1)
pub mod TwoSpaceContent {
    
}
/// vault/proofs/TwoSpace/TwoSpaceSeparation.dfy(2,1)
pub mod TwoSpaceSeparation {
    
}