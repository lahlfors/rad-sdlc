# Skills Repository

This repository contains specialized skills and tools for the Gemini Agent, focusing on Google Cloud and AI development.

## Available Skills

### Google Agent Development Kit (ADK) Cheatsheet
Located in `skills/adk_cheatsheet/`.
This "Hard Skill" provides a Model Context Protocol (MCP) server that gives the agent granular access to the Google Agent Development Kit (ADK) Python Cheatsheet. It allows the agent to search for specific syntax, examples, and patterns without needing to load the entire documentation into context.

## Deployment & Usage

### 1. Deploying Your Skills Server (Local Host)
To use this server, you must treat it as a local "tool host" that clients connect to.

*   **Command**: `/Users/laah/Code/Skills/.venv/bin/python /Users/laah/Code/Skills/skills/adk_cheatsheet/server.py`
*   **Verification**: Run the command in your terminal. It should start and wait for JSON-RPC connections (no output indicates it is ready/listening).

### 2. Integration with Google Gemini CLI

**Installation & Auth**
```bash
npm install -g @google/gemini-cli
gemini auth login
```

**Configure the MCP Connection**
Add your skills server to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "adk-cheatsheet": {
      "command": "python",
      "args": [
        "/Users/laah/Code/Skills/skills/adk_cheatsheet/server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Verification**
```bash
gemini mcp list
```

### 3. Integration with Google Antigravity

**Option A: UI Method**
1.  Open Agent Side Panel > Additional Options (...) > **"Manage MCP Servers"**.
2.  Add Server:
    *   **Name**: ADK Cheatsheet
    *   **Command**: `python`
    *   **Arguments**: `/Users/laah/Code/Skills/skills/adk_cheatsheet/server.py`

**Option B: Config File Method**
Create `.antigravity/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "adk-cheatsheet": {
      "command": "python",
      "args": ["/Users/laah/Code/Skills/skills/adk_cheatsheet/server.py"],
      "alwaysAllow": ["adk_lookup", "adk_list_table_of_contents"]
    }
  }
}
```

## Tool Usage

### `adk_lookup`
Searches the cheatsheet for information on a specific topic.
*   `adk_lookup(query="Callbacks")` -> Returns details on callback usage.

### `adk_list_table_of_contents`
Returns the structure of the documentation.

## License

Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
