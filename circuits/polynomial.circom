pragma circom 2.1.6;

template Polynomial() {
    signal input x;
    signal input y;

    y === x * x + 3 * x + 5;
}

component main { public [y] } = Polynomial();
