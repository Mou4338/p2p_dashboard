import streamlit as st
import pandas as pd

def show():
    st.markdown('<div class="section-header">P2P Process Guide — SAP MM Reference</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Process Steps", "T-Code Reference", "Configuration Guide"])

    with tab1:
        st.markdown("### Procure-to-Pay — Complete Process Guide")
        st.markdown(
            "The following section describes each step of the P2P cycle with its purpose, "
            "key fields to fill in SAP, and the expected system output."
        )

        steps = [
            (
                "1", "Purchase Requisition (PR)", "ME51N",
                "An internal request document raised by any department to procure a material or service. "
                "The PR is not sent to the vendor; it is an internal authorization document.",
                [
                    "Document Type: NB (Standard)",
                    "Account Assignment Category: Blank (Stock) or K (Cost Centre)",
                    "Material, Quantity, and Required Delivery Date",
                    "Plant and Storage Location",
                    "Purchasing Group",
                ],
                "PR Number generated (e.g. 1000010001). Status: Open."
            ),
            (
                "2", "Request for Quotation (RFQ)", "ME41",
                "An invitation sent to multiple vendors to submit competitive price quotations. "
                "This step is optional but represents procurement best practice.",
                [
                    "Quotation deadline date",
                    "Collective number for grouping RFQs",
                    "Add 3 or more vendor numbers",
                    "Copy item data from PR using ME54N",
                ],
                "RFQ documents generated and dispatched to vendors. Vendors submit quotations."
            ),
            (
                "3", "Quotation Comparison", "ME49",
                "Compare all vendor quotations on a single screen. SAP highlights the lowest price "
                "in green. Use ME47 to maintain quotation prices received from vendors.",
                [
                    "Enter Collective Number from RFQ",
                    "Select comparison currency",
                    "Set tolerance percentage for price difference",
                ],
                "Best vendor identified and selected. Quotation accepted via ME47."
            ),
            (
                "4", "Purchase Order (PO)", "ME21N",
                "A legally binding procurement document sent to the selected vendor. "
                "Can be created directly from a PR or standalone. Sent to vendor via message output.",
                [
                    "Vendor and Document Type",
                    "Purchasing Org., Purchasing Group, and Company Code",
                    "Payment Terms and Currency",
                    "Material, Quantity, Net Price, and Delivery Date",
                    "Plant and Storage Location",
                ],
                "PO Number generated (e.g. 4500010001). Dispatched to vendor via ME9F / NACE."
            ),
            (
                "5", "Goods Receipt (GR)", "MIGO",
                "When the vendor delivers goods, the warehouse records the receipt in SAP. "
                "This creates a Material Document and an Accounting Document simultaneously.",
                [
                    "Transaction: A01 - Goods Receipt",
                    "Reference Document Type: R01 - Purchase Order",
                    "Movement Type: 101 (GR for PO into Unrestricted Stock)",
                    "Quantity Received and Delivery Note / Challan Number",
                    "Storage Location and Item OK checkbox",
                ],
                "Material Document + Accounting Document created. Unrestricted stock increases."
            ),
            (
                "6", "Invoice Verification", "MIRO",
                "Accounts Payable verifies the vendor invoice against the PO and Goods Receipt "
                "(3-Way Match). If quantities and prices match within tolerance, the invoice is posted. "
                "Mismatches result in automatic invoice blocking.",
                [
                    "Invoice Date, Posting Date, and Amount",
                    "Tax Code (e.g. V0, V1, V2, V3 for GST)",
                    "Reference PO Number (system auto-proposes GR-based items)",
                    "Verify 3-Way Match before posting",
                ],
                "Invoice Document + FI Accounting Document. Vendor liability (payable) created."
            ),
            (
                "7", "Vendor Payment", "F110",
                "The Automatic Payment Program (APP) processes all due vendor invoices in batch "
                "based on payment terms and due dates, generating payment documents and clearing open items.",
                [
                    "Run Date and Run Identification",
                    "Company Code and Payment Method",
                    "Next Payment Date",
                    "Vendor selection (blank = all vendors)",
                ],
                "Payment Document posted. Vendor account cleared. Bank line items created."
            ),
        ]

        for step in steps:
            num, title, tcode, desc, fields, output = step
            with st.expander(f"Step {num}:  {title}   |   T-Code: {tcode}", expanded=False):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Purpose:**  {desc}")
                    st.markdown("**Key Fields to Enter in SAP:**")
                    for f in fields:
                        st.markdown(f"- {f}")
                with col2:
                    st.markdown(
                        f"""<div style='background:#EBF4FF;border-left:4px solid #2E75B6;
                        padding:14px;border-radius:5px;font-size:13px'>
                        <b>Transaction Code:</b><br>{tcode}<br><br>
                        <b>System Output:</b><br>{output}
                        </div>""",
                        unsafe_allow_html=True
                    )

    with tab2:
        st.markdown("### SAP Transaction Code Reference")

        tcodes = {
            "Purchase Requisition": [
                ("ME51N", "Create Purchase Requisition"),
                ("ME52N", "Change Purchase Requisition"),
                ("ME53N", "Display Purchase Requisition"),
                ("ME54N", "Release (Approve) Purchase Requisition"),
                ("ME5A",  "List of Purchase Requisitions"),
            ],
            "RFQ and Quotation": [
                ("ME41", "Create Request for Quotation"),
                ("ME42", "Change RFQ"),
                ("ME47", "Maintain Quotation (Enter Vendor Prices)"),
                ("ME48", "Display Quotation"),
                ("ME49", "Price Comparison List"),
            ],
            "Purchase Order": [
                ("ME21N", "Create Purchase Order"),
                ("ME22N", "Change Purchase Order"),
                ("ME23N", "Display Purchase Order"),
                ("ME2M",  "PO List by Material"),
                ("ME2L",  "PO List by Vendor"),
                ("ME9F",  "Output / Print Purchase Order"),
                ("ME11",  "Create Purchasing Info Record"),
                ("ME01",  "Maintain Source List"),
            ],
            "Goods Receipt": [
                ("MIGO", "Goods Receipt / Goods Issue / Transfer Posting"),
                ("MMBE", "Stock Overview"),
                ("MB51", "Material Document List"),
                ("MB52", "Warehouse Stocks of Material"),
                ("MB1A", "Goods Issue"),
                ("MB90", "Output for Material Documents"),
            ],
            "Invoice Verification": [
                ("MIRO", "Enter Incoming Invoice"),
                ("MIR4", "Display Invoice Document"),
                ("MIR7", "Park Incoming Invoice"),
                ("MRBR", "Release Blocked Invoices"),
                ("MR11", "Maintain GR/IR Clearing Account"),
                ("MR8M", "Cancel Invoice Document"),
            ],
            "Payment (FI Module)": [
                ("F110",  "Automatic Payment Program"),
                ("F-53",  "Post Outgoing Payment (Manual)"),
                ("FBL1N", "Vendor Line Item Report"),
                ("FK03",  "Display Vendor Master (FI View)"),
                ("F-44",  "Clear Vendor Account"),
                ("FF67",  "Manual Bank Statement"),
            ],
            "Master Data": [
                ("MM01", "Create Material Master"),
                ("XK01", "Create Vendor Master (Central)"),
                ("MK01", "Create Vendor Master (Purchasing View)"),
                ("FK01", "Create Vendor Master (Accounting View)"),
                ("ME11", "Create Purchasing Info Record"),
            ],
            "Configuration (SPRO)": [
                ("SPRO", "SAP Implementation Guide (IMG)"),
                ("OX02", "Define Company Code"),
                ("OX10", "Define Plant"),
                ("OX08", "Define Purchasing Organization"),
                ("OME4", "Define Purchasing Group"),
                ("OBYC", "Configure Automatic Account Determination"),
            ],
        }

        for category, codes in tcodes.items():
            st.markdown(f"#### {category}")
            df = pd.DataFrame(codes, columns=["T-Code", "Description"])
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("### SAP MM Configuration Checklist (SPRO)")
        st.info(
            "All configuration steps listed below must be completed in sequence "
            "before any P2P transactions can be executed in SAP."
        )

        config_steps = [
            ("Enterprise Structure", [
                ("OX02", "Define Company Code"),
                ("OX10", "Define Plant"),
                ("OX09", "Define Storage Location"),
                ("OX08", "Define Purchasing Organization"),
                ("OME4", "Define Purchasing Group"),
                ("OX18", "Assign Plant to Company Code"),
                ("OX01", "Assign Purchasing Org. to Company Code"),
                ("OX17", "Assign Purchasing Org. to Plant"),
            ]),
            ("Material Master Configuration", [
                ("OMS2", "Define Material Types"),
                ("OMS9", "Define Field Selection for Material Master"),
                ("MARA", "Define Units of Measure"),
                ("OMSR", "Define Number Ranges for Material Master"),
            ]),
            ("Vendor Master Configuration", [
                ("OBD3", "Define Account Groups for Vendors"),
                ("XKN1", "Define Number Ranges for Vendor Master"),
                ("FK15", "Assign Reconciliation Account to Vendor Group"),
            ]),
            ("Purchasing Configuration", [
                ("OMEF", "Define Number Ranges for Purchasing Documents"),
                ("OMEC", "Define Document Types for Purchase Orders"),
                ("OMEP", "Set Tolerance Keys for Price Variance"),
                ("OMR6", "Set Tolerance Limits for Invoice Verification"),
                ("NACE", "Configure Output (Message) Types for PO Printing"),
            ]),
            ("Inventory and Goods Receipt", [
                ("OMJJ", "Configure Movement Types"),
                ("OMB9", "Define Number Ranges for Material Documents"),
                ("OMWB", "Simulate Account Determination"),
                ("OBYC", "Configure Automatic Postings (Account Determination)"),
            ]),
            ("Invoice Verification", [
                ("OMR6", "Define Tolerance Keys for Invoice Verification"),
                ("OMR7", "Define Number Ranges for Invoice Documents"),
                ("OMRM", "Activate GR-Based Invoice Verification per Plant"),
            ]),
        ]

        for section, items in config_steps:
            with st.expander(f"{section}", expanded=False):
                df = pd.DataFrame(items, columns=["T-Code", "Configuration Step"])
                df["Status"] = "Pending"
                st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown(
            """<div style='background:#D4EDDA;border:1px solid #28A745;border-radius:6px;
            padding:14px 18px;font-size:13px;color:#155724'>
            <b>Important:</b> Always configure in strict sequence — Enterprise Structure first,
            then Master Data, then Purchasing, then Inventory, then Invoice Verification.
            Each configuration layer depends on the preceding one being completed correctly.
            </div>""",
            unsafe_allow_html=True
        )
