# Smart Data & AI Radar

A **£0-by-default**, GitHub-ready intelligence tool for discovering, extracting, ranking and analysing developments that matter to the UK Smart Data agenda.

The radar is deliberately not a generic AI-news feed. It uses a **UK Government / Smart Data policy lens**, with:

1. **Primary focus:** the intersection of **Smart Data and AI** — agentic AI, delegated authority, consent, digital identity, APIs and trust frameworks, interoperability, AI governance, data portability and AI-enabled services.
2. **Secondary focus:** **Smart Data** more broadly — policy, regulation, standards, Open Finance, property, energy, transport, retail, telecoms, trade, economic security and international models.

Raidiam is monitored because it publishes relevant specialist material, with an additional relevance signal for Marie Walker. This is **source monitoring, not alignment or opposition**.

## Cost model

The default configuration needs **no paid API keys**:

- discovery: Google News RSS + direct source monitoring;
- extraction: open-source Python libraries;
- first-stage relevance ranking: deterministic local scoring;
- analysis: Ollama running `qwen2.5:1.5b-instruct`;
- storage: SQLite;
- outputs: Markdown, HTML and JSON;
- automation: GitHub Actions.

OpenAI remains an optional backend, not a dependency.

## Weekly and monthly modes

The same intelligence engine has two analytical cadences.

### Weekly mode

```bash
smart-data-radar run --mode weekly
```

Default lookback: **7 days**. Weekly ranking gives more weight to:

- urgency;
- immediate impact and downstream consequences;
- whether an issue needs active monitoring;
- implementation risk;
- near-term policy opportunity.

The purpose is: **what changed, what matters now, and what needs watching next?**

### Monthly mode

```bash
smart-data-radar run --mode monthly
```

Default lookback: **30 days**. Monthly ranking reduces the recency/urgency bias and gives more weight to:

- strategic significance;
- cumulative impact;
- ability to advance or inform Smart Data policy;
- persistent policy gaps;
- structural opportunities and threats;
- signals likely to matter over the next quarter or longer.

The purpose is: **what is actually moving in the system, rather than merely making news?**

You can override the period, for example:

```bash
smart-data-radar run --mode monthly --days 45
```

## Policy-priority ranking

The LLM scores every selected item from **1–5** against ten signals:

| Signal | What it means |
|---|---|
| Urgency | How quickly policy attention may be needed |
| Impact | Likely scale of effect on Smart Data policy or delivery |
| Consequences | Breadth/depth of downstream effects if the development grows |
| Policy advancement | Capacity to advance or materially inform existing Smart Data policy |
| Opportunity | Exploitable policy, implementation or market opportunity |
| Monitoring need | Need for continuing observation because the issue is evolving/uncertain |
| Strategic significance | Importance beyond a single scheme or sector |
| Implementation risk | Delivery, governance, technical or regulatory risk exposed |
| Novelty | Whether this is a genuinely new signal rather than routine commentary |
| Evidence strength | Strength of the evidence contained in the item |

`src/smart_data_radar/prioritise.py` contains the transparent weekly and monthly weights. The overall article rank combines:

- **15%** deterministic relevance score;
- **20%** LLM relevance assessment;
- **65%** cadence-specific policy-priority score.

Evidence strength slightly tempers the priority score so weakly evidenced commentary does not outrank stronger material simply because its claims sound dramatic.

## PESTLE analysis

Every selected article receives a PESTLE assessment **from the UK Government / Smart Data perspective**, not a generic corporate PESTLE.

- **Political:** cross-government priorities, institutional ownership, international/devolution implications where evidenced.
- **Economic:** growth, competition, productivity, investment, consumers/SMEs and economic security.
- **Social:** trust, inclusion, accessibility, consumer behaviour and distributional effects.
- **Technological:** APIs, standards, interoperability, identity, AI capability, security and maturity.
- **Legal:** DUAA/data protection, consumer law, sector regulation, liability, accreditation and consent.
- **Environmental:** only when genuinely relevant. The model is instructed to leave it blank rather than invent a connection.

## SWOT analysis

SWOT is explicitly from the position of the **UK Smart Data programme**:

- **Strength:** existing capability/design that helps Government respond;
- **Weakness:** an internal programme, policy, governance or delivery gap exposed by the development;
- **Opportunity:** an external development Smart Data policy could potentially exploit;
- **Threat:** an external development that may obstruct, fragment or undermine Smart Data objectives.

This prevents the tool from accidentally producing a SWOT of the company that wrote the article.

## Humanised policy writing

The model is instructed to write like a concise UK policy analyst rather than an AI template. Each article begins with:

- **Bottom line** — one or two natural sentences for a senior reader;
- **What happened** — factual summary;
- **Why it matters for Government Smart Data** — policy interpretation;
- **AI / Smart Data connection**;
- **source perspective** — kept separate from the radar's analysis;
- **priority rationale**;
- PESTLE;
- SWOT;
- implications and trade-offs;
- questions to pursue;
- hashtags and confidence.

The prompt explicitly discourages formulaic phrases and does not force a recommendation when the evidence only supports monitoring.

## Intelligence hashtags

An item can receive **more than one** controlled hashtag. Examples:

`#AIxSmartData` `#PolicyGap` `#Opportunity` `#Threat` `#Monitor` `#Urgent` `#Strategic` `#ImplementationRisk` `#RegulatoryChange` `#ConsumerProtection` `#Interoperability` `#DigitalIdentity` `#Consent` `#Competition` `#EconomicSecurity` `#OpenFinance` `#OpenProperty` `#Energy` `#Transport` `#Trade` `#Fraud` `#International` `#TrustFramework` `#DataPortability`

Some tags are deterministic safeguards. For example, a monitoring score of 4–5 automatically adds `#Monitor`, and high urgency adds `#Urgent`. The LLM can add other controlled tags where the evidence supports them.

## Period-level synthesis

After analysing individual items, the radar writes a human-readable synthesis containing:

- ranked priorities;
- emerging patterns;
- AI + Smart Data developments;
- wider Smart Data developments;
- policy gaps;
- opportunities;
- threats;
- tensions to watch;
- a monitoring list;
- neutral questions for policy teams.

Weekly synthesis emphasises immediate movement. Monthly synthesis looks for recurring and structural signals.

## Sources

The initial configuration directly monitors:

- the GOV.UK **Creating a Smart Data economy** collection;
- Raidiam Insights.

Google News RSS supplies broader discovery. The relevance profile also prioritises primary/regulatory material and themes including the National Data Library, digital identity, competition, consumer protection, economic security, fraud, challenge prizes, sandboxes, supply-chain provenance and trusted data.

Edit:

- `config/interest_profile.yml` — topics and search phrases;
- `config/sources.yml` — monitored sources and source/person relevance signals.

## Outputs

Weekly mode creates:

- `output/weekly-latest.md`
- `output/weekly-latest.html`
- `output/weekly-latest.json`

Monthly mode creates:

- `output/monthly-latest.md`
- `output/monthly-latest.html`
- `output/monthly-latest.json`

`radar.db` retains article data and a history of weekly/monthly analyses.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e .
```

Install Ollama, then:

```bash
ollama pull qwen2.5:1.5b-instruct
smart-data-radar run --mode weekly
```

No API key is required.

### Ranking-only test

```bash
smart-data-radar run --mode weekly --no-llm
```

## GitHub automation

`.github/workflows/radar.yml` contains:

- a **weekly run every Monday at 07:10 UTC**;
- a **monthly run on the first day of each month at 07:30 UTC**;
- a manual Run Workflow control allowing either `weekly` or `monthly` mode.

The workflow installs Ollama, pulls the free local model, runs the relevant mode and commits that briefing back to the repository.

## Optional OpenAI backend

Not needed for the free version. If you later choose to use it:

```bash
pip install -e '.[openai]'
export LLM_BACKEND=openai
export OPENAI_API_KEY='...'
export OPENAI_MODEL='...'
smart-data-radar run --mode weekly
```

## Editorial safeguards

The prompt requires the model to:

- distinguish reported facts, source claims, opinion and radar analysis;
- identify commercial/source perspective;
- neither endorse nor oppose Raidiam;
- avoid fabricating corroboration;
- prefer concrete policy, governance and implementation implications over generic innovation language;
- leave irrelevant PESTLE categories blank;
- lower confidence when article extraction is weak;
- surface uncertainty and trade-offs rather than manufacture certainty.

## Tests

```bash
pip install -e '.[dev]'
pytest -q
```

The current test suite covers relevance scoring, deduplication, the structured LLM schema, weekly/monthly priority weighting, hashtag rules and PESTLE/SWOT digest output.
