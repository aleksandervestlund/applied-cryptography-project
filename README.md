# Applied Cryptography Project

## Setup

Install the Python dependencies you need for development:

```bash
pip install -r requirements/dev.txt
```

This project uses `snarkjs` as a local Node development dependency for
Groth16 proving and verification. Install Node.js 18 or newer, then install
the local npm dependencies:

```bash
npm install
```

Check that the local `snarkjs` CLI is available:

```bash
npx --no-install snarkjs --help
```

## ZK Proof Helpers

The Python wrapper lives in `source/zk_circuit_runner.py`. It calls the
repo-local `snarkjs` CLI through `npx --no-install`, so it will use the
version pinned in `package-lock.json`.

## Example Circuit

The repo includes `circuits/polynomial.circom`, a simple arithmetic proof:

```circom
pragma circom 2.1.6;

template Polynomial() {
    signal input x;
    signal input y;

    y === x * x + 3 * x + 5;
}

component main { public [y] } = Polynomial();
```

This proves knowledge of a private `x` such that public `y = x^2 + 3x + 5`.
For `circuits/inputs/polynomial_valid.json`, the prover knows `x = 9` and
claims public `y = 113`.

Use zkrepl or a local Circom setup to compile `circuits/polynomial.circom` and
generate these artifacts:

```text
circuits/artifacts/polynomial.wasm
circuits/artifacts/polynomial.zkey
circuits/artifacts/polynomial.vkey.json
```

Then generate and verify a proof with the Python wrapper:

```python
from pathlib import Path

from source.zk_circuit_runner import prove_groth16, verify_groth16


prove_groth16(
    input_path=Path("circuits/inputs/polynomial_valid.json"),
    wasm_path=Path("circuits/artifacts/polynomial.wasm"),
    zkey_path=Path("circuits/artifacts/polynomial.zkey"),
    proof_path=Path("circuits/artifacts/polynomial_proof.json"),
    public_path=Path("circuits/artifacts/polynomial_public.json"),
)

is_valid = verify_groth16(
    verification_key_path=Path("circuits/artifacts/polynomial.vkey.json"),
    public_path=Path("circuits/artifacts/polynomial_public.json"),
    proof_path=Path("circuits/artifacts/polynomial_proof.json"),
)
```

Or run the same flow through the command line:

```bash
python3 -m source.zk_circuit_runner prove \
  circuits/inputs/polynomial_valid.json \
  circuits/artifacts/polynomial.wasm \
  circuits/artifacts/polynomial.zkey \
  circuits/artifacts/polynomial_proof.json \
  circuits/artifacts/polynomial_public.json

python3 -m source.zk_circuit_runner verify \
  circuits/artifacts/polynomial.vkey.json \
  circuits/artifacts/polynomial_public.json \
  circuits/artifacts/polynomial_proof.json
```

Generate a Groth16 proof:

```python
from pathlib import Path

from source.zk_circuit_runner import prove_groth16


prove_groth16(
    input_path=Path("circuits/artifacts/input.json"),
    wasm_path=Path("circuits/artifacts/shot.wasm"),
    zkey_path=Path("circuits/artifacts/shot.zkey"),
    proof_path=Path("circuits/artifacts/proof.json"),
    public_path=Path("circuits/artifacts/public.json"),
)
```

Verify a Groth16 proof:

```python
from pathlib import Path

from source.zk_circuit_runner import verify_groth16


is_valid = verify_groth16(
    verification_key_path=Path("circuits/artifacts/shot.vkey.json"),
    public_path=Path("circuits/artifacts/public.json"),
    proof_path=Path("circuits/artifacts/proof.json"),
)
```

The prover needs the compiled circuit `.wasm`, the proving key `.zkey`, and
the private/public input JSON. The verifier needs only the verification key
JSON, public inputs, and proof JSON.
