from knex.utils import transform
import json


xform_networks_json = """
[
    {
        "parser": "GetIndex",
        "args":
        {
            "idx": 0
        }
    },
    {
        "parser": "Concat",
        "args":
        {
            "prefix": "",
            "suffix": "/24"
        }
    },
    {
        "parser": "IpNetwork",
        "input": "192.168.190.235/24",
        "args":
        {}
    }
]
"""

input_data = ["192.168.190.235", "192.168.191.2"]

end_obj = transform(input_data, xform_networks_json, raise_exception=True)

print(json.dumps(end_obj.history, indent=4))
print(end_obj.result)
