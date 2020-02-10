# import maya.cmds as mc
# import os
#
# def renameAssets(curr_name, curr_sufix, new_suffix, separator = "_"):
#     temp = curr_name.split(separator)
#     newtemp = [t.replace(curr_sufix, new_suffix) for t in temp]
#
#     result = separator.join(newtemp)
#     return result