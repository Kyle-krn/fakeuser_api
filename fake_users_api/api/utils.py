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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip