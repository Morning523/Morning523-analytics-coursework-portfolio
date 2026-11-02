# Prioritising Four Business Cases at Citi

*Individual case exercise. Built entirely on public sources — no confidential Citi data is used or implied. Author: Menglin (Leo) Tsai.*

## The question

Citi's brief named four possible workstreams. Where should Citi focus first, what value could be created or protected, and how should the work be managed?

| Topic | Business problem | Commercial value at stake | Critical unknown | Initial action |
|---|---|---|---|---|
| P&L attribution | "Resolution of audit points" — open audit points on how P&L is explained and evidenced | Value protection: control integrity, less repeat remediation, defensible closure | Severity, deadline, owner, closure criteria | **Lead** — diagnose |
| Structured notes | "AI-driven scalability" — volumes rebounded; can growth scale without cost and risk rising in step? | Sustainable contribution and operating leverage (sales volume is not profit) | What drove Q3, and the economics per note | **Lead** — test drivers |
| Equity derivatives UI/UX | "UI/UX innovation" — no user or task named yet | Productivity, fewer errors and rework; conversion where client-facing | Who the user is, and what the task costs today | **Scope** — discover |
| Valuation & risk AI | "Deployment of new AI tools" — a tool looking for a specific valuation or risk task | Incremental productivity and decision support, net of cost and risk | Whether a valuable task is uncovered by Citi's tools | **Scope** — assess gap |

**Recommendation:** different value, different investment case. Lead where a decision can move now; scope the two whose user or gap is still unknown.

## 1. P&L attribution — triage first, then fix the right control failure

**What we know, what we don't.** The brief asks to resolve audit points on Equities P&L attribution but gives no finding, severity, deadline, or owner.

- **CONFIRMED** — Fed/OCC orders on data and controls (Oct 2020); OCC ended its 2024 amendment in Dec 2025, but the original 2020 OCC order remains in force.
- **CONFIRMED** — PRA/FCA fined Citigroup Global Markets £61.6m (May 2024).
- **INFERENCE** — these regulatory items are context for why evidence matters; they are not evidence about this specific finding.
- **UNKNOWN** — finding text, severity, deadline, owner, closure criteria.

**Lead hypothesis (explained, not re-performable):** a second reviewer can't reach the same result from retained data, versions and rules — across four possible failure points: (A) data snapshots/sources differ, (B) model/version drift or unexplained P&L, (C) process ownership gaps (manual adjustments, sign-offs), (D) evidence that the right answer exists but can't be shown. If the result *can* already be re-performed, the real gap is how "closure" was defined (scope, owner, criteria).

**Value at stake:** not a new control tool — defensible closure, control integrity, less repeat remediation, lower operational risk. Proposed test: walk one flagged case end-to-end (AI in shadow mode only, never making the call).

**Measures:** closure evidence accepted by audit; time to re-perform a case; repeat findings/remediation rework; unexplained P&L within thresholds.

**Recommendation:** first priority for triage — not automatically the biggest investment. Confirm severity, deadline, owner and closure criteria, then walk a flagged case before choosing a fix. No savings are quantified without Citi data; regulatory items are firm-level context only.

*Sources: Fed/OCC (2020); OCC NR 2025-131; PRA/FCA final notices (22 May 2024).*

## 2. Structured notes — turn the rebound into sustainable contribution

**CONFIRMED (Citi, US SEC-registered notes, Q3 2025, per SRP):** $4.1bn sales, ~+60% on Q2 2025, 1,057 notes issued, ~$3.9m average size.

**Peer check (Q3 vs Q2 2025, same source):** Citi ~+60% ($4.1bn) vs. J.P. Morgan +25.7% ($5.4bn) — **INFERENCE:** peers rebounded too, but Citi grew faster. **UNKNOWN:** a same-basis Q2 split isn't public (the ≈$2.6bn figure is only back-calculated); margins and cost per note are unknown — sales volume is not profit.

**What drove the growth?** Sales = notes issued × average size. More notes implies a workload/capacity/cost-per-note question; bigger notes implies a pricing/risk-adjusted-contribution question; a mix shift implies a segment-economics question.

**Where could value leak? (hypotheses, not confirmed bottlenecks):** enquiry-to-quote conversion, quote turnaround time, quote-to-win conversion, product fit, rework/manual effort, risk capacity and pricing. **INFERENCE:** Citi issues on multi-issuer platforms such as SIMON (where it is a strategic investor, Feb 2022), where quotes compete side by side.

**What would justify investment?** Contribution after hedging, distribution, funding and operating costs; capacity released; cost to serve; feasibility. Value test: conversion value = incremental trades × risk-adjusted contribution per trade.

**Recommendation:** request Q2–Q3 issuance and quote-level data, find the actual growth source and the largest measurable leakage, then pick the highest-value fix. No growth waterfall exists without this data; no margin data is assumed.

*Sources: SRP (27 Feb, 30 Oct, 3 Nov 2025); Business Wire (15 Feb 2022).*

## 3. Equity derivatives UI/UX — invest in workflow value, not screens

The brief names no user or task. Friction and value below are hypotheses to observe, not findings: (1) who is the actual user? (2) which workflow has material friction? (3) who owns the workflow/interface? (4) who can authorise changes? (5) what measurable value could it create?

**Possible users (all hypotheses):** traders/risk managers (internal desk tools); advisers/distributors (quote and order screens, often third-party platforms); institutional clients (electronic trading, post-trade).

**Baseline before changing anything:** task time and waiting time, rework and error rates, throughput and task volume, conversion where client-facing. Capacity released is not cash saved until volumes or roles actually change. Value test: task volume × verified time saved × loaded cost.

**Recommendation:** pick one user group and one high-value workflow, baseline it, then invest only if the value of improving it justifies the cost. Channel context only: Citi is an issuer on SIMON and a strategic investor — that does not mean Citi controls SIMON's interface. No savings assumed before a baseline.

*Source: Business Wire (15 Feb 2022).*

## 4. Valuation & risk AI — prove incremental value before investing

**What Citi already runs (public):** AI tools used by colleagues in 84 countries, adoption above 70% (4Q25 results, Jan 2026); Citi Stylus Workspaces — agentic AI, phased rollout (Sep 2025); machine learning already used in FX, Equities and Rates e-trading (4Q25 presentation). **INFERENCE:** enterprise-wide adoption doesn't prove a *given* front-office task is covered, or that it isn't.

**Is there a valuable gap?** Assess each candidate task on: unmet need, existing tool coverage, productivity/decision value, build and integration cost, model and operational risk, governance and upkeep.

**One candidate to test (hypothesis):** AI-assisted explanation of intraday risk moves, from approved risk outputs only — it never sets prices, risk numbers, or approves decisions. Measures: time saved, source accuracy, unsupported claims, review effort, net benefit after control and run costs.

**Recommendation:** test the candidate against existing Citi tools first; proceed only if incremental value is meaningful and controls are acceptable, otherwise reuse or stop. Desk-level tool use at Citi is not public — this recommendation does not assume it.

*Sources: Citi 4Q25 results presentation and call (14 Jan 2026); Citi press release on Stylus Workspaces (22 Sep 2025); SR 11-7; PRA SS1/23.*

## Prioritisation across all four

| | P&L attribution | Structured notes | Equity derivatives UI/UX | Valuation & risk AI |
|---|---|---|---|---|
| Potential commercial value | Potentially high, severity-dependent | Potentially material, contribution unverified | Unknown, depends on the workflow | Unknown, net of cost and risk |
| Urgency | Conditional on severity/deadline/closure obligations | Medium — momentum window | Unknown — no stated deadline | Unknown — existing capability doesn't set urgency |
| Confidence in evidence | Medium — ask stated, finding not | Medium — volumes public, margins not | Low — no user named | Medium — capability public, gap not |
| Cost of initial discovery | Low — one flagged case | Medium — Q2–Q3 and quote data | Low — a few walkthroughs | Medium — task and tool review |
| Implementation risk | High — audit and regulators | Medium — documents, suitability | Scope-dependent | High — model risk, permissions |
| Decision type | **Risk triage priority** | **Commercial discovery priority** | Scope | Scope |

What would change this picture: audit severity and deadline · notes contribution economics · measured UI/UX friction/ownership/value · an uncovered AI task with positive net benefit. Ratings are an initial judgement from the brief and public evidence, for discussion — low-cost discovery is not the same as low implementation risk, and the two "scope" opportunities are not lower-value by default.

## How the four cases should be managed

**Principle:** separate business cases, coordinate only proven dependencies, share capabilities only where value justifies it.

- UI/UX + notes: coordinate only if workflow changes affect the quote or distribution funnel.
- UI/UX + AI: coordinate only if AI insight must sit inside the front-office workflow to create value.
- P&L + AI: reuse lineage/version tracking only where appropriate and justified.
- AI governance: one common framework, with review for each individual use case.

**Three-week plan:**

1. **Confirm** — scope, accountable owners, required data, decision criteria.
2. **Diagnose** — P&L control hypothesis; notes growth drivers; one UI/UX workflow; AI capability gap.
3. **Recommend** — a next step per opportunity: business case, coordinate further, investigate further, or stop.

**Week 3 decision gates:** P&L — is the control gap established, with an owner and closure requirement? Notes — is there a measurable commercial/efficiency opportunity worth pursuing? UI/UX — is there a validated workflow problem with a credible benefit? AI — is there an unmet need beyond Citi's tools, with acceptable risk and positive net benefit?

This produces a decision pack, not remediation or an approved programme — it depends on data access and people's time. Owners referenced throughout are roles to confirm, not named individuals; timing is an engagement-design assumption.
