import streamlit as st
import openai
import PyPDF2

# --- OLDAL BEÁLLÍTÁSOK ---
st.set_page_config(
    page_title="LexiBridge AI - Jogi Elemző",
    page_icon="⚖️",
    layout="centered"
)

# --- API KULCS KEZELÉS (FONTOS!) ---
# Amikor élesítjük a weboldalt, ezt ki fogjuk cserélni egy biztonságos megoldásra!
# Most még maradhat itt teszteléshez, DE NE TÖLTSD FEL SEHOVA NYILVÁNOSAN!
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- FŐ CÍMSOROK ---
st.title("⚖️ LexiBridge AI")
st.header("Nemzetközi szerződések villámgyors elemzése")
st.markdown("""
**Spórolj órákat, csökkentsd a kockázatot.** Ez az eszköz mesterséges intelligenciával olvassa át az angol vagy spanyol nyelvű 
jogi dokumentumokat (PDF), és magyarul foglalja össze a lényeget.
""")

st.divider()

# --- OLDSÁV (KAPCSOLAT) ---
with st.sidebar:
    st.header("📞 Kapcsolat & Infó")
    st.info(
        """
        Ez egy **LegalTech MVP (prototípus)**, 
        melyet egy 16 éves leendő jogász-fejlesztő készített.
        """
    )
    st.markdown("---")
    st.write("**Fejlesztő:** [A Te Neved]") # Írd át a nevedre!
    st.write("📧 Email: te.email.cimed@gmail.com") # Írd át!
    st.write("💼 LinkedIn: [Profil link]") # Ha van

# --- FŐ RÉSZ: FELTÖLTÉS ÉS ELEMZÉS ---
st.subheader("📄 Dokumentum feltöltése")
feltoltott_fajl = st.file_uploader("Húzd ide a szerződést (csak PDF formátum)", type="pdf")

if feltoltott_fajl is not None:
    # PDF beolvasása
    with st.spinner('PDF feldolgozása...'):
        pdf_olvaso = PyPDF2.PdfReader(feltoltott_fajl)
        teljes_szoveg = ""
        for oldal in pdf_olvaso.pages:
            szoveg = oldal.extract_text()
            if szoveg:
                teljes_szoveg += szoveg

    st.success(f"✅ PDF sikeresen beolvasva! ({len(pdf_olvaso.pages)} oldal)")
    st.markdown("---")

    # Elemzés gomb
    if st.button("🚀 AI Elemzés Indítása", type="primary"):
        if len(teljes_szoveg) < 50:
             st.error("Hiba: Nem sikerült elég szöveget kinyerni a PDF-ből. Lehet, hogy szkennelt kép?")
        else:
            with st.spinner('Az AI jogi asszisztens dolgozik... (ez eltarthat 10-20 másodpercig)'):
                try:
                    # A Prompt (az utasítás)
                    prompt_text = f"""
                    Te egy profi, nemzetközi jogban jártas asszisztens vagy. 
                    Feladatod az alábbi (angol vagy spanyol) szerződésszöveg elemzése.
                    
                    Válaszolj MAGYARUL, strukturáltan, az alábbi pontok szerint:
                    ### 👥 1. Szerződő Felek
                    [Kik a felek? Mi a szerepük?]

                    ### 🗓️ 2. Kulcsfontosságú Határidők és Fizetési Feltételek
                    [Mikor kell fizetni? Mennyit? Mik a mérföldkövek? Kötbér?]

                    ### ⚠️ 3. Fő Kockázatok és Kötelezettségek
                    [Mik a legveszélyesebb pontok a megbízott számára? Van-e rejtett költség?]

                    ### 📝 4. Vezetői Összefoglaló (TL;DR)
                    [3 tömör mondatban a szerződés lényege.]

                    ---
                    A SZERZŐDÉS SZÖVEGE (Részlet):
                    {teljes_szoveg[:5000]} # Az első 5000 karaktert küldjük
                    """

                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt_text}],
                        temperature=0.3 # Alacsonyabb érték = tényszerűbb válaszok
                    )
                    
                    # Eredmény megjelenítése
                    st.balloons() # Kis ünneplés, ha kész
                    st.subheader("📋 Elemzési Eredmény")
                    st.markdown(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Hiba történt az AI kommunikáció során: {e}")
                    st.warning("Ellenőrizd az API kulcsodat és az internetkapcsolatot!")