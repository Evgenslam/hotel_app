from inspect import  signature

# def create_dict_from_args(*args, **kwargs):
#     func_signature = signature(create_dict_from_args)
#     param_names = [param.name for param in func_signature.parameters.values()]
#
#     # Construct a dictionary from positional arguments
#     args_dict = dict(zip(param_names, args))
#
#     # Combine with keyword arguments
#     args_dict.update(kwargs)
#
#     return args_dict
#
# print(signature(get_hotels))