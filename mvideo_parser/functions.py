
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_random_user_agent():
    from random_user_agent.user_agent import UserAgent
    from random_user_agent.params import SoftwareName, OperatingSystem


    # you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
    # you can also set number of user agents required by providing `limit` as parameter

    software_names = [SoftwareName.ANDROID.value]

    user_agent_rotator = UserAgent(software_names=software_names, limit=5)

    # Get list of user agents.
    user_agents = user_agent_rotator.get_user_agents()

    # Get Random User Agent String.
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent
