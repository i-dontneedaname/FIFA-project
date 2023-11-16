def delete_none_values_from_dict(data: dict):
    # del_keys = [k for k in data.keys() if data[k] is None]
    #
    # for key in del_keys:
    #     del data[key]
    #
    # return data

    return {k: v for k, v in data.items() if v is not None}
