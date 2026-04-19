import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.sample_data import get_payment_data, VENDORS

def show():
    st.markdown('<div class="section-header">Vendor Payment — T-Code: F110 / F-53</div>', unsafe_allow_html=True)

    pay = get_payment_data()

    tab1, tab2, tab3 = st.tabs(["Payment Register", "Run Payment Program (F110)", "Payment Analytics"])

    with tab1:
        st.markdown("#### Vendor Payment Register — FBL1N / F110")
        c1, c2 = st.columns(2)
        with c1:
            status_filter = st.multiselect("Payment Status", pay["Status"].unique(),
                                           default=list(pay["Status"].unique()))
        with c2:
            vendor_filter = st.multiselect("Vendor",         pay["Vendor Name"].unique(),
                                           default=list(pay["Vendor Name"].unique()))

        filtered = pay[pay["Status"].isin(status_filter) & pay["Vendor Name"].isin(vendor_filter)]

        def color_row(row):
            c = {
                "Cleared": "background-color:#D4EDDA;color:#155724",
                "Pending": "background-color:#FFF3CD;color:#856404",
                "Overdue": "background-color:#F8D7DA;color:#721C24",
            }
            return [c.get(row["Status"], "")] * len(row)

        st.dataframe(
            filtered.style.apply(color_row, axis=1),
            use_container_width=True, height=380
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Payments",  len(filtered))
        m2.metric("Total Cleared",   f"Rs {filtered[filtered.Status=='Cleared']['Amount (Rs)'].sum():,.0f}")
        m3.metric("Pending",         len(filtered[filtered.Status == "Pending"]),
                  delta=f"Rs {filtered[filtered.Status=='Pending']['Amount (Rs)'].sum():,.0f}")
        m4.metric("Overdue",         len(filtered[filtered.Status == "Overdue"]),
                  delta_color="inverse",
                  delta=f"Rs {filtered[filtered.Status=='Overdue']['Amount (Rs)'].sum():,.0f}")

    with tab2:
        st.markdown("#### Automatic Payment Program — F110 (Simulation)")
        st.info(
            "The F110 Automatic Payment Program processes all due vendor invoices in batch, "
            "based on payment terms, due dates, and payment methods configured per vendor."
        )

        st.markdown("##### Step 1 — Configure Payment Run Parameters")
        with st.form("f110_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                run_date    = st.date_input("Run Date")
                run_id      = st.text_input("Run Identification (max 5 chars)", value="RUN01", max_chars=5)
                comp_code   = st.selectbox("Company Code", ["1000 - ABC Mfg. Mumbai", "2000 - ABC Mfg. Pune"])
            with c2:
                pay_method  = st.multiselect("Payment Methods",
                                             ["T - Bank Transfer", "C - Cheque", "O - Online Banking"],
                                             default=["T - Bank Transfer"])
                next_pay_dt = st.date_input("Next Payment Run Date")
                bank_acc    = st.selectbox("House Bank", ["HDFC - Main A/C", "SBI - Salary A/C", "ICICI - Vendor A/C"])
            with c3:
                vendors_sel = st.multiselect("Vendor Selection (Blank = All)", list(VENDORS.values()))
                min_amount  = st.number_input("Minimum Payment Amount (Rs)", min_value=0, value=1000)
                doc_type    = st.selectbox("Payment Document Type", ["ZP - Payment", "KZ - Vendor Payment"])

            submitted = st.form_submit_button("Execute Payment Run (F110)", use_container_width=True)

        if submitted:
            import random
            eligible = pay[pay.Status.isin(["Pending", "Overdue"])]
            if len(eligible):
                total_paid = eligible["Amount (Rs)"].sum()
                pay_doc    = random.randint(2000030000, 2000099999)
                st.success(f"Payment Run '{run_id}' executed successfully. {len(eligible)} payment(s) processed.")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Payments Processed", len(eligible))
                col2.metric("Total Amount",        f"Rs {total_paid:,.0f}")
                col3.metric("Payment Method",      pay_method[0] if pay_method else "T")
                col4.metric("Posting Document",    str(pay_doc))

                st.markdown("##### Payment Proposal (Simulated)")
                proposal = eligible[["Payment Doc", "Vendor Name", "Amount (Rs)", "Due Date", "Method"]].copy()
                proposal["Status After Run"] = "Cleared"
                st.dataframe(proposal, use_container_width=True)

                st.info(
                    "After the F110 payment run in SAP:\n"
                    "1. Payment document is posted in FI and vendor account is cleared.\n"
                    "2. Bank line items are created for reconciliation.\n"
                    "3. Payment medium (transfer advice or cheque) is generated via FBZP.\n"
                    "4. Bank statement is matched using T-Code FF67 or F-03."
                )
            else:
                st.warning("No eligible pending or overdue payments found for the selected criteria.")

        st.markdown("---")
        st.markdown("##### Manual Payment — F-53 (Individual Vendor)")
        with st.form("f53_form"):
            c1, c2 = st.columns(2)
            with c1:
                vendor_m = st.selectbox("Vendor",           [f"{k} - {v}" for k, v in VENDORS.items()])
                amount_m = st.number_input("Payment Amount (Rs)", min_value=0.0, value=25000.0)
                pay_date = st.date_input("Payment Date")
            with c2:
                bank_m   = st.selectbox("Bank Account",     ["HDFC Main", "SBI Salary", "ICICI Vendor"])
                ref_m    = st.text_input("Reference / Cheque No.", placeholder="CHQ-0012345")
                inv_m    = st.text_input("Clear Against Invoice",  placeholder="5105510012")
            sub_m = st.form_submit_button("Post Manual Payment (F-53)", use_container_width=True)

        if sub_m:
            import random
            pay_doc_m = random.randint(2000000100, 2000009999)
            st.success(f"Manual payment of Rs {amount_m:,.2f} posted successfully. Payment Document: {pay_doc_m}")

    with tab3:
        st.markdown("#### Payment Analytics")
        c1, c2 = st.columns(2)
        with c1:
            stat_amt = pay.groupby("Status")["Amount (Rs)"].sum().reset_index()
            fig = px.pie(stat_amt, names="Status", values="Amount (Rs)", hole=0.4,
                         title="Payment Amount by Status",
                         color="Status",
                         color_discrete_map={
                             "Cleared": "#28A745",
                             "Pending": "#FFC107",
                             "Overdue": "#DC3545"
                         })
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            vend_amt = pay.groupby("Vendor Name")["Amount (Rs)"].sum().reset_index()
            fig2 = px.bar(vend_amt, x="Amount (Rs)", y="Vendor Name", orientation='h',
                          title="Total Payments by Vendor",
                          color="Amount (Rs)", color_continuous_scale="Blues")
            fig2.update_layout(coloraxis_showscale=False,
                               yaxis=dict(categoryorder='total ascending'))
            st.plotly_chart(fig2, use_container_width=True)

        method_stat = pay.groupby("Method")["Amount (Rs)"].sum().reset_index()
        fig3 = px.pie(method_stat, names="Method", values="Amount (Rs)", hole=0.35,
                      title="Payment Methods Breakdown",
                      color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig3, use_container_width=True)
