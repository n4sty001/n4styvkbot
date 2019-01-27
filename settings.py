from plugins import *  # Importing all the plugins from plugins/ folder
from settings_base import BaseSettings  # Importing base settings


class BotSettings(BaseSettings):
    # See README.md for details!
    USERS = (    
         ("user", "7c326a5e8fb63ab992ef373a21cae8a16deb5b32d413c2da290f19bb246e180f2207c04f12fc63a664154",),
    )

    # Default settings for plugins
    DEFAULTS["PREFIXES"] = DEFAULT_PREFIXES = ("/","@",)
    DEFAULTS["ADMINS"] = DEFAULT_ADMINS = (156530323, )

    # You can setup plugins any way you like. See plugins's classes and README.md.
    # All available plugins can be found in folder `plugins` or in file `PLUGINS.md`.
    # Bot will use all plugins inside PLUGINS variable.
    help_plugin = HelpPlugin("pomogi", "pojalysto", "netgiorp", prefixes=DEFAULT_PREFIXES)

    # List of active plugins
    PLUGINS = (
        StoragePlugin(in_memory=True, save_to_file=True),
        StaffControlPlugin(prefixes=DEFAULT_PREFIXES, admins=DEFAULT_ADMINS, set_admins=True),
        ChatMetaPlugin(),
        UserMetaPlugin(),
        StatisticsPlugin(),

        VoterPlugin(prefixes=DEFAULT_PREFIXES),
        FacePlugin("сделай", prefixes=DEFAULT_PREFIXES),
        SmileWritePlugin(),
        JokePlugin(),
        GraffitiPlugin(),
        QuoteDoerPlugin(),
        WikiPlugin(),
        AnagramsPlugin(),
        MembersPlugin(),
        PairPlugin(),
        WhoIsPlugin(),
        YandexNewsPlugin(),
        AboutPlugin(),
        BirthdayPlugin(),
        TimePlugin(),
        MemeDoerPlugin(),
        QRCodePlugin(),
        ChatKickerPlugin(admins_only=True),
        RandomPostPlugin({"папуг2": -174568284,
            "savehouse": -174568284, "octavia": -174568284}),
        CalculatorPlugin(),
        VideoPlugin(),
        DispatchPlugin(),
        NamerPlugin(),
        help_plugin,

        # Needs tokens (see plugin's codes, some have defaults):
        SayerPlugin(),

        # Plugins for bot's control
        AntifloodPlugin(),
        NoQueuePlugin(),
        CommandAttacherPlugin(),
        ForwardedCheckerPlugin(),
    )

    help_plugin.add_plugins(PLUGINS)
