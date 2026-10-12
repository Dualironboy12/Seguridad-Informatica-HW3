#!/usr/bin/env python3
"""Simulador mínimo de Enigma I (3 rotores + reflector B) para demo educativa."""

from __future__ import annotations

import sys
from dataclasses import dataclass

# Wiring histórico (A=0 ... Z=25), notch indica cuándo avanza el siguiente rotor
ROTORS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
}
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


def _A0(ch: str) -> int:
    return ord(ch.upper()) - ord("A")


def _chr(i: int) -> str:
    return chr(ord("A") + (i % 26))


@dataclass
class Rotor:
    name: str
    wiring: str
    notch: str
    position: int = 0  # ring window letter offset 0..25
    ring_setting: int = 0

    def __post_init__(self) -> None:
        self.fwd = [_A0(c) for c in self.wiring]
        self.inv = [0] * 26
        for i, v in enumerate(self.fwd):
            self.inv[v] = i

    def at_notch(self) -> bool:
        return _chr(self.position) == self.notch

    def step(self) -> None:
        self.position = (self.position + 1) % 26

    def _map(self, mapping: list[int], x: int) -> int:
        shift = self.position - self.ring_setting
        return (mapping[(x + shift) % 26] - shift) % 26

    def forward(self, x: int) -> int:
        return self._map(self.fwd, x)

    def backward(self, x: int) -> int:
        return self._map(self.inv, x)


class Enigma:
    """Enigma I simplificada: sin plugboard (o plugboard identidad)."""

    def __init__(
        self,
        rotor_names: tuple[str, str, str] = ("I", "II", "III"),
        positions: str = "AAA",
        rings: str = "AAA",
        plugs: str = "",
    ) -> None:
        self.rotors = []
        for name, pos, ring in zip(rotor_names, positions.upper(), rings.upper()):
            wiring, notch = ROTORS[name]
            self.rotors.append(
                Rotor(name, wiring, notch, position=_A0(pos), ring_setting=_A0(ring))
            )
        self.reflector = [_A0(c) for c in REFLECTOR_B]
        self.plug = list(range(26))
        for pair in plugs.upper().split():
            if len(pair) == 2:
                a, b = _A0(pair[0]), _A0(pair[1])
                self.plug[a], self.plug[b] = b, a

    def _advance(self) -> None:
        # Double-stepping simplificado
        left, middle, right = self.rotors
        if middle.at_notch():
            middle.step()
            left.step()
        if right.at_notch():
            middle.step()
        right.step()

    def positions(self) -> str:
        return "".join(_chr(r.position) for r in self.rotors)

    def encode_char(self, ch: str) -> str:
        if not ch.isalpha():
            return ch
        self._advance()
        x = self.plug[_A0(ch)]
        for r in reversed(self.rotors):
            x = r.forward(x)
        x = self.reflector[x]
        for r in self.rotors:
            x = r.backward(x)
        x = self.plug[x]
        return _chr(x)

    def encode(self, text: str) -> str:
        return "".join(self.encode_char(c) for c in text.upper() if c.isalpha() or c == " ")


def demo(text: str = "HI") -> str:
    lines = [
        "=== Enigma I mini-simulator ===",
        "Rotors I/II/III, reflector B, positions AAA, no plugboard",
        "",
    ]
    enc = Enigma()
    cipher_parts = []
    for ch in text.upper():
        if not ch.isalpha():
            continue
        before = enc.positions()
        out = enc.encode_char(ch)
        after = enc.positions()
        lines.append(f"  {ch}  positions {before} -> {after}  =>  {out}")
        cipher_parts.append(out)
    ciphertext = "".join(cipher_parts)
    lines.append(f"Ciphertext: {ciphertext}")
    lines.append("")
    # Decrypt = encode again with same settings
    dec = Enigma()
    plain = dec.encode(ciphertext)
    lines.append(f"Decrypt with same settings: {plain}")
    lines.append("Propiedad: cifrar dos veces con la misma config recupera el texto")
    lines.append("(involución del cableado + reflector).")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    text = argv[0] if argv else "HI"
    print(demo(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
