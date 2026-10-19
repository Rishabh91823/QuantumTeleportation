from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import math

app = Flask(__name__)
CORS(app) 

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/run-teleportation', methods=['POST'])
def run_teleportation():
    data = request.json
    theta = float(data.get('theta', 0))
    phi = float(data.get('phi', 0))

    qr = QuantumRegister(3, name="q")
    crz = ClassicalRegister(1, name="crz")
    crx = ClassicalRegister(1, name="crx")
    crb = ClassicalRegister(1, name="crb")
    qc = QuantumCircuit(qr, crz, crx, crb)
    qc.u(theta, phi, 0, 0)
    qc.h(1)
    qc.cx(1, 2)

    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, crz) 
    qc.measure(1, crx) 
    
    with qc.if_test((crx, 1)):
        qc.x(2)
    with qc.if_test((crz, 1)):
        qc.z(2)
        
    qc.measure(2, crb) 

    simulator = AerSimulator()
    transpiled_qc = transpile(qc, simulator)
    job = simulator.run(transpiled_qc, shots=1024)
    counts = job.result().get_counts()

    return jsonify({"success": True, "counts": counts})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
