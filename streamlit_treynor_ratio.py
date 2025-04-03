import streamlit as st

def calculate_treynor_ratio(return_=None, beta=None, risk_free_rate=None, treynor_ratio=None):
    """
    Calculate the Treynor Ratio or any missing value (Return, Beta, Risk-Free Rate) given the other three.
    """

    inputs = [return_, beta, risk_free_rate, treynor_ratio]
    if inputs.count(None) > 1:
        return "❌ Error: Provide at least three values to calculate the missing one."

    try:
        if treynor_ratio is None:
            if return_ is not None and beta is not None and risk_free_rate is not None:
                if abs(beta) < 1e-8:
                    return "❌ Error: Beta is too close to zero. Cannot divide by zero."
                treynor_ratio = (return_ - risk_free_rate) / beta
        elif return_ is None:
            return_ = treynor_ratio * beta + risk_free_rate
        elif beta is None:
            if abs(treynor_ratio) < 1e-8:
                return "❌ Error: Treynor Ratio is too close to zero. Cannot divide by zero."
            beta = (return_ - risk_free_rate) / treynor_ratio
        elif risk_free_rate is None:
            risk_free_rate = return_ - (treynor_ratio * beta)

        return {
            "📈 Return": round(return_, 4),
            "⚖️ Beta": round(beta, 4),
            "💰 Risk-Free Rate": round(risk_free_rate, 4),
            "📊 Treynor Ratio": round(treynor_ratio, 4),
        }

    except Exception as e:
        return f"❌ Error: {e}"


def parse_input(label):
    value = st.text_input(label)
    if value.lower() == "none":
        return None
    try:
        value = value.strip()
        if value.endswith('%'):
            return float(value.strip('%')) / 100
        return float(value)
    except:
        return None


# Streamlit UI setup
st.set_page_config(page_title="Treynor Ratio Calculator", layout="centered")
st.title("📊 Treynor Ratio Calculator")
st.markdown("Enter any **three** of the following values. Use decimal or percentage format. Type `'None'` for the missing one.")

st.divider()

# Inputs
return_ = parse_input("Return (e.g., 0.12 or 12%)")
beta = parse_input("Beta")
risk_free_rate = parse_input("Risk-Free Rate (e.g., 0.05 or 5%)")
treynor_ratio = parse_input("Treynor Ratio")

# Calculation
if st.button("Calculate"):
    result = calculate_treynor_ratio(return_, beta, risk_free_rate, treynor_ratio)

    st.divider()
    st.subheader("✅ Result")
    if isinstance(result, dict):
        for key, value in result.items():
            st.write(f"**{key}:** {value}")
    else:
        st.error(result)
