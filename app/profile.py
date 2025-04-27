from utils.constant import TEMPLATE_PROFILE

class ProfileApp:

    @staticmethod
    def get_profile() -> str:
        raw_profile: str = TEMPLATE_PROFILE
        return raw_profile
