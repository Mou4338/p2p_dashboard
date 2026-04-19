import streamlit as st

st.set_page_config(
    page_title="P2P SAP Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1F4E79 0%, #2E75B6 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stRadio label { color: white !important; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #F0F6FF;
        border: 1px solid #C8DFF5;
        border-left: 4px solid #2E75B6;
        border-radius: 8px;
        padding: 12px 16px;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #1F4E79, #2E75B6);
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 16px;
    }

    /* Status badges */
    .badge-open     { background:#FFF3CD; color:#856404; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .badge-approved { background:#D4EDDA; color:#155724; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .badge-blocked  { background:#F8D7DA; color:#721C24; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .badge-posted   { background:#CCE5FF; color:#004085; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .badge-paid     { background:#D1ECF1; color:#0C5460; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }

    /* KPI card */
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #2E75B6;
        text-align: center;
    }
    .kpi-value { font-size: 32px; font-weight: 800; color: #1F4E79; }
    .kpi-label { font-size: 13px; color: #666; margin-top: 4px; }

    /* Table styling */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        background: #E8F1FB;
        color: #1F4E79;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #2E75B6 !important;
        color: white !important;
    }

    /* Process step */
    .process-step {
        background: white;
        border: 1px solid #C8DFF5;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        font-size: 13px;
        font-weight: 600;
        color: #1F4E79;
    }
    .process-arrow { font-size: 22px; color: #2E75B6; text-align: center; padding-top: 14px; }

    h1, h2, h3 { color: #1F4E79; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 P2P Dashboard")
    st.markdown("**ABC Manufacturing Ltd.**")
    st.markdown("SAP MM Module · 2024-25")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠  Overview",
            "📋  Purchase Requisition",
            "📦  Purchase Order",
            "🚚  Goods Receipt",
            "🧾  Invoice Verification",
            "💳  Vendor Payment",
            "📊  Analytics & Reports",
            "ℹ️  P2P Process Guide",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        "<small>KIIT University · SAP Project<br>Procure-to-Pay (P2P)<br>Academic Year 2024-25</small>",
        unsafe_allow_html=True
    )

# ── Route pages ─────────────────────────────────────────────────────────────
page_key = page.split("  ", 1)[-1].strip()

if page_key == "Overview":
    from pages.overview import show; show()
elif page_key == "Purchase Requisition":
    from pages.purchase_requisition import show; show()
elif page_key == "Purchase Order":
    from pages.purchase_order import show; show()
elif page_key == "Goods Receipt":
    from pages.goods_receipt import show; show()
elif page_key == "Invoice Verification":
    from pages.invoice_verification import show; show()
elif page_key == "Vendor Payment":
    from pages.vendor_payment import show; show()
elif page_key == "Analytics & Reports":
    from pages.analytics import show; show()
elif page_key == "P2P Process Guide":
    from pages.process_guide import show; show()
