# Hengellisen väkivallan merkkien tunnistaminen -sovellus
# Tämä Streamlit-sovellus auttaa kartoittamaan hengellisen väkivallan merkkejä.
# Kielivalinta: Suomi / English / Svenska

import streamlit as st
import json

# ----------------------
# Väriympäristön määritys
# ----------------------
# Käytetään värien kombinaatiota: tumma violetti, vaalea violetti, harmaa ja vaalea vihreä.
# Värit tuodaan näkyviin CSS-tyyleillä.
color_scheme = """
<style>
/* Tumma violetti taustalle ja otsikoille */
.main {
    background-color: #f8f5f0;
}
h1 {
    color: #5a2d82;
    font-weight: bold;
}
h2, h3 {
    color: #6b3fa0;
}
/* Vaalea violetti sivupalkkiin */
[data-testid="stSidebar"] {
    background-color: #ede4f0;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
    color: #5a2d82;
}
/* Vaalea vihreä painikkeille */
button {
    background-color: #a8d5a8 !important;
    color: #2d5a2d !important;
    border: none !important;
}
button:hover {
    background-color: #8ecb8e !important;
}
</style>
"""
st.markdown(color_scheme, unsafe_allow_html=True)

# ----------------------
# Session state -alustus
# ----------------------
# Streamlit nollaa muuttujat jokaisen painikepainallon jälkeen.
# Session state auttaa säilyttämään checkboxit ja muut tulokset.
if 'show_reflection' not in st.session_state:
    st.session_state.show_reflection = False
if 'reflection_data' not in st.session_state:
    st.session_state.reflection_data = None
if 'reflection_text' not in st.session_state:
    st.session_state.reflection_text = ""

# ----------------------
# Käännösten sanakirja
# ----------------------
# Avaimet ovat kielen näyttönimet. Jokainen arvo on sanakirja,
# joka kartoittaa UI-elementtien nimet käännettyihin merkkijonoihin.
translations = {
    "Suomi": {
        "title": "Hengellisen väkivallan merkkien tunnistaminen",
        "intro": (
            "Tämä työkalu on tarkoitettu nopeaan, ei-kliiniseen tarkistukseen. "
            "Se ei korvaa ammattimaista diagnoosia tai hoitoa. Käytä trauma-tietoista, "
            "kunnioittavaa kieltä ja älä kirjaa henkilötietoja."
        ),
        "sidebar_header": "Kysymyksiä asiakkaan tilanteen kartoittamiseksi",
        "questions": [
            "Kokeeko asiakas hengellistä painostusta tai pakottamista?",
            "Kokeeko asiakas pelkoa seurauksista, jos ei noudata ryhmän käytäntöjä?",
            "Kokeeko asiakas kontrollin tai vallankäytön kokemusta johtajien taholta?",
            "Kokeeko asiakas häpeän tai syyllisyyden korostamista hengellisissä asioissa?",
            "Kokeeko asiakas eristäytymistä tai yhteyksien rajoittamista?",
            "Kokeeko asiakas auktoriteetin tai johtajan väärinkäyttöä (emotionaalinen tai hengellinen)?",
            "Kokeeko asiakas rajoituksia omien rajojen ilmaisussa?",
            "Kokeeko asiakas uhkaa rangaistuksista tai sosiaalisesta eristämisestä eriävää mieltä kohtaan?",
        ],
        "slider_label": "Kuinka turvalliseksi asiakas tuntee olonsa keskustellessaan hengellisistä asioista?",
        "slider_scale_explanation": "1 = Asiakas tuntee itsensä hyvin pelokkaaksi ja 5 = Asiakas tuntee olonsa hyvin turvalliseksi.",
        "notes_label": "Vapaa muistiinpano (valinnainen, EI henkilötietoja)",
        "notes_placeholder": "Kirjaa lyhyitä havaintoja, huolia tai turvallisuuteen liittyviä huomioita...",
        "button": "Luo reflektio",
        "button_prompt": "Paina 'Luo reflektio' luodaksesi ehdotetun reflektiotekstin.",
        "incoming_subheader": "Sisääntulevat tiedot",
        "safety_prefix": "Turvallisuuden arvio (1–5):",
        "selected_indicators": "Valitut indikaattorit:",
        "no_indicators": "- Ei valittuja indikaattoreita",
        "case_notes": "Tapauksen muistiinpanot:",
        "reflection_header": "Reflektio",
        "reflection_placeholder": "Reflektio luotu tähän",
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
        "questions": [
            "Does the client experience spiritual pressure or coercion?",
            "Does the client fear consequences for not following group practices?",
            "Does the client experience control or abuse of power from leaders?",
            "Does the client experience emphasis on shame or guilt in spiritual matters?",
            "Does the client experience isolation or restricted contacts?",
            "Does the client experience misuse of authority by leaders (emotional or spiritual)?",
            "Does the client experience restrictions on expressing personal boundaries?",
            "Does the client experience threats of punishment or social exclusion for dissent?",
        ],
        "slider_label": "How safe does the client feel discussing spiritual matters?",
        "slider_scale_explanation": "1 = Client feels very fearful and 5 = Client feels very safe.",
        "notes_label": "Free-form case notes (optional, NO personal data)",
        "notes_placeholder": "Write short observations, concerns or safety notes...",
        "button": "Generate reflection",
        "button_prompt": "Press 'Generate reflection' to create a suggested reflection text.",
        "incoming_subheader": "Incoming information",
        "safety_prefix": "Safety rating (1–5):",
        "selected_indicators": "Selected indicators:",
        "no_indicators": "- No selected indicators",
        "case_notes": "Case notes:",
        "reflection_header": "Reflection",
        "reflection_placeholder": "Reflection generated here",
        "footer": "**Note:** Keep confidentiality, do not store personal data.",
        "language_label": "Language",
    },
    "Svenska": {
        "title": "Check-in för andliga övergrepp",
        "intro": (
            "Detta verktyg är avsett för en snabb, icke-klinisk check-in. "
            "Det ersätter inte professionell diagnos eller vård. Använd traumamedvetet, respektfullt språk "
            "och registrera inte personuppgifter."
        ),
        "sidebar_header": "Frågor för att kartlägga klientens situation",
        "questions": [
            "Upplever klienten andlig press eller tvång?",
            "Upplever klienten rädsla för konsekvenser om hen inte följer gruppens rutiner?",
            "Upplever klienten kontroll eller maktmissbruk från ledare?",
            "Upplever klienten skuld eller skam betonas i andliga frågor?",
            "Upplever klienten isolering eller begränsade kontakter?",
            "Upplever klienten ledarens maktmissbruk (emotionellt eller andligt)?",
            "Upplever klienten begränsningar i att uttrycka sina gränser?",
            "Upplever klienten hot om straff eller social uteslutning vid avvikande åsikt?",
        ],
        "slider_label": "Hur trygg känner sig klienten att diskutera andliga frågor?",
        "slider_scale_explanation": "1 = Klienten känner sig mycket rädd och 5 = Klienten känner sig mycket trygg.",
        "notes_label": "Fritt anteckningar (valfritt, INGA personuppgifter)",
        "notes_placeholder": "Skriv korta observationer, oro eller säkerhetsanteckningar...",
        "button": "Generera reflektion",
        "button_prompt": "Tryck 'Generera reflektion' för att skapa ett förslag till reflektion.",
        "incoming_subheader": "Inkommande uppgifter",
        "safety_prefix": "Trygghetsbedömning (1–5):",
        "selected_indicators": "Valda indikatorer:",
        "no_indicators": "- Inga valda indikatorer",
        "case_notes": "Fallanteckningar:",
        "reflection_header": "Reflektion",
        "reflection_placeholder": "Reflektion genererad här",
        "footer": "**Obs!** Behåll konfidentialitet, spara inte personuppgifter.",
        "language_label": "Språk",
    },
}


# ----------------------
# Generoi reflektio-teksti syötteiden perusteella
# ----------------------
def generate_reflection(lang, tr, data, facts):
    """Palauttaa lyhyen, trauma-tietoisen reflektiotekstin valitulla kielellä.

    - `lang` on valittu kieli (Suomi/English/Svenska)
    - `tr` on käännössanakirja kyseiselle kielelle
    - `data` sisältää avaimet: checked (lista), safe_slider (int), notes (str)
    """
    checked = data.get("checked", [])
    safe = data.get("safe_slider", "")
    notes = data.get("notes", "")

    # Rakennetaan ensin perusreflektio kielikohtaisesti
    base = []
    if lang == "Suomi":
        base.append(f"Turvallisuuden arvio: {safe}/5.")
        if checked:
            base.append("Havainnot: " + "; ".join(checked) + ".")
        else:
            base.append("Ei havaittuja indikaattoreita.")
        if notes:
            base.append("Muistiinpanot: " + notes)
        base.append(
            "Ehdotus: Kuuntele empaattisesti, vahvista asiakkaan tunteet ja kartoita välittömät turvallisuustoimet. Tarvittaessa ohjaa ammatilliseen tukeen."
        )
    elif lang == "English":
        base.append(f"Safety rating: {safe}/5.")
        if checked:
            base.append("Observations: " + "; ".join(checked) + ".")
        else:
            base.append("No selected indicators.")
        if notes:
            base.append("Notes: " + notes)
        base.append(
            "Suggested approach: Listen with empathy, validate feelings, assess immediate safety needs, and consider referral to professional support."
        )
    elif lang == "Svenska":
        base.append(f"Trygghetsbedömning: {safe}/5.")
        if checked:
            base.append("Observationer: " + "; ".join(checked) + ".")
        else:
            base.append("Inga valda indikatorer.")
        if notes:
            base.append("Anteckningar: " + notes)
        base.append(
            "Förslag: Lyssna empatiskt, bekräfta klientens känslor, bedöm omedelbara säkerhetsbehov och överväg remiss till professionellt stöd."
        )

    # Lisätään facts.json -sisältö loppuun (merkit, ohjeistus ja jatkotuki)
    facts_parts = ["\n\n---\n\n"]
    facts_parts.append({"Suomi": "Havaittuja merkkejä ja lähteitä:", "English": "Signs and sources:", "Svenska": "Tecken och källor:"}[lang])
    for f in facts.get("signs_of_spiritual_abuse", []):
        facts_parts.append(f"- {f['text']} ([lähde]({f['source']}))")

    facts_parts.append("")
    facts_parts.append({"Suomi": "Ohjeita tukemiseen:", "English": "Guidance for support:", "Svenska": "Vägledning för stöd:"}[lang])
    for g in facts.get("guidance_for_support", []):
        facts_parts.append(f"- {g['text']} ([lähde]({g['source']}))")

    facts_parts.append("")
    facts_parts.append({"Suomi": "Jatkotoimet ja tukipalvelut:", "English": "Next steps and follow-up support:", "Svenska": "Nästa steg och uppföljningsstöd:"}[lang])
    for s in facts.get("follow_up_support", []):
        facts_parts.append(f"- {s.get('name', s.get('text'))} ([linkki]({s['source']}))")

    return "\n\n".join(base + facts_parts)

# ----------------------
# Kielivalinta (ylä oikealla)
# ----------------------
# Käytämme kolumneja kielivalinnan asetteluun oikeaan yläkulmaan.
lang_options = ["Suomi", "English", "Svenska"]
cols = st.columns([3, 1])

with cols[1]:
    selected_lang = st.selectbox(
        translations[lang_options[0]]["language_label"],
        lang_options,
        index=0
    )

# Lyhennysmerkintä valittujen käännösten hakemiseen
tr = translations[selected_lang]

# ----------------------
# Sivun otsikko ja esittely
# ----------------------
st.set_page_config(page_title=tr["title"])
st.title(tr["title"])
st.markdown(tr["intro"])

# ----------------------
# Sivupalkin paneelit (käytämme käännöksiä)
# ----------------------
st.sidebar.header(tr["sidebar_header"])

# Kysymykset (muuttujanimike `questions` säilytetty logiikan vuoksi)
questions = tr["questions"]

# Alusta session state checkboxeille jos se ei vielä löydy
if 'checkbox_responses' not in st.session_state:
    st.session_state.checkbox_responses = {i: False for i in range(len(questions))}

# Tallenna vastaukset sanakirjaan, käyttäen session state:a säilyttämään arvot
responses = {}
for idx, q in enumerate(questions):
    # key-parametri yhdistää checkboxin session state:en
    value = st.sidebar.checkbox(
        q,
        value=st.session_state.checkbox_responses[idx],
        key=f"checkbox_{idx}"
    )
    responses[q] = value
    # Päivitä session state checkboxien arvot
    st.session_state.checkbox_responses[idx] = value

# Liukusäädin turvallisuuskokemukselle
safe_slider = st.sidebar.slider(tr["slider_label"], min_value=1, max_value=5, value=3)

# Asteikon selvennys
st.sidebar.markdown(tr["slider_scale_explanation"])

# Muistiinpanoalue
notes = st.sidebar.text_area(
    tr["notes_label"],
    placeholder=tr["notes_placeholder"],
    height=150
)

# ----------------------
# Reflektio-painike ja tuloste (logiikka säilytetty)
# ----------------------
# Painike tallentaa tiedot session state:iin, ja lataa facts.json
# joka sisältää merkit, ohjeet ja jatkotuen linkit. Tämä tiedosto luetaan
# paikallisesti, ja sen tiedot liitetään generoituun reflektioon.
if st.button(tr["button"]):
    # Kerää valitut indikaattorit
    checked = [k for k, v in responses.items() if v]

    # Tallenna reflektio-tiedot session state:iin
    st.session_state.show_reflection = True
    st.session_state.reflection_data = {
        "checked": checked,
        "safe_slider": safe_slider,
        "notes": notes,
    }

    # Ladataan paikallinen facts.json – sisältää lähde-linkit ja vinkit
    try:
        with open("facts.json", encoding="utf-8") as fh:
            facts = json.load(fh)
    except Exception:
        facts = {}

    # Luo reflektioteksti ja tallenna se
    st.session_state.reflection_text = generate_reflection(selected_lang, tr, st.session_state.reflection_data, facts)

# Näytä reflektio jos nappia on painettu (tiedot on session state:ssa)
if st.session_state.show_reflection and st.session_state.reflection_data is not None:
    data = st.session_state.reflection_data
    
    st.subheader(tr["incoming_subheader"])
    st.write(f"{tr['safety_prefix']} {data['safe_slider']}")

    st.write(tr["selected_indicators"])
    if data["checked"]:
        for item in data["checked"]:
            st.write(f"- {item}")
    else:
        st.write(tr["no_indicators"])

    if data["notes"]:
        st.write(tr["case_notes"])
        st.write(data["notes"])

    st.markdown("---")
    st.subheader(tr["reflection_header"])
    # Näytetään generoitu reflektio-teksti
    st.info(st.session_state.reflection_text)
else:
    st.write(tr["button_prompt"])

# Alatunnisteohje
st.markdown("---\n" + tr["footer"])
