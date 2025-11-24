import streamlit as st
from outreach_generator import OutreachGenerator  # import your backend
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ------------------- CONFIG -------------------
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
generator = OutreachGenerator(api_key=OPENROUTER_API_KEY)

# ------------------- STREAMLIT APP -------------------
st.set_page_config(page_title="AI Outreach Generator", layout="wide")
st.title("AI Outreach Generator")

st.write("Fill all fields below to generate a personalized outreach email.")

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
tone = st.selectbox("Select Tone", ["Formal", "Friendly", "Short", "Long"], index=1)  # Default = Friendly

# ------------------- GENERATE BUTTON -------------------
if st.button("Generate Outreach Email"):
    with st.spinner("Generating email..."):
        try:
            result = generator.generate_outreach(company_input, persona_input, product_input, tone=tone)

            st.subheader("Generated Outreach Email")
            st.text_area("Email", value=result.get("email", ""), height=200)

            st.subheader("Why This Match Works")
            reasons = result.get("why_this_match_works", [])
            for r in reasons:
                st.write(f"- {r}")

        except Exception as e:
            st.error(f"Error generating email: {e}")