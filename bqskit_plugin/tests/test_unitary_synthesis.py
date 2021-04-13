# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Tests for the UnitarySynthesis transpiler pass.
"""

from ddt import ddt, data

import numpy as np

from qiskit.test import QiskitTestCase
from qiskit.circuit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.transpiler.passes import UnitarySynthesis
from qiskit.transpiler import CouplingMap
from qiskit.quantum_info.operators import Operator
from qiskit.quantum_info.random import random_unitary
from qiskit import transpile


@ddt
class TestUnitarySynthesis(QiskitTestCase):
    """Test UnitarySynthesis pass."""

    @data(
        ['u3', 'rx', 'rz', 'cz', 'iswap'],
    )
    def test_two_qubit_synthesis_to_basis(self, basis_gates):
        """Verify two qubit unitaries are synthesized to match basis gates."""
        ghz = QuantumCircuit(3)
        ghz.h(0)
        ghz.cx(0, 1)
        ghz.cx(0, 2)
        ghz_op = Operator(ghz)

        qc = QuantumCircuit(3)
        qc.unitary(ghz_op, [0, 1, 2])
        dag = circuit_to_dag(qc)

        out = UnitarySynthesis(basis_gates, method='bqskit').run(dag)
        self.assertTrue(set(out.count_ops()).issubset(basis_gates))

    def test_random_unitary(self):
        cmap = CouplingMap.from_ring(5)
        unitary = random_unitary(32)
        qc = QuantumCircuit(5)
        qc.unitary(unitary, [0, 1, 2, 3, 4])
        tqc = transpile(qc, basis_gates=['cx', 'rz', 'sx', 'x', 'id'],
                        coupling_map=cmap,
                        unitary_synthesis_method='bqskit')
        print(Operator(tqc))
        print(unitary)
        self.assertTrue(np.isclose(unitary, Operator(tqc)).all())
