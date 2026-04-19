import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.sample_data import get_po_data, VENDORS, MATERIALS, PLANTS, PURCH_GROUPS

def show():
    st.markdown('<div class="section-header">Purchase Order — T-Code: ME21N</div>', unsafe_allow_html=True)

    po = get_po_data()

    tab1, tab2, tab3 = st.tabs(["PO Register", "Create Purchase Order", "PO Analytics"])

    with tab1:
        st.markdown("#### Purchase Order List — ME2M / ME23N")
        col1, col2 = st.columns(2)
        with col1:
            vendor_filter = st.multiselect("Filter by Vendor", po["Vendor Name"].unique(),
                                           default=list(po["Vendor Name"].unique()))
        with col2:
            status_filter = st.multiselect("Filter by Status", po["Status"].unique(),
                                           default=list(po["Status"].unique()))
        col3, col4 = st.columns(2)
        with col3:
            plant_filter = st.multiselect("Filter by Plant", po["Plant"].unique(),
                                          default=list(po["Plant"].unique()))
        with col4:
            search = st.text_input("Search PO Number or Material")

        filtered = po[
            po["Vendor Name"].isin(vendor_filter) &
            po["Status"].isin(status_filter) &
            po["Plant"].isin(plant_filter)
        ]
        if search:
            filtered = filtered[
                filtered["PO Number"].str.contains(search, case=False) |
                filtered["Description"].str.contains(search, case=False)
            ]

        def color_status(val):
            c = {
                "Open":                "background-color:#FFF3CD;color:#856404",
                "Partially Delivered": "background-color:#CCE5FF;color:#004085",
                "Fully Delivered":     "background-color:#D4EDDA;color:#155724",
                "Closed":              "background-color:#E2E3E5;color:#383D41",
            }
            return c.get(val, "")

        st.dataframe(
            filtered.style.applymap(color_status, subset=["Status"]),
            use_container_width=True, height=400
        )

        total_val = filtered["PO Value (Rs)"].sum()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total POs",        len(filtered))
        m2.metric("Total Value",       f"Rs {total_val:,.0f}")
        m3.metric("Open",              len(filtered[filtered.Status == "Open"]))
        m4.metric("Fully Delivered",   len(filtered[filtered.Status == "Fully Delivered"]))

    with tab2:
        st.markdown("#### Create Purchase Order — ME21N (Simulation)")
        st.info("Simulates the SAP ME21N Purchase Order creation screen with Header and Line Item data.")

        st.markdown("**PO Header Data**")
        with st.form("po_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                vendor    = st.selectbox("Vendor",            [f"{k} - {v}" for k, v in VENDORS.items()])
                doc_type  = st.selectbox("Document Type",     ["NB - Standard", "FO - Framework Order", "UB - Stock Transport"])
                po_date   = st.date_input("PO Date")
            with c2:
                pur_org   = st.selectbox("Purchasing Org.",   ["1000 - Central Purchasing", "2000 - Regional"])
                pur_grp   = st.selectbox("Purchasing Group",  PURCH_GROUPS)
                currency  = st.selectbox("Currency",          ["INR", "USD", "EUR"])
            with c3:
                pay_terms = st.selectbox("Payment Terms",     ["Net 30", "Net 45", "Net 60", "2/10 Net 30"])
                incoterms = st.selectbox("Incoterms",         ["CIF - Cost Insurance Freight", "FOB - Free on Board", "EXW - Ex Works"])
                comp_code = st.selectbox("Company Code",      ["1000 - ABC Mfg. Mumbai", "2000 - ABC Mfg. Pune"])

            st.markdown("**PO Item Data**")
            c4, c5, c6, c7 = st.columns(4)
            with c4:
                material  = st.selectbox("Material",          [f"{k} - {v[0]}" for k, v in MATERIALS.items()])
                qty       = st.number_input("Quantity",        min_value=1, value=200)
            with c5:
                uom       = st.selectbox("UOM",               ["PC", "KG", "LTR", "MTR", "SET"])
                net_price = st.number_input("Net Price (Rs)",  min_value=1.0, value=150.0, step=0.5)
            with c6:
                plant     = st.selectbox("Plant",             PLANTS)
                sloc      = st.selectbox("Storage Location",  ["0001 - Main", "0002 - Production", "0003 - QC"])
            with c7:
                del_date  = st.date_input("Delivery Date")
                gr_iv     = st.checkbox("GR-Based Invoice Verification", value=True)

            pr_ref    = st.text_input("PR Reference (Optional)", placeholder="e.g. 1000010012")
            submitted = st.form_submit_button("Create Purchase Order", use_container_width=True)

        if submitted:
            import random
            po_num = random.randint(4500020000, 4500099999)
            po_val = qty * net_price
            st.success(f"Purchase Order {po_num} created successfully.")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                **PO Header:**
                | Field | Value |
                |---|---|
                | PO Number | {po_num} |
                | Vendor | {vendor} |
                | PO Date | {po_date} |
                | Payment Terms | {pay_terms} |
                | Currency | {currency} |
                """)
            with col_b:
                st.markdown(f"""
                **PO Line Item 10:**
                | Field | Value |
                |---|---|
                | Material | {material} |
                | Quantity | {qty} {uom} |
                | Net Price | Rs {net_price:,.2f} |
                | **PO Value** | **Rs {po_val:,.2f}** |
                | Delivery Date | {del_date} |
                | Next Step | MIGO — Post Goods Receipt |
                """)

    with tab3:
        st.markdown("#### PO Analytics")
        c1, c2 = st.columns(2)
        with c1:
            vend_val = po.groupby("Vendor Name")["PO Value (Rs)"].sum().reset_index()
            fig = px.pie(vend_val, names="Vendor Name", values="PO Value (Rs)", hole=0.4,
                         title="PO Value by Vendor",
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            stat_val = po.groupby("Status")["PO Value (Rs)"].sum().reset_index()
            fig2 = px.bar(stat_val, x="Status", y="PO Value (Rs)",
                          title="PO Value by Status",
                          color="Status",
                          color_discrete_map={
                              "Open": "#FFC107",
                              "Partially Delivered": "#2E75B6",
                              "Fully Delivered": "#28A745",
                              "Closed": "#6C757D"
                          })
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            mat_val = po.groupby("Description")["PO Value (Rs)"].sum().nlargest(6).reset_index()
            fig3 = px.bar(mat_val, x="PO Value (Rs)", y="Description", orientation='h',
                          title="Top Materials by PO Value",
                          color="PO Value (Rs)", color_continuous_scale="Blues")
            fig3.update_layout(coloraxis_showscale=False,
                               yaxis=dict(categoryorder='total ascending'))
            st.plotly_chart(fig3, use_container_width=True)
        with c4:
            plant_val = po.groupby("Plant")["PO Value (Rs)"].sum().reset_index()
            fig4 = px.bar(plant_val, x="Plant", y="PO Value (Rs)",
                          title="PO Value by Plant",
                          color="PO Value (Rs)", color_continuous_scale="Blues")
            fig4.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig4, use_container_width=True)
