# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s5** — 43 questions (40 single-answer, 3 multi-select). Random-guess baseline: **24.0%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_C | 32.0% | 78% | 30.3% |
| position_B | 31.9% | 78% | 30.2% |
| numeric_middle | 44.1% | 28% | 29.6% |
| shortest_option | 27.4% | 100% | 27.4% |
| position_A | 28.1% | 80% | 27.3% |
| similar_twin_member | 32.0% | 35% | 26.8% |
| avoid_longest | 27.5% | 77% | 26.7% |
| position_D | 26.0% | 77% | 25.5% |
| stem_keyword_overlap | 21.9% | 73% | 22.5% |
| longest_option | 16.9% | 100% | 16.9% |
| odd_one_out | 14.0% | 100% | 14.0% |
| most_hedged | 12.9% | 16% | – |
| avoid_hedged | 19.4% | 16% | – |
| least_absolute | 9.7% | 14% | – |
| most_absolute | 34.2% | 14% | – |
| code_formatted_only | 17.2% | 16% | – |
| largest_image_option | 38.1% | 18% | – |
| smallest_image_option | 20.2% | 18% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (4)

- `s5-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 77, ratio 1.14) (in >=1 displayed pool variant)
- `s5-q025` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 104 chars vs longest distractor 96, ratio 1.08) (in >=1 displayed pool variant)
- `s5-q026` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 71, ratio 1.14) (in >=1 displayed pool variant)
- `s5-q036` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 75 chars vs longest distractor 72, ratio 1.04) (in >=1 displayed pool variant)
