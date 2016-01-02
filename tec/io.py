# -*- coding: utf-8 -*-
import tec

def to_json(obj):
    if isinstance(obj, tec.electrode.metal.Metal):
        encoded_obj = dict(obj)
        encoded_obj["__class__"] = str(encoded_obj["__class__"])
        return encoded_obj

def from_json(obj):
    if "__class__" in obj:
        if obj["__class__"] == "<class 'tec.electrode.metal.Metal'>":
            return tec.electrode.metal.Metal.from_dict(obj)

        if obj["__class__"] == "<class 'tec.electrode.semiconductor.SC'>":
            return tec.electrode.semiconductor.SC.from_dict(obj)
