# This project is a MCP server for privateemail


## To use this project follow the instructions below:


1. Init the project

```bash
git clone git@github.com:balazsarva-dev/private_email.git && cd private_email;
```

2. Add the dependencies defined in the pyproject.toml

```bash
uv sync;
```

3. Create .env file in the project root and copy the .env.example content into this

```bash
touch .env
```

4. Add the MCP server to claude mcp list

```bash
claude mcp add private-email -s user -- uv run --project $(pwd) private-email
```
