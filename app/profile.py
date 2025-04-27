from utils.constant import AUTHOR_PROFILE, DISCORD_BOT_REPO, BACKEND_REPO

class ProfileApp:

    @staticmethod
    def get_profile() -> str:
        raw_profile: str = f"""
            Hi, I'm mangoBot! I'm still in beta version! If you found any bug, please report to the owner!

            ## Basic Information
            - **Author**: [orangeMangoDimz]({AUTHOR_PROFILE})

            ## Support
            - Please give the repo star to support this bot 😊

            ## Links
            - [Discord Bot]({DISCORD_BOT_REPO})
            - [Server Repo]({BACKEND_REPO})
        """
        return raw_profile
