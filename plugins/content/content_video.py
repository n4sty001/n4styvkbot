from handler.base_plugin import CommandPlugin
import random

class VideoPlugin(CommandPlugin):
    __slots__ = ()

    def __init__(self, *commands, prefixes=None, strict=False):
        """Plugin sending some videos by request."""

        if not commands:
            commands = ("видео", "видос")

        super().__init__(*commands, prefixes=prefixes, strict=strict)

        self.description = ["Видео",
            f"{self.command_example()} [запрос] - поиск видео по запросу"]

    async def process_message(self, msg):
        data = await self.api.video.search(
            q=self.parse_message(msg, full=True)[1] or "милый котик",
            sort=2,
            count=10,
            adult=0,
            offset= random.randint(1, 300)
        )

        if not data or not data.get("items"):
            return await msg.answer("Я не могу получить видео или ничего не нашлось!")

        return await msg.answer(
            'Приятного просмотра!',
            attachment=','.join(
                f"video{vid['owner_id']}_{vid['id']}"
                    for vid in data["items"]
            )
        )
