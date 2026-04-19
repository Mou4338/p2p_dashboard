import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.sample_data import get_pr_data, get_po_data, get_gr_data, get_invoice_data, get_payment_data

def show():
    st.markdown('<div class="section-header">🏠 Procure-to-Pay — Overview Dashboard</div>', unsafe_allow_html=True)
    st.caption("ABC Manufacturing Ltd. · SAP MM · FY 2024-25")

    pr  = get_pr_data()
    po  = get_po_data()
    gr  = get_gr_data()
    inv = get_invoice_data()
    pay = get_payment_data()

    # ── KPI Row ──────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("📋 Total PRs", len(pr), delta=f"{len(pr[pr.Status=='Open'])} Open")
    with k2:
        st.metric("📦 Total POs", len(po), delta=f"₹{po['PO Value (₹)'].sum()/1e5:.1f}L value")
    with k3:
        st.metric("🚚 GR Posted", len(gr), delta=f"₹{gr['Value (₹)'].sum()/1e5:.1f}L received")
    with k4:
        blocked = len(inv[inv.Status=="Blocked"])
        st.metric("🧾 Invoices", len(inv), delta=f"{blocked} Blocked", delta_color="inverse")
    with k5:
        overdue = len(pay[pay.Status=="Overdue"])
        st.metric("💳 Payments", len(pay), delta=f"{overdue} Overdue", delta_color="inverse")

    st.markdown("---")

    # ── Process pipeline flow ────────────────────────────────────────────────
    st.markdown("#### 🔄 P2P Process Flow — Document Pipeline")
    cols = st.columns(9)
    steps = [
        ("📋","Purchase\nRequisition","PR"),
        ("➡️","",""),
        ("📝","Request for\nQuotation","RFQ"),
        ("➡️","",""),
        ("📦","Purchase\nOrder","PO"),
        ("➡️","",""),
        ("🚚","Goods\nReceipt","GR"),
        ("➡️","",""),
        ("🧾","Invoice &\nPayment","MIRO/F110"),
    ]
    for col, (icon, label, code) in zip(cols, steps):
        with col:
            if icon == "➡️":
                st.markdown("<div class='process-arrow'>→</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='process-step'>
                    <div style='font-size:24px'>{icon}</div>
                    <div style='font-size:11px;margin-top:4px'>{label}</div>
                    <div style='font-size:10px;color:#2E75B6;font-weight:700'>{code}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Charts Row 1 ─────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📋 PR Status Breakdown")
        pr_status = pr["Status"].value_counts().reset_index()
        pr_status.columns = ["Status","Count"]
        colors = {"Open":"#FFC107","Approved":"#28A745","Converted to PO":"#2E75B6","Rejected":"#DC3545"}
        fig = px.pie(pr_status, names="Status", values="Count",
                     color="Status", color_discrete_map=colors, hole=0.45)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True, height=300, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 💰 PO Value by Vendor (Top 5)")
        po_vend = po.groupby("Vendor Name")["PO Value (₹)"].sum().nlargest(5).reset_index()
        fig2 = px.bar(po_vend, x="PO Value (₹)", y="Vendor Name", orientation='h',
                      color="PO Value (₹)", color_continuous_scale=["#9DC3E6","#1F4E79"])
        fig2.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           coloraxis_showscale=False,
                           yaxis=dict(categoryorder='total ascending'))
        fig2.update_traces(texttemplate='₹%{x:,.0f}', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

    # ── Charts Row 2 ─────────────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### 🧾 Invoice Status Distribution")
        inv_stat = inv["Status"].value_counts().reset_index()
        inv_stat.columns = ["Status","Count"]
        inv_colors = {"Posted":"#2E75B6","Blocked":"#DC3545","Paid":"#28A745","In Verification":"#FFC107"}
        fig3 = px.bar(inv_stat, x="Status", y="Count",
                      color="Status", color_discrete_map=inv_colors)
        fig3.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### 📦 GR: Ordered vs Received Qty (Top 8)")
        gr_top = gr.head(8)[["Description","Qty Ordered","Qty Received"]]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Ordered",  x=gr_top["Description"], y=gr_top["Qty Ordered"],  marker_color="#9DC3E6"))
        fig4.add_trace(go.Bar(name="Received", x=gr_top["Description"], y=gr_top["Qty Received"], marker_color="#1F4E79"))
        fig4.update_layout(barmode='group', height=300, margin=dict(t=10,b=10,l=10,r=10),
                           xaxis_tickangle=-30, legend=dict(orientation="h",yanchor="bottom",y=1))
        st.plotly_chart(fig4, use_container_width=True)

    # ── Pending Actions Table ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### ⚠️ Pending Actions")
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("**🚫 Blocked Invoices (Require Release)**")
        blocked_inv = inv[inv.Status == "Blocked"][["Invoice No","Vendor Name","Total Amt (₹)","Block Reason","Due Date"]]
        st.dataframe(blocked_inv.reset_index(drop=True), use_container_width=True, height=200)

    with col6:
        st.markdown("**⏰ Overdue Payments**")
        overdue_pay = pay[pay.Status == "Overdue"][["Payment Doc","Vendor Name","Amount (₹)","Due Date","Method"]]
        st.dataframe(overdue_pay.reset_index(drop=True), use_container_width=True, height=200)

    # ── Summary financials ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📈 Financial Summary")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>₹{po['PO Value (₹)'].sum()/1e5:.1f}L</div>
            <div class='kpi-label'>Total PO Value</div></div>""", unsafe_allow_html=True)
    with f2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>₹{gr['Value (₹)'].sum()/1e5:.1f}L</div>
            <div class='kpi-label'>Goods Received Value</div></div>""", unsafe_allow_html=True)
    with f3:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>₹{inv['Total Amt (₹)'].sum()/1e5:.1f}L</div>
            <div class='kpi-label'>Total Invoice Value</div></div>""", unsafe_allow_html=True)
    with f4:
        paid_amt = pay[pay.Status=="Cleared"]["Amount (₹)"].sum()
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>₹{paid_amt/1e5:.1f}L</div>
            <div class='kpi-label'>Payments Cleared</div></div>""", unsafe_allow_html=True)
