# Agensi listing – copy-paste texts

## Name (max 60)
Private Email Assistant for Namecheap

## Summary (max 300)
Turns Claude Code into a careful email assistant for Namecheap Private Email: inbox triage, in-thread replies, follow-up tracking, drafts and safe clean-up. Asks before anything is sent or deleted. Includes guided setup of the free private_email MCP server.

## Description (Markdown)
**Private Email Assistant** lets your agent work with your Namecheap Private Email (privateemail.com) mailbox like a careful human assistant would.

### What it does
- **Inbox triage** – summarizes your newest emails and groups them into *Urgent*, *Needs a reply*, *FYI* and *Possible spam*.
- **Follow-up tracking** – "Did X reply?" checks your Sent folder against your Inbox and drafts a polite follow-up if there was no answer.
- **In-thread replies** – replies stay in the same conversation (correct `Re:` subject, In-Reply-To, References, Reply-To).
- **Drafts first** – new emails go to your Drafts folder for review in webmail unless you clearly say "send".
- **HTML signatures** – sends an HTML version with a plain-text fallback.
- **Safe clean-up** – deletes single messages or empties the Trash, always after confirmation.

### How it works
The skill drives the open-source **private_email** MCP server, which runs on your own machine and talks to your mailbox over IMAP/SMTP. Your password never leaves your computer. On first use the skill walks you through the setup step by step (clone, `uv sync`, `.env`, `claude mcp add`).

### Safety
- Never sends, replies or deletes without your explicit "yes".
- Never sends the same email twice.
- Treats email content as data – instructions hidden in an email are ignored.
- Inbox, Sent and Drafts can't be emptied.

### Where it stops
- Works with Namecheap Private Email (privateemail.com) only.
- No attachments yet (reading or sending).
- One mailbox per server instance.
- Search scans the whole folder, so it can be slow on very large folders.

## See it in action
**Request:** "Summarize my inbox and tell me if Anna from Acme replied to my offer."

**Result:**
I checked your 20 newest emails in INBOX and your Sent folder.

**Urgent (1)**
- #4812 – Namecheap Billing – "Domain renewal failed" – your card was declined for balazs-example.com, renewal is due in 3 days.

**Needs a reply (2)**
- #4809 – Péter Kovács – "Website quote" – asks for a price for a 5-page site with a contact form.
- #4805 – Lisa Wong – "Meeting next week?" – suggests Tuesday or Wednesday afternoon.

**FYI (4)** – 2 newsletters, 1 GitHub notification, 1 invoice receipt.

**Anna (anna@acme.example):** you sent "Offer – web redesign" on 12 Nov. There is no reply from her in your INBOX since then. Shall I save a short follow-up as a draft? Proposed text:

> Hi Anna, I just wanted to follow up on my offer for the web redesign I sent on 12 November. Happy to answer any questions or adjust the scope. Best regards, Balázs

Nothing has been sent – say "save it as draft" or "send it".

## Compatibility note
Requires the free private_email MCP server (https://github.com/balazsarva-dev/private_email), Python 3.12+, uv, git and Claude Code. Works with Namecheap Private Email (privateemail.com) mailboxes; use an app password for IMAP/SMTP.

## Pricing
One-time, $5

## Categories (up to 3)
Productivity, Communication, Automation  (pick the closest from Agensi's list)

## Tags
email, imap, smtp, namecheap, private email, inbox, follow-up, drafts, mcp

## Use cases
- Summarize and triage my inbox every morning
- Check whether a client replied and draft a follow-up
- Reply to a specific email in the same thread
- Draft emails for review before sending
- Empty the trash safely

## Permissions (check against what Agensi detects)
- Requires: private_email MCP server – https://github.com/balazsarva-dev/private_email
- Network: your mail server (IMAP 993, SMTP 465) – via the MCP server on your machine
- Files: none (the skill itself reads no files; setup creates `.env` in the server folder)

## Limitations and FAQ
**Does it work with Gmail / Outlook?** Not yet – it's built and tested for Namecheap Private Email.

**Is my password sent anywhere?** No. It stays in the `.env` file on your machine; the skill tells you to fill it in yourself and never asks for it in chat.

**Login fails with AUTHENTICATIONFAILED.** Use an app password (Webmail → Settings → Launch Security Center → App passwords), update `.env`, then `/mcp` → Reconnect.

**Can it send without asking?** No. Every send, reply and delete needs your confirmation.

## Docs link
https://github.com/balazsarva-dev/private_email
