# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s5** — 30 questions (27 single-answer, 3 multi-select). Random-guess baseline: **23.3%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_C | 35.0% | 74% | 32.0% |
| position_B | 34.3% | 76% | 31.6% |
| position_A | 33.7% | 77% | 31.3% |
| numeric_middle | 49.5% | 26% | 30.2% |
| position_D | 30.3% | 73% | 28.4% |
| stem_keyword_overlap | 26.0% | 100% | 26.0% |
| avoid_longest | 25.2% | 100% | 25.2% |
| shortest_option | 25.0% | 100% | 25.0% |
| longest_option | 22.2% | 100% | 22.2% |
| odd_one_out | 8.2% | 100% | 8.2% |
| most_hedged | 12.9% | 23% | – |
| avoid_hedged | 19.4% | 23% | – |
| least_absolute | 9.7% | 21% | – |
| most_absolute | 34.2% | 21% | – |
| code_formatted_only | 12.5% | 24% | – |
| similar_twin_member | 40.7% | 22% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (6)

- `s5-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 77, ratio 1.14) (in >=1 displayed pool variant)
- `s5-q016` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 89, ratio 1.11) (in >=1 displayed pool variant)
- `s5-q018` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 92 chars vs longest distractor 89, ratio 1.03) (in >=1 displayed pool variant)
- `s5-q025` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 104 chars vs longest distractor 96, ratio 1.08) (in >=1 displayed pool variant)
- `s5-q026` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 71, ratio 1.14) (in >=1 displayed pool variant)
- `s5-q036` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 75 chars vs longest distractor 72, ratio 1.04) (in >=1 displayed pool variant)
