from botcommon.choosers.challengetype import challenge_type_chooser
from botcommon.modelbase import ModelBase


class Person(ModelBase):

    async def get_new_challenge(self):


        challenge_type = await challenge_type_chooser.async_pick({
            "person_xp": self.row.xp,
        })
        return challenge_type


        pass  # ?
