##### Author: Pierre LIENHART
##### Contact: pierre.lienhart@gmail.com

# Datadog data science homework - Problem 1

## Execution environment
This notebook has been developed using [Jupyter](https://jupyter.org/) (version 4.4.0) and [`conda`](https://docs.conda.io/en/latest/) 
package manager (version 4.6.11). To ensure our notebook runs using the appropriate dependencies and that its results are
reproducible, we first create and activate a dedicated Python (virtual) execution environment using the problem's 
*requirements.txt* file and the following commands:

```bash
conda create -y -c conda-forge -n <env-friendly-name> --file </path/to/requirements.txt>
conda activate <env-friendly-name>
```

We now need to create a Jupyter kernel for this execution environment using the following command:

```bash
python -m ipykernel install --user --name=<kernel-friendly-name>
```

Now our dedicated execution environment is available in the list of Jupyter kernels. The notebook associated with 
Problem 1 can be safely run using this kernel. 

