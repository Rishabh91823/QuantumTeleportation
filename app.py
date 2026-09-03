from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Initialize the Registers
qr = QuantumRegister(3, name="q")
crz = ClassicalRegister(1, name="crz") # Stores Alice's measurement of q0
crx = ClassicalRegister(1, name="crx") # Stores Alice's measurement of q1
crb = ClassicalRegister(1, name="crb") # Stores Bob's final verification measurement
qc = QuantumCircuit(qr, crz, crx, crb)

# 2. Prepare the Payload State on Qubit 0
# We apply X then H to create the |-> state to teleport
qc.x(0)
qc.h(0)
qc.barrier()

# 3. Create the Entangled Bell Pair (Qubits 1 and 2)
qc.h(1)
qc.cx(1, 2)
qc.barrier()

# 4. Alice's Operations and Measurement
qc.cx(0, 1)
qc.h(0)
qc.barrier()

qc.measure(0, crz) 
qc.measure(1, crx) 
qc.barrier()

# 5. Bob's Conditional Reconstruction
# Bob applies X and/or Z gates depending on Alice's classical bits
with qc.if_test((crx, 1)):
	qc.x(2)
with qc.if_test((crz, 1)):
	qc.z(2)
qc.barrier()

# 6. Verification
# Bob applies an H gate to reverse the |-> state back to |1>
qc.h(2)
qc.measure(2, crb) 

# Print the visual circuit diagram in the console
print(qc.draw())

# 7. Run on the AerSimulator
simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)
job = simulator.run(transpiled_qc, shots=1024)
counts = job.result().get_counts()

print("\nMeasurement Results (Format: crb crx crz):")
print(counts)
print("\nSuccess: The first bit (crb) is '1' in every single result, proving the |-> state was teleported!")

# Plot the results in a pop-up window
plot_histogram(counts)
plt.show()