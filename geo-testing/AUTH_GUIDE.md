# 🔐 ChatGPT Authentication Guide

## How It Works

The GEO testing system uses **saved session authentication** to avoid logging in every time:

```
Login Once → Save Session → Reuse Forever (until expired)
```

### Saved Session File
- **Location**: `storage/auth_state.json`
- **Contains**: Cookies, tokens, session data
- **Validity**: Usually 30+ days
- **Security**: Local only, never committed to git

---

## ✅ Check if You're Logged In

```bash
python test_auth.py
```

**Output:**
- ✅ "SUCCESS! You're logged in" → You're good to go!
- ❌ "FAILED! Not logged in" → Session expired, re-authenticate below

---

## 🔄 How to Re-Authenticate

### **Option 1: Manual Login** (Recommended, Most Secure)

```bash
python scripts/login.py --manual
```

**What happens:**
1. Browser opens to ChatGPT
2. You login manually (supports 2FA, Google login, etc.)
3. Script saves your session
4. Done! ✅

**Best for:**
- 2FA enabled accounts
- Google/Microsoft SSO
- Maximum security (no passwords in code)

---

### **Option 2: Automated Login** (Faster)

```bash
python scripts/login.py --auto
```

**Requirements:**
- Credentials in `.env` file:
  ```
  CHATGPT_EMAIL=your@email.com
  CHATGPT_PASSWORD=yourpassword
  ```

**What happens:**
1. Script reads credentials from `.env`
2. Automatically logs in
3. Saves session
4. Done! ✅

**Best for:**
- Quick re-authentication
- No 2FA accounts
- Automated workflows

---

### **Option 3: Quick Legacy Script**

```bash
python scripts/record_login.py
```

Uses hardcoded credentials (already has your email/password).

---

## 🚨 Troubleshooting

### "Auth state file NOT found"
**Fix:** Run any login script above

### "Session expired"
**Fix:** Your session lasted 30+ days and expired. Just re-login:
```bash
python scripts/login.py --manual
```

### "Login failed" (automated)
**Possible causes:**
- Wrong password in `.env`
- 2FA enabled → Use `--manual` instead
- ChatGPT UI changed → Use `--manual` instead

---

## 🔒 Security Notes

1. **`.env` file** contains your password → Never commit to git ✅ (already in .gitignore)
2. **`auth_state.json`** contains session tokens → Never commit to git ✅ (already in .gitignore)
3. **Manual login** is more secure (no passwords stored)
4. **Automated login** is convenient but stores password in `.env`

---

## 📋 Current Status

✅ **Your setup:**
- Email: maria@citable.xyz
- Password: Stored in `.env`
- Session: Valid until expired
- Auth file: `storage/auth_state.json` ✅

**Test auth:** `python test_auth.py`  
**Re-login manually:** `python scripts/login.py --manual`  
**Re-login auto:** `python scripts/login.py --auto`

---

## 🎯 When Testing Runs

The `run_from_db.py` script automatically:
1. Checks if `storage/auth_state.json` exists
2. Loads your saved session
3. Opens ChatGPT already logged in
4. Runs all tests
5. Closes browser

**No manual login needed during testing!** 🎉

---

## 💡 Pro Tips

1. **Session lasts 30+ days** → Login once per month
2. **Browser stays open** during testing → You can watch it work
3. **Session works headless too** → Change `headless=False` to `True` for background testing
4. **Multiple accounts?** → Create different auth files and switch between them

---

## 🆘 Quick Commands

```bash
# Check if logged in
python test_auth.py

# Login manually (safest)
python scripts/login.py --manual

# Login automatically
python scripts/login.py --auto

# Check credentials
cat .env | grep CHATGPT

# View saved session (don't share this!)
cat storage/auth_state.json | head -5
```

