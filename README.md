# BQSKit Qiskit Unitary Synthesis plugin

This repository contains a PoC unitary synthesis plugin for Qiskit. Currently
it depends on the in progress qiskit pull request:

https://github.com/Qiskit/qiskit-terra/pull/6124

## Install and Use plugin

To use the unitary synthesis plugin first install qiskit terra with the pull
request:
```bash
pip install git+https://github.com/mtreinish/qiskit-core@synthesis-plugins
```

and then install this plugin package by running from the root of this repo:

```bash
pip install .
```

This will install the plugin and qiskit will automatically detect it at runtime.
You can then opt-in to using the bqskit plugin by using the transpile kwarg,
`unitary_synthesis_method`. For example:

```python
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.quantum_info.random import random_unitary
from qiskit.test.mock import FakeLima

unitary = random_unitary(32)
backend = FakeLima()
qc = QuantumCircuit(5)
qc.unitary(unitary, [0, 1, 2, 3, 4])
tqc = transpile(qc, backend, unitary_synthesis_method='bqskit')
print(tqc)
```
