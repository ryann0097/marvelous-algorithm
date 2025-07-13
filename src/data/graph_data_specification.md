# Data Specification

There are few graphs that are used for scheduling benchmarking. It's important to mention about the data specification.
Well, let's start to breakdown:

## Filename pattern:

<workflow_name>_Nodes_<number_of_graph_edges>_CCR_<CCR>.gxl

- **workflow_name**: Name of the scientific workflow.
- **Nodes**> Number of tasks (nodes/vertices) in the graph.
- **CCR**: Communication to Computation Ratio (explained below).

--- 

## Workflow Descriptions

These workflows represent real-world scientific application commonly used in optmization and scheduling research.

- **CyberShake**: used in sysmic risk analysis.
- **Inspiral**: related to physics and gravitational waves detection.
- **Montage**: used in astronomic images montage.
- **Sipht**: used in chemical processes analysis.

--- 

## Params

### Nodes 

The number of tasks, or, as you prefer to call, the number of vertexes that the graph contains.

- 50
- 100
- 200

### CCR (Communication to Computation Ratio): 

At multiprocessor architetures, it's normal to see this type of parameter. This means the ratio between the medium cost between tasks and the makespan of the task.

- Low values: indicates low communication related to the computation, more independent tasks;
- High values: indicates expensive communication, tasks with more dependency among them.

--- 

## Available Graph Files

The graphs we have at the folder 'data':

- CyberShake_Nodes_200_CCR_0.1.gxl
- CyberShake_Nodes_50_CCR_10.0.gxl
- CyberShake_Nodes_50_CCR_1.0.gxl
- Inspiral_Nodes_100_CCR_0.1.gxl
- Inspiral_Nodes_100_CCR_10.0.gxl
- Inspiral_Nodes_200_CCR_0.1.gxl
- Inspiral_Nodes_50_CCR_1.0.gxl
- Montage_Nodes_100_CCR_0.1.gxl	
- Montage_Nodes_200_CCR_0.1.gxl
- Montage_Nodes_200_CCR_10.0.gxl
- Sipht_Nodes_100_CCR_10.0.gxl
- Sipht_Nodes_100_CCR_1.0.gxl
- Sipht_Nodes_200_CCR_0.1.gxl
- Sipht_Nodes_50_CCR_0.1.gxl
- Sipht_Nodes_50_CCR_1.0.gxl

