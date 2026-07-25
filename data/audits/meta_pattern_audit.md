# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s6** — 30 questions (27 single-answer, 3 multi-select). Random-guess baseline: **25.0%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| similar_twin_member | 40.0% | 59% | 33.9% |
| position_A | 36.8% | 70% | 33.3% |
| position_B | 36.8% | 70% | 33.3% |
| position_C | 36.8% | 70% | 33.3% |
| position_D | 32.3% | 69% | 30.0% |
| numeric_middle | 30.4% | 27% | 26.5% |
| avoid_longest | 26.0% | 95% | 25.9% |
| stem_keyword_overlap | 25.7% | 79% | 25.5% |
| longest_option | 23.3% | 100% | 23.3% |
| shortest_option | 21.7% | 100% | 21.7% |
| odd_one_out | 10.7% | 100% | 10.7% |
| most_hedged | 25.0% | 23% | – |
| avoid_hedged | 28.2% | 23% | – |
| least_absolute | 12.8% | 23% | – |
| most_absolute | 37.2% | 23% | – |
| code_formatted_only | 20.4% | 10% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (7)

- `s6-q013` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 108 chars vs longest distractor 101, ratio 1.07) (in >=1 displayed pool variant)
- `s6-q020` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 63 chars vs longest distractor 62, ratio 1.02) (in >=1 displayed pool variant)
- `s6-q021` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 112 chars vs longest distractor 104, ratio 1.08) (in >=1 displayed pool variant)
- `s6-q031` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 94 chars vs longest distractor 93, ratio 1.01) (in >=1 displayed pool variant)
- `s6-q032` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 128 chars vs longest distractor 124, ratio 1.03) (in >=1 displayed pool variant)
- `s6-q034` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 97 chars vs longest distractor 84, ratio 1.15) (in >=1 displayed pool variant)
- `s6-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 57 chars vs longest distractor 55, ratio 1.04) (in >=1 displayed pool variant)

## Cross-question duplicate option texts

- "`estimator.options.dynamical_decoupling.enable = true`…" appears as: s6-q026:wrong, s6-q039:correct
- "`estimator.options.resilience.zne_mitigation = true`…" appears as: s6-q026:correct, s6-q039:wrong
