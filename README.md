# 🎂 VITMAS Birthday Telegram Bot

A sophisticated Telegram bot that automatically sends birthday reminders by fetching birthday data from Google Sheets. Built for the VITMAS club at VIT Vellore to celebrate member birthdays.

## Accesing the bot on Telegram
Search for [@vitmas_bday_bot](https://t.me/vitmas_bday_bot) on telegram and click on start to subscrive to this service.
/upcoming will send upcoming 3 Birthdays

-> New functions will be added soon

## ✨ Features

- 🤖 **Automated Birthday Alerts** - Sends birthday reminders tomorrow at scheduled times via cron
- 🎯 **Command Support** - Interactive Telegram commands for users
- 📊 **Google Sheets Integration** - Centralized birthday database with easy management
- 👥 **User Registration** - Automatic user tracking when they subscribe
- 🔐 **OAuth2 Secure** - Uses Google OAuth2 for authentication
- 📱 **Webhook Support** - Real-time message handling via Telegram webhook
- 🚀 **Scalable** - Clean modular architecture, easy to extend

## 🏗️ Architecture

The application follows a modular design pattern with clear separation of concerns:

```
┌─────────────────┐
│    Telegram     │
│      API        │
└────────┬────────┘
         │
    ┌────▼────────┐
    │  Flask App  │
    └────┬────────┘
         │
    ┌────┴────────────────┬────────────────┬──────────────┐
    │                     │                │              │
┌───▼──────┐  ┌──────────▼──────┐  ┌─────▼──────┐  ┌────▼──────┐
│  Handlers │  │     Routes      │  │ Telegram   │  │  Birthday │
│           │  │                 │  │  Service   │  │   Logic   │
└───────────┘  └─────────────────┘  └────────────┘  └────────────┘
    │                                                      │
    └──────────────────┬─────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    ┌───▼──────┐  ┌───▼────────┐  ┌─▼────────────┐
    │  Users   │  │   Sheets   │  │   Config     │
    │ Service  │  │  Service   │  │              │
    └──────────┘  └───────┬────┘  └──────────────┘
                          │
                    ┌─────▼──────┐
                    │   Google   │
                    │   Sheets   │
                    └────────────┘
```

## 📦 Prerequisites

- **Python 3.8+**
- **Telegram Bot Token** from [BotFather](https://t.me/botfather)
- **Google Cloud Service Account** with Sheets and Drive API enabled
- **Google Sheet ID** with birthday data
- **Server/Host** for running Flask (supports Heroku, Vercel, AWS, etc.)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/VITMASClub/vitmas-bdays-telegram-bot.git
cd vitmas-bdays-telegram-bot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root (or set via your hosting platform):

```env
BOT_TOKEN=your_telegram_bot_token_here
SHEET_ID=your_google_sheet_id_here
GOOGLE_CREDENTIALS={"type":"service_account","project_id":"..."}
```

> **Note:** For `GOOGLE_CREDENTIALS`, paste the entire JSON from your Google service account key file as a single-line JSON string.

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ Yes | Your Telegram bot token from BotFather |
| `SHEET_ID` | ✅ Yes | Google Sheet ID containing birthday data |
| `GOOGLE_CREDENTIALS` | ✅ Yes | Google service account credentials (JSON) |

### Google Sheets Setup

Your Google Sheet must have two worksheets:

**1. Main Sheet (Birthday Data)**
```
| Name     | DOB    | Phone     |
|----------|--------|-----------|
| John Doe | 15/03  | +91912345 |
| Jane Doe | 22/07  | +91987654 |
```

**2. Users Sheet (Registered Users)**
```
| ChatID      |
|-------------|
| 123456789   |
| 987654321   |
```

## 🚀 Usage

### Running the Bot

```bash
python app.py
```

The server will start on `http://0.0.0.0:5000`

### Telegram Commands

Users can interact with the bot using these commands:

| Command | Description |
|---------|-------------|
| `/start` | Subscribe to birthday alerts |
| `/upcoming` | View the next 3 upcoming birthdays |

### Example Interactions

```
User: /start
Bot: ✅ Subscribed to birthday alerts!

User: /upcoming
Bot: 🎂 Upcoming Birthdays:

1. John Doe - Mar 15
2. Jane Doe - Jul 22
3. Admin User - Dec 01
```

## 📡 API Endpoints

### 1. **Webhook Endpoint**
Receives and processes incoming Telegram messages.

```http
POST /webhook
Content-Type: application/json

{
  "update_id": 123456789,
  "message": {
    "chat": {
      "id": 987654321
    },
    "text": "/start"
  }
}
```

**Response:**
```
ok
```

### 2. **Cron Birthday Alert**
Triggers sending birthday alerts for upcoming birthdays (meant for cron jobs).

```http
GET /send-birthday-alert
```

**Response:**
```
Sent
```

Or if no birthdays:
```
No birthdays
```

## 📖 Setup Guides

### Setting up Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/start` and follow prompts
3. Send `/newbot` to create a new bot
4. Enter bot name and username
5. Copy the **Bot Token** - save this to `BOT_TOKEN` env variable
6. Send `/setwebhook` command to BotFather
7. Set webhook URL: `https://yourdomain.com/webhook`

### Setting up Google Cloud & Sheets

**Step 1: Create Google Cloud Project**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Sheets API** and **Google Drive API**

**Step 2: Create Service Account**
1. Go to **Service Accounts** in Google Cloud
2. Click "Create Service Account"
3. Fill in account details
4. Click "Create and Continue"
5. In the Keys section, create a JSON key
6. Download the JSON file - this is your `GOOGLE_CREDENTIALS`

**Step 3: Create Google Sheet**
1. Create a new Google Sheet
2. Rename the first sheet to match your data (or use default)
3. Add a second sheet named **"Users"**
4. Copy the Sheet ID from the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
5. Share the sheet with your service account email address

## 📁 Project Structure

```
vitmas-bdays-telegram-bot/
├── app.py                 # Flask app entry point (8 lines)
├── config.py              # Configuration & environment setup
├── routes.py              # Flask routes (webhook & cron endpoints)
├── handlers.py            # Telegram command handlers
├── telegram_service.py    # Telegram API operations
├── sheets_service.py      # Google Sheets operations
├── birthday_logic.py      # Birthday calculations & logic
├── users.py               # User management
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── credentials.json       # Google service account (not in repo)
├── users.json             # User data backup (local)
└── test.py                # Testing script
```

### Module Descriptions

| Module | Purpose |
|--------|---------|
| **app.py** | Clean Flask application entry point |
| **config.py** | Centralized environment variables and OAuth setup |
| **routes.py** | Webhook and cron endpoints for Flask |
| **handlers.py** | Business logic for Telegram commands |
| **telegram_service.py** | Direct Telegram API communication |
| **sheets_service.py** | Google Sheets read/write operations |
| **birthday_logic.py** | Birthday date calculations and filtering |
| **users.py** | User registration and management |

## 🧪 Testing

Run the test script to verify Google Sheets connectivity:

```bash
python test.py
```

This will fetch and print all birthday records from your configured sheet.

## 🚢 Deployment

### Heroku

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
git push heroku main
```

### AWS Lambda / Vercel

Use the Flask app with serverless adapters or deploy as a container.

### Self-hosted

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Waitress (Windows)
waitress-serve --port=5000 app:app
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `BOT_TOKEN not found` | Verify environment variable is set correctly |
| `Google Sheets permission denied` | Ensure service account email is shared on the sheet |
| `Webhook not receiving messages` | Verify webhook URL is correct and publicly accessible |
| `ImportError: No module named 'gspread'` | Run `pip install -r requirements.txt` |
| `DOB format error` | Ensure date format is exactly `DD/MM` (e.g., `15/03`) |

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- **VITMAS Development Team**
- Created for VIT Vellore's VITMAS Club

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ for VITMAS Club at VIT Vellore**
