"""knex utils"""
import knex
import sys
import json


def build_lookup():
    parser_names = knex.__all__
    parser_objs = [getattr(sys.modules["knex"], x) for x in parser_names]
    return dict(zip(parser_names, parser_objs))


def transform(input_data, xformer_json, raise_exception=False):
    xformer = json.loads(xformer_json)
    last_object = None
    for x in xformer:
        if last_object is None:
            last_object = LOADER_LOOKUP.get("Start")(
                input_data, raise_exception=raise_exception
            )
        parser = LOADER_LOOKUP.get(x.get("parser"))
        args = x.get("args")
        last_object = last_object > parser(**args)
    return last_object


LOADER_LOOKUP = build_lookup()
