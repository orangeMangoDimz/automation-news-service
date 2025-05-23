# Instruction
SUMMARIZE_INSTRUCTION = """
[Aturan]
- Ringkas artikel di atas menjadi point-point penting saja
- Langsung gunakan format di bawah ini
- Jangan tambahkan apapun di luar format di bawah

[Format]
- [Judul point]
    - [Isi point 1]
    - [Isi point 2]
    - [Isi point 3]
    dan seterusnya ...
"""

# Monday motivation
TODAY_WORD_CONTENT = "Berikan kata-kata untuk hari ini"
TODAY_WORD_INSTRUCTION = """
[Aturan]
- Berikan 1 kalimat saja
- Langsung berikan isi kalimatnya Isi kalimat harus bisa memberikan semangat dan motivasi
"""

# Date
LIST_OF_DAYS = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu",
}

LIST_OF_MONTHS = {
    "January": "Januari",
    "February": "Februari",
    "March": "Maret",
    "April": "April",
    "May": "Mei",
    "June": "Juni",
    "July": "Juli",
    "August": "Agustus",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Desember",
}

# Gemini
API_KEY_NOT_FOUND = "You need to insert Gemini API Key first!"
RESPONSE_NOT_FOUND = "No Response from AI"

# Response
No_NEWS_YET = "Belum ada berita untuk sekarang"

# Timeout
PAGE_LOAD_TIMEOUT = 5

# Pagination
PAGINATION_LINK_LIMIT = 2

# Other
DEBUG_MODE = "Your are not setitng debug status! It will set TRUE automaticly!"
ENV_NOT_COMPLETE = "ENV are not fully set! Please refer to the .env.example"

# Profile
AUTHOR_PROFILE = "https://github.com/orangeMangoDimz"
DISCORD_BOT_REPO = "https://github.com/orangeMangoDimz/mango-bot"
BACKEND_REPO = "https://github.com/orangeMangoDimz/automation-news-service"
TEMPLATE_PROFILE = f"""
### Profile
Hi, I'm mangoBot!
I'm still in beta version!
If you found any bug, please report to the owner!
### Basic Information
- **Author**: [orangeMangoDimz]({AUTHOR_PROFILE})
### Support
- Please give the repo star to support this bot 😊
## Links
- [Discord Bot]({DISCORD_BOT_REPO})
- [Server Repo]({BACKEND_REPO})
"""
