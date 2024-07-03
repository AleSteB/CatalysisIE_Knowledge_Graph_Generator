The tool consists following modules: preprocess_onto.py, txt_extract.py, text_mining.py, onto_extension.py also there are jupyter notebook with SPARQL queries examples and functions for querying the ontology depending on the information of interest. 
Before starting the code, some preparations must be done:
-	Folder structure must have the following:

```bash
main_folder
├── import
├── ontologies
├── ontology_snipet
└── classlist
```
 	
-	The ontology to be extended must be stored in the “ontologies” folder;
-	The following modules need to be installed/placed here:
	-	Pytorch version 1.8.0 and cuda toolkit version 11.1
	-	CatalysisIE (https://github.com/nsndimt/CatalysisIE)
	-	Robot command line tool (http://robot.obolibrary.org/)
	-	PDFDataExtractor (https://pdfdataextractor.readthedocs.io/en/latest/getting_started/installation.html)
-	Global variables listed in config.json must be adjusted for the process.

- Tables listing the output of the queries as described in the paper are listed in the [output](./output/) folder
