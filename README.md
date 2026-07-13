# Xiaomi Bootloader Unlock Request Automation (boot-unloader)

A lightweight Python script designed to automate sending bootloader 
unlock requests (`bl-auth`) to the Xiaomi API before the UTC+8 midnight reset window.

## Disclaimer

This project is totally experimental and I only built it to **gain experience about mitmproxy**.
It is not my fault if it doesn't work, Xiaomi bans your account, or somewhere some nuclear weapons detonate.
I am making it open-source **only** as to share my knowledge. Use at your own risk. 

## Features

- **Token Validation:** Verifies that your session cookie is active and valid before entering the countdown loop.
- **Precise Countdown:** Computes the remaining time until UTC+8 midnight and enters a high-frequency polling window.
- **Auto-Retry Loop:** Rapidly transmits application requests when the deadline window opens to maximize acceptance chances.

## Prerequisites

- Python 3.10 or higher
- Target application credentials intercepted from your device

## Installation

1. **Clone or download this repository** to your local machine.
2. **Install the required dependencies** using `uv`:

```bash
uv sync
```

## Configuration

The script authenticates using session cookies extracted from an intercepted device request.

1. Create a file named `.env` in the same directory as `main.py`.
2. Add your intercepted `COOKIE` string to the file:

```env
COOKIE="<cookie-here>"
```

> [!TIP]
> For best results, capture your login session token and launch this script within 
**30 minutes (1800 seconds)** of the midnight reset window to help prevent token expiration.

## Usage

Run the script directly from your terminal:

```bash
uv run main.py
```

### How It Works

1. The script validates your token configuration.
2. It idles safely while tracking time down to **X seconds (defaults to 10)** before UTC+8 midnight.
3. Once inside this X-second threshold, it fires requests every `0.1` seconds until midnight passes.

## Token Extraction 

I used [mitmproxy](https://www.mitmproxy.org/) and [android-unpinner](https://github.com/mitmproxy/android-unpinner)
to extract the session data from the Mi Community app. Use **android-unpinner** to remove certificate requiriments 
of Mi Community app. No root needed. Afterwards, configure your device to communicate through **mitmproxy**.
Make sure you can listen to the communication of the Mi Community app. Login and try unlocking the bootloader.
It should fail, but you can now copy the cookies from the **mitmweb** interface.

## License

MIT
