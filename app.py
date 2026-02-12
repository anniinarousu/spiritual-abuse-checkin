# Hengellisen väkivallan merkkien tunnistaminen -sovellus
# Tämä Streamlit-sovellus auttaa kartoittamaan hengellisen väkivallan merkkejä.
# Kielivalinta: Suomi / English / Svenska

import streamlit as st
import json
import google.generativeai as genai
import os

# ----------------------
# TÄRKEÄÄ: st.set_page_config() täytyy olla ENSIMMÄINEN Streamlit-komento
# ----------------------
st.set_page_config(
    page_title="Hengellisen väkivallan merkkien tunnistaminen | Spiritual Abuse Check-in",
    page_icon="🛡️",
    layout="centered"
)

# ----------------------
# Väriympäristön määritys
# ----------------------
color_scheme = """
<style>
/* Pääalueen tausta */
.main {
    background-color: #f8f5f0;
}

/* Otsikot - turkoosi */
h1 {
    color: #369694 !important;
    font-weight: bold;
}
h2, h3 {
    color: #369694 !important;
}

/* Yläpalkin ikonit */
header[data-testid="stHeader"] {
    background-color: #85dbd9 !important;
}
header[data-testid="stHeader"] button {
    color: white !important;
}
header[data-testid="stHeader"] svg {
    fill: white !important;
    stroke: white !important;
}

/* Sivupalkki - tumma lila tausta */
[data-testid="stSidebar"] {
    background-color: #7a72bd !important;
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: white !important;
    background-color: transparent !important;
}

/* ===== CHECKBOX ===== */
[data-testid="stSidebar"] .stCheckbox,
[data-testid="stSidebar"] .stCheckbox > div,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] .stCheckbox > div > div {
    background-color: transparent !important;
    background: transparent !important;
}

/* Checkbox ruutu - turkoosi */
[data-testid="stSidebar"] .stCheckbox [data-baseweb="checkbox"] span,
[data-testid="stSidebar"] .stCheckbox [data-baseweb="checkbox"] > div:first-child {
    background-color: #85dbd9 !important;
    border-color: #85dbd9 !important;
}

/* Checkbox väkänen - valkoinen */
[data-testid="stSidebar"] .stCheckbox svg {
    color: white !important;
    fill: white !important;
    stroke: white !important;
}

/* ===== SLIDER ===== */
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stSlider > div,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    background-color: transparent !important;
    background: transparent !important;
}

/* Slider numerot 1 ja 5 - valkoinen teksti, EI taustaa */
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
    color: white !important;
    background-color: transparent !important;
    background: none !important;
}

/* Slider kaikki span ja p elementit - ei taustaa */
[data-testid="stSidebar"] .stSlider p,
[data-testid="stSidebar"] .stSlider span {
    color: white !important;
    background-color: transparent !important;
    background: none !important;
}

/* Slider container - läpinäkyvä */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* Slider VIIVA (track) - VAIN viiva turkoosi */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div:nth-child(1) > div {
    background: #85dbd9 !important;
    background-color: #85dbd9 !important;
}

/* Slider track fill - turkoosi */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[style*="rgb(255"] {
    background: #85dbd9 !important;
    background-color: #85dbd9 !important;
}

/* Slider PALLO (thumb) - turkoosi */
[data-testid="stSidebar"] .stSlider [role="slider"] {
    background-color: #85dbd9 !important;
    border-color: #85dbd9 !important;
}

/* Slider arvo nupissa - ei taustaa */
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
    color: white !important;
    background-color: transparent !important;
    background: none !important;
}

/* Varmista ettei mikään muu slider-elementti saa taustaa */
[data-testid="stSidebar"] .stSlider div[data-testid] {
    background: transparent !important;
    background-color: transparent !important;
}

/* ===== PAINIKE ===== */
.stButton > button {
    background-color: #85dbd9 !important;
    color: white !important;
    border: none !important;
}
.stButton > button:hover {
    background-color: #6bc9c7 !important;
}

/* ===== REFLEKTIO LAATIKKO ===== */
[data-testid="stAlert"],
.stAlert {
    background-color: #85dbd9 !important;
    border: none !important;
    color: white !important;
}
.stAlert p, .stAlert div, .stAlert span, .stAlert a {
    color: white !important;
}

/* ===== TEXT AREA ===== */
[data-testid="stSidebar"] .stTextArea,
[data-testid="stSidebar"] .stTextArea > div,
[data-testid="stSidebar"] .stTextArea label {
    background-color: transparent !important;
}
[data-testid="stSidebar"] .stTextArea textarea {
    background-color: #5a5a9e !important;
    color: white !important;
}
[data-testid="stSidebar"] .stTextArea textarea::placeholder {
    color: rgba(255,255,255,0.7) !important;
}

/* ===== FOCUS-REUNAT - tumma turkoosi ===== */
[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within,
[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within {
    border-color: #369694 !important;
    box-shadow: 0 0 0 2px #369694 !important;
    outline: none !important;
}
[data-testid="stSelectbox"] input:focus {
    border-color: #369694 !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stSidebar"] .stCheckbox input:focus + div,
[data-testid="stSidebar"] .stCheckbox [data-baseweb="checkbox"]:focus-within,
[data-testid="stSidebar"] .stCheckbox:focus-within,
[data-testid="stSidebar"] .stCheckbox > div:focus-within {
    border-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stSidebar"] .stCheckbox label:focus-within {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stSidebar"] .stSlider [role="slider"]:focus,
[data-testid="stSidebar"] .stSlider [role="slider"]:active {
    border-color: #369694 !important;
    box-shadow: 0 0 0 2px #369694 !important;
    outline: none !important;
}

[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: #369694 !important;
    box-shadow: 0 0 0 2px #369694 !important;
    outline: none !important;
}
[data-testid="stSidebar"] .stTextArea > div:focus-within {
    border-color: #369694 !important;
    box-shadow: none !important;
}

.stButton > button:focus {
    border-color: #369694 !important;
    box-shadow: 0 0 0 2px #369694 !important;
    outline: none !important;
}

[data-testid="stSidebar"] input:focus,
[data-testid="stSidebar"] select:focus {
    border-color: #369694 !important;
    box-shadow: 0 0 0 2px #369694 !important;
    outline: none !important;
}

*:focus {
    outline-color: #369694 !important;
}
[data-baseweb] *:focus,
[data-baseweb] *:focus-visible {
    border-color: #369694 !important;
}
[data-testid="stSidebar"] [data-baseweb="checkbox"]:focus-within > div {
    box-shadow: none !important;
    border-color: transparent !important;
}
</style>
"""
st.markdown(color_scheme, unsafe_allow_html=True)

# ----------------------
# Session state -alustus
# ----------------------
if 'show_reflection' not in st.session_state:
    st.session_state.show_reflection = False
if 'reflection_data' not in st.session_state:
    st.session_state.reflection_data = None
if 'reflection_text' not in st.session_state:
    st.session_state.reflection_text = ""
if 'selected_lang' not in st.session_state:
    st.session_state.selected_lang = "Suomi"

# ----------------------
# Käännösten sanakirja
# ----------------------
translations = {
    "Suomi": {
        "title": "Hengellisen väkivallan merkkien tunnistaminen",
        "intro": (
            "Tämä työkalu on tarkoitettu nopeaan, ei-kliiniseen kartoitukseen. "
            "Se ei korvaa ammattimaista diagnoosia tai hoitoa. Käytä trauma-tietoista, "
            "kunnioittavaa kieltä ja älä kirjaa henkilötietoja."
        ),
        "sidebar_header": "Kysymyksiä asiakkaan tilanteen kartoittamiseksi",
        "questions": {
            "pelottelu": "Onko asiakasta peloteltu Jumalan rangaistuksilla, kadotuksella tai pahoilla hengillä?",
            "kontrolli": "Onko asiakkaan yksityiselämän valintoja (pukeutuminen, seurustelu, ystävät, opiskelu, työ) säännelty uskonnollisin perustein?",
            "eristaminen": "Onko asiakasta eristetty yhteisön ulkopuolisista ihmisistä tai suljettu yhteisöstä ulos?",
            "hapaiseminen": "Onko asiakasta julkisesti nöyryytetty tai häpäisty yhteisössä?",
            "autonomia": "Onko asiakkaan omaa ajattelua, tunteita tai moraalista harkintaa kielletty 'jumalallisen auktoriteetin' nimissä?",
            "seksuaalisuus": "Onko asiakkaan seksuaalista tai kehollista itsemääräämisoikeutta loukattu uskonnollisin perustein?",
            "sielunhoito": "Onko rukousta, sielunhoitoa tai rippiä käytetty painostamiseen, nöyryyttämiseen tai vallankäyttöön?",
            "vaikeneminen": "Onko asiakasta painostettu vaikenemaan väkivallasta tai hyväksikäytöstä yhteisön maineen suojelemiseksi?",
            "sukupuoli": "Onko asiakasta syrjitty, nöyryytetty tai uhkailtu sukupuolen tai seksuaalisen suuntautumisen vuoksi?",
            "talous": "Onko asiakasta painostettu antamaan rahaa, omaisuutta tai työpanosta yhteisölle uskonnolliseen auktoriteettiin vedoten?",
            "terveys": "Onko asiakkaan pääsyä terveydenhuoltoon rajoitettu uskonnollisin perustein?",
        },
        "question_categories": {
            "pelottelu": "Pelottelu ja uhkailu",
            "kontrolli": "Kontrollointi ja alistaminen",
            "eristaminen": "Sosiaalinen eristäminen",
            "hapaiseminen": "Julkinen häpäiseminen",
            "autonomia": "Identiteetin murentaminen",
            "seksuaalisuus": "Seksuaalinen itsemääräämisoikeus",
            "sielunhoito": "Hengellisen tuen vääristäminen",
            "vaikeneminen": "Väkivallasta vaikeneminen",
            "sukupuoli": "Syrjintä",
            "talous": "Taloudellinen riisto",
            "terveys": "Terveydenhuollon rajoittaminen",
        },
        "slider_label": "Kuinka turvalliseksi asiakas tuntee olonsa keskustellessaan hengellisistä asioista?",
        "slider_scale_explanation": "1 = Asiakas tuntee itsensä hyvin pelokkaaksi ja 5 = Asiakas tuntee olonsa hyvin turvalliseksi.",
        "notes_label": "Vapaa muistiinpano (valinnainen, EI henkilötietoja)",
        "notes_placeholder": "Kirjaa lyhyitä havaintoja, huolia tai turvallisuuteen liittyviä huomioita...",
        "button": "Luo reflektio",
        "button_prompt": "Paina 'Luo reflektio' luodaksesi ehdotetun reflektiotekstin.",
        "incoming_subheader": "Yhteenveto kartoituksesta",
        "safety_prefix": "Turvallisuuden arvio (1–5):",
        "selected_indicators": "Havaitut hengellisen väkivallan muodot:",
        "no_indicators": "Ei havaittuja indikaattoreita",
        "case_notes": "Muistiinpanot:",
        "reflection_header": "AI-avusteinen reflektio",
        "footer": "**Huom.** Säilytä luottamuksellisuus, älä tallenna henkilötietoja.",
        "language_label": "Kieli",
    },
    "English": {
        "title": "Spiritual Abuse Check-in",
        "intro": (
            "This tool is intended as a quick, non-clinical check-in. "
            "It does not replace professional diagnosis or care. Use trauma-informed, respectful language "
            "and do not record personal identifying information."
        ),
        "sidebar_header": "Questions to map the client's situation",
        "questions": {
            "pelottelu": "Has the client been threatened with God's punishment, damnation, or evil spirits?",
            "kontrolli": "Have the client's personal choices (clothing, dating, friends, studies, work) been regulated on religious grounds?",
            "eristaminen": "Has the client been isolated from people outside the community or excluded from the community?",
            "hapaiseminen": "Has the client been publicly humiliated or shamed in the community?",
            "autonomia": "Has the client's own thinking, feelings, or moral judgment been forbidden in the name of 'divine authority'?",
            "seksuaalisuus": "Has the client's sexual or bodily autonomy been violated on religious grounds?",
            "sielunhoito": "Has prayer, pastoral care, or confession been used for pressure, humiliation, or exercise of power?",
            "vaikeneminen": "Has the client been pressured to remain silent about violence or abuse to protect the community's reputation?",
            "sukupuoli": "Has the client been discriminated against, humiliated, or threatened because of gender or sexual orientation?",
            "talous": "Has the client been pressured to give money, property, or labor to the community citing religious authority?",
            "terveys": "Has the client's access to healthcare been restricted on religious grounds?",
        },
        "question_categories": {
            "pelottelu": "Intimidation and threats",
            "kontrolli": "Control and subjugation",
            "eristaminen": "Social isolation",
            "hapaiseminen": "Public shaming",
            "autonomia": "Identity erosion",
            "seksuaalisuus": "Sexual autonomy",
            "sielunhoito": "Distortion of spiritual support",
            "vaikeneminen": "Silencing about violence",
            "sukupuoli": "Discrimination",
            "talous": "Financial exploitation",
            "terveys": "Healthcare restrictions",
        },
        "slider_label": "How safe does the client feel discussing spiritual matters?",
        "slider_scale_explanation": "1 = Client feels very fearful and 5 = Client feels very safe.",
        "notes_label": "Free-form case notes (optional, NO personal data)",
        "notes_placeholder": "Write short observations, concerns or safety notes...",
        "button": "Generate reflection",
        "button_prompt": "Press 'Generate reflection' to create a suggested reflection text.",
        "incoming_subheader": "Summary of check-in",
        "safety_prefix": "Safety rating (1–5):",
        "selected_indicators": "Identified forms of spiritual abuse:",
        "no_indicators": "No indicators identified",
        "case_notes": "Notes:",
        "reflection_header": "AI-assisted reflection",
        "footer": "**Note:** Keep confidentiality, do not store personal data.",
        "language_label": "Language",
    },
    "Svenska": {
        "title": "Check-in för andligt våld",
        "intro": (
            "Detta verktyg är avsett för en snabb, icke-klinisk check-in. "
            "Det ersätter inte professionell diagnos eller vård. Använd traumamedvetet, respektfullt språk "
            "och registrera inte personuppgifter."
        ),
        "sidebar_header": "Frågor för att kartlägga klientens situation",
        "questions": {
            "pelottelu": "Har klienten hotats med Guds straff, fördömelse eller onda andar?",
            "kontrolli": "Har klientens personliga val (klädsel, dejting, vänner, studier, arbete) reglerats på religiösa grunder?",
            "eristaminen": "Har klienten isolerats från personer utanför gemenskapen eller uteslutits från gemenskapen?",
            "hapaiseminen": "Har klienten blivit offentligt förödmjukad eller skambelagd i gemenskapen?",
            "autonomia": "Har klientens eget tänkande, känslor eller moraliska omdöme förbjudits i 'gudomlig auktoritets' namn?",
            "seksuaalisuus": "Har klientens sexuella eller kroppsliga autonomi kränkts på religiösa grunder?",
            "sielunhoito": "Har bön, själavård eller bikt använts för press, förödmjukelse eller maktutövning?",
            "vaikeneminen": "Har klienten pressats att tiga om våld eller övergrepp för att skydda gemenskapens rykte?",
            "sukupuoli": "Har klienten diskriminerats, förödmjukats eller hotats på grund av kön eller sexuell läggning?",
            "talous": "Har klienten pressats att ge pengar, egendom eller arbete till gemenskapen med hänvisning till religiös auktoritet?",
            "terveys": "Har klientens tillgång till sjukvård begränsats på religiösa grunder?",
        },
        "question_categories": {
            "pelottelu": "Hot och skrämsel",
            "kontrolli": "Kontroll och underkastelse",
            "eristaminen": "Social isolering",
            "hapaiseminen": "Offentlig skam",
            "autonomia": "Identitetsurholkning",
            "seksuaalisuus": "Sexuell autonomi",
            "sielunhoito": "Förvrängning av andligt stöd",
            "vaikeneminen": "Tystnad om våld",
            "sukupuoli": "Diskriminering",
            "talous": "Ekonomisk exploatering",
            "terveys": "Sjukvårdsbegränsningar",
        },
        "slider_label": "Hur trygg känner sig klienten att diskutera andliga frågor?",
        "slider_scale_explanation": "1 = Klienten känner sig mycket rädd och 5 = Klienten känner sig mycket trygg.",
        "notes_label": "Fria anteckningar (valfritt, INGA personuppgifter)",
        "notes_placeholder": "Skriv korta observationer, oro eller säkerhetsanteckningar...",
        "button": "Generera reflektion",
        "button_prompt": "Tryck 'Generera reflektion' för att skapa ett förslag till reflektion.",
        "incoming_subheader": "Sammanfattning av check-in",
        "safety_prefix": "Trygghetsbedömning (1–5):",
        "selected_indicators": "Identifierade former av andligt våld:",
        "no_indicators": "Inga indikatorer identifierade",
        "case_notes": "Anteckningar:",
        "reflection_header": "AI-assisterad reflektion",
        "footer": "**Obs!** Behåll konfidentialitet, spara inte personuppgifter.",
        "language_label": "Språk",
    },
}


# ----------------------
# AI-avusteinen reflektio (Gemini API)
# ----------------------
def generate_ai_reflection(lang, data, facts, tr):
    """
    Generoi älykkään, kontekstuaalisen reflektion Gemini AI:n avulla.
    """
    checked_keys = data.get("checked_keys", [])
    safe = data.get("safe_slider", 3)
    notes = data.get("notes", "")
    categories = tr.get("question_categories", {})
    
    checked_categories = [categories.get(k, k) for k in checked_keys]
    
    lang_names = {
        "Suomi": "suomeksi",
        "English": "in English",
        "Svenska": "på svenska"
    }
    lang_instruction = lang_names.get(lang, "suomeksi")
    
    if checked_categories:
        indicators_text = "\n".join([f"- {cat}" for cat in checked_categories])
    else:
        indicators_text = "Ei valittuja indikaattoreita."
    
    support_list = []
    for s in facts.get("follow_up_support", []):
        name = s.get('name', s.get('text', ''))
        source = s.get('source', '')
        if name and source:
            support_list.append(f"- {name}: {source}")
    support_text = "\n".join(support_list) if support_list else "Ei saatavilla."
    
    prompt = f"""Olet trauma-tietoinen ammattilainen, joka auttaa kartoittamaan hengellisen väkivallan merkkejä.

Asiakkaan tilanne:
- Turvallisuuden kokemus: {safe}/5 (1=hyvin pelokas, 5=hyvin turvallinen)
- Havaitut hengellisen väkivallan muodot:
{indicators_text}
- Työntekijän muistiinpanot: {notes if notes else "Ei muistiinpanoja."}

Tukipalvelut Suomessa:
{support_text}

Tehtäväsi:
1. Kirjoita lyhyt, empaattinen yhteenveto asiakkaan tilanteesta
2. Analysoi mitä havaitut merkit voivat tarkoittaa asiakkaan kokemuksessa
3. Anna 3-4 konkreettista suositusta työntekijälle
4. Mainitse sopivat tukipalvelut

Kirjoita vastaus {lang_instruction}. Käytä trauma-tietoista, kunnioittavaa kieltä. 
Älä käytä liian kliinistä kieltä. Ole empaattinen mutta ammatillinen.
Käytä markdown-muotoilua (## otsikoille, **lihavointi**, - listoille)."""

    try:
        # Hae API-avain - kokeile molempia tapoja
        api_key = None
        
        # Yritä ensin st.secrets
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass
        
        # Jos ei löydy, yritä ympäristömuuttujaa
        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            st.warning("API-avainta ei löytynyt. Käytetään vaihtoehtoista menetelmää.")
            return fallback_reflection(lang, data, facts, tr)
        
        # Konfiguroi Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generoi vastaus
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        st.warning(f"AI-reflektio ei onnistunut: {e}")
        return fallback_reflection(lang, data, facts, tr)


def fallback_reflection(lang, data, facts, tr):
    """
    Vaihtoehtoinen sääntöpohjainen reflektio, jos AI ei toimi.
    """
    checked_keys = data.get("checked_keys", [])
    safe = data.get("safe_slider", 3)
    notes = data.get("notes", "")
    categories = tr.get("question_categories", {})
    
    num_indicators = len(checked_keys)
    parts = []
    
    if lang == "Suomi":
        if num_indicators >= 5:
            parts.append("## ⚠️ Vakavia huolenaiheita havaittu\n")
        elif num_indicators >= 3:
            parts.append("## ⚡ Useita huolenaiheita havaittu\n")
        elif num_indicators >= 1:
            parts.append("## 📋 Joitakin huolenaiheita havaittu\n")
        else:
            parts.append("## ✅ Ei merkittäviä huolenaiheita havaittu\n")
        
        parts.append(f"**Turvallisuuden kokemus:** {safe}/5\n")
        
        if checked_keys:
            parts.append("### Havaitut muodot:\n")
            for key in checked_keys:
                cat = categories.get(key, key)
                parts.append(f"- {cat}")
        
        if notes:
            parts.append(f"\n### Muistiinpanot:\n{notes}")
        
        parts.append("\n### Suositukset:\n")
        parts.append("- Kuuntele empaattisesti")
        parts.append("- Vahvista asiakkaan kokemukset")
        parts.append("- Arvioi turvallisuustilanne")
        parts.append("- Ohjaa tarvittaessa ammatilliseen tukeen")
        
    elif lang == "English":
        if num_indicators >= 5:
            parts.append("## ⚠️ Serious concerns identified\n")
        elif num_indicators >= 3:
            parts.append("## ⚡ Multiple concerns identified\n")
        elif num_indicators >= 1:
            parts.append("## 📋 Some concerns identified\n")
        else:
            parts.append("## ✅ No significant concerns identified\n")
        
        parts.append(f"**Safety experience:** {safe}/5\n")
        
        if checked_keys:
            parts.append("### Identified forms:\n")
            for key in checked_keys:
                cat = categories.get(key, key)
                parts.append(f"- {cat}")
        
        if notes:
            parts.append(f"\n### Notes:\n{notes}")
        
        parts.append("\n### Recommendations:\n")
        parts.append("- Listen empathetically")
        parts.append("- Validate the client's experiences")
        parts.append("- Assess safety situation")
        parts.append("- Refer to professional support if needed")
        
    elif lang == "Svenska":
        if num_indicators >= 5:
            parts.append("## ⚠️ Allvarliga bekymmer identifierade\n")
        elif num_indicators >= 3:
            parts.append("## ⚡ Flera bekymmer identifierade\n")
        elif num_indicators >= 1:
            parts.append("## 📋 Vissa bekymmer identifierade\n")
        else:
            parts.append("## ✅ Inga betydande bekymmer identifierade\n")
        
        parts.append(f"**Trygghetsupplevelse:** {safe}/5\n")
        
        if checked_keys:
            parts.append("### Identifierade former:\n")
            for key in checked_keys:
                cat = categories.get(key, key)
                parts.append(f"- {cat}")
        
        if notes:
            parts.append(f"\n### Anteckningar:\n{notes}")
        
        parts.append("\n### Rekommendationer:\n")
        parts.append("- Lyssna empatiskt")
        parts.append("- Bekräfta klientens upplevelser")
        parts.append("- Bedöm säkerhetssituationen")
        parts.append("- Hänvisa till professionellt stöd vid behov")
    
    parts.append("\n---\n### Tukipalvelut:\n")
    for s in facts.get("follow_up_support", []):
        name = s.get('name', s.get('text', ''))
        source = s.get('source', '')
        if name and source:
            parts.append(f"- [{name}]({source})")
    
    return "\n".join(parts)


# ----------------------
# Kielivalinta
# ----------------------
lang_options = ["Suomi", "English", "Svenska"]
tr = translations[st.session_state.selected_lang]

cols = st.columns([3, 1])

with cols[1]:
    selected_lang = st.selectbox(
        tr["language_label"],
        lang_options,
        index=lang_options.index(st.session_state.selected_lang),
        key="language_selector"
    )
    if selected_lang != st.session_state.selected_lang:
        st.session_state.selected_lang = selected_lang
        st.session_state.show_reflection = False
        st.session_state.reflection_data = None
        st.session_state.reflection_text = ""
        st.rerun()

tr = translations[st.session_state.selected_lang]

# ----------------------
# Sivun otsikko ja esittely
# ----------------------
st.title(tr["title"])
st.markdown(tr["intro"])

# ----------------------
# Sivupalkin paneelit
# ----------------------
st.sidebar.header(tr["sidebar_header"])

questions = tr["questions"]

checkbox_state_key = f'checkbox_responses_{st.session_state.selected_lang}'
if checkbox_state_key not in st.session_state:
    st.session_state[checkbox_state_key] = {key: False for key in questions.keys()}

responses = {}
for key, question in questions.items():
    checkbox_key = f"checkbox_{st.session_state.selected_lang}_{key}"
    value = st.sidebar.checkbox(
        question,
        value=st.session_state[checkbox_state_key].get(key, False),
        key=checkbox_key
    )
    responses[key] = value
    st.session_state[checkbox_state_key][key] = value

slider_key = f"safe_slider_{st.session_state.selected_lang}"
safe_slider = st.sidebar.slider(
    tr["slider_label"],
    min_value=1,
    max_value=5,
    value=3,
    key=slider_key
)

st.sidebar.markdown(tr["slider_scale_explanation"])

notes_key = f"notes_{st.session_state.selected_lang}"
notes = st.sidebar.text_area(
    tr["notes_label"],
    placeholder=tr["notes_placeholder"],
    height=150,
    key=notes_key
)

# ----------------------
# Reflektio-painike
# ----------------------
if st.button(tr["button"]):
    checked_keys = [k for k, v in responses.items() if v]
    checked_labels = [questions[k] for k in checked_keys]
    categories = tr.get("question_categories", {})
    checked_categories = [categories.get(k, k) for k in checked_keys]

    st.session_state.show_reflection = True
    st.session_state.reflection_data = {
        "checked_keys": checked_keys,
        "checked_labels": checked_labels,
        "checked_categories": checked_categories,
        "safe_slider": safe_slider,
        "notes": notes,
    }

    try:
        with open("facts.json", encoding="utf-8") as fh:
            facts = json.load(fh)
    except FileNotFoundError:
        facts = {"follow_up_support": []}
    except json.JSONDecodeError:
        facts = {"follow_up_support": []}
    except Exception:
        facts = {"follow_up_support": []}

    st.session_state.reflection_text = generate_ai_reflection(
        st.session_state.selected_lang,
        st.session_state.reflection_data,
        facts,
        tr
    )

# Näytä reflektio
if st.session_state.show_reflection and st.session_state.reflection_data is not None:
    data = st.session_state.reflection_data
    
    st.subheader(tr["incoming_subheader"])
    st.write(f"{tr['safety_prefix']} {data['safe_slider']}")

    st.write(tr["selected_indicators"])
    if data["checked_categories"]:
        for item in data["checked_categories"]:
            st.write(f"- {item}")
    else:
        st.write(tr["no_indicators"])

    if data["notes"]:
        st.write(tr["case_notes"])
        st.write(data["notes"])

    st.markdown("---")
    st.subheader(tr["reflection_header"])
    st.markdown(st.session_state.reflection_text)
else:
    st.write(tr["button_prompt"])

st.markdown("---\n" + tr["footer"])