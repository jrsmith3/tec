# -*- coding: utf-8 -*-
import tec

def to_json(obj):
    if isinstance(obj, tec.electrode.metal.Metal):
        encoded_obj = dict(obj)
        encoded_obj["__class__"] = str(encoded_obj["__class__"])
        return encoded_obj

