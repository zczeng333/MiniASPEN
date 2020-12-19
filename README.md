Documentation
=============
**General Description:**

This project provides solutions to several crucial problems in PSE

Project mainly includes three parts:
1. common utils for project
2. system decomposition utils
3. system tearing utils

Dependencies
-------------
**Language:**  python 3.x

package             | version       
------------------- | --------------
*numpy*|1.18.2
*pandas*|1.1.5
*scipy*|1.5.3


**Interpreter:**  python 3.x

Project Architecture
-------------
```buildoutcfg
│  main.py      // main function
│  README.md    // help
│
├─.idea
│  │  .gitignore
│  │  encodings.xml
│  │  MiniASPEN.iml
│  │  misc.xml
│  │  modules.xml
│  │  vcs.xml
│  │  workspace-Surface-Zhichen.xml
│  │  workspace.xml
│  │
│  └─inspectionProfiles
│          profiles_settings.xml
│
├─common            // common utils
│  │  Graph.py      // graph class
│  │  Sys2Graph.py  // convert system to graph representation
│  │  Sys2Matrix.py // convert system to matrix representation
│  │  __init__.py   // initilization function for common utils
│  │
│  └─__pycache__
│          Graph.cpython-37.pyc
│          Sys2Graph.cpython-37.pyc
│          Sys2Matrix.cpython-37.pyc
│          __init__.cpython-37.pyc
│
├─decompose                 // system decomposition utils
│  │  Decompose.py          // decomposition class
│  │  EqSolver.py           // equation solver class
│  │  OutputSelection.py    // select optimal output variables for equations
│  │  __init__.py           // initialization function for decomposition utils
│  │
│  └─__pycache__
│          Decompose.cpython-37.pyc
│          EqSolver.cpython-37.pyc
│          OutputSelection.cpython-37.pyc
│          __init__.cpython-37.pyc
│
└─tear  // system tear utils
   │  IntProg.py    // integer programming class
   │  TearSolver.py // system tearing solver class
   │  __init__.py   // initialization function for system tearing utils
   │
   └─__pycache__
           IntProg.cpython-37.pyc
           TearSolver.cpython-37.pyc
           __init__.cpython-37.pyc
```

Usage
-------------
Directly run main.py to start

Implement your own examples (to be continued...)