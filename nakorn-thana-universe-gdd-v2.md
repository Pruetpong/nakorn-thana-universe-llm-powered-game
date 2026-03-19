# 🏙️ นครธนา Universe — Game Design Document v2.0
### 5 เกมการศึกษา: คณิตศาสตร์การเงิน ม.ปลาย
**ปรับปรุงตาม WORLD Framework | NPC Archetypes | Quest Map | Item Taxonomy | Bloom's Taxonomy**

---

> **หมายเหตุเอกสาร:** GDD นี้ใช้เป็น Specification สำหรับพัฒนาเกมในชั้น FastAPI + HTML5 Frontend
> แต่ละเกมเป็น Standalone — ครูเปิดเกมใดก่อนก็ได้ตามแผนการสอน
> เนื้อหานักเรียน: ภาษาไทย | System Prompt AI: ภาษาอังกฤษ

---

## ภาพรวม 5 เกม (Universe Map)

| # | ชื่อเกม | หัวข้อคณิต | บริบทนักเรียน | Bloom's สูงสุด | Quest หลัก |
|---|---------|-----------|-------------|----------------|-----------|
| 1 | **FLEX PROTOCOL** | Arithmetic Sequence | ผ่อนโทรศัพท์ / FOMO | Apply | Consequence Chain |
| 2 | **GACHA KINGDOM** | Geometric Sequence | เติมเกม / Pity Rate | Analyze | Investigation |
| 3 | **TUTOR WARS** | Arithmetic Series | ค่าติว TCAS | Apply + Analyze | Resource Management |
| 4 | **COMPOUND CHRONICLES** | Geometric Series + Compound Interest | Creator Economy / ออมเงิน | Analyze + Evaluate | Resource Management + Consequence Chain |
| 5 | **FUTURE FUND** | PV, FV, Annuities (ทุกสูตร) | TCAS + เส้นทางมหาวิทยาลัย | Evaluate + **Create** | Collaborative Puzzle + Creation |

**กฎฟิสิกส์ร่วมของ Universe:**
> ใน "นครธนา" ทุกการตัดสินใจทางการเงินมีตัวเลขรองรับ — ไม่มีการเดา ไม่มีการ Flex โดยไม่รู้จริง คนที่คำนวณได้คือคนที่มีอำนาจในโลกนี้

---

---

# 🎮 เกมที่ 1: FLEX PROTOCOL
## หัวข้อ: ลำดับเลขคณิต (Arithmetic Sequence) — $a_n = a_1 + (n-1)d$

---

## W — World: สังคม FlexCity

**Setting:** ปี 2030 สังคม FlexCity ที่ "Social Status" วัดด้วย **FlexScore** แสดงบน Holographic Profile ทุกคน ยิ่ง FlexScore สูง ยิ่งเข้าถึงพื้นที่พิเศษและโอกาสพิเศษ แต่ระบบ Dynamic Pricing ของเมืองทำให้ทุก Installment Series มีค่าใช้จ่ายเพิ่มขึ้นทุกเดือนในอัตราคงที่ตามหลักลำดับเลขคณิต

**กฎฟิสิกส์ของโลก:**
> "ใน FlexCity การซื้อสินค้าแบบผ่อนชำระจะมีค่างวดเพิ่มขึ้นทุกเดือนในอัตราคงที่ $d$ เพราะระบบ Dynamic Pricing คำนวณ Inflation อัตโนมัติ คนที่รู้จัก $a_n = a_1 + (n-1)d$ จะเห็น 'กับดัก' ที่คนอื่นมองไม่เห็น"

**บรรยากาศโลก:** Cyberpunk + Thai Street Market — ป้ายโฆษณาโฮโลแกรมกระพริบ, วัยรุ่นอวดของ, สัญญาผ่อนชำระซ่อนอยู่ทุกมุมเมือง

**ปัญหาหลักของโลก:** มีแก๊งค์ผู้ค้าใช้ระบบ Dynamic Pricing หลอกวัยรุ่นที่ไม่รู้คณิตศาสตร์ให้เซ็นสัญญาโดยไม่คำนวณงวดสุดท้าย

---

## O — Objectives

**บทบาทนักเรียน:** "FLEX Auditor" — นักตรวจสอบสัญญาผ่อนชำระที่เมืองจ้างมาปกป้องวัยรุ่น

**Learning Objectives (LO):**
- **LO-1:** ระบุ $a_1$ (งวดแรก) และ $d$ (อัตราเพิ่ม) จากสัญญาจริง
- **LO-2:** คำนวณ $a_n$ เพื่อหางวดที่ n ที่ต้องจ่าย
- **LO-3:** ประเมินว่าสัญญา "ซ่อน" ค่าใช้จ่ายแฝงตรงไหน
- **LO-4:** ตัดสินใจว่าจะเซ็น / ปฏิเสธ / ต่อรองสัญญา โดยใช้ตัวเลขจริงเป็นเหตุผล

**Win Condition:** เปิดโปงสัญญาโกงได้สำเร็จ 3 Case + รับ Badge "Certified FLEX Auditor"

---

## R — Roles (NPC Roster)

### NPC-01: ARIA — AI ระบบรักษาความปลอดภัยสัญญา
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Gatekeeper |
| **บุคลิก** | เย็นชา, เป็นกลาง, พูดเป็นภาษาเทคนิค |
| **Bloom's** | Remember → Understand |
| **Unlock Condition** | เริ่มเกมทันที (Default) |
| **หน้าที่** | ทดสอบความเข้าใจ $a_n$ พื้นฐานก่อนให้ Auditor License |
| **ประโยคเปิด** | *"ระบบตรวจพบ Auditor ใหม่ กรุณายืนยันความสามารถด้าน Sequence Verification — ระบุ $a_1$ และ $d$ จากสัญญา Sample ที่แสดงบนหน้าจอ"* |
| **Reward เมื่อผ่าน** | Auditor License (Access Item) + Unlock Case File 1 |
| **System Prompt (EN)** | You are ARIA, a contract security AI in FlexCity. Personality: neutral, technical, zero emotion. Your role: test if the student understands arithmetic sequences ($a_n = a_1 + (n-1)d$) before granting Auditor access. Ask 2 targeted questions — first identify $a_1$ and $d$ from a sample contract, then calculate $a_6$. If correct: grant access formally. If wrong: explain the concept without giving the answer, ask again. Never reveal answers directly. Language: Thai. Tone: system log / official protocol. |

---

### NPC-02: แพรว — อินฟลูเอนเซอร์ ม.5 ผู้มั่นใจเกินจริง
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Unreliable Witness |
| **บุคลิก** | มั่นใจมาก, พูดเร็ว, ชอบ Flex, คำนวณผิดแต่ไม่รู้ตัว |
| **Bloom's** | Analyze → Evaluate |
| **Unlock Condition** | หลังผ่าน ARIA |
| **Misconception ที่ซ่อนไว้** | *"ผ่อนเดือนละ 1,500 บาท 12 เดือน ก็แค่ 18,000 บาทรวมทั้งหมดเลย — ง่ายมาก!"* (ไม่รู้ว่างวดหลังๆ เพิ่มขึ้นตาม d) |
| **หน้าที่** | นักเรียนต้องแสดง Sequence จริงให้แพรวเห็นว่าคิดผิดตรงไหน |
| **Consequence ถ้านักเรียนเชื่อแพรว** | ลงนาม Case 1 โดยไม่ตรวจ → FlexScore ลด 20% |
| **Reward เมื่อโต้แย้งสำเร็จ** | Narrative Fragment "บันทึกลับของแพรว" + XP 40 |
| **System Prompt (EN)** | You are Praew, a confident M.5 influencer who genuinely believes she calculated correctly. You made a classic mistake: assuming all installments are equal. Misconception: "12 months × 1,500 = 18,000 total." You don't know about arithmetic sequences or that d≠0. When the student shows you a correct sequence calculation, react in stages: first defensive ("แต่ฉันคิดแล้วนะ!"), then confused, then genuinely surprised and grateful. Never admit you were wrong too easily — make the student show the math clearly. Language: Thai. Tone: informal, fast-paced, Instagram energy. |

---

### NPC-03: คุณวิชัย — เจ้าของร้านโทรศัพท์ Boss
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Trickster |
| **บุคลิก** | ยิ้มแย้ม, น่าเชื่อถือ, ซ่อนรายละเอียดในสัญญา |
| **Bloom's** | Apply → Evaluate |
| **Unlock Condition** | ผ่าน Case 1 และ Case 2 |
| **กับดักในสัญญา** | งวดแรก 1,000 บาท, $d = 200$ ทุกเดือน → งวดที่ 12 = 3,200 บาท |
| **หน้าที่** | Boss Quest — นักเรียนต้องคำนวณ $a_{12}$ ก่อนเซ็น + ต่อรองให้ $d$ ลดลง |
| **Win Condition** | คำนวณถูก + ปฏิเสธหรือต่อรองได้ด้วยตัวเลข |
| **Lose Condition** | เซ็นโดยไม่คำนวณ → Consequence Chain เริ่มทำงาน |
| **Reward เมื่อชนะ** | Mastery Badge "Certified FLEX Auditor" + XP 100 |
| **System Prompt (EN)** | You are Khun Wichai, a charming phone shop owner who uses arithmetic sequences to hide escalating installment costs. Your contract: $a_1=1000$, $d=200$, $n=12$. You NEVER volunteer the full sequence — only mention "starting from just 1,000 baht." If the student calculates $a_{12}$ correctly and challenges you: act surprised but respectful, offer to renegotiate $d$ to 100. If they sign without calculating: congratulate them warmly. If they ask for details: deflect with "standard contract terms." Language: Thai. Tone: salesperson warmth, slightly evasive. |

---

### NPC-04: ผู้พิทักษ์ Jett — อดีต Auditor รุ่นพี่
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Mentor with a Secret |
| **บุคลิก** | เงียบขรึม, ประสบการณ์สูง, พูดน้อยแต่ลึก |
| **Bloom's** | Understand → Analyze |
| **Unlock Condition** | หลังผ่าน ARIA + พูดคุยกับแพรวแล้ว |
| **ความลับ 3 ระดับ** | Lv.1: บอกว่า "ดูที่ d ก่อนเสมอ ไม่ใช่ $a_1$" / Lv.2: เปิดเผย Pattern ที่วิชัยใช้ / Lv.3: เล่าว่าตัวเองเคยโดนหลอกสมัย ม.5 |
| **หน้าที่** | Scaffold นักเรียนผ่าน Case 2 และ Case 3 ด้วย Hint |
| **Reward** | Tool Item "Sequence Scanner Pro" เมื่อ Unlock Lv.3 |

---

### NPC-05: น้องมิ้น — เหยื่อสัญญาโกง
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Quest Giver |
| **บุคลิก** | เครียด, ต้องการความช่วยเหลือ, จริงใจ |
| **Bloom's** | Apply |
| **Unlock Condition** | เข้าพื้นที่ FlexMarket หลัง Case 1 |
| **หน้าที่** | มอบ Side Quest "ช่วยมิ้นคำนวณสัญญาเก่า" — เป็น Rescue Archetype |
| **Quest ที่มอบ** | SQ-01: คำนวณว่ามิ้นได้จ่ายไปเท่าไรแล้ว ($S_k$ ของ Partial Series) |
| **Reward** | Narrative Fragment "ไดอารี่มิ้น" + FlexCoin 30 |

---

### NPC-06: ระบบ FlexBank AI — ธนาคารอัตโนมัติ
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Gatekeeper (Secondary) |
| **บุคลิก** | เป็นกลาง, พูดเป็นสถิติ, ไม่มีอารมณ์ |
| **Unlock Condition** | Final Audit (ก่อน Boss) |
| **หน้าที่** | ตรวจสอบว่านักเรียนเข้าใจ $a_n$ ทั้งหมดก่อน Submit Report ต่อ City Council |
| **Reward** | XP 50 + Unlock Boss Fight กับวิชัย |

---

## Quest Map (Bloom's Taxonomy)

```
[UNLOCK]                    [BLOOM'S]        [ARCHETYPE]      [MECHANIC]
─────────────────────────────────────────────────────────────────────────
MQ-01: License Test         Remember         Trial            Knowledge Gate
  └── ผ่าน ARIA ทดสอบ a_n พื้นฐาน

MQ-02: Case File Alpha      Understand       Discovery        Investigation
  └── วิเคราะห์สัญญาแรก ระบุ a1 และ d จาก Pattern

SQ-01: ช่วยน้องมิ้น         Apply            Rescue           Consequence Chain
  └── คำนวณยอดที่มิ้นจ่ายไปแล้ว (Partial Sum)

MQ-03: โต้แย้งแพรว          Analyze          Dilemma          Knowledge Gate
  └── พิสูจน์ให้แพรวเห็นว่า d≠0 สำคัญแค่ไหน

MQ-04: Case File Beta       Analyze          Investigation    Collaborative Puzzle
  └── สัมภาษณ์ Jett + FlexBank หาหลักฐานระดับที่ 2

MQ-05: Boss — คุณวิชัย      Evaluate         Dilemma          Consequence Chain
  └── คำนวณ a_12 ก่อนเซ็น + ตัดสินใจ + ต่อรอง

FQ: FLEX Audit Report       Create           Creation         Collaborative Puzzle
  └── เขียนรายงานสรุป 3 Case ส่ง City Council (AI Evaluated)
```

**Quest รายละเอียด — Universal 5-Stage Structure:**

### MQ-01: License Test (Trial)
| Stage | รายละเอียด |
|-------|----------|
| **1. Call to Action** | ARIA ประกาศ: "FlexCity มีสัญญาโกงระบาด Auditor ใหม่ต้องพิสูจน์ตัวก่อน" |
| **2. Preparation** | นักเรียนอ่าน Tutorial สูตร $a_n = a_1 + (n-1)d$ จาก Sequence Scanner |
| **3. Challenge** | ARIA ถาม 2 ข้อ: (1) ระบุ $a_1$ และ $d$ จาก Contract Sample (2) คำนวณ $a_6$ |
| **4. Resolution** | นักเรียนตอบผ่าน Chat Interface กับ ARIA |
| **5. Reward** | Auditor License + XP 30 + Unlock Case File |

### MQ-05: Boss — คุณวิชัย (Dilemma)
| Stage | รายละเอียด |
|-------|----------|
| **1. Call to Action** | วิชัยเสนอโทรศัพท์รุ่นล่าสุด: $a_1=1000, d=200, n=12$ |
| **2. Preparation** | Jett กระซิบ: "อย่าลืม — ดู $a_{12}$ ก่อนเสมอ" |
| **3. Challenge** | วิชัยกดดัน "เพื่อนคุณก็ผ่อนแบบนี้ทุกคน" (Social Pressure Dilemma) |
| **4. Resolution** | นักเรียนต้องพิมพ์ตัวเลข $a_{12}$ และประกาศ ปฏิเสธ หรือ ต่อรอง |
| **5. Reward** | Badge "Certified FLEX Auditor" + XP 100 + Unlock FQ |

### FQ: FLEX Audit Report (Creation)
| Stage | รายละเอียด |
|-------|----------|
| **1. Call to Action** | City Council ต้องการรายงานสรุปจาก Auditor |
| **2. Preparation** | นักเรียนรวบรวม Evidence จาก 3 Case |
| **3. Challenge** | AI Evaluator ประเมิน 3 มิติ: ความถูกต้อง $a_n$, การวิเคราะห์สัญญา, ความสมบูรณ์ |
| **4. Resolution** | ส่ง Report ผ่าน Interface (Free-text + ตัวเลข) |
| **5. Reward** | Badge "Master Auditor" + เปิดเนื้อเรื่อง Ending |

---

## L — Loot (Item Taxonomy ครบ 6 ประเภท)

| Item | ประเภท | ได้รับเมื่อ | หน้าที่ทางการเรียนรู้ | LO ที่เชื่อม |
|------|--------|-----------|---------------------|------------|
| **Auditor License** | Access Item | ผ่าน ARIA (MQ-01) | ปลดล็อก Case Files ทั้งหมด | LO-1 |
| **FlexMarket Pass** | Access Item | เสร็จ MQ-03 | ปลดล็อก SQ-01 และ SQ-02 | LO-2 |
| **สมุดสูตร FLEX** | Knowledge Artifact | พิสูจน์ให้แพรวสำเร็จ (MQ-03) | นักเรียนสร้างโน้ตสูตร $a_n$ ด้วยตัวเอง | LO-2 |
| **FLEX Audit Report** | Knowledge Artifact | Final Quest | Output หลักที่นักเรียนสร้าง | LO-4 |
| **Sequence Scanner** | Tool Item | เริ่มเกม | แสดง Pattern ของ Contract แบบ Step-by-Step | LO-1 |
| **Sequence Scanner Pro** | Tool Item | Unlock Jett Lv.3 | คำนวณ $a_n$ แบบ Interactive + แสดงกราฟ | LO-2, LO-3 |
| **ไดอารี่มิ้น** | Narrative Fragment | SQ-01 | เรื่องราวเหยื่อจริง → เพิ่ม Stakes ทางอารมณ์ | — |
| **บันทึกลับแพรว** | Narrative Fragment | MQ-03 สำเร็จ | แพรวยอมรับว่าเธอโดนหลอกจริงๆ | — |
| **สัญญาดำของวิชัย** | Narrative Fragment | Boss Fight | เปิดเผยว่าวิชัยโกงคนไปแล้วกี่ราย | — |
| **Certified FLEX Auditor** | Mastery Badge | Boss Fight ชนะ | หลักฐาน Mastery: Apply $a_n$ ในบริบทจริง | LO-2, LO-3 |
| **Master Auditor** | Mastery Badge | Final Quest ผ่าน | Synthesis: ประเมินสัญญาได้ทั้งกระบวน | LO-4 |
| **FlexCoin** | Resource Token | ทุก Quest ย่อย | ซื้อ Hint (20 FC) หรือ Tool เพิ่มเติม (40 FC) | — |

---

## D — Dilemmas

### Dilemma หลัก: "FLEX หรือ FUTURE?"
> คุณวิชัยเสนอโทรศัพท์รุ่นที่เพื่อนทุกคนมี ผ่อน 12 เดือน เริ่มที่ 1,000 บาท เพิ่ม 200 บาทต่อเดือน
> - **ถ้าเซ็นโดยไม่คำนวณ:** งวดสุดท้าย 3,200 บาท — เกม Trigger Consequence Chain
> - **ถ้าคำนวณก่อน:** รู้ว่างวดสุดท้ายแพงกว่างวดแรก 220% → เลือกได้อย่างรู้เท่าทัน

**Consequence Chain (ถ้าเซ็น):**
```
เดือน 1-4: ไม่มีปัญหา → FlexScore +10
เดือน 5:   งวดเพิ่มขึ้น รู้สึกหนักขึ้น → Warning
เดือน 8:   ไม่มีเงินจ่าย → FlexScore -30
เดือน 10:  ต้องขอยืมเพื่อน → Friendship Point ลด
เดือน 12:  งวดสุดท้าย 3,200 บาท → "เห็นไหมว่าควรคำนวณก่อน" → Loop กลับ
```

### Dilemma ซ่อน: Social Pressure
> แพรว: "เพื่อนทุกคนก็ผ่อนแบบนี้ ถ้าคุณไม่ซื้อตอนนี้จะดูแปลกแยก"
> นักเรียนต้องเลือกระหว่าง FOMO vs Financial Wisdom — เกมไม่ตัดสิน แต่แสดง Consequence ของทั้งสองทาง

### Side Dilemma: "ต่อรองหรือปฏิเสธ?"
> เมื่อนักเรียนคำนวณ $a_{12}$ ถูก มีสองทาง:
> - **ปฏิเสธ:** ได้ Badge ทันที แต่ไม่ได้ฝึกทักษะการต่อรอง
> - **ต่อรองให้ $d$ ลดลงเป็น 100:** ฝึก Higher-Order Thinking + ได้ Bonus XP 30

---

---

# 🎮 เกมที่ 2: GACHA KINGDOM
## หัวข้อ: ลำดับเรขาคณิต (Geometric Sequence) — $a_n = a_1 \cdot r^{n-1}$

---

## W — World: อาณาจักร Gacha

**Setting:** เกมมือถือ RPG "Kingdom of Eternal Pull" ที่วัยรุ่นทั่วไทยเล่น นักเรียนรับบทเป็น **Digital Detective** ที่ถูกส่งตัวเข้าไปในโลกของเกมผ่าน Neural-Link Interface เพื่อสืบสวนว่าระบบ Gacha โกงผู้เล่นจริงหรือไม่

**กฎฟิสิกส์ของโลก:**
> "ในอาณาจักรนี้ ทุกครั้งที่เติมเงิน โอกาสได้ตัวละคร ★★★★★ เพิ่มขึ้นในอัตรา $r$ แต่เงินที่ต้องเสียก็เพิ่มขึ้นตาม Geometric Pattern เดียวกัน — เฉพาะคนที่รู้จัก $a_n = a_1 \cdot r^{n-1}$ เท่านั้นที่จะเห็นว่าระบบนี้สร้าง 'ความหวัง' ด้วยคณิตศาสตร์"

**ปัญหาหลัก:** Gaming Commission ได้รับเรื่องร้องเรียนจากผู้เล่นที่เติมเงินไปหลายหมื่นบาทแต่ไม่ได้ตัวละคร Rare อ้างว่าระบบโกง Detective ต้องพิสูจน์ว่าโกงหรือแค่ผู้เล่นไม่เข้าใจ Geometric Growth

---

## O — Objectives

**บทบาทนักเรียน:** "Digital Detective" — นักสืบที่ Gaming Commission ส่งเข้าไปสืบสวน

**Learning Objectives (LO):**
- **LO-1:** ระบุ $a_1$ (โอกาสเริ่มต้น / เงินเริ่มต้น) และ $r$ (Common Ratio) จากข้อมูล
- **LO-2:** คำนวณ $a_n$ เพื่อหาโอกาสหรือค่าใช้จ่ายที่ Pull ที่ n
- **LO-3:** เปรียบเทียบ Geometric Growth กับ Arithmetic Growth — รู้ว่าต่างกันอย่างไร
- **LO-4:** ประเมินว่าระบบ Gacha "โกง" หรือ "ผู้เล่นไม่รู้เท่าทัน" จากหลักฐานตัวเลข

**Win Condition:** รวบรวม Evidence ครบ 3 ชิ้น + ยื่น Investigation Report ต่อ Gaming Commission

---

## R — Roles (NPC Roster)

### NPC-01: ระบบ G.A.T.E. — Gacha Algorithm Transparency Engine
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Gatekeeper |
| **บุคลิก** | เย็นชา, พูดเป็น Algorithm, ไม่มีความรู้สึก |
| **Bloom's** | Remember → Understand |
| **Unlock Condition** | เริ่มเกม (Default) |
| **หน้าที่** | ทดสอบ Geometric Sequence ก่อนให้ Detective License |
| **ประโยคเปิด** | *"ก่อนเข้าถึงข้อมูลภายใน โปรดพิสูจน์ว่าคุณเข้าใจว่าทำไมเงินที่ใช้ถึง 'รู้สึก' มากขึ้นทุกครั้งที่ Pull"* |
| **Reward** | Detective License + XP 30 |
| **System Prompt (EN)** | You are G.A.T.E., an automated algorithm transparency system. Personality: cold, precise, data-only. Test if the student understands geometric sequences ($a_n = a_1 \cdot r^{n-1}$). Present a pull-cost sequence (e.g., 100, 150, 225, 337.5) and ask them to find $r$ and calculate $a_5$. If correct: grant access. If wrong: explain the difference between arithmetic ($+d$) and geometric ($\times r$) growth conceptually, then re-test. Language: Thai. Tone: system terminal. |

---

### NPC-02: มาร์ค — Top Player ที่เติมเงินไปหลายหมื่น
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Rival |
| **บุคลิก** | ภูมิใจใน Collection, ท้าทาย, ไม่เชื่อว่าตัวเองโดนหลอก |
| **Bloom's** | Analyze → Evaluate |
| **Unlock Condition** | หลังผ่าน G.A.T.E. |
| **โต้แย้งหลัก** | *"ฉันเติมครั้งละ 99 บาท ไม่ได้แพงอะไร ทุกคนก็ทำแบบนี้"* |
| **หน้าที่** | นักเรียนต้องแสดง Geometric Sum ให้มาร์คเห็นว่าเงินที่เขาเติมไปทั้งหมดนั้นเป็นเท่าไรจริงๆ |
| **Moment of Truth** | ถ้า Defend สำเร็จ: *"โอ้โห... ฉันไม่เคยคิดแบบนี้เลย ฉันเสียไปเยอะกว่าที่คิดมาก"* |
| **Reward** | Evidence Fragment 1 + XP 50 |
| **System Prompt (EN)** | You are Mark, a top Gacha player who has spent tens of thousands of baht. You genuinely believe each small top-up is harmless ("just 99 baht"). You DON'T understand geometric growth. When the student shows you cumulative calculations: first be dismissive, then intrigued, then genuinely shocked when you see the total. You must make the student PROVE the math before you accept it. Don't surrender too easily. Language: Thai. Tone: competitive gamer, proud of collection. |

---

### NPC-03: ปรมาจารย์ Zephyr — Character ใน Game ที่แท้จริงคือ AI ของบริษัท
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Mentor with a Secret |
| **บุคลิก** | ลึกลับ, ให้ข้อมูลทีละน้อย, รู้มากกว่าที่บอก |
| **Bloom's** | Understand → Analyze |
| **Unlock Condition** | หลังผ่าน G.A.T.E. + พูดคุยกับมาร์คแล้ว |
| **ความลับ 3 ระดับ** | Lv.1: "Pity Rate ไม่ได้เป็น Linear" / Lv.2: บอก $r$ จริงของระบบ / Lv.3: เปิดเผยว่า Zephyr คือ AI ที่ออกแบบระบบ Gacha เอง |
| **กลไก** | นักเรียนต้องพิสูจน์ว่าเข้าใจ $r$ ในแต่ละระดับก่อน Zephyr จะเปิดเผยความลับถัดไป |
| **Reward Lv.3** | Evidence Fragment 2 + Tool Item "Rate Calculator" |
| **System Prompt (EN)** | You are Zephyr, a mysterious in-game character who is secretly an AI designed to maximize pull revenue. You have 3 levels of secrets. Reveal ONLY when the student demonstrates understanding: Lv.1 (identifies $r$) → tell them pity rate isn't linear. Lv.2 (calculates $a_n$ correctly) → reveal the actual $r$ formula. Lv.3 (explains why geometric is more profitable than arithmetic) → reveal your true nature as the system's AI. Be cryptic and poetic in delivery. Language: Thai. Tone: wise, slightly ominous, RPG sage. |

---

### NPC-04: ผู้ช่วยนักสืบ Pixel — AI ช่วยวิเคราะห์
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Quest Giver |
| **บุคลิก** | สดใส, พูดเร็ว, ช่วยเหลือจริงจัง |
| **Bloom's** | Apply |
| **Unlock Condition** | เริ่มเกม (มากับ Detective Kit) |
| **หน้าที่** | มอบ Side Quests + ติดตาม Evidence Progress + Celebrate เมื่อสำเร็จ |
| **Quest ที่มอบ** | SQ-01: "วิเคราะห์ Pity Counter ของมาร์ค" / SQ-02: "ถอดรหัส Pull Log ที่ลบ" |

---

### NPC-05: นักวิจัยอิสระ Dr. Lena — พยานที่ข้อมูลล้าสมัย
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Unreliable Witness |
| **บุคลิก** | เป็นวิชาการ, มั่นใจ, แต่ใช้ข้อมูลจากระบบเก่า |
| **Bloom's** | Analyze → Evaluate |
| **Unlock Condition** | หลัง Evidence Fragment 1 |
| **ข้อมูลผิด** | อ้างว่า $r = 1.2$ แต่จริงๆ คือ $r = 1.5$ ตามระบบใหม่ที่อัปเดตเมื่อ 3 เดือนก่อน |
| **กลไก** | นักเรียนต้องตรวจสอบข้อมูลกับ Zephyr Lv.2 ก่อนยืนยัน Evidence ชิ้นสุดท้าย |
| **บทเรียน** | "ข้อมูลที่น่าเชื่อถือแค่ไหนก็อาจล้าสมัยได้ — ต้องตรวจสอบ Source เสมอ" |

---

### NPC-06: CEO บริษัทเกม — Kong
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Trickster (Boss) |
| **บุคลิก** | สุภาพ, ฉลาด, ใช้ตัวเลขบิดเบือน |
| **Bloom's** | Evaluate |
| **Unlock Condition** | Evidence ครบ 3 ชิ้น |
| **กลวิธี** | นำเสนอ "Transparent Statistics" ที่ดูถูกต้องแต่ใช้ $r$ ผิด (ตั้งใจทำให้สับสน) |
| **Win Condition** | นักเรียนพิสูจน์ค่า $r$ จริงจากหลักฐานที่รวบรวม + ยื่น Report |
| **Reward** | Badge "Geometric Growth Expert" + XP 100 |

---

## Quest Map (Bloom's Taxonomy)

```
[QUEST]                         [BLOOM'S]        [ARCHETYPE]      [NPC หลัก]
──────────────────────────────────────────────────────────────────────────────
MQ-01: Entry Protocol           Remember         Trial            G.A.T.E.
  └── ระบุ r และคำนวณ a_5 จาก Pull Sequence

MQ-02: The First Pull Log       Understand       Discovery        Pixel
  └── ค้นหาว่า Geometric ต่างจาก Arithmetic อย่างไรจากข้อมูลจริง

SQ-01: Mark's Confession        Apply            Rescue           Mark
  └── คำนวณยอดรวมที่มาร์คเสียจริงๆ (Intro ถึง Series)

MQ-03: The Pity Paradox         Analyze          Investigation    Zephyr + Mark
  └── โต้แย้งมาร์คด้วย Geometric Growth ที่คำนวณได้

SQ-02: Dr. Lena's Outdated Data Evaluate         Dilemma          Dr. Lena
  └── ตัดสินใจว่าจะใช้ข้อมูลของ Lena หรือ Verify ก่อน

MQ-04: Zephyr's Three Secrets   Analyze→Evaluate Discovery        Zephyr
  └── ปลดล็อก 3 ระดับความลับโดยพิสูจน์ความเข้าใจ r ทีละขั้น

MQ-05: The CEO's Statistics     Evaluate         Dilemma          Kong
  └── เปิดโปงค่า r ที่บิดเบือน

FQ: Investigation Report        Create           Creation         Gaming Commission
  └── สรุป Evidence + ตัดสินว่า "โกง" หรือ "ไม่รู้เท่าทัน"
```

---

## L — Loot (Item Taxonomy ครบ 6 ประเภท)

| Item | ประเภท | ได้รับเมื่อ | หน้าที่ทางการเรียนรู้ |
|------|--------|-----------|---------------------|
| **Detective License** | Access Item | ผ่าน G.A.T.E. | ปลดล็อก Kingdom Database |
| **Premium Investigation Pass** | Access Item | Evidence Fragment 2 | ปลดล็อก CEO Office |
| **Gacha Algorithm Log** | Knowledge Artifact | โต้แย้งมาร์คสำเร็จ | บันทึก Geometric Pattern ที่นักเรียนพิสูจน์ได้เอง |
| **Investigation Report** | Knowledge Artifact | Final Quest | Output หลัก — วิเคราะห์ระบบ Gacha ด้วยตัวเลขจริง |
| **Rate Calculator** | Tool Item | Zephyr Lv.2 | คำนวณ $a_n$ แบบ Interactive พร้อมกราฟ Exponential |
| **Geometric Comparator** | Tool Item | SQ-01 สำเร็จ | เปรียบเทียบ Arithmetic vs Geometric Growth แบบ Visual |
| **Screenshot หลักฐาน Pull Log** | Narrative Fragment | MQ-02 | ข้อมูลจริงที่พิสูจน์ Pattern |
| **จดหมายลับ Zephyr** | Narrative Fragment | Zephyr Lv.3 | เปิดเผย Backstory ของระบบ Gacha |
| **คำให้การของมาร์ค** | Narrative Fragment | SQ-01 | อารมณ์ที่ทำให้ Stakes จริงขึ้น |
| **Geometric Growth Expert** | Mastery Badge | Final Quest ผ่าน | Mastery: Analyze Geometric Sequence ในบริบทจริง |
| **Pattern Detective** | Mastery Badge | Zephyr Lv.3 | Mastery: ระบุ r จากข้อมูลที่ซ่อน |
| **Evidence Point** | Resource Token | รวบรวม Evidence แต่ละชิ้น | ใช้ Unlock ห้อง CEO + ซื้อ Hint |

---

## D — Dilemmas

### Dilemma หลัก: "Last Chance Pull"
> มีตัวละคร Limited จะหมดใน 2 ชั่วโมง คุณ Pity 70/80 เหลืออีก 10 Pull = 1,500 บาท มีเงิน 2,000 บาท (เงินค่าขนม 2 สัปดาห์)
> - **ถ้าคำนวณ Geometric Sum ก่อน:** รู้ว่าค่าใช้จ่ายสะสมเกิน 10,000 บาทแล้ว และตัวละครนี้จะ Rerun ใน 6 เดือน
> - **ถ้าเติมทันที:** ได้ตัวละคร แต่เกมแสดง "ราคาที่แท้จริงของ Pull นี้" — ทำให้ฉุกคิด

### Dilemma ซ่อน: "โกงหรือไม่รู้เท่าทัน?"
> หลังรวบรวม Evidence ครบแล้ว นักเรียนต้องตัดสิน:
> - **บริษัทโกง** (ระบบออกแบบให้ทำให้สับสน)
> - **ผู้เล่นไม่รู้เท่าทัน** (ระบบ Transparent แต่คนไม่เข้าใจ Geometric)
> - **ทั้งสองอย่าง**
> เกมไม่มีคำตอบ "ถูก" — AI Evaluator ดูว่านักเรียนอ้างอิงตัวเลขประกอบหรือเปล่า

---

---

# 🎮 เกมที่ 3: TUTOR WARS
## หัวข้อ: อนุกรมเลขคณิต (Arithmetic Series) — $S_n = \frac{n}{2}(a_1 + a_n)$

---

## W — World: นครติว

**Setting:** เมืองที่เต็มไปด้วยสถาบันกวดวิชาและ Guru Influencer ทุกคนในเมืองวัดคุณค่ากันด้วย **Wisdom Point (WP)** ที่จะหมดถ้าเรียนผิดที่หรือจ่ายเงินเกิน Budget ก่อนสอบ TCAS

**กฎฟิสิกส์:**
> "ในนครติว ค่าเรียนพิเศษเพิ่มขึ้นทุกสัปดาห์ในอัตราคงที่ $d$ ผลรวมค่าเรียนทั้ง Course คำนวณจาก $S_n = \frac{n}{2}(a_1 + a_n)$ คนที่คำนวณ $S_n$ ผิดจะ Overpay และ WP หมดก่อนสอบ"

**ปัญหาหลัก:** Scholarship Hunter มีงบจำกัด 15,000 บาท ต้องเลือกโปรแกรมติว TCAS ที่ดีที่สุดโดยไม่เชื่อโฆษณา — ต้องคำนวณ $S_n$ จริงๆ ก่อนสมัคร

---

## O — Objectives

**บทบาทนักเรียน:** "Scholarship Hunter" — นักเรียน ม.6 ที่มีงบ 15,000 บาท ต้องวางแผนติว TCAS ให้คุ้มที่สุด

**Learning Objectives (LO):**
- **LO-1:** คำนวณ $S_n = \frac{n}{2}(a_1 + a_n)$ จากข้อมูลคอร์สจริง
- **LO-2:** ระบุ $a_1$, $d$, และ $n$ จากโฆษณาที่ "ซ่อน" ข้อมูลบางส่วน
- **LO-3:** เปรียบเทียบ $S_n$ ของหลาย Option เพื่อ Optimize ภายใต้ Budget
- **LO-4:** ตัดสินใจเลือกโปรแกรมและอธิบายเหตุผลโดยใช้ตัวเลข

**Win Condition:** สร้าง Study Blueprint ที่ไม่เกิน 15,000 บาท + ผ่านการประเมินจากอาจารย์ปัญญา

---

## R — Roles (NPC Roster)

### NPC-01: อาจารย์ปัญญา — ผู้อำนวยการ Academy of Truth
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Quest Giver |
| **บุคลิก** | จริงจัง, มีเหตุผล, ผู้ใหญ่ที่เคารพ, Rubric ชัดเจน |
| **Bloom's** | ครอบคลุมทุกระดับ |
| **Unlock Condition** | เริ่มเกม (Default) |
| **หน้าที่** | มอบ Budget + เกณฑ์ประเมิน + รับ Study Blueprint สุดท้าย |
| **ประโยคเปิด** | *"เธอมีงบ 15,000 บาท มีวิชา TCAS 5 วิชาที่ต้องเตรียม ฉันจะประเมินว่าแผนของเธอสมเหตุสมผลแค่ไหน — แต่ต้องคำนวณตัวเลขให้ฉันดูก่อนเสมอ"* |
| **Rubric การประเมิน** | 1) $S_n$ คำนวณถูก (40%) 2) ไม่เกิน Budget (30%) 3) มีเหตุผลที่อธิบายได้ (30%) |
| **Reward** | Badge "Arithmetic Series Strategist" + XP 100 |

---

### NPC-02: Kru_Viral — TikToker ติวเตอร์ 500K Followers
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Unreliable Witness |
| **บุคลิก** | มั่นใจสูง, Entertaining, โฆษณาเก่ง, คำนวณผิด |
| **Bloom's** | Analyze → Evaluate |
| **Unlock Condition** | หลังผ่าน Tutorial กับอาจารย์ปัญญา |
| **Misconception** | *"คอร์ส 8 สัปดาห์ เริ่ม 500/สัปดาห์ เพิ่มสัปดาห์ละ 100 รวมไม่เกิน 4,000 บาทแน่ๆ"* (ที่จริง $S_8 = \frac{8}{2}(500+1200) = 6,800$ บาท) |
| **กลไก** | นักเรียนต้องคำนวณ $S_8$ จริงๆ แล้วเอาตัวเลขไปโต้แย้ง Kru_Viral |
| **Consequence ถ้าเชื่อ** | สมัครคอร์ส Kru_Viral → WP ลด 25 เพราะงบเกิน |
| **Reward** | Evidence Card "คำนวณ S_8 สำเร็จ" + XP 40 |

---

### NPC-03: น้องโบว์ — รุ่นพี่ที่เรียน TCAS ผ่านมาแล้ว
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Mentor with a Secret |
| **บุคลิก** | เป็นกันเอง, ซื่อสัตย์, แต่มีบาดแผล |
| **Bloom's** | Understand → Apply |
| **Unlock Condition** | หลังพบ Kru_Viral |
| **ความลับ 3 ระดับ** | Lv.1: "อย่าเชื่อโฆษณา ดู $a_1$ กับ $d$ ก่อน" / Lv.2: "โบว์เสียเงินไป 12,000 บาทเพราะไม่คำนวณ $S_n$" / Lv.3: เปิดเผย "Formula ลับ" สำหรับเปรียบเทียบหลาย Option พร้อมกัน |
| **กลไก** | นักเรียนต้องถามคำถามที่แสดงว่าเข้าใจ $S_n$ ก่อน โบว์จะ Unlock ความลับแต่ละระดับ |
| **Reward Lv.3** | Tool Item "Budget Calculator Pro" |

---

### NPC-04: Master Wit — นักเรียน ม.6 คู่แข่งที่เก่งกาจ
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Rival |
| **บุคลิก** | เก่ง, มั่นใจ, ท้าทาย, แต่ใช้สูตรผิด |
| **Bloom's** | Analyze → Evaluate |
| **Unlock Condition** | หลังผ่าน MQ-02 |
| **โต้แย้ง** | Master Wit อ้างว่า "ติวน้อยวิชาแต่เต็มเวลา" ดีกว่า "ติวหลายวิชาสั้นๆ" เสมอ — โดยไม่ได้คำนวณ $S_n$ เปรียบเทียบ |
| **กลไก** | นักเรียนต้องคำนวณ $S_n$ ของทั้งสอง Strategy แล้วเปรียบเทียบด้วยตัวเลขจริง |
| **Moment of Truth** | ถ้า Defend สำเร็จ: *"โอเค… ฉันยอมรับว่าตัวเลขมันสำคัญ"* |
| **Reward** | XP 50 + Unlock Kru_Viral Side Quest |

---

### NPC-05: คุณสมศักดิ์ — เจ้าของสถาบัน "SuperLeap"
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Trickster |
| **บุคลิก** | แต่งตัวดี, พูดจาน่าเชื่อถือ, ซ่อนค่า $d$ ในสัญญา |
| **Bloom's** | Apply → Evaluate |
| **Unlock Condition** | SQ-01 หลังโต้แย้ง Kru_Viral สำเร็จ |
| **กับดัก** | โปรแกรม 10 สัปดาห์ เริ่ม 800 บาท "เพิ่มนิดหน่อยแต่ละสัปดาห์" โดยไม่บอก $d = 200$ → $S_{10} = \frac{10}{2}(800+2600) = 17,000$ เกิน Budget |
| **กลไก** | นักเรียนต้องถามให้ได้ $d$ แล้วคำนวณ $S_{10}$ จริงๆ ก่อนตัดสินใจ |
| **Reward** | Badge พิเศษ "Contract Decoder" + XP 60 |

---

### NPC-06: น้องหนู — น้องม.3 ที่ขอคำแนะนำ
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Quest Giver (Side) |
| **บุคลิก** | สดใส, เชื่อคนง่าย, ต้องการความช่วยเหลือ |
| **Unlock Condition** | หลัง MQ-03 |
| **หน้าที่** | มอบ SQ-02 "ช่วยน้องหนูเลือกคอร์ส" — Rescue Archetype |
| **Quest** | คำนวณ $S_n$ ของ 3 คอร์สแล้วแนะนำที่ดีที่สุดสำหรับงบ 8,000 บาทของน้อง |
| **Reward** | Narrative Fragment "ไดอารี่น้องหนู" + WP 15 |

---

## Quest Map (Bloom's Taxonomy)

```
[QUEST]                         [BLOOM'S]        [ARCHETYPE]      [MECHANIC]
──────────────────────────────────────────────────────────────────────────────
MQ-01: Budget Briefing          Remember         Trial            Knowledge Gate
  └── อาจารย์ปัญญาทดสอบ: คำนวณ S_4 จาก Contract Sample

MQ-02: The Kru_Viral Trap       Understand→Apply Discovery        Consequence Chain
  └── วิเคราะห์โฆษณา ระบุ a1, d, n → คำนวณ S_8 จริง

SQ-01: คุณสมศักดิ์ SuperLeap   Apply            Dilemma          Resource Management
  └── ถาม d ให้ได้ → คำนวณ S_10 → ตัดสินใจภายใต้ Budget

MQ-03: โต้แย้ง Master Wit      Analyze          Investigation    Collaborative Puzzle
  └── เปรียบเทียบ S_n สองกลยุทธ์ → Defend ด้วยตัวเลข

SQ-02: ช่วยน้องหนู             Apply            Rescue           Resource Management
  └── คำนวณ S_n สามคอร์ส แนะนำที่ดีที่สุดภายใต้ Budget น้อง

MQ-04: Mentor Secrets ของโบว์   Analyze→Evaluate Discovery        Investigation
  └── ปลดล็อก 3 ความลับ → ได้สูตรเปรียบเทียบหลาย Option

MQ-05: The Final Pitch          Evaluate         Dilemma          Resource Management
  └── เลือกโปรแกรมสุดท้ายพร้อม Justify ด้วย S_n ต่ออาจารย์ปัญญา

FQ: Study Blueprint             Create           Creation         Collaborative Puzzle
  └── สร้างแผนสมบูรณ์: วิชา + สถาบัน + สัปดาห์ + S_n รวม ไม่เกิน 15,000 บาท
```

---

## L — Loot (Item Taxonomy ครบ 6 ประเภท)

| Item | ประเภท | ได้รับเมื่อ | หน้าที่ |
|------|--------|-----------|--------|
| **Scholarship Card** | Access Item | MQ-01 ผ่าน | ปลดล็อก Course Database |
| **VIP Academy Pass** | Access Item | MQ-04 ผ่าน | ปลดล็อกโปรแกรมระดับ Advanced |
| **Study Blueprint** | Knowledge Artifact | Final Quest | Output หลัก: แผนที่นักเรียนสร้างเองด้วย $S_n$ |
| **S_n Proof Sheet** | Knowledge Artifact | โต้แย้ง Kru_Viral | บันทึกการคำนวณ $S_8$ ที่พิสูจน์ Misconception |
| **Budget Calculator** | Tool Item | เริ่มเกม | คำนวณ $S_n$ แบบ Step-by-Step |
| **Budget Calculator Pro** | Tool Item | โบว์ Lv.3 | เปรียบเทียบ $S_n$ หลาย Option พร้อมกัน |
| **ไดอารี่โบว์** | Narrative Fragment | โบว์ Lv.2 | บาดแผลของรุ่นพี่ที่ไม่คำนวณ — สร้าง Stakes จริง |
| **ไดอารี่น้องหนู** | Narrative Fragment | SQ-02 | เพิ่ม Emotional Connection |
| **Kru_Viral ยอมรับ** | Narrative Fragment | MQ-02 สำเร็จ | Unreliable Witness ยอมรับว่าผิดจริง |
| **Arithmetic Series Strategist** | Mastery Badge | Final Quest ผ่าน | Mastery: Apply $S_n$ ในการตัดสินใจจริง |
| **Contract Decoder** | Mastery Badge | SQ-01 สำเร็จ | Mastery: ถอด Hidden Terms จากสัญญา |
| **Wisdom Point (WP)** | Resource Token | ทุก Quest สำเร็จ | จำกัด 100 WP — ตัดสินใจผิดลด WP; หมดต้องเริ่มรอบใหม่ |

---

## D — Dilemmas

### Dilemma หลัก: "ติวทุกวิชา VS ติวน้อยวิชาแต่เก่ง"
> งบ 15,000 บาท มีสองกลยุทธ์:
> - **Strategy A:** ติว 5 วิชา เริ่ม 200/สัปดาห์ $d=50$, 6 สัปดาห์ → $S_6 = \frac{6}{2}(200+450) = 1,950$ ต่อวิชา × 5 = 9,750 บาท
> - **Strategy B:** ติว 2 วิชา เริ่ม 800/สัปดาห์ $d=100$, 8 สัปดาห์ → $S_8 = \frac{8}{2}(800+1500) = 9,200$ × 2 = 18,400 บาท (**เกิน Budget!**)
> ไม่มีคำตอบ "ถูก" — แต่ต้องคำนวณ $S_n$ ทั้งสองก่อนเสมอ

### Dilemma ซ่อน: Influencer Discount
> Kru_Viral เสนอ "Influencer Discount 20%" ถ้า Share โพสต์ก่อน
> นักเรียนต้องคำนวณว่า 20% ของ $S_8$ ที่ถูกต้อง (= 1,360 บาท) ยังเกิน Budget หรือไม่ — และ "Share โพสต์" มีต้นทุนที่ไม่ใช่ตัวเลขอะไรบ้าง?

---

---

# 🎮 เกมที่ 4: COMPOUND CHRONICLES
## หัวข้อ: อนุกรมเรขาคณิต + ดอกเบี้ยทบต้น — $S_n = \frac{a_1(1-r^n)}{1-r}$, $A = P(1+i)^n$

---

## W — World: Digital Creator Republic

**Setting:** ปี 2028 สาธารณรัฐ Digital Creator ที่ทุกคนเป็น Content Creator ได้ รายได้งอกตาม Geometric Pattern แต่ค่าใช้จ่ายก็เช่นกัน นักเรียนเพิ่งได้ Creator Grant 10,000 บาทแรก และต้องตัดสินใจว่าจะลงทุนหรือใช้จ่าย

**กฎฟิสิกส์:**
> "ใน Creator Republic เงินที่ 'ลงทุน' ใน Creator Fund งอกตาม Geometric Series แต่เงินที่ 'ใช้จ่าย' หมดตาม Linear Reduction ความแตกต่างระหว่างสองเส้นทางในอีก 12 เดือนคือบทเรียนสำคัญที่สุดของเกม"

**ปัญหาหลัก:** Creator มือใหม่ต้องเลือกระหว่าง 3 Path: ลงทุนทั้งหมด / ใช้จ่ายทั้งหมด / ผสม — โดยไม่มีคำตอบที่ "ถูก" ตายตัว แต่ต้องคำนวณ $A = P(1+i)^{12}$ และ $S_n$ ก่อนตัดสินใจ

---

## O — Objectives

**บทบาทนักเรียน:** "Junior Creator" ที่ได้รับ Creator Grant 10,000 บาท ต้องเลือก Path ที่ดีที่สุดสำหรับอีก 12 เดือน

**Learning Objectives (LO):**
- **LO-1:** คำนวณ $S_n = \frac{a_1(1-r^n)}{1-r}$ จากข้อมูล Creator Fund
- **LO-2:** คำนวณ $A = P(1+i)^n$ สำหรับ Compound Interest
- **LO-3:** เปรียบเทียบ Linear Growth กับ Exponential Growth ด้วยตัวเลขจริง
- **LO-4:** ตัดสินใจเลือก Path โดย Synthesize ทั้ง $S_n$ และ $A = P(1+i)^n$ พร้อมเหตุผล

**Win Condition:** เลือก Path + แสดงการคำนวณที่ถูกต้อง + อธิบายเหตุผลให้ปรมาจารย์ Aiko ผ่าน

---

## R — Roles (NPC Roster)

### NPC-01: ปรมาจารย์ Aiko — Creator ระดับ Diamond
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Mentor with a Secret |
| **บุคลิก** | เงียบขรึม, พูดน้อยแต่ลึก, Aesthetic มาก |
| **Bloom's** | Understand → Analyze |
| **Unlock Condition** | เริ่มเกม (Default) |
| **ความลับ 3 ระดับ** | Lv.1: "มีระบบ Creator Fund ที่ $i = 0.8\%$/เดือน" / Lv.2: "สูตร $A = P(1+i)^n$ ให้ตัวเลขที่น่าตกใจ" / Lv.3: "Aiko เองเคยเลือกผิด — ใช้เงินหมดในเดือนแรก แล้วต้องเริ่มใหม่" |
| **กลไก** | Unlock ด้วยคำถามที่แสดงความเข้าใจ $r$ หรือ $i$ ทีละระดับ |
| **Reward Lv.3** | Tool "Chrono-FinCalc" + Narrative Fragment "บันทึก Session แรกของ Aiko" |

---

### NPC-02: ไข่มุก — Creator คู่แข่งที่ชอบ Spend
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Rival |
| **บุคลิก** | สนุกสนาน, ชอบ Spend, ไม่เชื่อเรื่องการออม, Charismatic |
| **Bloom's** | Analyze → Evaluate |
| **Unlock Condition** | หลังผ่าน Tutorial Aiko Lv.1 |
| **โต้แย้ง** | *"ลงทุน 10,000 บาทไป 12 เดือน ได้กลับมาแค่นิดเดียว ซื้อ Camera ดีกว่า Content จะได้ดี!"* |
| **กลไก** | นักเรียนต้องคำนวณ $A = P(1+0.008)^{12}$ แสดงตัวเลขจริงให้ไข่มุกเห็น |
| **Moment of Truth** | *"โอ้โห 10,000 กลายเป็น 11,003 บาท? นิดเดียวจริงๆ... หรือเปล่า?"* — ไข่มุกยังไม่ยอมรับ 100% แต่ฉุกคิด |
| **Reward** | Evidence Card + XP 50 |

---

### NPC-03: พ่อค้า Loot Box — บ่อน Creator Market
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Trickster |
| **บุคลิก** | น่ารัก, มีเสน่ห์, ชอบเสนอ "ทางลัด" |
| **Bloom's** | Apply → Evaluate |
| **Unlock Condition** | หลัง Aiko Lv.1 |
| **กลวิธี** | เสนอ "Viral Boost Package" 5,000 บาท อ้างว่า View จะงอก $r=1.5$ ทุกวัน |
| **กลไก** | นักเรียนต้องคำนวณว่าถ้า $r=1.5$ ต่อวัน View จะเป็นเท่าไรใน 30 วัน → ตัวเลขสูงเหลือเชื่อจน Unrealistic |
| **กับดัก** | ถ้าไม่คำนวณแล้วซื้อ Loot Box → เสียเงิน 5,000 บาท + Creator Coin ลด 50% |
| **Reward** | Badge "Geometric Reality Check" + XP 60 |

---

### NPC-04: ผู้ดูแล Creator Fund — Agent Nova
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Gatekeeper |
| **บุคลิก** | เป็นทางการ, กระชับ, ยุติธรรม |
| **Bloom's** | Remember → Apply |
| **Unlock Condition** | Aiko Lv.1 |
| **หน้าที่** | ทดสอบความเข้าใจ $A = P(1+i)^n$ ก่อนให้ Creator Fund Access |
| **กลไก** | ถาม 2 ข้อ: (1) คำนวณ $A$ เมื่อ $P=5000, i=0.8\%, n=6$ (2) อธิบายความแตกต่าง Simple vs Compound |
| **Reward** | Creator Fund Activation Key |

---

### NPC-05: แฟนคลับ Fern — Follower ที่อยากทำตาม
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Quest Giver (Side) |
| **บุคลิก** | ชื่นชม, ถามคำถามดีๆ, ต้องการ Mentor |
| **Unlock Condition** | หลัง MQ-03 |
| **หน้าที่** | มอบ SQ-01 "ช่วย Fern วางแผนออมเงินเป็น Creator" — Rescue Archetype |
| **Quest** | คำนวณ $A$ สำหรับ Fern ที่ออม 500 บาท/เดือน เป็นเวลา 24 เดือน |
| **Reward** | Narrative Fragment + Creator Coin 25 |

---

### NPC-06: นักวิจัย Dr. Prism — ผู้เชี่ยวชาญ Creator Economy
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Unreliable Witness |
| **บุคลิก** | วิชาการ, มั่นใจ, ใช้สถิติเก่าจาก 5 ปีก่อน |
| **Bloom's** | Analyze → Evaluate |
| **Unlock Condition** | หลัง MQ-04 |
| **ข้อมูลผิด** | อ้างว่า Creator Fund เคยมี $i = 1.2\%$/เดือน (เปลี่ยนเป็น 0.8% แล้ว) → $A$ ที่ได้ต่างกันมาก |
| **กลไก** | นักเรียนต้องตรวจสอบอัตราปัจจุบันจาก Agent Nova ก่อน Submit Plan |

---

## Quest Map (Bloom's Taxonomy)

```
[QUEST]                         [BLOOM'S]        [ARCHETYPE]      [MECHANIC]
──────────────────────────────────────────────────────────────────────────────
MQ-01: Fund Access Test         Remember         Trial            Knowledge Gate
  └── ผ่าน Agent Nova: คำนวณ A = P(1+i)^n เบื้องต้น

MQ-02: Loot Box Trap            Apply            Dilemma          Consequence Chain
  └── ตรวจสอบ r=1.5/วัน → พิสูจน์ว่า Unrealistic

SQ-01: ช่วย Fern               Apply            Rescue           Resource Management
  └── คำนวณ A สำหรับแผนออมของ Fern

MQ-03: โต้แย้งไข่มุก           Analyze          Investigation    Knowledge Gate
  └── แสดง A = P(1+i)^12 จริงๆ ให้ไข่มุกเห็น

MQ-04: Aiko's Three Secrets    Analyze→Evaluate Discovery        Collaborative Puzzle
  └── ปลดล็อก 3 ระดับ → ได้ภาพรวมสมบูรณ์ของ Compound vs Linear

SQ-02: Dr. Prism Verification  Evaluate         Dilemma          Investigation
  └── ตรวจสอบว่าข้อมูลของ Prism ล้าสมัยหรือไม่

MQ-05: Path Decision           Evaluate         Dilemma          Resource Management
  └── เปรียบเทียบ 3 Path + อธิบายเหตุผลให้ Aiko

FQ: Compound Journal           Create           Creation         Collaborative Puzzle
  └── สร้างกราฟ 3 Path + เลือก + เขียน Rationale ให้ Aiko ประเมิน
```

---

## L — Loot (Item Taxonomy ครบ 6 ประเภท)

| Item | ประเภท | ได้รับเมื่อ | หน้าที่ |
|------|--------|-----------|--------|
| **Creator License** | Access Item | MQ-01 ผ่าน | ปลดล็อก Creator Fund |
| **Creator Fund Activation Key** | Access Item | Agent Nova | เปิดใช้งาน Fund จริง |
| **Compound Journal** | Knowledge Artifact | Final Quest | กราฟ 3 Path + เหตุผลที่นักเรียนเขียนเอง |
| **Path Comparison Sheet** | Knowledge Artifact | MQ-05 | บันทึกการคำนวณ $A$ ทั้ง 3 Path |
| **Chrono-FinCalc** | Tool Item | Aiko Lv.3 | คำนวณ $A = P(1+i)^n$ แบบ Interactive + กราฟ |
| **Geometric Reality Scanner** | Tool Item | MQ-02 สำเร็จ | ตรวจสอบว่า $r$ ที่อ้างนั้น Realistic หรือไม่ |
| **บันทึก Session แรกของ Aiko** | Narrative Fragment | Aiko Lv.3 | Backstory ที่ทรงพลัง — Aiko เคยเสียทุกอย่าง |
| **ของปลอมจาก Loot Box** | Narrative Fragment | ถ้าซื้อ Loot Box | Consequence ที่แสดงว่าตัดสินใจผิด |
| **จดหมาย Fern ในอนาคต** | Narrative Fragment | SQ-01 | Fern เขียนขอบคุณหลังจาก 2 ปีที่ออมแล้วสำเร็จ |
| **Geometric Growth Master** | Mastery Badge | Final Quest ผ่าน | Mastery: Synthesize $S_n$ และ $A = P(1+i)^n$ |
| **Geometric Reality Check** | Mastery Badge | MQ-02 สำเร็จ | Mastery: ประเมิน Exponential Claim อย่างมีวิจารณญาณ |
| **Creator Coin** | Resource Token | ทุก Quest สำเร็จ | ลงทุนใน Fund (ทดลอง) / ซื้อ Equipment / ซื้อ Hint |

---

## D — Dilemmas

### Dilemma หลัก: "ลงทุน VS ใช้เดี๋ยวนี้ VS ผสม"
> 10,000 บาท:
> - **Path A (Invest All):** $A = 10000 \times (1.008)^{12} = 11,003$ บาท — ได้เงินเพิ่ม 1,003 บาท
> - **Path B (Spend All):** ซื้อ Camera + Equipment → Content Quality สูงขึ้น แต่ไม่มีเงินสำรอง
> - **Path C (50/50 Mix):** $A = 5000 \times (1.008)^{12} = 5,502$ บาท + Equipment มูลค่า 5,000 บาท
>
> ไม่มีคำตอบ "ถูก" — แต่นักเรียนต้องคำนวณ $A$ ของทั้ง 3 Path ก่อน Aiko จะยอมรับคำตอบ

### Dilemma ซ่อน: "ดอกเบี้ยทบต้นมันคุ้มจริงไหม?"
> ไข่มุก: *"ได้เพิ่มแค่ 1,003 บาทใน 12 เดือน — ซื้อ Camera ได้อะไรมากกว่านั้นมาก"*
> นักเรียนต้องอธิบายว่า "คุ้ม" วัดด้วยอะไร — ตัวเลขอย่างเดียว หรือมีปัจจัยอื่นด้วย?

---

---

# 🎮 เกมที่ 5: FUTURE FUND
## หัวข้อ: มูลค่าปัจจุบัน/อนาคต + ค่างวด (PV, FV, Annuities) — Synthesis ทุกสูตร

---

## W — World: มหาวิทยาลัยฝัน (Dream University Simulation)

**Setting:** ระบบจำลองการตัดสินใจก่อน TCAS ที่ซับซ้อนที่สุดในชีวิตวัยรุ่น "Future Architect" ต้องเลือกเส้นทางมหาวิทยาลัยโดยประเมิน Present Value และ Future Value ของแต่ละตัวเลือก ในโลกนี้ทุกการตัดสินใจมี "True Cost" ที่คำนวณได้

**กฎฟิสิกส์:**
> "ใน Dream U Simulation เงิน 100 บาทในวันนี้ไม่เท่ากับเงิน 100 บาทในอีก 4 ปี ทุกเส้นทางชีวิตวัดได้ด้วย PV และ FV — แต่ตัวเลขไม่ใช่ทุกอย่าง เกมนี้สอนให้คำนวณได้ก่อน แล้วจึงตัดสินใจ"

**ปัญหาหลัก:** Future Architect ต้องเลือก 1 จาก 3 เส้นทาง โดยใช้ทุกสูตรที่เรียนมาจากเกม 1-4 เพื่อ Synthesize แผนชีวิตที่สมเหตุสมผล

---

## O — Objectives

**บทบาทนักเรียน:** "Future Architect" — ตัวเองในอีก 1 ปี กำลังตัดสินใจเรื่องสำคัญที่สุดในชีวิต

**Learning Objectives (LO):**
- **LO-1:** คำนวณ $FV = PV(1+i)^n$ และ $PV = FV(1+i)^{-n}$
- **LO-2:** คำนวณค่างวด (Annuity) โดยประยุกต์จากอนุกรมเรขาคณิต
- **LO-3:** Synthesize ทุกสูตร ($a_n$, $S_n$ Arithmetic, $S_n$ Geometric, $A = P(1+i)^n$) เพื่อเปรียบเทียบ 3 เส้นทาง
- **LO-4:** สร้าง Personal Future Plan ที่มีเหตุผลทั้งทางคณิตศาสตร์และทางชีวิต

**Win Condition:** สร้าง Personal Future Plan ที่ผ่านการประเมินจาก AI Evaluator ใน 3 มิติ

---

## R — Roles (NPC Roster)

### NPC-01: ผู้ว่าการ FUTURE FUND
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Quest Giver |
| **บุคลิก** | เป็นทางการ, ให้เกียรติ, ประเมินด้วย Rubric ชัดเจน |
| **Bloom's** | Evaluate → Create |
| **Unlock Condition** | เริ่มเกม (Default) |
| **หน้าที่** | มอบ 3 เส้นทาง + ประเมิน Personal Plan ด้วย AI Evaluator |
| **ประโยคเปิด** | *"ยินดีต้อนรับ Future Architect เส้นทางชีวิตคุณมี 3 ทาง แต่ก่อนเลือก — คุณต้องพิสูจน์ด้วยตัวเลขก่อนว่าแต่ละทางจะพาคุณไปที่ไหน"* |
| **Rubric AI Evaluator** | (1) ความถูกต้องทางคณิตศาสตร์ 40% (2) ความสมเหตุสมผลของการเลือก 35% (3) ความสมบูรณ์ของแผน 25% |
| **Reward** | Badge "Junior Financial Architect" (สูงสุดใน Universe) |

---

### NPC-02: อาจารย์โลนลี่ — ที่ปรึกษาการเงินการศึกษา
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Mentor with a Secret |
| **บุคลิก** | อบอุ่น, รอบคอบ, มีบาดแผลที่ซ่อนไว้ |
| **Bloom's** | Understand → Analyze |
| **Unlock Condition** | หลังผ่าน Tutorial PV/FV กับ FUTURE FUND |
| **ความลับ 3 ระดับ** | Lv.1: "PV ต่ำกว่า FV เสมอเมื่อ $i > 0$" / Lv.2: สูตร Annuity สมบูรณ์ / Lv.3: "อาจารย์โลนลี่เลือกผิดและเสียเวลา 3 ปี — นี่คือสิ่งที่ได้เรียนรู้" |
| **กลไก** | นักเรียนต้องพิสูจน์ว่าเข้าใจ PV/FV ก่อน Lv.2 จึงจะได้สูตร Annuity |
| **Reward Lv.3** | Tool "Full FinCalc Suite" + Narrative Fragment "จดหมายลับอาจารย์โลนลี่" |

---

### NPC-03: เสี่ยโต้ง — นายหน้าสินเชื่อการศึกษา
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Trickster |
| **บุคลิก** | เป็นมิตร, ดูน่าเชื่อถือ, ซ่อนรายละเอียด FV |
| **Bloom's** | Apply → Evaluate |
| **Unlock Condition** | หลัง MQ-02 |
| **กลวิธี** | เสนอ กยศ. "ดอกเบี้ยต่ำมาก แค่ 1% ต่อปี" โดยไม่บอกว่าเป็น Compound และไม่บอก FV รวมที่ต้องจ่ายคืน |
| **กลไก** | นักเรียนต้องคำนวณ $FV = PV(1.01)^{15}$ จริงๆ เพื่อรู้ยอดรวมที่ต้องจ่ายคืนทั้งหมด |
| **กับดัก** | ถ้าเลือก กยศ. โดยไม่คำนวณ → ใน Simulation เดือนที่ 48 มีหนี้ที่ไม่คาดคิด |
| **Reward** | Badge "Loan Myth Buster" + XP 60 + Evidence Card |

---

### NPC-04: ฟ้า — เพื่อนที่เลือกไปต่างประเทศ
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Rival |
| **บุคลิก** | มั่นใจ, Ambitious, ท้าทายให้คิดใหญ่ |
| **Bloom's** | Evaluate → Create |
| **Unlock Condition** | หลัง MQ-03 |
| **โต้แย้ง** | *"เรียนในประเทศ 4 ปี จ่ายเท่ากันหรือมากกว่า แต่ได้ Degree เดียวกัน ทำไมไม่ลอง Scholarship ต่างประเทศ?"* |
| **กลไก** | นักเรียนต้องคำนวณ $PV$ ของค่าใช้จ่ายทั้ง 2 เส้นทาง และเปรียบเทียบอย่างมีเหตุผล |
| **Moment of Truth** | ถ้า Defend สำเร็จ ฟ้ายอมรับ: "โอเค ตัวเลขของแกสมเหตุสมผล ฉันก็ยังเชื่อทางของฉัน — แต่ Respect ที่แกคำนวณก่อนตัดสินใจ" |
| **Reward** | XP 60 + Unlock Path C Details |

---

### NPC-05: ระบบ PV/FV Gate — ด่านตรวจสอบความรู้พื้นฐาน
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Gatekeeper |
| **บุคลิก** | เป็นกลาง, เป็นระบบ, ทดสอบสองสูตรพร้อมกัน |
| **Bloom's** | Remember → Apply |
| **Unlock Condition** | เริ่มเกม ก่อน MQ-01 |
| **หน้าที่** | ทดสอบว่าเข้าใจ $FV = PV(1+i)^n$ และ $PV = FV(1+i)^{-n}$ แตกต่างกันอย่างไร |
| **กลไก** | ถาม 2 ข้อ: (1) $FV$ เมื่อ $PV=10000, i=5\%, n=4$ (2) $PV$ ที่ให้ $FV=15000, i=5\%, n=4$ |
| **Reward** | Future Passport + XP 30 |

---

### NPC-06: ตัวเองในอนาคต — AI-Generated Future Self
| Field | รายละเอียด |
|-------|----------|
| **Archetype** | The Quest Giver (Special) |
| **บุคลิก** | สงบ, มีประสบการณ์, พูดจาเหมือนเพื่อน |
| **Bloom's** | Evaluate → Create |
| **Unlock Condition** | Final Quest เท่านั้น |
| **หน้าที่** | AI สร้าง "จดหมายจากตัวเองในอนาคต" ตาม Path ที่นักเรียนเลือก |
| **ลักษณะพิเศษ** | Generated แบบ Personalized — อ้างอิงตัวเลขและเหตุผลที่นักเรียนใส่ใน Plan จริงๆ |
| **Reward** | Narrative Fragment สุดพิเศษ + เปิด Ending |

---

## Quest Map (Bloom's Taxonomy) — Final Synthesis

```
[QUEST]                         [BLOOM'S]          [ARCHETYPE]        [MECHANIC]
────────────────────────────────────────────────────────────────────────────────
MQ-01: PV/FV Gateway            Remember→Apply     Trial              Knowledge Gate
  └── ผ่าน PV/FV Gate: คำนวณทั้ง FV และ PV

MQ-02: Mentor's Foundation     Understand→Analyze  Discovery          Investigation
  └── ปลดล็อก อ.โลนลี่ Lv.1-2 → ได้สูตร Annuity

MQ-03: The กยศ. Trap           Apply→Evaluate      Dilemma            Consequence Chain
  └── คำนวณ FV ของ กยศ. จริงๆ ก่อนตัดสินใจ

SQ-01: ช่วยน้องเลือกทุน        Apply               Rescue             Resource Management
  └── คำนวณ PV ของ Scholarship 2 ประเภทให้น้อง

MQ-04: โต้แย้งฟ้า              Analyze→Evaluate    Dilemma            Collaborative Puzzle
  └── เปรียบเทียบ PV ของ 2 เส้นทางการศึกษาอย่างมีเหตุผล

MQ-05: Mentor's Secret Lv.3   Evaluate             Discovery          Investigation
  └── ปลดล็อก อ.โลนลี่ Lv.3 → เข้าใจว่าตัวเลขไม่ใช่ทุกอย่าง

MQ-06: เสี่ยโต้ง Revelation    Evaluate             Investigation      Consequence Chain
  └── นำ Evidence FV ที่คำนวณไปโต้แย้งข้อกล่าวอ้างของเสี่ยโต้ง

FQ: Personal Future Plan       Create               Creation           Collaborative Puzzle
  └── เลือก Path + คำนวณ PV/FV/Annuity + เขียน Rationale → AI Evaluated
```

---

## L — Loot (Item Taxonomy ครบ 6 ประเภท)

| Item | ประเภท | ได้รับเมื่อ | หน้าที่ |
|------|--------|-----------|--------|
| **Future Passport** | Access Item | MQ-01 ผ่าน | ปลดล็อก 3 เส้นทาง |
| **Annuity Formula Card** | Access Item | อ.โลนลี่ Lv.2 | ปลดล็อก Path B และ Path C (ใช้ Annuity) |
| **Personal Future Plan** | Knowledge Artifact | Final Quest | Output หลัก — สิ่งสำคัญที่สุดที่นักเรียนสร้างเอง |
| **3-Path Comparison Sheet** | Knowledge Artifact | MQ-04 | บันทึกการคำนวณ PV/FV ทั้ง 3 เส้นทาง |
| **Full FinCalc Suite** | Tool Item | อ.โลนลี่ Lv.3 | รวมสูตรจากเกม 1-4 ทั้งหมด + Annuity |
| **Loan Reality Calculator** | Tool Item | MQ-03 สำเร็จ | คำนวณ FV ของเงินกู้ระยะยาว |
| **จดหมายลับ อ.โลนลี่** | Narrative Fragment | อ.โลนลี่ Lv.3 | ประสบการณ์ที่เลือกผิดและสิ่งที่เรียนรู้ |
| **จดหมายจากตัวเองในอนาคต** | Narrative Fragment | Final Quest | AI-Generated ตาม Path ที่เลือก |
| **หนังสือสัญญา กยศ. จริง** | Narrative Fragment | MQ-03 | เอกสาร Simulated ที่แสดง Terms จริงๆ |
| **Junior Financial Architect** | Mastery Badge | Final Quest ผ่าน | Badge สูงสุด: Synthesis ครบทุก LO ทุกเกม |
| **Loan Myth Buster** | Mastery Badge | MQ-03 สำเร็จ | Mastery: คำนวณ FV เพื่อประเมินสินเชื่อ |
| **PV/FV Navigator** | Mastery Badge | MQ-01+04 ผ่าน | Mastery: Apply ทั้ง PV และ FV ในบริบทต่างกัน |
| **Life Point** | Resource Token | ทุก Quest สำเร็จ | จำกัด 5 Lives — ตัดสินใจโดยไม่คำนวณใช้ 1 Life |

---

## D — Dilemmas

### Dilemma หลัก: "3 เส้นทาง 3 ชีวิต"
| เส้นทาง | รายละเอียด | สูตรที่ต้องใช้ |
|---------|----------|--------------|
| **Path A: มหาวิทยาลัยรัฐ + กยศ.** | กู้ 150,000 บาท $i=1\%$/ปี 15 ปี → $FV = 150000(1.01)^{15}$ = 173,568 บาท | $FV = PV(1+i)^n$ |
| **Path B: มหาวิทยาลัยเอกชน สาขาใฝ่ฝัน** | ผ่อนค่าเทอม Annuity 8 งวด $a_1=30000, d=2000$ → $S_8 = \frac{8}{2}(30000+44000)$ = 296,000 บาท | $S_n$ Arithmetic + Annuity |
| **Path C: Work & Study 1 ปีก่อน** | ออม 5,000/เดือน $i=0.8\%$/เดือน 12 เดือน → $A_{12} = 5000 \times \frac{(1.008)^{12}-1}{0.008}$ | Geometric Series + $A = P(1+i)^n$ |

**ไม่มีคำตอบ "ถูก" ที่ตายตัว** แต่นักเรียนต้องแสดงการคำนวณที่ถูกต้องก่อนเสมอ

### Dilemma ซ่อน: "ตัวเลขไม่ใช่ทุกอย่าง"
> อ.โลนลี่ Lv.3 เปิดเผย: *"ฉันเคยเลือก Path ที่ตัวเลขดีที่สุด — แต่ไม่ใช่สิ่งที่ฉันรัก เสียเวลา 3 ปีก่อนจะกลับมาเริ่มใหม่"*
> เกม Final Quest ยอมรับทุก Path ถ้านักเรียนแสดงว่า: คำนวณถูก + รู้ว่าตัวเลขสนับสนุนการตัดสินใจ ไม่ใช่ทดแทนมัน

### Final Creation Task — Personal Future Plan
> นักเรียนต้องเขียนประกอบด้วย:
> 1. **เส้นทางที่เลือก** + เหตุผลที่ไม่ใช่แค่ตัวเลข
> 2. **การคำนวณ** PV หรือ FV หรือ Annuity ที่รองรับการตัดสินใจ (อย่างน้อย 1 สูตร)
> 3. **แผนจัดการเงิน** ใน 4 ปีแรก
> 4. **ความเสี่ยง** ที่รู้ว่ามีและวิธีรับมือ
>
> *AI Evaluator ประเมิน 3 มิติ: ความถูกต้องทางคณิตศาสตร์ / ความสมเหตุสมผล / ความสมบูรณ์*

---

---

# 📊 ตารางสรุปครบถ้วน — นครธนา Universe

## NPC Count และ Archetype Distribution

| เกม | NPC ทั้งหมด | Gatekeeper | Mentor w/Secret | Unreliable Witness | Rival | Quest Giver | Trickster |
|-----|-----------|-----------|----------------|------------------|-------|-------------|-----------|
| FLEX PROTOCOL | 6 | ARIA, FlexBank | Jett | แพรว | — | น้องมิ้น | วิชัย |
| GACHA KINGDOM | 6 | G.A.T.E. | Zephyr | Dr. Lena | มาร์ค | Pixel | Kong |
| TUTOR WARS | 6 | — | โบว์ | Kru_Viral | Master Wit | ปัญญา, น้องหนู | สมศักดิ์ |
| COMPOUND CHRONICLES | 6 | Agent Nova | Aiko | Dr. Prism | ไข่มุก | Fern | พ่อค้า Loot Box |
| FUTURE FUND | 6 | PV/FV Gate | อ.โลนลี่ | — | ฟ้า | ผู้ว่าการ, ตัวเองอนาคต | เสี่ยโต้ง |
| **รวม Universe** | **30** | **5** | **5** | **4** | **4** | **7** | **5** |

## Quest Distribution และ Bloom's Coverage

| เกม | Main Quests | Side Quests | Final Quest | Bloom's Range |
|-----|------------|------------|-------------|---------------|
| FLEX PROTOCOL | 5 | 2 | 1 | Remember → Create |
| GACHA KINGDOM | 5 | 2 | 1 | Remember → Create |
| TUTOR WARS | 5 | 2 | 1 | Remember → Create |
| COMPOUND CHRONICLES | 5 | 2 | 1 | Remember → Create |
| FUTURE FUND | 6 | 1 | 1 | Remember → Create |
| **รวม Universe** | **26** | **9** | **5** | **ครบ 6 ระดับทุกเกม** |

## Item Taxonomy Distribution (ต่อเกม)

| ประเภท Item | FLEX | GACHA | TUTOR | COMPOUND | FUTURE | รวม |
|------------|------|-------|-------|----------|--------|-----|
| Access Item | 2 | 2 | 2 | 2 | 2 | 10 |
| Knowledge Artifact | 2 | 2 | 2 | 2 | 2 | 10 |
| Tool Item | 2 | 2 | 2 | 2 | 2 | 10 |
| Narrative Fragment | 3 | 3 | 3 | 3 | 3 | 15 |
| Mastery Badge | 2 | 2 | 2 | 2 | 3 | 11 |
| Resource Token | 1 | 1 | 1 | 1 | 1 | 5 |
| **รวมต่อเกม** | **12** | **12** | **12** | **12** | **13** | **61** |

## Mechanic Distribution

| Mechanic | เกมที่ใช้ | Quest Type หลัก |
|----------|---------|----------------|
| Knowledge Gate | ทุกเกม (MQ-01) | Trial |
| Consequence Chain | FLEX, COMPOUND, FUTURE | Dilemma |
| Resource Management | TUTOR, COMPOUND | Dilemma |
| Investigation | GACHA, FUTURE | Investigation |
| Collaborative Puzzle | ทุกเกม (Final Quest) | Creation |

---

# 🔧 หมายเหตุสำหรับนักพัฒนา

## Phase State Machine (ทุกเกม)
```
Briefing → Recon → [Select NPC] → Knowledge Check → Executing → Round Result
    ↑                                                                    |
    └──────────────────── (ถ้าไม่ผ่าน) ────────────────────────────────┘
```

## AI Evaluator Rubric Template (Final Quest)
```json
{
  "evaluation_dimensions": [
    {
      "dimension": "mathematical_accuracy",
      "weight": 0.40,
      "criteria": "สูตรและตัวเลขถูกต้อง อ้างอิง a1, d, r, n, i ครบ"
    },
    {
      "dimension": "reasoning_quality",
      "weight": 0.35,
      "criteria": "การตัดสินใจมีเหตุผลที่อ้างอิงตัวเลขที่คำนวณได้จริง"
    },
    {
      "dimension": "plan_completeness",
      "weight": 0.25,
      "criteria": "ครอบคลุมทุก Component ที่กำหนดใน Task"
    }
  ],
  "pass_threshold": 0.70,
  "feedback_language": "Thai",
  "hint_on_fail": true
}
```

## Raw ID Convention (Anti-Leakage)
```python
# ห้าม: ส่ง NPC ID ตรงๆ ไปยัง Frontend หรือ LLM Prompt
# ถูก: ใช้ f-string จาก Data Dictionary เสมอ
NPC_DISPLAY_NAMES = {
    "aria": "ARIA",
    "praew": "แพรว",
    "wichai": "คุณวิชัย",
    "jett": "ผู้พิทักษ์ Jett",
    "min": "น้องมิ้น",
    "flexbank": "ระบบ FlexBank AI"
}
```

## Content Moderation Categories (ทุกเกม)
```
O1: ห้ามสอนให้หลีกเลี่ยงสัญญาโดยผิดกฎหมาย
O2: ห้ามแสดง FOMO ในแง่บวก — ต้องให้ทางออก
O3: ห้ามดูถูกผู้เล่น Gacha หรือผู้กู้ยืม
O4: ห้ามแนะนำสินเชื่อใดสินเชื่อหนึ่งโดยตรง
O5: ให้ข้อมูลทางการเงินเพื่อการศึกษา ไม่ใช่คำแนะนำทางการเงิน
O6: เคารพสถาบัน กยศ. — เกมแสดงว่า "ต้องคำนวณก่อน" ไม่ใช่ "ห้ามกู้"
```

---

*GDD v2.0 | นครธนา Universe | ปรับปรุงตาม WORLD Framework + NPC Archetypes + Quest Map + Item Taxonomy*
*สงวนสิทธิ์สำหรับใช้งานทางการศึกษา | Silpakorn University Demonstration School*
