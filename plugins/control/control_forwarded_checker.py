from handler.base_plugin import BasePlugin
from utils import traverse


class ForwardedCheckerPlugin(BasePlugin):
    __slots__ = ("allow_self", )

    def __init__(self, allow_self=False):
        """Checks messages' forwarded messages for commands."""
        super().__init__()

        self.allow_self = allow_self

    async def check_message(self, msg):
        if not self.allow_self:
            c = self.api.target_client

            if c.group:
                nid = self.api.vk_groups[c.target].group_id
            else:
                nid = self.api.vk_users[c.target].user_id

            if msg.user_id == nid:
                return False

        return not msg.is_out

    async def process_message(self, msg):
        try:
            await self.bot.handler.process(next(traverse(
                await msg.get_full_forwarded())))
        except StopIteration:
            pass
