import streamlit as st
import pages.analytics
st.write("IMPORT WORKED")

st.set_page_config(
    page_title="P2P SAP Dashboard | ABC Manufacturing Ltd.",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1F4E79 0%, #2E75B6 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.25); }
    [data-testid="metric-container"] {
        background: #F0F6FF;
        border: 1px solid #C8DFF5;
        border-left: 4px solid #2E75B6;
        border-radius: 6px;
        padding: 12px 16px;
    }
    .section-header {
        background: linear-gradient(90deg, #1F4E79, #2E75B6);
        color: white;
        padding: 11px 22px;
        border-radius: 6px;
        font-size: 17px;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-bottom: 18px;
    }
    .kpi-card {
        background: white;
        border-radius: 8px;
        padding: 20px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-top: 4px solid #2E75B6;
        text-align: center;
    }
    .kpi-value { font-size: 30px; font-weight: 800; color: #1F4E79; }
    .kpi-label { font-size: 12px; color: #555; margin-top: 5px;
                 text-transform: uppercase; letter-spacing: 0.5px; }
    .stDataFrame { border-radius: 6px; overflow: hidden; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 5px 5px 0 0;
        background: #E8F1FB;
        color: #1F4E79;
        font-weight: 600;
        font-size: 13px;
    }
    .stTabs [aria-selected="true"] {
        background: #2E75B6 !important;
        color: white !important;
    }
    .process-step {
        background: white;
        border: 1px solid #C8DFF5;
        border-radius: 7px;
        padding: 14px 8px;
        text-align: center;
        font-size: 12px;
        font-weight: 600;
        color: #1F4E79;
        line-height: 1.5;
    }
    .sidebar-banner {
        background: rgba(255,255,255,0.12);
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 12px;
        line-height: 1.7;
        margin-top: 8px;
    }
    h1, h2, h3 { color: #1F4E79; }
    h4 { color: #2E75B6; }
    .stButton > button {
        background: #2E75B6;
        color: white;
        font-weight: 600;
        border-radius: 5px;
        border: none;
    }
    .stButton > button:hover { background: #1F4E79; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### P2P Dashboard")
    st.markdown("**ABC Manufacturing Ltd.**")
    st.markdown("SAP MM Module — 2024-25")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Purchase Requisition",
            "Purchase Order",
            "Goods Receipt",
            "Invoice Verification",
            "Vendor Payment",
            "Analytics and Reports",
            "P2P Process Guide",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        """<div class='sidebar-banner'>
            KIIT University<br>
            SAP Project Report<br>
            Procure-to-Pay (P2P)<br>
            Academic Year 2024-25
        </div>""",
        unsafe_allow_html=True
    )

if page == "Overview":
    from pages.overview import show; show()
elif page == "Purchase Requisition":
    from pages.purchase_requisition import show; show()
elif page == "Purchase Order":
    from pages.purchase_order import show; show()
elif page == "Goods Receipt":
    from pages.goods_receipt import show; show()
elif page == "Invoice Verification":
    from pages.invoice_verification import show; show()
elif page == "Vendor Payment":
    from pages.vendor_payment import show; show()
elif page == "Analytics and Reports":
    from pages.analytics import show; show()
elif page == "P2P Process Guide":
    from pages.process_guide import show; show()
