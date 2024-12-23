# Data Files Documentation

In this directory are all the files necessary for the use of the algorithms in `/src`.

In order for the scripts to work correctly, the .dat must be constructing using the corresponding parameters and format. This can be done through the use of the TroublemakerR **R** library, documentation at https://cran.r-project.org/web/packages/TroublemakeR/TroublemakeR.pdf.

---

### **RegionProblems.zip**
Contains all the necessary information about the variables and restrictions of the problem or subproblem to solve, stored as `.dat` files. It uses the same format as the original files.

- **Note**: Due to the size of the files, they must be compressed to upload to the repository. Adding the names of the files to `.gitignore` should allow you to extract the files without encountering issues with GitHub.

---

### **municip_keys.csv**
To improve performance, the code uses numerical IDs for each municipality instead of their names. This file provides a key to map municipality names to their IDs.

**Format**:
```
municipality_name,municipality_id
```

**Example**:
```
Viborg,95
Vordingborg,96
Ærø,97
Århus,98
```

---

### **municip_neighbors.txt**
This file contains the list of adjacent municipalities (neighbors) for each municipality.

**Format**:
```
municipality_id;neighbor_id_1,neighbor_id_2,...
```

- If a municipality is isolated (i.e., has no neighbors), the corresponding line is:
  ```
  municipality_id;
  ```

- **Special Case**: The neighbors for Christiansø and Frederiksberg could not be recovered. These municipalities are marked as isolated due to their minimal impact on the problem.

**Example**:
```
12;72,2,22,23,3,5,42
13;89,91,30,92
14;48,84,4,66,63
15;
```

---

### **cell_ids.csv**
This file maps each cell in the problem to the municipality it belongs to.

Each line contains a cell ID and its corresponding municipality ID, separated by a comma:

```
cell_id,municipality_id
```

**Example**:
```
446996,21
446997,21
449068,37
449069,37
```

---


