# AI Outreach Generator — Task 3 Deliverable

An end-to-end prompt-driven workflow that creates hyper-personalized sales outreach emails for Betopia’s **Task 3 — “AI Outreach Generator”** challenge. The system gathers structured company, persona, and product data, feeds it into a carefully engineered prompt, and renders consistent outputs with justification bullets and tone control.

---

## Folder Guide

| Path | Description |
| --- | --- |
| `App.py` | Streamlit UI that lets non-technical users enter profiles, pick a tone (Formal/Friendly/Short/Long), and trigger the LLM call. It also renders the outreach email plus the “Why this match works” bullets. |
| `AI Outreach Generator.py` | Reusable Python module + CLI example that encapsulates the `OutreachGenerator` class. Shows the prompt template, OpenRouter request, and JSON parsing logic for automation scripts or notebooks. |
| `test.py` | Simple connectivity smoke test to verify the OpenRouter API key and model before running the main app. |
| `requirements.txt` | Locked Python dependencies for both the CLI module and Streamlit app. |
| `venv/` | Local virtual environment (not required if you prefer your own). |

---

## Prompt Template (Deliverable #1)

The shared template (see `OutreachGenerator.build_prompt`) enforces:
```
You are an expert AI Outreach Generator.

### COMPANY PROFILE:
{company}

### PERSONA PROFILE:
{persona}

### PRODUCT DESCRIPTION:
{product}

### REQUIREMENTS:
- Tone: {tone} (Formal / Friendly / Short / Long)
- Highly personalized email
- Include 1 strong CTA
- Explain why the prospect is a strong match in 3 bullet points
- Return output clearly separated into EMAIL + REASONS sections (Streamlit) or JSON (CLI).
```
This structure keeps hallucinations low by constraining the model and forcing direct reuse of supplied facts.

---

## Code Calling the LLM (Deliverable #2)

- **Streamlit (`App.py`)** builds the prompt from UI inputs, calls OpenRouter via `requests.post`, and then parses the SECTION-based response for display.
- **CLI module (`AI Outreach Generator.py`)** exposes the `OutreachGenerator` class with a `generate_outreach()` method used by scripts or tests. It expects an `OPENROUTER_API_KEY` and defaults to `meta-llama/llama-3.3-70b-instruct:free`.

Both paths rely on the same prompt philosophy, ensuring consistent reasoning no matter the interface.

---

## Example Output (Deliverable #3)

Sample generated email for the default Betopia inputs (tone: Friendly):

```
EMAIL:
Hi Rajiur,

Loved seeing Betopia scale its HR footprint in Bangladesh. With 4.5k teammates and hiring still accelerating, keeping talent funnels warm without exhausting your HR ops team is an enormous lift. Our AI Outreach Generator plugs into your ATS to auto-draft outreach that mirrors your brand voice, highlights recent wins like the HR expansion, and surfaces top-fit candidates before competitors even notice them.

If you’d like, I can share a live workspace showing how your KPIs (time-to-hire and retention) improve within a single sprint. Are you free for a quick 20‑minute session next Tuesday?

Best,
<Rep Name>

REASONS:
- References Betopia’s latest HR expansion to prove research.
- Speaks directly to Rajiur’s KPIs (time-to-hire, retention).
- CTA ties demo value to the hiring-speed pain point.
```

Feel free to swap tone to `Formal`, `Short`, or `Long`; the email phrasing and CTA adjust accordingly while the justification bullets stay grounded in the supplied data.

---

## Discussion — Why This Personalization Works (Deliverable #4)

1. **Grounded context only:** Every sentence is built from the explicit company/persona/product fields, so hallucinations are minimized and compliance teams can audit the inputs.
2. **Tone-aware messaging:** The prompt injects the requested tone into the instructions, keeping brand alignment whether executives expect concise notes or relationship-driven copy.
3. **Bidirectional value framing:** The CTA connects Betopia’s KPIs (time-to-hire, retention) with the product’s value props (hyper-personalization, CRM-ready outputs), which increases reply odds versus generic pitches.
4. **Reason bullets for SDR coaching:** The “Why this match works” list doubles as a QA checklist—sales leaders can inspect whether each email actually references pain points, tech stack, and desired outcomes.

---

## Running the Project

1. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
2. **Provide credentials**
   - CLI/tests: set `OPENROUTER_API_KEY` in a `.env`.
   - Streamlit: add the key to `.streamlit/secrets.toml` as `OPENROUTER_API_KEY="..."`.
3. **Launch Streamlit UI**
   ```
   streamlit run App.py
   ```
4. **CLI example**
   ```
   python "AI Outreach Generator.py"
   ```
5. **Connectivity smoke test**
   ```
   python test.py
   ```

---

## Matching the Task 3 Checklist

- ✅ Prompt template documented with reasoning guardrails.
- ✅ Production-ready code paths: interactive Streamlit UI plus reusable Python module.
- ✅ Example outreach output showing both email and justification bullets.
- ✅ Discussion section explaining the personalization strategy and why it resonates.
- ✅ Tone toggles, anti-hallucination constraints, and match rationales implemented in code.

You now have a clear README and a working system to demo AI-driven outreach personalization. Customize the inputs, tweak tones, and extend the prompt for any future sales playbooks.

