import streamlit as st
from Backend import (
    run_resume_analysis,
    generate_chatbot_response,
    get_file_hash
)

st.set_page_config(
    page_title="ResumeAI — Career Intelligence",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">

<style>
:root {
    --bg-void:       #050810;
    --bg-deep:       #090d1a;
    --bg-panel:      #0d1220;
    --bg-glass:      rgba(255,255,255,0.035);
    --bg-glass-hover:rgba(255,255,255,0.065);
    --border:        rgba(255,255,255,0.07);
    --border-lit:    rgba(99,202,255,0.25);
    --accent-cyan:   #3ECFFF;
    --accent-violet: #9B6FFF;
    --accent-mint:   #00E5B0;
    --accent-amber:  #FFB347;
    --text-primary:  #EEF2FF;
    --text-muted:    #6B7A9F;
    --text-dim:      #3A435E;
    --glow-cyan:     0 0 40px rgba(62,207,255,0.15);
    --glow-violet:   0 0 40px rgba(155,111,255,0.15);
    --radius-card:   20px;
    --radius-pill:   999px;
}
*, *::before, *::after { box-sizing: border-box; }
.stApp {
    background: var(--bg-void);
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem; max-width: 1280px; }

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(62,207,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(62,207,255,0.03) 1px, transparent 1px);
    background-size: 64px 64px;
    pointer-events: none;
    z-index: 0;
}

.hero-wrap {
    position: relative;
    text-align: center;
    padding: 3rem 2rem 2rem;
    overflow: hidden;
    margin-bottom: 1rem;
}
.hero-glow {
    position: absolute;
    top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 640px; height: 320px;
    background: radial-gradient(ellipse at 50% 0%, rgba(62,207,255,0.18) 0%, rgba(155,111,255,0.10) 45%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(62,207,255,0.08);
    border: 1px solid rgba(62,207,255,0.22);
    color: var(--accent-cyan);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: var(--radius-pill);
    margin-bottom: 1.5rem;
}
.hero-tag .dot {
    width: 6px; height: 6px;
    background: var(--accent-cyan);
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.4; transform:scale(0.7); }
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -0.03em;
    margin: 0 auto 1rem;
    max-width: 800px;
}
.hero-title .highlight {
    background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-violet) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.7;
}

.features-row {
    display: flex;
    gap: 14px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
}
.feat-chip {
    display: flex;
    align-items: center;
    gap: 9px;
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-pill);
    padding: 10px 18px;
    font-size: 0.88rem;
    font-weight: 500;
    color: var(--text-primary);
    transition: border-color 0.25s, background 0.25s, transform 0.2s;
    cursor: default;
}
.feat-chip:hover {
    background: var(--bg-glass-hover);
    border-color: var(--border-lit);
    transform: translateY(-2px);
}
.feat-chip .icon {
    font-size: 1.05rem;
}
.feat-chip .chip-label {
    color: var(--text-muted);
    font-weight: 400;
    margin-left: 2px;
    font-size: 0.82rem;
}

.upload-section-inner {
    text-align: center;
    margin-bottom: 1rem;
}
.upload-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.upload-hint {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-bottom: 0;
}

[data-testid="stFileUploader"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 auto !important;
}
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] section {
    width: auto !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 auto !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    min-height: unset !important;
    box-shadow: none !important;
}
[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] > div > span,
[data-testid="stFileUploaderDropzone"] > div > div > span {
    display: none !important;
}
[data-testid="stFileUploaderDropzone"] button {
    display: block !important;
    margin: 0 auto !important;
    background: linear-gradient(135deg, rgba(62,207,255,0.12), rgba(155,111,255,0.12)) !important;
    border: 1px solid rgba(62,207,255,0.3) !important;
    border-radius: 12px !important;
    color: var(--accent-cyan) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 10px 24px !important;
    transition: background 0.2s, border-color 0.2s, transform 0.2s !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background: linear-gradient(135deg, rgba(62,207,255,0.22), rgba(155,111,255,0.22)) !important;
    border-color: var(--accent-cyan) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stFileUploaderFile"] {
    background: rgba(62,207,255,0.06) !important;
    border: 1px solid rgba(62,207,255,0.18) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    margin: 12px auto 0 !important;
}

.element-container { margin-bottom: 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0.35rem !important; }
.stMarkdown { margin: 0 !important; padding: 0 !important; }

.sec-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.6rem;
    margin-top: 0.4rem;
}
.sec-header .sec-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.sec-icon-cyan   { background: rgba(62,207,255,0.12); border: 1px solid rgba(62,207,255,0.2); }
.sec-icon-violet { background: rgba(155,111,255,0.12); border: 1px solid rgba(155,111,255,0.2); }
.sec-icon-mint   { background: rgba(0,229,176,0.10); border: 1px solid rgba(0,229,176,0.2); }
.sec-icon-amber  { background: rgba(255,179,71,0.10); border: 1px solid rgba(255,179,71,0.2); }
.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}
.sec-count {
    margin-left: auto;
    font-size: 0.78rem;
    color: var(--text-muted);
    background: var(--bg-glass);
    border: 1px solid var(--border);
    padding: 3px 10px;
    border-radius: var(--radius-pill);
}

.skills-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1.2rem;
}
.skill-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 13px;
    border-radius: var(--radius-pill);
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    border: 1px solid transparent;
    transition: transform 0.15s, box-shadow 0.15s;
    cursor: default;
}
.skill-badge:hover { transform: translateY(-2px); }
.badge-cyan   { background: rgba(62,207,255,0.10); border-color: rgba(62,207,255,0.22); color: var(--accent-cyan); }
.badge-violet { background: rgba(155,111,255,0.10); border-color: rgba(155,111,255,0.22); color: var(--accent-violet); }
.badge-mint   { background: rgba(0,229,176,0.10); border-color: rgba(0,229,176,0.22); color: var(--accent-mint); }
.badge-amber  { background: rgba(255,179,71,0.10); border-color: rgba(255,179,71,0.22); color: var(--accent-amber); }
.badge-missing { background: rgba(255,70,70,0.08); border-color: rgba(255,70,70,0.2); color: #FF7070; }

.match-grid { display: flex; flex-direction: column; gap: 10px; }
.match-card {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 16px 18px;
    display: grid;
    grid-template-columns: 36px 1fr auto;
    align-items: center;
    gap: 14px;
    transition: border-color 0.25s, background 0.25s, transform 0.2s, box-shadow 0.25s;
    position: relative;
    overflow: hidden;
}
.match-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
}
.match-card-1::before { background: linear-gradient(180deg, #FFD700, #FFB347); }
.match-card-2::before { background: linear-gradient(180deg, #C0C0C0, #A8A8A8); }
.match-card-3::before { background: linear-gradient(180deg, #CD7F32, #A0522D); }
.match-card-4::before, .match-card-5::before { background: linear-gradient(180deg, var(--accent-cyan), var(--accent-violet)); }
.match-card:hover {
    border-color: var(--border-lit);
    transform: translateX(4px);
    box-shadow: var(--glow-cyan);
    background: rgba(13,18,32,0.9);
}
.rank-circle {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 800;
}
.rank-1 { background: rgba(255,215,0,0.12); color: #FFD700; border: 1px solid rgba(255,215,0,0.3); }
.rank-2 { background: rgba(192,192,192,0.12); color: #C0C0C0; border: 1px solid rgba(192,192,192,0.3); }
.rank-3 { background: rgba(205,127,50,0.12); color: #CD7F32; border: 1px solid rgba(205,127,50,0.3); }
.rank-other { background: var(--bg-glass); color: var(--text-muted); border: 1px solid var(--border); }
.match-info .role-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.97rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
}
.match-bar-track {
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: var(--radius-pill);
    overflow: hidden;
    width: 100%;
}
.match-bar-fill {
    height: 4px;
    border-radius: var(--radius-pill);
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet));
}
.match-score-pill {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: var(--radius-pill);
    white-space: nowrap;
}
.score-high  { background: rgba(0,229,176,0.12); color: var(--accent-mint); border: 1px solid rgba(0,229,176,0.25); }
.score-mid   { background: rgba(62,207,255,0.10); color: var(--accent-cyan); border: 1px solid rgba(62,207,255,0.2); }
.score-low   { background: rgba(155,111,255,0.10); color: var(--accent-violet); border: 1px solid rgba(155,111,255,0.2); }

details {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 0 !important;
    margin-bottom: 10px !important;
    overflow: hidden !important;
    transition: border-color 0.25s !important;
}
details:hover { border-color: rgba(155,111,255,0.25) !important; }
details[open] { border-color: rgba(155,111,255,0.3) !important; }
summary {
    padding: 16px 20px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    cursor: pointer !important;
    list-style: none !important;
}
summary::-webkit-details-marker { display: none; }
details > div { padding: 0 20px 18px !important; }

[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

.chat-response {
    background: linear-gradient(135deg, rgba(62,207,255,0.06) 0%, rgba(155,111,255,0.06) 100%);
    border: 1px solid rgba(62,207,255,0.15);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 14px;
    padding: 20px 22px;
    color: var(--text-primary);
    font-size: 0.97rem;
    line-height: 1.75;
    margin-top: 1rem;
    box-shadow: var(--glow-cyan);
}
.chat-avatar {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(62,207,255,0.08);
    border: 1px solid rgba(62,207,255,0.18);
    border-radius: var(--radius-pill);
    padding: 5px 12px 5px 8px;
    font-size: 0.8rem;
    color: var(--accent-cyan);
    font-weight: 600;
    margin-bottom: 10px;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-violet) 100%);
    color: #050810;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.6rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.92rem;
    letter-spacing: 0.02em;
    transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 20px rgba(62,207,255,0.2);
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
    box-shadow: 0 8px 28px rgba(62,207,255,0.3);
}
.stTextInput > div > div > input {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.93rem !important;
    transition: border-color 0.25s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 3px rgba(62,207,255,0.1) !important;
}
[data-testid="column"] {
    padding-left: 0.4rem !important;
    padding-right: 0.4rem !important;
}
div[data-testid="stColumns"] {
    gap: 0.6rem !important;
}
.stSuccess {
    background: rgba(0,229,176,0.08) !important;
    border: 1px solid rgba(0,229,176,0.2) !important;
    border-radius: 12px !important;
    color: var(--accent-mint) !important;
}
.stWarning {
    background: rgba(255,179,71,0.08) !important;
    border: 1px solid rgba(255,179,71,0.2) !important;
    border-radius: 12px !important;
}
.stInfo {
    background: rgba(62,207,255,0.06) !important;
    border: 1px solid rgba(62,207,255,0.15) !important;
    border-radius: 12px !important;
}
.footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    color: var(--text-dim);
    font-size: 0.8rem;
    letter-spacing: 0.04em;
}
.footer span { color: var(--text-muted); }
.stSpinner > div {
    border-color: var(--accent-cyan) transparent transparent transparent !important;
}
.label-muted {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 6px;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
.anim { animation: fadeUp 0.45s ease both; }
.anim-d1 { animation-delay: 0.05s; }
.anim-d2 { animation-delay: 0.12s; }
.anim-d3 { animation-delay: 0.2s; }
</style>
""", unsafe_allow_html=True)

BADGE_COLORS = ["badge-cyan", "badge-violet", "badge-mint", "badge-amber"]

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "last_file_hash" not in st.session_state:
    st.session_state.last_file_hash = None
if "chat_response" not in st.session_state:
    st.session_state.chat_response = ""


def skill_badges(skills, color_class="badge-cyan", missing=False):
    cls = "badge-missing" if missing else color_class
    return " ".join(
        f'<span class="skill-badge {cls}">{s}</span>' for s in skills
    )


def score_class(score):
    if score >= 70:
        return "score-high"
    if score >= 45:
        return "score-mid"
    return "score-low"


def render_match_cards(matched_jobs):
    st.markdown("""
    <div class="sec-header anim">
        <div class="sec-icon sec-icon-cyan">💼</div>
        <div class="sec-title">Top Matched Job Roles</div>
    </div>
    """, unsafe_allow_html=True)

    if matched_jobs.empty:
        st.warning("No job matches found.")
        return

    top5 = matched_jobs.head(5).sort_values("match_score", ascending=False)

    cards_html = '<div class="match-grid">'
    rank_labels = {
        1: ("rank-1", "match-card-1"),
        2: ("rank-2", "match-card-2"),
        3: ("rank-3", "match-card-3"),
        4: ("rank-other", "match-card-4"),
        5: ("rank-other", "match-card-5")
    }

    for idx, (_, row) in enumerate(top5.iterrows(), 1):
        score = float(row["match_score"])
        role = row["job_role"]
        bar = max(0, min(int(score), 100))
        rk_cls, card_cls = rank_labels.get(idx, ("rank-other", "match-card-4"))
        sc_cls = score_class(score)
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        rank_label = medals.get(idx, str(idx))

        cards_html += f"""
        <div class="match-card {card_cls} anim anim-d{min(idx,3)}">
            <div class="rank-circle {rk_cls}">{rank_label}</div>
            <div class="match-info">
                <div class="role-name">{role}</div>
                <div class="match-bar-track">
                    <div class="match-bar-fill" style="width:{bar}%"></div>
                </div>
            </div>
            <div class="match-score-pill {sc_cls}">{score:.1f}%</div>
        </div>"""

    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


st.markdown("""
<div class="hero-wrap">
    <div class="hero-glow"></div>
    <div class="hero-tag"><span class="dot"></span>AI-Powered · Intelligent · Instant</div>
    <div class="hero-title">
        Your Resume,<br>
        <span class="highlight">Decoder.</span>
    </div>
    <div class="hero-sub">
        Upload your resume and get instant job matching, skill gap analysis, course recommendations, and AI career guidance.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="features-row">
    <div class="feat-chip"><span class="icon">⚡</span> Smart Job Matching <span class="chip-label">Smart jobs</span></div>
    <div class="feat-chip"><span class="icon">🔍</span> Skill Gap Analysis <span class="chip-label">role-specific</span></div>
    <div class="feat-chip"><span class="icon">📘</span> Course Picks <span class="chip-label">Skill based</span></div>
    <div class="feat-chip"><span class="icon">🤖</span> AI Career Chat <span class="chip-label">gemini</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="upload-section-inner">
    <div class="upload-label">📂 Drop your resume here</div>
    <div class="upload-hint">Supports PDF and DOCX — analysis takes just a few seconds</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"],
    label_visibility="collapsed"
)

analyze_clicked = st.button("Analyze Resume ⚡")

if uploaded_file is not None:
    current_hash = get_file_hash(uploaded_file)

    if st.session_state.last_file_hash != current_hash:
        st.session_state.analysis_done = False
        st.session_state.analysis_result = None
        st.session_state.chat_response = ""
        st.session_state.last_file_hash = current_hash

    if analyze_clicked:
        try:
            with st.spinner("Analyzing your resume…"):
                result = run_resume_analysis(resume_file=uploaded_file)

            st.session_state.analysis_result = result
            st.session_state.analysis_done = True
            st.session_state.chat_response = ""

        except Exception as e:
            st.session_state.analysis_done = False
            st.session_state.analysis_result = None
            st.error(f"Error: {e}")

if st.session_state.analysis_done and st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result
    extracted_skills = result["extracted_skills"]
    matched_jobs = result["matched_jobs"]
    role_analysis = result["role_analysis"]

    st.success("✅ Resume analyzed successfully!")

    st.markdown(f"""
    <div class="sec-header anim">
        <div class="sec-icon sec-icon-mint">✨</div>
        <div class="sec-title">Extracted Skills</div>
        <div class="sec-count">{len(extracted_skills)} found</div>
    </div>
    """, unsafe_allow_html=True)

    if extracted_skills:
        colors = [BADGE_COLORS[i % len(BADGE_COLORS)] for i in range(len(extracted_skills))]
        badges = " ".join(
            f'<span class="skill-badge {colors[i]}">{s}</span>'
            for i, s in enumerate(extracted_skills)
        )
        st.markdown(f'<div class="skills-cloud anim anim-d1">{badges}</div>', unsafe_allow_html=True)
    else:
        st.warning("No skills detected from the resume.")

    render_match_cards(matched_jobs)

    st.markdown("""
    <div class="sec-header anim">
        <div class="sec-icon sec-icon-violet">📊</div>
        <div class="sec-title">Role-wise Skill Gap & Course Recommendations</div>
    </div>
    """, unsafe_allow_html=True)

    filtered_roles = role_analysis[:5]

    if filtered_roles:
        for idx, item in enumerate(filtered_roles, 1):
            with st.expander(f"#{idx}  {item['job_role']}  —  {item['match_score']}% match"):

                required_skills = item.get("required_skills", [])
                if isinstance(required_skills, list) and required_skills:
                    st.markdown('<div class="label-muted">Required Skills</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="skills-cloud">{skill_badges(required_skills, "badge-violet")}</div>',
                        unsafe_allow_html=True
                    )

                matched_skills = item.get("matched_skills", [])
                if matched_skills:
                    st.markdown('<div class="label-muted" style="margin-top:12px">✅ Matched Skills</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="skills-cloud">{skill_badges(matched_skills, "badge-mint")}</div>',
                        unsafe_allow_html=True
                    )

                if item.get("missing_skills"):
                    st.markdown('<div class="label-muted" style="margin-top:12px">❌ Missing Skills</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="skills-cloud">{skill_badges(item["missing_skills"], missing=True)}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.success("🎉 No missing skills for this role!")

                st.markdown('<div class="label-muted" style="margin-top:16px">📘 Recommended Courses</div>', unsafe_allow_html=True)
                if not item["recommended_courses"].empty:
                    courses_df = item["recommended_courses"][["skill", "course_name"]].copy()
                    courses_df.columns = ["Skill", "Course Name"]
                    courses_df.index = range(1, len(courses_df) + 1)
                    st.dataframe(courses_df, use_container_width=True)
                else:
                    st.info("No course recommendations available.")
    else:
        st.warning("No role analysis available.")

    st.markdown("""
    <div class="sec-header anim">
        <div class="sec-icon sec-icon-amber">🤖</div>
        <div class="sec-title">AI Career Guidance</div>
    </div>
    """, unsafe_allow_html=True)

    user_question = st.text_input(
        "Ask your career question",
        placeholder="e.g. Which role suits me best? What should I learn next?",
        label_visibility="collapsed"
    )

    ask_clicked = st.button("Ask AI ⚡", key="ask_ai_button")

    if ask_clicked:
        if not user_question.strip():
            st.warning("Please enter a question first.")
        else:
            try:
                with st.spinner("Generating answer…"):
                    chatbot_response = generate_chatbot_response(
                        user_question=user_question,
                        extracted_skills=extracted_skills,
                        role_analysis=filtered_roles
                    )

                st.session_state.chat_response = chatbot_response

            except Exception as e:
                st.session_state.chat_response = ""
                st.error(f"Chatbot error: {e}")

    if st.session_state.chat_response:
        st.markdown(f"""
        <div class="chat-avatar">🤖 ResumeAI</div>
        <div class="chat-response">{st.session_state.chat_response}</div>
        """, unsafe_allow_html=True)

elif uploaded_file is None:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 2rem; color: var(--text-muted);">
        <div style="font-size:3.5rem; margin-bottom:1rem; opacity:0.4;">⬆</div>
        <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:var(--text-primary); margin-bottom:6px;">
            Upload a resume to begin
        </div>
        <div style="font-size:0.88rem;">PDF or DOCX · Instant analysis · No signup required</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Built with <span>Streamlit</span> · <span>Gemini AI</span> · <span>CSV-based course recommendations</span>
</div>
""", unsafe_allow_html=True)