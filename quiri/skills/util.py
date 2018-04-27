import imp
import os
from os.path import isdir, join, splitext

from . import Answer


def error(message: str, code: int = 400):
    answer = Answer().set_error(message, code)
    return answer.build(None, 0), code


def _create_skill_registrant(name, skills_dir):
    loc = join(skills_dir, name)
    if isdir(loc) and "__init__.py" not in os.listdir(loc):
        return None
    if isdir(loc):
        modname = "__init__"
        path = [loc]
    else:
        modname = splitext(name)[0]
        path = [skills_dir]
    try:
        (f, pathname, desc) = imp.find_module(modname, path)
        skill = imp.load_module(modname, f, pathname, desc)
    except ImportError:
        return None

    return getattr(skill, "register", None)


def get_skills(skills_dir):
    skills = []
    possible_skills = os.listdir(skills_dir)
    for p in possible_skills:
        register = _create_skill_registrant(p, skills_dir)
        if register:
            register(skills.append)
    return skills
