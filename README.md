# This project is a MCP server for privateemail


## To use this project follow the instructions below:


1. Init the project

*A, without cloning*

```bash
uv init private_email && sleep 2; cd private_email
```

*B, with repo cloning*

```bash
git clone git@github.com:balazsarva-dev/private_email.git
```

2. Add the dependencies

```bash
uv add "mcp[cli]" && uv add python-dotenv;
```

3. Create .env file in the project root

```bash
touch .env
```

4. Add the MCP server to claude mcp list

```bash
claude mcp add private-email -s user -- uv run --project /home/balazsarva1982/Projects/private_email private-email
```
