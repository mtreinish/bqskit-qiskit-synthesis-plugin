# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from bqskit import synthesize_for_qiskit
from qiskit.transpiler.passes.synthesis import plugin
from qiskit.converters import circuit_to_dag
from qiskit.circuit import QuantumCircuit
from qiskit.extensions.quantum_initializer import isometry

"""A unitary synthesis plugin for using BQSKit."""


class BqskitSynthesisPlugin(plugin.UnitarySynthesisPlugin):

    @property
    def supports_basis_gates(self):
        return True

    @property
    def supports_coupling_map(self):
        return True

    @property
    def supports_approximation_degree(self):
        return False

    def run(self, unitary, **options):
        cmap = options['coupling_map']
        basis = options['basis_gates']
        qubits = options['qubits']
        if unitary.shape <= (5, 5) or unitary.shape > (2, 2):
            cg = None
            if cmap is not None and qubits is not None:
                cg = list(
                    cmap.subgraph(qubits).get_edges())
            synth_out = synthesize_for_qiskit(unitary,
                                              basis_gates=basis,
                                              coupling_graph=cg)
            synth_dag = circuit_to_dag(QuantumCircuit.from_qasm_str(synth_out))
        else:
            synth_dag = circuit_to_dag(
                isometry.Isometry(unitary, 0, 0).definition)
        return synth_dag
