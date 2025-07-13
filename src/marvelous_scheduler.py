from saga.scheduler import Scheduler, Task
import networkx as nx
import marvelous_algorithm as ma
from typing import Dict, Hashable, List, Tuple

"""
MarvelousScheduler implements a task scheduling algorithm based on a customized strategy 
that seeks to maximize parallelism by matching independent tasks for concurrent execution.

Main Features:
--------------
- Applies a preprocessing step to ensure the task graph is acyclic (using `ma.deciclify`).
- Schedules tasks over a set of heterogeneous processors, each potentially having different execution speeds.
- Identifies sets of independent, ready-to-run tasks and applies maximum matching (via `ma.matching_ready_tasks`) 
  to determine which pairs of tasks can be executed in parallel.
- Prioritizes tasks with no dependencies and schedules remaining tasks based on processor availability and readiness.

Workflow:
---------
1. Preprocessing:
    - The input task graph (DAG) is cleaned of cycles using the `deciclify()` function to ensure valid scheduling.

2. Initialization:
    - Processor list and counters are initialized.
    - Execution times are derived from the "weight" attribute of each task node.
    - Tasks without predecessors (in-degree 0) are marked as ready.

3. Main scheduling loop:
    - Events in the execution queue are handled in time order (`queue.sort()`).
    - Finished tasks are marked and their successors are checked for readiness.
    - A list of currently executable (pendent) tasks is built.
    - Tasks are matched in pairs via a co-comparability graph and maximum matching.
    - Matched tasks are assigned to the two processors with earliest availability.
    - Remaining tasks are scheduled one by one to the next available processor.

4. Final step:
    - Constructs a schedule dictionary mapping each processor to a list of `Task` objects with assigned start and end times.

Assumptions:
------------
- Each task node in the task graph has a "weight" attribute representing execution cost.
- Each processor node in the processor network has a "weight" attribute representing speed (default: 1.0).
- The graph is a valid DAG after preprocessing.
- The number of processors is ≥ 2.

Returns:
--------
Dict[Hashable, List[Task]]: A mapping from processor names to lists of scheduled Task objects, each with:
    - name: Task identifier
    - start: Start time
    - end: Completion time
    - node: Processor identifier

Dependencies:
-------------
- networkx for graph structures and algorithms
- marvelous_algorithm (contains deciclify and matching_ready_tasks)
- saga.scheduler.Scheduler and saga.scheduler.Task (base classes)

"""


class MarvelousScheduler(Scheduler):
    @staticmethod
    def pre_processing(task_graph: nx.DiGraph):
        task_graph = ma.deciclify(task_graph, list(task_graph.nodes)[0])
        return task_graph

    def schedule(self, network: nx.Graph, task_graph: nx.DiGraph) -> Dict[Hashable, List[Task]]:
        proc_list = list(network.nodes)
        num_procs = len(proc_list)

        task_graph = self.pre_processing(task_graph)

        execution_time = {
            node: task_graph.nodes[node]["weight"]
            for node in task_graph.nodes
        }

        global_time = 0
        processors = [0] * num_procs
        processed = set()
        queue = []

        start = {}
        end = {}
        alloc = {}
        pendent_tasks = set()

        """
        As primeiras tarefas que serão executadas são as que não tem nenhum precedente,
        ou seja: não tem nenhuma tarefa que a antecede. Essas são as tarefas independentes.
        """
        for node in task_graph.nodes:
            if task_graph.in_degree(node) == 0:
                pendent_tasks.add(node)

        """
        Processamento comum das tarefas, baseando-se em um esquema de fila padrão, como
        ocorre em processadores normais.
        """

        while len(processed) < len(task_graph.nodes):
            queue.sort()
            while queue and queue[0][0] <= global_time:
                end_task, task, p_idx = queue.pop(0)
                processed.add(task)
                processors[p_idx] = end_task
                for successor in task_graph.successors(task):
                    if all(pred in processed for pred in task_graph.predecessors(successor)):
                        pendent_tasks.add(successor)

            tasks_to_execute = list(pendent_tasks)
            used_tasks = set()

            """
            Aqui está a mágica do escalonamento:
            é feito um matching com as tarefas que podem ser paralelizáveis
            para encontrar o máximo paralelismo. Se uma tarefa for executável
            e seu par no matching também é capaz de ser executável, começamos a processar as duas.
            Isso quer dizer que são paralelizáveis.
            """

            matching = ma.matching_ready_tasks(task_graph, tasks_to_execute)
            for u, v in matching:
                available = sorted((t, i) for i, t in enumerate(processors))
                p1_idx, p2_idx = available[0][1], available[1][1]
                p1_name, p2_name = proc_list[p1_idx], proc_list[p2_idx]

                start[u] = global_time
                speed_1 = network.nodes[p1_name].get("weight", 1.0)
                end[u] = global_time + execution_time[u] / speed_1
                alloc[u] = p1_idx
                queue.append((end[u], u, p1_idx))

                start[v] = global_time
                speed_2 = network.nodes[p2_name].get("weight", 1.0)
                end[v] = global_time + execution_time[v] / speed_2
                alloc[v] = p2_idx
                queue.append((end[v], v, p2_idx))

                used_tasks.update([u, v])

            """
            As tarefas que tem dependências são executadas ao final, pois é entedido
            que todas as suas predecessoras já foram executadas com sucesso.
            """

            for task in tasks_to_execute:
                if task in used_tasks:
                    continue
                p_idx = processors.index(min(processors))
                p_name = proc_list[p_idx]

                start[task] = global_time
                speed = network.nodes[p_name].get("weight", 1.0)
                end[task] = global_time + execution_time[task] / speed
                alloc[task] = p_idx
                queue.append((end[task], task, p_idx))
                used_tasks.add(task)

            pendent_tasks -= used_tasks

            if queue:
                global_time = min(evt[0] for evt in queue)
            else:
                break

        schedule: Dict[Hashable, List[Task]] = {proc_name: [] for proc_name in proc_list}
        for task in task_graph.nodes:
            p_idx = alloc[task]
            p_name = proc_list[p_idx]
            t = Task(node=p_name, name=task, start=start[task], end=end[task])
            schedule[p_name].append(t)

        return schedule
