# The narrowing lattice, and exactly when attribution depends on order

**2026-08-28.** P3.2. Formalises what [`paper/draft.md`](paper/draft.md) §5 argues in prose.

**It found an error in the argument it was meant to support**, in the specification's own
illustrative example and in the paper that reproduced it. The correction is in §4 and it makes the
claim sharper rather than weaker.

---

## 1 · The lattice

Let `V = {APPROVE, REVIEW, ESCALATE, REJECT}` ordered by severity:

```
APPROVE  <  REVIEW  <  ESCALATE  <  REJECT
```

`(V, ≤)` is a total order, hence a join-semilattice where `a ∨ b = max(a, b)`. Write `⊥ = APPROVE`
for the least element — the verdict when nothing objects.

A **control** `c` observes a request and proposes `p(c) ∈ V`. Controls propose; they do not assign.
Composition is join:

```
verdict(C) = ⊥ ∨ p(c₁) ∨ p(c₂) ∨ … ∨ p(cₙ)    =    max over C of p
```

This is what *"a control may only narrow"* means operationally, and stating it as a join rather than
as a prohibition matters: **widening is not forbidden, it is inexpressible.** A control returning an
opinion that gets joined has no code path by which to loosen anything, so there is nothing to audit.
A design that instead lets controls assign a verdict and then checks for widening satisfies the same
requirement while carrying a bug surface this one does not have.

---

## 2 · Proposition 1 — the verdict is order-independent

`max` is commutative, associative and idempotent. Therefore for any permutation `σ` of `C`:

```
verdict(σ(C)) = verdict(C)
```

**So order-independence of the verdict is a theorem, not a requirement.** An implementation cannot
fail it except by leaving the lattice — by letting some control assign rather than propose. That is
worth knowing, because it means the corresponding clause is a consequence to be checked rather than
a discipline to be maintained, and an implementation may reorder or parallelise its controls freely.

---

## 3 · Attribution, defined

Fix an evaluation order `σ = (c₁, …, cₙ)`. Let `r₀ = ⊥` and `rᵢ = rᵢ₋₁ ∨ p(cᵢ)` be the running
verdict.

Control `cᵢ` **narrows** under `σ` when `rᵢ > rᵢ₋₁` — strictly. Let `N(σ)` be the subsequence of
controls that narrow.

**Attribution** is the last element of `N(σ)`, or undefined when `N(σ)` is empty (every control
proposed `⊥`; nothing decided because there was nothing to decide).

`N(σ)` is well defined precisely because widening is impossible: a control proposing something no
stricter than the running verdict changes nothing, so it did not narrow.

---

## 4 · Proposition 2 — attribution is the *first* control attaining the maximum

Let `m = verdict(C)` and let `A = { c ∈ C : p(c) = m }`, the **argmax set**.

> **Claim.** For any order `σ` with `m > ⊥`, the last element of `N(σ)` is the earliest member of
> `A` in `σ`.

*Proof.* The running verdict `rᵢ` is non-decreasing and bounded above by `m`. Let `cₖ` be the
earliest member of `A` in `σ`. Then `rₖ = rₖ₋₁ ∨ m = m`, and since `rₖ₋₁ < m` — no control before
`cₖ` proposed `m`, and all proposals are `≤ m` — `cₖ` narrows. For every `j > k`, `rⱼ₋₁ = m` already,
so `rⱼ = m ∨ p(cⱼ) = m` and `cⱼ` does not narrow. Hence `cₖ` is the last narrower. ∎

**Corollary.** Attribution is order-dependent **if and only if `|A| > 1`.**

If exactly one control attains the maximum, every order attributes to that control. **Order only
matters when there is a tie at the top.**

---

## 5 · The correction

Both the specification's rationale for its attribution clause and §5.1 of the paper illustrate
order-dependence with this example:

> treasury narrows `APPROVE` to `REVIEW`, and risk then narrows `REVIEW` to `ESCALATE` — the answer
> is `ESCALATE` either way round, but the control that *determined* it differs.

**It does not differ.** Here `m = ESCALATE` and `A = {risk}`, so by Proposition 2 attribution is
`risk` under both orders. Enumerated:

| Order | Narrowers | Attributed |
|---|---|---|
| treasury, risk | treasury, risk | **risk** |
| risk, treasury | risk | **risk** |

The example demonstrates that the *verdict* is order-independent, which was never in doubt, and
demonstrates nothing about attribution.

A correct witness needs a tie. Take a sanctioned counterparty whose payment a spending limit also
refuses — both propose `REJECT`, so `|A| = 2`:

| Order | Narrowers | Attributed |
|---|---|---|
| sanctions, treasury | sanctions | **sanctions** |
| treasury, sanctions | treasury | **treasury** |

**This is the same case the dispositive-control clause was written for**, and the formalisation
explains why it had to exist rather than merely recording that it does. Ties at the maximum are not
an edge case in this domain: a barred counterparty and an exhausted budget both produce `REJECT`,
and any two categorical refusals collide at the top of the lattice by construction.

### What the correction does to the argument

**It sharpens it.** The paper claimed *attribution depends on evaluation order*. The precise claim is:

> Attribution depends on evaluation order **exactly when more than one control attains the maximum
> severity** — and in a system with categorical controls, that is the common case rather than a
> corner.

Everything that followed still holds. A specification requiring attribution must still make order
normative, because it cannot know in advance whether a given decision has a tie at the top. But the
reason is now stated exactly, and the dispositive-control mechanism stops looking like a patch and
starts looking like the resolution of a tie the lattice cannot break on its own.

**A total order on verdicts cannot distinguish two controls that both reach the maximum. Something
outside the lattice has to, and declaring a precedence among dispositive controls is that
something.**

---

## 6 · Proposition 3 — dispositive controls restore determinacy

Let `D ⊆ C` be a declared, totally ordered set of dispositive controls. Redefine attribution:

```
attribution(σ) = the ≺-greatest member of D whose finding is present, if any;
                 otherwise the last element of N(σ)
```

Where a dispositive control's finding is present, attribution no longer reads `σ` at all, so it is
order-independent by construction. Where none is present, Proposition 2 applies and attribution is
order-independent iff `|A| = 1`.

Two consequences follow directly and both are already required:

1. **A dispositive control must record its finding unconditionally.** Attribution now depends on
   the finding being *present*, not on its having changed the verdict. A control that stays silent
   when it did not narrow cannot be dispositive.
2. **`D` and its precedence must be declared in advance.** An implementation free to nominate `D`
   after the fact can attribute any decision to anything, which is the failure the whole mechanism
   exists to prevent.

---

## 7 · What this is not

**Not machine-checked.** Proposition 2 is a paragraph of ordinary mathematics and the enumeration
in §5 was run, but nothing here is verified in a proof assistant. Intent-Driven Computing
(arXiv:2605.24036) has a Coq proof of narrowing under composition; this note has a proof a reader
checks by reading. That is a real difference in assurance and it is stated rather than blurred.

**Not a claim about the lattice.** Join-semilattice composition of security decisions is old.
Proposition 1 is textbook. The content here is Proposition 2 and its corollary — the precise
condition under which attribution becomes indeterminate — and the observation that resolving it
requires structure outside the lattice.

**Not a defence of the total order.** That `ESCALATE > REVIEW` is a normative choice made because
`REVIEW` is pausable and `ESCALATE` is blocking. Nothing here proves it; a different ordering would
give a different lattice and the propositions would still hold.

---

## 8 · Downstream corrections

| Where | Change |
|---|---|
| `aegs/spec/04-verdicts.md`, VERD-4 rationale | Illustrative example replaced with one that exhibits the property, and the corollary stated |
| `research/paper/draft.md` §5.1–§5.2 | Same correction, plus the sharpened claim |
| `tesoro/tests/test_invariants.py` | Both propositions enumerated over permutations against the real verdict resolution |
