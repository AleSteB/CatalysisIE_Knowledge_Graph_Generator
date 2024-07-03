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
└── classlist
```
 	
-	The ontology to be extended must be stored in the “ontologies” folder
-	The following modules need to be installed/placed here:
	-	Pytorch version 1.8.0 and cuda toolkit version 11.1
	-	CatalysisIE (https://github.com/nsndimt/CatalysisIE)
	-	Robot command line tool (http://robot.obolibrary.org/)
	-	PDFDataExtractor (https://pdfdataextractor.readthedocs.io/en/latest/getting_started/installation.html)
	- 	More details regarding modules listed in [cat_environment.yml](./cat_environment.yml) and [cat_environment.txt](./cat_environment.txt)

-	Global variables listed in config.json must be adjusted for the process


## MODEL

### Usage

1. Execute `create_ChEBIdict.py` to create a dictionary of all ChEBI classes for later entity recognition (might take some time)
2. Place PDFs in folder import 
3. Check `config.json` and adjust settings where necessary
4. Execute `run_pdfs.py` (this uses modules `txt_extract.py`, `text_mining`, `preprocess_onto`, and `onto_extension`)


