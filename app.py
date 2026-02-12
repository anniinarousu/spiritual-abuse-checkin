# Hengellisen väkivallan merkkien tunnistaminen -sovellus
# Tämä Streamlit-sovellus auttaa kartoittamaan hengellisen väkivallan merkkejä.
# Kielivalinta: Suomi / English / Svenska

import streamlit as st
import json

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

/* Yläpalkin ikonit (share, tähti, kynä, github, kolme pistettä) */
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
[data-testid="stSidebar"] p {
    color: white !important;
}

/* Checkbox - poista turkoosi boxi, pidä lila tausta */
[data-testid="stSidebar"] .stCheckbox {
    background-color: transparent !important;
}
[data-testid="stSidebar"] .stCheckbox > div {
    background-color: transparent !important;
}
[data-testid="stSidebar"] .stCheckbox label {
    background-color: transparent !important;
    color: white !important;
}
[data-testid="stSidebar"] .stCheckbox > div > div {
    background-color: transparent !important;
}

/* Checkbox täppä - turkoosi väri */
[data-testid="stSidebar"] input[type="checkbox"]:checked + div > svg {
    color: #85dbd9 !important;
    fill: #85dbd9 !important;
}
[data-testid="stSidebar"] .stCheckbox svg {
    color: #85dbd9 !important;
    fill: #85dbd9 !important;
}

/* Slider - poista kaikki taustavärit */
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stSlider > div,
[data-testid="stSidebar"] .stSlider > div > div,
[data-testid="stSidebar"] .stSlider > div > div > div,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] .stSlider label {
    background-color: transparent !important;
    background: transparent !important;
}

/* Slider numero - valkoinen */
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div:last-child {
    color: white !important;
}

/* Slider palkki - MOLEMMAT puolet turkoosi */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div:first-child > div,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    background: #85dbd9 !important;
    background-color: #85dbd9 !important;
}

/* Slider track - koko palkki turkoosi */
[data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] div[role="slider"] ~ div,
[data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] > div > div:first-child {
    background: #85dbd9 !important;
}

/* Slider nuppi - turkoosi */
[data-testid="stSidebar"] .stSlider [role="slider"] {
    background-color: #85dbd9 !important;
    border-color: #85dbd9 !important;
}

/* Luo reflektio -painike */
.stButton > button {
    background-color: #85dbd9 !important;
    color: white !important;
    border: none !important;
}
.stButton > button:hover {
    background-color: #6bc9c7 !important;
}

/* Reflektio info-laatikko */
[data-testid="stAlert"],
.stAlert {
    background-color: #85dbd9 !important;
    border: none !important;
    color: white !important;
}
.stAlert p, .stAlert div, .stAlert span {
    color: white !important;
}

/* Text area sivupalkissa */
[data-testid="stSidebar"] .stTextArea {
    background-color: transparent !important;
}
[data-testid="stSidebar"] .stTextArea > div {
    background-color: transparent !important;
}
[data-testid="stSidebar"] .stTextArea textarea {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
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
# Kysymykset perustuvat UUT:n (Uskontojen uhrien tuki) materiaaliin
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
        "severity_high": "Vakavia huolenaiheita havaittu",
        "severity_medium": "Useita huolenaiheita havaittu",
        "severity_low": "Joitakin huolenaiheita havaittu",
        "severity_none": "Ei merkittäviä huolenaiheita havaittu",
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
        "severity_high": "Serious concerns identified",
        "severity_medium": "Multiple concerns identified",
        "severity_low": "Some concerns identified",
        "severity_none": "No significant concerns identified",
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
        "severity_high": "Allvarliga bekymmer identifierade",
        "severity_medium": "Flera bekymmer identifierade",
        "severity_low": "Vissa bekymmer identifierade",
        "severity_none": "Inga betydande bekymmer identifierade",
    },
}


# ----------------------
# AI-avusteinen reflektio
# ----------------------
def generate_ai_reflection(lang, data, facts, tr):
    """
    Generoi älykkään, kontekstuaalisen reflektion valittujen indikaattorien perusteella.
    Analysoi vastaukset ja tuottaa kategoriakohtaista palautetta.
    """
    checked_keys = data.get("checked_keys", [])
    checked_labels = data.get("checked_labels", [])
    safe = data.get("safe_slider", 3)
    notes = data.get("notes", "")
    categories = tr.get("question_categories", {})
    
    # Määritä vakavuustaso
    num_indicators = len(checked_keys)
    if num_indicators >= 5:
        severity = "high"
    elif num_indicators >= 3:
        severity = "medium"
    elif num_indicators >= 1:
        severity = "low"
    else:
        severity = "none"
    
    reflection_parts = []
    
    # === SUOMI ===
    if lang == "Suomi":
        # Otsikko vakavuuden mukaan
        if severity == "high":
            reflection_parts.append(f"## ⚠️ {tr['severity_high']}\n")
        elif severity == "medium":
            reflection_parts.append(f"## ⚡ {tr['severity_medium']}\n")
        elif severity == "low":
            reflection_parts.append(f"## 📋 {tr['severity_low']}\n")
        else:
            reflection_parts.append(f"## ✅ {tr['severity_none']}\n")
        
        # Turvallisuusarvio
        reflection_parts.append(f"**Turvallisuuden kokemus:** {safe}/5")
        if safe <= 2:
            reflection_parts.append("*Asiakkaan turvallisuuden kokemus on matala. Tämä on tärkeä huomioida keskustelussa.*\n")
        elif safe >= 4:
            reflection_parts.append("*Asiakas kokee voivansa keskustella suhteellisen turvallisesti.*\n")
        else:
            reflection_parts.append("")
        
        # Analyysi valituista kategorioista
        if checked_keys:
            reflection_parts.append("### Havaitut hengellisen väkivallan muodot\n")
            reflection_parts.append("Kartoituksen perusteella asiakkaan kokemuksessa nousee esiin seuraavia hengellisen väkivallan piirteitä:\n")
            
            for key in checked_keys:
                category_name = categories.get(key, key)
                reflection_parts.append(f"**{category_name}**")
                
                # Kategoria-kohtaiset selitykset ja suositukset
                if key == "pelottelu":
                    reflection_parts.append("Pelottelua Jumalan rangaistuksilla tai pahoilla hengillä käytetään usein kontrolloimaan yhteisön jäseniä. Tämä voi aiheuttaa syvää ahdistusta ja pelkoa, joka vaikuttaa arkeen myös yhteisön ulkopuolella.\n")
                elif key == "kontrolli":
                    reflection_parts.append("Yksityiselämän kontrollointi uskonnollisin perustein rajoittaa ihmisen autonomiaa ja itsemääräämisoikeutta. Tämä voi vaikuttaa identiteettiin ja kykyyn tehdä itsenäisiä päätöksiä.\n")
                elif key == "eristaminen":
                    reflection_parts.append("Sosiaalinen eristäminen heikentää tukiverkostoa ja lisää riippuvuutta yhteisöstä. Yhteyksien rajoittaminen voi tehdä yhteisöstä lähtemisen erittäin vaikeaksi.\n")
                elif key == "hapaiseminen":
                    reflection_parts.append("Julkinen häpäiseminen ja nöyryyttäminen voivat aiheuttaa syvää häpeää ja traumaa. Tämä on vakava vallankäytön muoto.\n")
                elif key == "autonomia":
                    reflection_parts.append("Oman ajattelun ja tunteiden kieltäminen murentaa identiteettiä ja itseluottamusta. Toipuminen vaatii usein oman äänen ja arvojen uudelleen löytämistä.\n")
                elif key == "seksuaalisuus":
                    reflection_parts.append("Seksuaalisen itsemääräämisoikeuden loukkaaminen on vakava väkivallan muoto. Tämä voi aiheuttaa pitkäaikaisia vaikutuksia kehosuhteeseen ja seksuaalisuuteen.\n")
                elif key == "sielunhoito":
                    reflection_parts.append("Hengellisen tuen vääristäminen rikkoo luottamusta ja voi tehdä avun hakemisesta vaikeaa tulevaisuudessa.\n")
                elif key == "vaikeneminen":
                    reflection_parts.append("Painostus vaieta väkivallasta estää avun saamisen ja suojelee tekijöitä. Tämä voi aiheuttaa syvää yksinäisyyttä ja häpeää.\n")
                elif key == "sukupuoli":
                    reflection_parts.append("Syrjintä sukupuolen tai seksuaalisen suuntautumisen vuoksi voi aiheuttaa syvää häpeää ja identiteettikriisin.\n")
                elif key == "talous":
                    reflection_parts.append("Taloudellinen riisto voi aiheuttaa konkreettisia ongelmia toimeentuloon ja lisätä riippuvuutta yhteisöstä.\n")
                elif key == "terveys":
                    reflection_parts.append("Terveydenhuollon rajoittaminen vaarantaa fyysisen ja psyykkisen terveyden.\n")
            
            # Kokonaisarvio
            reflection_parts.append("### Kokonaisarvio\n")
            if severity == "high":
                reflection_parts.append("Asiakkaan kokemuksessa on useita vakavia hengellisen väkivallan piirteitä. On tärkeää varmistaa asiakkaan turvallisuus ja ohjata ammatilliseen tukeen.\n")
            elif severity == "medium":
                reflection_parts.append("Asiakkaan kokemuksessa on merkittäviä hengellisen väkivallan piirteitä. Suositellaan jatkotukea ja tilanteen seurantaa.\n")
            else:
                reflection_parts.append("Asiakkaan kokemuksessa on joitakin huolenaiheita. Keskustelun jatkaminen ja tilanteen kartoittaminen on suositeltavaa.\n")
        else:
            reflection_parts.append("Kartoituksen perusteella ei havaittu selkeitä hengellisen väkivallan indikaattoreita. Tämä ei kuitenkaan sulje pois kokemuksia – asiakas ei välttämättä ole valmis kertomaan kaikesta.\n")
        
        # Muistiinpanot
        if notes:
            reflection_parts.append(f"### Muistiinpanot\n{notes}\n")
        
        # Suositukset
        reflection_parts.append("### Suositeltavat toimenpiteet\n")
        reflection_parts.append("- **Kuuntele** empaattisesti ja vahvista asiakkaan kokemukset todellisiksi")
        reflection_parts.append("- **Vältä** vähättelyä tai painostamista toimintaan, johon asiakas ei ole valmis")
        reflection_parts.append("- **Arvioi** välitön turvallisuustilanne")
        reflection_parts.append("- **Ohjaa** tarvittaessa ammatilliseen tukeen")
        
    # === ENGLISH ===
    elif lang == "English":
        if severity == "high":
            reflection_parts.append(f"## ⚠️ {tr['severity_high']}\n")
        elif severity == "medium":
            reflection_parts.append(f"## ⚡ {tr['severity_medium']}\n")
        elif severity == "low":
            reflection_parts.append(f"## 📋 {tr['severity_low']}\n")
        else:
            reflection_parts.append(f"## ✅ {tr['severity_none']}\n")
        
        reflection_parts.append(f"**Safety experience:** {safe}/5")
        if safe <= 2:
            reflection_parts.append("*The client's sense of safety is low. This is important to consider in the conversation.*\n")
        elif safe >= 4:
            reflection_parts.append("*The client feels relatively safe to discuss.*\n")
        else:
            reflection_parts.append("")
        
        if checked_keys:
            reflection_parts.append("### Identified forms of spiritual abuse\n")
            reflection_parts.append("Based on the check-in, the following characteristics of spiritual abuse emerge in the client's experience:\n")
            
            for key in checked_keys:
                category_name = categories.get(key, key)
                reflection_parts.append(f"**{category_name}**")
                
                if key == "pelottelu":
                    reflection_parts.append("Intimidation with God's punishment or evil spirits is often used to control community members. This can cause deep anxiety and fear.\n")
                elif key == "kontrolli":
                    reflection_parts.append("Controlling private life on religious grounds limits a person's autonomy and self-determination.\n")
                elif key == "eristaminen":
                    reflection_parts.append("Social isolation weakens support networks and increases dependence on the community.\n")
                elif key == "hapaiseminen":
                    reflection_parts.append("Public shaming and humiliation can cause deep shame and trauma.\n")
                elif key == "autonomia":
                    reflection_parts.append("Denying one's own thinking and feelings erodes identity and self-confidence.\n")
                elif key == "seksuaalisuus":
                    reflection_parts.append("Violation of sexual autonomy is a serious form of violence.\n")
                elif key == "sielunhoito":
                    reflection_parts.append("Distortion of spiritual support breaks trust and can make seeking help difficult.\n")
                elif key == "vaikeneminen":
                    reflection_parts.append("Pressure to remain silent about violence prevents getting help and protects perpetrators.\n")
                elif key == "sukupuoli":
                    reflection_parts.append("Discrimination based on gender or sexual orientation can cause deep shame.\n")
                elif key == "talous":
                    reflection_parts.append("Financial exploitation can cause concrete problems and increase dependence on the community.\n")
                elif key == "terveys":
                    reflection_parts.append("Restricting healthcare endangers physical and mental health.\n")
            
            reflection_parts.append("### Overall assessment\n")
            if severity == "high":
                reflection_parts.append("The client's experience shows multiple serious characteristics of spiritual abuse. It is important to ensure the client's safety and refer to professional support.\n")
            elif severity == "medium":
                reflection_parts.append("The client's experience shows significant characteristics of spiritual abuse. Continued support and monitoring is recommended.\n")
            else:
                reflection_parts.append("The client's experience shows some concerns. Continuing the conversation and mapping the situation is recommended.\n")
        else:
            reflection_parts.append("Based on the check-in, no clear indicators of spiritual abuse were identified. However, this does not rule out experiences – the client may not be ready to share everything.\n")
        
        if notes:
            reflection_parts.append(f"### Notes\n{notes}\n")
        
        reflection_parts.append("### Recommended actions\n")
        reflection_parts.append("- **Listen** empathetically and validate the client's experiences")
        reflection_parts.append("- **Avoid** minimizing or pressuring action the client is not ready for")
        reflection_parts.append("- **Assess** immediate safety situation")
        reflection_parts.append("- **Refer** to professional support if needed")
        
    # === SVENSKA ===
    elif lang == "Svenska":
        if severity == "high":
            reflection_parts.append(f"## ⚠️ {tr['severity_high']}\n")
        elif severity == "medium":
            reflection_parts.append(f"## ⚡ {tr['severity_medium']}\n")
        elif severity == "low":
            reflection_parts.append(f"## 📋 {tr['severity_low']}\n")
        else:
            reflection_parts.append(f"## ✅ {tr['severity_none']}\n")
        
        reflection_parts.append(f"**Trygghetsupplevelse:** {safe}/5")
        if safe <= 2:
            reflection_parts.append("*Klientens trygghetsupplevelse är låg. Detta är viktigt att beakta i samtalet.*\n")
        elif safe >= 4:
            reflection_parts.append("*Klienten känner sig relativt trygg att diskutera.*\n")
        else:
            reflection_parts.append("")
        
        if checked_keys:
            reflection_parts.append("### Identifierade former av andligt våld\n")
            reflection_parts.append("Baserat på check-in framträder följande kännetecken på andligt våld i klientens upplevelse:\n")
            
            for key in checked_keys:
                category_name = categories.get(key, key)
                reflection_parts.append(f"**{category_name}**")
                reflection_parts.append("Detta är en allvarlig form av andligt våld som kräver uppmärksamhet.\n")
            
            reflection_parts.append("### Övergripande bedömning\n")
            if severity == "high":
                reflection_parts.append("Klientens upplevelse visar flera allvarliga kännetecken på andligt våld. Det är viktigt att säkerställa klientens säkerhet och hänvisa till professionellt stöd.\n")
            elif severity == "medium":
                reflection_parts.append("Klientens upplevelse visar betydande kännetecken på andligt våld. Fortsatt stöd och uppföljning rekommenderas.\n")
            else:
                reflection_parts.append("Klientens upplevelse visar vissa bekymmer. Att fortsätta samtalet och kartlägga situationen rekommenderas.\n")
        else:
            reflection_parts.append("Baserat på check-in identifierades inga tydliga indikatorer på andligt våld. Detta utesluter dock inte upplevelser – klienten kanske inte är redo att dela allt.\n")
        
        if notes:
            reflection_parts.append(f"### Anteckningar\n{notes}\n")
        
        reflection_parts.append("### Rekommenderade åtgärder\n")
        reflection_parts.append("- **Lyssna** empatiskt och bekräfta klientens upplevelser")
        reflection_parts.append("- **Undvik** att minimera eller pressa till handling klienten inte är redo för")
        reflection_parts.append("- **Bedöm** omedelbar säkerhetssituation")
        reflection_parts.append("- **Hänvisa** till professionellt stöd vid behov")
    
    # Lisää lähteet ja tukipalvelut facts.json:sta
    reflection_parts.append("\n---\n")
    
    support_header = {
        "Suomi": "### Tukipalvelut ja lisätiedot",
        "English": "### Support services and additional information",
        "Svenska": "### Stödtjänster och ytterligare information"
    }
    reflection_parts.append(support_header[lang])
    
    for s in facts.get("follow_up_support", []):
        name = s.get('name', s.get('text', ''))
        source = s.get('source', '')
        if name and source:
            reflection_parts.append(f"- [{name}]({source})")
    
    return "\n".join(reflection_parts)


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
        st.warning("facts.json-tiedostoa ei löytynyt.")
        facts = {"follow_up_support": []}
    except json.JSONDecodeError:
        st.error("facts.json-tiedoston lukeminen epäonnistui.")
        facts = {"follow_up_support": []}
    except Exception as e:
        st.error(f"Virhe: {e}")
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