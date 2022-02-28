import re


def toBytes(transform):
    r = re.compile("([-+]?\d*\.\d+|\d+)([a-zA-Z]+)")
    match = r.match(transform)

    if match:
        value = match.group(1)
        unit = match.group(2)
        unit = unit.lower()
        if value is None:
            return 0
        if unit == "kb":
            return float(value) * 1000
        if unit == "mb":
            return float(value) * 1000000
        if unit == "gb":
            return float(value) * 1000000
    else:
        raise Exception("error formation %s", transform)
