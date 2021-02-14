from psycopg2.extras import Json
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

    def pop_sendables(self):
        rv = self.sendables[:]
        self.sendables.clear()
        return rv

    async def save_state(self):
        await self.challenge.update(
            state_code=self.state.name,
            #executor_data=???, Json( )?
        )

    async def next_variant_num(self):
        executor_data = self.challenge.row.executor_data
        nvariants = executor_data.get("nvariants", 0)
        variant_num = nvariants + 1
        executor_data["nvariants"] = nvariants + 1
        await self.challenge.update(executor_data=Json(executor_data))
        return variant_num
