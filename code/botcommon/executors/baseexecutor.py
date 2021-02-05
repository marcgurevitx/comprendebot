from transitions.extensions.asyncio import AsyncMachine


class BaseExecutor:
    states = None
    initial = None
    transitions = None

    def __init__(self, challenge):
        self.challenge = challenge
        self.sendables = []
        self.machine = self._get_machine()
        if self.challenge.row.state_code:
            self.machine.set_state(self.challenge.row.state_code)

    def _get_machine(self):
        assert self.states
        assert self.initial
        assert self.transitions
        machine = AsyncMachine(
            model=self,
            states=self.states,
            initial=self.initial,
            transitions=self.transitions,
        )
        return machine

    def dump_sendables(self):
        for sendable in self.sendables:
            yield sendable
        self.sendables = []

    async def save_state(self):
        await self.challenge.update(
            state_code=self.state.name,
            #executor_data=???, Json( )?
        )
