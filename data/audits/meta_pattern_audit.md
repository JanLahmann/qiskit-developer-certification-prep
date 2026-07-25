# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s8** — 16 questions (14 single-answer, 2 multi-select). Random-guess baseline: **23.9%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_A | 38.5% | 74% | 34.7% |
| position_B | 37.7% | 76% | 34.4% |
| similar_twin_member | 42.0% | 49% | 32.9% |
| position_D | 30.6% | 70% | 28.6% |
| position_C | 29.4% | 73% | 27.9% |
| avoid_longest | 25.8% | 93% | 25.6% |
| longest_option | 25.0% | 100% | 25.0% |
| shortest_option | 24.3% | 100% | 24.3% |
| numeric_middle | 16.7% | 33% | 21.5% |
| stem_keyword_overlap | 15.2% | 93% | 15.8% |
| odd_one_out | 9.3% | 100% | 9.3% |
| most_hedged | – | 0% | – |
| avoid_hedged | – | 0% | – |
| least_absolute | 0.0% | 14% | – |
| most_absolute | 65.0% | 14% | – |
| code_formatted_only | – | 0% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (4)

- `s8-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 96 chars vs longest distractor 94, ratio 1.02) (in >=1 displayed pool variant)
- `s8-q013` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 78, ratio 1.04) (in >=1 displayed pool variant)
- `s8-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 24 chars vs longest distractor 20, ratio 1.20) (in >=1 displayed pool variant)
- `s8-q021` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 160 chars vs longest distractor 140, ratio 1.14) (in >=1 displayed pool variant)
