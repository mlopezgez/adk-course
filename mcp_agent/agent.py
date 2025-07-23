import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# It's good practice to define paths dynamically if possible,
# or ensure the user understands the need for an ABSOLUTE path.
# For this example, we'll construct a path relative to this file,
# assuming '/path/to/your/folder' is in the same directory as agent.py.
# REPLACE THIS with an actual absolute path if needed for your setup.
TARGET_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "/Users/matias/Documents/Projects/ADK/course",
)

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="mcp_agent",
    instruction=(
        "Help the user with mapping, directions, and finding places using Google Maps tools."
        "Also, you have the capacity of listing files in the users directory"
    ),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",  # Argument for npx to auto-confirm install
                    "@modelcontextprotocol/server-filesystem",
                    os.path.abspath(TARGET_FOLDER_PATH),
                ],
            ),
            # Optional: Filter which tools from the MCP server are exposed
            tool_filter=["list_directory", "read_file"],
        ),
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                # Pass the API key as an environment variable to the npx process
                # This is how the MCP server for Google Maps expects the key.
                env={"GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY},
            ),
            # You can filter for specific Maps tools if needed:
            # tool_filter=["get_directions", "find_place_by_id"],
        ),
    ],
)
