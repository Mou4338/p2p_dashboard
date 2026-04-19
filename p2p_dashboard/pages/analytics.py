import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.sample_data import get_pr_data, get_po_data, get_gr_data, get_invoice_data, get_payment_data

def show():
    st.markdown('<div class="section-header">📊 Analytics & Reports</div>', unsafe_allow_html=True)

    pr  = get_pr_data()
    po  = get_po_data()
    gr  = get_gr_data()
    inv = get_invoice_data()
    pay = get_payment_data()

    tab1, tab2, tab3 = st.tabs(["📈 Executive Dashboard", "📉 Spend Analysis", "📋 Custom Reports"])

    # ── Tab 1: Executive Dashboard ────────────────────────────────────────────
    with tab1:
        st.markdown("#### Executive Summary — P2P KPIs")

        # Cycle time simulation
        np.random.seed(5)
        months = ["Oct'24","Nov'24","Dec'24","Jan'25","Feb'25","Mar'25","Apr'25"]
        po_monthly   = np.random.randint(2,8,7)
        inv_monthly  = np.random.randint(3,10,7)
        pay_monthly  = np.random.randint(15,35,7)

        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=po_monthly, name="PR→PO (days)",
                                     mode='lines+markers', line=dict(color="#2E75B6",width=2)))
            fig.add_trace(go.Scatter(x=months, y=inv_monthly, name="PO→Invoice (days)",
                                     mode='lines+markers', line=dict(color="#FFC107",width=2)))
            fig.add_trace(go.Scatter(x=months, y=pay_monthly, name="Invoice→Payment (days)",
                                     mode='lines+markers', line=dict(color="#DC3545",width=2)))
            fig.update_layout(title="📅 Procurement Cycle Times (Days)", height=350,
                              legend=dict(orientation="h",yanchor="bottom",y=-0.4))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            monthly_spend = np.random.randint(800000, 3000000, 7)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=months, y=monthly_spend, marker_color="#2E75B6"))
            fig2.add_trace(go.Scatter(x=months, y=pd.Series(monthly_spend).rolling(3).mean(),
                                      name="3M Avg", line=dict(color="#DC3545",dash="dash")))
            fig2.update_layout(title="💰 Monthly Procurement Spend (₹)", height=350,
                               showlegend=True, legend=dict(orientation="h",yanchor="bottom",y=-0.4))
            st.plotly_chart(fig2, use_container_width=True)

        # Funnel
        col3, col4 = st.columns(2)
        with col3:
            funnel_vals = [len(pr), len(po), len(gr), len(inv), len(pay)]
            funnel_labs = ["Purchase Requisitions","Purchase Orders","Goods Receipts","Invoices Posted","Payments Made"]
            fig3 = go.Figure(go.Funnel(
                y=funnel_labs, x=funnel_vals,
                textinfo="value+percent initial",
                marker=dict(color=["#1F4E79","#2E75B6","#5BA3D4","#9DC3E6","#C8DFF5"])
            ))
            fig3.update_layout(title="🔽 P2P Document Funnel", height=380)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            # Vendor on-time delivery
            vendors = list(set(gr["Vendor"].tolist()))[:5]
            ontime  = np.random.randint(70,98,5)
            fig4 = go.Figure(go.Bar(
                x=ontime, y=vendors[:5], orientation='h',
                marker=dict(color=["#28A745" if v>85 else "#FFC107" if v>75 else "#DC3545" for v in ontime])
            ))
            fig4.add_vline(x=85, line_dash="dash", line_color="#DC3545",
                           annotation_text="Target 85%", annotation_position="top right")
            fig4.update_layout(title="🚚 Vendor On-Time Delivery %", height=380,
                               xaxis=dict(range=[0,100]))
            st.plotly_chart(fig4, use_container_width=True)

    # ── Tab 2: Spend Analysis ─────────────────────────────────────────────────
    with tab2:
        st.markdown("#### Spend Analysis")

        c1, c2 = st.columns(2)
        with c1:
            mat_spend = po.groupby("Description")["PO Value (₹)"].sum().reset_index()
            fig = px.treemap(mat_spend, path=["Description"], values="PO Value (₹)",
                             title="Spend by Material (Treemap)",
                             color="PO Value (₹)", color_continuous_scale="Blues")
            fig.update_layout(height=380)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            vend_spend = po.groupby("Vendor Name")["PO Value (₹)"].sum().reset_index()
            vend_spend["% Share"] = (vend_spend["PO Value (₹)"] / vend_spend["PO Value (₹)"].sum() * 100).round(1)
            fig2 = px.bar(vend_spend, x="Vendor Name", y="PO Value (₹)",
                          title="Vendor-wise Spend",
                          color="PO Value (₹)", color_continuous_scale="Blues",
                          text="% Share")
            fig2.update_traces(texttemplate='%{text}%', textposition='outside')
            fig2.update_layout(height=380, coloraxis_showscale=False, xaxis_tickangle=-20)
            st.plotly_chart(fig2, use_container_width=True)

        # Price variance
        st.markdown("#### 📉 Price Variance Analysis (PO vs Invoice)")
        np.random.seed(7)
        variance_data = pd.DataFrame({
            "Material": po["Description"].head(8),
            "PO Price (₹)": po["Net Price (₹)"].head(8),
            "Invoice Price (₹)": po["Net Price (₹)"].head(8) * np.random.uniform(0.95,1.08,8),
        })
        variance_data["Variance (₹)"] = variance_data["Invoice Price (₹)"] - variance_data["PO Price (₹)"]
        variance_data["Variance %"]    = (variance_data["Variance (₹)"] / variance_data["PO Price (₹)"] * 100).round(2)
        variance_data["Within Tolerance?"] = variance_data["Variance %"].abs().apply(lambda x: "✅ Yes" if x<=5 else "❌ No")

        col5, col6 = st.columns([2,1])
        with col5:
            fig3 = px.bar(variance_data, x="Material", y="Variance %",
                          color="Variance %",
                          color_continuous_scale=["#28A745","#FFC107","#DC3545"],
                          title="Price Variance % (PO vs Invoice)")
            fig3.add_hline(y=5, line_dash="dash", line_color="red", annotation_text="Tolerance Limit 5%")
            fig3.add_hline(y=-5, line_dash="dash", line_color="red")
            fig3.update_layout(height=320, xaxis_tickangle=-30, coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        with col6:
            st.dataframe(variance_data[["Material","Variance %","Within Tolerance?"]],
                         use_container_width=True, height=320)

    # ── Tab 3: Custom Reports ─────────────────────────────────────────────────
    with tab3:
        st.markdown("#### Custom Reports — Download as CSV")

        report_type = st.selectbox("Select Report", [
            "Open Purchase Orders",
            "Blocked Invoices",
            "Overdue Payments",
            "Full P2P Register (All Docs)",
            "Vendor Performance Summary",
        ])

        if report_type == "Open Purchase Orders":
            data = po[po.Status=="Open"]
        elif report_type == "Blocked Invoices":
            data = inv[inv.Status=="Blocked"]
        elif report_type == "Overdue Payments":
            data = pay[pay.Status=="Overdue"]
        elif report_type == "Full P2P Register (All Docs)":
            data = pd.concat([
                pr.rename(columns={"PR Number":"Doc No"}).assign(Type="PR"),
                po.rename(columns={"PO Number":"Doc No"}).assign(Type="PO"),
            ], ignore_index=True)
        else:  # Vendor Performance
            data = pd.DataFrame({
                "Vendor": list(VENDORS.values() if True else VENDORS.values()),
                "POs Raised": [len(po[po["Vendor Name"]==v]) for v in po["Vendor Name"].unique()[:5]],
                "Invoices": [len(inv[inv["Vendor Name"]==v]) for v in inv["Vendor Name"].unique()[:5]],
                "Avg Payment Days": np.random.randint(25,45,5),
                "On-Time Delivery %": np.random.randint(70,98,5),
            })

        st.dataframe(data, use_container_width=True, height=350)
        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button(f"⬇️ Download {report_type} as CSV", csv,
                           file_name=f"{report_type.replace(' ','_').lower()}.csv",
                           mime="text/csv", use_container_width=True)

from data.sample_data import VENDORS
