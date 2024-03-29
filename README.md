# Anonymization Of Social Networks
This repository is the codebase for an anonymzation tool that we have created. A prospective user can use this for implementing anonymization for social networks using different methods, privacy measures, centralities etc. A prospective user can also use this code base to anonymize social networks with multiple sensitive labels.

## Codebase structure

* [data](data): The 4 primary datasets used for testing. All the data for this project is in gml format. Any additional data that you add must be stored here.
  * [misc](data/misc) Other datasets
* [docs](docs): Required documentation for the codebase. Here, important files are the <strong>Complete_Summary.csv</strong> that consists of all the data and plots and <strong>Final Report</strong>.
* [src](src): The 4 primary datasets used for testing 
* [test](test) Test cases and their outputs
  * [algorithm_testing](test/algorithm_testing): Folder to run all the tests from. It consists of some default usecases that we used for testing that a user can run (and change). It also consists of user_test.py file which when executed a user can try out on their own social network.
  * [outputs_images](test/ouputs_images) Some important output images obtained from test cases.


## Software Requirements
The project requries python3. We suggest use of Anaconda https://www.anaconda.com/.  
There are few important external libraries that a user needs to install, outside of the base libraries that Anaconda uses.

| Library | Description |
| ---- | --- |
| [**Networkx**](https://networkx.github.io/) | NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks. Codebase uses this extensively |
| [**Matplotlib**](https://matplotlib.org/) | Python plotting function we used to plot networkx |
| [**Pandas**](https://pandas.pydata.org/) | To help with saving data and CSV  |
| [**Psutil**](https://psutil.readthedocs.io/en/latest/) | Codebase uses it for finding memory utilization during runtime.


## To develop the Anonymization tool on your own machine
1. Clone the project:
```
git clone https://github.com/dhruvchamania/TSE_Final_Project.git
```
2. Go to the algorithm_testing folder:
### All the code runs from this folder.
```
cd TSE_Final_Project\test\algorithm_testing
```

3. Run the already present test cases:  

```
python test6.py
or
python edge_ms.py
```  
4. Run test cases where you want to choose your own social netowrk or if you want to make a graph on your own and test. There are many options available to run this.
```
python user_test.py
```  

<strong>Additional Detail is available in our wiki page.</strong>

