# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **all sections** — 243 questions (214 single-answer, 29 multi-select). Random-guess baseline: **25.0%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| similar_twin_member | 32.1% | 41% | 27.9% |
| stem_keyword_overlap | 26.7% | 86% | 26.5% |
| position_B | 26.2% | 100% | 26.2% |
| position_A | 26.2% | 100% | 26.2% |
| longest_option | 25.3% | 100% | 25.3% |
| most_absolute | 25.3% | 36% | 25.1% |
| position_C | 24.8% | 100% | 24.8% |
| avoid_longest | 24.8% | 95% | 24.8% |
| avoid_hedged | 24.1% | 30% | 24.7% |
| most_hedged | 21.7% | 30% | 24.0% |
| least_absolute | 20.8% | 36% | 23.5% |
| position_D | 22.9% | 100% | 22.9% |
| shortest_option | 16.8% | 100% | 16.8% |
| odd_one_out | 13.2% | 100% | 13.2% |
| code_formatted_only | 25.9% | 20% | – |
| numeric_middle | 25.0% | 17% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (48)

- `s1-q012` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 70, ratio 1.17)
- `s1-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 70 chars vs longest distractor 69, ratio 1.01)
- `s1-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 80 chars vs longest distractor 65, ratio 1.23)
- `s1-q020` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 93 chars vs longest distractor 81, ratio 1.15)
- `s1-q026` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 69 chars vs longest distractor 60, ratio 1.15)
- `s1-q035` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 85 chars vs longest distractor 79, ratio 1.08)
- `s1-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 70, ratio 1.01)
- `s1-q040` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 41 chars vs longest distractor 34, ratio 1.21)
- `s2-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 27 chars vs longest distractor 25, ratio 1.08)
- `s2-q018` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 101 chars vs longest distractor 78, ratio 1.29)
- `s2-q023` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 61 chars vs longest distractor 60, ratio 1.02)
- `s2-q024` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 61 chars vs longest distractor 49, ratio 1.24)
- `s2-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 94 chars vs longest distractor 82, ratio 1.15)
- `s3-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 65 chars vs longest distractor 49, ratio 1.33)
- `s3-q017` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 79, ratio 1.25)
- `s3-q024` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 44 chars vs longest distractor 42, ratio 1.05)
- `s3-q028` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 78 chars vs longest distractor 77, ratio 1.01)
- `s3-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 96, ratio 1.03)
- `s3-q034` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 130 chars vs longest distractor 124, ratio 1.05)
- `s3-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 79, ratio 1.11)
- `s3-q039` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 95 chars vs longest distractor 77, ratio 1.23)
- `s3-q052` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 72, ratio 1.14)
- `s4-q012` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 161 chars vs longest distractor 144, ratio 1.12)
- `s4-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 91 chars vs longest distractor 89, ratio 1.02)
- `s4-q019` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 54, ratio 1.02)
- `s4-q020` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 112 chars vs longest distractor 100, ratio 1.12)
- `s4-q027` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 71, ratio 1.14)
- `s4-q032` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 108 chars vs longest distractor 86, ratio 1.26)
- `s4-q040` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 62, ratio 1.15)
- `s4-q042` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 74 chars vs longest distractor 66, ratio 1.12)
- `s5-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 74, ratio 1.19)
- `s5-q016` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 89, ratio 1.11)
- `s5-q018` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 92 chars vs longest distractor 89, ratio 1.03)
- `s5-q025` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 104 chars vs longest distractor 96, ratio 1.08)
- `s5-q026` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 71, ratio 1.14)
- `s5-q036` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 75 chars vs longest distractor 72, ratio 1.04)
- `s6-q020` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 63 chars vs longest distractor 62, ratio 1.02)
- `s6-q021` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 112 chars vs longest distractor 104, ratio 1.08)
- `s6-q032` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 128 chars vs longest distractor 124, ratio 1.03)
- `s6-q034` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 97 chars vs longest distractor 84, ratio 1.15)
- `s6-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 57 chars vs longest distractor 55, ratio 1.04)
- `s7-q015` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 59 chars vs longest distractor 46, ratio 1.28)
- `s7-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 46, ratio 1.20)
- `s7-q024` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 79 chars vs longest distractor 68, ratio 1.16)
- `s7-q028` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 107 chars vs longest distractor 97, ratio 1.10)
- `s8-q013` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 72, ratio 1.12)
- `s8-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 24 chars vs longest distractor 20, ratio 1.20)
- `s8-q021` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 160 chars vs longest distractor 140, ratio 1.14)

## Cross-question duplicate option texts

- "`estimator.options.dynamical_decoupling.enable = true`…" appears as: s6-q026:wrong, s6-q039:correct
- "`estimator.options.resilience.zne_mitigation = true`…" appears as: s6-q026:correct, s6-q039:wrong
