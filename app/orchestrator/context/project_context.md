# YahyaTel Persistent Project Context

YahyaTel is an imaginary Oman-based telecom analytics platform inspired by Omantel.

Project type:
- FYP demo
- not production software
- 2 week deadline
- foundation over polish

Main feature:
- B2B churn prediction workflow

Workflow:
Customer data
→ XGBoost churn prediction
→ risk explanation
→ retention strategy
→ chatbot explanation (English/Arabic)

Secondary feature:
- B2C fake ISP storefront
- fake package purchase popup
- optional fake order save

Frontend:
- React
- Vite
- TypeScript
- Tailwind CSS

Backend:
- FastAPI
- Python

Database:
- PostgreSQL

Authentication:
- JWT
- bcrypt password hashing
- role-based access

Roles:
- Admin
- Customer Agent
- Customer

Chatbot:
- restricted YahyaTel support chatbot
- explains churn results and retention strategies
- not general AI assistant
- not orchestration brain

Current implementation decisions:
- The GitHub churn FastAPI project still needs to be downloaded/setup.
- Dataset is not real customer data. Use existing/public telecom churn data for the demo.
- PostgreSQL is the preferred database unless Version 1 requires Supabase.
- Chatbot should use Groq/Llama through an environment variable.
- Do not hardcode API keys.
- Chatbot is required, but it is only an explanation/support layer.
- Chatbot should explain churn predictions, risk factors, and retention strategies in English/Arabic.

ML:
- XGBoost
- telecom churn prediction
- reusable GitHub telecom churn FastAPI project
- configurable JSON retention engine

Not included:
- real billing
- payment gateway
- telecom infrastructure
- enterprise scaling
- production hardening

# Approved Rebuild Scope

Status: APPROVED

Must-have:
- JWT authentication
- bcrypt password hashing
- role-based access: Admin, Customer Agent, Customer
- B2B churn prediction flow
- XGBoost prediction using reused GitHub/FYP model work
- risk explanation
- configurable JSON retention strategy engine
- Groq/Llama chatbot explanation layer
- English/Arabic support
- B2C fake ISP storefront
- fake package purchase popup
- PostgreSQL preferred database
- demo documentation

Should-have:
- basic Tailwind polish
- responsive layout
- fake order save if easy
- Docker only if easy

Cut-if-needed:
- CI/CD
- real billing
- payment gateway
- Safari-specific testing
- enterprise scalability
- advanced analytics
- production hardening

Important:
- Supabase is not the default fallback.
- Use PostgreSQL unless Version 1 already strongly depends on Supabase.
