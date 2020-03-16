##### Author: Pierre LIENHART
##### Contact: pierre.lienhart@gmail.com

# Datadog data science homework - Problem 1

## Execution environment
To ensure our notebook runs using the appropriate dependencies and that its results are reproducible, we first create 
and activate a dedicated Python (virtual) execution environment using the problem's  *requirements.txt* file. Change 
your current directory to the problem's directory and run the following commands:

```bash
conda create -y -c conda-forge -n py36-problem-1 --file requirements.txt
conda activate problem-1
```

We now need to create a Jupyter kernel for this execution environment using the following command:

```bash
python -m ipykernel install --user --name=py36-problem-1
```

Now our dedicated execution environment is available in the list of Jupyter kernels. The notebook associated with 
Problem 1 can be safely run using this kernel. You can now start a Jupyter Notebook server using the following command:

```bash 
jupyter notebook
```

