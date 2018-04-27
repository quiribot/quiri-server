from responds.group import Group, prefix, route

from .skills import Core
from .skills.util import error, get_skills


@prefix("/api")
class ApiGroup(Group):
    core = Core()

    def __init__(self, skills_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for skill in get_skills(skills_dir):
            self.core.add_skill(skill)
        # TODO: add skills

    @route("/process", methods=('POST', ))
    async def search(self, ctx):
        q = ctx.request.args.get("q")
        if not q:
            return error("Please send a q query string argument", code=400)
        res = await self.core.process(q, {})
        if not res:
            # TODO: regular search
            # TODO: is 404 okay?
            return error("No response", code=404)
        return res, 200
