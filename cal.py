import math
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

x = sp.symbols('x')

st.set_page_config(page_title="🧮 Ultimate Math Helper", layout="centered")
st.title("🧮 Ultimate Math Helper")
st.write("All-in-one **scientific & symbolic calculator** with step-by-step explanations and plotting!")

menu = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Basic Arithmetic",
        "Roots & Powers",
        "Logarithm",
        "Trigonometry",
        "Equation Solving",
        "Derivative",
        "Integration",
        "Limit",
        "Series Expansion (Taylor / Maclaurin)",
        "Simplify / Expand / Factor Expression",
        "Factorial / GCD / LCM",
        "Define & Evaluate Function",
        "Plot Function"
    ]
)

# ---------------- BASIC ----------------
if menu == "Basic Arithmetic":
    num1 = st.number_input("Enter first number", value=0.0)
    num2 = st.number_input("Enter second number", value=0.0)
    op = st.radio("Choose operation", ["+", "-", "*", "/", "^"])
    if st.button("Calculate"):
        try:
            if op == "+": st.success(num1 + num2)
            elif op == "-": st.success(num1 - num2)
            elif op == "*": st.success(num1 * num2)
            elif op == "/":
                st.success(num1 / num2 if num2 != 0 else "❌ Division by zero")
            elif op == "^": st.success(num1 ** num2)
        except Exception as e:
            st.error(e)

# ---------------- ROOTS ----------------
elif menu == "Roots & Powers":
    num = st.number_input("Enter number", value=0.0)
    root_type = st.radio("Choose root", ["Square Root", "N-th Root"])
    if root_type == "Square Root":
        if st.button("Compute √"):
            st.success(math.sqrt(num) if num >= 0 else "❌ Negative number")
    else:
        n = st.number_input("Enter n (root degree)", value=2.0)
        if st.button("Compute n-th Root"):
            st.success(num ** (1/n) if n != 0 else "❌ Root degree cannot be zero")

# ---------------- LOG ----------------
elif menu == "Logarithm":
    num = st.number_input("Enter number (>0)", value=1.0)
    base = st.text_input("Enter base (leave empty for natural log)")
    if st.button("Compute log"):
        if num <= 0:
            st.error("Log undefined for ≤ 0")
        else:
            st.success(math.log(num) if base == "" else math.log(num, float(base)))

# ---------------- TRIG ----------------
elif menu == "Trigonometry":
    angle = st.number_input("Enter angle (degrees)", value=0.0)
    rad = math.radians(angle)
    if st.button("Compute trig functions"):
        st.write(f"sin({angle}) = {math.sin(rad)}")
        st.write(f"cos({angle}) = {math.cos(rad)}")
        st.write(f"tan({angle}) = {math.tan(rad)}")

# ---------------- EQUATION ----------------
elif menu == "Equation Solving":
    eq_str = st.text_input("Enter equation (e.g. x**2 - 4 = 0)")
    step_mode = st.checkbox("Show steps")
    if st.button("Solve"):
        try:
            if "=" in eq_str:
                left, right = eq_str.split("=")
                eq = sp.Eq(sp.sympify(left), sp.sympify(right))
            else:
                eq = sp.Eq(sp.sympify(eq_str), 0)
            solutions = sp.solve(eq, x)
            st.success(f"Solutions: {solutions}")

            if step_mode:
                st.write("### Steps:")
                st.latex(sp.latex(eq))
                factored = sp.factor(eq.lhs - eq.rhs)
                st.latex(f"Factorized: {sp.latex(factored)}")

        except Exception as e:
            st.error(e)

# ---------------- DERIVATIVE ----------------
elif menu == "Derivative":
    expr_str = st.text_input("Enter function f(x)")
    step_mode = st.checkbox("Show steps")
    if st.button("Differentiate"):
        expr = sp.sympify(expr_str)
        derivative = sp.diff(expr, x)
        st.success(f"f'(x) = {derivative}")

        if step_mode:
            st.write("### Steps:")
            st.latex(f"f(x) = {sp.latex(expr)}")
            for term in expr.as_ordered_terms():
                st.latex(f"d/dx({sp.latex(term)}) = {sp.latex(sp.diff(term, x))}")
            st.latex(f"f'(x) = {sp.latex(derivative)}")

# ---------------- INTEGRATION ----------------
elif menu == "Integration":
    expr_str = st.text_input("Enter function f(x)")
    mode = st.radio("Choose type", ["Indefinite", "Definite"])
    step_mode = st.checkbox("Show steps")
    if st.button("Integrate"):
        expr = sp.sympify(expr_str)
        if mode == "Indefinite":
            result = sp.integrate(expr, x)
            st.success(f"∫ f(x) dx = {result}")
            if step_mode:
                st.latex(f"∫ {sp.latex(expr)} dx = {sp.latex(result)}")
        else:
            a = st.number_input("Lower limit a", value=0.0)
            b = st.number_input("Upper limit b", value=1.0)
            result = sp.integrate(expr, (x, a, b))
            st.success(f"∫[{a},{b}] f(x) dx = {result}")
            if step_mode:
                F = sp.integrate(expr, x)
                st.latex(f"F(x) = {sp.latex(F)}")
                st.latex(f"F({b}) - F({a}) = {F.subs(x,b)} - {F.subs(x,a)} = {result}")

# ---------------- LIMIT ----------------
elif menu == "Limit":
    expr_str = st.text_input("Enter function f(x)")
    point = st.text_input("Limit point (use oo for infinity)", value="0")
    direction = st.radio("Direction", ["both", "+", "-"])
    step_mode = st.checkbox("Show steps")
    if st.button("Compute Limit"):
        expr = sp.sympify(expr_str)
        lim_point = sp.oo if point == "oo" else sp.sympify(point)
        result = sp.limit(expr, x, lim_point, dir="+" if direction=="+" else "-" if direction=="-" else None)
        st.success(f"Limit = {result}")
        if step_mode:
            st.write("### Steps:")
            st.latex(f"\\lim_{{x→{sp.latex(lim_point)}}} {sp.latex(expr)} = {sp.latex(result)}")

# ---------------- SERIES ----------------
elif menu == "Series Expansion (Taylor / Maclaurin)":
    expr_str = st.text_input("Enter function f(x)")
    center = st.text_input("Center a (default=0)")
    order = st.number_input("Order n", min_value=1, value=5)
    if st.button("Expand series"):
        expr = sp.sympify(expr_str)
        a = 0 if center.strip()=="" else sp.sympify(center)
        series = sp.series(expr, x, a, order).removeO()
        st.success(series)
        if st.checkbox("Plot original vs series"):
            f = sp.lambdify(x, expr, "numpy")
            g = sp.lambdify(x, series, "numpy")
            X = np.linspace(-5,5,400)
            Yf, Yg = f(X), g(X)
            fig, ax = plt.subplots()
            ax.plot(X,Yf,label="f(x)")
            ax.plot(X,Yg,"--",label="Series")
            ax.axhline(0,color="black")
            ax.axvline(0,color="black")
            ax.legend(); ax.grid(True)
            st.pyplot(fig)

# ---------------- SIMPLIFY ----------------
elif menu == "Simplify / Expand / Factor Expression":
    expr_str = st.text_input("Enter expression")
    if st.button("Process"):
        expr = sp.sympify(expr_str)
        st.write("Simplified:", sp.simplify(expr))
        st.write("Expanded:", sp.expand(expr))
        st.write("Factored:", sp.factor(expr))

# ---------------- FACTORIAL ----------------
elif menu == "Factorial / GCD / LCM":
    choice = st.radio("Choose operation", ["Factorial", "GCD", "LCM"])
    if choice == "Factorial":
        n = st.number_input("Enter integer", min_value=0, value=5)
        if st.button("Compute"):
            st.success(math.factorial(n))
    elif choice == "GCD":
        a = st.number_input("First integer", value=6)
        b = st.number_input("Second integer", value=9)
        if st.button("Compute"):
            st.success(math.gcd(int(a),int(b)))
    else:
        a = st.number_input("First integer", value=6)
        b = st.number_input("Second integer", value=9)
        if st.button("Compute"):
            st.success(abs(int(a*b))//math.gcd(int(a),int(b)))

# ---------------- FUNCTION ----------------
elif menu == "Define & Evaluate Function":
    expr_str = st.text_input("Define f(x)")
    val = st.number_input("Value of x", value=1.0)
    if st.button("Evaluate"):
        expr = sp.sympify(expr_str)
        st.success(expr.subs(x, val))

# ---------------- PLOT ----------------
elif menu == "Plot Function":
    expr_str = st.text_input("Enter function f(x)")
    xmin = st.number_input("x-min", value=-5.0)
    xmax = st.number_input("x-max", value=5.0)
    if st.button("Plot"):
        expr = sp.sympify(expr_str)
        f = sp.lambdify(x, expr, "numpy")
        X = np.linspace(xmin, xmax, 400)
        Y = f(X)
        fig, ax = plt.subplots()
        ax.plot(X,Y,label=f"f(x)={expr}")
        ax.axhline(0,color="black"); ax.axvline(0,color="black")
        ax.legend(); ax.grid(True)
        st.pyplot(fig)
