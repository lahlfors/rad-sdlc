# ADK Cheatsheet MCP Server - Deployment & Usage

This document describes how to deploy and use the ADK Cheatsheet MCP Server.

## 1. Description
This "Hard Skill" provides a Model Context Protocol (MCP) server that gives the agent granular access to the Google Agent Development Kit (ADK) Python Cheatsheet. It allows the agent to search for specific syntax, examples, and patterns without needing to load the entire documentation into context.

## 2. Deploying Your Skills Server (Local Host)
To use this server, you must treat it as a local "tool host" that clients connect to.

*   **Command**: `/Users/laah/Code/Skills/.venv/bin/python /Users/laah/Code/Skills/skills/adk_cheatsheet/server.py`
*   **Verification**: Run the command in your terminal. It should start and wait for JSON-RPC connections (no output indicates it is ready/listening).

## 3. Integration with Google Gemini CLI
The Gemini CLI is a terminal-based tool that can "consult" your skills before running commands.

### Installation & Auth
If you haven't installed it yet:
```bash
npm install -g @google/gemini-cli
gemini auth login
```

### Configure the MCP Connection
The Gemini CLI looks for a global configuration file to know which servers to listen to.

1.  Open (or create) the settings file: `~/.gemini/settings.json`
2.  Add your skills server to the "mcpServers" block:

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

### Verification
Run the following command in your terminal to verify the CLI sees the skills:
```bash
gemini mcp list
```
You should see `adk-cheatsheet` listed with a status of Connected.

## 4. Integration with Google Antigravity
Antigravity (the agentic IDE) has a dedicated UI for managing these connections, as it relies on them for its "Mission Control" agents.

### Option A: Add the Server (UI Method)
1.  Launch Google Antigravity.
2.  Open the Agent Side Panel (Right-hand sidebar).
3.  Click the **Additional Options (...)** icon in the top header of the panel.
4.  Select **"Manage MCP Servers"**.
5.  Enter the following details:
    *   **Name**: ADK Cheatsheet
    *   **Transport Type**: Stdio
    *   **Command**: `python`
    *   **Arguments**:
        *   Arg 1: `/Users/laah/Code/Skills/skills/adk_cheatsheet/server.py`

### Option B: Add the Server (Config File Method)
If you prefer a specific config file for your project:

1.  Create an `mcp.json` file in your project's hidden folder: `.antigravity/mcp.json` (Create the folder if it doesn't exist).
2.  Add the content:

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
*Note: The `alwaysAllow` field prevents the agent from asking for permission every time it wants to read the cheatsheet.*

## 5. Tool Usage

The server exposes two primary tools:

### `adk_lookup`
Searches the cheatsheet for information on a specific topic.

- **Signature**: `adk_lookup(query: str) -> str`
- **Example**:
  - User asks: "How do I use callbacks in ADK?"
  - Agent calls: `adk_lookup("Callbacks")`
  - Result: Returns code examples and explanations for `before_agent_callback`, `after_tool_callback`, etc.

### `adk_list_table_of_contents`
Returns the structure of the documentation.

- **Signature**: `adk_list_table_of_contents() -> str`
- **Example**:
  - Agent calls: `adk_list_table_of_contents()`
  - Result: Returns a list of all sections (e.g., "1. Core Concepts", "2. Agent Definitions").

## 6. Best Practices for the Agent
- **Don't Guess**: If you are unsure about a specific ADK class or method signature, use `adk_lookup`.
- **Be Specific**: Search for specific class names (e.g., `LlmAgent`, `LoopAgent`) for better results.
- **Cross-Reference**: If the first lookup is insufficient, use the table of contents to find related sections.
