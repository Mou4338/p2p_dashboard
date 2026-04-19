import streamlit as st

def show():
    st.markdown('<div class="section-header">ℹ️ P2P Process Guide — SAP MM Reference</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📖 Process Steps", "💻 T-Code Reference", "🔧 Configuration Guide"])

    with tab1:
        st.markdown("### Procure-to-Pay — Complete Process Guide")

        steps = [
            ("1", "📋", "Purchase Requisition (PR)", "ME51N",
             "An internal request document to procure materials/services. Raised by any department.",
             ["Document Type: NB (Standard)","Account Assignment Category","Material, Qty, Required Date","Plant & Storage Location","Purchasing Group"],
             "PR Number generated (e.g. 1000010001). Status: Open."),

            ("2", "📝", "Request for Quotation (RFQ)", "ME41",
             "Invitation to vendors to submit competitive price quotations. Optional but best practice.",
             ["Quotation Deadline","Collective No. for grouping","Add 3+ vendor numbers","Copy from PR using ME54N"],
             "RFQ documents sent to vendors. Vendors submit quotations."),

            ("3", "💰", "Quotation Comparison", "ME49",
             "Compare all vendor quotations on a single screen. SAP highlights the best price in green.",
             ["Enter Collective No. from RFQ","Select currency for comparison","Set tolerance for price difference"],
             "Best vendor identified. Quotation accepted using ME47."),

            ("4", "📦", "Create Purchase Order (PO)", "ME21N",
             "Legally binding document sent to the vendor. Can be created from PR or standalone.",
             ["Vendor + Document Type","Purchasing Org + Group + Company Code","Payment Terms + Currency","Material, Qty, Net Price, Delivery Date","Plant + Storage Location"],
             "PO Number (e.g. 4500010001). Sent to vendor via output (ME9F)."),

            ("5", "🚚", "Goods Receipt (GR)", "MIGO",
             "When vendor delivers goods, warehouse records receipt. Updates stock and creates accounting document.",
             ["Transaction: A01 – Goods Receipt","Reference: R01 – Purchase Order","Movement Type: 101","Qty Received + Delivery Note","Storage Location + Item OK checkbox"],
             "Material Document + Accounting Document. Unrestricted stock increases."),

            ("6", "🧾", "Invoice Verification", "MIRO",
             "Accounts payable verifies vendor invoice against PO and GR (3-Way Match). Posts payable.",
             ["Invoice Date + Amount + Tax Code","Reference PO Number","System auto-proposes GR quantities","Check tolerances for qty/price variance","Post or block if mismatch"],
             "Invoice Document + FI Accounting Document. Vendor payable created."),

            ("7", "💳", "Vendor Payment", "F110",
             "Automatic Payment Program processes all due invoices and makes payment to vendors.",
             ["Run Date + Run ID","Company Code + Payment Method","Next Payment Date","Vendor selection (blank = all)","Execute + Post Payment"],
             "Payment Document. Vendor account cleared. Bank line items created."),
        ]

        for step in steps:
            num, icon, title, tcode, desc, fields, output = step
            with st.expander(f"**Step {num}: {icon} {title}** — T-Code: `{tcode}`", expanded=False):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.markdown(f"**📌 Purpose:** {desc}")
                    st.markdown("**🔑 Key Fields to Enter:**")
                    for f in fields:
                        st.markdown(f"  • {f}")
                with col2:
                    st.markdown(f"""
                    <div style='background:#F0F6FF;border-left:4px solid #2E75B6;padding:12px;border-radius:6px'>
                        <b>T-Code:</b> {tcode}<br><br>
                        <b>Output:</b><br>{output}
                    </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("### SAP Transaction Code Reference")

        tcodes = {
            "Purchase Requisition": [
                ("ME51N","Create Purchase Requisition"),
                ("ME52N","Change Purchase Requisition"),
                ("ME53N","Display Purchase Requisition"),
                ("ME54N","Release (Approve) Purchase Requisition"),
                ("ME5A", "List of Purchase Requisitions"),
            ],
            "RFQ & Quotation": [
                ("ME41","Create Request for Quotation"),
                ("ME42","Change RFQ"),
                ("ME47","Maintain Quotation (Enter Vendor Prices)"),
                ("ME48","Display Quotation"),
                ("ME49","Price Comparison List"),
            ],
            "Purchase Order": [
                ("ME21N","Create Purchase Order"),
                ("ME22N","Change Purchase Order"),
                ("ME23N","Display Purchase Order"),
                ("ME2M","PO List by Material"),
                ("ME2L","PO List by Vendor"),
                ("ME9F","Output/Print Purchase Order"),
                ("ME11","Create Purchasing Info Record"),
                ("ME01","Maintain Source List"),
            ],
            "Goods Receipt": [
                ("MIGO","Goods Receipt / Goods Issue / Transfer Posting"),
                ("MMBE","Stock Overview"),
                ("MB51","Material Document List"),
                ("MB52","Warehouse Stocks of Material"),
                ("MB1A","Goods Issue"),
                ("MB90","Output for Material Documents"),
            ],
            "Invoice Verification": [
                ("MIRO","Enter Incoming Invoice"),
                ("MIR4","Display Invoice Document"),
                ("MIR7","Park Incoming Invoice"),
                ("MRBR","Release Blocked Invoices"),
                ("MR11","Maintain GR/IR Clearing Account"),
                ("MR8M","Cancel Invoice Document"),
            ],
            "Payment (FI)": [
                ("F110","Automatic Payment Program"),
                ("F-53","Post Outgoing Payment (Manual)"),
                ("FBL1N","Vendor Line Items"),
                ("FK03","Display Vendor Master (FI View)"),
                ("F-44","Clear Vendor Account"),
                ("FF67","Manual Bank Statement"),
            ],
            "Master Data": [
                ("MM01","Create Material Master"),
                ("XK01","Create Vendor Master (Central)"),
                ("MK01","Create Vendor Master (Purchasing)"),
                ("FK01","Create Vendor Master (Accounting)"),
                ("ME11","Create Purchasing Info Record"),
            ],
            "Configuration (SPRO)": [
                ("SPRO","SAP IMG – Customizing"),
                ("OX02","Define Company Code"),
                ("OX10","Define Plant"),
                ("OX08","Define Purchasing Organization"),
                ("OME4","Define Purchasing Group"),
                ("OBYC","Configure Automatic Account Determination"),
            ],
        }

        for category, codes in tcodes.items():
            st.markdown(f"#### {category}")
            import pandas as pd
            df = pd.DataFrame(codes, columns=["T-Code","Description"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown("")

    with tab3:
        st.markdown("### SAP MM Configuration Checklist (SPRO)")
        st.info("This checklist covers all mandatory configuration steps for a P2P implementation.")

        config_steps = [
            ("Enterprise Structure", [
                ("OX02", "Define Company Code"),
                ("OX10", "Define Plant"),
                ("OX09", "Define Storage Location"),
                ("OX08", "Define Purchasing Organization"),
                ("OME4","Define Purchasing Group"),
                ("OX18","Assign Plant to Company Code"),
                ("OX01","Assign Purchasing Org. to Company Code"),
                ("OX17","Assign Purchasing Org. to Plant"),
            ]),
            ("Material Master", [
                ("OMS2","Define Material Types"),
                ("OMS9","Define Field Selection for Material Master"),
                ("MARA","Define UOM / Units of Measure"),
                ("OMSR","Define Number Ranges for Material Master"),
            ]),
            ("Vendor Master", [
                ("OBD3","Define Account Groups for Vendors"),
                ("XKN1","Define Number Ranges for Vendor Master"),
                ("FK15","Assign Reconciliation Account"),
            ]),
            ("Purchasing", [
                ("OMEF","Define Number Ranges for PO Documents"),
                ("OMEC","Define Document Types for Purchase Orders"),
                ("OMEP","Set Tolerance Keys for Price Variance"),
                ("OMR6","Set Tolerance Limits for Invoice Verification"),
                ("NACE","Configure Output (Message) for PO printing"),
            ]),
            ("Inventory / Goods Receipt", [
                ("OMJJ","Configure Movement Types"),
                ("OMB9","Define Number Ranges for Material Documents"),
                ("OMWB","Simulate Account Determination"),
                ("OBYC","Configure Automatic Postings (Account Determination)"),
            ]),
            ("Invoice Verification", [
                ("OMR6","Define Tolerance Keys for Invoice Verification"),
                ("OMR7","Define Number Ranges for Invoice Documents"),
                ("OMRM","Activate GR-Based Invoice Verification"),
            ]),
        ]

        for section, items in config_steps:
            with st.expander(f"⚙️ {section}", expanded=False):
                import pandas as pd
                df = pd.DataFrame(items, columns=["T-Code","Configuration Step"])
                df["Done?"] = "☐"
                st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("""
        <div style='background:#D4EDDA;border:1px solid #28A745;border-radius:8px;padding:16px'>
            <b>💡 Pro Tip:</b> Always configure in the order: Enterprise Structure → Master Data → 
            Purchasing Config → Inventory Config → Invoice Verification Config.<br>
            Each step depends on the previous one being completed correctly.
        </div>""", unsafe_allow_html=True)
