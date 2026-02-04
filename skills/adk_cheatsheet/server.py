# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP server
mcp = FastMCP("adk-cheatsheet")

# Load content
CONTENT_FILE = os.path.join(os.path.dirname(__file__), "cheatsheet_content.md")

def _get_content():
    """Reads the cheatsheet content safely."""
    if not os.path.exists(CONTENT_FILE):
        return "Error: Cheatsheet content file not found."
    with open(CONTENT_FILE, "r") as f:
        return f.read()

@mcp.tool()
def adk_lookup(query: str) -> str:
    """
    Search the ADK cheatsheet for information.
    
    Args:
        query: The topic or keyword to search for (e.g., "Agent Config", "LlmAgent", "Callbacks").
    
    Returns:
        Relevant sections of the cheatsheet or a message if not found.
    """
    content = _get_content()
    # Simple search implementation for now - return full content if small, or chunks
    # For this "cheatsheet", returning the whole thing might be too big, 
    # but let's start by just searching for the query in the text and returning a window.
    
    lines = content.split('\n')
    results = []
    
    # Basic keyword search with context window
    for i, line in enumerate(lines):
        if query.lower() in line.lower():
            # Add context: 5 lines before and 20 lines after
            start = max(0, i - 5)
            end = min(len(lines), i + 20)
            chunk = "\n".join(lines[start:end])
            results.append(f"--- Match at line {i+1} ---\n{chunk}\n")
            
            # Limit to 5 matches to avoid exploding context
            if len(results) >= 5:
                break
    
    if not results:
        return f"No matches found for '{query}' in the ADK cheatsheet."
        
    return "\n".join(results)

@mcp.tool()
def adk_list_table_of_contents() -> str:
    """
    Returns the Table of Contents of the ADK cheatsheet to help navigate topics.
    """
    content = _get_content()
    toc_lines = []
    recording = False
    
    for line in content.split('\n'):
        if "## Table of Contents" in line:
            recording = True
        if recording:
            toc_lines.append(line)
            # Stop recording if we hit the next major header (assuming consistent formatting)
            if line.startswith("## ") and "Table of Contents" not in line and "1." not in line:
                 # This is a bit heuristic, but for markdown it usually works to stop at the next H2
                 # Actually, let's just grab the block until the horizontal rule or next section
                 pass
        
        # Stop heuristically after we see the end of the TOC (usually a generated list)
        # Simplified: just grep for lines starting with 'number. ['
        
    # Re-implementation: Just filter for lines that look like TOC entries
    toc = [line for line in content.split('\n') if line.strip().startswith(tuple(f"{i}." for i in range(1, 20)))]
    
    if not toc:
        return "Could not parse Table of Contents."
        
    return "\n".join(toc)

if __name__ == "__main__":
    mcp.run()
