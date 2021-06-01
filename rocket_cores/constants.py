from typing import Final

GRAPHQL_API_URL: Final[str] = "https://api.spacex.land/graphql/"


CORE_QUERY: Final[
    str
] = """query($lim: Int) {
  cores(sort: "reuse_count", order: "desc", limit: $lim) { 
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
