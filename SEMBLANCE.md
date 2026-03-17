# Hermes Telegram Semblance Document

## What Happened

A test message was scheduled via Hermes cron job to be delivered to a Telegram channel.
The message was NOT delivered. Here is the full investigation.

## The Error

From `~/.hermes/logs/gateway.error.log`:

```
2026-03-17 09:48:04,790 ERROR cron.scheduler: Job '474f00965460': delivery error: Telegram send failed: Chat not found
```

**Root Cause:** Telegram API returned "Chat not found" for chat ID `-1003778120257`.

## Why the Message Failed

There are two errors found in the logs:

### Error 1: Chat Not Found

The cron job tried to deliver to `telegram:-1003778120257` but Telegram's API
could not find that chat. This happens when:

1. **The bot is NOT a member of the channel/group**
   - The Hermes Telegram bot must be added to the target channel as an admin
   - Without membership, the bot cannot send messages to that chat

2. **The chat ID is incorrect**
   - The URL `https://web.telegram.org/a/#-1003778120257` shows the web client's
     internal ID. The actual Telegram API chat ID may differ.
   - Telegram supergroups/channels use IDs starting with `-100` followed by the
     numeric ID. The ID from the URL `-1003778120257` may need to be verified.

3. **The bot lacks permissions**
   - Even if added to the channel, the bot needs "Post Messages" permission

### Error 2: Duplicate Gateway (Earlier)

```
2026-03-17 09:36:10,646 ERROR gateway.platforms.telegram:
  Another local Hermes gateway is already using this Telegram bot token (PID 78567).
  Stop the other gateway before starting a second Telegram poller.
```

This means another Hermes gateway process was already running on the same bot token,
which can cause conflicts.

## How to Fix It

### Step 1: Add the Bot to the Channel

1. Open Telegram and go to the target channel
2. Go to Channel Settings → Administrators
3. Click "Add Administrator"
4. Search for your Hermes bot (bot username from BotFather)
5. Grant it at minimum "Post Messages" permission
6. Save

### Step 2: Verify the Chat ID

Get the correct chat ID by sending a message IN the channel/group where the bot
is a member, then check:

```bash
# Replace BOT_TOKEN with your actual bot token
curl -s "https://api.telegram.org/bot<BOT_TOKEN>/getUpdates" | python3 -m json.tool
```

Look for the `chat.id` field in the response. Use that exact number (including
the minus sign for groups/channels) as your delivery target.

Alternatively, forward a message from the channel to @userinfobot or @RawDataBot
to get the chat ID.

### Step 3: Fix the Duplicate Gateway

Stop the conflicting Hermes gateway process:

```bash
# Find the process
ps aux | grep hermes | grep gateway

# Kill the old one
kill 78567
```

Then restart the gateway cleanly:

```bash
hermes gateway start
```

### Step 4: Retry the Message

Once the bot is added and the chat ID is confirmed, schedule a new test:

```bash
# From Hermes CLI, ask it to send a test message to the correct chat ID
# Example with corrected chat ID:
hermes cron create --name "telegram-test" \
  --schedule "1m" \
  --deliver "telegram:<CORRECT_CHAT_ID>" \
  --repeat 1 \
  --prompt "Hello from Hermes! Test message."
```

Or simply message the Hermes bot directly on Telegram to verify it's responding.

## Checklist

- [ ] Bot is added to the target channel/group as admin
- [ ] Bot has "Post Messages" permission
- [ ] Chat ID is verified via getUpdates or @RawDataBot
- [ ] No duplicate gateway processes running
- [ ] Test message delivered successfully

## Logs Location

All relevant logs can be found at:

```
~/.hermes/logs/errors.log           — Application errors
~/.hermes/logs/gateway.error.log    — Gateway-specific errors
~/.hermes/logs/gateway.log          — Full gateway activity log
```

## Summary

The message failed because of **"Chat not found"** — most likely the Hermes
Telegram bot has not been added as an administrator to the target channel
(`-1003778120257`). Add the bot to the channel with posting permissions,
verify the chat ID, and retry.
