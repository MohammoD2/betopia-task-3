import streamlit as st
import os
import requests
import json

# ------------------- CONFIG -------------------
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]  # Make sure this is set in your environment
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ------------------- HELPER FUNCTION -------------------
def generate_outreach_email(company_input, persona_input, product_input, tone="Friendly"):
    """
    Generate personalized outreach email using OpenRouter LLM.
    """
    prompt = f"""
You are an expert AI Outreach Generator.

### COMPANY PROFILE:
{company_input}

### PERSONA PROFILE:
{persona_input}

### PRODUCT DESCRIPTION:
{product_input}

### REQUIREMENTS:
- Tone: {tone} (Formal / Friendly / Short / Long)
- Highly personalized email
- Include 1 strong CTA
- Explain why the prospect is a strong match in 3 bullet points
- Return output in JSON format:

JSON FORMAT:
{{
  "email": "<personalized outreach email>",
  "why_this_match_works": ["Reason 1", "Reason 2", "Reason 3"]
}}
"""

    try:
        response = requests.post(
            url=OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            })
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except:
                # fallback if LLM returns non-JSON
                return {"email": content, "why_this_match_works": []}
        else:
            return {"email": f"OpenRouter API error: {response.status_code}", "why_this_match_works": []}
    except Exception as e:
        return {"email": f"Exception occurred: {str(e)}", "why_this_match_works": []}

# ------------------- STREAMLIT UI -------------------
st.set_page_config(page_title="AI Outreach Generator", layout="wide")
st.title("AI Outreach Generator for Betopia Interview Task")

st.write("This app generates a personalized outreach email for Betopia based on the input data.")

# ------------------- COMPANY INPUTS -------------------
with st.expander("Company Profile", expanded=True):
    company_name = st.text_input("Company Name", value="Betopia")
    industry = st.text_input("Industry", value="Tech / HR")
    size = st.text_input("Company Size", value="4.5k employees")
    location = st.text_input("Location", value="Bangladesh")
    website = st.text_input("Website", value="https://betopiagroup.com/")
    pain_points = st.text_area("Pain Points (comma separated)", value="Hiring challenges")
    recent_news = st.text_area("Recent News (optional)", value="Recently expanded HR department")
    tech_stack = st.text_input("Tech Stack (optional)", value="HR software, ATS systems")

company_input = f"""
Company: {company_name}
Industry: {industry}
Size: {size}
Location: {location}
Website: {website}
Pain Points: {pain_points}
Recent News: {recent_news}
Tech Stack: {tech_stack}
"""

# ------------------- PERSONA INPUTS -------------------
with st.expander("Persona Profile", expanded=True):
    persona_name = st.text_input("Persona Name", value="Md. Rajiur Rahman Ayon")
    role = st.text_input("Role", value="HR Manager")
    seniority = st.text_input("Seniority / Level", value="Manager")
    responsibilities = st.text_area("Responsibilities (comma separated)", value="Recruitment, onboarding, employee engagement")
    kpis = st.text_area("KPIs (comma separated)", value="Time-to-hire, Employee retention")
    challenges = st.text_area("Challenges", value="Filling positions quickly, managing applicant pipeline")
    cares_about = st.text_area("What they care about most", value="Faster hiring, quality candidates, reducing manual work")

persona_input = f"""
Name: {persona_name}
Role: {role}
Seniority: {seniority}
Responsibilities: {responsibilities}
KPIs: {kpis}
Challenges: {challenges}
What they care about: {cares_about}
"""

# ------------------- PRODUCT INPUTS -------------------
with st.expander("Product Description", expanded=True):
    product_name = st.text_input("Product Name", value="AI Outreach Generator")
    short_summary = st.text_area("Short Summary", value="AI tool to generate personalized B2B outreach messages")
    core_value_props = st.text_area("Core Value Propositions (comma separated)", value="Hyper-personalization, Multi-tone support, CRM-ready outputs")
    features = st.text_area("Features (comma separated)", value="Automated outreach, Custom prompt templates, LLM-powered personalization")
    target_users = st.text_area("Target Users", value="Sales teams, Marketing, BDRs")
    main_benefits = st.text_area("Main Benefits", value="Saves time, Increases reply rates, Ensures relevant messaging")
    risks_eliminated = st.text_area("Risks it Eliminates", value="Generic emails, Low engagement, Manual copywriting errors")

product_input = f"""
Product: {product_name}
Short Summary: {short_summary}
Core Value Props: {core_value_props}
Features: {features}
Target Users: {target_users}
Main Benefits: {main_benefits}
Risks it Eliminates: {risks_eliminated}
"""

# ------------------- TONE SELECTION -------------------
tone = st.selectbox("Select Tone", ["Formal", "Friendly", "Short", "Long"], index=1)

# ------------------- GENERATE BUTTON -------------------
if st.button("Generate Outreach Email"):
    with st.spinner("Generating email..."):
        result = generate_outreach_email(company_input, persona_input, product_input, tone=tone)

        st.subheader("Generated Outreach Email")
        st.text_area("Email", value=result.get("email", ""), height=200)

        st.subheader("Why This Match Works")
        reasons = result.get("why_this_match_works", [])
        for r in reasons:
            st.write(f"- {r}")
