# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s4** — 36 questions (32 single-answer, 4 multi-select). Random-guess baseline: **22.7%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_C | 32.8% | 76% | 30.4% |
| position_B | 32.5% | 77% | 30.2% |
| position_D | 32.5% | 77% | 30.2% |
| position_A | 32.0% | 78% | 29.9% |
| shortest_option | 28.4% | 100% | 28.4% |
| longest_option | 25.0% | 100% | 25.0% |
| most_absolute | 24.5% | 65% | 23.9% |
| stem_keyword_overlap | 23.8% | 100% | 23.8% |
| avoid_longest | 23.6% | 100% | 23.6% |
| avoid_hedged | 24.0% | 60% | 23.4% |
| code_formatted_only | 20.8% | 30% | 22.1% |
| most_hedged | 20.8% | 60% | 21.6% |
| least_absolute | 18.5% | 65% | 20.0% |
| odd_one_out | 10.8% | 100% | 10.8% |
| numeric_middle | 23.3% | 18% | – |
| similar_twin_member | 38.5% | 23% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (8)

- `s4-q012` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 161 chars vs longest distractor 144, ratio 1.12) (in >=1 displayed pool variant)
- `s4-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 91 chars vs longest distractor 90, ratio 1.01) (in >=1 displayed pool variant)
- `s4-q019` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 54, ratio 1.02) (in >=1 displayed pool variant)
- `s4-q020` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 112 chars vs longest distractor 102, ratio 1.10) (in >=1 displayed pool variant)
- `s4-q027` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 74, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q032` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 108 chars vs longest distractor 99, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q040` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 65, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q042` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 74 chars vs longest distractor 66, ratio 1.12) (in >=1 displayed pool variant)
