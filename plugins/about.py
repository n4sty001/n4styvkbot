from handler.base_plugin import CommandPlugin


class AboutPlugin(CommandPlugin):
    __slots__ = ("version", )

    def __init__(self, *commands, prefixes=None, strict=False, version=8.0):
        """Answers with information about bot."""

        if not commands:
            commands= ("alive",)

        super().__init__(*commands, prefixes=prefixes, strict=strict)

        self.version = version

        self.description = (
            "О боте",
            "Вывод информации о боте.",
            f"{self.command_example()} - вывести информацию."
        )

    async def process_message(self, msg):
        message = "Жив"
                      
        return await msg.answer(message)
