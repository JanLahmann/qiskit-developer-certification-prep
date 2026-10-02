# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s8** — 20 questions (18 single-answer, 2 multi-select). Random-guess baseline: **23.3%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| similar_twin_member | 39.9% | 44% | 30.6% |
| position_D | 30.1% | 74% | 28.3% |
| position_A | 29.5% | 75% | 28.0% |
| shortest_option | 27.9% | 100% | 27.9% |
| position_C | 29.2% | 76% | 27.8% |
| position_B | 28.8% | 77% | 27.5% |
| avoid_longest | 26.1% | 94% | 25.9% |
| numeric_middle | 23.9% | 39% | 23.6% |
| longest_option | 19.4% | 100% | 19.4% |
| stem_keyword_overlap | 15.2% | 89% | 16.1% |
| odd_one_out | 12.9% | 100% | 12.9% |
| most_hedged | 0.0% | 4% | – |
| avoid_hedged | 25.0% | 4% | – |
| least_absolute | 0.0% | 17% | – |
| most_absolute | 56.7% | 17% | – |
| code_formatted_only | – | 0% | – |
| largest_image_option | 62.5% | 6% | – |
| smallest_image_option | 0.0% | 6% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (4)

- `s8-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 96 chars vs longest distractor 94, ratio 1.02) (in >=1 displayed pool variant)
- `s8-q013` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 78, ratio 1.04) (in >=1 displayed pool variant)
- `s8-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 24 chars vs longest distractor 20, ratio 1.20) (in >=1 displayed pool variant)
- `s8-q021` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 160 chars vs longest distractor 140, ratio 1.14) (in >=1 displayed pool variant)
