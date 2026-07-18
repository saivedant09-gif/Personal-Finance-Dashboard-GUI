import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import display
from database import Display_Report
from database import create_database
from database import save_transaction
from database import Delete
from database import Update
from database import Analytics
from database import search

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_database()

if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "del_form" not in st.session_state:
    st.session_state.del_form = False
if "update_form" not in st.session_state:
    st.session_state.update_form = False
if "Search_form" not in st.session_state:
    st.session_state.Search_form = False

st.title("💰 Personal Finance Dashboard")

st.markdown("""
### Manage your income, expenses and savings effortlessly.

Track your financial records with interactive charts and analytics.
""")

st.caption("👨‍💻 Developed by **R Sai Vedant**")

st.divider()

st.subheader("📊 Financial Summary")

report = Display_Report()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 Income",
        f"₹ {report['income']:,.2f}"
    )

with col2:
    st.metric(
        "💸 Expense",
        f"₹ {report['expense']:,.2f}"
    )

with col3:
    st.metric(
        "💰 Savings",
        f"₹ {report['savings']:,.2f}"
    )

st.divider()

st.subheader("📋 My Transactions")

rows = display()

df = pd.DataFrame(
    rows,
    columns=["ID", "Type", "Category", "Amount", "Date"]
)

with st.expander("📄 View Transactions", expanded=True):

    st.data_editor(
        df,
        use_container_width=True
    )

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Transactions as CSV",
    data=csv,
    file_name="transactions.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

with st.sidebar:

    st.title("💰 Finance Manager")

    st.caption("Quick Actions")

    st.divider()

    but1 = st.button("➕ Add Transaction")

    if but1:
        st.session_state.show_form = True

    if st.session_state.show_form:

        with st.form("transaction_form"):

            st.subheader("➕ Add Transaction")
            typ = st.selectbox(
                "Transaction Type",
                ["Income", "Expense"]
            )

            cat = st.text_input("Category")

            amt = st.number_input(
                "Amount",
                min_value=0.0,
                step=1.0
            )

            date = st.date_input(
                "Date",
                value=datetime.today()
            )

            submit = st.form_submit_button(
                "Save Transaction",
                use_container_width=True
            )

            if submit:
                save_transaction(
                    typ,
                    cat,
                    amt,
                    date
                )
                st.success("Transaction Saved Successfully!")
                st.rerun()

    st.divider()

    but2 = st.button("🗑 Delete Transaction")

    if but2:
        st.session_state.del_form = True

    if st.session_state.del_form:

        with st.form("delete_form"):

            st.subheader("🗑 Delete Transaction")

            id1 = st.number_input(
                "Transaction ID",
                min_value=1,
                step=1
            )

            submit = st.form_submit_button(
                "Delete",
                use_container_width=True
            )

            if submit:
                Delete(id1)
                st.success("Transaction Deleted Successfully!")
                st.rerun()

    st.divider()

    but3 = st.button("✏ Update Transaction")

    if but3:
        st.session_state.update_form = True

    if st.session_state.update_form:

        with st.form("update_form"):

            st.subheader("✏ Update Transaction")

            id2 = st.number_input(
                "Transaction ID",
                min_value=1,
                step=1
            )

            typ = st.selectbox(
                "Transaction Type",
                ["Income", "Expense"],
                key="update_type"
            )

            cat = st.text_input(
                "Category",
                key="update_category"
            )

            amt = st.number_input(
                "Amount",
                min_value=0.0,
                step=1.0,
                key="update_amount"
            )

            date = st.date_input(
                "Date",
                key="update_date"
            )

            submit = st.form_submit_button(
                "Update Transaction",
                use_container_width=True
            )

            if submit:
                Update(
                    id2,
                    typ,
                    cat,
                    amt,
                    date
                )
                st.success("Transaction Updated Successfully!")
                st.rerun()

    st.divider()

    st.subheader("🔍 Search")

    search_category = st.text_input(
        "Category",
        placeholder="Example: Food"
    )
    if search_category.strip():

        sear = search(search_category)

        if len(sear) > 0:

            search_df = pd.DataFrame(
                sear,
                columns=["ID", "Type", "Category", "Amount", "Date"]
            )

            st.dataframe(
                search_df,
                use_container_width=True
            )

        else:
            st.warning("No Transactions Found")

st.divider()

st.subheader("📈 Expense Analytics")

ana = Analytics()

df_anal = pd.DataFrame(
    ana,
    columns=["Category", "Amount"]
)

with st.expander("📊 View Expense Summary", expanded=True):

    st.dataframe(
        df_anal,
        use_container_width=True
    )

if not df_anal.empty:

    left, right = st.columns(2)

    fig = px.pie(
        df_anal,
        names="Category",
        values="Amount",
        title="Expense Distribution",
        hole=0.45
    )

    with left:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    fig2 = px.bar(
        df_anal,
        x="Category",
        y="Amount",
        title="Expenses by Category",
        text_auto=True
    )

    with right:
        st.plotly_chart(
            fig2,
            use_container_width=True
        )

else:

    st.info("No expense data available.")

st.divider()

st.success("✅ Personal Finance Dashboard Ready")
st.divider()

st.markdown(
"""
<center>
Made with ❤️ by <b>R Sai Vedant</b><br>
Python • Streamlit • SQLite • Plotly
</center>
""",
unsafe_allow_html=True
)