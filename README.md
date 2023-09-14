## NCSA-WEST: NCSA-Workshop on Exascale Simulation Technologies

Are you frustrated that high-performance tools require effort proportional to the number of target machines TIMES the number of workloads? Come see what CEESD (https://ceesd.illinois.edu/) has developed to address this problem. CEESD is a DOE-funded center working to experimentally and computationally understand scramjets (supersonic combustion air-breathing jet engines), and is developing and using these tools to do so. 

**Synopsis:**  This workshop will provide a hands-on view of two new technologies: MIRGE and Parsl.  Hear about the latest developments, try out the tools, and initiate collaborations.
​​​​
MIRGE (https://github.com/illinois-ceesd/mirgecom/wiki/MIRGE) addresses the question: "Can high-level numpy-based numerical code yield credibly high performance workloads, across CPUs and GPUs?" It’s a framework for designing and executing array-based scientific applications by leveraging a dataflow graph.  Codes are written in Python, but execute seamlessly on HPC resources with accelerators.

Parsl (https://parsl-project.org) enables users to create parallel programs that glue together Python functions and/or external components, including compiled programs. Parsl programs can be executed on any compute resource from laptops to supercomputers. This leads to rapid testing and execution on a range of HPC resources.

**Goal:** This workshop aims to showcase these technologies, to identify challenges in exascale computing, and to initiate further collaborations with researchers at NCSA and across campus.

**Where:** NCSA 1030

**When:** Friday September 15, 2023, 9am – noon.

**What to bring:** a laptop and optionally your own Python-based application

**What to do beforehand:** to participate in the Parsl hands-on example, you need to register at https://identity.ncsa.illinois.edu/join/XWAH2MWFC9  If you have NCSA credentials, you can use them to log in; if not, click the “Register as New User and Join” link (be sure to check your email as you will need to confirm your new user identity).

**Schedule:**

```
 900– 915: Brief Introduction, overview (Luke Olson, Bill Gropp)
 915- 930: MIRGE: conceptual overview   (Andreas Klöckner)
 930–1000: MIRGE: hands-on example      (with CEESD developers)
1000-1015: break
1015-1030: Parsl: conceptual overview   (Dan Katz, Doug Friedel)
1030–1100: Parsl: hands-on example      (with CEESD developers)
1100-1200: Bring your own code (optional)
```

## Materials for MIRGE Demo

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/illinois-ceesd/NCSA-WEST/HEAD)
