# Beatport Automation Tool

Automated Beatport account creation, bulk purchasing, and PDF receipt generation — with Cloudflare Turnstile bypass, proxy support, and a rich terminal UI.

---

## Features

- **Automated Account Creation** — Generates fake identities, fills signup forms, and handles the full registration flow
- **Cloudflare Turnstile Bypass** — Intercepts and solves Turnstile captchas via 2Captcha API
- **Billing Registration** — Automatically sets up billing with card details after account creation
- **Bulk Purchasing** — Purchase any product across multiple accounts in a single session
- **Smart Purchase Verification** — Detects successful purchases even when the checkout API returns errors
- **IP Address Tracking** — Captures the proxy IP for each purchase and stores it in CSV
- **PDF Receipt Export** — Generates branded PDF receipts with song names, IP addresses, and company branding
- **Multi-Card Rotation** — Randomly picks from a pool of configured cards for each account
- **Proxy Support** — Routes all browser traffic through a configurable proxy
- **Rich Terminal UI** — Progress bars, styled tables, color-coded output, and session summaries
- **Credential Logging** — All created accounts and purchases saved to CSV
- **File Logging** — Persistent log file with timestamped entries for debugging

---

## Prerequisites

- **Python 3.10+**
- **2Captcha API Key** — Required for solving Cloudflare Turnstile captchas ([2captcha.com](https://2captcha.com))
- **Proxy** (recommended) — Residential proxy to avoid IP-based rate limiting

---

## Installation

### 1. Get the project

**If you have repo access:**
```bash
git clone <repository-url>
cd beatport-acc-creator
```

**If you received a ZIP:**
```
Extract the ZIP to a folder and open a terminal there.
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browsers

```bash
playwright install chromium
```

### 4. Create the `.env` file

Copy the example and fill in your credentials:

```bash
cp .env.example .env
```

Then edit `.env` with your actual values:

```env
TWOCAPTCHA_API_KEY=your_2captcha_api_key
BEATPORT_SITEKEY=0x4AAAAAAARdaJSylLhXz0zB

# Proxy
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password
PROXY_HOST=gate.decodo.com
PROXY_PORT=10001

# Cards (format: number,expiry,cvv separated by semicolons)
CARDS=4111111111111111,12/31,123;5500000000000004,12/31,456
```

| Variable | Description |
|---|---|
| `TWOCAPTCHA_API_KEY` | Your 2Captcha API key for solving Turnstile captchas |
| `BEATPORT_SITEKEY` | Beatport's Cloudflare Turnstile site key (pre-filled) |
| `PROXY_USERNAME` | Proxy authentication username |
| `PROXY_PASSWORD` | Proxy authentication password |
| `PROXY_HOST` | Proxy server hostname |
| `PROXY_PORT` | Proxy server port |
| `CARDS` | Payment cards in `number,M/YY,cvv` format, separated by `;` |

### 5. Run

```bash
python main.py
```

---

## Usage

When you launch the tool, you'll see:

```
╭─────────────────────────────────────────────────────╮
│        Beatport Automation Tool                     │
│  Account creation, automated purchases, and receipts│
╰─────────────────────────────────────────────────────╯

Select an option:
  1. Create accounts
  2. Perform purchases
  3. Export PDF receipt

Option: > _
```

### Option 1: Create Accounts

Enter the number of accounts to create. The bot processes each account automatically:

1. Generates a fake identity (name, email, username, password, US address)
2. Checks email/username availability via Beatport API
3. Creates the account with Turnstile captcha bypass
4. Sets up billing with a randomly selected card
5. Saves credentials to `created_accounts.csv`

### Option 2: Perform Purchases

1. Enter the Beatport product URL (e.g., `https://www.beatport.com/fr/release/caliente/5812893`)
2. Enter the number of purchases to perform
3. The bot filters eligible accounts (those that haven't already purchased the product)
4. For each account: logs in, captures the proxy IP, verifies the library, and completes the purchase
5. Updates CSV with the purchase record and IP address

**Smart error handling:** If the checkout API returns an error (e.g., HTTP 400), the bot checks the library to verify if the purchase actually went through before retrying.

### Option 3: Export PDF Receipt

Generates a branded PDF receipt (`purchase_receipt.pdf`) listing all purchases across all accounts:

- **Header:** Company logo + document title + generation date
- **Body:** Table with song names (extracted from URLs) and IP addresses
- **Footer:** Beatpush, Inc. company address

---

## Output Files

| File | Description |
|---|---|
| `created_accounts.csv` | All account credentials and purchase records |
| `beatport_bot.log` | Timestamped log file for debugging |
| `purchase_receipt.pdf` | Generated PDF receipt (via option 3) |

### CSV Format

```csv
email,password,username,first_name,last_name,card_number,card_type,created_at,purchased_songs,purchase_ips
li5yl.john@inbox.testmail.app,aB3!xYz9,john4821,John,Smith,4165...5229,001,2026-03-06T14:30:00,https://www.beatport.com/fr/release/caliente/5812893,203.0.113.42
```

- `purchased_songs`: Pipe-separated (`|`) list of product URLs
- `purchase_ips`: Pipe-separated (`|`) list of proxy IPs (parallel to purchased_songs)

---

## Card Configuration

Cards are configured in the `.env` file using a compact format:

```
CARDS=number,expiry,cvv;number,expiry,cvv
```

- **Expiry format:** `M/YY` (e.g., `3/31` = March 2031)
- **Separator:** `;` between cards
- The bot randomly selects a card for each account

**Example with multiple cards:**
```
CARDS=4165981722225229,3/31,673;5354563333133382,3/31,818;5200828444428210,3/31,897
```

---

## Project Structure

```
beatport-acc-creator/
├── main.py              # Entry point — menu, account/purchase loops, CSV management
├── automator.py         # Core automation — Playwright browser control
├── pdf_generator.py     # PDF receipt generation
├── configs.py           # Config class — loads .env variables
├── logger.py            # Rich console output + file logging
├── requirements.txt     # Python dependencies
├── assets/
│   └── logo.png         # Company logo for PDF header
├── .env                 # Your credentials (not in repo)
├── .env.example         # Template for .env
├── LICENSE              # License & Terms of Service
│
├── created_accounts.csv # Output — account credentials & purchases (not in repo)
├── purchase_receipt.pdf # Output — generated PDF receipt (not in repo)
└── beatport_bot.log     # Output — timestamped log file (not in repo)
```

---

## Troubleshooting

### "TWOCAPTCHA_API_KEY" / KeyError on startup

Your `.env` file is missing or incomplete:
1. Copy `.env.example` to `.env`
2. Fill in all required values
3. Make sure there are no extra spaces around the `=` sign

### Playwright browser not found

Run the browser installer:
```bash
playwright install chromium
```

### Captcha solving fails / times out

- Verify your 2Captcha API key is correct and has balance
- Check that `BEATPORT_SITEKEY` matches the current Beatport Turnstile key
- 2Captcha Turnstile solving typically takes 10-20 seconds

### Proxy connection errors

- Verify your proxy credentials and host/port in `.env`
- Ensure the proxy supports HTTP/HTTPS traffic
- Check that the proxy service is active and not rate-limiting

### State/Province selection fails repeatedly

The bot generates US addresses using Faker. Occasionally, a generated state abbreviation doesn't match Beatport's dropdown options. The bot retries automatically (up to 5 times) with new address data.

### Checkout returns error but purchase succeeded

This is handled automatically. When checkout returns an error (e.g., HTTP 400 "Cart does not contain any items"), the bot checks the library to verify if the purchase went through before retrying.

### Account creation succeeds but billing fails

The account is still created and saved to CSV. You can manually set up billing later. Common causes:
- Card was declined or expired
- Proxy IP was flagged by the payment processor

---

## FAQ

**How long does each account take?**
Typically 30-60 seconds per account, depending on captcha solving speed and network latency.

**Can I run it headless (no browser window)?**
The browser currently launches in visible mode (`headless=False`) for debugging. To run headless, modify `automator.py` line 64: change `headless=False` to `headless=True`. (May not work properly in headless!)

**What if Beatport changes their signup flow?**
The bot interacts with specific form elements by role/label. If Beatport significantly changes their UI, the selectors in `automator.py` may need updating.

**Can I use different email domains?**
Currently uses `inbox.testmail.app`. To change it, modify the `email_address` format in `automator.py` in the `_sync_generate_fake_data` method.

**Is each account created with a unique IP?**
If your proxy rotates IPs per session (e.g., residential rotating proxies), yes. Each account gets a fresh browser context routed through the proxy.

---

## Support & Pricing

| | |
|---|---|
| **Price** | Contact for pricing |
| **Purchase & Support** | [Contact on Telegram](https://t.me/AkibHridoy) |

### Developer

**Abir Hasan**
- GitHub: [github.com/AbirHasan2005](https://github.com/AbirHasan2005)
- Telegram: [t.me/AbirHasan2005](https://t.me/AbirHasan2005)

---

## License & Legal

This software is proprietary and commercially licensed. By using this tool, you agree to the terms outlined in the [LICENSE](LICENSE) file, which includes the License Agreement, Terms of Service, Confidentiality & Anti-Redistribution Policy, and Privacy Policy.

**Unauthorized redistribution of this software is strictly prohibited and will result in legal action.**
