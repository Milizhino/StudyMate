import streamlit as st
import json
import os
import bcrypt
import requests
import base64
from pypdf import PdfReader
import cv2
import tempfile
from datetime import datetime


# ==================================================
# STUDYMATE
# ==================================================

st.set_page_config(
    page_title="StudyMate",
    page_icon="🎓",
    layout="wide"
)


# ==================================================
# 🌍 JEZICI
# ==================================================

JEZICI = {
    "🇭🇷 Hrvatski": "hr",
    "🇬🇧 English": "en",
    "🇩🇪 Deutsch": "de",
    "🇫🇷 Français": "fr",
    "🇪🇸 Español": "es",
    "🇮🇹 Italiano": "it",
    "🇵🇹 Português": "pt",
    "🇯🇵 日本語": "ja",
    "🇨🇳 中文": "zh",
    "🇰🇷 한국어": "ko",
    "🇷🇺 Русский": "ru",
    "🇸🇦 العربية": "ar",
    "🇹🇷 Türkçe": "tr",
    "🇵🇱 Polski": "pl",
    "🇳🇱 Nederlands": "nl",
    "🇸🇪 Svenska": "sv",
    "🇩🇰 Dansk": "da",
    "🇳🇴 Norsk": "no",
    "🇫🇮 Suomi": "fi",
    "🇨🇿 Čeština": "cs",
    "🇸🇰 Slovenčina": "sk",
    "🇭🇺 Magyar": "hu",
    "🇷🇴 Română": "ro",
    "🇺🇦 Українська": "uk",
    "🇬🇷 Ελληνικά": "el",
    "🇮🇱 עברית": "he",
    "🇮🇳 हिन्दी": "hi",
    "🇻🇳 Tiếng Việt": "vi",
    "🇮🇩 Bahasa Indonesia": "id",
    "🇹🇭 ไทย": "th",
    "🇧🇩 বাংলা": "bn",
    "🇵🇭 Filipino": "fil",
    "🇲🇾 Bahasa Melayu": "ms",
}


if "jezik" not in st.session_state:
    st.session_state.jezik = "hr"


# ==================================================
# 🌍 PRIJEVODI
# ==================================================

PRIJEVODI = {

    "hr": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Tvoj osobni centar za učenje",
        "sto_raditi": "Što želiš raditi?",
        "ai": "🤖 AI pomoćnik",
        "kvizovi": "🧠 Kvizovi",
        "biljeske": "📝 Bilješke",
        "kalkulator": "🧮 Kalkulator",
        "ai_kviz": "✨ Napravi kviz pomoću AI-a",
        "povijest": "📚 Povijest",
        "pocetna": "← Početna",
        "jezik": "🌍 Jezik",

        "dodaj_pitanje": "➕ Dodaj pitanje",
        "pitanje": "Pitanje",
        "odgovor": "Odgovor",
        "tocan_odgovor": "Koji je točan odgovor?",
        "spremi_pitanje": "💾 Spremi pitanje",
        "pitanje_spremljeno": "Pitanje je spremljeno! 🧠",
        "ispuni_pitanje": "Ispuni pitanje i sva 4 odgovora.",
        "rijesi_kviz": "🎯 Riješi kviz",
        "odaberi_odgovor": "Odaberi odgovor:",
        "zavrsi_kviz": "🏆 Završi kviz",
        "rezultat": "🏆 Rezultat",
        "nema_pitanja": "Još nema spremljenih pitanja.",
        "upravljanje_pitanjima": "🗑️ Upravljanje pitanjima",
        "obrisi": "🗑️ Obriši",
        "pitanje_obrisano": "Pitanje je obrisano!",
        "nema_pitanja_brisanje": "Nema pitanja za brisanje.",

        "dodaj_biljesku": "➕ Dodaj bilješku",
        "naslov_biljeske": "Naslov bilješke",
        "sadrzaj_biljeske": "Sadržaj bilješke",
        "pin_zakljucavanje": "🔒 PIN za zaključavanje",
        "zakljucaj_biljesku": "🔒 Zaključaj ovu bilješku",
        "spremi_biljesku": "💾 Spremi bilješku",
        "pin_obavezan": "Za zaključanu bilješku moraš postaviti PIN.",
        "biljeska_spremljena": "Bilješka je spremljena! 📚",
        "ispuni_biljesku": "Upiši naslov i sadržaj bilješke.",
        "moje_biljeske": "📚 Moje bilješke",
        "unesi_pin": "Unesi PIN za otključavanje",
        "otkljucaj": "🔓 Otključaj",
        "pogresan_pin": "❌ Pogrešan PIN.",

        "kalkulator_naslov": "🧮 Matematički kalkulator",
        "upisi_zadatak": "✏️ Upiši matematički zadatak",
        "slikaj_zadatak": "Slikaj zadatak",
        "rijesi_zadatak": "🧮 Riješi zadatak",
        "rjesavam_zadatak": "🤖 Rješavam zadatak...",
        "kalkulator_nedostupan": "❌ Kalkulator trenutno nije dostupan.",
        "citam_sliku": "📷 AI čita matematički zadatak sa slike...",
        "slika_greska": "❌ AI nije uspio obraditi sliku.",
        "unesi_ili_slikaj": "✏️ Upiši matematički zadatak ili 📷 fotografiraj zadatak.",

        "tema_kviza": "📚 Tema kviza",
        "broj_pitanja": "🔢 Broj pitanja",
        "generiraj_kviz": "✨ Generiraj kviz",
        "generira_pitanja": "🤖 AI generira pitanja...",
        "generirano_pitanja": "🎉 Generirano je",
        "pitanja": "pitanja!",
        "neispravan_popis": "❌ AI nije vratio ispravan popis pitanja.",
        "neispravan_format": "❌ AI nije vratio ispravan format pitanja.",
        "ai_nedostupan": "❌ AI trenutno nije dostupan.",
        "unesi_temu": "Upiši temu kviza.",

        "povijest_naslov": "📚 Povijest",
        "tip_zapis": "📝 Zapis",
        "pitanje_povijest": "Pitanje",
        "odgovor_povijest": "Odgovor",
        "obrisi_cijelu_povijest": "🗑️ Obriši cijelu povijest",
        "povijest_obrisana": "Povijest je obrisana.",
        "nema_povijesti": "📭 Još nema spremljenih pitanja i odgovora."
    },

    "en": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Your personal learning center",
        "sto_raditi": "What do you want to do?",
        "ai": "🤖 AI Assistant",
        "kvizovi": "🧠 Quizzes",
        "biljeske": "📝 Notes",
        "kalkulator": "🧮 Calculator",
        "ai_kviz": "✨ Create a quiz with AI",
        "povijest": "📚 History",
        "pocetna": "← Home",
        "jezik": "🌍 Language"
    },

    "de": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Dein persönliches Lernzentrum",
        "sto_raditi": "Was möchtest du machen?",
        "ai": "🤖 KI-Assistent",
        "kvizovi": "🧠 Quiz",
        "biljeske": "📝 Notizen",
        "kalkulator": "🧮 Rechner",
        "ai_kviz": "✨ Quiz mit KI erstellen",
        "povijest": "📚 Verlauf",
        "pocetna": "← Startseite",
        "jezik": "🌍 Sprache"
    },

    "fr": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Ton centre personnel d'apprentissage",
        "sto_raditi": "Que veux-tu faire ?",
        "ai": "🤖 Assistant IA",
        "kvizovi": "🧠 Quiz",
        "biljeske": "📝 Notes",
        "kalkulator": "🧮 Calculatrice",
        "ai_kviz": "✨ Créer un quiz avec l'IA",
        "povijest": "📚 Historique",
        "pocetna": "← Accueil",
        "jezik": "🌍 Langue"
    },

    "es": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Tu centro personal de aprendizaje",
        "sto_raditi": "¿Qué quieres hacer?",
        "ai": "🤖 Asistente de IA",
        "kvizovi": "🧠 Cuestionarios",
        "biljeske": "📝 Notas",
        "kalkulator": "🧮 Calculadora",
        "ai_kviz": "✨ Crear cuestionario con IA",
        "povijest": "📚 Historial",
        "pocetna": "← Inicio",
        "jezik": "🌍 Idioma"
    },

    "it": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Il tuo centro personale per lo studio",
        "sto_raditi": "Cosa vuoi fare?",
        "ai": "🤖 Assistente IA",
        "kvizovi": "🧠 Quiz",
        "biljeske": "📝 Note",
        "kalkulator": "🧮 Calcolatrice",
        "ai_kviz": "✨ Crea un quiz con l'IA",
        "povijest": "📚 Cronologia",
        "pocetna": "← Home",
        "jezik": "🌍 Lingua"
    },

    "pt": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "O teu centro pessoal de aprendizagem",
        "sto_raditi": "O que queres fazer?",
        "ai": "🤖 Assistente de IA",
        "kvizovi": "🧠 Questionários",
        "biljeske": "📝 Notas",
        "kalkulator": "🧮 Calculadora",
        "ai_kviz": "✨ Criar questionário com IA",
        "povijest": "📚 Histórico",
        "pocetna": "← Início",
        "jezik": "🌍 Idioma"
    },

    "ja": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "あなたの学習センター",
        "sto_raditi": "何をしますか？",
        "ai": "🤖 AIアシスタント",
        "kvizovi": "🧠 クイズ",
        "biljeske": "📝 ノート",
        "kalkulator": "🧮 電卓",
        "ai_kviz": "✨ AIでクイズを作成",
        "povijest": "📚 履歴",
        "pocetna": "← ホーム",
        "jezik": "🌍 言語"
    },

    "zh": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "你的个人学习中心",
        "sto_raditi": "你想做什么？",
        "ai": "🤖 AI 助手",
        "kvizovi": "🧠 测验",
        "biljeske": "📝 笔记",
        "kalkulator": "🧮 计算器",
        "ai_kviz": "✨ 使用 AI 创建测验",
        "povijest": "📚 历史记录",
        "pocetna": "← 首页",
        "jezik": "🌍 语言"
    },

    "ko": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "나만의 학습 센터",
        "sto_raditi": "무엇을 하시겠어요?",
        "ai": "🤖 AI 도우미",
        "kvizovi": "🧠 퀴즈",
        "biljeske": "📝 노트",
        "kalkulator": "🧮 계산기",
        "ai_kviz": "✨ AI로 퀴즈 만들기",
        "povijest": "📚 기록",
        "pocetna": "← 홈",
        "jezik": "🌍 언어"
    },

    "ru": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Твой личный учебный центр",
        "sto_raditi": "Что ты хочешь сделать?",
        "ai": "🤖 ИИ-помощник",
        "kvizovi": "🧠 Викторины",
        "biljeske": "📝 Заметки",
        "kalkulator": "🧮 Калькулятор",
        "ai_kviz": "✨ Создать викторину с ИИ",
        "povijest": "📚 История",
        "pocetna": "← Главная",
        "jezik": "🌍 Язык"
    },

    "ar": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "مركزك الشخصي للتعلم",
        "sto_raditi": "ماذا تريد أن تفعل؟",
        "ai": "🤖 مساعد الذكاء الاصطناعي",
        "kvizovi": "🧠 الاختبارات",
        "biljeske": "📝 الملاحظات",
        "kalkulator": "🧮 الآلة الحاسبة",
        "ai_kviz": "✨ إنشاء اختبار باستخدام الذكاء الاصطناعي",
        "povijest": "📚 السجل",
        "pocetna": "← الصفحة الرئيسية",
        "jezik": "🌍 اللغة"
    },

    "tr": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Kişisel öğrenme merkeziniz",
        "sto_raditi": "Ne yapmak istiyorsun?",
        "ai": "🤖 Yapay Zeka Asistanı",
        "kvizovi": "🧠 Testler",
        "biljeske": "📝 Notlar",
        "kalkulator": "🧮 Hesap Makinesi",
        "ai_kviz": "✨ Yapay Zeka ile test oluştur",
        "povijest": "📚 Geçmiş",
        "pocetna": "← Ana Sayfa",
        "jezik": "🌍 Dil"
    },

    "pl": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Twoje osobiste centrum nauki",
        "sto_raditi": "Co chcesz zrobić?",
        "ai": "🤖 Asystent AI",
        "kvizovi": "🧠 Quizy",
        "biljeske": "📝 Notatki",
        "kalkulator": "🧮 Kalkulator",
        "ai_kviz": "✨ Utwórz quiz za pomocą AI",
        "povijest": "📚 Historia",
        "pocetna": "← Strona główna",
        "jezik": "🌍 Język"
    },

    "nl": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Jouw persoonlijke leercentrum",
        "sto_raditi": "Wat wil je doen?",
        "ai": "🤖 AI-assistent",
        "kvizovi": "🧠 Quizzen",
        "biljeske": "📝 Notities",
        "kalkulator": "🧮 Rekenmachine",
        "ai_kviz": "✨ Quiz maken met AI",
        "povijest": "📚 Geschiedenis",
        "pocetna": "← Home",
        "jezik": "🌍 Taal"
    },

    "sv": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Ditt personliga lärcenter",
        "sto_raditi": "Vad vill du göra?",
        "ai": "🤖 AI-assistent",
        "kvizovi": "🧠 Quiz",
        "biljeske": "📝 Anteckningar",
        "kalkulator": "🧮 Kalkylator",
        "ai_kviz": "✨ Skapa quiz med AI",
        "povijest": "📚 Historik",
        "pocetna": "← Hem",
        "jezik": "🌍 Språk"
    },

    "da": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Dit personlige læringscenter",
        "sto_raditi": "Hvad vil du gøre?",
        "ai": "🤖 AI-assistent",
        "kvizovi": "🧠 Quizzer",
        "biljeske": "📝 Noter",
        "kalkulator": "🧮 Lommeregner",
        "ai_kviz": "✨ Opret quiz med AI",
        "povijest": "📚 Historik",
        "pocetna": "← Hjem",
        "jezik": "🌍 Sprog"
    },

    "no": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Ditt personlige læringssenter",
        "sto_raditi": "Hva vil du gjøre?",
        "ai": "🤖 AI-assistent",
        "kvizovi": "🧠 Quiz",
        "biljeske": "📝 Notater",
        "kalkulator": "🧮 Kalkulator",
        "ai_kviz": "✨ Lag quiz med AI",
        "povijest": "📚 Historikk",
        "pocetna": "← Hjem",
        "jezik": "🌍 Språk"
    },

    "fi": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Henkilökohtainen oppimiskeskuksesi",
        "sto_raditi": "Mitä haluat tehdä?",
        "ai": "🤖 Tekoälyavustaja",
        "kvizovi": "🧠 Tietovisat",
        "biljeske": "📝 Muistiinpanot",
        "kalkulator": "🧮 Laskin",
        "ai_kviz": "✨ Luo tietovisa tekoälyllä",
        "povijest": "📚 Historia",
        "pocetna": "← Etusivu",
        "jezik": "🌍 Kieli"
    },

    "cs": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Tvé osobní centrum pro učení",
        "sto_raditi": "Co chceš dělat?",
        "ai": "🤖 AI asistent",
        "kvizovi": "🧠 Kvízy",
        "biljeske": "📝 Poznámky",
        "kalkulator": "🧮 Kalkulačka",
        "ai_kviz": "✨ Vytvořit kvíz pomocí AI",
        "povijest": "📚 Historie",
        "pocetna": "← Domů",
        "jezik": "🌍 Jazyk"
    },

    "sk": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Tvoje osobné centrum učenia",
        "sto_raditi": "Čo chceš robiť?",
        "ai": "🤖 AI asistent",
        "kvizovi": "🧠 Kvízy",
        "biljeske": "📝 Poznámky",
        "kalkulator": "🧮 Kalkulačka",
        "ai_kviz": "✨ Vytvoriť kvíz pomocou AI",
        "povijest": "📚 História",
        "pocetna": "← Domov",
        "jezik": "🌍 Jazyk"
    },

    "hu": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Személyes tanulási központod",
        "sto_raditi": "Mit szeretnél csinálni?",
        "ai": "🤖 AI-asszisztens",
        "kvizovi": "🧠 Kvízek",
        "biljeske": "📝 Jegyzetek",
        "kalkulator": "🧮 Számológép",
        "ai_kviz": "✨ Kvíz készítése AI-val",
        "povijest": "📚 Előzmények",
        "pocetna": "← Kezdőlap",
        "jezik": "🌍 Nyelv"
    },

    "ro": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Centrul tău personal de învățare",
        "sto_raditi": "Ce vrei să faci?",
        "ai": "🤖 Asistent AI",
        "kvizovi": "🧠 Chestionare",
        "biljeske": "📝 Notițe",
        "kalkulator": "🧮 Calculator",
        "ai_kviz": "✨ Creează un chestionar cu AI",
        "povijest": "📚 Istoric",
        "pocetna": "← Acasă",
        "jezik": "🌍 Limbă"
    },

    "uk": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Твій особистий навчальний центр",
        "sto_raditi": "Що ти хочеш зробити?",
        "ai": "🤖 AI-помічник",
        "kvizovi": "🧠 Тести",
        "biljeske": "📝 Нотатки",
        "kalkulator": "🧮 Калькулятор",
        "ai_kviz": "✨ Створити тест за допомогою AI",
        "povijest": "📚 Історія",
        "pocetna": "← Головна",
        "jezik": "🌍 Мова"
    },

    "el": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Το προσωπικό σου κέντρο μάθησης",
        "sto_raditi": "Τι θέλεις να κάνεις?",
        "ai": "🤖 Βοηθός AI",
        "kvizovi": "🧠 Κουίζ",
        "biljeske": "📝 Σημειώσεις",
        "kalkulator": "🧮 Αριθμομηχανή",
        "ai_kviz": "✨ Δημιουργία κουίζ με AI",
        "povijest": "📚 Ιστορικό",
        "pocetna": "← Αρχική",
        "jezik": "🌍 Γλώσσα"
    },

    "he": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "מרכז הלמידה האישי שלך",
        "sto_raditi": "מה תרצה לעשות?",
        "ai": "🤖 עוזר AI",
        "kvizovi": "🧠 חידונים",
        "biljeske": "📝 הערות",
        "kalkulator": "🧮 מחשבון",
        "ai_kviz": "✨ צור חידון באמצעות AI",
        "povijest": "📚 היסטוריה",
        "pocetna": "← דף הבית",
        "jezik": "🌍 שפה"
    },

    "hi": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "आपका व्यक्तिगत अध्ययन केंद्र",
        "sto_raditi": "आप क्या करना चाहते हैं?",
        "ai": "🤖 AI सहायक",
        "kvizovi": "🧠 क्विज़",
        "biljeske": "📝 नोट्स",
        "kalkulator": "🧮 कैलकुलेटर",
        "ai_kviz": "✨ AI से क्विज़ बनाएं",
        "povijest": "📚 इतिहास",
        "pocetna": "← होम",
        "jezik": "🌍 भाषा"
    },

    "vi": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Trung tâm học tập cá nhân của bạn",
        "sto_raditi": "Bạn muốn làm gì?",
        "ai": "🤖 Trợ lý AI",
        "kvizovi": "🧠 Câu đố",
        "biljeske": "📝 Ghi chú",
        "kalkulator": "🧮 Máy tính",
        "ai_kviz": "✨ Tạo câu đố bằng AI",
        "povijest": "📚 Lịch sử",
        "pocetna": "← Trang chủ",
        "jezik": "🌍 Ngôn ngữ"
    },

    "id": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Pusat belajar pribadi Anda",
        "sto_raditi": "Apa yang ingin kamu lakukan?",
        "ai": "🤖 Asisten AI",
        "kvizovi": "🧠 Kuis",
        "biljeske": "📝 Catatan",
        "kalkulator": "🧮 Kalkulator",
        "ai_kviz": "✨ Buat kuis dengan AI",
        "povijest": "📚 Riwayat",
        "pocetna": "← Beranda",
        "jezik": "🌍 Bahasa"
    },

    "th": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "ศูนย์การเรียนรู้ส่วนตัวของคุณ",
        "sto_raditi": "คุณต้องการทำอะไร?",
        "ai": "🤖 ผู้ช่วย AI",
        "kvizovi": "🧠 แบบทดสอบ",
        "biljeske": "📝 บันทึก",
        "kalkulator": "🧮 เครื่องคิดเลข",
        "ai_kviz": "✨ สร้างแบบทดสอบด้วย AI",
        "povijest": "📚 ประวัติ",
        "pocetna": "← หน้าหลัก",
        "jezik": "🌍 ภาษา"
    },

    "bn": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "আপনার ব্যক্তিগত শেখার কেন্দ্র",
        "sto_raditi": "আপনি কী করতে চান?",
        "ai": "🤖 AI সহকারী",
        "kvizovi": "🧠 কুইজ",
        "biljeske": "📝 নোট",
        "kalkulator": "🧮 ক্যালকুলেটর",
        "ai_kviz": "✨ AI দিয়ে কুইজ তৈরি করুন",
        "povijest": "📚 ইতিহাস",
        "pocetna": "← হোম",
        "jezik": "🌍 ভাষা"
    },

    "fil": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Ang iyong personal na learning center",
        "sto_raditi": "Ano ang gusto mong gawin?",
        "ai": "🤖 AI Assistant",
        "kvizovi": "🧠 Mga Quiz",
        "biljeske": "📝 Mga Tala",
        "kalkulator": "🧮 Calculator",
        "ai_kviz": "✨ Gumawa ng quiz gamit ang AI",
        "povijest": "📚 Kasaysayan",
        "pocetna": "← Home",
        "jezik": "🌍 Wika"
    },

    "ms": {
        "naslov": "🎓 StudyMate",
        "podnaslov": "Pusat pembelajaran peribadi anda",
        "sto_raditi": "Apa yang anda mahu lakukan?",
        "ai": "🤖 Pembantu AI",
        "kvizovi": "🧠 Kuiz",
        "biljeske": "📝 Nota",
        "kalkulator": "🧮 Kalkulator",
        "ai_kviz": "✨ Cipta kuiz dengan AI",
        "povijest": "📚 Sejarah",
        "pocetna": "← Laman Utama",
        "jezik": "🌍 Bahasa"
    }
}


# ==================================================
# DOPUNA PRIJEVODA
# ==================================================

SVE_TIPKE = [
    "naslov",
    "podnaslov",
    "sto_raditi",
    "ai",
    "kvizovi",
    "biljeske",
    "kalkulator",
    "ai_kviz",
    "povijest",
    "pocetna",
    "jezik",
    "dodaj_pitanje",
    "pitanje",
    "odgovor",
    "tocan_odgovor",
    "spremi_pitanje",
    "pitanje_spremljeno",
    "ispuni_pitanje",
    "rijesi_kviz",
    "odaberi_odgovor",
    "zavrsi_kviz",
    "rezultat",
    "nema_pitanja",
    "upravljanje_pitanjima",
    "obrisi",
    "pitanje_obrisano",
    "nema_pitanja_brisanje",
    "dodaj_biljesku",
    "naslov_biljeske",
    "sadrzaj_biljeske",
    "pin_zakljucavanje",
    "zakljucaj_biljesku",
    "spremi_biljesku",
    "pin_obavezan",
    "biljeska_spremljena",
    "ispuni_biljesku",
    "moje_biljeske",
    "unesi_pin",
    "otkljucaj",
    "pogresan_pin",
    "kalkulator_naslov",
    "upisi_zadatak",
    "slikaj_zadatak",
    "rijesi_zadatak",
    "rjesavam_zadatak",
    "kalkulator_nedostupan",
    "citam_sliku",
    "slika_greska",
    "unesi_ili_slikaj",
    "tema_kviza",
    "broj_pitanja",
    "generiraj_kviz",
    "generira_pitanja",
    "generirano_pitanja",
    "pitanja",
    "neispravan_popis",
    "neispravan_format",
    "ai_nedostupan",
    "unesi_temu",
    "povijest_naslov",
    "tip_zapis",
    "pitanje_povijest",
    "odgovor_povijest",
    "obrisi_cijelu_povijest",
    "povijest_obrisana",
    "nema_povijesti"
]


for kod_jezika in PRIJEVODI:

    for tipka in SVE_TIPKE:

        if tipka not in PRIJEVODI[kod_jezika]:

            PRIJEVODI[kod_jezika][tipka] = PRIJEVODI["hr"].get(
                tipka,
                tipka
            )


# ==================================================
# 🌍 ODABIR JEZIKA
# ==================================================

jezik_lijevo, jezik_desno = st.columns([8, 2])

with jezik_desno:

    trenutni_index = list(JEZICI.values()).index(
        st.session_state.jezik
    )

    odabrani_jezik = st.selectbox(
        "🌍",
        list(JEZICI.keys()),
        index=trenutni_index,
        label_visibility="collapsed",
        key="odabir_jezika"
    )

st.session_state.jezik = JEZICI[odabrani_jezik]


# ==================================================
# JEZIK AI ODGOVORA
# ==================================================

JEZIK_AI = {
    "hr": "standardnom hrvatskom jeziku",
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "ja": "日本語",
    "zh": "中文",
    "ko": "한국어",
    "ru": "Русский",
    "ar": "العربية",
    "tr": "Türkçe",
    "pl": "Polski",
    "nl": "Nederlands",
    "sv": "Svenska",
    "da": "Dansk",
    "no": "Norsk",
    "fi": "Suomi",
    "cs": "Čeština",
    "sk": "Slovenčina",
    "hu": "Magyar",
    "ro": "Română",
    "uk": "Українська",
    "el": "Ελληνικά",
    "he": "עברית",
    "hi": "हिन्दी",
    "vi": "Tiếng Việt",
    "id": "Bahasa Indonesia",
    "th": "ไทย",
    "bn": "বাংলা",
    "fil": "Filipino",
    "ms": "Bahasa Melayu"
}

JEZIK_ODGOVORA = JEZIK_AI.get(
    st.session_state.jezik,
    "standardnom hrvatskom jeziku"
)

T = PRIJEVODI.get(
    st.session_state.jezik,
    PRIJEVODI["hr"]
)


# ==================================================
# SESSION STATE
# ==================================================

if "prikazi_ai" not in st.session_state:
    st.session_state.prikazi_ai = False

if "prikazi_kviz" not in st.session_state:
    st.session_state.prikazi_kviz = False

if "prikazi_biljeske" not in st.session_state:
    st.session_state.prikazi_biljeske = False

if "prikazi_kalkulator" not in st.session_state:
    st.session_state.prikazi_kalkulator = False

if "prikazi_povijest" not in st.session_state:
    st.session_state.prikazi_povijest = False

if "prikazi_ai_kviz" not in st.session_state:
    st.session_state.prikazi_ai_kviz = False

if "kvizovi" not in st.session_state:
    st.session_state.kvizovi = []

if "povijest" not in st.session_state:
    st.session_state.povijest = []

if "biljeske" not in st.session_state:
    st.session_state.biljeske = []


# ==================================================
# UČITAJ POVIJEST
# ==================================================

if os.path.exists("povijest.json") and not st.session_state.povijest:

    try:

        with open(
            "povijest.json",
            "r",
            encoding="utf-8"
        ) as file:

            podaci = json.load(file)

        if isinstance(podaci, list):
            st.session_state.povijest = podaci

    except Exception:

        st.session_state.povijest = []


# ==================================================
# UČITAJ KVIZOVE
# ==================================================

if os.path.exists("kvizovi.json") and not st.session_state.kvizovi:

    try:

        with open(
            "kvizovi.json",
            "r",
            encoding="utf-8"
        ) as file:

            podaci = json.load(file)

        if isinstance(podaci, list):

            st.session_state.kvizovi = [
                kviz
                for kviz in podaci
                if isinstance(kviz, dict)
                and "pitanje" in kviz
                and "odgovori" in kviz
                and "tocni_odgovor" in kviz
            ]

    except Exception:

        st.session_state.kvizovi = []


# ==================================================
# PROVJERA JE LI NEKA STRANICA OTVORENA
# ==================================================

stranica_otvorena = (
    st.session_state.prikazi_ai
    or st.session_state.prikazi_kviz
    or st.session_state.prikazi_biljeske
    or st.session_state.prikazi_kalkulator
    or st.session_state.prikazi_povijest
    or st.session_state.prikazi_ai_kviz
)


# ==================================================
# NASLOV GLAVNE STRANICE
# ==================================================

if not stranica_otvorena:

    st.title(T["naslov"])
    st.subheader(T["podnaslov"])


# ==================================================
# GLAVNI IZBORNIK
# ==================================================

if not stranica_otvorena:

    st.divider()

    st.header(T["sto_raditi"])


    # ----------------------------------------------
    # AI POMOĆNIK
    # ----------------------------------------------

    if st.button(
        T["ai"],
        use_container_width=True,
        key="glavni_ai"
    ):

        st.session_state.prikazi_ai = True
        st.session_state.prikazi_kviz = False
        st.session_state.prikazi_biljeske = False
        st.session_state.prikazi_kalkulator = False
        st.session_state.prikazi_povijest = False
        st.session_state.prikazi_ai_kviz = False

        st.rerun()


    # ----------------------------------------------
    # KVIZOVI
    # ----------------------------------------------

    if st.button(
        T["kvizovi"],
        use_container_width=True,
        key="glavni_kvizovi"
    ):

        st.session_state.prikazi_ai = False
        st.session_state.prikazi_kviz = True
        st.session_state.prikazi_biljeske = False
        st.session_state.prikazi_kalkulator = False
        st.session_state.prikazi_povijest = False
        st.session_state.prikazi_ai_kviz = False

        st.rerun()


    # ----------------------------------------------
    # BILJEŠKE
    # ----------------------------------------------

    if st.button(
        T["biljeske"],
        use_container_width=True,
        key="glavni_biljeske"
    ):

        st.session_state.prikazi_ai = False
        st.session_state.prikazi_kviz = False
        st.session_state.prikazi_biljeske = True
        st.session_state.prikazi_kalkulator = False
        st.session_state.prikazi_povijest = False
        st.session_state.prikazi_ai_kviz = False

        st.rerun()


    # ----------------------------------------------
    # KALKULATOR
    # ----------------------------------------------

    if st.button(
        T["kalkulator"],
        use_container_width=True,
        key="glavni_kalkulator"
    ):

        st.session_state.prikazi_ai = False
        st.session_state.prikazi_kviz = False
        st.session_state.prikazi_biljeske = False
        st.session_state.prikazi_kalkulator = True
        st.session_state.prikazi_povijest = False
        st.session_state.prikazi_ai_kviz = False

        st.rerun()


    # ----------------------------------------------
    # AI KVIZ
    # ----------------------------------------------

    if st.button(
        T["ai_kviz"],
        use_container_width=True,
        key="glavni_ai_kviz"
    ):

        st.session_state.prikazi_ai = False
        st.session_state.prikazi_kviz = False
        st.session_state.prikazi_biljeske = False
        st.session_state.prikazi_kalkulator = False
        st.session_state.prikazi_povijest = False
        st.session_state.prikazi_ai_kviz = True

        st.rerun()


    # ----------------------------------------------
    # POVIJEST
    # ----------------------------------------------

    if st.button(
        T["povijest"],
        use_container_width=True,
        key="glavni_povijest"
    ):

        st.session_state.prikazi_ai = False
        st.session_state.prikazi_kviz = False
        st.session_state.prikazi_biljeske = False
        st.session_state.prikazi_kalkulator = False
        st.session_state.prikazi_povijest = True
        st.session_state.prikazi_ai_kviz = False

        st.rerun()


# ==================================================
# 🤖 AI POMOĆNIK
# ==================================================

if st.session_state.prikazi_ai:

    # ----------------------------------------------
    # STRELICA
    # ----------------------------------------------

    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            font-size: 28px;
            padding: 0px;
            margin: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "←",
        key="pocetna_ai",
        type="tertiary"
    ):

        st.session_state.prikazi_ai = False
        st.rerun()


    st.divider()

    st.header("🤖 AI pomoćnik")


    # ----------------------------------------------
    # CHAT STATE
    # ----------------------------------------------

    if "ai_chat" not in st.session_state:
        st.session_state.ai_chat = []


    # ----------------------------------------------
    # PRIKAŽI DOSADAŠNJI RAZGOVOR
    # ----------------------------------------------

    for poruka_chat in st.session_state.ai_chat:

        if poruka_chat.get("uloga") == "user":

            with st.chat_message("user"):

                if poruka_chat.get("slika"):

                    st.image(
                        poruka_chat["slika"],
                        width=400
                    )

                if poruka_chat.get("datoteka"):

                    st.write(
                        "📎 " + poruka_chat["datoteka"]
                    )

                if poruka_chat.get("tekst"):

                    st.write(
                        poruka_chat["tekst"]
                    )


        elif poruka_chat.get("uloga") == "assistant":

            with st.chat_message("assistant"):

                st.write(
                    poruka_chat["tekst"]
                )


    # ----------------------------------------------
    # CHAT INPUT
    # ----------------------------------------------

    poruka = st.chat_input(
        "Napiši pitanje...",
        key="ai_chat_input",
        accept_file=True,
        file_type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "pdf",
            "mp4",
            "mov",
            "avi",
            "mkv",
            "webm"
        ]
    )


    # ----------------------------------------------
    # AKO JE POSLANA PORUKA
    # ----------------------------------------------

    if poruka:

        pitanje_ai = poruka.text
        datoteke = poruka.files

        slika = None
        pdf = None
        video = None


        # ------------------------------------------
        # PREPOZNAJ PRIVITAK
        # ------------------------------------------

        if datoteke:

            datoteka = datoteke[0]

            if datoteka.name.lower().endswith(".pdf"):

                pdf = datoteka

            elif datoteka.name.lower().endswith(
                (
                    ".mp4",
                    ".mov",
                    ".avi",
                    ".mkv",
                    ".webm"
                )
            ):

                video = datoteka

            else:

                slika = datoteka


        # ------------------------------------------
        # PRIKAŽI KORISNIKOVU PORUKU
        # ------------------------------------------

        with st.chat_message("user"):

            if slika:

                st.image(
                    slika,
                    width=400
                )

            if pdf:

                st.write(
                    "📄 " + pdf.name
                )

            if video:

                st.write(
                    "🎥 " + video.name
                )

            if pitanje_ai:

                st.write(
                    pitanje_ai
                )


        # ------------------------------------------
        # SPREMI PORUKU
        # ------------------------------------------

        st.session_state.ai_chat.append({
            "uloga": "user",
            "tekst": pitanje_ai,
            "slika": (
                slika.getvalue()
                if slika
                else None
            ),
            "datoteka": (
                pdf.name
                if pdf
                else (
                    video.name
                    if video
                    else None
                )
            )
        })


        # ------------------------------------------
        # AI
        # ------------------------------------------

        try:

            # --------------------------------------
            # SLIKA
            # --------------------------------------

            if slika:

                slika_base64 = base64.b64encode(
                    slika.getvalue()
                ).decode("utf-8")

                odgovor = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "gemma3:4b",
                        "prompt": (
                            "Ti si StudyMate, školski AI pomoćnik. "
                            f"Odgovaraj isključivo na jeziku: "
                            f"{JEZIK_ODGOVORA}. "

                            "Pažljivo pogledaj poslanu sliku. "
                            "Pročitaj sve što se nalazi na slici. "

                            "Ako je na slici matematički zadatak, "
                            "riješi ga korak po korak i provjeri rezultat. "

                            "Ako je na slici tekst, objasni ga učeniku. "

                            "Odgovori upravo na pitanje učenika. "

                            "Nemoj izmišljati činjenice. "

                            "Ako nisi siguran, jasno reci da nisi siguran. "

                            "Piši jednostavno i jasno.\n\n"

                            f"Pitanje učenika: {pitanje_ai}"
                        ),
                        "images": [
                            slika_base64
                        ],
                        "stream": False
                    },
                    timeout=180
                )


            # --------------------------------------
            # PDF
            # --------------------------------------

            elif pdf:

                pdf_reader = PdfReader(pdf)

                pdf_tekst = ""

                for stranica in pdf_reader.pages:

                    tekst_stranice = (
                        stranica.extract_text()
                        or ""
                    )

                    pdf_tekst += (
                        tekst_stranice
                        + "\n"
                    )

                pdf_tekst = pdf_tekst[:50000]

                odgovor = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen3:8b",
                        "prompt": (
                            "Ti si StudyMate, školski AI pomoćnik. "
                            f"Odgovaraj isključivo na jeziku: "
                            f"{JEZIK_ODGOVORA}. "

                            "Pažljivo pročitaj sadržaj PDF-a. "

                            "Ako PDF sadrži pitanja, pronađi ih. "

                            "Ako učenik traži odgovore, "
                            "odgovori redom. "

                            "Numeriraj odgovore istim redoslijedom. "

                            "Nemoj izmišljati činjenice. "

                            "Ako nisi siguran, jasno reci da nisi siguran.\n\n"

                            f"Pitanje učenika: {pitanje_ai}\n\n"

                            "SADRŽAJ PDF-a:\n"
                            f"{pdf_tekst}"
                        ),
                        "stream": False
                    },
                    timeout=180
                )


            # --------------------------------------
            # VIDEO
            # --------------------------------------

            elif video:

                privremena_datoteka = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp4"
                )

                privremena_datoteka.write(
                    video.getvalue()
                )

                privremena_datoteka.close()

                video_capture = cv2.VideoCapture(
                    privremena_datoteka.name
                )

                ukupno_frameova = int(
                    video_capture.get(
                        cv2.CAP_PROP_FRAME_COUNT
                    )
                )

                fps = video_capture.get(
                    cv2.CAP_PROP_FPS
                )

                if fps <= 0:
                    fps = 25

                trajanje = (
                    ukupno_frameova / fps
                    if ukupno_frameova > 0
                    else 0
                )

                broj_frameova = min(
                    6,
                    max(
                        1,
                        ukupno_frameova
                    )
                )

                slike_videa = []

                for i in range(
                    broj_frameova
                ):

                    if broj_frameova == 1:

                        pozicija = 0

                    else:

                        pozicija = int(
                            (
                                i / (broj_frameova - 1)
                            )
                            * (
                                ukupno_frameova - 1
                            )
                        )

                    video_capture.set(
                        cv2.CAP_PROP_POS_FRAMES,
                        pozicija
                    )

                    uspjeh, frame = (
                        video_capture.read()
                    )

                    if uspjeh:

                        uspjeh_jpg, buffer = (
                            cv2.imencode(
                                ".jpg",
                                frame
                            )
                        )

                        if uspjeh_jpg:

                            slike_videa.append(
                                base64.b64encode(
                                    buffer
                                ).decode("utf-8")
                            )

                video_capture.release()

                try:

                    os.remove(
                        privremena_datoteka.name
                    )

                except Exception:

                    pass

                odgovor = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "gemma3:4b",
                        "prompt": (
                            "Ti si StudyMate, školski AI pomoćnik. "
                            f"Odgovaraj isključivo na jeziku: "
                            f"{JEZIK_ODGOVORA}. "

                            "Analiziraj slike uzete iz poslanog videa. "

                            f"Video traje približno {trajanje:.1f} sekundi. "

                            "Pokušaj razumjeti što se događa u videu "
                            "na temelju prikazanih kadrova. "

                            "Odgovori upravo na pitanje učenika. "

                            "Nemoj izmišljati ono što se ne vidi. "

                            "Ako se odgovor ne može utvrditi, "
                            "jasno reci da nisi siguran.\n\n"

                            f"Pitanje učenika: {pitanje_ai}"
                        ),
                        "images": slike_videa,
                        "stream": False
                    },
                    timeout=180
                )


            # --------------------------------------
            # BEZ PRIVITKA
            # --------------------------------------

            else:

                razgovor = ""

                for poruka_chat in st.session_state.ai_chat:

                    if poruka_chat.get("uloga") == "user":

                        razgovor += (
                            "Učenik: "
                            + poruka_chat.get(
                                "tekst",
                                ""
                            )
                            + "\n"
                        )

                    elif poruka_chat.get("uloga") == "assistant":

                        razgovor += (
                            "StudyMate: "
                            + poruka_chat.get(
                                "tekst",
                                ""
                            )
                            + "\n"
                        )

                odgovor = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen3:8b",
                        "prompt": (
                            "Ti si StudyMate, školski AI pomoćnik. "

                            f"Odgovaraj isključivo na jeziku: "
                            f"{JEZIK_ODGOVORA}. "

                            "Jako je važno da koristiš cijeli "
                            "prethodni razgovor. "

                            "Moraš pamtiti informacije koje je "
                            "učenik ranije napisao u ovom razgovoru. "

                            "Ako je učenik ranije rekao svoje ime, "
                            "zapamti ga i koristi ga kada te pita "
                            "kako se zove. "

                            "Odgovori upravo na zadnje pitanje učenika. "

                            "Nemoj ponovno samo pozdravljati učenika "
                            "ako je postavio konkretno pitanje. "

                            "Nemoj izmišljati činjenice. "

                            "Ako nisi siguran, jasno reci da nisi siguran. "

                            "Kod matematike koristi točne formule "
                            "i pokaži postupak. "

                            "Kod fizike koristi izraz "
                            "'jednoliko pravocrtno gibanje'. "

                            "Piši prirodnim i jasnim jezikom.\n\n"

                            "PRETHODNI RAZGOVOR:\n"
                            + razgovor
                            + "\n\n"

                            "Sada odgovori na zadnju poruku učenika."
                        ),
                        "stream": False
                    },
                    timeout=180
                )


            # --------------------------------------
            # ODGOVOR AI-a
            # --------------------------------------

            if odgovor.status_code == 200:

                tekst = odgovor.json().get(
                    "response",
                    ""
                )

                if not tekst:

                    tekst = "AI nije vratio odgovor."

                with st.chat_message("assistant"):

                    st.write(
                        tekst
                    )

                st.session_state.ai_chat.append({
                    "uloga": "assistant",
                    "tekst": tekst,
                    "slika": None,
                    "datoteka": None
                })


                st.session_state.povijest.append({
                    "tip": "🤖 AI pomoćnik",
                    "pitanje": pitanje_ai,
                    "odgovor": tekst,
                    "vrijeme": datetime.now().strftime(
                        "%d.%m.%Y. %H:%M"
                    )
                })


                with open(
                    "povijest.json",
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        st.session_state.povijest,
                        file,
                        ensure_ascii=False,
                        indent=4
                    )

            else:

                st.error(
                    "❌ AI trenutno nije dostupan."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Ollama nije pokrenuta. Pokreni Ollamu pa pokušaj ponovno."
            )

        except Exception as e:

            st.error(
                f"❌ Greška pri povezivanju s AI-em: {e}"
            )


# ==================================================
# 🧠 KVIZOVI
# ==================================================

if st.session_state.prikazi_kviz:

    if st.button(
        T["pocetna"],
        key="pocetna_kviz"
    ):

        st.session_state.prikazi_kviz = False
        st.rerun()


    st.divider()

    st.header(T["kvizovi"])


    # ----------------------------------------------
    # DODAJ PITANJE
    # ----------------------------------------------

    st.subheader(
        T["dodaj_pitanje"]
    )

    pitanje = st.text_input(
        T["pitanje"],
        key="novo_pitanje"
    )

    odgovor1 = st.text_input(
        f"{T['odgovor']} 1",
        key="odg1"
    )

    odgovor2 = st.text_input(
        f"{T['odgovor']} 2",
        key="odg2"
    )

    odgovor3 = st.text_input(
        f"{T['odgovor']} 3",
        key="odg3"
    )

    odgovor4 = st.text_input(
        f"{T['odgovor']} 4",
        key="odg4"
    )

    tocni_odgovor = st.selectbox(
        T["tocan_odgovor"],
        [
            odgovor1,
            odgovor2,
            odgovor3,
            odgovor4
        ],
        key="tocni"
    )


    if st.button(
        T["spremi_pitanje"],
        key="spremi_pitanje"
    ):

        if pitanje and all([
            odgovor1,
            odgovor2,
            odgovor3,
            odgovor4
        ]):

            st.session_state.kvizovi.append({
                "pitanje": pitanje,
                "odgovori": [
                    odgovor1,
                    odgovor2,
                    odgovor3,
                    odgovor4
                ],
                "tocni_odgovor": tocni_odgovor
            })

            with open(
                "kvizovi.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    st.session_state.kvizovi,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            st.success(
                T["pitanje_spremljeno"]
            )

        else:

            st.warning(
                T["ispuni_pitanje"]
            )


    st.divider()


    # ----------------------------------------------
    # RIJEŠI KVIZ
    # ----------------------------------------------

    st.subheader(
        T["rijesi_kviz"]
    )

    if st.session_state.kvizovi:

        odgovori_korisnika = []

        for i, kviz in enumerate(
            st.session_state.kvizovi
        ):

            st.write(
                f"**{i + 1}. {kviz['pitanje']}**"
            )

            odgovor = st.radio(
                T["odaberi_odgovor"],
                kviz["odgovori"],
                key=f"odgovor_{i}"
            )

            odgovori_korisnika.append(
                odgovor
            )


        if st.button(
            T["zavrsi_kviz"],
            key="zavrsi_kviz"
        ):

            rezultat = 0

            for i, kviz in enumerate(
                st.session_state.kvizovi
            ):

                if (
                    odgovori_korisnika[i]
                    == kviz["tocni_odgovor"]
                ):

                    rezultat += 1


            ukupno = len(
                st.session_state.kvizovi
            )

            postotak = int(
                (rezultat / ukupno) * 100
            )

            st.success(
                f"{T['rezultat']}: "
                f"{rezultat}/{ukupno} "
                f"({postotak}%)"
            )

    else:

        st.info(
            T["nema_pitanja"]
        )


    st.divider()


    # ----------------------------------------------
    # UPRAVLJANJE PITANJIMA
    # ----------------------------------------------

    st.subheader(
        T["upravljanje_pitanjima"]
    )

    if st.session_state.kvizovi:

        for i, kviz in enumerate(
            st.session_state.kvizovi
        ):

            st.write(
                f"{i + 1}. {kviz['pitanje']}"
            )

            if st.button(
                T["obrisi"],
                key=f"obrisi_{i}"
            ):

                st.session_state.kvizovi.pop(i)

                with open(
                    "kvizovi.json",
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        st.session_state.kvizovi,
                        file,
                        ensure_ascii=False,
                        indent=4
                    )

                st.success(
                    T["pitanje_obrisano"]
                )

                st.rerun()

    else:

        st.info(
            T["nema_pitanja_brisanje"]
        )


# ==================================================
# 📝 BILJEŠKE
# ==================================================

if st.session_state.prikazi_biljeske:

    if st.button(
        T["pocetna"],
        key="pocetna_biljeske"
    ):

        st.session_state.prikazi_biljeske = False
        st.rerun()


    st.divider()

    st.header(
        T["biljeske"]
    )

    FILE_NAME = "biljeske.json"


    # ----------------------------------------------
    # UČITAJ BILJEŠKE
    # ----------------------------------------------

    if os.path.exists(FILE_NAME):

        try:

            with open(
                FILE_NAME,
                "r",
                encoding="utf-8"
            ) as file:

                st.session_state.biljeske = json.load(
                    file
                )

        except Exception:

            st.session_state.biljeske = []

    else:

        st.session_state.biljeske = []


    # ----------------------------------------------
    # NOVA BILJEŠKA
    # ----------------------------------------------

    st.subheader(
        T["dodaj_biljesku"]
    )

    naslov = st.text_input(
        T["naslov_biljeske"],
        key="naslov_nove_biljeske"
    )

    sadrzaj = st.text_area(
        T["sadrzaj_biljeske"],
        key="sadrzaj_nove_biljeske"
    )

    pin = st.text_input(
        T["pin_zakljucavanje"],
        type="password",
        key="pin_nove_biljeske"
    )

    zakljucaj = st.checkbox(
        T["zakljucaj_biljesku"],
        key="zakljucaj_novu_biljesku"
    )


    if st.button(
        T["spremi_biljesku"],
        key="spremi_biljesku"
    ):

        if zakljucaj and not pin:

            st.warning(
                T["pin_obavezan"]
            )

        elif naslov and sadrzaj:

            pin_hash = ""

            if zakljucaj:

                pin_hash = bcrypt.hashpw(
                    pin.encode("utf-8"),
                    bcrypt.gensalt()
                ).decode("utf-8")


            st.session_state.biljeske.append({
                "naslov": naslov,
                "sadrzaj": sadrzaj,
                "pin": pin_hash,
                "zakljucana": zakljucaj
            })


            with open(
                FILE_NAME,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    st.session_state.biljeske,
                    file,
                    ensure_ascii=False,
                    indent=4
                )


            st.success(
                T["biljeska_spremljena"]
            )

        else:

            st.warning(
                T["ispuni_biljesku"]
            )


    st.divider()


    # ----------------------------------------------
    # MOJE BILJEŠKE
    # ----------------------------------------------

    st.subheader(
        T["moje_biljeske"]
    )


    for i, biljeska in enumerate(
        st.session_state.biljeske
    ):

        if biljeska.get("zakljucana"):

            st.write(
                f"🔒 **{biljeska.get('naslov', '')}**"
            )

            otkljucavanje = st.text_input(
                T["unesi_pin"],
                type="password",
                key=f"pin_{i}"
            )


            if st.button(
                T["otkljucaj"],
                key=f"unlock_{i}"
            ):

                try:

                    if bcrypt.checkpw(
                        otkljucavanje.encode("utf-8"),
                        biljeska["pin"].encode("utf-8")
                    ):

                        st.success(
                            biljeska.get(
                                "sadrzaj",
                                ""
                            )
                        )

                    else:

                        st.error(
                            T["pogresan_pin"]
                        )

                except Exception:

                    st.error(
                        T["pogresan_pin"]
                    )

        else:

            st.write(
                f"📄 **{biljeska.get('naslov', '')}**"
            )

            st.write(
                biljeska.get(
                    "sadrzaj",
                    ""
                )
            )

        st.divider()


# ==================================================
# 🧮 MATEMATIČKI KALKULATOR
# ==================================================

if st.session_state.prikazi_kalkulator:

    if st.button(
        T["pocetna"],
        key="pocetna_kalkulator"
    ):

        st.session_state.prikazi_kalkulator = False
        st.rerun()


    st.divider()

    st.header(
        T["kalkulator_naslov"]
    )


    lijevo, desno = st.columns(
        [3, 1]
    )


    with lijevo:

        matematicki_zadatak = st.text_area(
            T["upisi_zadatak"],
            placeholder="npr. 2x + 5 = 15",
            height=150,
            key="matematicki_zadatak"
        )


    with desno:

        st.write("📷")

        fotografija = st.camera_input(
            T["slikaj_zadatak"]
        )


    if st.button(
        T["rijesi_zadatak"],
        key="rijesi_matematiku"
    ):

        if matematicki_zadatak:

            st.info(
                T["rjesavam_zadatak"]
            )


            try:

                odgovor = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen3:8b",
                        "prompt": (
                            "Ti si matematički pomoćnik "
                            "u aplikaciji StudyMate. "

                            f"Odgovaraj isključivo na jeziku: "
                            f"{JEZIK_ODGOVORA}. "

                            "Rješavaj samo matematičke zadatke. "

                            "Uvijek provjeri matematičku točnost odgovora. "

                            "Prikaži cijeli postupak korak po korak. "

                            "Na kraju jasno napiši konačan odgovor. "

                            "Ako pitanje nije matematičko, reci da možeš "
                            "rješavati samo matematičke zadatke.\n\n"

                            f"Matematički zadatak: "
                            f"{matematicki_zadatak}"
                        ),
                        "stream": False
                    },
                    timeout=180
                )


                if odgovor.status_code == 200:

                    tekst = odgovor.json().get(
                        "response",
                        ""
                    )

                    st.success(
                        tekst
                    )

                else:

                    st.error(
                        T["kalkulator_nedostupan"]
                    )

            except Exception:

                st.error(
                    T["kalkulator_nedostupan"]
                )


        elif fotografija:

            st.info(
                T["citam_sliku"]
            )


            try:

                slika_base64 = base64.b64encode(
                    fotografija.getvalue()
                ).decode("utf-8")


                odgovor = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "gemma3:4b",
                        "prompt": (
                            "Ti si matematički pomoćnik "
                            "u aplikaciji StudyMate. "

                            f"Odgovaraj isključivo na jeziku: "
                            f"{JEZIK_ODGOVORA}. "

                            "Pogledaj sliku i utvrdi nalazi li se "
                            "na njoj matematički zadatak. "

                            "Ako nije matematički zadatak, jasno reci "
                            "da možeš rješavati samo matematičke zadatke. "

                            "Ako jest matematički zadatak, pažljivo "
                            "pročitaj sve brojeve, znakove, formule "
                            "i izraze. "

                            "Riješi zadatak potpuno točno. "

                            "Prikaži cijeli postupak korak po korak. "

                            "Nemoj preskakati važne korake. "

                            "Na kraju jasno napiši: KONAČNO RJEŠENJE. "

                            "Obavezno provjeri rezultat prije konačnog odgovora."
                        ),
                        "images": [
                            slika_base64
                        ],
                        "stream": False
                    },
                    timeout=180
                )


                if odgovor.status_code == 200:

                    tekst = odgovor.json().get(
                        "response",
                        ""
                    )

                    st.success(
                        tekst
                    )

                else:

                    st.error(
                        T["slika_greska"]
                    )

            except Exception:

                st.error(
                    T["slika_greska"]
                )


        else:

            st.warning(
                T["unesi_ili_slikaj"]
            )


# ==================================================
# 📚 POVIJEST
# ==================================================

if st.session_state.prikazi_povijest:

    if st.button(
        T["pocetna"],
        key="pocetna_povijest"
    ):

        st.session_state.prikazi_povijest = False
        st.rerun()


    st.divider()

    st.header(
        T["povijest_naslov"]
    )


    if st.session_state.povijest:

        for zapis in reversed(
            st.session_state.povijest
        ):

            st.subheader(
                f"{zapis.get('tip', T['tip_zapis'])} "
                f"— {zapis.get('vrijeme', '')}"
            )

            st.write(
                f"**{T['pitanje_povijest']}:** "
                f"{zapis.get('pitanje', '')}"
            )

            st.write(
                f"**{T['odgovor_povijest']}:** "
                f"{zapis.get('odgovor', '')}"
            )

            st.divider()


        if st.button(
            T["obrisi_cijelu_povijest"],
            key="obrisi_cijelu_povijest"
        ):

            st.session_state.povijest = []


            with open(
                "povijest.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    ensure_ascii=False,
                    indent=4
                )


            st.success(
                T["povijest_obrisana"]
            )

            st.rerun()

    else:

        st.info(
            T["nema_povijesti"]
        )


# ==================================================
# ✨ AI GENERATOR KVIZA
# ==================================================

if st.session_state.prikazi_ai_kviz:

    if st.button(
        T["pocetna"],
        key="pocetna_ai_kviz"
    ):

        st.session_state.prikazi_ai_kviz = False
        st.rerun()


    st.divider()

    st.header(
        T["ai_kviz"]
    )


    tema_kviza = st.text_input(
        T["tema_kviza"],
        placeholder="npr. 1. Newtonov zakon",
        key="tema_ai_kviza"
    )


    broj_pitanja = st.number_input(
        T["broj_pitanja"],
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        key="broj_ai_pitanja"
    )


    if st.button(
        T["generiraj_kviz"],
        key="generiraj_ai_kviz"
    ):

        if tema_kviza:

            st.info(
                T["generira_pitanja"]
            )


            try:

                odgovor = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen3:8b",
                        "prompt": (
                            "Ti si StudyMate i izrađuješ školski kviz. "

                            f"Odgovaraj isključivo na jeziku: "
                            f"{JEZIK_ODGOVORA}. "

                            "Napravi točno "
                            f"{broj_pitanja} pitanja na temu: "
                            f"{tema_kviza}. "

                            "Za svako pitanje napravi točno 4 "
                            "ponuđena odgovora. "

                            "Samo jedan odgovor smije biti točan. "

                            "VRATI ODGOVOR ISKLJUČIVO U OVOM JSON FORMATU: "

                            "["
                            "{"
                            "\"pitanje\": \"tekst pitanja\", "
                            "\"odgovori\": ["
                            "\"odgovor 1\", "
                            "\"odgovor 2\", "
                            "\"odgovor 3\", "
                            "\"odgovor 4\""
                            "], "
                            "\"tocni_odgovor\": \"točan odgovor\""
                            "}"
                            "] "

                            "Nemoj dodavati nikakav tekst prije "
                            "ili poslije JSON-a."
                        ),
                        "stream": False
                    },
                    timeout=180
                )


                if odgovor.status_code == 200:

                    tekst = odgovor.json().get(
                        "response",
                        ""
                    )


                    try:

                        nova_pitanja = json.loads(
                            tekst
                        )


                        if isinstance(
                            nova_pitanja,
                            list
                        ):

                            ispravna_pitanja = [
                                kviz
                                for kviz in nova_pitanja
                                if (
                                    isinstance(
                                        kviz,
                                        dict
                                    )
                                    and "pitanje" in kviz
                                    and "odgovori" in kviz
                                    and "tocni_odgovor" in kviz
                                    and isinstance(
                                        kviz["odgovori"],
                                        list
                                    )
                                    and len(
                                        kviz["odgovori"]
                                    ) == 4
                                )
                            ]


                            # Provjeri da je točan odgovor
                            # stvarno među ponuđenima

                            ispravna_pitanja = [
                                kviz
                                for kviz in ispravna_pitanja
                                if kviz["tocni_odgovor"]
                                in kviz["odgovori"]
                            ]


                            st.session_state.kvizovi.extend(
                                ispravna_pitanja
                            )


                            with open(
                                "kvizovi.json",
                                "w",
                                encoding="utf-8"
                            ) as file:

                                json.dump(
                                    st.session_state.kvizovi,
                                    file,
                                    ensure_ascii=False,
                                    indent=4
                                )


                            st.success(
                                f"{T['generirano_pitanja']} "
                                f"{len(ispravna_pitanja)} "
                                f"{T['pitanja']}"
                            )

                        else:

                            st.error(
                                T["neispravan_popis"]
                            )


                    except json.JSONDecodeError:

                        st.error(
                            T["neispravan_format"]
                        )

                else:

                    st.error(
                        T["ai_nedostupan"]
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Ollama nije pokrenuta."
                )

            except Exception as e:

                st.error(
                    f"❌ Greška: {e}"
                )

        else:

            st.warning(
                T["unesi_temu"]
            )


# ==================================================
# KRAJ - SAMO POČETNA STRANICA
# ==================================================

if not (
    st.session_state.prikazi_ai
    or st.session_state.prikazi_kviz
    or st.session_state.prikazi_biljeske
    or st.session_state.prikazi_kalkulator
    or st.session_state.prikazi_povijest
    or st.session_state.prikazi_ai_kviz
):

    st.divider()

    st.write(
        "💡 StudyMate ti pomaže organizirati "
        "učenje na jednom mjestu."
    )