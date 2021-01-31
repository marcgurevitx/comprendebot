from botcommon.choosers.challengetype import challenge_type_chooser
from botcommon.modelbase import ModelBase


class Person(ModelBase):

    async def get_new_challenge(self):


        xxx = await challenge_type_chooser.async_pick(   None   )
        return xxx


        pass  # ?
