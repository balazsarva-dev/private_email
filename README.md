# private_email – MCP server for Private Email

## 1. What is this used for?

This MCP server connects Claude Code to your Private Email (privateemail.com) mailbox.

After setup you can:
- list emails in any of your folders via the `list_messages` tool,
- search emails via the `search_message` tool,
- read specific email(s) via the `read_message` tool,
- delete a message via the `delete_message` tool,
- empty your Trash folder via the `vacuum_folder` tool.

What else is it good for?
- it can draft emails and save them to your Drafts folder (`draft_message`),
- it can send emails (`send_message`) – Claude Code asks for permission before each tool call by default.


## 2. Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- [Claude Code](https://claude.com/claude-code)
- a Private Email (privateemail.com) account


## 3. Installation

1. Clone the repository with SSH or HTTPS:

```bash
git clone git@github.com:balazsarva-dev/private_email.git && cd private_email
```

or
```bash
git clone https://github.com/balazsarva-dev/private_email.git && cd private_email
```


2. Install the dependencies defined in pyproject.toml:

```bash
uv sync
```

3. Create the .env file from the example, then fill in your email address and password:

```bash
cp .env.example .env
```

4. Add the MCP server to Claude Code:

```bash
claude mcp add private-email -s user -- uv run --project $(pwd) private-email
```

5. Restart Claude Code, then run `/mcp` to check that the `private-email` server is connected.
