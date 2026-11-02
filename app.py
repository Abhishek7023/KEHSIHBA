"""
VenturePath AI - Platform for Young Entrepreneurs and First-Time Founders
Backend API and Web Server powered by Flask and SQLite
"""

import os
import json
import sqlite3
import datetime
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venturepath.db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# ---------------------------------------------------------
# DATABASE INITIALIZATION & HELPERS
# ---------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Active workspace state
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workspace_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            selected_business TEXT,
            skills TEXT,
            budget REAL DEFAULT 10000,
            mode TEXT DEFAULT 'all',
            time_commitment TEXT DEFAULT 'part-time',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Roadmap completed items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_items (
            business_name TEXT,
            step_index INTEGER,
            is_completed INTEGER DEFAULT 0,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (business_name, step_index)
        )
    """)
    
    # Budget plans
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget_plans (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            starting_capital REAL DEFAULT 20000,
            equipment_cost REAL DEFAULT 4000,
            marketing_cost REAL DEFAULT 3000,
            registration_cost REAL DEFAULT 1500,
            inventory_cost REAL DEFAULT 2500,
            monthly_expenses REAL DEFAULT 3500,
            selling_price REAL DEFAULT 1200,
            expected_sales INTEGER DEFAULT 15,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Customer outreach tracker
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outreach_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_name TEXT NOT NULL,
            channel TEXT DEFAULT 'WhatsApp',
            status TEXT DEFAULT 'Identified',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Validation history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idea_title TEXT NOT NULL,
            target_market TEXT,
            score INTEGER,
            verdict TEXT,
            data_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Ensure default workspace row exists
    cursor.execute("INSERT OR IGNORE INTO workspace_state (id, selected_business, skills, budget, mode) VALUES (1, 'Social Media Management', '[\"marketing\", \"design\"]', 10000, 'online')")
    cursor.execute("INSERT OR IGNORE INTO budget_plans (id) VALUES (1)")
    
    # Seed default sample leads if table empty
    cursor.execute("SELECT COUNT(*) as cnt FROM outreach_leads")
    if cursor.fetchone()["cnt"] == 0:
        cursor.execute("INSERT INTO outreach_leads (lead_name, channel, status, notes) VALUES ('Brew & Bean Cafe (Bandra)', 'WhatsApp', 'Contacted', 'Sent tailored 3-post demo pack')")
        cursor.execute("INSERT INTO outreach_leads (lead_name, channel, status, notes) VALUES ('Urban Glow Salon', 'Instagram DM', 'Replied', 'Meeting requested for Thursday 4 PM')")
        cursor.execute("INSERT INTO outreach_leads (lead_name, channel, status, notes) VALUES ('FitPulse Gym Academy', 'Email', 'Identified', 'Needs reels for summer student discount')")
    
    conn.commit()
    conn.close()

# Initialize DB on module load
init_db()

# ---------------------------------------------------------
# COMPREHENSIVE BUSINESS CATALOG
# ---------------------------------------------------------
BUSINESSES = [
    {
        "id": "smm-agency",
        "name": "Social Media Management & Reels Agency",
        "tagline": "Turn local shops and brands into local viral sensations",
        "skills": ["marketing", "design", "communication", "editing", "social media"],
        "interests": ["creative", "tech", "services"],
        "budget": 3000,
        "mode": "online",
        "time": "part-time",
        "difficulty": "Beginner Friendly",
        "revenue_model": "Monthly Retainer (₹6,000 – ₹20,000 / client / month)",
        "description": "Manage content calendars, create Instagram Reels, design carousel posts, and drive footfall and inquiries for local cafes, salons, fitness studios, and boutique brands.",
        "clients": ["Independent Cafes & Bakeries", "Hair & Skin Salons", "Fitness Studios & Trainers", "Local Boutiques", "Coaching Institutes"],
        "capex_breakdown": {
            "Canva Pro / CapCut Pro": 1000,
            "Portfolio Domain & Setup": 1000,
            "Sample Ad Credit": 1000
        },
        "first_steps": [
            "Pick 1 specific niche (e.g., student-friendly cafes or yoga teachers).",
            "Produce 3 spec Reels and 3 carousel posts showing before-and-after improvements.",
            "Offer a 7-day free trial or 50% first-month launch discount to 2 local owners.",
            "Record performance metrics and convert them to your first paid retainers."
        ],
        "roadmap_stages": [
            {"title": "Idea & Niche Discovery", "tasks": ["Select niche market (e.g. hospitality, wellness, retail)", "Audit 10 local business Instagram profiles", "Define your unique service package"]},
            {"title": "Market & Pricing Research", "tasks": ["Survey local business pricing expectations", "Set 3 tier packages (Starter ₹5k, Growth ₹12k, Pro ₹20k)", "Identify active local trade groups"]},
            {"title": "Validation & Portfolio", "tasks": ["Build 5 high-converting specimen designs", "Record 3 sample viral hooks tailored to your target niche", "Collect first qualitative feedback from 3 peers"]},
            {"title": "Competitor & Gap Analysis", "tasks": ["Examine 4 competing freelance creators", "Find underserved gaps (e.g. quick turnaround, regional language copy)", "Formulate your unfair advantage"]},
            {"title": "Business Model & Deliverables", "tasks": ["Draft standardized monthly scope document", "Set revision boundaries (max 2 revisions per post)", "Select payment terms (50% upfront, 50% milestone)"]},
            {"title": "Budget & Software Setup", "tasks": ["Setup free or low-cost scheduling tools", "Prepare invoicing template with UPI/bank details", "Calculate break-even client count (2 clients = profitable)"]},
            {"title": "MVP Offer Launch", "tasks": ["Create a clean Notion or Carrd one-page portfolio", "Write your personalized founder intro script", "Secure first trial client from personal network"]},
            {"title": "First 10 Customers Acquisition", "tasks": ["Walk into 15 neighborhood businesses with tailor-made sample reels", "Send 25 personalized WhatsApp & Instagram DMs", "Secure 3 signed monthly retainers"]},
            {"title": "Delivery & Testimonial Capture", "tasks": ["Deliver week 1 content 24 hours ahead of deadline", "Generate first month report with follower and reach metrics", "Request a video/WhatsApp review snippet"]},
            {"title": "Growth & Sub-Contracting", "tasks": ["Hire junior student editor for video cut-downs", "Upsell existing clients on Meta Ad management", "Standardize client onboarding workflow"]}
        ]
    },
    {
        "id": "web-dev",
        "name": "Web Development & Landing Pages",
        "tagline": "Modern responsive digital storefronts for growing businesses",
        "skills": ["coding", "technology", "web development", "design"],
        "interests": ["tech", "services"],
        "budget": 4500,
        "mode": "online",
        "time": "part-time",
        "difficulty": "Intermediate",
        "revenue_model": "Fixed Project Fee (₹8,000 – ₹35,000 / site) + Annual Maintenance (₹3,000/yr)",
        "description": "Design and build fast, responsive websites, landing pages, and appointment booking systems for professionals, clinics, educational classes, and local retail stores.",
        "clients": ["Doctors & Health Clinics", "Coaching Classes & Tutors", "Architects & Interior Designers", "Event Planners", "Local Manufacturers"],
        "capex_breakdown": {
            "Domain & Cloud Hosting": 2500,
            "Template Assets / Icons": 1000,
            "Proposal Software & Invoicing": 1000
        },
        "first_steps": [
            "Build 2 live demo sites (e.g., a dental clinic landing page and a boutique portfolio).",
            "Prepare a 48-hour turnaround promise guarantee.",
            "Reach out to businesses whose Google Maps listing has no website.",
            "Pitch a low-friction ₹6,999 launch package."
        ],
        "roadmap_stages": [
            {"title": "Tech Stack & Blueprint", "tasks": ["Select high-velocity stack (HTML/Tailwind/Flask or React)", "Set up reusable starter boilerplates", "Benchmark 10 high-ranking local business sites"]},
            {"title": "Market Scoping", "tasks": ["List 50 businesses on Google Maps without websites", "Categorize by average transaction value", "Estimate willingness to pay in your city"]},
            {"title": "Validation & Demos", "tasks": ["Build demo dental clinic landing page", "Build demo tuition center portal", "Host both live with custom subdomains"]},
            {"title": "Competitor Benchmark", "tasks": ["Analyze typical agency turnaround time (usually 3–4 weeks)", "Price yourself 40% lower with 3-day delivery guarantee", "Highlight direct WhatsApp chat widget integration"]},
            {"title": "Commercial Architecture", "tasks": ["Create a 1-page plain English service contract", "Set milestones: 40% advance, 40% preview, 20% go-live", "Include 30 days free bug-fix warranty"]},
            {"title": "Tooling Budget", "tasks": ["Host on low-cost reliable VPS or Netlify/Vercel", "Setup professional domain email", "Establish client staging environment"]},
            {"title": "MVP Launch", "tasks": ["Launch your own portfolio showcasing the 2 demo sites", "Add live WhatsApp click-to-chat CTA", "Publish case study on LinkedIn and Twitter/X"]},
            {"title": "Direct Outreach", "tasks": ["Visit 10 local businesses with their live mockups on an iPad/phone", "Cold email 20 coaching institutes with speed audit reports", "Close your first 2 paying clients"]},
            {"title": "Client Handover & Praise", "tasks": ["Conduct a 15-minute video walkthrough showing how to edit content", "Deliver Google Analytics setup", "Collect 5-star Google Review and testimonial quote"]},
            {"title": "Recurring Revenue Model", "tasks": ["Offer ₹500/month hosting & maintenance retainers", "Add SEO add-ons and Google Business Profile optimization", "Establish referral fee (10% kickback for client referrals)"]}
        ]
    },
    {
        "id": "video-editing",
        "name": "Short-Form Video & Podcast Editing",
        "tagline": "Turn long videos and podcasts into high-engagement Reels and Shorts",
        "skills": ["editing", "creativity", "video", "design"],
        "interests": ["creative", "tech"],
        "budget": 2500,
        "mode": "online",
        "time": "part-time",
        "difficulty": "Beginner Friendly",
        "revenue_model": "Per Video (₹600 – ₹1,500 / Reel) or Monthly Bundle (₹12,000 / 15 videos)",
        "description": "Produce engaging, retention-optimized short-form videos with captions, sound effects, b-roll cuts, and eye-catching hooks for podcasters, founders, influencers, and fitness coaches.",
        "clients": ["YouTubers & Podcasters", "Personal Brand Founders", "Fitness & Diet Coaches", "Real Estate Agents", "Motivational Speakers"],
        "capex_breakdown": {
            "Audio & SFX Library License": 1000,
            "Cloud Storage (Google Drive / DropBox)": 800,
            "Font & Motion Preset Bundles": 700
        },
        "first_steps": [
            "Download an interview or podcast of a popular creator.",
            "Cut 2 high-energy 45-second clips with captions, zooms, and sound design.",
            "Tag them on X/Instagram and DM the link to the creator.",
            "Offer 1 free sample edit to prove your turnaround speed."
        ],
        "roadmap_stages": [
            {"title": "Hook & Style Curation", "tasks": ["Study Alex Hormozi and Ali Abdaal short-form editing styles", "Master dynamic captions and motion tracking", "Assemble sound effects toolkit"]},
            {"title": "Target Audience Scouting", "tasks": ["Identify 30 Indian creators with 10k–100k subscribers", "Analyze their current shorts engagement", "Note specific pacing and audio flaws to solve"]},
            {"title": "Spec Work Validation", "tasks": ["Edit 3 sample shorts from publicly available podcast clips", "Upload to Google Drive with clean presentation", "Solicit feedback from creator subreddits"]},
            {"title": "Value Proposition", "tasks": ["Define promise: '24-hour turnaround, zero hassle, first revision free'", "Structure pack of 12 reels/month", "Prepare contract covering raw file retention"]},
            {"title": "Workflow Systems", "tasks": ["Create Google Drive client drop folders", "Standardize file naming conventions", "Build reusable Premiere / DaVinci / CapCut project presets"]},
            {"title": "Finances & Cashflow", "tasks": ["Calculate cost per editing hour", "Set payment gateway with instant settlement", "Aim for 3 ongoing creator accounts"]},
            {"title": "Founder Outreach", "tasks": ["Send 5 custom-edited sample videos to target podcasters per day", "Write respectful, value-first direct messages", "Include drive preview link (no attachments)"]},
            {"title": "First 3 Client Closures", "tasks": ["Convert trial samples into paid monthly package", "Deliver first batch with 3 variations of hooks", "Achieve 90%+ on-time delivery metric"]},
            {"title": "Client Success & Upsell", "tasks": ["Proactively suggest 3 video topic ideas to each client", "Offer YouTube thumbnail design as complimentary add-on", "Request quote for your website portfolio"]},
            {"title": "Agency Scaling", "tasks": ["Partner with a freelance scriptwriter", "Create automated intake form for footage", "Scale to 5 retained creator accounts"]}
        ]
    },
    {
        "id": "graphic-design",
        "name": "Brand Identity & Graphic Design",
        "tagline": "Logos, brand guidelines, and visual assets that convert",
        "skills": ["design", "art", "creativity", "communication"],
        "interests": ["creative", "services"],
        "budget": 2000,
        "mode": "online",
        "time": "part-time",
        "difficulty": "Beginner Friendly",
        "revenue_model": "Brand Identity Package (₹5,000 – ₹25,000) or Social Media Assets (₹4,000/mo)",
        "description": "Craft cohesive visual branding, modern logos, packaging design, marketing banners, and pitch decks for early-stage startups and modern consumer brands.",
        "clients": ["New Startups & Incubators", "D2C Food & Fashion Brands", "College Event Fests", "Local Restaurants & Cafes", "Corporate Freelancers"],
        "capex_breakdown": {
            "Design Tool Subscriptions": 1000,
            "Stock Assets / Fonts": 600,
            "Behance & Portfolio Presence": 400
        },
        "first_steps": [
            "Create 3 fictional brand redesigns for known local brands.",
            "Publish rich case studies on Behance and LinkedIn.",
            "Join early startup communities (e.g. Indie Hackers, eChai, college E-cells).",
            "Offer branding packages to campus startups."
        ],
        "roadmap_stages": [
            {"title": "Aesthetic Mastery", "tasks": ["Establish deep knowledge of typography and color psychology", "Curate a personal brand moodboard", "Set up Figma and Illustrator workspaces"]},
            {"title": "Niche Positioning", "tasks": ["Choose focus (e.g. coffee brands, tech SaaS, personal branding)", "Map price elasticity of early founders", "Draft tiered branding scope"]},
            {"title": "Spec Portfolio Build", "tasks": ["Design full visual identity for 2 fictional startups", "Include logo, typography scale, color palette, and business cards", "Publish to Behance with high-res mockups"]},
            {"title": "Competitor Breakdown", "tasks": ["Review 5 top freelance designers on Dribbble", "Identify slow communication weaknesses to outshine", "Formulate clear revision policy"]},
            {"title": "Pricing & Licensing", "tasks": ["Define commercial asset transfer rights", "Establish standard 50% deposit policy", "Draft simple 1-page copyright transfer agreement"]},
            {"title": "Budget Management", "tasks": ["Maintain zero unneeded overhead", "Organize vector asset library", "Create standard invoice templates"]},
            {"title": "Outreach & Inbound", "tasks": ["Share design breakdowns and before-afters on LinkedIn", "Reach out to 15 newly registered companies on MCA portal", "Engage with college incubator teams"]},
            {"title": "Client Delivery", "tasks": ["Present concepts inside real-world 3D mockups", "Provide logo files in PNG, SVG, PDF, and EPS formats", "Provide brand color guidelines sheet"]},
            {"title": "Referrals & Testimonials", "tasks": ["Deliver final zip bundle with personal thank you video", "Ask for introduction to 1 fellow founder", "Publish client case study"]},
            {"title": "Expansion into UI/UX", "tasks": ["Learn mobile and web UI prototyping in Figma", "Upsell existing clients on website design", "Increase baseline package price by 30%"]}
        ]
    },
    {
        "id": "online-tutoring",
        "name": "STEM & Coding Micro-Tutoring",
        "tagline": "High-impact 1-on-1 and small batch practical tutoring",
        "skills": ["teaching", "communication", "coding", "academics"],
        "interests": ["education", "services", "tech"],
        "budget": 1500,
        "mode": "online",
        "time": "part-time",
        "difficulty": "Beginner Friendly",
        "revenue_model": "Monthly per student (₹2,500 – ₹6,000 / month / student)",
        "description": "Provide personalized coding, mathematics, or computer science practical tutoring for high school students, engineering juniors, and career-switchers.",
        "clients": ["Junior College Students", "First-Year CS/IT Undergrads", "Parents seeking Coding Mentors", "Working Professionals learning Python/SQL"],
        "capex_breakdown": {
            "Digital Stylus / Pen Tablet": 1000,
            "Zoom / Google Meet & Materials": 500
        },
        "first_steps": [
            "Identify 2 high-demand subjects (e.g., Python Basics, Data Structures, or 12th Maths).",
            "Prepare a 4-week structured practical syllabus.",
            "Offer a free 45-minute demo class to test teaching style.",
            "Share demo announcements in college groups and neighborhood WhatsApp circles."
        ],
        "roadmap_stages": [
            {"title": "Curriculum Design", "tasks": ["Draft week-by-week outcome oriented lesson plan", "Prepare 15 practical code challenges and quizzes", "Select student level and prerequisites"]},
            {"title": "Audience Validation", "tasks": ["Talk to 10 junior students about exam and coding pain points", "Determine peak exam/semester months", "Set affordable batch pricing"]},
            {"title": "Demo Class Prep", "tasks": ["Create visually clean slides and interactive live demo", "Record a 3-minute sample explanation video", "Test mic and screen-sharing setup"]},
            {"title": "Channel Research", "tasks": ["Locate local parent groups and student WhatsApp boards", "Post educational tips and solved problems", "Engage in college technical club discussions"]},
            {"title": "Batch Structure", "tasks": ["Cap batch size to maximum 6 students for high engagement", "Set 3 classes/week schedule with recorded sessions", "Establish attendance and homework tracking"]},
            {"title": "Platform Setup", "tasks": ["Organize Google Classroom for notes and assignments", "Integrate UPI QR code for fee collection", "Maintain student progress sheets"]},
            {"title": "Launch First Cohort", "tasks": ["Host free weekend workshop 'Master Python in 2 Hours'", "Pitch paid 4-week cohort at the end of workshop", "Enroll first 5 paying students"]},
            {"title": "Student Transformation", "tasks": ["Conduct weekly 1-on-1 doubt clearing slots", "Help students build 1 portfolio project", "Send weekly progress updates to parents"]},
            {"title": "Testimonials & Proof", "tasks": ["Collect student grade improvements and reviews", "Publish project screenshots with student permission", "Offer 15% discount for next semester enrollments"]},
            {"title": "Self-Paced Course Scale", "tasks": ["Record high-performing lectures into video course", "Launch cohort 2 with student teaching assistants", "Expand into specialized interview prep"]}
        ]
    },
    {
        "id": "handmade-merch",
        "name": "Artisanal D2C & Campus Merch Brand",
        "tagline": "Custom designed apparel, accessories, and curated aesthetic goods",
        "skills": ["craft", "art", "creativity", "marketing"],
        "interests": ["creative", "ecommerce", "products"],
        "budget": 6000,
        "mode": "hybrid",
        "time": "part-time",
        "difficulty": "Intermediate",
        "revenue_model": "Product Margins (50% – 70% Gross Margin per unit)",
        "description": "Design and manufacture custom university hoodies, aesthetic tote bags, enamel pins, artisanal resin decor, or customized stationery for students and aesthetic enthusiasts.",
        "clients": ["College Students & Clubs", "Gift Shoppers", "Fest Organizers", "Pop-up Flea Markets", "Instagram Aesthetic Shoppers"],
        "capex_breakdown": {
            "Initial Raw Material / Blank Samples": 3500,
            "Packaging & Brand Stickers": 1500,
            "Sample Photography & Shipping": 1000
        },
        "first_steps": [
            "Select 1 flagship product (e.g. embroidered college oversized hoodies or customized keychains).",
            "Order 5 trial pieces to inspect quality and fabric weight.",
            "Run a pre-order campaign with mockups before full manufacturing.",
            "Set up an Instagram storefront with UPI payment link."
        ],
        "roadmap_stages": [
            {"title": "Product Concept", "tasks": ["Survey 50 campus students on preferred designs", "Determine price ceiling (e.g. ₹699 for tote, ₹1,299 for hoodie)", "Pick unique aesthetic theme"]},
            {"title": "Vendor & Sourcing", "tasks": ["Source 3 wholesale manufacturers or fabric printers", "Order material swatches and inspect stitch quality", "Negotiate low Minimum Order Quantity (MOQ of 10-20 pcs)"]},
            {"title": "Sampling & Validation", "tasks": ["Produce 3 prototype finished units", "Conduct wear and wash durability test", "Photograph prototypes on campus with friends"]},
            {"title": "Competitor Analysis", "tasks": ["Compare delivery times and pricing of popular Instagram pages", "Include premium unboxing card with handwritten note", "Ensure 60%+ contribution margin"]},
            {"title": "Unit Economics", "tasks": ["Calculate exact Cost of Goods Sold (COGS)", "Factor packaging, courier, and payment fees", "Set break-even sales volume"]},
            {"title": "Storefront Setup", "tasks": ["Create Instagram page and WhatsApp catalog", "Setup payment via UPI or Razorpay link", "Design aesthetic shipping labels"]},
            {"title": "Pre-Order Launch", "tasks": ["Announce limited first drop (only 30 pieces)", "Offer early bird perk for first 10 orders", "Collect 100% advance payment on pre-orders"]},
            {"title": "Campus Distribution", "tasks": ["Deliver orders in person on campus to generate word of mouth", "Host a pop-up stall during college festival", "Encourage unboxing story tags with giveaway incentive"]},
            {"title": "Review Collection", "tasks": ["Repost customer stories to Instagram highlights", "Gather feedback on sizing and durability", "Refine design based on top requests"]},
            {"title": "Drop 2 Expansion", "tasks": ["Reinvest profits into larger batch size (50-100 units)", "Collaborate with college student ambassadors", "Introduce seasonal limited editions"]}
        ]
    },
    {
        "id": "ai-content-workflow",
        "name": "AI Automation & Workflow Consulting",
        "tagline": "Automate repetitive business workflows with modern AI & Zapier/Make",
        "skills": ["coding", "technology", "marketing", "communication"],
        "interests": ["tech", "services"],
        "budget": 3500,
        "mode": "online",
        "time": "part-time",
        "difficulty": "Intermediate",
        "revenue_model": "Setup Fee (₹10,000 – ₹30,000) + Monthly Maintenance Retainer",
        "description": "Help real estate brokers, recruitment consultants, and e-commerce stores integrate automated customer WhatsApp replies, lead qualification bots, and automated CRM pipelines.",
        "clients": ["Real Estate Brokers", "Recruitment Consultancies", "E-commerce Brands", "Event Organizers", "Accounting Firms"],
        "capex_breakdown": {
            "Make.com / OpenAI API credits": 1500,
            "Domain & Demo Bot Hosting": 1200,
            "Demo WhatsApp Business Account": 800
        },
        "first_steps": [
            "Build 1 working WhatsApp auto-responder bot that books appointments into Google Calendar.",
            "Record a 2-minute Loom/video showing the bot answering questions instantly.",
            "Send the demo to 10 busy local brokers.",
            "Offer a 'pay only if satisfied' pilot implementation."
        ],
        "roadmap_stages": [
            {"title": "Core Automation Skill", "tasks": ["Master Make.com, Zapier, and WhatsApp Cloud API / Twilio", "Build template for lead capture into Google Sheets and CRM", "Test webhook triggers and error handling"]},
            {"title": "Niche Discovery", "tasks": ["Select high-lead-volume industry (e.g. property brokers)", "Map their manual repetitive tasks (e.g. typing property details 50x a day)", "Quantify hours saved (approx 15 hrs/week)"]},
            {"title": "Functional Prototype", "tasks": ["Build live demo bot for property inquiries", "Create interactive booking demo link", "Document setup instructions"]},
            {"title": "Value Pitching", "tasks": ["Position as 'Never lose a midnight buyer lead again'", "Structure pricing: ₹12k setup + ₹3k/month upkeep", "Draft simple Service Level Agreement"]},
            {"title": "Security & Privacy", "tasks": ["Ensure compliance with WhatsApp business policies", "Safeguard customer lead databases", "Setup automated alert if any webhook fails"]},
            {"title": "Budget Management", "tasks": ["Optimize API token consumption to keep running cost under ₹500/mo", "Charge client software subscriptions directly", "Track profitability per integration"]},
            {"title": "Direct Demos", "tasks": ["Reach out to 20 local brokers on WhatsApp with a 1-click test link", "Ask them to message the test bot with 'Looking for 2BHK'", "Showcase instant qualification response"]},
            {"title": "First 2 Client Deployments", "tasks": ["Deploy automation to live client phone number within 48 hours", "Train client's team on reading the Google Sheet dashboard", "Collect upfront setup payment"]},
            {"title": "Proof of ROI", "tasks": ["Measure response time drop from 4 hours to 10 seconds", "Capture client voice note expressing satisfaction", "Package into a 1-page case study"]},
            {"title": "Productized Service", "tasks": ["Package the workflow into a plug-and-play solution", "Offer to 50 more brokers in neighboring districts", "Introduce AI voice agent extensions"]}
        ]
    },
    {
        "id": "event-photo-reels",
        "name": "Event Media & Instant Social Coverage",
        "tagline": "Same-day photo & video highlights for college fests, corporate events & parties",
        "skills": ["editing", "video", "communication", "marketing"],
        "interests": ["creative", "services"],
        "budget": 5000,
        "mode": "offline",
        "time": "weekend",
        "difficulty": "Beginner Friendly",
        "revenue_model": "Per Event Day (₹5,000 – ₹18,000 / day)",
        "description": "Provide rapid-turnaround photography and same-evening edited vertical Reels for college festivals, corporate conferences, birthdays, and sports tournaments.",
        "clients": ["College Student Councils", "Corporate HR & Offsite Teams", "Sports Academies & Marathons", "Wedding/Birthday Families", "Nightclubs & Venues"],
        "capex_breakdown": {
            "Phone Gimbal / Portable LED Light": 3000,
            "Fast Memory Cards & Cloud Drive": 1200,
            "Promotional Badges & Marketing": 800
        },
        "first_steps": [
            "Offer to shoot the next college departmental fest for free in exchange for credit.",
            "Deliver a high-energy recap reel before midnight of the same day.",
            "Share the reel with fest heads and college official handles.",
            "Use the footage as your primary event portfolio."
        ],
        "roadmap_stages": [
            {"title": "Equipment Optimization", "tasks": ["Calibrate smartphone 4K 60fps cinematic settings", "Invest in portable wireless mic and pocket light", "Test rapid footage transfer to laptop/phone"]},
            {"title": "Event Market Mapping", "tasks": ["List upcoming college fests and local cultural events", "Identify private party organizers in your city", "Determine typical event photographer lag (often 2–3 weeks)"]},
            {"title": "Same-Day Delivery Offer", "tasks": ["Define USP: 'Highlights delivered within 4 hours of event finish'", "Prepare pre-licensed upbeat soundtrack library", "Build quick mobile editing workflow"]},
            {"title": "Pricing & Packaging", "tasks": ["Package 1: Half-day coverage + 1 Reel + 40 edited photos (₹6,000)", "Package 2: Full-day + 3 Reels + Raw footage drop (₹12,000)", "Require 50% non-refundable date booking advance"]},
            {"title": "Event Agreement", "tasks": ["Draft terms covering equipment safety, meals, and delivery hours", "Specify copyright and promotional use rights", "Include cancellation guidelines"]},
            {"title": "Budget Tracking", "tasks": ["Allocate travel and local transit costs into quotes", "Budget for cloud storage backup", "Maintain 70%+ gross margin per event"]},
            {"title": "Portfolio Creation", "tasks": ["Cover 1 high-visibility campus or community event", "Post reel with event hashtags and organizers tagged", "Distribute business cards to attendees"]},
            {"title": "Event Outreach", "tasks": ["Pitch to 10 college fest committees with your same-day reel", "Contact 5 corporate event planners on LinkedIn", "Secure first paid booking"]},
            {"title": "Flawless Execution", "tasks": ["Arrive 45 minutes early for venue lighting check", "Capture candid attendee reactions and key moments", "Deliver 60-second highlight reel before midnight"]},
            {"title": "Retainer Partnerships", "tasks": ["Become official media partner for recurring annual fests", "Partner with event decorators and DJs for mutual referrals", "Train a second shooter to cover parallel dates"]}
        ]
    }
]

# ---------------------------------------------------------
# GEMINI AI VALIDATION & FALLBACK HEURISTICS
# ---------------------------------------------------------
def call_gemini_api(prompt):
    """
    Calls Google Gemini API using REST endpoint with GEMINI_API_KEY.
    Returns parsed JSON or None if unavailable.
    """
    if not GEMINI_API_KEY:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json"
        }
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_text)
    except Exception as e:
        print(f"[Gemini API Warning] {e}")
    return None

def heuristic_idea_validator(idea_title, target_market, problem_solved, pricing, budget):
    """
    Deep, honest startup validator providing realistic critical analysis.
    Does NOT blindly praise every idea; highlights concrete risks and experiments.
    """
    title_lower = (idea_title or "").lower()
    desc_lower = (problem_solved or "").lower()
    budget_val = float(budget or 10000)
    
    # Analyze capital intensity
    is_hardware = any(w in title_lower or w in desc_lower for w in ["hardware", "manufacturing", "drone", "robot", "ev", "solar", "device"])
    is_platform = any(w in title_lower or w in desc_lower for w in ["marketplace", "uber for", "tinder for", "network", "social app", "platform"])
    is_service = any(w in title_lower or w in desc_lower for w in ["agency", "management", "tutoring", "editing", "service", "consulting", "design", "development"])
    
    # Calculate scores
    problem_score = 78
    market_score = 72
    moat_score = 65
    financial_score = 80
    
    strengths = []
    weaknesses = []
    critical_risks = []
    experiments = []
    
    if is_service:
        problem_score = 86
        financial_score = 92
        moat_score = 62
        strengths.append("Low capital requirement; cash flow can be generated in the first 14 days.")
        strengths.append("High control over service delivery and direct relationship with buyers.")
        strengths.append("Easy to pivot or tailor services based on client requests.")
        weaknesses.append("High reliance on personal time; difficult to scale without hiring competent talent.")
        weaknesses.append("Low defensive moat initially; competitors can copy identical service offerings.")
        critical_risks.append("Client churn: If clients leave after 1-2 months, you remain stuck in constant customer hunting.")
        critical_risks.append("Scope creep: Clients demanding extra work without paying additional fees.")
        experiments.append("Build 3 bespoke specimen deliverables and send to 10 prospective clients with a 50% pilot discount.")
        experiments.append("Walk in to 5 local businesses or message 15 decision makers to evaluate if this problem is in their top 3 urgent priorities.")
        experiments.append("Attempt to secure 1 upfront deposit before spending money on any software or branding.")
    elif is_platform:
        problem_score = 68
        financial_score = 55
        moat_score = 75
        strengths.append("High upside and scalable network effects once critical mass is achieved.")
        strengths.append("Software margins are very high once the platform is built.")
        weaknesses.append("The 'Chicken-and-Egg' dilemma: sellers won't join without buyers, and buyers won't join without sellers.")
        weaknesses.append("Substantial customer acquisition cost (CAC) required to seed both sides.")
        critical_risks.append("Running out of capital before reaching critical mass of active users.")
        critical_risks.append("Platform disintermediation: users might exchange contact info and deal directly offline to bypass fees.")
        experiments.append("Do things that don't scale: manually connect 10 buyers with 10 sellers via a WhatsApp group or Google Sheet before building software.")
        experiments.append("Create a simple landing page with a waitlist and measure conversion rate from 100 targeted campus visitors.")
        experiments.append("Interview 5 buyers and 5 sellers individually to uncover which side has the more agonizing pain point.")
    elif is_hardware:
        problem_score = 70
        financial_score = 45
        moat_score = 85
        strengths.append("Strong IP defensibility and high barrier to entry against low-effort copycats.")
        strengths.append("Tangible physical value proposition that customers can clearly see and touch.")
        weaknesses.append("High upfront prototyping, tooling, and component procurement costs.")
        weaknesses.append("Supply chain delays, defective units, and complex warranty/return logistics.")
        critical_risks.append("Working capital trap: inventory ties up your cash before sales occur.")
        critical_risks.append("Component obsolescence or unexpected regulatory certifications.")
        experiments.append("Build a functional proof-of-concept using off-the-shelf components before custom manufacturing.")
        experiments.append("Launch a pre-order campaign with 3D renders and detailed specs to validate willingness to pay.")
        experiments.append("Quote manufacturing costs with 3 local fabricators to calculate true unit economics.")
    else:
        # Generic well-grounded assessment
        strengths.append("Solves a recognizable operational or creative bottleneck for customers.")
        strengths.append("Can be started with lean resources and iterative feedback loops.")
        weaknesses.append("Requires continuous outbound sales and disciplined pipeline management.")
        weaknesses.append("Pricing power may be constrained until brand credibility is established.")
        critical_risks.append("Underestimating customer acquisition effort: building it does not mean they will come.")
        critical_risks.append("Cash flow lag: payment delays of 30-60 days can choke operational runway.")
        experiments.append("Interview 5 prospective buyers without pitching; ask how they currently solve this problem.")
        experiments.append("Pre-sell the service/product with a 1-page proposal; require a 20% token deposit.")
        experiments.append("Run a ₹500 test ad or 20 targeted direct outreach messages to gauge click/reply rate.")

    # Calculate overall index
    overall_score = int((problem_score * 0.3) + (market_score * 0.25) + (moat_score * 0.2) + (financial_score * 0.25))
    
    if overall_score >= 80:
        verdict = "STRONG OPPORTUNITY"
        verdict_badge = "green"
        summary = "This idea has solid unit economics, manageable startup friction, and genuine commercial demand. Focus on immediate customer acquisition rather than over-engineering."
    elif overall_score >= 65:
        verdict = "VIABLE WITH CAUTION"
        verdict_badge = "yellow"
        summary = "Feasible, but possesses identifiable blind spots around retention or customer acquisition costs. Run the recommended validation experiments before committing capital."
    else:
        verdict = "NEEDS SIGNIFICANT PIVOT"
        verdict_badge = "red"
        summary = "High capital or operational risk for a first-time founder. Highly recommend narrowing the scope to a focused service or concierge MVP to test demand with zero financial risk."

    return {
        "idea_title": idea_title or "Submitted Business Concept",
        "overall_score": overall_score,
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "summary": summary,
        "scores": {
            "problem_intensity": problem_score,
            "market_demand": market_score,
            "defensibility": moat_score,
            "financial_ease": financial_score
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "critical_risks": critical_risks,
        "validation_experiments": experiments,
        "is_ai_generated": False
    }

# ---------------------------------------------------------
# ROUTES & REST APIS
# ---------------------------------------------------------
@app.route("/")
def home():
    """Renders main single-page application"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM workspace_state WHERE id = 1")
    user_state = dict(c.fetchone() or {})
    c.execute("SELECT * FROM budget_plans WHERE id = 1")
    budget_state = dict(c.fetchone() or {})
    c.execute("SELECT * FROM outreach_leads ORDER BY id DESC")
    leads = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return render_template(
        "index.html",
        businesses=BUSINESSES,
        user_state=user_state,
        budget_state=budget_state,
        leads=leads,
        gemini_enabled=bool(GEMINI_API_KEY)
    )

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "platform": "VenturePath AI",
        "gemini_active": bool(GEMINI_API_KEY),
        "db_connected": os.path.exists(DB_PATH)
    })

@app.route("/api/businesses", methods=["GET"])
def get_businesses():
    return jsonify({"businesses": BUSINESSES})

@app.route("/api/recommend", methods=["POST"])
def recommend_businesses():
    """
    Multi-criteria recommendation algorithm matching skills, budget, mode, and interests.
    """
    data = request.get_json(silent=True) or {}
    user_skills = [s.lower().strip() for s in data.get("skills", []) if s.strip()]
    user_interests = [i.lower().strip() for i in data.get("interests", []) if i.strip()]
    budget = float(data.get("budget", 15000) or 15000)
    mode = (data.get("mode", "all") or "all").lower()
    time_avail = (data.get("time", "part-time") or "part-time").lower()
    
    scored = []
    for b in BUSINESSES:
        score = 0
        match_reasons = []
        
        # 1. Skills match (up to 40 pts)
        skill_matches = sum(1 for s in user_skills if any(s in b_skill or b_skill in s for b_skill in b["skills"]))
        if skill_matches > 0:
            pts = min(40, skill_matches * 15)
            score += pts
            match_reasons.append(f"Matches {skill_matches} of your core skills ({', '.join(b['skills'][:2])})")
        else:
            score += 10 # Base learnable potential
            
        # 2. Budget feasibility (up to 30 pts)
        if budget >= b["budget"]:
            score += 30
            surplus = int(budget - b["budget"])
            match_reasons.append(f"Comfortably within budget (₹{b['budget']:,} required, ₹{surplus:,} safety runway)")
        else:
            shortfall = int(b["budget"] - budget)
            score += max(5, int(20 - (shortfall / 1000)))
            match_reasons.append(f"Slightly above target (needs ₹{shortfall:,} additional lean bootstrap)")
            
        # 3. Mode compatibility (up to 15 pts)
        if mode == "all" or b["mode"] == mode or b["mode"] == "hybrid":
            score += 15
            match_reasons.append(f"Perfect fit for {b['mode'].upper()} execution")
        else:
            score += 5
            
        # 4. Interests alignment (up to 15 pts)
        int_matches = sum(1 for i in user_interests if i in b["interests"])
        if int_matches > 0:
            score += 15
            match_reasons.append(f"Aligns with your passion for {', '.join(b['interests'])}")
        else:
            score += 8
            
        # Calculate percentage match 0-100%
        match_pct = min(98, max(55, score))
        scored.append((match_pct, b, match_reasons))
        
    scored.sort(key=lambda item: item[0], reverse=True)
    
    results = []
    for match_pct, b, reasons in scored:
        item = dict(b)
        item["match_percentage"] = match_pct
        item["match_reasons"] = reasons
        results.append(item)
        
    # Persist search state
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        UPDATE workspace_state 
        SET skills = ?, budget = ?, mode = ?, time_commitment = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = 1
    """, (json.dumps(user_skills), budget, mode, time_avail))
    conn.commit()
    conn.close()
    
    return jsonify({"recommendations": results})

@app.route("/api/roadmap", methods=["POST"])
def get_roadmap():
    """Returns the comprehensive 10-milestone roadmap for the chosen business"""
    data = request.get_json(silent=True) or {}
    business_name = data.get("business_name", "")
    
    business = next((b for b in BUSINESSES if b["name"] == business_name or b["id"] == business_name), None)
    if not business:
        business = BUSINESSES[0] # Default to first
        
    # Fetch completed milestone tasks from DB
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT step_index, is_completed, notes FROM roadmap_items WHERE business_name = ?", (business["name"],))
    completed_map = {row["step_index"]: bool(row["is_completed"]) for row in c.fetchall()}
    conn.close()
    
    stages = []
    for idx, stage in enumerate(business["roadmap_stages"]):
        is_done = completed_map.get(idx, False)
        stages.append({
            "index": idx,
            "title": stage["title"],
            "tasks": stage["tasks"],
            "is_completed": is_done,
            "estimated_timeline": f"Week {idx // 2 + 1}" if idx > 0 else "Days 1–3"
        })
        
    completed_count = sum(1 for s in stages if s["is_completed"])
    progress_percentage = int((completed_count / len(stages)) * 100) if stages else 0
    
    return jsonify({
        "business": business,
        "stages": stages,
        "completed_count": completed_count,
        "total_stages": len(stages),
        "progress_percentage": progress_percentage
    })

@app.route("/api/validate", methods=["POST"])
def validate_idea():
    """
    AI-Powered Business Idea Validator.
    Uses Gemini API if key is available; otherwise provides expert heuristic validation.
    """
    data = request.get_json(silent=True) or {}
    idea_title = data.get("idea_title", "").strip()
    target_market = data.get("target_market", "").strip()
    problem_solved = data.get("problem_solved", "").strip()
    pricing = data.get("pricing", "").strip()
    budget = data.get("budget", 10000)
    
    if not idea_title:
        return jsonify({"error": "Please provide an idea title or description"}), 400

    # Try Gemini API first if configured
    gemini_result = None
    if GEMINI_API_KEY:
        prompt = f"""
        You are a seasoned startup accelerator director and critical business architect for college founders.
        Evaluate this early-stage business idea with honesty, rigor, and practical advice. Do NOT give naive praise.
        
        Idea: {idea_title}
        Target Market: {target_market}
        Problem Solved: {problem_solved}
        Proposed Pricing: {pricing}
        Starting Capital: ₹{budget}
        
        Return a strict JSON object with these keys:
        {{
          "idea_title": "{idea_title}",
          "overall_score": <number 0-100>,
          "verdict": "<HIGH POTENTIAL | PROCEED WITH CAUTION | PIVOT RECOMMENDED>",
          "verdict_badge": "<green | yellow | red>",
          "summary": "<2 sentence honest verdict>",
          "scores": {{
            "problem_intensity": <0-100>,
            "market_demand": <0-100>,
            "defensibility": <0-100>,
            "financial_ease": <0-100>
          }},
          "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
          "weaknesses": ["<blindspot 1>", "<blindspot 2>", "<blindspot 3>"],
          "critical_risks": ["<dealbreaker risk 1>", "<dealbreaker risk 2>"],
          "validation_experiments": ["<concrete test 1>", "<concrete test 2>", "<concrete test 3>"],
          "is_ai_generated": true
        }}
        """
        gemini_result = call_gemini_api(prompt)

    if gemini_result and "overall_score" in gemini_result:
        evaluation = gemini_result
        evaluation["is_ai_generated"] = True
    else:
        evaluation = heuristic_idea_validator(idea_title, target_market, problem_solved, pricing, budget)

    # Save to history
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO validation_history (idea_title, target_market, score, verdict, data_json)
            VALUES (?, ?, ?, ?, ?)
        """, (idea_title, target_market, evaluation["overall_score"], evaluation["verdict"], json.dumps(evaluation)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving validation: {e}")

    return jsonify({"evaluation": evaluation})

@app.route("/api/outreach", methods=["POST"])
def generate_outreach_templates():
    """Generates personalized first 10 customers templates and channel strategy"""
    data = request.get_json(silent=True) or {}
    business_name = data.get("business_name", "My Startup").strip()
    founder_name = data.get("founder_name", "Alex").strip()
    target_prospect = data.get("target_prospect", "Local Cafe Owner").strip()
    niche = data.get("niche", "Hospitality & Retail").strip()
    value_prop = data.get("value_prop", "grow your weekly inquiries through high-converting Reels").strip()
    
    whatsapp_msg = (
        f"Hi {target_prospect}! 👋 My name is {founder_name}, a student founder working on {business_name}.\n\n"
        f"I've been a frequent visitor of your business and noticed an opportunity to help you {value_prop}.\n\n"
        f"I created 2 sample mockups specifically tailored for your brand (no cost at all). "
        f"Would you be open to me sharing a quick 60-second video walkthrough here on WhatsApp?\n\n"
        f"No pressure at all—appreciate your time and keep doing great work!"
    )
    
    email_subject = f"Quick question regarding {target_prospect}'s growth ({business_name})"
    email_body = (
        f"Dear {target_prospect},\n\n"
        f"I hope you are having a productive week.\n\n"
        f"My name is {founder_name}, founder of {business_name}. I specialize in helping {niche} businesses {value_prop}.\n\n"
        f"Rather than sending a generic sales pitch, I audited your current digital presence and drafted 3 high-impact recommendations you can implement right away:\n"
        f"1. Immediate opportunity to capture weekend footfall.\n"
        f"2. A simple conversion tweak on your inquiry flow.\n"
        f"3. A sample high-retention content template.\n\n"
        f"Would you have 10 minutes this Thursday or Friday for a brief call, or would you prefer I send the PDF summary over email?\n\n"
        f"Warm regards,\n"
        f"{founder_name}\n"
        f"{business_name}"
    )
    
    social_dm = (
        f"Hey {target_prospect}! Love what you've built with your brand. "
        f"I'm {founder_name} from {business_name}. We help brands in {niche} {value_prop}. "
        f"Just designed a custom specimen for you guys—mind if I send over the link here to get your thoughts?"
    )
    
    follow_up_msg = (
        f"Hi {target_prospect}! Hope you're doing well. Just wanted to float this back to the top of your inbox in case it got buried. "
        f"Happy to send over the free sample whenever you have a moment, or feel free to let me know if this isn't on your radar right now. Thank you!"
    )
    
    discovery_questions = [
        "What is currently your single most reliable source of new customers?",
        "How much time do you or your team spend each week managing this manually?",
        "If you could fix one bottleneck in your business this month, what would it be?",
        "What has stopped you from solving this previously (time, cost, or finding the right person)?",
        "What would a successful outcome look like for you 60 days from now?"
    ]
    
    channels = [
        {"name": "Local Physical Walk-ins & Meetups", "fit": "High", "why": "Immediate trust building; owners appreciate face-to-face initiative."},
        {"name": "WhatsApp Community Groups & Referrals", "fit": "Very High", "why": "Direct attention with 98% open rates in Indian market."},
        {"name": "Instagram Direct Messaging", "fit": "High", "why": "Visual portfolio link delivers instant proof within the app."},
        {"name": "LinkedIn Founder Outreach", "fit": "Medium", "why": "Best for B2B consulting, tech services, and corporate clients."}
    ]

    return jsonify({
        "whatsapp_template": whatsapp_msg,
        "email_template": {"subject": email_subject, "body": email_body},
        "social_dm_template": social_dm,
        "follow_up_template": follow_up_msg,
        "discovery_questions": discovery_questions,
        "recommended_channels": channels
    })

@app.route("/api/budget/calculate", methods=["POST"])
def calculate_budget():
    """
    Financial calculation engine providing startup costs, break-even, runway, and profit estimates.
    """
    data = request.get_json(silent=True) or {}
    starting_capital = float(data.get("starting_capital", 20000) or 0)
    equipment = float(data.get("equipment_cost", 4000) or 0)
    marketing = float(data.get("marketing_cost", 3000) or 0)
    registration = float(data.get("registration_cost", 1500) or 0)
    inventory = float(data.get("inventory_cost", 2500) or 0)
    monthly_expenses = float(data.get("monthly_expenses", 3500) or 0)
    selling_price = float(data.get("selling_price", 1200) or 0)
    sales_volume = int(data.get("expected_sales", 15) or 0)
    
    total_startup_capex = equipment + marketing + registration + inventory
    remaining_capital = starting_capital - total_startup_capex
    estimated_monthly_revenue = selling_price * sales_volume
    estimated_monthly_profit = estimated_monthly_revenue - monthly_expenses
    
    # Break-even sales volume: monthly expenses / selling price
    break_even_units = int((monthly_expenses / selling_price) + 0.99) if selling_price > 0 else 0
    
    # Estimated runway in months
    runway_months = 0
    if remaining_capital > 0:
        if monthly_expenses > 0:
            runway_months = round(remaining_capital / monthly_expenses, 1)
        else:
            runway_months = 12.0
            
    # Persist in DB
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        UPDATE budget_plans SET
            starting_capital = ?, equipment_cost = ?, marketing_cost = ?,
            registration_cost = ?, inventory_cost = ?, monthly_expenses = ?,
            selling_price = ?, expected_sales = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = 1
    """, (starting_capital, equipment, marketing, registration, inventory, monthly_expenses, selling_price, sales_volume))
    conn.commit()
    conn.close()

    return jsonify({
        "total_startup_capex": round(total_startup_capex, 2),
        "remaining_capital": round(remaining_capital, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "estimated_monthly_revenue": round(estimated_monthly_revenue, 2),
        "estimated_monthly_profit": round(estimated_monthly_profit, 2),
        "break_even_units": break_even_units,
        "runway_months": runway_months,
        "is_profitable": estimated_monthly_profit > 0
    })

@app.route("/api/resources", methods=["GET"])
def get_resources():
    """
    Curated Indian & Global official startup resources directory.
    Uses verified official governmental and platform URLs.
    """
    category = request.args.get("category", "all").lower()
    query = request.args.get("q", "").lower().strip()
    
    directory = [
        {
            "title": "Startup India Official Portal",
            "category": "government",
            "url": "https://www.startupindia.gov.in/",
            "badge": "Official Govt",
            "description": "Government of India flagship initiative offering DPIIT recognition, tax exemptions, seed fund schemes, and patent fast-tracking for registered startups.",
            "benefits": ["DPIIT Recognition", "Startup India Seed Fund Scheme", "3-year Income Tax Exemption"]
        },
        {
            "title": "Udyam MSME Registration Portal",
            "category": "government",
            "url": "https://udyamregistration.gov.in/",
            "badge": "Official MSME",
            "description": "Zero-fee official government registration for Micro, Small and Medium Enterprises. Unlocks collateral-free bank loans and priority sector credit.",
            "benefits": ["100% Free Registration", "Collateral-free CGTMSE bank loans", "Protection against delayed payments"]
        },
        {
            "title": "Ministry of Corporate Affairs (MCA)",
            "category": "legal",
            "url": "https://www.mca.gov.in/",
            "badge": "Official MCA",
            "description": "Incorporation portal for One Person Companies (OPC), Private Limited Companies, and LLPs (Limited Liability Partnerships) in India.",
            "benefits": ["SPICe+ Incorporation", "Director Identification (DIN)", "Name Reservation Service (RUN)"]
        },
        {
            "title": "Google Trends Market Research",
            "category": "research",
            "url": "https://trends.google.com/trends/",
            "badge": "Research Tool",
            "description": "Real-time search volume and regional interest analytics across Indian cities and states to validate customer demand before building.",
            "benefits": ["City-level interest breakdown", "Related rising search queries", "Seasonality trend curves"]
        },
        {
            "title": "T-Hub Hyderabad & NSRCEL IIM-B",
            "category": "incubator",
            "url": "https://t-hub.co/",
            "badge": "Top Incubator",
            "description": "India's premier startup innovation hubs offering university founder acceleration programs, prototyping labs, and investor demo days.",
            "benefits": ["Seed grant opportunities", "Academic mentorship", "Cloud credits (AWS, Google Cloud)"]
        },
        {
            "title": "Legal Agreement & NDA Templates",
            "category": "legal",
            "url": "https://www.startupindia.gov.in/content/sih/en/reources.html",
            "badge": "Verified Templates",
            "description": "Standard verified legal templates including Co-founder Agreements, Non-Disclosure Agreements (NDAs), and Freelance Client Contracts.",
            "benefits": ["IP assignment clauses", "Founder vesting schedules", "Dispute resolution standard terms"]
        }
    ]
    
    filtered = directory
    if category != "all":
        filtered = [r for r in filtered if r["category"] == category]
    if query:
        filtered = [r for r in filtered if query in r["title"].lower() or query in r["description"].lower()]
        
    return jsonify({"resources": filtered})

@app.route("/api/workspace", methods=["GET"])
def get_workspace():
    """Returns aggregated user workspace state for the dashboard"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM workspace_state WHERE id = 1")
    state = dict(c.fetchone() or {})
    c.execute("SELECT * FROM budget_plans WHERE id = 1")
    budget = dict(c.fetchone() or {})
    c.execute("SELECT * FROM outreach_leads ORDER BY id DESC")
    leads = [dict(row) for row in c.fetchall()]
    
    # Active business
    active_b_name = state.get("selected_business", "Social Media Management & Reels Agency")
    business = next((b for b in BUSINESSES if b["name"] == active_b_name or b["id"] == active_b_name), BUSINESSES[0])
    
    # Roadmap items
    c.execute("SELECT step_index, is_completed FROM roadmap_items WHERE business_name = ?", (business["name"],))
    completed_map = {row["step_index"]: bool(row["is_completed"]) for row in c.fetchall()}
    conn.close()
    
    total_stages = len(business["roadmap_stages"])
    completed_stages = sum(1 for i in range(total_stages) if completed_map.get(i, False))
    progress = int((completed_stages / total_stages) * 100) if total_stages else 0

    return jsonify({
        "state": state,
        "active_business": business,
        "budget": budget,
        "leads": leads,
        "roadmap_summary": {
            "completed": completed_stages,
            "total": total_stages,
            "percentage": progress
        }
    })

@app.route("/api/workspace/toggle-milestone", methods=["POST"])
def toggle_milestone():
    """Toggles completion state of a specific roadmap milestone"""
    data = request.get_json(silent=True) or {}
    business_name = data.get("business_name", "")
    step_index = int(data.get("step_index", 0))
    is_completed = 1 if data.get("is_completed", False) else 0
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO roadmap_items (business_name, step_index, is_completed, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(business_name, step_index) DO UPDATE SET
            is_completed = excluded.is_completed,
            updated_at = CURRENT_TIMESTAMP
    """, (business_name, step_index, is_completed))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "step_index": step_index, "is_completed": bool(is_completed)})

@app.route("/api/workspace/select-business", methods=["POST"])
def select_business():
    """Updates active selected business in workspace"""
    data = request.get_json(silent=True) or {}
    business_name = data.get("business_name", "")
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE workspace_state SET selected_business = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1", (business_name,))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "selected_business": business_name})

@app.route("/api/workspace/add-lead", methods=["POST"])
def add_lead():
    """Adds a new prospect lead to the CRM outreach table"""
    data = request.get_json(silent=True) or {}
    name = (data.get("lead_name") or "").strip()
    channel = (data.get("channel") or "WhatsApp").strip()
    status = (data.get("status") or "Identified").strip()
    notes = (data.get("notes") or "").strip()
    
    if not name:
        return jsonify({"error": "Lead name is required"}), 400
        
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO outreach_leads (lead_name, channel, status, notes) VALUES (?, ?, ?, ?)", (name, channel, status, notes))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    
    return jsonify({"success": True, "lead": {"id": new_id, "lead_name": name, "channel": channel, "status": status, "notes": notes}})

@app.route("/api/workspace/update-lead-status", methods=["POST"])
def update_lead_status():
    data = request.get_json(silent=True) or {}
    lead_id = int(data.get("id", 0))
    status = (data.get("status") or "Contacted").strip()
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE outreach_leads SET status = ? WHERE id = ?", (status, lead_id))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "id": lead_id, "status": status})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"==================================================")
    print(f" VenturePath AI Server running at http://localhost:{port}")
    print(f" Gemini AI Engine: {'ACTIVE (Online Key)' if GEMINI_API_KEY else 'OFFLINE DEMO MODE (Intelligent Heuristics)'}")
    print(f" SQLite Database: {DB_PATH}")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=True)
