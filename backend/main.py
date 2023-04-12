#!/usr/bin/env python3

# based on https://github.com/golemfactory/yapapi/blob/0.10.0/examples/hello-world/hello.py

from typing import AsyncIterable

from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm

from fastapi import FastAPI


async def golem_worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script = context.new_script()
        future_result = script.run("/bin/sh", "-c", "date")
        yield script
        task.accept_result(result=await future_result)


async def run_on_golem() -> str:
    package = await vm.repo(
        image_hash="d646d7b93083d817846c2ae5c62c72ca0507782385a2e29291a3d376",
    )
    tasks = [Task(data=None)]
    result = None
    async with Golem(budget=1.0, subnet_tag="public") as golem:
        async for completed in golem.execute_tasks(golem_worker, tasks, payload=package):
            # do not return from here, because golem throws CancelledError
            result = completed.result.stdout
    return result


enable_default_logger()

app = FastAPI()

@app.get("/api/date/")
async def root():
    return await run_on_golem()
