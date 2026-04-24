import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SNARKJS_COMMAND = ("npx", "--no-install", "snarkjs")


class SnarkJSError(RuntimeError):
    """Raised when snarkjs cannot complete a proving or verification command."""


@dataclass(frozen=True, slots=True)
class SnarkJSOutput:
    stdout: str
    stderr: str
    returncode: int


def prove_groth16(
    input_path: Path,
    wasm_path: Path,
    zkey_path: Path,
    proof_path: Path,
    public_path: Path,
) -> SnarkJSOutput:
    """Generate a Groth16 proof and public inputs with snarkjs."""
    return _run_snarkjs(
        (
            "groth16",
            "fullprove",
            str(input_path),
            str(wasm_path),
            str(zkey_path),
            str(proof_path),
            str(public_path),
        ),
        check=True,
    )


def verify_groth16(
    verification_key_path: Path,
    public_path: Path,
    proof_path: Path,
) -> bool:
    """Return whether snarkjs accepts a Groth16 proof."""
    result = _run_snarkjs(
        (
            "groth16",
            "verify",
            str(verification_key_path),
            str(public_path),
            str(proof_path),
        ),
        check=False,
    )

    output = f"{result.stdout}\n{result.stderr}"
    if "OK" in output:
        return True
    if "Invalid proof" in output:
        return False
    if result.returncode != 0:
        raise SnarkJSError(_format_failure(result))
    return False


def export_verification_key(
    zkey_path: Path,
    verification_key_path: Path,
) -> SnarkJSOutput:
    """Export the verifier's JSON key from a Groth16 zkey."""
    return _run_snarkjs(
        (
            "zkey",
            "export",
            "verificationkey",
            str(zkey_path),
            str(verification_key_path),
        ),
        check=True,
    )


def _run_snarkjs(
    args: tuple[str, ...],
    *,
    check: bool,
) -> SnarkJSOutput:
    command = (*SNARKJS_COMMAND, *args)
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    result = SnarkJSOutput(
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
    )

    if check and completed.returncode != 0:
        raise SnarkJSError(_format_failure(result))

    return result


def _format_failure(result: SnarkJSOutput) -> str:
    details = "\n".join(
        part
        for part in (
            f"snarkjs exited with {result.returncode}",
            result.stdout.strip(),
            result.stderr.strip(),
        )
        if part
    )
    return details


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Groth16 proof commands through repo-local snarkjs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prove_parser = subparsers.add_parser(
        "prove",
        help="Generate a Groth16 proof and public inputs.",
    )
    prove_parser.add_argument("input_path", type=Path)
    prove_parser.add_argument("wasm_path", type=Path)
    prove_parser.add_argument("zkey_path", type=Path)
    prove_parser.add_argument("proof_path", type=Path)
    prove_parser.add_argument("public_path", type=Path)

    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify a Groth16 proof.",
    )
    verify_parser.add_argument("verification_key_path", type=Path)
    verify_parser.add_argument("public_path", type=Path)
    verify_parser.add_argument("proof_path", type=Path)

    export_parser = subparsers.add_parser(
        "export-vkey",
        help="Export a Groth16 verification key JSON from a zkey.",
    )
    export_parser.add_argument("zkey_path", type=Path)
    export_parser.add_argument("verification_key_path", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "prove":
            result = prove_groth16(
                args.input_path,
                args.wasm_path,
                args.zkey_path,
                args.proof_path,
                args.public_path,
            )
            _print_output(result)
            print(f"Wrote proof to {args.proof_path}")
            print(f"Wrote public inputs to {args.public_path}")
            return 0

        if args.command == "verify":
            is_valid = verify_groth16(
                args.verification_key_path,
                args.public_path,
                args.proof_path,
            )
            print("Proof is valid" if is_valid else "Proof is invalid")
            return 0 if is_valid else 1

        if args.command == "export-vkey":
            result = export_verification_key(
                args.zkey_path,
                args.verification_key_path,
            )
            _print_output(result)
            print(f"Wrote verification key to {args.verification_key_path}")
            return 0

    except SnarkJSError as error:
        print(str(error), file=sys.stderr)
        return 2

    parser.error(f"unknown command: {args.command}")
    return 2


def _print_output(result: SnarkJSOutput) -> None:
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
