## CatalysisIE based Knowledge Graph Generator
Repository for the publication "Generating knowledge graphs through text mining of catalysis research related literature". 
The two Excel-files listing the output of the queries as described in the publication are contained in the [output](./output/) folder

The tool consists following modules: preprocess_onto.py, txt_extract.py, text_mining.py, onto_extension.py also there are jupyter notebook with SPARQL queries examples and functions for querying the ontology depending on the information of interest. 

### Preparations
Before starting the code, some preparations must be done:
-	Folder structure must be the following:

```bash
main_folder
├── import
├── ontologies
├── ontology_snipet
├── CatalysisIE
├── PDFDataExtractor
├── robot
├── output
└── classlist
```
 	
-	The ontology to be extended must be stored in the “ontologies” folder
-	The following modules need to be installed/placed here:
	-	Pytorch version 1.8.0 and cuda toolkit version 11.1
	-	Clone the CatalysisIE (https://github.com/nsndimt/CatalysisIE) repository and download their checkpoints if needed
	-	Robot command line tool (http://robot.obolibrary.org/)
	-	PDFDataExtractor (https://pdfdataextractor.readthedocs.io/en/latest/getting_started/installation.html)
	- 	More details regarding modules listed in [cat_environment.yml](./envs/cat_environment.yml) and [cat_environment.txt](./envs/cat_environment.txt)

-	Global variables listed in config.json must be adjusted for the process

### CatalysisIE Checkpoint
The checkpoint of the extended CatalysisIE model is found here:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12634956.svg)](https://doi.org/10.5281/zenodo.12634956)


### Usage

1. Execute `create_ChEBIdict.py` to create a dictionary of all ChEBI classes for later entity recognition (might take some time)
2. Place PDFs in folder import 
3. Make sure a model for 
3. Insert your Scopus API key in `config.json` and adjust other settings where necessary
4. Execute `run_pdfs.py` (this uses modules `txt_extract.py`, `text_mining.py`, `preprocess_onto.py`, and `onto_extension.py` and stores resulting knowledge graph in [ontologies](./ontologies/))
5. Execute the jupyter notebook `user_queries.ipynb` for predefined queries on the resulting knowledge graph


### Remarks
The directory [labeling](./labeling/) contains json files exported from labelStudio for the labeling of abstracts of both the methanation and hydroformylation datasets.
Furthermore, this directory contains the resulting labeling of the models and the performances of the models.

