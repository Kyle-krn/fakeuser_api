def flatten(dictionary: dict) -> dict:
    res = {}
    for k, v in dictionary.items():
        if not isinstance(v, dict):
            res[k] = v
        else:
            if v == {}:
                res[k] = ""
            else:
                for ks, vs in flatten(v).items():
                    res[k + '/' + ks] = vs
    return res