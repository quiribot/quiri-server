from responds.group import Group, prefix, route

from .skills import Core


@prefix("/api")
class ApiGroup(Group):
    core = Core()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: add skills

    @route("/process", methods=('POST', ))
    async def search(self, ctx):
        data = ctx.request.get_data().decode('utf-8')
        res = await self.core.process(data, {})
        if not res:
            # TODO: regular search
            pass
        return res, 200
