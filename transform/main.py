import json
import math
from sympy import pi, symbols, cos, sin
from sympy.printing import latex

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq


def func_name(t: str, i: int) -> str:
    return f"F_{{{t}{i}}}"


def serialize_coefficients(coeffs: list[complex], correction: float) -> str:
    result = correction
    t = symbols("t")
    for i in range(1, len(coeffs)):
        angle = i*t*2*pi
        result += coeffs[i-1].real*cos(angle) + \
            coeffs[i-1].imag*sin(angle)
    return latex(result)


def test_data(samples=1000):
    # shape of "data"
    # {
    #   angles: float[],
    #   radii: float[],
    # }[]

    angles = []
    radii = []

    for i in range(samples):
        angle = 2 * math.pi * (i/samples)
        angles.append(angle)
        radii.append(math.cos(2*angle))

    return [{
        "angles": angles,
        "radii": radii,
    }]


def transform(data, samples=50):
    equations = []

    for n, stroke in enumerate(data):
        angle_array = np.array(stroke["angles"])
        radius_array = np.array(stroke["radii"])

        angles_coefficients, angle_correction = approximate(
            angle_array, samples)
        radii_coefficients, radius_correction = approximate(
            radius_array, samples)

        angle_name = func_name("angle", n)
        radius_name = func_name("radius", n)

        equations.append(
            f"{angle_name}(t)={serialize_coefficients(angles_coefficients, angle_correction)}")
        equations.append(
            f"{radius_name}(t)={serialize_coefficients(radii_coefficients, radius_correction)}")
        equations.append(
            f"({radius_name}(t)\\cos({angle_name}(t)),{radius_name}(t)\\sin({angle_name}(t)))")

    return equations


def plt_input(data):
    x = []
    y = []

    for i, stroke in enumerate(data):
        for angle, radius in zip(stroke["angles"], stroke["radii"]):
            x.append(radius * math.cos(angle))
            y.append(radius * math.sin(angle))

    fig, ax = plt.subplots()

    ax.set_aspect("equal")
    ax.grid()
    ax.scatter(x, y, s=1)

    plt.show()


def approximate(series: list[float], samples=50):
    time = np.linspace(0, 1, len(series))
    period = 1

    def cn(n: int):
        c = series*np.exp(-1j*2*n*np.pi*time/period)
        return c.sum()/c.size

    return np.array([2*cn(i) for i in range(1, samples+1)]), cn(0).real


def evaluate_coeff(coeffs: list[complex], x: int):
    result = np.zeros(len(coeffs))

    for i in range(1, len(coeffs)):
        result[i] = coeffs[i-1].real*np.cos(2*np.pi*i*x) - \
            coeffs[i-1].imag*np.sin(2*np.pi*i*x)

    return result.sum()


def approximate_series(series: list[float]):
    time = np.linspace(0, 1, len(series))
    coefficients, correction = approximate(series, 200)

    fig, ax = plt.subplots(4)
    ax[0].plot(
        np.linspace(0, len(coefficients), len(coefficients)), coefficients,
    )
    # predicted = 6.5/10 * \
    #     (3.5+6.5/1.26 *
    #      np.array([evaluate_coeff(coefficients, i) for i in time]))
    predicted = np.array(
        [evaluate_coeff(coefficients, i)+correction for i in time])
    ax[1].plot(time, predicted)
    ax[2].plot(time, series)
    ax[3].plot(time, series-predicted)

    plt.show()


def compare_test(data):
    time = np.linspace(0, 1, len(data[0]["angles"]))

    a_coefficients, a_correction = approximate(data[0]["angles"], 200)
    angles = [evaluate_coeff(a_coefficients, i)+a_correction for i in time]

    r_coefficients, r_correction = approximate(data[0]["radii"], 200)
    radii = [evaluate_coeff(r_coefficients, i)+r_correction for i in time]

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.scatter(angles, radii, s=1)
    ax.scatter(data[0]["angles"], data[0]["radii"])
    plt.show()


if __name__ == "__main__":
    np.set_printoptions(suppress=True)

    parser = argparse.ArgumentParser(
        prog='Preprocess',
        description='Runs edge detection and brightness gating on images.')

    parser.add_argument('-s', '--samples', type=int, default=350)
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default="equations.txt")

    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.loads(f.read())

        equations = transform(data, samples=args.samples)
        with open(args.output, "w") as out:
            for e in equations:
                out.write(e + "\n")

    # with open("complex.json", "r") as f:
    #     data = json.loads(f.read())

    #     indices = [0, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 33, 34, 35]
    #     filtered = [data[i] for i in indices]
    #     single = {
    #         "angles": [],
    #         "radii": [],
    #     }
    #     for i in indices:
    #         single["angles"] += data[i]["angles"]
    #         single["radii"] += data[i]["radii"]
    #     plt_input([single])

    #     # data = test_data()
    #     # plt_input(data)

    #     # approximate_series(data[0]["radii"])
    #     # plt_input(data)

    #     equations = transform([single], samples=350)
    #     with open("output.txt", "w") as out:
    #         for e in equations:
    #             out.write(e + "\n")
