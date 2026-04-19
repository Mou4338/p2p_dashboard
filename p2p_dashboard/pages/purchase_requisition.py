import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.sample_data import get_pr_data, MATERIALS, PLANTS, PURCH_GROUPS

def show():
    st.markdown('<div class="section-header">Purchase Requisition — T-Code: ME51N</div>', unsafe_allow_html=True)

    pr = get_pr_data()

    tab1, tab2, tab3 = st.tabs(["PR Register", "Create New PR", "PR Analytics"])

    with tab1:
        st.markdown("#### All Purchase Requisitions")
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect("Filter by Status", pr["Status"].unique(), default=list(pr["Status"].unique()))
        with col2:
            plant_filter  = st.multiselect("Filter by Plant",  pr["Plant"].unique(),  default=list(pr["Plant"].unique()))
        with col3:
            search = st.text_input("Search by Material or PR Number")

        filtered = pr[pr["Status"].isin(status_filter) & pr["Plant"].isin(plant_filter)]
        if search:
            filtered = filtered[
                filtered["PR Number"].str.contains(search, case=False) |
                filtered["Description"].str.contains(search, case=False)
            ]

        def color_status(val):
            colors = {
                "Open":            "background-color:#FFF3CD;color:#856404",
                "Approved":        "background-color:#D4EDDA;color:#155724",
                "Converted to PO": "background-color:#CCE5FF;color:#004085",
                "Rejected":        "background-color:#F8D7DA;color:#721C24",
            }
            return colors.get(val, "")

        st.dataframe(
            filtered.style.applymap(color_status, subset=["Status"]),
            use_container_width=True, height=420
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total PRs",         len(filtered))
        m2.metric("Open",              len(filtered[filtered.Status == "Open"]))
        m3.metric("Approved",          len(filtered[filtered.Status == "Approved"]))
        m4.metric("Converted to PO",   len(filtered[filtered.Status == "Converted to PO"]))

    with tab2:
        st.markdown("#### Create Purchase Requisition — ME51N (Simulation)")
        st.info("Fill in all mandatory fields below and click Submit to simulate SAP ME51N PR creation.")

        with st.form("pr_form"):
            col1, col2 = st.columns(2)
            with col1:
                doc_type = st.selectbox("Document Type",         ["NB - Standard", "KA - Framework", "UB - Stock Transfer"])
                mat_code = st.selectbox("Material",              [f"{k} - {v[0]}" for k, v in MATERIALS.items()])
                qty      = st.number_input("Quantity",           min_value=1, value=100)
                uom      = st.selectbox("Unit of Measure",       ["PC", "KG", "LTR", "MTR", "SET"])
                req_date = st.date_input("Required Delivery Date")
            with col2:
                plant      = st.selectbox("Plant",               PLANTS)
                sloc       = st.selectbox("Storage Location",    ["0001 - Main Store", "0002 - Production Store", "0003 - QC Store"])
                pur_grp    = st.selectbox("Purchasing Group",    PURCH_GROUPS)
                acct_assign= st.selectbox("Account Assignment",  ["Blank - Stock", "K - Cost Centre", "P - Project", "A - Asset"])
                raised_by  = st.text_input("Raised By",          value="Enter Name")

            desc = st.text_area("Item Description / Short Text",
                                placeholder="e.g. Steel Rod 10mm for production line A")

            submitted = st.form_submit_button("Submit Purchase Requisition", use_container_width=True)

        if submitted:
            import random
            pr_num = random.randint(1000020000, 1000099999)
            st.success(f"Purchase Requisition {pr_num} created successfully.")
            st.markdown(f"""
            | Field | Value |
            |---|---|
            | PR Number | {pr_num} |
            | Material | {mat_code} |
            | Quantity | {qty} {uom} |
            | Plant | {plant} |
            | Required Delivery Date | {req_date} |
            | Status | Open |
            | Next Step | T-Code ME41 — Create RFQ, or ME21N — Convert directly to PO |
            """)

    with tab3:
        st.markdown("#### PR Analytics")
        col1, col2 = st.columns(2)
        with col1:
            grp = pr["Status"].value_counts().reset_index()
            grp.columns = ["Status", "Count"]
            fig = px.pie(grp, names="Status", values="Count", hole=0.4,
                         title="PRs by Status",
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            grp2 = pr.groupby("Plant")["Est. Value (Rs)"].sum().reset_index()
            fig2 = px.bar(grp2, x="Plant", y="Est. Value (Rs)",
                          title="Estimated PR Value by Plant",
                          color="Est. Value (Rs)", color_continuous_scale="Blues")
            fig2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            grp3 = pr["Purch. Group"].value_counts().reset_index()
            grp3.columns = ["Group", "Count"]
            fig3 = px.bar(grp3, x="Group", y="Count",
                          title="PRs by Purchasing Group",
                          color="Count", color_continuous_scale="Blues")
            fig3.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        with col4:
            grp4 = pr.groupby("Description")["Quantity"].sum().nlargest(6).reset_index()
            fig4 = px.bar(grp4, x="Quantity", y="Description", orientation='h',
                          title="Top Materials by Requested Quantity",
                          color="Quantity", color_continuous_scale="Blues")
            fig4.update_layout(coloraxis_showscale=False,
                               yaxis=dict(categoryorder='total ascending'))
            st.plotly_chart(fig4, use_container_width=True)
