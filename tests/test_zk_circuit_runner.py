import contextlib
import io
import tempfile
from pathlib import Path
from unittest import TestCase

from source.zk_circuit_runner import main


class ZKCircuitRunnerCLITests(TestCase):
    def test_cli_proves_and_verifies_polynomial_proof(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            proof_path = Path(temp_dir) / "proof.json"
            public_path = Path(temp_dir) / "public.json"

            prove_exit_code = _run_cli(
                [
                    "prove",
                    "circuits/inputs/polynomial_valid.json",
                    "circuits/main.wasm",
                    "circuits/main.groth16.zkey",
                    str(proof_path),
                    str(public_path),
                ]
            )

            self.assertEqual(prove_exit_code, 0)
            self.assertTrue(proof_path.exists())
            self.assertTrue(public_path.exists())

            verify_exit_code = _run_cli(
                [
                    "verify",
                    "circuits/main.groth16.vkey.json",
                    str(public_path),
                    str(proof_path),
                ]
            )

            self.assertEqual(verify_exit_code, 0)

    def test_cli_rejects_invalid_polynomial_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            proof_path = Path(temp_dir) / "proof.json"
            public_path = Path(temp_dir) / "public.json"

            prove_exit_code = _run_cli(
                [
                    "prove",
                    "circuits/inputs/polynomial_invalid.json",
                    "circuits/main.wasm",
                    "circuits/main.groth16.zkey",
                    str(proof_path),
                    str(public_path),
                ]
            )

            self.assertEqual(prove_exit_code, 2)
            self.assertFalse(proof_path.exists())
            self.assertFalse(public_path.exists())

    def test_cli_exports_verification_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            verification_key_path = Path(temp_dir) / "vkey.json"

            exit_code = _run_cli(
                [
                    "export-vkey",
                    "circuits/main.groth16.zkey",
                    str(verification_key_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(verification_key_path.exists())


def _run_cli(argv: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()):
        with contextlib.redirect_stderr(io.StringIO()):
            return main(argv)
