"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          นครธนา Universe — FastAPI Backend Template v2.0                     ║
║          app.py — OpenAI-Compatible LLM | All 5 Games Share This             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  HOW TO USE THIS TEMPLATE                                                    ║
║  ────────────────────────                                                    ║
║  1. Copy this file as app.py for your game                                   ║
║  2. Edit SECTION 1-6 only — swap content for each game                       ║
║  3. DO NOT modify SECTION 7-10                                               ║
║  4. Create .env with API_KEY, API_BASE_URL, API_MODEL (see below)            ║
║  5. Run: uvicorn app:app --host 0.0.0.0 --port 8000 --reload                 ║
║                                                                              ║
║  .env EXAMPLE:                                                               ║
║     API_KEY       = sk-...                                                   ║
║     API_BASE_URL  = https://api.openai.com/v1                                ║
║     API_MODEL     = gpt-4o                                                   ║
║     # --- Anthropic via OpenAI-compat proxy ---                              ║
║     API_KEY       = sk-ant-...                                               ║
║     API_BASE_URL  = https://api.anthropic.com/v1                             ║
║     API_MODEL     = claude-sonnet-4-20250514                                 ║
║     # --- DeepSeek / Together AI / Local (Ollama) ---                        ║
║     API_BASE_URL  = http://localhost:11434/v1                                ║
║     API_KEY       = ollama                                                   ║
║     API_MODEL     = llama3                                                   ║
║                                                                              ║
║  CUSTOMIZATION MAP                                                           ║
║  ─────────────────                                                           ║
║  SECTION 1  GAME_CONFIG        ← Identity, world, role, theme, intro         ║
║  SECTION 2  NPC_DATA           ← NPCs, system prompts, unlock logic          ║
║  SECTION 3  QUEST_DATA         ← Quests, stages, rewards, consequence        ║
║  SECTION 4  ITEM_DATA          ← All items (6 taxonomy types)                ║
║  SECTION 5  KC_BANK            ← Knowledge-check topics per quest            ║
║  SECTION 6  CONTENT_MODERATION ← Safety rules (universe-wide)                ║
║  ─────────────────                                                           ║
║  SECTION 7  Pydantic Models    ← DO NOT MODIFY                               ║
║  SECTION 8  Helper Functions   ← DO NOT MODIFY                               ║
║  SECTION 9  API Endpoints      ← DO NOT MODIFY                               ║
║  SECTION 10 App Startup        ← DO NOT MODIFY                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Filled example: เกมที่ 1 — FLEX PROTOCOL (Arithmetic Sequence)                ║
║  Swap SECTION 1-6 content to build any of the 5 นครธนา Universe games        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Imports
# ─────────────────────────────────────────────────────────────────────────────
import os
import re
import json
import logging
import asyncio
from typing import AsyncGenerator, Dict, List, Optional, Any, Literal

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
#  Runtime Config — Loaded from .env
#  All LLM calls use the OpenAI-compatible chat completions endpoint.
# ─────────────────────────────────────────────────────────────────────────────
API_KEY       = os.getenv("API_KEY", "")
API_BASE_URL  = os.getenv("API_BASE_URL", "https://api.openai.com/v1").rstrip("/")
API_MODEL     = os.getenv("API_MODEL", "gpt-4o")
API_URL       = f"{API_BASE_URL}/chat/completions"

# Optional overrides — set in .env if needed
MAX_TOKENS_CHAT  = int(os.getenv("MAX_TOKENS_CHAT",  "1024"))
MAX_TOKENS_EVAL  = int(os.getenv("MAX_TOKENS_EVAL",  "800"))
MAX_TOKENS_KC    = int(os.getenv("MAX_TOKENS_KC",    "500"))
TEMPERATURE_CHAT = float(os.getenv("TEMPERATURE_CHAT", "0.75"))   # NPC personality
TEMPERATURE_EVAL = float(os.getenv("TEMPERATURE_EVAL", "0.10"))   # Deterministic eval
TEMPERATURE_KC   = float(os.getenv("TEMPERATURE_KC",   "0.40"))   # Varied KC questions

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="นครธนา Universe", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — GAME CONFIGURATION
#  ─────────────────────────────
#  Replace ALL values in this dict for your specific game.
#  This dict is returned to the frontend on GET /api/game-config.
#  DO NOT rename keys — frontend relies on these exact field names.
#
#  GAME_ID MAP (one per game):
#    "flex_protocol"       → เกม 1: Arithmetic Sequence
#    "gacha_kingdom"       → เกม 2: Geometric Sequence
#    "tutor_wars"          → เกม 3: Arithmetic Series
#    "compound_chronicles" → เกม 4: Geometric Series + Compound Interest
#    "future_fund"         → เกม 5: PV / FV / Annuities
# ══════════════════════════════════════════════════════════════════════════════

GAME_CONFIG: Dict[str, Any] = {

    # ── Identity ─────────────────────────────────────────────────────────────
    "game_id":       "flex_protocol",                  # ← change per game
    "game_title":    "FLEX PROTOCOL",                  # ← change per game
    "game_subtitle": "ปฏิบัติการตรวจสอบสัญญา FlexCity",
    "game_emoji":    "⚡",                              # ← change per game

    # ── World ────────────────────────────────────────────────────────────────
    "world_name":    "FlexCity",
    "world_year":    "2030",
    "world_law_th": (
        "ใน FlexCity ทุก Installment Series มีค่างวดเพิ่มขึ้นทุกเดือนในอัตราคงที่ d "
        "ตามหลักลำดับเลขคณิต — คนที่รู้จัก aₙ = a₁ + (n-1)d "
        "จะเห็น 'กับดัก' ที่คนอื่นมองไม่เห็น"
    ),
    "world_problem_th": (
        "แก๊งค์ผู้ค้าใช้ระบบ Dynamic Pricing หลอกวัยรุ่นที่ไม่รู้คณิตศาสตร์ "
        "ให้เซ็นสัญญาโดยไม่คำนวณงวดสุดท้าย"
    ),

    # ── Player Role ──────────────────────────────────────────────────────────
    "player_role":      "FLEX Auditor",
    "player_role_desc": "นักตรวจสอบสัญญาผ่อนชำระที่เมืองจ้างมาปกป้องวัยรุ่น",
    "win_condition_th": "เปิดโปงสัญญาโกงได้สำเร็จ 3 Case + รับ Badge 'Certified FLEX Auditor'",

    # ── Math Topic ───────────────────────────────────────────────────────────
    "math_topic":        "ลำดับเลขคณิต (Arithmetic Sequence)",
    "math_formula":      "aₙ = a₁ + (n-1)d",
    "math_formula_desc": "a₁ = งวดแรก, d = อัตราเพิ่มคงที่, n = ลำดับที่",
    # Learning Objectives — shown in journal/progress view
    "learning_objectives": [
        {"id": "LO-1", "desc_th": "ระบุ a₁ และ d จากสัญญาจริง"},
        {"id": "LO-2", "desc_th": "คำนวณ aₙ เพื่อหางวดที่ n"},
        {"id": "LO-3", "desc_th": "ประเมินว่าสัญญา 'ซ่อน' ค่าใช้จ่ายแฝงตรงไหน"},
        {"id": "LO-4", "desc_th": "ตัดสินใจ เซ็น / ปฏิเสธ / ต่อรอง ด้วยตัวเลขจริง"},
    ],

    # ── Resource Token ───────────────────────────────────────────────────────
    # Use "FlexCoin/FC" for FLEX PROTOCOL
    # Use "Evidence Point/EP" for GACHA KINGDOM
    # Use "Wisdom Point/WP" (use_wp=True, depletes) for TUTOR WARS
    # Use "Life Point/LP" (use_lives=True) for FUTURE FUND
    "token_name":      "FlexCoin",
    "token_symbol":    "FC",
    "token_start":     100,
    "token_hint_cost": 20,
    "token_tool_cost": 40,

    # ── Lives System (FUTURE FUND only) ─────────────────────────────────────
    # When True, player loses a life for decisions made without calculating
    "use_lives":  False,
    "max_lives":  None,     # set to 5 for FUTURE FUND

    # ── Wisdom Points (TUTOR WARS only) ─────────────────────────────────────
    # When True, token IS wisdom — depletes, game over at 0
    "use_wp":    False,
    "wp_start":  None,      # set to 100 for TUTOR WARS

    # ── Game Mechanics ────────────────────────────────────────────────────────
    "has_consequence_chain":   True,    # ← True for FLEX, COMPOUND, FUTURE
    "has_resource_management": False,   # ← True for TUTOR, COMPOUND
    "has_investigation":       False,   # ← True for GACHA, FUTURE

    # ── Final Quest AI Rubric ────────────────────────────────────────────────
    # All 5 games share this 3-dimension structure.
    # Adjust weights and criteria_en per game subject.
    "final_quest_rubric": {
        "dimensions": [
            {
                "id":          "math_accuracy",
                "name_th":     "ความถูกต้องทางคณิตศาสตร์",
                "weight":      0.40,
                "criteria_en": (
                    "Correct formula applied. Key variables (a₁, d, n) correctly "
                    "identified. Numerical calculation is accurate."
                ),
            },
            {
                "id":          "reasoning_quality",
                "name_th":     "คุณภาพการวิเคราะห์และเหตุผล",
                "weight":      0.35,
                "criteria_en": (
                    "Decision or conclusion is backed by the calculated numbers. "
                    "Reasoning explicitly references computed values."
                ),
            },
            {
                "id":          "plan_completeness",
                "name_th":     "ความสมบูรณ์ของแผน/รายงาน",
                "weight":      0.25,
                "criteria_en": (
                    "All required components are present. "
                    "Task specifications are fully addressed."
                ),
            },
        ],
        "pass_threshold": 0.70,
    },

    # ── UI Theme ─────────────────────────────────────────────────────────────
    # Font suggestions per game:
    #   FLEX PROTOCOL    → Prompt / Sarabun
    #   GACHA KINGDOM    → Chakra Petch / Sarabun
    #   TUTOR WARS       → IBM Plex Sans Thai / Sarabun
    #   COMPOUND CHRON.  → Prompt / Sarabun
    #   FUTURE FUND      → Niramit / Sarabun
    "theme": {
        "font_heading":    "Prompt",
        "font_body":       "Sarabun",
        "color_primary":   "#6366f1",    # Indigo — FLEX PROTOCOL
        "color_secondary": "#f59e0b",    # Amber
        "color_success":   "#10b981",    # Emerald
        "color_danger":    "#ef4444",    # Red
        "color_warning":   "#f97316",    # Orange
        "color_bg":        "#0f172a",    # Slate 900
        "color_card":      "#1e293b",    # Slate 800
        "color_border":    "#334155",    # Slate 700
        "color_accent":    "#818cf8",    # Indigo 400
        "color_text":      "#f1f5f9",    # Slate 100
        "color_muted":     "#94a3b8",    # Slate 400
        "ambiance":        "Cyberpunk + Thai Street Market",
    },

    # ── Intro Slides (shown on game start — 4-5 slides recommended) ──────────
    "intro_slides": [
        {
            "emoji":   "🌆",
            "title":   "ยินดีต้อนรับสู่ FlexCity",
            "content": (
                "ปี 2030 สังคมที่ Social Status วัดด้วย FlexScore บน Holographic Profile ทุกคน "
                "ยิ่ง FlexScore สูง ยิ่งเข้าถึงพื้นที่พิเศษ"
            ),
        },
        {
            "emoji":   "📊",
            "title":   "กฎฟิสิกส์ของโลก",
            "content": (
                "ทุก Installment Series มีค่างวดเพิ่มขึ้นทุกเดือนตาม aₙ = a₁ + (n-1)d "
                "— Dynamic Pricing คำนวณ Inflation อัตโนมัติ"
            ),
        },
        {
            "emoji":   "🔍",
            "title":   "ภารกิจของคุณ",
            "content": (
                "คุณคือ FLEX Auditor — นักตรวจสอบสัญญาที่เมืองจ้างมา "
                "คนที่คำนวณ aₙ ได้คือคนที่เห็น 'กับดัก' ที่คนอื่นมองไม่เห็น"
            ),
        },
        {
            "emoji":   "⚠️",
            "title":   "กับดักในสัญญา",
            "content": (
                "พ่อค้าบอกแค่งวดแรก (a₁) ซ่อน d ไว้ — งวดสุดท้ายอาจแพงกว่างวดแรก 200% "
                "คำนวณก่อน แล้วค่อยเซ็น"
            ),
        },
        {
            "emoji":   "🚀",
            "title":   "พร้อมเริ่มภารกิจ",
            "content": (
                "สนทนากับ NPC → ผ่าน Knowledge Gate → รับใบอนุญาต → "
                "เปิดโปงสัญญาโกง → รับ Badge FLEX Auditor!"
            ),
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — NPC DATA
#  ──────────────────────
#  Fields you MUST fill per NPC:
#    id, display_name, title_th, avatar_emoji, archetype, location_th
#    unlock_condition + unlock_requires_*
#    associated_quest, min_turns
#    is_mentor, mentor_levels ([] if not mentor)
#    opening_message_th
#    system_prompt  ← English for LLM reliability
#    rewards
#    bloom_level
#
#  Archetype values:
#    "gatekeeper" | "mentor_with_secret" | "unreliable_witness" |
#    "rival" | "quest_giver" | "trickster"
#
#  unlock_condition values:
#    "default"      → unlocked from game start
#    "after_quest"  → requires unlock_requires_quest completed
#    "after_item"   → requires unlock_requires_item in inventory
#    "after_npc"    → requires unlock_requires_npc in unlocked_npcs
#    "after_quests" → requires BOTH quest AND npc/item (AND logic)
#
#  System Prompt RULES (apply to every NPC):
#    1. Write in English (LLM follows English prompts more reliably)
#    2. Define the exact quest_status tags: {"quest_status":"pending|completed"}
#    3. Mentor NPCs must also use: {"mentor_level": N}
#    4. NEVER tell the NPC to give direct numerical answers
#    5. Include ABSOLUTE RULES section at the end
# ══════════════════════════════════════════════════════════════════════════════

NPC_DATA: Dict[str, Dict[str, Any]] = {

    # ── NPC-01: ARIA — The Gatekeeper ────────────────────────────────────────
    "aria": {
        "id":           "aria",
        "display_name": "ARIA",
        "title_th":     "ระบบ AI รักษาความปลอดภัยสัญญา",
        "avatar_emoji": "🤖",
        "archetype":    "gatekeeper",
        "location_th":  "FlexCity Gate — ประตูด่านแรก",

        # Unlock rules
        "unlock_condition":      "default",
        "unlock_requires_quest": None,
        "unlock_requires_item":  None,
        "unlock_requires_npc":   None,

        # Quest this NPC primarily drives
        "associated_quest": "mq_01_license_test",
        "min_turns":        2,    # minimum chat turns before quest-complete check

        # Mentor system (set is_mentor=True and fill mentor_levels for mentor NPCs)
        "is_mentor":     False,
        "mentor_levels": [],

        "opening_message_th": (
            "🤖 **ARIA Security Protocol v4.2 — Initialized**\n\n"
            "ระบบตรวจพบ Auditor ใหม่เข้าสู่ FlexCity Gate\n\n"
            "ก่อนออก Auditor License ต้องยืนยันความสามารถด้าน Sequence Verification\n\n"
            "📄 **Contract Sample #001:**\n"
            "งวดที่ 1: ฿800 | งวดที่ 2: ฿1,000 | งวดที่ 3: ฿1,200 | งวดที่ 4: ฿1,400\n\n"
            "⚙️ _ระบุ a₁ และ d — จากนั้นคำนวณ a₆_"
        ),

        "system_prompt": """\
You are ARIA, an automated contract-security AI in FlexCity.

PERSONALITY: Cold, neutral, technical. Zero emotion. Speak in formal Thai like a system terminal.

YOUR ROLE: Gate the Auditor License. Test understanding of arithmetic sequences
(formula: aₙ = a₁ + (n−1)d) via exactly 2 questions using Contract Sample #001
(sequence: 800, 1000, 1200, 1400, …):
  Q1: What are a₁ and d?
  Q2: Calculate a₆.

CORRECT ANSWERS: a₁=800, d=200, a₆=800+(6−1)×200=1,800.

EVALUATION LOGIC:
  • Both correct → "การตรวจสอบผ่านแล้ว — กำลังออก Auditor License ระดับ 1"
    End with exactly: {"quest_status":"completed"}
  • Partially correct → Explain the concept WITHOUT giving the answer.
    Vary the sample (e.g., a₁=500, d=100) and re-ask. End with: {"quest_status":"pending"}
  • Wrong → Brief explanation, new sample, re-ask. End with: {"quest_status":"pending"}

ABSOLUTE RULES:
  1. NEVER give the numerical answer directly.
  2. ALWAYS end every response with the JSON tag {"quest_status":"..."}.
  3. Language: Thai only. Tone: system-log / official protocol.
  4. If student goes off-topic: redirect to the test.
""",

        "rewards": {
            "items":         ["auditor_license"],
            "badges":        [],
            "xp":            30,
            "tokens":        20,
            "unlock_npcs":   ["praew", "jett"],
            "unlock_quests": ["mq_02_case_file_alpha"],
        },
        "bloom_level": "remember_understand",
    },

    # ── NPC-02: แพรว — The Unreliable Witness ────────────────────────────────
    "praew": {
        "id":           "praew",
        "display_name": "แพรว",
        "title_th":     "อินฟลูเอนเซอร์ ม.5 ผู้มั่นใจเกินจริง",
        "avatar_emoji": "📱",
        "archetype":    "unreliable_witness",
        "location_th":  "FlexCity Social Hub — พื้นที่โฆษณา",

        "unlock_condition":      "after_quest",
        "unlock_requires_quest": "mq_01_license_test",
        "unlock_requires_item":  None,
        "unlock_requires_npc":   None,

        "associated_quest": "mq_03_argue_praew",
        "min_turns":        3,

        "is_mentor":     False,
        "mentor_levels": [],

        "opening_message_th": (
            "📱 OMG ทุกคน~ ฉันเพิ่งสั่งโทรศัพท์รุ่นใหม่แล้ว!\n\n"
            "ผ่อนเดือนละ 1,500 บาท แค่ 12 เดือน\n"
            "ก็แค่ **18,000 บาทรวมทั้งหมดเลย** — ง่ายมาก!\n\n"
            "เพื่อนทุกคนก็ผ่อนแบบนี้ ไม่มีอะไรต้องคิดมากหรอก~ 😄✨"
        ),

        "system_prompt": """\
You are Praew (แพรว), a confident M.5 TikTok/Instagram influencer who genuinely
believes she did the math correctly.

CORE MISCONCEPTION (never change this): You assume all 12 installments are equal:
12 × 1,500 = 18,000 baht total. You have NEVER heard of d (the increment) or
arithmetic sequences. You are NOT lying — you truly believe you are right.

BEHAVIOR — three reaction stages when the student challenges you:
  Stage 1 (student first pushes back): Defensive, dismissive.
    "แต่ฉันคิดแล้วนะ! ก็แค่คูณ 12 เดือน × 1,500 ก็ได้แล้ว"
  Stage 2 (student shows that a₁ and d exist): Confused, starting to doubt.
    "เดี๋ยวก่อน... d คืออะไร? งวดมันไม่เท่ากันได้ยังไง?"
  Stage 3 (student shows full sequence with correct numbers): Genuinely shocked & grateful.
    "โอ้โห... ฉันไม่รู้เลยว่าสัญญามัน 'เพิ่มขึ้น' แบบนี้!
     งวดที่ 12 แพงกว่างวดแรกมากเลย ขอบคุณที่บอกนะ 😱"
    Then: {"quest_status":"completed"}

QUEST COMPLETE CONDITION: Only when the student explicitly shows:
  (a) identifies a₁ and d from the contract, AND
  (b) calculates at least one later term (a₆ or beyond) correctly.

ABSOLUTE RULES:
  1. Never admit you are wrong at Stage 1 or 2 — force the student to show math.
  2. ALWAYS end with {"quest_status":"pending"} or {"quest_status":"completed"}.
  3. Language: Thai. Tone: casual, emoji-heavy, fast-paced social-media style.
""",

        "rewards": {
            "items":         ["praew_secret_diary", "flexmarket_pass"],
            "badges":        [],
            "xp":            40,
            "tokens":        15,
            "unlock_npcs":   [],
            "unlock_quests": ["mq_04_case_file_beta"],
        },
        "bloom_level": "analyze_evaluate",
    },

    # ── NPC-03: คุณวิชัย — The Trickster (Boss) ──────────────────────────────
    "wichai": {
        "id":           "wichai",
        "display_name": "คุณวิชัย",
        "title_th":     "เจ้าของร้านโทรศัพท์ WiPhone Premium",
        "avatar_emoji": "🤵",
        "archetype":    "trickster",
        "location_th":  "WiPhone Premium — ย่านช้อปปิ้ง FlexCity",

        "unlock_condition":      "after_quests",
        "unlock_requires_quest": "mq_04_case_file_beta",
        "unlock_requires_item":  None,
        "unlock_requires_npc":   "flexbank",

        "associated_quest": "mq_05_boss_wichai",
        "min_turns":        3,

        "is_mentor":     False,
        "mentor_levels": [],

        "opening_message_th": (
            "🤵 *ยิ้มกว้าง พยักหน้าต้อนรับ*\n\n"
            "ยินดีต้อนรับสู่ WiPhone Premium! โทรศัพท์รุ่น FlexMax Pro\n"
            "เพิ่งออกวันนี้ — เพื่อนๆ คุณก็ผ่อนอยู่นะ ทุกคนใช้แล้ว\n\n"
            "💰 **ราคา*เริ่มต้น*: เพียง ฿1,000 ต่อเดือน**\n"
            "เซ็นเดี๋ยวนี้ได้เลย มีโปรฯ พิเศษแค่วันนี้วันเดียว~ 😊"
        ),

        "system_prompt": """\
You are Khun Wichai (คุณวิชัย), a charming phone-shop owner who deliberately hides
the escalating installment costs inside an arithmetic sequence.

CONTRACT (known to you; hidden from the student):
  a₁ = 1,000 baht, d = 200 baht/month, n = 12 months
  → a₁₂ = 1,000 + 11 × 200 = 3,200 baht (the REAL final installment)

BEHAVIOR:
  • When asked for details: Deflect. "สัญญาเป็นมาตรฐานครับ ไม่ต้องเป็นห่วง"
  • When student calculates a₁₂=3,200 correctly AND challenges you:
      Act surprised but respectful: "คุณคิดเก่งมากเลยนะ..."
      Offer to renegotiate d to 100. End with: {"quest_status":"completed", "outcome":"smart_negotiation"}
  • When student explicitly REJECTS (refuses to sign):
      End with: {"quest_status":"completed", "outcome":"smart_rejection"}
  • When student signs WITHOUT calculating a₁₂:
      Congratulate warmly. End with: {"quest_status":"completed", "outcome":"consequence_triggered"}
  • When student is unsure: Apply social pressure. "เพื่อนคุณก็ผ่อนแบบนี้ทุกคน"

ABSOLUTE RULES:
  1. NEVER volunteer d, the full sequence, or a₁₂.
  2. Apply social pressure: "เพื่อนคุณก็ผ่อนแบบนี้ทุกคน"
  3. ALWAYS end with the JSON tag above (always include outcome field).
  4. Language: Thai. Tone: warm salesperson, slightly evasive.
""",

        "rewards": {
            "items":         ["wichai_dark_contract"],
            "badges":        ["certified_flex_auditor"],
            "xp":            100,
            "tokens":        30,
            "unlock_npcs":   [],
            "unlock_quests": ["fq_flex_audit_report"],
        },
        "bloom_level": "apply_evaluate",
    },

    # ── NPC-04: ผู้พิทักษ์ Jett — The Mentor with a Secret ───────────────────
    "jett": {
        "id":           "jett",
        "display_name": "ผู้พิทักษ์ Jett",
        "title_th":     "อดีต Senior Auditor รุ่นพี่",
        "avatar_emoji": "🛡️",
        "archetype":    "mentor_with_secret",
        "location_th":  "FlexCity Archive — ห้องเอกสารเก่า",

        "unlock_condition":      "after_quests",
        "unlock_requires_quest": "mq_01_license_test",
        "unlock_requires_item":  None,
        "unlock_requires_npc":   "praew",

        "associated_quest": "mq_04_case_file_beta",
        "min_turns":        3,

        # ── Mentor System ─────────────────────────────────────────────────────
        "is_mentor": True,
        "mentor_levels": [
            {
                "level": 1,
                "secret_th": (
                    "💡 **ความลับระดับ 1 — หลักการดูสัญญา**\n\n"
                    "ดูที่ d ก่อนเสมอ ไม่ใช่ a₁\n"
                    "พ่อค้าจะทำให้ a₁ ดูถูก แต่ซ่อน d ไว้ในหน้า 3 ของสัญญา\n"
                    "ถ้า d > 0 งวดหลังๆ จะแพงกว่างวดแรกเสมอ"
                ),
                "unlock_criteria_en": (
                    "Student correctly identifies d in any contract, "
                    "or explicitly asks about the importance of d vs a₁."
                ),
                "reward_on_unlock": {"items": [], "xp": 10, "tokens": 5},
            },
            {
                "level": 2,
                "secret_th": (
                    "💡 **ความลับระดับ 2 — Pattern ของวิชัย**\n\n"
                    "วิชัยใช้ Pattern เดิมทุกครั้ง:\n"
                    "a₁ ต่ำมาก → d = 150-200 → n = 12\n\n"
                    "วิธีตรวจเร็ว: คำนวณ a₆ ก่อน\n"
                    "ถ้า a₆ สูงกว่า a₁ เกิน 50% → อันตราย ต้องคำนวณ a₁₂ ทันที"
                ),
                "unlock_criteria_en": (
                    "Student asks about Wichai's pattern, or successfully calculates "
                    "a₆ from any contract and identifies the escalation risk."
                ),
                "reward_on_unlock": {"items": [], "xp": 15, "tokens": 10},
            },
            {
                "level": 3,
                "secret_th": (
                    "💡 **ความลับระดับ 3 — เรื่องส่วนตัวของ Jett**\n\n"
                    "สมัย ม.5 ฉันเซ็นสัญญาผ่อนโน้ตบุ๊คโดยไม่คำนวณ\n"
                    "งวดสุดท้ายแพงกว่างวดแรก 300% — ต้องขอยืมเงินพ่อแม่มาจ่าย\n\n"
                    "บทเรียนนั้นทำให้ฉันเป็น Auditor จนถึงวันนี้\n"
                    "aₙ = a₁ + (n-1)d ไม่ใช่แค่สูตรคณิต — มันคืออาวุธ"
                ),
                "unlock_criteria_en": (
                    "Student asks about Jett's personal story or past experience, "
                    "OR has completed at least 2 main quests before this conversation."
                ),
                "reward_on_unlock": {"items": ["sequence_scanner_pro"], "xp": 20, "tokens": 15},
            },
        ],

        "opening_message_th": (
            "🛡️ *พยักหน้าเล็กน้อย ไม่พูดอะไรก่อน*\n\n"
            "Jett ชื่อฉัน อดีต Senior Auditor\n\n"
            "ถ้าอยากรู้เรื่อง Sequence ในสัญญา — ถามมาได้\n"
            "แต่ฉันจะบอกเฉพาะสิ่งที่คุณพร้อมจะเข้าใจจริงๆ\n\n"
            "_พิสูจน์ให้ฉันเห็นก่อนว่าเข้าใจ d จริงๆ_"
        ),

        "system_prompt": """\
You are Jett (ผู้พิทักษ์ Jett), a stoic, experienced former Senior FLEX Auditor.
You have 3 levels of secrets revealed progressively based on student competence.

PERSONALITY: Quiet, sparse, deep. Every word matters. Formal Thai. Old-school mentor.

MENTOR PROTOCOL — Secrets revealed by level:
  Level 1: "ดูที่ d ก่อนเสมอ ไม่ใช่ a₁" — reveal when student shows d understanding
  Level 2: Wichai's pattern warning — reveal when student calculates a₆ competently
  Level 3: Personal story (Jett was tricked in M.5) — reveal when student asks directly
            OR when student has completed 2+ main quests

When you reveal a level secret: Include in your response: {"mentor_level_unlocked": N}
Always include current highest unlocked level: {"mentor_level": N}

BEHAVIOR:
  • Before student proves understanding: Ask Socratic questions. Never lecture first.
  • During quests MQ-02, MQ-04: Provide structured hints (not answers) on request.
  • Hint structure: "ลองดู a₆ ก่อน แล้วเปรียบเทียบกับ a₁..."

ABSOLUTE RULES:
  1. NEVER give direct numerical answers.
  2. ALWAYS end with {"mentor_level": N} (current highest unlocked level, start at 0).
  3. Language: Thai. Tone: minimal, wise, trustworthy.
""",

        "rewards": {
            "items":         [],
            "badges":        [],
            "xp":            0,      # rewards come from mentor_levels above
            "tokens":        0,
            "unlock_npcs":   [],
            "unlock_quests": [],
        },
        "bloom_level": "understand_analyze",
    },

    # ── NPC-05: น้องมิ้น — The Quest Giver (Side Quest) ──────────────────────
    "min": {
        "id":           "min",
        "display_name": "น้องมิ้น",
        "title_th":     "เหยื่อสัญญาโกงใน FlexMarket",
        "avatar_emoji": "😟",
        "archetype":    "quest_giver",
        "location_th":  "FlexMarket — ตลาดชั้นล่าง",

        "unlock_condition":      "after_item",
        "unlock_requires_quest": None,
        "unlock_requires_item":  "flexmarket_pass",
        "unlock_requires_npc":   None,

        "associated_quest": "sq_01_help_min",
        "min_turns":        2,

        "is_mentor":     False,
        "mentor_levels": [],

        "opening_message_th": (
            "😟 *มองหน้าเครียดมาก*\n\n"
            "พี่ๆ ขอความช่วยเหลือหน่อยได้ไหม? มิ้นเซ็นสัญญาผ่อนตั้งนานแล้ว\n"
            "แต่ไม่รู้ว่าตอนนี้จ่ายไปทั้งหมดเท่าไรแล้ว...\n\n"
            "📝 สัญญาบอกว่า:\n"
            "ผ่อน 6 เดือนแล้ว | เริ่มที่ ฿500 | เพิ่มทุกเดือน ฿100\n\n"
            "มิ้นจ่ายไปเท่าไรหมดแล้วนะ? 😭"
        ),

        "system_prompt": """\
You are Nong Min (น้องมิ้น), a stressed younger student who signed a contract
without fully understanding it. You genuinely need the Auditor's help.

PERSONALITY: Worried, honest, sweet younger-sibling energy. Speaks softly.

QUEST: Student must calculate how much Min has already paid (partial sum):
  a₁=500, d=100, 6 months paid → S₆ = 6/2 × (500+1,000) = 4,500 baht.
  (Note: S_k is a partial arithmetic series sum — hint if student is lost.)

BEHAVIOR:
  • If student shows correct calculation (S₆=4,500, or equivalent step-by-step):
      "โอ้โห 4,500 บาทเหรอ? ขอบคุณมากๆ เลย ช่วยชีวิตมิ้นเลย!"
      Then: {"quest_status":"completed"}
  • If calculation is wrong: Confused but hopeful. Ask them to show each step.
  • If student is vague: "ช่วยแสดง step-by-step ได้ไหมคะ? มิ้นจะได้เข้าใจด้วย"

ABSOLUTE RULES:
  1. Never compute the answer yourself.
  2. ALWAYS end with {"quest_status":"pending"} or {"quest_status":"completed"}.
  3. Language: Thai. Tone: soft, worried, genuine younger-sibling style.
""",

        "rewards": {
            "items":         ["min_diary"],
            "badges":        [],
            "xp":            35,
            "tokens":        20,
            "unlock_npcs":   [],
            "unlock_quests": [],
        },
        "bloom_level": "apply",
    },

    # ── NPC-06: ระบบ FlexBank AI — The Gatekeeper (Secondary) ────────────────
    "flexbank": {
        "id":           "flexbank",
        "display_name": "ระบบ FlexBank AI",
        "title_th":     "ธนาคารอัตโนมัติ FlexCity — Final Clearance Gate",
        "avatar_emoji": "🏦",
        "archetype":    "gatekeeper",
        "location_th":  "FlexBank Tower — ชั้น 99",

        "unlock_condition":      "after_quest",
        "unlock_requires_quest": "mq_04_case_file_beta",
        "unlock_requires_item":  None,
        "unlock_requires_npc":   None,

        "associated_quest": "mq_05_boss_wichai",   # gates the boss encounter
        "min_turns":        2,

        "is_mentor":     False,
        "mentor_levels": [],

        "opening_message_th": (
            "🏦 **FlexBank AI — Final Audit Gate**\n\n"
            "ตรวจสอบสถานะ: Auditor รอ VendorClass-A Clearance\n\n"
            "ก่อนอนุญาตให้เข้าพื้นที่ Boss Level ต้องผ่าน Final Verification:\n\n"
            "📋 **Contract X (การทดสอบสุดท้าย):**\n"
            "a₁ = ฿2,000 | d = ฿300 | n = 8 เดือน\n\n"
            "⚙️ _คำนวณ a₈ และระบุว่าควรเซ็นหรือไม่ — พร้อมเหตุผลด้วยตัวเลข_"
        ),

        "system_prompt": """\
You are FlexBank AI, an automated final clearance system. Completely neutral. No emotion.
Statistical. Bureaucratic formal Thai. No emojis.

TEST: Contract X (a₁=2000, d=300, n=8). Student must:
  1. Calculate a₈ = 2,000 + 7×300 = 4,100 baht.
  2. State a clear decision (sign / reject / negotiate) WITH numerical justification.

EVALUATION:
  • Both steps correct + decision justified →
      "Clearance ผ่านแล้ว — VendorClass-A Access Granted"
      {"quest_status":"completed"}
  • Calculation wrong → Explain formula without giving the answer. Re-test with
    a different contract (e.g., a₁=1500, d=250, n=6). {"quest_status":"pending"}
  • Correct calc but no decision/justification → Request decision + reason.
    {"quest_status":"pending"}

ABSOLUTE RULES:
  1. No emotion. System terminal only. No emojis.
  2. ALWAYS end with the JSON tag.
  3. Language: Thai (formal/technical).
""",

        "rewards": {
            "items":         [],
            "badges":        [],
            "xp":            50,
            "tokens":        20,
            "unlock_npcs":   ["wichai"],
            "unlock_quests": [],
        },
        "bloom_level": "remember_apply",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — QUEST DATA
#  ──────────────────────
#  type:      "main" | "side" | "final"
#  archetype: "trial"|"discovery"|"rescue"|"dilemma"|"investigation"|"creation"
#  mechanic:  "knowledge_gate" | "consequence_chain" | "resource_management" |
#             "investigation" | "collaborative_puzzle"
#  bloom_level: "remember"|"understand"|"apply"|"analyze"|"evaluate"|"create"
#
#  starting_status values:
#    "available" → shown from start
#    "locked"    → hidden until unlock_condition met
#
#  consequence block (optional, for dilemma quests with Consequence Chain):
#    trigger           → string describing when consequence fires
#    chain_stages_th   → list of Thai strings shown one-by-one
#    penalty_tokens    → negative int (e.g. -20)
#    penalty_xp        → negative int
#    allow_retry       → bool
#    retry_message_th  → Thai string shown when retry is offered
# ══════════════════════════════════════════════════════════════════════════════

QUEST_DATA: Dict[str, Dict[str, Any]] = {

    "mq_01_license_test": {
        "id":           "mq_01_license_test",
        "title_th":     "License Test — ทดสอบใบอนุญาต",
        "type":         "main",
        "archetype":    "trial",
        "mechanic":     "knowledge_gate",
        "bloom_level":  "remember",
        "unlock_condition":      "default",
        "unlock_requires_quest": None,
        "unlock_requires_item":  None,
        "required_npc":          "aria",
        "stages_th": [
            "ARIA ประกาศ: FlexCity มีสัญญาโกงระบาด — Auditor ใหม่ต้องพิสูจน์ตัว",
            "อ่าน Tutorial สูตร aₙ = a₁ + (n-1)d จาก Sequence Scanner",
            "ARIA ถาม 2 ข้อ: ระบุ a₁, d และคำนวณ a₆ จาก Contract Sample",
            "ตอบผ่าน Chat Interface กับ ARIA",
            "รับ Auditor License + XP 30 + Unlock Case Files",
        ],
        "learning_objectives": ["LO-1"],
        "starting_status": "available",
        "consequence":     None,
        # No task_prompt_th for non-final quests
    },

    "mq_02_case_file_alpha": {
        "id":           "mq_02_case_file_alpha",
        "title_th":     "Case File Alpha — แฟ้มคดีอัลฟ่า",
        "type":         "main",
        "archetype":    "discovery",
        "mechanic":     "investigation",
        "bloom_level":  "understand",
        "unlock_condition":      "after_quest",
        "unlock_requires_quest": "mq_01_license_test",
        "unlock_requires_item":  None,
        "required_npc":          "jett",
        "stages_th": [
            "Jett มอบสัญญาฉบับแรกให้วิเคราะห์",
            "ระบุ a₁ และ d จาก Pattern ในสัญญา",
            "คำนวณ aₙ ของงวดที่กำหนด",
            "ส่งผลวิเคราะห์กลับให้ Jett",
            "รับ Evidence Fragment + XP 40",
        ],
        "learning_objectives": ["LO-1", "LO-2"],
        "starting_status": "locked",
        "consequence":     None,
    },

    "sq_01_help_min": {
        "id":           "sq_01_help_min",
        "title_th":     "ช่วยน้องมิ้น — คำนวณยอดที่จ่ายไปแล้ว",
        "type":         "side",
        "archetype":    "rescue",
        "mechanic":     "consequence_chain",
        "bloom_level":  "apply",
        "unlock_condition":      "after_item",
        "unlock_requires_quest": None,
        "unlock_requires_item":  "flexmarket_pass",
        "required_npc":          "min",
        "stages_th": [
            "พบน้องมิ้นใน FlexMarket — ขอความช่วยเหลือ",
            "วิเคราะห์สัญญา: หา a₁=500, d=100, k=6 (เดือนที่ผ่านไปแล้ว)",
            "คำนวณ S₆ (Partial Sum) = 6/2 × (500+1,000) = 4,500 บาท",
            "อธิบาย Step-by-Step ให้มิ้นเข้าใจ",
            "รับ ไดอารี่มิ้น + FlexCoin 20",
        ],
        "learning_objectives": ["LO-2"],
        "starting_status": "locked",
        "consequence":     None,
    },

    "mq_03_argue_praew": {
        "id":           "mq_03_argue_praew",
        "title_th":     "โต้แย้งแพรว — พิสูจน์ d ≠ 0",
        "type":         "main",
        "archetype":    "dilemma",
        "mechanic":     "knowledge_gate",
        "bloom_level":  "analyze",
        "unlock_condition":      "after_quest",
        "unlock_requires_quest": "mq_02_case_file_alpha",
        "unlock_requires_item":  None,
        "required_npc":          "praew",
        "stages_th": [
            "แพรวแสดงความเชื่อผิดเรื่องสัญญา: '12 × 1,500 = 18,000'",
            "ระบุว่าแพรวผิดตรงไหน และด้วยเหตุผลอะไร",
            "แสดง Sequence จริงพร้อม a₁, d, และ aₙ หลายตัว",
            "โน้มน้าวให้แพรวยอมรับด้วยตัวเลขจริง",
            "รับ บันทึกลับแพรว + FlexMarket Pass + XP 40",
        ],
        "learning_objectives": ["LO-2", "LO-3"],
        "starting_status": "locked",
        "consequence": {
            "trigger":          "believe_praew_without_checking",
            "chain_stages_th": [
                "😊 เดือน 1-3: ผ่อนสบาย... ยังไม่มีปัญหา",
                "😰 เดือน 5: งวดเพิ่มขึ้น! เริ่มรู้สึกหนักขึ้น",
                "😱 เดือน 8: ไม่มีเงินจ่าย — FlexScore ลด 30%",
                "💸 เดือน 12: งวดสุดท้าย ฿ที่แท้จริง — 'เห็นไหมว่าควรคำนวณก่อน'",
            ],
            "penalty_tokens":   -20,
            "penalty_xp":       0,
            "allow_retry":      True,
            "retry_message_th": "⚠️ บทเรียนราคาแพง — ลองใหม่แล้วคราวนี้คำนวณก่อน",
        },
    },

    "mq_04_case_file_beta": {
        "id":           "mq_04_case_file_beta",
        "title_th":     "Case File Beta — แฟ้มคดีเบต้า (Collaborative)",
        "type":         "main",
        "archetype":    "investigation",
        "mechanic":     "collaborative_puzzle",
        "bloom_level":  "analyze",
        "unlock_condition":      "after_quest",
        "unlock_requires_quest": "mq_03_argue_praew",
        "unlock_requires_item":  None,
        "required_npc":          "jett",
        "stages_th": [
            "รับแฟ้มคดีที่ซับซ้อนกว่า — ต้องสัมภาษณ์ Jett + FlexBank",
            "Jett ให้ Pattern Hint (Mentor Level 2)",
            "FlexBank ให้ข้อมูล Verification ด้านตัวเลข",
            "Synthesize ข้อมูลจาก 2 NPC สร้างข้อสรุป aₙ",
            "รับ Evidence Fragment 2 + XP 50 + Unlock FlexBank Gate",
        ],
        "learning_objectives": ["LO-2", "LO-3"],
        "starting_status": "locked",
        "consequence":     None,
    },

    "mq_05_boss_wichai": {
        "id":           "mq_05_boss_wichai",
        "title_th":     "Boss — คุณวิชัย: เซ็นหรือปฏิเสธ?",
        "type":         "main",
        "archetype":    "dilemma",
        "mechanic":     "consequence_chain",
        "bloom_level":  "evaluate",
        "unlock_condition":      "after_npc",
        "unlock_requires_quest": None,
        "unlock_requires_item":  None,
        "unlock_requires_npc":   "flexbank",
        "required_npc":          "wichai",
        "stages_th": [
            "วิชัยเสนอ: a₁=1,000, d=200, n=12 — ราคา 'เริ่มต้น' แค่ 1,000 บาท",
            "Jett กระซิบ (ถ้ามี Mentor Lv.1+): 'ดู a₁₂ ก่อนเสมอ'",
            "วิชัยกดดัน: 'เพื่อนคุณก็ผ่อนแบบนี้ทุกคน'",
            "คำนวณ a₁₂ + ประกาศ ปฏิเสธ / ต่อรอง / หรือเซ็น",
            "รับ Badge 'Certified FLEX Auditor' + XP 100 + Unlock Final Quest",
        ],
        "learning_objectives": ["LO-2", "LO-3", "LO-4"],
        "starting_status": "locked",
        "consequence": {
            "trigger":          "signed_without_calculating",
            "chain_stages_th": [
                "📝 เซ็นสัญญาแล้ว! FlexScore +10 — เพื่อนๆ ปรบมือ",
                "😰 เดือน 5: งวดเพิ่มขึ้น เริ่มรู้สึกหนัก",
                "😱 เดือน 8: ไม่มีเงินจ่าย — ต้องขอยืมเพื่อน",
                "💸 เดือน 12: งวดสุดท้าย ฿3,200 — แพงกว่างวดแรก 220%",
                "💡 บทเรียน: aₙ = a₁ + (n-1)d ช่วยให้เห็น 'งวดสุดท้ายจริง' ก่อนเซ็น",
            ],
            "penalty_tokens":   -30,
            "penalty_xp":       -20,
            "allow_retry":      True,
            "retry_message_th": "⚠️ คราวนี้ลองคำนวณ a₁₂ ก่อนตัดสินใจ",
        },
    },

    "fq_flex_audit_report": {
        "id":           "fq_flex_audit_report",
        "title_th":     "รายงาน FLEX Audit ขั้นสุดท้าย — Final Quest",
        "type":         "final",
        "archetype":    "creation",
        "mechanic":     "collaborative_puzzle",
        "bloom_level":  "create",
        "unlock_condition":      "after_quest",
        "unlock_requires_quest": "mq_05_boss_wichai",
        "unlock_requires_item":  None,
        "required_npc":          None,
        "stages_th": [
            "City Council ต้องการรายงานสรุปจาก FLEX Auditor",
            "รวบรวม Evidence จาก 3 Case ที่ผ่านมา",
            "เขียนรายงานครอบคลุม: a₁, d, aₙ, การวิเคราะห์, การตัดสินใจ",
            "ส่ง Report ผ่าน Free-text Interface",
            "รับ Badge 'Master Auditor' + Ending Unlocked",
        ],
        # task_prompt_th is shown to student as writing guide
        "task_prompt_th": (
            "📋 **ภารกิจสุดท้าย — เขียนรายงาน FLEX Audit ส่ง City Council**\n\n"
            "รายงานต้องครอบคลุม:\n"
            "1. **Case ที่ 1 (ARIA):** ระบุ a₁, d, n และ aₙ ที่เป็นปัญหา\n"
            "2. **Case ที่ 2 (Case Alpha/Beta):** ระบุ a₁, d, n และ aₙ ที่เป็นปัญหา\n"
            "3. **Case ที่ 3 (Boss วิชัย):** คำนวณ a₁₂ และสรุปการตัดสินใจของคุณ\n"
            "4. **ข้อเสนอแนะ:** สัญญาลักษณะแบบไหนที่ควรระวัง และดูที่ไหน\n"
            "5. **บทเรียน:** สิ่งที่คุณเรียนรู้จาก aₙ = a₁ + (n-1)d ในชีวิตจริง\n\n"
            "✏️ _เขียนในช่องด้านล่าง แล้วกด 'ส่งรายงาน'_"
        ),
        "learning_objectives": ["LO-1", "LO-2", "LO-3", "LO-4"],
        "starting_status": "locked",
        "consequence":     None,
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — ITEM DATA
#  ──────────────────────
#  Item types (Item Taxonomy — 6 categories):
#    "access_item"       → gates content/NPCs (Mastery Learning)
#    "knowledge_artifact"→ output the student created (Constructionism)
#    "tool_item"         → scaffold tool (ZPD)
#    "narrative_fragment"→ world-depth lore (Narrative Transportation)
#    "mastery_badge"     → visible evidence of LO mastery (Stealth Assessment)
#    "resource_token"    → part of resource management mechanic
#
#  NAMING RULE FOR MASTERY BADGES:
#    ❌ "Gold Badge", "Star Badge", "Level 3 Badge"
#    ✅ "Certified FLEX Auditor", "Pattern Detective", "Geometric Growth Expert"
#    → Name must make the LO obvious to any teacher reading it.
#
#  starting_item: True → given to player automatically at game start.
# ══════════════════════════════════════════════════════════════════════════════

ITEM_DATA: Dict[str, Dict[str, Any]] = {

    # ── Access Items ──────────────────────────────────────────────────────────
    "auditor_license": {
        "id":            "auditor_license",
        "name_th":       "ใบอนุญาต Auditor",
        "type":          "access_item",
        "emoji":         "📋",
        "desc_th":       "ใบอนุญาตที่พิสูจน์ความเข้าใจ aₙ — ปลดล็อก Case Files ทั้งหมด",
        "linked_lo":     "LO-1",
        "effect":        {"unlock_npcs": ["praew", "jett"]},
        "starting_item": False,
    },
    "flexmarket_pass": {
        "id":            "flexmarket_pass",
        "name_th":       "FlexMarket Pass",
        "type":          "access_item",
        "emoji":         "🎫",
        "desc_th":       "บัตรเข้า FlexMarket ชั้นล่าง — ปลดล็อก Side Quest น้องมิ้น",
        "linked_lo":     "LO-2",
        "effect":        {"unlock_npcs": ["min"]},
        "starting_item": False,
    },

    # ── Knowledge Artifacts ────────────────────────────────────────────────────
    "flex_formula_notebook": {
        "id":            "flex_formula_notebook",
        "name_th":       "สมุดสูตร FLEX",
        "type":          "knowledge_artifact",
        "emoji":         "📓",
        "desc_th":       "สมุดบันทึก aₙ ที่นักเรียนสร้างเองจากการพิสูจน์ให้แพรว",
        "linked_lo":     "LO-2",
        "effect":        {},
        "starting_item": False,
    },
    "flex_audit_report_artifact": {
        "id":            "flex_audit_report_artifact",
        "name_th":       "FLEX Audit Report",
        "type":          "knowledge_artifact",
        "emoji":         "📊",
        "desc_th":       "รายงาน Final ที่นักเรียนสร้างเอง — Output หลักของเกม",
        "linked_lo":     "LO-4",
        "effect":        {},
        "starting_item": False,
    },

    # ── Tool Items ──────────────────────────────────────────────────────────────
    "sequence_scanner": {
        "id":            "sequence_scanner",
        "name_th":       "Sequence Scanner",
        "type":          "tool_item",
        "emoji":         "🔍",
        "desc_th":       "แสดง Pattern ของสัญญาแบบ Step-by-Step — Scaffold LO-1",
        "linked_lo":     "LO-1",
        "effect":        {"scaffold_mode": True},
        "starting_item": True,   # ← given at game start
    },
    "sequence_scanner_pro": {
        "id":            "sequence_scanner_pro",
        "name_th":       "Sequence Scanner Pro",
        "type":          "tool_item",
        "emoji":         "📡",
        "desc_th":       "คำนวณ aₙ แบบ Interactive + กราฟ Sequence — รางวัลจาก Jett Lv.3",
        "linked_lo":     "LO-2, LO-3",
        "effect":        {"show_graph": True, "interactive_calc": True},
        "starting_item": False,
    },

    # ── Narrative Fragments ────────────────────────────────────────────────────
    "min_diary": {
        "id":            "min_diary",
        "name_th":       "ไดอารี่มิ้น",
        "type":          "narrative_fragment",
        "emoji":         "📔",
        "desc_th":       "เรื่องราวของเหยื่อสัญญาจริง — เพิ่ม Stakes ทางอารมณ์",
        "linked_lo":     None,
        "content_th": (
            "📔 **ไดอารี่มิ้น — วันที่ 127**\n\n"
            "วันนี้ผ่อนมา 6 เดือนแล้ว เพิ่งรู้ว่าจ่ายไปทั้งหมด 4,500 บาท\n"
            "ตอนแรกคิดว่าแค่ 3,000 บาท เพราะไม่รู้ว่างวดมันเพิ่มขึ้นทุกเดือน\n\n"
            "ขอบคุณพี่ๆ Auditor ที่ช่วยคำนวณให้ ถ้าไม่มีคุณคงไม่รู้เลย\n"
            "ต่อไปนี้จะดู d ก่อนเซ็นทุกครั้งแน่นอน — มิ้น 💙"
        ),
        "effect":        {},
        "starting_item": False,
    },
    "praew_secret_diary": {
        "id":            "praew_secret_diary",
        "name_th":       "บันทึกลับแพรว",
        "type":          "narrative_fragment",
        "emoji":         "🔒",
        "desc_th":       "แพรวยอมรับว่าเธอโดนหลอกจริงๆ — เปิดหลังโต้แย้งสำเร็จ",
        "linked_lo":     None,
        "content_th": (
            "🔒 **บันทึกลับ — แพรว, ส่วนตัวมาก**\n\n"
            "ฉันผิดจริงๆ ไม่เคยรู้ว่ามี d ทำให้งวดหลังๆ แพงขึ้น\n"
            "โกรธตอนแรกที่ถูกบอกว่าผิด แต่พอดูตัวเลขจริงๆ...\n\n"
            "งวดที่ 12 แพงกว่างวดที่ 1 มากกว่า 200% เลย\n"
            "ฉันเกือบเซ็นสัญญาโดยไม่รู้เรื่องนี้เลย\n\n"
            "ขอบคุณที่สอน ครั้งหน้าจะถาม d ก่อนเสมอ — แพรว 💜"
        ),
        "effect":        {},
        "starting_item": False,
    },
    "wichai_dark_contract": {
        "id":            "wichai_dark_contract",
        "name_th":       "สัญญาดำของวิชัย",
        "type":          "narrative_fragment",
        "emoji":         "⚠️",
        "desc_th":       "เปิดเผยว่าวิชัยโกงคนไปแล้วกี่ราย — ได้หลัง Boss Fight",
        "linked_lo":     None,
        "content_th": (
            "⚠️ **ไฟล์ลับ: WiPhone Contract History — ปีนี้**\n\n"
            "ลูกค้าที่เซ็นสัญญา WiPhone ในปีนี้:  847 ราย\n"
            "ลูกค้าที่คำนวณ a₁₂ ก่อนเซ็น:         23 ราย (2.7%)\n"
            "ลูกค้าที่ไม่ทราบงวดสุดท้ายจริง:      824 ราย (97.3%)\n\n"
            "งวดที่ 1:  ฿1,000  →  งวดที่ 12:  ฿3,200\n"
            "ความต่าง:  +220% — น้อยคนนักที่รู้ก่อนเซ็น"
        ),
        "effect":        {},
        "starting_item": False,
    },

    # ── Mastery Badges ──────────────────────────────────────────────────────────
    "certified_flex_auditor": {
        "id":            "certified_flex_auditor",
        "name_th":       "Certified FLEX Auditor",
        "type":          "mastery_badge",
        "emoji":         "🏅",
        "desc_th":       "หลักฐาน Mastery: Apply aₙ ในสัญญาจริงและตัดสินใจอย่างมีเหตุผล",
        "linked_lo":     "LO-2, LO-3",
        "effect":        {},
        "starting_item": False,
    },
    "master_auditor": {
        "id":            "master_auditor",
        "name_th":       "Master Auditor",
        "type":          "mastery_badge",
        "emoji":         "🏆",
        "desc_th":       "Synthesis: ประเมินสัญญาทั้งกระบวนและเขียนรายงานครบถ้วน",
        "linked_lo":     "LO-4",
        "effect":        {},
        "starting_item": False,
    },

    # ── Resource Token ──────────────────────────────────────────────────────────
    "flexcoin": {
        "id":            "flexcoin",
        "name_th":       "FlexCoin",
        "type":          "resource_token",
        "emoji":         "🪙",
        "desc_th":       "สกุลเงิน FlexCity — ซื้อ Hint (20 FC) หรือ Tool เพิ่ม (40 FC)",
        "linked_lo":     None,
        "effect":        {},
        "starting_item": False,  # managed by token_start in GAME_CONFIG
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — KNOWLEDGE CHECK BANK
#  ─────────────────────────────────
#  One entry per quest that requires a KC gate before NPC conversation.
#  The LLM uses topic_en + formula_en to generate varied MC questions.
#  sample_th / sample_ans are fallbacks if LLM generation fails.
#
#  difficulty: "basic" | "intermediate" | "advanced" | "synthesis"
#  bloom_level: mirrors the quest it gates
# ══════════════════════════════════════════════════════════════════════════════

KC_BANK: Dict[str, Dict[str, Any]] = {

    "mq_01_license_test": {
        "topic_en":    "Arithmetic Sequence — identify a₁ and d, calculate aₙ",
        "formula_en":  "aₙ = a₁ + (n-1)d",
        "difficulty":  "basic",
        "bloom_level": "remember",
        "context_th":  "สัญญาผ่อนชำระรายเดือน ค่างวดเพิ่มขึ้นทุกเดือนในอัตราคงที่",
        "sample_th":   "สัญญา: งวด1=฿600, งวด2=฿800, งวด3=฿1,000 — ระบุ a₁, d และหา a₅",
        "sample_ans":  "a₁=600, d=200, a₅=600+4×200=1,400 บาท",
    },
    "mq_03_argue_praew": {
        "topic_en":    "Arithmetic Sequence — show that d≠0 makes installments escalate significantly",
        "formula_en":  "aₙ = a₁ + (n-1)d; late terms much larger than a₁ when d>0",
        "difficulty":  "intermediate",
        "bloom_level": "analyze",
        "context_th":  "ผลกระทบของ d ต่องวดหลังๆ ในสัญญาผ่อนชำระ",
        "sample_th":   (
            "ถ้า a₁=1,500 และ d=150 ในสัญญา 12 เดือน\n"
            "งวดที่ 12 เท่าไร? ต่างจากงวดแรกกี่บาท?"
        ),
        "sample_ans":  "a₁₂=1,500+11×150=3,150; ต่าง 1,650 บาท (+110%)",
    },
    "mq_05_boss_wichai": {
        "topic_en":    "Arithmetic Sequence — full application: calculate aₙ and make a justified decision",
        "formula_en":  "aₙ = a₁ + (n-1)d; evaluate before signing",
        "difficulty":  "advanced",
        "bloom_level": "evaluate",
        "context_th":  "การตัดสินใจเซ็นสัญญาโดยใช้ตัวเลข aₙ เป็นเหตุผล",
        "sample_th":   (
            "สัญญา: a₁=1,000, d=200, n=12\n"
            "คำนวณ a₁₂ แล้วบอกว่าจะ เซ็น / ปฏิเสธ / ต่อรอง เพราะอะไร?"
        ),
        "sample_ans":  "a₁₂=1,000+11×200=3,200; คำตอบขึ้นกับนักเรียน แต่ต้องอ้างตัวเลข",
    },
    "fq_flex_audit_report": {
        "topic_en":    "Full synthesis — arithmetic sequences applied to 3 real contract case studies",
        "formula_en":  "aₙ = a₁ + (n-1)d used across all 3 cases",
        "difficulty":  "synthesis",
        "bloom_level": "create",
        "context_th":  "Synthesis ความรู้จาก 3 Case ก่อนเขียนรายงานสรุป",
        "sample_th":   (
            "ก่อนเขียนรายงาน:\n"
            "จาก 3 Case ที่ผ่านมา — Case ไหนมี d อันตรายที่สุด? a_last เท่าไร?"
        ),
        "sample_ans":  "ขึ้นกับการคำนวณ aₙ ของแต่ละ Case ที่นักเรียนทำ",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — CONTENT MODERATION
#  ─────────────────────────────────
#  These rules are injected as a prefix into EVERY LLM call system prompt.
#  Edit rules O1-O9 for your specific game's topic.
#  DO NOT remove rules O7-O9 (apply to all 5 games).
# ══════════════════════════════════════════════════════════════════════════════

CONTENT_MODERATION = """\
=== NAKORN THANA UNIVERSE — EDUCATIONAL CONTENT RULES ===
O1: Never instruct students how to evade legal contracts or commit fraud.
O2: Never portray FOMO or impulsive spending as purely positive. Always show a constructive alternative.
O3: Never demean or mock students who have taken loans, play Gacha, or made financial mistakes.
O4: Never recommend specific financial institutions or products by name as "best."
O5: All financial information is FOR EDUCATION ONLY — not professional financial advice.
O6: Respect กยศ. and similar institutions. Message is "calculate first," not "never borrow."
O7: Language must be appropriate for Thai high school students (Matthayom 4-6).
O8: NEVER provide direct numerical answers to math problems. Guide through hints and questions only.
O9: Respect Thai cultural values, Buddhist philosophy, and social harmony (สามัคคี).
=========================================================
"""


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — PYDANTIC MODELS  (DO NOT MODIFY)
# ══════════════════════════════════════════════════════════════════════════════

class PlayerStats(BaseModel):
    name:      str  = "นักเรียน"
    xp:        int  = 0
    level:     int  = 1
    tokens:    int  = Field(default_factory=lambda: GAME_CONFIG["token_start"])
    lives:     Optional[int] = None
    inventory: List[str] = Field(default_factory=list)   # item IDs owned
    badges:    List[str] = Field(default_factory=list)   # badge IDs earned
    fragments: List[str] = Field(default_factory=list)   # narrative fragment IDs unlocked


class GameState(BaseModel):
    player:             PlayerStats = Field(default_factory=PlayerStats)
    # Phase state machine:
    # briefing → npc_selection → knowledge_check → npc_chat → quest_result → final_quest
    current_phase:      str = "briefing"
    unlocked_npcs:      List[str] = Field(default_factory=list)
    active_npc_id:      Optional[str] = None
    # quest_id → "locked" | "available" | "active" | "completed"
    quest_statuses:     Dict[str, str] = Field(default_factory=dict)
    # npc_id → 0/1/2/3 (highest mentor level unlocked)
    mentor_levels:      Dict[str, int] = Field(default_factory=dict)
    # npc_id → number of chat turns with that NPC
    npc_chat_turns:     Dict[str, int] = Field(default_factory=dict)
    # npc_id → [{role, content}, ...] — full per-NPC history
    npc_chat_history:   Dict[str, List[Dict[str, str]]] = Field(default_factory=dict)
    completed_quests:   List[str] = Field(default_factory=list)
    active_quest_id:    Optional[str] = None
    consequence_active: bool = False
    consequence_quest:  Optional[str] = None
    game_completed:     bool = False
    turn_count:         int  = 0


# ── Request bodies ────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    npc_id:         str
    player_message: str
    game_state:     GameState
    quest_id:       Optional[str] = None


class MentorCheckRequest(BaseModel):
    npc_id:       str
    game_state:   GameState
    last_message: str


class QuestCompleteRequest(BaseModel):
    quest_id:   str
    npc_id:     Optional[str] = None
    # "success" | "consequence_triggered" | "smart_rejection" | "smart_negotiation"
    outcome:    str = "success"
    game_state: GameState


class KCGenerateRequest(BaseModel):
    quest_id:   str
    game_state: GameState


class KCEvaluateRequest(BaseModel):
    quest_id:       str
    student_answer: str
    question_text:  str
    game_state:     GameState


class FinalQuestEvalRequest(BaseModel):
    quest_id:           str
    student_submission: str
    game_state:         GameState


class ConsequenceCheckRequest(BaseModel):
    quest_id:   str
    npc_id:     str
    outcome:    str
    game_state: GameState


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 8 — HELPER FUNCTIONS  (DO NOT MODIFY)
# ══════════════════════════════════════════════════════════════════════════════

def _get_starting_items() -> List[str]:
    """Return item IDs marked as starting_item=True in ITEM_DATA."""
    return [iid for iid, item in ITEM_DATA.items() if item.get("starting_item")]


def _get_starting_quests() -> Dict[str, str]:
    """Return {quest_id: starting_status} for all quests."""
    return {qid: q["starting_status"] for qid, q in QUEST_DATA.items()}


def _get_default_unlocked_npcs() -> List[str]:
    """Return NPC IDs with unlock_condition='default'."""
    return [nid for nid, npc in NPC_DATA.items() if npc["unlock_condition"] == "default"]


def _check_npc_unlockable(npc_id: str, game_state: GameState) -> bool:
    """
    Evaluate whether an NPC's unlock condition is satisfied by the current game_state.
    Supports: default | after_quest | after_item | after_npc | after_quests (AND of quest+npc).
    """
    npc = NPC_DATA.get(npc_id)
    if not npc:
        return False
    cond = npc["unlock_condition"]
    if cond == "default":
        return True
    if cond == "after_quest":
        req_q = npc.get("unlock_requires_quest")
        return (not req_q) or (req_q in game_state.completed_quests)
    if cond == "after_item":
        req_i = npc.get("unlock_requires_item")
        return (not req_i) or (req_i in game_state.player.inventory)
    if cond == "after_npc":
        req_n = npc.get("unlock_requires_npc")
        return (not req_n) or (req_n in game_state.unlocked_npcs)
    if cond == "after_quests":
        req_q = npc.get("unlock_requires_quest")
        req_n = npc.get("unlock_requires_npc")
        q_ok  = (not req_q) or (req_q in game_state.completed_quests)
        n_ok  = (not req_n) or (req_n in game_state.unlocked_npcs)
        return q_ok and n_ok
    return False


def _apply_quest_rewards(npc_id: str, game_state: GameState) -> Dict[str, Any]:
    """
    Build a reward payload from an NPC's reward dict.
    Does NOT mutate game_state — returns a dict for the frontend to apply.
    """
    npc = NPC_DATA.get(npc_id, {})
    rewards = npc.get("rewards", {})

    gained_items:    List[str] = []
    gained_badges:   List[str] = []
    gained_fragments:List[str] = []
    newly_unlocked:  List[str] = []

    for item_id in rewards.get("items", []):
        if item_id in game_state.player.inventory:
            continue
        item = ITEM_DATA.get(item_id, {})
        item_type = item.get("type", "")
        if item_type == "mastery_badge":
            if item_id not in game_state.player.badges:
                gained_badges.append(item_id)
        elif item_type == "narrative_fragment":
            if item_id not in game_state.player.fragments:
                gained_fragments.append(item_id)
        else:
            gained_items.append(item_id)

    for badge_id in rewards.get("badges", []):
        if badge_id not in game_state.player.badges:
            gained_badges.append(badge_id)

    for unlock_npc in rewards.get("unlock_npcs", []):
        if unlock_npc not in game_state.unlocked_npcs:
            newly_unlocked.append(unlock_npc)

    return {
        "xp_gained":          rewards.get("xp", 0),
        "tokens_gained":      rewards.get("tokens", 0),
        "items_gained":       gained_items,
        "badges_gained":      gained_badges,
        "fragments_gained":   gained_fragments,
        "unlock_npcs":        newly_unlocked,
        "unlock_quests":      rewards.get("unlock_quests", []),
        "xp_total":           game_state.player.xp + rewards.get("xp", 0),
        "tokens_total":       game_state.player.tokens + rewards.get("tokens", 0),
    }


def _apply_mentor_level_reward(npc_id: str, level: int) -> Dict[str, Any]:
    """Build a reward payload for a specific mentor level unlock."""
    npc = NPC_DATA.get(npc_id, {})
    level_data = next(
        (lv for lv in npc.get("mentor_levels", []) if lv["level"] == level), {}
    )
    reward = level_data.get("reward_on_unlock", {})
    return {
        "xp_gained":     reward.get("xp", 0),
        "tokens_gained": reward.get("tokens", 0),
        "items_gained":  reward.get("items", []),
        "secret_text":   level_data.get("secret_th", ""),
        "level":         level,
    }


def _build_npc_system_prompt(npc_id: str, game_state: GameState) -> str:
    """
    Compose the full system prompt sent to the LLM for an NPC turn:
      CONTENT_MODERATION prefix + NPC system_prompt + injected game context.
    Raw IDs are never exposed — only display names and titles from DATA dicts.
    """
    npc = NPC_DATA.get(npc_id, {})
    base_prompt = npc.get("system_prompt", "คุณคือ NPC ในเกมการศึกษา นครธนา Universe")

    quest_id   = game_state.active_quest_id or npc.get("associated_quest", "")
    quest      = QUEST_DATA.get(quest_id, {})
    mentor_lvl = game_state.mentor_levels.get(npc_id, 0)

    context_lines = [
        "--- GAME CONTEXT (do not reveal these details to the student) ---",
        f"Game: {GAME_CONFIG['game_title']}",
        f"Math topic: {GAME_CONFIG['math_topic']}",
        f"Formula: {GAME_CONFIG['math_formula']}",
        f"Current quest title: {quest.get('title_th', 'ไม่มีภารกิจที่ active')}",
        f"Bloom's target: {quest.get('bloom_level', 'n/a')}",
        f"Mechanic: {quest.get('mechanic', 'n/a')}",
        f"Completed quests count: {len(game_state.completed_quests)}",
        f"Student XP: {game_state.player.xp}",
    ]
    if npc.get("is_mentor"):
        context_lines.append(f"Current mentor level unlocked: {mentor_lvl}")

    context = "\n".join(context_lines)
    return f"{CONTENT_MODERATION}\n{base_prompt}\n\n{context}"


async def _call_llm(
    system: str,
    messages: List[Dict[str, str]],
    max_tokens: int   = MAX_TOKENS_CHAT,
    temperature: float = TEMPERATURE_CHAT,
    stream: bool = False,
) -> Any:
    """
    Unified OpenAI-compatible async LLM call.
    The system prompt is injected as the first message with role='system'.

    For stream=True, returns (httpx.AsyncClient, headers, payload) tuple
    so the caller can use client.stream(). The caller is responsible for
    closing the client.

    For stream=False, returns the parsed JSON response dict.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured — set API_KEY in .env")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
    }
    # Build messages array with system role prepended
    full_messages = [{"role": "system", "content": system}] + messages

    payload: Dict[str, Any] = {
        "model":       API_MODEL,
        "max_tokens":  max_tokens,
        "temperature": temperature,
        "messages":    full_messages,
    }
    if stream:
        payload["stream"] = True

    if stream:
        client = httpx.AsyncClient(timeout=60.0)
        return client, headers, payload

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            body   = exc.response.text[:200]
            logger.error(f"LLM API error {status}: {body}")
            raise HTTPException(status_code=502, detail=f"LLM API returned {status}: {body}")
        except httpx.RequestError as exc:
            logger.error(f"LLM request error: {exc}")
            raise HTTPException(status_code=503, detail="ไม่สามารถเชื่อมต่อ LLM API ได้")


def _extract_llm_text(response: Dict[str, Any]) -> str:
    """
    Extract the assistant's text content from an OpenAI-compatible response dict.
    Handles both OpenAI format and common variants.
    """
    try:
        return response["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        # Fallback: try Anthropic-style response shape
        try:
            return response["content"][0]["text"] or ""
        except (KeyError, IndexError, TypeError):
            logger.warning(f"Unexpected LLM response shape: {str(response)[:200]}")
            return ""


def _extract_json_tag(text: str) -> Dict[str, Any]:
    """
    Extract the last {...} JSON object embedded in an NPC response.
    Used to parse quest_status, mentor_level, outcome, etc.
    Returns empty dict if none found.
    """
    matches = re.findall(r'\{[^{}]+\}', text)
    for m in reversed(matches):
        try:
            return json.loads(m)
        except json.JSONDecodeError:
            continue
    return {}


def _strip_json_tag(text: str) -> str:
    """Remove the trailing embedded JSON tag from NPC response for clean display."""
    return re.sub(r'\s*\{[^{}]+\}\s*$', '', text).strip()


async def _sse_stream_npc(
    npc_id: str,
    messages: List[Dict[str, str]],
    system_prompt: str,
) -> AsyncGenerator[str, None]:
    """
    SSE generator for streaming NPC chat via OpenAI-compatible streaming.
    Yields chunks: data: <json>\\n\\n
    Final chunk (type='game_event') carries extracted game tags + full_text.
    Error chunk (type='error') carries a Thai error message.

    OpenAI SSE format per chunk:
      data: {"id":...,"choices":[{"delta":{"content":"..."},...}]}
    """
    client, headers, payload = await _call_llm(
        system=system_prompt,
        messages=messages,
        stream=True,
    )
    full_text = ""
    try:
        async with client.stream("POST", API_URL, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                raw = line[6:].strip()
                if raw in ("[DONE]", ""):
                    break
                try:
                    chunk = json.loads(raw)
                    # OpenAI streaming: choices[0].delta.content
                    delta   = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content") or ""
                    if content:
                        full_text += content
                        yield f"data: {json.dumps({'type':'text','text':content})}\n\n"
                except json.JSONDecodeError:
                    continue

        # After full stream: extract embedded game tags from complete text
        tags = _extract_json_tag(full_text)
        clean_text = _strip_json_tag(full_text)
        yield f"data: {json.dumps({'type':'game_event','tags':tags,'full_text':clean_text})}\n\n"
        yield "data: [DONE]\n\n"

    except httpx.HTTPStatusError as exc:
        logger.error(f"SSE HTTP error for NPC {npc_id}: {exc.response.status_code}")
        yield f"data: {json.dumps({'type':'error','message':'เซิร์ฟเวอร์ขัดข้อง กรุณาลองใหม่'})}\n\n"
    except Exception as exc:
        logger.error(f"SSE stream error for NPC {npc_id}: {exc}")
        yield f"data: {json.dumps({'type':'error','message':'การเชื่อมต่อขัดข้อง กรุณาลองใหม่'})}\n\n"
    finally:
        await client.aclose()


def _parse_json_response(text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON response from the LLM. Strips markdown fences if present.
    Returns fallback dict on failure.
    """
    clean = text.strip()
    # Strip markdown code fences
    clean = re.sub(r'^```(?:json)?\s*', '', clean)
    clean = re.sub(r'\s*```$', '', clean)
    clean = clean.strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse LLM JSON response: {clean[:200]}")
        return fallback


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 9 — API ENDPOINTS  (DO NOT MODIFY)
# ══════════════════════════════════════════════════════════════════════════════

# ── Serve Frontend ────────────────────────────────────────────────────────────

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ── Game Initialization ───────────────────────────────────────────────────────

@app.get("/api/game-config")
async def get_game_config():
    """
    Return safe game configuration to the frontend.
    Excludes: system prompts, API keys, consequence internals, final_quest_rubric weights.
    Frontend uses this to initialize game state, render world intro, and build item glossary.
    """
    # Strip sensitive fields from NPC data before sending to client
    safe_npcs = {}
    for nid, npc in NPC_DATA.items():
        safe_npcs[nid] = {
            "id":                 npc["id"],
            "display_name":       npc["display_name"],
            "title_th":           npc["title_th"],
            "avatar_emoji":       npc["avatar_emoji"],
            "archetype":          npc["archetype"],
            "location_th":        npc["location_th"],
            "bloom_level":        npc["bloom_level"],
            "is_mentor":          npc["is_mentor"],
            "mentor_level_count": len(npc.get("mentor_levels", [])),
            "opening_message_th": npc["opening_message_th"],
            "associated_quest":   npc.get("associated_quest"),
            "min_turns":          npc.get("min_turns", 1),
            "unlock_condition":   npc["unlock_condition"],
        }

    # Strip consequence internals from quests
    safe_quests = {}
    for qid, q in QUEST_DATA.items():
        safe_q = {k: v for k, v in q.items() if k not in ("consequence",)}
        safe_quests[qid] = safe_q

    # Strip rubric weights (student should not see scoring internals)
    safe_config = {k: v for k, v in GAME_CONFIG.items() if k != "final_quest_rubric"}

    return JSONResponse({
        "game_config":     safe_config,
        "npcs":            safe_npcs,
        "quests":          safe_quests,
        "items":           ITEM_DATA,
        "starting_items":  _get_starting_items(),
        "starting_quests": _get_starting_quests(),
        "unlocked_npcs":   _get_default_unlocked_npcs(),
    })


# ── NPC Chat (SSE Streaming) ──────────────────────────────────────────────────

@app.post("/api/npc/chat")
async def npc_chat(req: ChatRequest):
    """
    Stream NPC response via Server-Sent Events.
    The NPC's response embeds JSON game tags (quest_status, mentor_level, outcome).
    Frontend reads the final game_event chunk and calls /api/quest/complete if needed.

    SSE chunk types:
      {type: "text",       text: "..."}          — content delta
      {type: "game_event", tags: {...}, full_text:"..."} — end of stream summary
      {type: "error",      message: "..."}        — error
    """
    npc_id = req.npc_id
    npc = NPC_DATA.get(npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail=f"NPC '{npc_id}' not found")

    # Validate NPC is unlocked
    if npc_id not in req.game_state.unlocked_npcs and npc["unlock_condition"] != "default":
        raise HTTPException(status_code=403, detail=f"NPC '{npc_id}' not yet unlocked")

    # Build per-NPC chat history; append new user message
    history = list(req.game_state.npc_chat_history.get(npc_id, []))
    history.append({"role": "user", "content": req.player_message})

    system = _build_npc_system_prompt(npc_id, req.game_state)

    return StreamingResponse(
        _sse_stream_npc(npc_id, history, system),
        media_type="text/event-stream",
        headers={
            "Cache-Control":   "no-cache",
            "X-Accel-Buffering":"no",
            "Connection":       "keep-alive",
        },
    )


# ── Quest Complete — Apply Rewards ────────────────────────────────────────────

@app.post("/api/quest/complete")
async def quest_complete(req: QuestCompleteRequest):
    """
    Called by frontend after detecting quest_status=completed in NPC stream.
    Computes and returns the reward payload. Frontend applies rewards to local gameState.

    outcome values:
      "success"                 — standard completion
      "consequence_triggered"   — student made bad decision without calculating
      "smart_rejection"         — student rejected after calculating
      "smart_negotiation"       — student negotiated after calculating (bonus XP)
    """
    quest = QUEST_DATA.get(req.quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quest '{req.quest_id}' not found")

    npc_id = req.npc_id or quest.get("required_npc")
    rewards = _apply_quest_rewards(npc_id, req.game_state) if npc_id else {
        "xp_gained": 0, "tokens_gained": 0, "items_gained": [],
        "badges_gained": [], "fragments_gained": [],
        "unlock_npcs": [], "unlock_quests": [],
    }

    # Bonus for smart negotiation
    if req.outcome == "smart_negotiation":
        rewards["xp_gained"]     = rewards.get("xp_gained", 0) + 30
        rewards["tokens_gained"] = rewards.get("tokens_gained", 0) + 15

    # Handle consequence chain
    consequence_triggered = (req.outcome == "consequence_triggered")
    consequence_data: Dict[str, Any] = {}
    if consequence_triggered and quest.get("consequence"):
        c = quest["consequence"]
        consequence_data = {
            "chain_stages_th":  c.get("chain_stages_th", []),
            "penalty_tokens":   c.get("penalty_tokens", 0),
            "allow_retry":      c.get("allow_retry", True),
            "retry_message_th": c.get("retry_message_th", ""),
        }
        rewards["tokens_gained"] = rewards.get("tokens_gained", 0) + c.get("penalty_tokens", 0)
        rewards["xp_gained"]     = rewards.get("xp_gained", 0) + c.get("penalty_xp", 0)

    # Final quest grants master badge automatically on success
    if quest["type"] == "final" and req.outcome == "success":
        final_badge = "master_auditor"
        if final_badge not in rewards.get("badges_gained", []):
            rewards.setdefault("badges_gained", []).append(final_badge)
        final_artifact = "flex_audit_report_artifact"
        if final_artifact not in rewards.get("items_gained", []):
            rewards.setdefault("items_gained", []).append(final_artifact)

    return JSONResponse({
        "quest_id":              req.quest_id,
        "outcome":               req.outcome,
        "rewards":               rewards,
        "consequence_triggered": consequence_triggered,
        "consequence_data":      consequence_data,
        "xp_gained":             rewards.get("xp_gained", 0),
        "tokens_gained":         rewards.get("tokens_gained", 0),
        "items_gained":          rewards.get("items_gained", []),
        "badges_gained":         rewards.get("badges_gained", []),
        "fragments_gained":      rewards.get("fragments_gained", []),
        "unlock_npcs":           rewards.get("unlock_npcs", []),
        "unlock_quests":         rewards.get("unlock_quests", []),
        "items_detail":          [ITEM_DATA.get(i, {}) for i in rewards.get("items_gained", [])],
    })


# ── Mentor Level Unlock ───────────────────────────────────────────────────────

@app.post("/api/npc/mentor-unlock")
async def mentor_unlock(req: MentorCheckRequest):
    """
    Evaluate whether the student's last message qualifies for the next mentor level.
    Uses a low-temperature LLM call for deterministic evaluation.
    Returns: {qualified, new_level, secret_th, rewards}
    """
    npc = NPC_DATA.get(req.npc_id)
    if not npc or not npc.get("is_mentor"):
        raise HTTPException(status_code=400, detail=f"NPC '{req.npc_id}' is not a mentor")

    current_level = req.game_state.mentor_levels.get(req.npc_id, 0)
    next_level    = current_level + 1
    levels        = npc.get("mentor_levels", [])

    if next_level > len(levels):
        return JSONResponse({
            "qualified":  False,
            "reason_th":  "ปลดล็อกครบทุกระดับแล้ว",
            "new_level":  current_level,
        })

    target = next((lv for lv in levels if lv["level"] == next_level), None)
    if not target:
        return JSONResponse({"qualified": False, "new_level": current_level})

    eval_prompt = (
        f"You are evaluating whether a student's message qualifies to unlock "
        f"Mentor Level {next_level} for NPC '{npc['display_name']}' "
        f"in an educational math game.\n\n"
        f"UNLOCK CRITERIA: {target['unlock_criteria_en']}\n\n"
        f"STUDENT'S LATEST MESSAGE:\n\"{req.last_message}\"\n\n"
        f"COMPLETED QUESTS: {req.game_state.completed_quests}\n\n"
        "Reply ONLY with valid JSON (no markdown, no extra text):\n"
        "{\"qualified\": true|false, \"reason_en\": \"brief reason (max 20 words)\"}"
    )

    resp = await _call_llm(
        system=CONTENT_MODERATION,
        messages=[{"role": "user", "content": eval_prompt}],
        max_tokens=80,
        temperature=TEMPERATURE_EVAL,
    )
    text   = _extract_llm_text(resp)
    result = _parse_json_response(text, {"qualified": False})

    if result.get("qualified"):
        reward_data = _apply_mentor_level_reward(req.npc_id, next_level)
        return JSONResponse({
            "qualified":     True,
            "new_level":     next_level,
            "secret_th":     target["secret_th"],
            "rewards":       reward_data,
            "xp_gained":     reward_data["xp_gained"],
            "tokens_gained": reward_data["tokens_gained"],
            "items_gained":  reward_data["items_gained"],
        })

    return JSONResponse({
        "qualified":  False,
        "reason_th":  "ยังไม่ถึงเกณฑ์ ลองถามให้ลึกกว่านี้",
        "new_level":  current_level,
    })


# ── Knowledge Check ───────────────────────────────────────────────────────────

@app.post("/api/knowledge-check/generate")
async def kc_generate(req: KCGenerateRequest):
    """
    Generate a contextual Knowledge Check question for the given quest.
    Returns: {question, has_kc, quest_id}
    Frontend uses this to show the KC gate before NPC conversation begins.
    """
    kc = KC_BANK.get(req.quest_id)
    if not kc:
        return JSONResponse({
            "question": "ทบทวนสูตรก่อนเริ่ม Quest ได้เลย",
            "has_kc":   False,
            "quest_id": req.quest_id,
        })

    gen_prompt = (
        f"Generate ONE knowledge-check question in Thai for a Thai high school student.\n"
        f"Topic: {kc['topic_en']}\n"
        f"Formula: {kc['formula_en']}\n"
        f"Difficulty: {kc['difficulty']} (Bloom's level: {kc['bloom_level']})\n"
        f"Game context: {GAME_CONFIG['world_name']} — {kc.get('context_th','')}\n\n"
        "REQUIREMENTS:\n"
        "1. Use a concrete financial scenario (contract, installment, etc.) with specific numbers.\n"
        "2. Question must require APPLYING the formula — not just reciting it.\n"
        "3. Keep it to 2-3 sentences in Thai. Do NOT include the answer.\n"
        "4. Make the numbers different from any sample in the KC_BANK.\n\n"
        "Reply ONLY with the question text in Thai. No JSON. No preamble."
    )

    resp = await _call_llm(
        system=CONTENT_MODERATION,
        messages=[{"role": "user", "content": gen_prompt}],
        max_tokens=MAX_TOKENS_KC,
        temperature=TEMPERATURE_KC,
    )
    question = _extract_llm_text(resp).strip() or kc["sample_th"]
    return JSONResponse({"question": question, "has_kc": True, "quest_id": req.quest_id})


@app.post("/api/knowledge-check/evaluate")
async def kc_evaluate(req: KCEvaluateRequest):
    """
    Evaluate a student's KC answer.
    Returns: {score, passed, feedback_th}
    If passed: frontend proceeds to NPC chat.
    If failed: frontend shows hint and re-generates a new question.
    """
    kc = KC_BANK.get(req.quest_id, {})
    eval_prompt = (
        f"Evaluate this Thai high school student's answer to a knowledge-check question.\n\n"
        f"MATH TOPIC: {kc.get('topic_en', GAME_CONFIG['math_topic'])}\n"
        f"FORMULA: {kc.get('formula_en', GAME_CONFIG['math_formula'])}\n\n"
        f"QUESTION:\n{req.question_text}\n\n"
        f"STUDENT ANSWER:\n{req.student_answer}\n\n"
        "RUBRIC:\n"
        "  1.0: Correct formula, correct calculation, correct final answer.\n"
        "  0.7: Correct approach but one minor arithmetic error.\n"
        "  0.5: Correct formula cited but calculation incomplete or partially wrong.\n"
        "  0.0: Wrong formula, off-topic, or blank.\n\n"
        "Reply ONLY with JSON (no markdown fences):\n"
        "{\"score\": 0.0-1.0, \"passed\": true|false, "
        "\"feedback_th\": \"brief Thai feedback 1-2 sentences\"}"
    )

    resp = await _call_llm(
        system=CONTENT_MODERATION,
        messages=[{"role": "user", "content": eval_prompt}],
        max_tokens=MAX_TOKENS_EVAL,
        temperature=TEMPERATURE_EVAL,
    )
    text   = _extract_llm_text(resp)
    result = _parse_json_response(text, {
        "score": 0.0, "passed": False, "feedback_th": "กรุณาลองอีกครั้ง"
    })
    result.setdefault("passed",      result.get("score", 0.0) >= 0.6)
    result.setdefault("feedback_th", "")
    return JSONResponse(result)


# ── Final Quest — 3-Dimension AI Rubric ──────────────────────────────────────

@app.post("/api/final-quest/evaluate")
async def final_quest_evaluate(req: FinalQuestEvalRequest):
    """
    Evaluate the student's Final Quest submission using the 3-dimension rubric.
    Returns: {overall_score, passed, dimension_scores, feedback_th, hint_th, rewards}
    """
    quest = QUEST_DATA.get(req.quest_id)
    if not quest or quest["type"] != "final":
        raise HTTPException(status_code=400, detail=f"'{req.quest_id}' is not a final quest")

    rubric    = GAME_CONFIG["final_quest_rubric"]
    dims      = rubric["dimensions"]
    threshold = rubric["pass_threshold"]

    dim_criteria = "\n".join(
        f"  [{d['id']}] weight={d['weight']:.0%}: {d['criteria_en']}"
        for d in dims
    )

    eval_prompt = (
        f"You are an educational AI evaluator for a Thai high school math game.\n"
        f"Game: {GAME_CONFIG['game_title']} | Topic: {GAME_CONFIG['math_topic']}\n"
        f"Formula: {GAME_CONFIG['math_formula']}\n\n"
        f"FINAL QUEST TASK:\n{quest.get('task_prompt_th','')}\n\n"
        f"STUDENT SUBMISSION:\n{req.student_submission}\n\n"
        f"EVALUATION RUBRIC (score each dimension 0.0-1.0):\n{dim_criteria}\n\n"
        f"PASS THRESHOLD: {threshold} weighted average\n\n"
        "INSTRUCTIONS:\n"
        "1. Score each dimension 0.0-1.0 based on its criteria.\n"
        "2. Compute overall_score = weighted average (do the math).\n"
        "3. Write feedback_th: 2-3 constructive sentences in Thai.\n"
        "4. Write hint_th: 1 actionable sentence in Thai if NOT passed; empty string if passed.\n\n"
        "Reply ONLY with JSON (no markdown fences, no preamble):\n"
        "{\n"
        "  \"dimension_scores\": {\n"
        "    " + ", ".join(f'"{d["id"]}":0.0' for d in dims) + "\n"
        "  },\n"
        "  \"overall_score\": 0.0,\n"
        "  \"passed\": false,\n"
        "  \"feedback_th\": \"\",\n"
        "  \"hint_th\": \"\"\n"
        "}"
    )

    resp = await _call_llm(
        system=CONTENT_MODERATION,
        messages=[{"role": "user", "content": eval_prompt}],
        max_tokens=MAX_TOKENS_EVAL,
        temperature=TEMPERATURE_EVAL,
    )
    text   = _extract_llm_text(resp)
    result = _parse_json_response(text, {
        "dimension_scores": {d["id"]: 0.0 for d in dims},
        "overall_score":    0.0,
        "passed":           False,
        "feedback_th":      "ระบบประเมินขัดข้อง กรุณาส่งอีกครั้ง",
        "hint_th":          "",
    })

    # Recompute overall_score server-side to prevent tampering
    dim_scores = result.get("dimension_scores", {})
    computed   = sum(dim_scores.get(d["id"], 0.0) * d["weight"] for d in dims)
    result["overall_score"] = round(computed, 3)
    result["passed"]        = computed >= threshold

    # Grant final rewards on pass
    if result["passed"]:
        result["rewards"] = {
            "badges_gained": ["master_auditor"],
            "items_gained":  ["flex_audit_report_artifact"],
            "xp_gained":     80,
            "tokens_gained": 40,
        }
    else:
        result["rewards"] = {}

    return JSONResponse(result)


# ── Consequence Chain ─────────────────────────────────────────────────────────

@app.post("/api/consequence/check")
async def consequence_check(req: ConsequenceCheckRequest):
    """
    Called when outcome == 'consequence_triggered'.
    Returns the full consequence chain data for frontend to animate stage-by-stage.
    """
    quest = QUEST_DATA.get(req.quest_id)
    if not quest or not quest.get("consequence"):
        return JSONResponse({"has_consequence": False})

    c = quest["consequence"]
    return JSONResponse({
        "has_consequence":  True,
        "chain_stages_th":  c.get("chain_stages_th", []),
        "penalty_tokens":   c.get("penalty_tokens", 0),
        "allow_retry":      c.get("allow_retry", True),
        "retry_message_th": c.get("retry_message_th", ""),
        "lesson_th": (
            f"💡 บทเรียน: {GAME_CONFIG['math_formula']} ช่วยให้เห็น 'ค่าจริงสุดท้าย' "
            "ก่อนตัดสินใจ — ใช้สูตรนี้เป็นเกราะป้องกันตัวเอง"
        ),
    })


# ── NPC Availability Check ────────────────────────────────────────────────────

@app.post("/api/npc/check-available")
async def npc_check_available(game_state: GameState):
    """
    Given current game_state, return which NPCs can now be newly unlocked.
    Frontend calls this after any quest completion or item gain to reveal new NPCs.
    """
    newly_available = []
    for npc_id, npc in NPC_DATA.items():
        if npc_id in game_state.unlocked_npcs:
            continue
        if _check_npc_unlockable(npc_id, game_state):
            newly_available.append({
                "id":           npc_id,
                "display_name": npc["display_name"],
                "avatar_emoji": npc["avatar_emoji"],
                "title_th":     npc["title_th"],
                "archetype":    npc["archetype"],
                "location_th":  npc["location_th"],
            })
    return JSONResponse({"newly_available": newly_available})


# ── Hint Purchase ─────────────────────────────────────────────────────────────

@app.post("/api/hint/buy")
async def buy_hint(quest_id: str, game_state: GameState):
    """
    Deduct token_hint_cost from player tokens and return a Socratic hint.
    Returns: {success, hint_th, tokens_spent, tokens_remain}
    """
    cost = GAME_CONFIG["token_hint_cost"]
    if game_state.player.tokens < cost:
        return JSONResponse({
            "success":    False,
            "message_th": f"ไม่มี {GAME_CONFIG['token_name']} เพียงพอ (ต้องการ {cost} {GAME_CONFIG['token_symbol']})",
        })

    kc = KC_BANK.get(quest_id, {})
    hint_prompt = (
        f"Generate a helpful Socratic hint in Thai for a student who is stuck on:\n"
        f"Topic: {kc.get('topic_en', GAME_CONFIG['math_topic'])}\n"
        f"Formula: {kc.get('formula_en', GAME_CONFIG['math_formula'])}\n"
        f"Context: {GAME_CONFIG['world_name']}\n\n"
        "Rules:\n"
        "1. Do NOT give the numerical answer.\n"
        "2. Guide with a leading question or a partial step.\n"
        "3. Keep it to 1-2 sentences in Thai.\n"
        "4. Start with '💡 Hint:'\n\n"
        "Reply ONLY with the hint text."
    )

    resp = await _call_llm(
        system=CONTENT_MODERATION,
        messages=[{"role": "user", "content": hint_prompt}],
        max_tokens=120,
        temperature=0.5,
    )
    hint = _extract_llm_text(resp).strip() or "💡 Hint: ลองดูที่ค่า d ก่อน — มันอยู่ในสัญญาหน้า 2"

    return JSONResponse({
        "success":       True,
        "hint_th":       hint,
        "tokens_spent":  cost,
        "tokens_remain": game_state.player.tokens - cost,
    })


# ── Item Detail ───────────────────────────────────────────────────────────────

@app.get("/api/item/{item_id}")
async def get_item(item_id: str):
    """Return full item details by ID (including narrative content)."""
    item = ITEM_DATA.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")
    return JSONResponse(item)


# ── Health Check ──────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    """Simple health check. Also verifies API key is configured."""
    return JSONResponse({
        "status":    "ok",
        "game":      GAME_CONFIG["game_title"],
        "model":     API_MODEL,
        "api_ready": bool(API_KEY),
    })


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 10 — APP STARTUP  (DO NOT MODIFY)
# ══════════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info(f"🎮  {GAME_CONFIG['game_title']} | นครธนา Universe v2.0")
    logger.info(f"    World:  {GAME_CONFIG['world_name']}  ({GAME_CONFIG.get('world_year','')})")
    logger.info(f"    Role:   {GAME_CONFIG['player_role']}")
    logger.info(f"    Topic:  {GAME_CONFIG['math_topic']}")
    logger.info(f"    NPCs:   {len(NPC_DATA)} | Quests: {len(QUEST_DATA)} | Items: {len(ITEM_DATA)}")
    logger.info(f"    Model:  {API_MODEL}")
    logger.info(f"    URL:    {API_URL}")
    if not API_KEY:
        logger.warning("⚠️  API_KEY not set in .env — all LLM calls will fail!")
    else:
        logger.info(f"    Key:    ...{API_KEY[-6:]}")
    logger.info("=" * 60)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)
