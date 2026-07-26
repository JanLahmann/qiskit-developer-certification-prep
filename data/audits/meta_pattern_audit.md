# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **all sections** — 268 questions (239 single-answer, 29 multi-select). Random-guess baseline: **23.8%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_B | 32.7% | 77% | 30.6% |
| similar_twin_member | 39.9% | 42% | 30.5% |
| position_A | 32.3% | 76% | 30.3% |
| position_C | 32.0% | 76% | 30.0% |
| position_D | 31.5% | 76% | 29.6% |
| most_absolute | 29.8% | 31% | 25.7% |
| avoid_hedged | 28.0% | 28% | 25.0% |
| avoid_longest | 24.2% | 96% | 24.2% |
| stem_keyword_overlap | 23.6% | 84% | 23.6% |
| longest_option | 23.2% | 100% | 23.2% |
| shortest_option | 22.7% | 100% | 22.7% |
| most_hedged | 17.5% | 28% | 22.0% |
| least_absolute | 15.8% | 31% | 21.3% |
| odd_one_out | 11.2% | 100% | 11.2% |
| code_formatted_only | 19.3% | 18% | – |
| numeric_middle | 34.8% | 17% | – |
| largest_image_option | 11.1% | 2% | – |
| smallest_image_option | 25.0% | 2% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (57)

- `s1-q012` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 70, ratio 1.17) (in >=1 displayed pool variant)
- `s1-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 70 chars vs longest distractor 69, ratio 1.01) (in >=1 displayed pool variant)
- `s1-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 80 chars vs longest distractor 65, ratio 1.23) (in >=1 displayed pool variant)
- `s1-q020` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 93 chars vs longest distractor 81, ratio 1.15) (in >=1 displayed pool variant)
- `s1-q026` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 69 chars vs longest distractor 60, ratio 1.15) (in >=1 displayed pool variant)
- `s1-q035` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 85 chars vs longest distractor 79, ratio 1.08) (in >=1 displayed pool variant)
- `s1-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 70, ratio 1.01) (in >=1 displayed pool variant)
- `s1-q040` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 41 chars vs longest distractor 34, ratio 1.21) (in >=1 displayed pool variant)
- `s1-q048` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 91 chars vs longest distractor 83, ratio 1.10) (in >=1 displayed pool variant)
- `s2-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 27 chars vs longest distractor 25, ratio 1.08) (in >=1 displayed pool variant)
- `s2-q018` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 101 chars vs longest distractor 78, ratio 1.29) (in >=1 displayed pool variant)
- `s2-q022` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 50 chars vs longest distractor 46, ratio 1.09) (in >=1 displayed pool variant)
- `s2-q023` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 61 chars vs longest distractor 60, ratio 1.02) (in >=1 displayed pool variant)
- `s2-q024` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 61 chars vs longest distractor 49, ratio 1.24) (in >=1 displayed pool variant)
- `s2-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 94 chars vs longest distractor 82, ratio 1.15) (in >=1 displayed pool variant)
- `s2-q036` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 109 chars vs longest distractor 99, ratio 1.10) (in >=1 displayed pool variant)
- `s2-q037` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 87 chars vs longest distractor 80, ratio 1.09) (in >=1 displayed pool variant)
- `s3-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 65 chars vs longest distractor 54, ratio 1.20) (in >=1 displayed pool variant)
- `s3-q017` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 79, ratio 1.25) (in >=1 displayed pool variant)
- `s3-q017` (predict-output) — **stem_echo_tell** [medium]: correct option echoes stem vocabulary (overlap 4 vs best distractor 2) (in >=1 displayed pool variant)
- `s3-q024` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 44 chars vs longest distractor 42, ratio 1.05) (in >=1 displayed pool variant)
- `s3-q028` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 78 chars vs longest distractor 77, ratio 1.01) (in >=1 displayed pool variant)
- `s3-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 96, ratio 1.03) (in >=1 displayed pool variant)
- `s3-q034` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 130 chars vs longest distractor 124, ratio 1.05) (in >=1 displayed pool variant)
- `s3-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 79, ratio 1.11) (in >=1 displayed pool variant)
- `s3-q039` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 95 chars vs longest distractor 77, ratio 1.23) (in >=1 displayed pool variant)
- `s3-q052` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 72, ratio 1.14) (in >=1 displayed pool variant)
- `s3-q052` (predict-output) — **stem_echo_tell** [medium]: correct option echoes stem vocabulary (overlap 5 vs best distractor 2) (in >=1 displayed pool variant)
- `s4-q012` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 161 chars vs longest distractor 144, ratio 1.12) (in >=1 displayed pool variant)
- `s4-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 91 chars vs longest distractor 90, ratio 1.01) (in >=1 displayed pool variant)
- `s4-q019` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 54, ratio 1.02) (in >=1 displayed pool variant)
- `s4-q020` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 112 chars vs longest distractor 102, ratio 1.10) (in >=1 displayed pool variant)
- `s4-q027` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 74, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q032` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 108 chars vs longest distractor 99, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q040` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 65, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q042` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 74 chars vs longest distractor 66, ratio 1.12) (in >=1 displayed pool variant)
- `s5-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 77, ratio 1.14) (in >=1 displayed pool variant)
- `s5-q016` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 89, ratio 1.11) (in >=1 displayed pool variant)
- `s5-q018` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 92 chars vs longest distractor 89, ratio 1.03) (in >=1 displayed pool variant)
- `s5-q025` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 104 chars vs longest distractor 96, ratio 1.08) (in >=1 displayed pool variant)
- `s5-q026` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 71, ratio 1.14) (in >=1 displayed pool variant)
- `s5-q036` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 75 chars vs longest distractor 72, ratio 1.04) (in >=1 displayed pool variant)
- `s6-q013` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 108 chars vs longest distractor 101, ratio 1.07) (in >=1 displayed pool variant)
- `s6-q020` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 63 chars vs longest distractor 62, ratio 1.02) (in >=1 displayed pool variant)
- `s6-q021` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 112 chars vs longest distractor 104, ratio 1.08) (in >=1 displayed pool variant)
- `s6-q031` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 94 chars vs longest distractor 93, ratio 1.01) (in >=1 displayed pool variant)
- `s6-q032` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 128 chars vs longest distractor 124, ratio 1.03) (in >=1 displayed pool variant)
- `s6-q034` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 97 chars vs longest distractor 84, ratio 1.15) (in >=1 displayed pool variant)
- `s6-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 57 chars vs longest distractor 55, ratio 1.04) (in >=1 displayed pool variant)
- `s7-q015` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 59 chars vs longest distractor 52, ratio 1.13) (in >=1 displayed pool variant)
- `s7-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 50, ratio 1.10) (in >=1 displayed pool variant)
- `s7-q023` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 72 chars vs longest distractor 62, ratio 1.16) (in >=1 displayed pool variant)
- `s7-q024` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 79 chars vs longest distractor 68, ratio 1.16) (in >=1 displayed pool variant)
- `s7-q028` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 107 chars vs longest distractor 97, ratio 1.10) (in >=1 displayed pool variant)
- `s7-q036` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 39 chars vs longest distractor 37, ratio 1.05) (in >=1 displayed pool variant)
- `s8-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 96 chars vs longest distractor 94, ratio 1.02) (in >=1 displayed pool variant)
- `s8-q013` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 78, ratio 1.04) (in >=1 displayed pool variant)
- `s8-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 24 chars vs longest distractor 20, ratio 1.20) (in >=1 displayed pool variant)
- `s8-q021` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 160 chars vs longest distractor 140, ratio 1.14) (in >=1 displayed pool variant)

## Cross-question duplicate option texts

- "`estimator.options.dynamical_decoupling.enable = true`…" appears as: s6-q026:wrong, s6-q039:correct
- "`estimator.options.resilience.zne_mitigation = true`…" appears as: s6-q026:correct, s6-q039:wrong
