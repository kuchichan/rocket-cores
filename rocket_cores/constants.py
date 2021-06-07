from typing import Final

MAX_CORE_LIMIT = 10
GRAPHQL_API_URL: Final[str] = "https://api.spacex.land/graphql/"


CORE_QUERY_LIMIT: Final[
    str
] = """query($lim: Int, $offset: Int) {
  cores(sort: "reuse_count", order: "desc", limit: $lim, offset: $offset) { 
    id
    reuse_count
  }
}
"""

CORE_QUERY: Final[
    str
] = """ {
  cores(sort: "reuse_count", order: "desc") { 
    id
    reuse_count
  }
}
"""


PAYLOAD_QUERY: str = """query($id: String) {{
  {launches_type} (find: {{ core_serial: $id }}) {{
    rocket {{
      second_stage {{
        payloads {{
          payload_mass_kg
        }}
      }}
    }}
  launch_success
  }}
}}
"""
