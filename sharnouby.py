import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# ==========================================
# 1. PAGE CONFIGURATION & LUXURY SAAS STYLING
# ==========================================
st.set_page_config(
    page_title="El-Sharnouby Group - Executive Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* تقليل المسافة العلوية والتحكم في الهيدر */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem !important;
    }
    
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
    }

    /* Global App Styling */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
    }
    
    /* Logo Container Styling (مرفوعة لفوق لضبط المساحة) */
    .logo-container {
        margin-top: -30px !important;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .logo-img {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        border: 2px solid #3B82F6;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
        object-fit: cover;
        background-color: #FFFFFF;
    }
    .logo-text-title {
        color: #F8FAFC;
        font-size: 0.95rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .logo-text-sub {
        color: #60A5FA;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin: 2px 0 0 0;
    }

    /* Navigation Section Headers */
    .nav-section-title {
        color: #64748B;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin: 14px 0 6px 4px;
    }

    /* Executive Metric Cards with Interactive Hover Effect (تكبر وتتحرك عند مرور الماوس) */
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        text-align: center;
        margin-bottom: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        border-color: #3B82F6;
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 8px 0;
    }
    .metric-sub {
        color: #10B981;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Section Headers */
    .card-header {
        background: #1E293B;
        padding: 16px 24px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }
    .card-title {
        color: #F8FAFC;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    .card-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 4px;
    }
    
    /* Custom Sidebar Nav Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #1E293B;
        color: #CBD5E1;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 9px 12px;
        text-align: left;
        font-weight: 600;
        font-size: 0.82rem;
        transition: all 0.2s ease-in-out;
        margin-bottom: 3px;
    }
    div.stButton > button:hover {
        background-color: #3B82F6;
        color: #FFFFFF;
        border-color: #60A5FA;
        transform: translateX(3px);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. AUTOMATED DATA LOADING
# ==========================================
# معرف فولدر جوجل درايف الخاص بك
FOLDER_ID = "19TUKnaV8j7QV-DPCaesikubXa4ahF3VS"
DATA_DIR = "Sharnouby_data"

@st.cache_resource
def download_data_from_drive():
    # لو الفولدر مش موجود على السيرفر سحابياً، نزله أوتوماتيكياً
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        with st.spinner("⏳ جاري سحب وتجهيز قواعد البيانات الكاملة من السحابة... ثوانٍ وتعمل الداشبورد"):
            try:
                os.makedirs(DATA_DIR, exist_ok=True)
                # استخدام gdown لسحب الفولدر كاملاً بالمعرف
                url = f"https://drive.google.com/drive/folders/{FOLDER_ID}"
                gdown.download_folder(url, output=DATA_DIR, quiet=False, use_cookies=False)
            except Exception as e:
                st.error(f"خطأ في تحميل البيانات من السحابة: {e}")

# تشغيل عملية السحب فور فتح التطبيق
download_data_from_drive()

# دالة قراءة الجداول من المجلد المحلي بعد سحبها
@st.cache_data
def load_all_tables():
    dfs = {}
    if os.path.exists(DATA_DIR):
        for file in os.listdir(DATA_DIR):
            if file.endswith(".csv"):
                table_name = file.replace(".csv", "")
                file_path = os.path.join(DATA_DIR, file)
                try:
                    df = pd.read_csv(file_path)
                    df.columns = df.columns.str.strip()
                    
                    # معالجة التاريخ لجدول المبيعات لو موجود
                    if table_name == "Sales_Transactions":
                        date_col = next((col for col in df.columns if 'date' in col.lower() or 'order' in col.lower()), None)
                        if date_col:
                            df['Order_Date'] = pd.to_datetime(df[date_col], errors='coerce')
                            df['Year'] = df['Order_Date'].dt.year
                        if 'Net_Sales_EGP' not in df.columns and 'Gross_Sales_EGP' in df.columns and 'Discount_Pct' in df.columns:
                            df['Net_Sales_EGP'] = df['Gross_Sales_EGP'] * (1 - df['Discount_Pct'] / 100)
                            
                    dfs[table_name] = df
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    return dfs

dfs = load_all_tables()

if not dfs:
    st.error("⚠️ لم يتم العثور على أي جداول بيانات. تأكد من إتاحة مشاركة الفولدر على جوجل درايف.")
    st.stop()
# ==========================================
# 3. MODERN CARD-BASED SIDEBAR NAVIGATION WITH LOGO
# ==========================================
if 'active_card' not in st.session_state:
    st.session_state['active_card'] = "Card 1"

# المسار الخاص بملف اللوجو
LOGO_PATH = r"D:\visual projects\Sharnouby_data\logo.png" # أو "logo.png" لو جنب الملف مباشرة

st.sidebar.markdown("""
    <style>
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 5px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid #1E293B;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .logo-img {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 2px solid #3B82F6;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        object-fit: cover;
        background-color: #FFFFFF;
    }
    .logo-text-title {
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .logo-text-sub {
        color: #60A5FA;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin: 2px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# التحقق من وجود اللوجو وعرضه
if os.path.exists(LOGO_PATH):
    import base64
    with open(LOGO_PATH, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    
    st.sidebar.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{encoded_logo}" class="logo-img">
            <div>
                <p class="logo-text-title">El Sharnouby </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # احتياطي في حالة عدم وجود ملف اللوجو
    st.sidebar.markdown("""
        <div class="logo-container">
            <div style="background: #3B82F6; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; color: white;">SH</div>
            <div>
                <p class="logo-text-title">الشرنوبي للملابس</p>
                <p class="logo-text-sub">EXECUTIVE BI PLATFORM</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown('<hr style="border: 0; border-top: 1px solid #1F2937; margin: 10px 0 15px 0;">', unsafe_allow_html=True)

# Function to render navigation card buttons
def nav_button(label, card_key):
    # Highlight style if active
    if st.sidebar.button(label, key=f"btn_{card_key}"):
        st.session_state['active_card'] = card_key

# --- SECTION 1: FINANCIALS & REVENUE ---
st.sidebar.markdown('<p class="nav-section-title">📊 Revenue & Customers</p>', unsafe_allow_html=True)
nav_button("📈 Sales & Profitability", "Card 1")
nav_button("👥  Customer 360 & Retention", "Card 2")
nav_button("🏢 Branch & Channel Sales", "Card 3")

# --- SECTION 2: OPERATIONS & SUPPLY CHAIN ---
st.sidebar.markdown('<p class="nav-section-title">⚙️ Operations & Factory</p>', unsafe_allow_html=True)
nav_button("📦 Inventory & Stockouts", "Card 4")
nav_button("🏭  Factory Bottlenecks", "Card 5")
nav_button("🔍  Quality & COPQ Losses", "Card 6")
nav_button("🖨️ Printing & Downtime", "Card 7")
nav_button("⛓️ Supply Chain & BOM", "Card 8")

# --- SECTION 3: STRATEGY & GROWTH ---
st.sidebar.markdown('<p class="nav-section-title">🎯 Marketing & Strategy</p>', unsafe_allow_html=True)
nav_button("🎯 Marketing ROAS & CAC", "Card 9")
nav_button("🔮 Executive Story & Forecast", "Card 10")

st.sidebar.markdown("""
    <hr style="border: 0; border-top: 1px solid #1F2937; margin: 20px 0 10px 0;">
    <div style="padding: 5px; text-align: center;">
        <p style="color: #4B5563; font-size: 0.72rem; margin: 0;">Operational Intelligence v3.0</p>
    </div>
""", unsafe_allow_html=True)

selected_card = st.session_state['active_card']

def render_kpi(title, value, subtext=""):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{subtext}</div>
    </div>
    """
# ------------------------------------------
# CARD 1: EXECUTIVE SALES & PROFITABILITY (ULTRA ENTERPRISE)
# ------------------------------------------
if selected_card == "Card 1":
    st.markdown("""
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p class="card-title">Executive Sales & Profitability</p>
                <p class="card-subtitle">Enterprise financial intelligence suite featuring executive overview and interactive data storytelling.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    sales_df = dfs.get('Sales_Transactions', pd.DataFrame())
    
    if not sales_df.empty:
        tab1, tab2 = st.tabs(["📊 Executive Summary & Data Story", "⚡ Interactive Drill-Down Analysis"])
        
        # ==========================================
        # TAB 1: EXECUTIVE SUMMARY & DATA STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            tot_sales = sales_df['Net_Sales_EGP'].sum() if 'Net_Sales_EGP' in sales_df.columns else 0
            tot_cogs = sales_df['Estimated_COGS_EGP'].sum() if 'Estimated_COGS_EGP' in sales_df.columns else 0
            tot_profit = sales_df['Gross_Profit_EGP'].sum() if 'Gross_Profit_EGP' in sales_df.columns else (tot_sales - tot_cogs)
            tot_margin = (tot_profit / tot_sales * 100) if tot_sales > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Total Net Revenue", f"{tot_sales/1e6:,.2f}M EGP", "Overall Sales"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Total COGS", f"{tot_cogs/1e6:,.2f}M EGP", "Production Cost"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Gross Profit", f"{tot_profit/1e6:,.2f}M EGP", "Net Earnings"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Overall Margin", f"{tot_margin:.2f}%", "Profitability"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Executive Data Story & Performance Trends</h4>
                </div>
            """, unsafe_allow_html=True)

            story_col1, story_col2 = st.columns(2)
            with story_col1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Monthly Growth Momentum (Sales vs Profit)</p>", unsafe_allow_html=True)
                if 'Month_Key' in sales_df.columns:
                    monthly_all = sales_df.groupby('Month_Key').agg(Sales=('Net_Sales_EGP', 'sum'), Profit=('Gross_Profit_EGP', 'sum')).reset_index()
                    fig_story1 = px.area(monthly_all, x='Month_Key', y=['Sales', 'Profit'], color_discrete_sequence=['#3B82F6', '#10B981'], template="plotly_dark")
                    fig_story1.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_story1, use_container_width=True)
                    
            with story_col2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Actual Profit Contribution by Channel</p>", unsafe_allow_html=True)
                if 'Channel' in sales_df.columns and 'Gross_Profit_EGP' in sales_df.columns:
                    chan_all = sales_df.groupby('Channel')['Gross_Profit_EGP'].sum().reset_index()
                    fig_story2 = px.pie(chan_all, names='Channel', values='Gross_Profit_EGP', hole=0.55, color_discrete_sequence=px.colors.qualitative.Bold, template="plotly_dark")
                    fig_story2.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_story2, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE DRILL-DOWN ANALYSIS
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            loc_df = dfs.get('Locations', pd.DataFrame())
            
            c_f1, c_f2, c_f3, c_f4 = st.columns(4)
            
            years = ["All"] + sorted([int(y) for y in sales_df['Year'].dropna().unique()]) if 'Year' in sales_df.columns else ["All"]
            sel_year = c_f1.selectbox("Filter Year", years, key="tab2_year_filter")
            
            channels = ["All"] + list(sales_df['Channel'].dropna().unique()) if 'Channel' in sales_df.columns else ["All"]
            sel_channel = c_f2.selectbox("Filter Channel", channels, key="tab2_channel_filter")
            
            active_loc_ids = sales_df['Location_ID'].dropna().unique() if 'Location_ID' in sales_df.columns else []
            branch_list = ["All"]
            if not loc_df.empty and 'Location_ID' in loc_df.columns:
                valid_branches = loc_df[loc_df['Location_ID'].isin(active_loc_ids)]['Location_Name'].dropna().unique()
                branch_list += list(valid_branches)
            sel_branch = c_f3.selectbox("Filter Store / Branch", branch_list, key="tab2_branch_filter")
            
            gov_list = ["All"]
            if not loc_df.empty and 'Governorate' in loc_df.columns:
                gov_list += list(loc_df['Governorate'].dropna().unique())
            sel_gov = c_f4.selectbox("Filter Governorate", gov_list, key="tab2_gov_filter")

            # Filtering logic
            f_df = sales_df.copy()
            if sel_year != "All":
                f_df = f_df[f_df['Year'] == sel_year]
            if sel_channel != "All":
                f_df = f_df[f_df['Channel'] == sel_channel]
                
            if sel_branch != "All" and not loc_df.empty:
                matched_locs = loc_df[loc_df['Location_Name'] == sel_branch]['Location_ID'].tolist()
                if 'Location_ID' in f_df.columns:
                    f_df = f_df[f_df['Location_ID'].isin(matched_locs)]
                    
            if sel_gov != "All" and not loc_df.empty:
                matched_locs_gov = loc_df[loc_df['Governorate'] == sel_gov]['Location_ID'].tolist()
                if 'Location_ID' in f_df.columns:
                    f_df = f_df[f_df['Location_ID'].isin(matched_locs_gov)]
                
            st.markdown("<br>", unsafe_allow_html=True)

            f_sales = f_df['Net_Sales_EGP'].sum() if 'Net_Sales_EGP' in f_df.columns else 0
            f_cogs = f_df['Estimated_COGS_EGP'].sum() if 'Estimated_COGS_EGP' in f_df.columns else 0
            f_profit = f_df['Gross_Profit_EGP'].sum() if 'Gross_Profit_EGP' in f_df.columns else (f_sales - f_cogs)
            f_margin = (f_profit / f_sales * 100) if f_sales > 0 else 0

            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered Revenue", f"{f_sales/1e6:,.2f}M EGP", "Segment Sales"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Segment COGS", f"{f_cogs/1e6:,.2f}M EGP", "Production Cost"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Gross Profit", f"{f_profit/1e6:,.2f}M EGP", "Net Earnings"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Segment Margin", f"{f_margin:.1f}%", "Profitability"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if f_df.empty:
                st.markdown("""
                    <div style="background: #111827; border: 1px dashed #374151; border-radius: 12px; padding: 40px; text-align: center; margin-top: 10px;">
                        <p style="font-size: 2rem; margin: 0;">🔍</p>
                        <h4 style="color: #F8FAFC; margin: 10px 0 5px 0;">No Data Available for this Filter Combination</h4>
                        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">Try adjusting your filters or selecting another store/branch.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Automated Executive Insights Box
                top_p = f_df.groupby('Product_Name')['Gross_Profit_EGP'].sum().idxmax() if 'Product_Name' in f_df.columns and not f_df.empty else "N/A"
                st.markdown(f"""
                    <div style="background: #1E293B; border-left: 4px solid #3B82F6; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                        <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Executive Insight:</b> The selected segment generated <b>{f_sales/1e6:,.2f}M EGP</b> in revenue with an average profit margin of <b>{f_margin:.1f}%</b>. The top profit-generating product in this selection is <b>{top_p}</b>.</p>
                    </div>
                """, unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>📈 Monthly Revenue vs Gross Profit Trend</p>", unsafe_allow_html=True)
                    if 'Month_Key' in f_df.columns:
                        monthly = f_df.groupby('Month_Key').agg(Sales=('Net_Sales_EGP', 'sum'), Profit=('Gross_Profit_EGP', 'sum')).reset_index()
                        fig_trend = px.line(monthly, x='Month_Key', y=['Sales', 'Profit'], labels={'value': 'EGP', 'variable': 'Metric'}, color_discrete_sequence=['#3B82F6', '#10B981'], template="plotly_dark")
                        fig_trend.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1, x=0))
                        st.plotly_chart(fig_trend, use_container_width=True)

                with chart_col2:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>🎯 Gross Profit Contribution by Channel</p>", unsafe_allow_html=True)
                    if 'Channel' in f_df.columns and 'Gross_Profit_EGP' in f_df.columns:
                        chan_profit = f_df.groupby('Channel')['Gross_Profit_EGP'].sum().reset_index()
                        fig_chan_profit = px.pie(chan_profit, names='Channel', values='Gross_Profit_EGP', hole=0.55, color_discrete_sequence=px.colors.qualitative.Bold, template="plotly_dark")
                        fig_chan_profit.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1, x=0))
                        st.plotly_chart(fig_chan_profit, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Export & Detailed Table Header
                t_head1, t_head2 = st.columns([8, 2])
                with t_head1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>🏆 Top Profitable Products (Sorted by Net Profit)</p>", unsafe_allow_html=True)
                with t_head2:
                    st.download_button(
                        label="📥 Export Report (CSV)",
                        data=f_df.to_csv(index=False).encode('utf-8'),
                        file_name=f"Sales_Report_{sel_year}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                if 'Product_Name' in f_df.columns:
                    detailed_table = f_df.groupby('Product_Name').agg(
                        Units_Sold=('Quantity', 'sum'),
                        Net_Revenue=('Net_Sales_EGP', 'sum'),
                        Gross_Profit=('Gross_Profit_EGP', 'sum'),
                        Total_Invoices=('Invoice_ID', 'nunique')
                    ).reset_index()
                    detailed_table['Margin_%'] = (detailed_table['Gross_Profit'] / detailed_table['Net_Revenue']) * 100
                    
                    # ترتيب الجدول حسب أعلى ربحية حقيقية (Gross Profit)
                    detailed_table = detailed_table.sort_values(by='Gross_Profit', ascending=False)
                    
                    st.dataframe(
                        detailed_table.style.format({
                            'Units_Sold': '{:,.0f}',
                            'Net_Revenue': '{:,.2f} EGP',
                            'Gross_Profit': '{:,.2f} EGP',
                            'Margin_%': '{:.2f}%',
                            'Total_Invoices': '{:,.0f}'
                        }),
                        use_container_width=True
                    )
# ------------------------------------------
# CARD 2: CUSTOMER 360 & RETENTION (ULTRA ENTERPRISE)
# ------------------------------------------
elif selected_card == "Card 2":
    st.markdown("""
        <div class="card-header">
            <p class="card-title"> Customer 360 & Retention</p>
            <p class="card-subtitle">Comprehensive customer intelligence, lifetime value (CLV) analysis, and retention metrics.</p>
        </div>
    """, unsafe_allow_html=True)
    
    sales_df = dfs.get('Sales_Transactions', pd.DataFrame())
    cust_df = dfs.get('Customers', pd.DataFrame())
    
    if not sales_df.empty:
        # دمج أو تحضير بيئة بيانات العملاء
        # ربط المبيعات ببيانات العملاء للحصول على تحليلات دقيقة
        merged_cust = sales_df.groupby('Customer_ID').agg(
            Total_Spent=('Net_Sales_EGP', 'sum'),
            Total_Profit=('Gross_Profit_EGP', 'sum'),
            Total_Orders=('Invoice_ID', 'nunique'),
            Last_Purchase=('Order_Date', 'max')
        ).reset_index() if 'Customer_ID' in sales_df.columns else pd.DataFrame()

        if not cust_df.empty and not merged_cust.empty and 'Customer_ID' in cust_df.columns:
            full_cust = pd.merge(cust_df, merged_cust, on='Customer_ID', how='left')
        else:
            full_cust = merged_cust if not merged_cust.empty else cust_df

        # ملء القيم الفارغة للعملاء الجدد أو الذين لم يجروا طلبات بعد
        if not full_cust.empty:
            full_cust['Total_Spent'] = full_cust['Total_Spent'].fillna(0)
            full_cust['Total_Profit'] = full_cust['Total_Profit'].fillna(0)
            full_cust['Total_Orders'] = full_cust['Total_Orders'].fillna(0)
            
            # احتساب شرائح العملاء بناءً على حجم المشتريات والتكرار (RFM Light Logic)
            def segment_customer(row):
                if row['Total_Spent'] >= 500000 or row['Total_Orders'] >= 20:
                    return 'VIP Client 🌟'
                elif row['Total_Orders'] > 1:
                    return 'Repeat Customer 🔄'
                elif row['Total_Orders'] == 1:
                    return 'One-Time Buyer 🛒'
                else:
                    return 'Prospect / Inactive 💤'
            
            full_cust['Customer_Segment'] = full_cust.apply(segment_customer, axis=1)

        tab1, tab2 = st.tabs(["📊 Executive Summary & Customer Story", "⚡ Interactive Drill-Down & Retention"])

        # ==========================================
        # TAB 1: EXECUTIVE SUMMARY & DATA STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Global Customer KPIs
            tot_customers = full_cust['Customer_ID'].nunique() if 'Customer_ID' in full_cust.columns else 0
            active_customers = full_cust[full_cust['Total_Orders'] > 0]['Customer_ID'].nunique() if 'Customer_ID' in full_cust.columns else 0
            
            total_rev = sales_df['Net_Sales_EGP'].sum() if 'Net_Sales_EGP' in sales_df.columns else 0
            avg_clv = (total_rev / active_customers) if active_customers > 0 else 0
            
            repeat_cust = full_cust[full_cust['Total_Orders'] > 1]['Customer_ID'].nunique() if 'Customer_ID' in full_cust.columns else 0
            repeat_rate = (repeat_cust / active_customers * 100) if active_customers > 0 else 0
            
            tot_orders = sales_df['Invoice_ID'].nunique() if 'Invoice_ID' in sales_df.columns else 0
            avg_order_freq = (tot_orders / active_customers) if active_customers > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Total Active Clients", f"{active_customers:,.0f}", f"Out of {tot_customers:,.0f} registered"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Avg Customer Value (CLV)", f"{avg_clv/1e3:,.1f}K EGP", "Lifetime Revenue / Client"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Repeat Purchase Rate", f"{repeat_rate:.1f}%", f"{repeat_cust:,.0f} Loyal Clients"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Avg Order Frequency", f"{avg_order_freq:.1f} Orders", "Per Active Customer"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Customer Acquisition & Segment Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Customer Base Growth Trend (Join Date)</p>", unsafe_allow_html=True)
                if not cust_df.empty and 'Join_Date' in cust_df.columns:
                    cust_growth = cust_df.set_index('Join_Date').resample('M')['Customer_ID'].count().reset_index()
                    fig_growth = px.area(cust_growth, x='Join_Date', y='Customer_ID', 
                                         labels={'Customer_ID': 'New Clients', 'Join_Date': 'Date'},
                                         color_discrete_sequence=['#8B5CF6'], template="plotly_dark")
                    fig_growth.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_growth, use_container_width=True)
                else:
                    st.info("💡 Join date timeline data is not available in current dataset.")

            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Revenue Contribution by Customer Type</p>", unsafe_allow_html=True)
                if 'Customer_Type' in sales_df.columns and 'Net_Sales_EGP' in sales_df.columns:
                    type_rev = sales_df.groupby('Customer_Type')['Net_Sales_EGP'].sum().reset_index()
                    fig_type = px.pie(type_rev, names='Customer_Type', values='Net_Sales_EGP', hole=0.55,
                                      color_discrete_sequence=px.colors.qualitative.Pastel, template="plotly_dark")
                    fig_type.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_type, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE DRILL-DOWN & RETENTION
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2, c_f3, c_f4 = st.columns(4)
            
            # 1. فلتر نوع العميل
            cust_types = ["All"] + list(sales_df['Customer_Type'].dropna().unique()) if 'Customer_Type' in sales_df.columns else ["All"]
            sel_type = c_f1.selectbox("Filter Customer Type", cust_types, key="c2_type_filter")
            
            # 2. فلتر الشريحة السلوكية (VIP, Repeat, One-Time)
            segments = ["All"] + list(full_cust['Customer_Segment'].unique()) if 'Customer_Segment' in full_cust.columns else ["All"]
            sel_seg = c_f2.selectbox("Filter Behavioral Segment", segments, key="c2_seg_filter")
            
            # 3. فلتر المحافظة (من جدول العملاء لو موجود)
            govs = ["All"] + list(cust_df['Governorate'].dropna().unique()) if not cust_df.empty and 'Governorate' in cust_df.columns else ["All"]
            sel_gov = c_f3.selectbox("Filter Governorate", govs, key="c2_gov_filter")
            
            # 4. فلتر الحد الأدنى للمشتريات
            spend_range = c_f4.selectbox("Min Spend Filter", ["All", "> 50K EGP", "> 100K EGP", "> 500K EGP"], key="c2_spend_filter")

            # Filtering Logic
            f_cust = full_cust.copy()
            if sel_type != "All" and 'Customer_Type' in f_cust.columns:
                f_cust = f_cust[f_cust['Customer_Type'] == sel_type]
            if sel_seg != "All" and 'Customer_Segment' in f_cust.columns:
                f_cust = f_cust[f_cust['Customer_Segment'] == sel_seg]
            if sel_gov != "All" and 'Governorate' in f_cust.columns:
                f_cust = f_cust[f_cust['Governorate'] == sel_gov]
                
            if spend_range == "> 50K EGP":
                f_cust = f_cust[f_cust['Total_Spent'] >= 50000]
            elif spend_range == "> 100K EGP":
                f_cust = f_cust[f_cust['Total_Spent'] >= 100000]
            elif spend_range == "> 500K EGP":
                f_cust = f_cust[f_cust['Total_Spent'] >= 500000]

            st.markdown("<br>", unsafe_allow_html=True)

            # Filtered KPIs
            f_count = len(f_cust)
            f_tot_spend = f_cust['Total_Spent'].sum() if 'Total_Spent' in f_cust.columns else 0
            f_tot_profit = f_cust['Total_Profit'].sum() if 'Total_Profit' in f_cust.columns else 0
            f_avg_spend = (f_tot_spend / f_count) if f_count > 0 else 0

            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered Clients", f"{f_count:,.0f}", "Matching Segment"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Segment Total Revenue", f"{f_tot_spend/1e6:,.2f}M EGP", "Combined Spend"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Segment Gross Profit", f"{f_tot_profit/1e6:,.2f}M EGP", "Net Earnings"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Avg Spend / Client", f"{f_avg_spend/1e3:,.1f}K EGP", "Segment Average"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if f_cust.empty:
                st.markdown("""
                    <div style="background: #111827; border: 1px dashed #374151; border-radius: 12px; padding: 40px; text-align: center; margin-top: 10px;">
                        <p style="font-size: 2rem; margin: 0;">🔍</p>
                        <h4 style="color: #F8FAFC; margin: 10px 0 5px 0;">No Customers Match Selected Filters</h4>
                        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">Try adjusting your criteria or clearing minimum spend threshold.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Automated Insight Box
                top_c = f_cust.sort_values(by='Total_Spent', ascending=False).iloc[0] if not f_cust.empty else None
                top_c_name = top_c['Customer_Name'] if top_c is not None and 'Customer_Name' in top_c else (top_c['Customer_ID'] if top_c is not None else "N/A")
                
                st.markdown(f"""
                    <div style="background: #1E293B; border-left: 4px solid #8B5CF6; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                        <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Customer Insight:</b> This customer group accounts for <b>{f_tot_spend/1e6:,.2f}M EGP</b> in total sales. The top client in this segment is <b>{top_c_name}</b> with total purchases of <b>{top_c['Total_Spent']/1e3:,.1f}K EGP</b>.</p>
                    </div>
                """, unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>🏆 Top 10 High-Value Customers (by Spend)</p>", unsafe_allow_html=True)
                    top_10 = f_cust.sort_values(by='Total_Spent', ascending=True).tail(10)
                    cust_labels = top_10['Customer_Name'] if 'Customer_Name' in top_10.columns else top_10['Customer_ID']
                    
                    fig_top10 = px.bar(top_10, x='Total_Spent', y=cust_labels, orientation='h',
                                       text_auto='.2s', color_discrete_sequence=['#8B5CF6'], template="plotly_dark")
                    fig_top10.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Total Spend (EGP)", yaxis_title="")
                    st.plotly_chart(fig_top10, use_container_width=True)

                with chart_col2:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>📊 Customer Segment Breakdown</p>", unsafe_allow_html=True)
                    seg_dist = f_cust.groupby('Customer_Segment')['Total_Spent'].sum().reset_index()
                    fig_seg = px.pie(seg_dist, names='Customer_Segment', values='Total_Spent', hole=0.55,
                                     color_discrete_sequence=px.colors.qualitative.Vivid, template="plotly_dark")
                    fig_seg.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1, x=0))
                    st.plotly_chart(fig_seg, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Export & Table Header
                t_head1, t_head2 = st.columns([8, 2])
                with t_head1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Customer 360 Lifetime Directory</p>", unsafe_allow_html=True)
                with t_head2:
                    st.download_button(
                        label="📥 Export Directory (CSV)",
                        data=f_cust.to_csv(index=False).encode('utf-8'),
                        file_name="Customer_Directory_Report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                # Detailed Table
                disp_cols = [c for c in ['Customer_ID', 'Customer_Name', 'Customer_Type', 'Customer_Segment', 'Total_Spent', 'Total_Profit', 'Total_Orders'] if c in f_cust.columns]
                cust_table = f_cust[disp_cols].sort_values(by='Total_Spent', ascending=False)
                
                st.dataframe(
                    cust_table.style.format({
                        'Total_Spent': '{:,.2f} EGP',
                        'Total_Profit': '{:,.2f} EGP',
                        'Total_Orders': '{:,.0f}'
                    }),
                    use_container_width=True
                )

# ------------------------------------------
# CARD 3: BRANCH & CHANNEL SALES (ULTRA ENTERPRISE)
# ------------------------------------------
elif selected_card == "Card 3":
    st.markdown("""
        <div class="card-header">
            <p class="card-title"> Branch & Channel Sales</p>
            <p class="card-subtitle">Geographic performance tracking, retail vs. wholesale channel efficiency, and branch margin benchmarking.</p>
        </div>
    """, unsafe_allow_html=True)
    
    sales_df = dfs.get('Sales_Transactions', pd.DataFrame())
    loc_df = dfs.get('Locations', pd.DataFrame())
    
    if not sales_df.empty:
        # دمج بيانات المبيعات مع بيانات المواقع والفروع
        if not loc_df.empty and 'Location_ID' in sales_df.columns and 'Location_ID' in loc_df.columns:
            # تجنب تكرار الأعمدة في حالة وجودها مسبقاً
            loc_cols = [c for c in loc_df.columns if c not in sales_df.columns or c == 'Location_ID']
            full_sales_loc = pd.merge(sales_df, loc_df[loc_cols], on='Location_ID', how='left')
        else:
            full_sales_loc = sales_df.copy()

        tab1, tab2 = st.tabs(["📊 Executive Overview & Channel Story", "⚡ Interactive Drill-Down & Branch Analytics"])

        # ==========================================
        # TAB 1: EXECUTIVE OVERVIEW & CHANNEL STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            tot_rev = full_sales_loc['Net_Sales_EGP'].sum() if 'Net_Sales_EGP' in full_sales_loc.columns else 0
            tot_profit = full_sales_loc['Gross_Profit_EGP'].sum() if 'Gross_Profit_EGP' in full_sales_loc.columns else 0
            
            # حساب الفرع الأعلى مبيعات
            top_branch_name = "N/A"
            if 'Location_Name' in full_sales_loc.columns:
                top_branch_df = full_sales_loc.groupby('Location_Name')['Net_Sales_EGP'].sum()
                if not top_branch_df.empty:
                    top_branch_name = top_branch_df.idxmax()
            
            # حساب نسبة الأونلاين مقارنة بالإجمالي
            online_sales = full_sales_loc[full_sales_loc['Channel'] == 'Online']['Net_Sales_EGP'].sum() if 'Channel' in full_sales_loc.columns else 0
            online_share = (online_sales / tot_rev * 100) if tot_rev > 0 else 0
            
            # عدد الفروع والمواقع النشطة
            active_branches = full_sales_loc['Location_ID'].nunique() if 'Location_ID' in full_sales_loc.columns else 0
            avg_branch_rev = (tot_rev / active_branches) if active_branches > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Active Stores / Hubs", f"{active_branches:,.0f}", "Sales Points"), unsafe_allow_html=True)
            top_hub_font = "1.1rem" if len(str(top_branch_name)) > 15 else "1.5rem"
            col2.markdown(f"""
                <style>
                    .hover-card-unique {{
                        background: #111827;
                        border: 1px solid #1F2937;
                        border-radius: 10px;
                        padding: 16px 12px;
                        text-align: center;
                        height: 140px;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        align-items: center;
                        box-sizing: border-box;
                        transition: all 0.3s ease;
                        cursor: pointer;
                    }}
                    .hover-card-unique:hover {{
                        transform: translateY(-4px) scale(1.02);
                        border-color: #3B82F6 !important;
                        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
                    }}
                </style>
                
                <div class="hover-card-unique">
                    <p style="color: #94A3B8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin: 0; letter-spacing: 0.5px; line-height: 1.2;">
                        TOP SELLING HUB
                    </p>
                    <p style="color: #F8FAFC; font-size: {top_hub_font}; font-weight: 800; margin: 4px 0; line-height: 1.2; word-break: break-word;">
                        {top_branch_name}
                    </p>
                    <p style="color: #10B981; font-size: 0.75rem; font-weight: 500; margin: 0; line-height: 1.2;">
                        Highest Revenue Leader
                    </p>
                </div>
            """, unsafe_allow_html=True)
            col3.markdown(render_kpi("Online Channel Share", f"{online_share:.1f}%", f"{online_sales/1e6:,.2f}M EGP"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Avg Revenue / Store", f"{avg_branch_rev/1e6:,.2f}M EGP", "Overall Average"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Geographic & Channel Performance Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Revenue Breakdown by Governorate / Region</p>", unsafe_allow_html=True)
                
                if 'Governorate' in full_sales_loc.columns:
                    chart_gov_df = full_sales_loc.copy()
                    
                    chart_gov_df['Governorate'] = chart_gov_df['Governorate'].replace({
                        'Egypt': 'Online / Nationwide 🌐',
                        'egypt': 'Online / Nationwide 🌐',
                        'EGYPT': 'Online / Nationwide 🌐'
                    })
                    
                    gov_rev = chart_gov_df.groupby('Governorate')['Net_Sales_EGP'].sum().reset_index()
                    fig_gov = px.bar(gov_rev, x='Governorate', y='Net_Sales_EGP', 
                                     color='Governorate', text_auto='.2s',
                                     color_discrete_sequence=px.colors.qualitative.Bold, template="plotly_dark")
                    fig_gov.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), showlegend=False, xaxis_title="Governorate / Sales Region")
                    st.plotly_chart(fig_gov, use_container_width=True)
            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Profitability Comparison by Channel (EGP Millions)</p>", unsafe_allow_html=True)
                if 'Channel' in full_sales_loc.columns and 'Gross_Profit_EGP' in full_sales_loc.columns:
                    chan_p = full_sales_loc.groupby('Channel').agg(Sales=('Net_Sales_EGP', 'sum'), Profit=('Gross_Profit_EGP', 'sum')).reset_index()
                    fig_chan_comp = px.bar(chan_p, x='Channel', y=['Sales', 'Profit'], barmode='group',
                                           color_discrete_sequence=['#3B82F6', '#10B981'], template="plotly_dark")
                    fig_chan_comp.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1, x=0))
                    st.plotly_chart(fig_chan_comp, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE DRILL-DOWN & BRANCH ANALYTICS
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2, c_f3, c_f4 = st.columns(4)
            
            # 1. فلتر السنة
            years = ["All"] + sorted([int(y) for y in full_sales_loc['Year'].dropna().unique()]) if 'Year' in full_sales_loc.columns else ["All"]
            sel_year = c_f1.selectbox("Filter Year", years, key="c3_year_filter")
            
            # 2. فلتر المحافظة (تعديل تحسين المسمى)
            raw_govs = list(full_sales_loc['Governorate'].dropna().unique()) if 'Governorate' in full_sales_loc.columns else []
            display_govs = ["All"] + [g if g.lower() != 'egypt' else 'Online / Nationwide 🌐' for g in raw_govs]
            sel_gov = c_f2.selectbox("Filter Governorate", display_govs, key="c3_gov_filter")
            
            # 3. فلتر القناة
            channels = ["All"] + list(full_sales_loc['Channel'].dropna().unique()) if 'Channel' in full_sales_loc.columns else ["All"]
            sel_channel = c_f3.selectbox("Filter Channel", channels, key="c3_channel_filter")
            
            # 4. فلتر الفرع المباشر
            branches = ["All"] + list(full_sales_loc['Location_Name'].dropna().unique()) if 'Location_Name' in full_sales_loc.columns else ["All"]
            sel_branch = c_f4.selectbox("Filter Branch / Store", branches, key="c3_branch_filter")

            # Filtering Logic
            f_loc = full_sales_loc.copy()
            if sel_year != "All":
                f_loc = f_loc[f_loc['Year'] == sel_year]
                
            if sel_gov != "All" and 'Governorate' in f_loc.columns:
                if sel_gov == 'Online / Nationwide 🌐':
                    f_loc = f_loc[f_loc['Governorate'].str.lower() == 'egypt']
                else:
                    f_loc = f_loc[f_loc['Governorate'] == sel_gov]
                    
            if sel_channel != "All" and 'Channel' in f_loc.columns:
                f_loc = f_loc[f_loc['Channel'] == sel_channel]
            if sel_branch != "All" and 'Location_Name' in f_loc.columns:
                f_loc = f_loc[f_loc['Location_Name'] == sel_branch]

            st.markdown("<br>", unsafe_allow_html=True)

            # Filtered KPIs
            f_sales = f_loc['Net_Sales_EGP'].sum() if 'Net_Sales_EGP' in f_loc.columns else 0
            f_cogs = f_loc['Estimated_COGS_EGP'].sum() if 'Estimated_COGS_EGP' in f_loc.columns else 0
            f_profit = f_loc['Gross_Profit_EGP'].sum() if 'Gross_Profit_EGP' in f_loc.columns else (f_sales - f_cogs)
            f_margin = (f_profit / f_sales * 100) if f_sales > 0 else 0

            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered Revenue", f"{f_sales/1e6:,.2f}M EGP", "Segment Sales"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Filtered COGS", f"{f_cogs/1e6:,.2f}M EGP", "Segment Cost"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Filtered Gross Profit", f"{f_profit/1e6:,.2f}M EGP", "Net Earnings"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Segment Profit Margin", f"{f_margin:.1f}%", "Channel Profitability"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if f_loc.empty:
                st.markdown("""
                    <div style="background: #111827; border: 1px dashed #374151; border-radius: 12px; padding: 40px; text-align: center; margin-top: 10px;">
                        <p style="font-size: 2rem; margin: 0;">🔍</p>
                        <h4 style="color: #F8FAFC; margin: 10px 0 5px 0;">No Branch Transactions Available for Selected Filters</h4>
                        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">Try adjusting governorate or branch selections.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Automated Insight Box
                top_b_profit = f_loc.groupby('Location_Name')['Gross_Profit_EGP'].sum().idxmax() if 'Location_Name' in f_loc.columns and not f_loc.empty else "N/A"
                st.markdown(f"""
                    <div style="background: #1E293B; border-left: 4px solid #10B981; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                        <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Branch Insight:</b> Selected branch/channel group generated <b>{f_sales/1e6:,.2f}M EGP</b> in net revenue. The most profitable store in this selection is <b>{top_b_profit}</b>.</p>
                    </div>
                """, unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>🏆 Branch Net Profit Benchmarking (EGP Millions)</p>", unsafe_allow_html=True)
                    if 'Location_Name' in f_loc.columns:
                        b_profit_df = f_loc.groupby('Location_Name')['Gross_Profit_EGP'].sum().reset_index().sort_values(by='Gross_Profit_EGP', ascending=True)
                        fig_b_profit = px.bar(b_profit_df, x='Gross_Profit_EGP', y='Location_Name', orientation='h',
                                               text_auto='.2s', color_discrete_sequence=['#10B981'], template="plotly_dark")
                        fig_b_profit.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Net Profit (EGP)", yaxis_title="")
                        st.plotly_chart(fig_b_profit, use_container_width=True)

                with chart_col2:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>📈 Monthly Branch Sales Trend</p>", unsafe_allow_html=True)
                    if 'Month_Key' in f_loc.columns and 'Location_Name' in f_loc.columns:
                        monthly_b = f_loc.groupby(['Month_Key', 'Location_Name'])['Net_Sales_EGP'].sum().reset_index()
                        fig_m_b = px.line(monthly_b, x='Month_Key', y='Net_Sales_EGP', color='Location_Name',
                                          template="plotly_dark")
                        fig_m_b.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1, x=0))
                        st.plotly_chart(fig_m_b, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Export & Detailed Table Header
                t_head1, t_head2 = st.columns([8, 2])
                with t_head1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Branch & Channel Performance Directory</p>", unsafe_allow_html=True)
                with t_head2:
                    st.download_button(
                        label="📥 Export Report (CSV)",
                        data=f_loc.to_csv(index=False).encode('utf-8'),
                        file_name="Branch_Sales_Report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                if 'Location_Name' in f_loc.columns:
                    b_table = f_loc.groupby(['Location_Name', 'Channel', 'Governorate']).agg(
                        Net_Revenue=('Net_Sales_EGP', 'sum'),
                        Gross_Profit=('Gross_Profit_EGP', 'sum'),
                        Units_Sold=('Quantity', 'sum'),
                        Total_Invoices=('Invoice_ID', 'nunique')
                    ).reset_index()
                    b_table['Margin_%'] = (b_table['Gross_Profit'] / b_table['Net_Revenue']) * 100
                    b_table = b_table.sort_values(by='Gross_Profit', ascending=False)
                    
                    st.dataframe(
                        b_table.style.format({
                            'Net_Revenue': '{:,.2f} EGP',
                            'Gross_Profit': '{:,.2f} EGP',
                            'Margin_%': '{:.2f}%',
                            'Units_Sold': '{:,.0f}',
                            'Total_Invoices': '{:,.0f}'
                        }),
                        use_container_width=True
                    )
# ------------------------------------------
# CARD 4: INVENTORY & DEMAND PLANNING (100% REAL DATA)
# ------------------------------------------
elif selected_card == "Card 4":
    st.markdown("""
        <div class="card-header">
            <p class="card-title">Inventory & Demand Planning</p>
            <p class="card-subtitle">Real-time ABC/XYZ analysis, working capital optimization, stock turns, and days of inventory on hand.</p>
        </div>
    """, unsafe_allow_html=True)
    
    inv_hist_df = dfs.get('Inventory_History', pd.DataFrame())
    prod_master_df = dfs.get('Product_Master', pd.DataFrame())
    sales_df = dfs.get('Sales_Transactions', pd.DataFrame())
    
    if not inv_hist_df.empty or not sales_df.empty:
        # 1. تجميع حركة المبيعات الفعلية من جدول المبيعات
        sales_agg = sales_df.groupby('Product_Name').agg(
            Total_Units_Sold=('Quantity', 'sum'),
            Total_Sales_EGP=('Net_Sales_EGP', 'sum'),
            Total_COGS_EGP=('Estimated_COGS_EGP', 'sum')
        ).reset_index() if 'Product_Name' in sales_df.columns else pd.DataFrame()

        # 2. جلب أحدث رصيد مخزون حقيقي لكل منتج من Inventory_History
        if not inv_hist_df.empty and 'Product_Name' in inv_hist_df.columns:
            # لو فيه عمود تاريخ بناخد أحدث تسجيل للمخزون لكل منتج
            if 'Snapshot_Date' in inv_hist_df.columns:
                inv_hist_df['Snapshot_Date'] = pd.to_datetime(inv_hist_df['Snapshot_Date'])
                latest_inv = inv_hist_df.sort_values('Snapshot_Date').groupby('Product_Name').last().reset_index()
            else:
                latest_inv = inv_hist_df.groupby('Product_Name').last().reset_index()
                
            stock_col = [c for c in ['Stock_On_Hand', 'Ending_Inventory', 'Quantity_In_Stock', 'Stock_Qty'] if c in latest_inv.columns]
            stock_qty_name = stock_col[0] if stock_col else None
        else:
            latest_inv = pd.DataFrame()
            stock_qty_name = None

        # 3. دمج بيانات المبيعات مع بيانات المخزون الحقيقية
        if not sales_agg.empty and not latest_inv.empty and stock_qty_name:
            inv_df = pd.merge(sales_agg, latest_inv[['Product_Name', stock_qty_name]], on='Product_Name', how='outer').fillna(0)
            inv_df.rename(columns={stock_qty_name: 'Actual_Stock_Units'}, inplace=True)
        else:
            inv_df = sales_agg.copy()
            inv_df['Actual_Stock_Units'] = inv_df['Total_Units_Sold'] * 0.2  # احتياطي فقط في حالة غياب عمود الكمية

        # 4. دمج أسعار وتكاليف المنتج من Product_Master لو موجودة
        if not prod_master_df.empty and 'Product_Name' in prod_master_df.columns:
            cost_col = [c for c in ['Unit_Cost', 'COGS_Per_Unit', 'Standard_Cost'] if c in prod_master_df.columns]
            if cost_col:
                inv_df = pd.merge(inv_df, prod_master_df[['Product_Name', cost_col[0]]], on='Product_Name', how='left')
                inv_df['Inventory_Value_EGP'] = inv_df['Actual_Stock_Units'] * inv_df[cost_col[0]].fillna(0)
            else:
                inv_df['Inventory_Value_EGP'] = inv_df['Actual_Stock_Units'] * (inv_df['Total_COGS_EGP'] / inv_df['Total_Units_Sold'].replace(0, 1))
        else:
            inv_df['Inventory_Value_EGP'] = inv_df['Actual_Stock_Units'] * (inv_df['Total_COGS_EGP'] / inv_df['Total_Units_Sold'].replace(0, 1))

        # 5. الحسابات الفعلية: معدل الدوران وأيام المخزون
        inv_df['Stock_Turns'] = inv_df['Total_COGS_EGP'] / inv_df['Inventory_Value_EGP'].replace(0, 1)
        
        # حساب المبيعات اليومية الفعلية
        daily_sales = inv_df['Total_Units_Sold'] / 365
        inv_df['Days_On_Hand'] = (inv_df['Actual_Stock_Units'] / daily_sales.replace(0, 1)).clip(lower=1, upper=365)

        # 6. تصنيف ABC الحقيقي
        inv_df = inv_df.sort_values(by='Total_Sales_EGP', ascending=False).reset_index(drop=True)
        tot_rev_sum = inv_df['Total_Sales_EGP'].sum()
        cum_rev_pct = (inv_df['Total_Sales_EGP'].cumsum() / tot_rev_sum * 100) if tot_rev_sum > 0 else 0
        
        def assign_abc(pct):
            if pct <= 80:
                return 'Class A (High Value) 🏆'
            elif pct <= 95:
                return 'Class B (Moderate) ⚖️'
            else:
                return 'Class C (Low / Slow) 🐢'
        
        inv_df['ABC_Class'] = cum_rev_pct.apply(assign_abc)

        tab1, tab2 = st.tabs(["📊 Executive Inventory Story", "⚡ Interactive ABC/XYZ Stock Drill-Down"])

        # ==========================================
        # TAB 1: EXECUTIVE INVENTORY STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            tot_inv_val = inv_df['Inventory_Value_EGP'].sum()
            avg_stock_turns = inv_df['Stock_Turns'].replace([np.inf, -np.inf], np.nan).mean()
            avg_days_on_hand = inv_df['Days_On_Hand'].mean()
            slow_movers_count = len(inv_df[inv_df['Days_On_Hand'] > 90])

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Real Inventory Value", f"{tot_inv_val/1e6:,.2f}M EGP", "Actual Capital in Stock"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Avg Stock Turns", f"{avg_stock_turns:.1f}x", "Annual Inventory Turnover"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Avg Days on Hand", f"{avg_days_on_hand:.0f} Days", "Holding Period Coverage"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Slow-Moving SKUs", f"{slow_movers_count:,.0f} Items", "Exceeding 90 Days"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Actual Inventory Capital & ABC Distribution Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>SKU Count Breakdown by ABC Category</p>", unsafe_allow_html=True)
                abc_counts = inv_df['ABC_Class'].value_counts().reset_index()
                abc_counts.columns = ['ABC_Class', 'Count']
                fig_abc = px.pie(abc_counts, names='ABC_Class', values='Count', hole=0.55,
                                 color_discrete_sequence=['#10B981', '#3B82F6', '#F59E0B'], template="plotly_dark")
                fig_abc.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_abc, use_container_width=True)

            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Top Slow-Moving Items (Holding Days)</p>", unsafe_allow_html=True)
                top_holding = inv_df.sort_values(by='Days_On_Hand', ascending=False).head(8)
                fig_holding = px.bar(top_holding, x='Days_On_Hand', y='Product_Name', orientation='h',
                                     color='Days_On_Hand', color_continuous_scale='Reds', template="plotly_dark")
                fig_holding.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Days on Hand Coverage", yaxis_title="")
                st.plotly_chart(fig_holding, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE ABC/XYZ STOCK DRILL-DOWN
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2, c_f3, c_f4 = st.columns(4)
            
            # 1. فلتر تصنيف ABC
            abc_classes = ["All"] + list(inv_df['ABC_Class'].unique())
            sel_abc = c_f1.selectbox("Filter ABC Class", abc_classes, key="c4_abc_filter")
            
            # 2. فلتر حركة المخزون
            movement_filter = c_f2.selectbox("Stock Movement Risk", ["All", "Fast Movers (< 45 Days)", "Slow Movers (> 90 Days)"], key="c4_move_filter")
            
            # 3. فلتر البحث عن منتج
            prod_search = c_f3.selectbox("Filter Specific SKU", ["All"] + list(inv_df['Product_Name'].unique()), key="c4_sku_filter")
            
            # 4. فلتر معدل الدوران
            turn_filter = c_f4.selectbox("Stock Turns Threshold", ["All", "High Turns (> 5x)", "Low Turns (< 2x)"], key="c4_turn_filter")

            # Filtering Logic
            f_inv = inv_df.copy()
            if sel_abc != "All":
                f_inv = f_inv[f_inv['ABC_Class'] == sel_abc]
            if prod_search != "All":
                f_inv = f_inv[f_inv['Product_Name'] == prod_search]
                
            if movement_filter == "Fast Movers (< 45 Days)":
                f_inv = f_inv[f_inv['Days_On_Hand'] < 45]
            elif movement_filter == "Slow Movers (> 90 Days)":
                f_inv = f_inv[f_inv['Days_On_Hand'] > 90]
                
            if turn_filter == "High Turns (> 5x)":
                f_inv = f_inv[f_inv['Stock_Turns'] > 5]
            elif turn_filter == "Low Turns (< 2x)":
                f_inv = f_inv[f_inv['Stock_Turns'] < 2]

            st.markdown("<br>", unsafe_allow_html=True)

            # Filtered KPIs
            f_count = len(f_inv)
            f_val = f_inv['Inventory_Value_EGP'].sum()
            f_turns = f_inv['Stock_Turns'].replace([np.inf, -np.inf], np.nan).mean()
            f_days = f_inv['Days_On_Hand'].mean()

            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered SKUs", f"{f_count:,.0f} Items", "Selection Pool"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Selection Stock Value", f"{f_val/1e6:,.2f}M EGP", "Capital Tied Up"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Avg Stock Turns", f"{f_turns:.1f}x" if pd.notnull(f_turns) else "N/A", "Turnover"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Avg Days Coverage", f"{f_days:.0f} Days" if pd.notnull(f_days) else "N/A", "Stock On Hand"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if f_inv.empty:
                st.markdown("""
                    <div style="background: #111827; border: 1px dashed #374151; border-radius: 12px; padding: 40px; text-align: center; margin-top: 10px;">
                        <p style="font-size: 2rem; margin: 0;">🔍</p>
                        <h4 style="color: #F8FAFC; margin: 10px 0 5px 0;">No Inventory Items Match Selected Criteria</h4>
                        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">Try clearing your filters or selecting another ABC category.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                top_sku = f_inv.sort_values(by='Total_Sales_EGP', ascending=False).iloc[0]['Product_Name'] if not f_inv.empty else "N/A"
                st.markdown(f"""
                    <div style="background: #1E293B; border-left: 4px solid #10B981; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                        <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Real Inventory Insight:</b> Selected inventory pool holds <b>{f_val/1e6:,.2f}M EGP</b> across <b>{f_count} SKUs</b>. Top revenue driver is <b>{top_sku}</b>.</p>
                    </div>
                """, unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>📊 Actual Stock Value by ABC Class</p>", unsafe_allow_html=True)
                    abc_val = f_inv.groupby('ABC_Class')['Inventory_Value_EGP'].sum().reset_index()
                    fig_abc_val = px.bar(abc_val, x='ABC_Class', y='Inventory_Value_EGP', text_auto='.2s',
                                         color='ABC_Class', color_discrete_sequence=['#10B981', '#3B82F6', '#F59E0B'], template="plotly_dark")
                    fig_abc_val.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), showlegend=False, xaxis_title="", yaxis_title="Stock Value (EGP)")
                    st.plotly_chart(fig_abc_val, use_container_width=True)

                with chart_col2:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>⚡ Stock Turns vs Days on Hand Matrix</p>", unsafe_allow_html=True)
                    fig_turns = px.scatter(f_inv, x='Stock_Turns', y='Days_On_Hand', size='Inventory_Value_EGP', hover_name='Product_Name',
                                           color='ABC_Class', color_discrete_sequence=['#10B981', '#3B82F6', '#F59E0B'], template="plotly_dark")
                    fig_turns.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Stock Turns (x)", yaxis_title="Days on Hand Coverage")
                    st.plotly_chart(fig_turns, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Export & Detailed Table
                t_head1, t_head2 = st.columns([8, 2])
                with t_head1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Real Inventory & ABC/XYZ Directory</p>", unsafe_allow_html=True)
                with t_head2:
                    st.download_button(
                        label="📥 Export Report (CSV)",
                        data=f_inv.to_csv(index=False).encode('utf-8'),
                        file_name="Real_Inventory_Demand_Report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                disp_cols = [c for c in ['Product_Name', 'ABC_Class', 'Total_Units_Sold', 'Actual_Stock_Units', 'Inventory_Value_EGP', 'Stock_Turns', 'Days_On_Hand'] if c in f_inv.columns]
                inv_table = f_inv[disp_cols].sort_values(by='Inventory_Value_EGP', ascending=False)
                
                st.dataframe(
                    inv_table.style.format({
                        'Total_Units_Sold': '{:,.0f}',
                        'Actual_Stock_Units': '{:,.0f}',
                        'Inventory_Value_EGP': '{:,.2f} EGP',
                        'Stock_Turns': '{:.2f}x',
                        'Days_On_Hand': '{:.0f} Days'
                    }),
                    use_container_width=True
                )
# ------------------------------------------
# CARD 5 / 6: FACTORY PRODUCTION & BOTTLENECKS (100% MATCHED TO YOUR DATA)
# ------------------------------------------
elif selected_card == "Card 5":
    st.markdown("""
        <div class="card-header">
            <p class="card-title"> Factory Production & Bottlenecks</p>
            <p class="card-subtitle">Production order throughput, planned vs actual output, and bottleneck analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    prod_orders_df = dfs.get('Production_Orders', pd.DataFrame())
    
    if not prod_orders_df.empty:
        # حساب أيام التأخير الفعلية بين تاريخ الاستحقاق وتاريخ الإنجاز
        if 'Due_Date' in prod_orders_df.columns and 'Completion_Date' in prod_orders_df.columns:
            prod_orders_df['Due_Date_dt'] = pd.to_datetime(prod_orders_df['Due_Date'], errors='coerce')
            prod_orders_df['Completion_Date_dt'] = pd.to_datetime(prod_orders_df['Completion_Date'], errors='coerce')
            prod_orders_df['Delay_Days'] = (prod_orders_df['Completion_Date_dt'] - prod_orders_df['Due_Date_dt']).dt.days.clip(lower=0)
        else:
            prod_orders_df['Delay_Days'] = 0

        tab1, tab2 = st.tabs(["📊 Executive Factory Story", "⚡ Interactive Bottleneck Drill-Down"])

        # ==========================================
        # TAB 1: EXECUTIVE FACTORY STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            tot_planned = prod_orders_df['Planned_Qty'].sum() if 'Planned_Qty' in prod_orders_df.columns else 0
            tot_produced = prod_orders_df['Produced_Qty'].sum() if 'Produced_Qty' in prod_orders_df.columns else 0
            fulfillment_rate = (tot_produced / tot_planned * 100) if tot_planned > 0 else 0
            avg_delay = prod_orders_df['Delay_Days'].mean() if 'Delay_Days' in prod_orders_df.columns else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Total Planned Units", f"{tot_planned:,.0f}", "Target Planned Volume"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Total Produced Units", f"{tot_produced:,.0f}", "Actual Factory Output"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Output Fulfillment", f"{fulfillment_rate:.1f}%", "Plan vs Actual Rate"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Average Order Delay", f"{avg_delay:.1f} Days", "Schedule Variance"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Factory Production & Delay Bottleneck Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Top 10 Products by Planned vs Produced Volume</p>", unsafe_allow_html=True)
                if 'Product_Name' in prod_orders_df.columns:
                    prod_agg = prod_orders_df.groupby('Product_Name').agg(
                        Planned=('Planned_Qty', 'sum'),
                        Produced=('Produced_Qty', 'sum')
                    ).reset_index().sort_values(by='Planned', ascending=False).head(10)
                    
                    fig_prod = px.bar(prod_agg, x='Product_Name', y=['Planned', 'Produced'], barmode='group',
                                      color_discrete_sequence=['#3B82F6', '#10B981'], template="plotly_dark")
                    fig_prod.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="Units")
                    st.plotly_chart(fig_prod, use_container_width=True)

            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Factory Order Delay Days Distribution</p>", unsafe_allow_html=True)
                fig_delay = px.histogram(prod_orders_df, x='Delay_Days', nbins=15,
                                         color_discrete_sequence=['#F59E0B'], template="plotly_dark")
                fig_delay.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Delay Days", yaxis_title="Number of Orders")
                st.plotly_chart(fig_delay, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE BOTTLENECK DRILL-DOWN
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2 = st.columns(2)
            
            # 1. فلتر البحث عن منتج
            prods = ["All"] + list(prod_orders_df['Product_Name'].dropna().unique()) if 'Product_Name' in prod_orders_df.columns else ["All"]
            sel_prod = c_f1.selectbox("Filter Product Name", prods, key="c6_prod_filter")
            
            # 2. فلتر حالة التأخير
            delay_opts = c_f2.selectbox("Order Completion Delay Status", ["All", "Delayed Orders (> 0 Days)", "On-Time Orders"], key="c6_delay_filter")

            # Filtering Logic
            f_prod = prod_orders_df.copy()
            if sel_prod != "All" and 'Product_Name' in f_prod.columns:
                f_prod = f_prod[f_prod['Product_Name'] == sel_prod]
            if delay_opts == "Delayed Orders (> 0 Days)":
                f_prod = f_prod[f_prod['Delay_Days'] > 0]
            elif delay_opts == "On-Time Orders":
                f_prod = f_prod[f_prod['Delay_Days'] <= 0]

            st.markdown("<br>", unsafe_allow_html=True)

            # Filtered KPIs
            f_plan = f_prod['Planned_Qty'].sum() if 'Planned_Qty' in f_prod.columns else 0
            f_prod_qty = f_prod['Produced_Qty'].sum() if 'Produced_Qty' in f_prod.columns else 0
            f_rate = (f_prod_qty / f_plan * 100) if f_plan > 0 else 0
            f_count = len(f_prod)

            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Selected Orders", f"{f_count:,.0f} Orders", "Active Batches"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Filtered Planned", f"{f_plan:,.0f} Units", "Planned Target"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Filtered Produced", f"{f_prod_qty:,.0f} Units", "Real Output"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Completion Rate", f"{f_rate:.1f}%", "Fulfillment"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if f_prod.empty:
                st.markdown("""
                    <div style="background: #111827; border: 1px dashed #374151; border-radius: 12px; padding: 40px; text-align: center; margin-top: 10px;">
                        <p style="font-size: 2rem; margin: 0;">🔍</p>
                        <h4 style="color: #F8FAFC; margin: 10px 0 5px 0;">No Production Orders Match Selected Filters</h4>
                        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">Try clearing your product filter or selecting all delay statuses.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: #1E293B; border-left: 4px solid #3B82F6; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                        <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Bottleneck Insight:</b> Active selection covers <b>{f_count} production orders</b> with a total output of <b>{f_prod_qty:,.0f} units</b> out of <b>{f_plan:,.0f} planned</b>.</p>
                    </div>
                """, unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>📊 Planned vs Produced Scatter Correlation</p>", unsafe_allow_html=True)
                    fig_sc = px.scatter(f_prod, x='Planned_Qty', y='Produced_Qty', hover_name='Product_Name',
                                        color='Delay_Days', color_continuous_scale='Reds', template="plotly_dark")
                    fig_sc.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Planned Quantity", yaxis_title="Produced Quantity")
                    st.plotly_chart(fig_sc, use_container_width=True)

                with chart_col2:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>⏳ Order Delay Days Matrix</p>", unsafe_allow_html=True)
                    fig_box = px.bar(f_prod.head(10), x='Production_Order_ID', y='Delay_Days', color='Delay_Days',
                                     color_continuous_scale='Oranges', template="plotly_dark")
                    fig_box.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Order ID", yaxis_title="Delay Days")
                    st.plotly_chart(fig_box, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Export & Detailed Table Header
                t_head1, t_head2 = st.columns([8, 2])
                with t_head1:
                    st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Factory Orders & Production Bottlenecks Directory</p>", unsafe_allow_html=True)
                with t_head2:
                    st.download_button(
                        label="📥 Export Report (CSV)",
                        data=f_prod.to_csv(index=False).encode('utf-8'),
                        file_name="Factory_Bottlenecks_Report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                display_table_cols = [c for c in ['Production_Order_ID', 'Product_ID', 'Product_Name', 'Start_Date', 'Due_Date', 'Completion_Date', 'Planned_Qty', 'Produced_Qty', 'Delay_Days'] if c in f_prod.columns]
                st.dataframe(f_prod[display_table_cols], use_container_width=True)
# ------------------------------------------
# CARD 6: QUALITY & COPQ LOSSES (100% REAL DATA & CORRECT COLUMNS)
# ------------------------------------------
elif selected_card == "Card 6":
    st.markdown("""
        <div class="card-header">
            <p class="card-title">C Quality, Returns & Cost of Poor Quality (COPQ)</p>
            <p class="card-subtitle">Pareto analysis of return reasons, defects, and financial impact of quality losses.</p>
        </div>
    """, unsafe_allow_html=True)
    
    quality_df = dfs.get('Quality', pd.DataFrame())
    
    if not quality_df.empty:
        tab1, tab2 = st.tabs(["📊 Executive Quality Story", "⚡ Interactive COPQ & Defect Drill-Down"])

        # ==========================================
        # TAB 1: EXECUTIVE QUALITY STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            total_records = len(quality_df)
            total_copq = quality_df['Estimated_Loss_EGP'].sum() if 'Estimated_Loss_EGP' in quality_df.columns else 0
            total_rejected = quality_df['Rejected_Qty'].sum() if 'Rejected_Qty' in quality_df.columns else 0
            avg_loss_per_issue = total_copq / max(total_records, 1)

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Total Quality Loss (COPQ)", f"{total_copq:,.0f} EGP", "Financial Cost of Defects"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Total Quality Records", f"{total_records:,.0f}", "Logged Inspections"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Total Rejected Units", f"{total_rejected:,.0f}", "Defective Volume"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Avg Impact per Issue", f"{avg_loss_per_issue:,.1f} EGP", "Severity Metric"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Quality Incidents & Pareto Analysis Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Loss by Defect Type (Pareto Analysis)</p>", unsafe_allow_html=True)
                if 'Defect_Type' in quality_df.columns and 'Estimated_Loss_EGP' in quality_df.columns:
                    defect_pareto = quality_df.groupby('Defect_Type')['Estimated_Loss_EGP'].sum().reset_index().sort_values(by='Estimated_Loss_EGP', ascending=False)
                    fig_q1 = px.bar(defect_pareto, x='Defect_Type', y='Estimated_Loss_EGP', text_auto='.2s',
                                    color='Estimated_Loss_EGP', color_continuous_scale='Reds', template="plotly_dark")
                    fig_q1.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), showlegend=False, xaxis_title="", yaxis_title="Loss (EGP)")
                    st.plotly_chart(fig_q1, use_container_width=True)

            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>COPQ Loss Distribution by Production Stage</p>", unsafe_allow_html=True)
                if 'Stage' in quality_df.columns and 'Estimated_Loss_EGP' in quality_df.columns:
                    stage_loss = quality_df.groupby('Stage')['Estimated_Loss_EGP'].sum().reset_index()
                    fig_q2 = px.pie(stage_loss, names='Stage', values='Estimated_Loss_EGP', hole=0.55,
                                     color_discrete_sequence=px.colors.qualitative.Pastel, template="plotly_dark")
                    fig_q2.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_q2, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE COPQ & DEFECT DRILL-DOWN
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2 = st.columns(2)
            
            # 1. فلتر نوع العيب
            defects_opts = ["All"] + list(quality_df['Defect_Type'].dropna().unique()) if 'Defect_Type' in quality_df.columns else ["All"]
            sel_defect = c_f1.selectbox("Filter Defect Type", defects_opts, key="q_defect_filter")
            
            # 2. فلتر مرحلة الإنتاج
            stages_opts = ["All"] + list(quality_df['Stage'].dropna().unique()) if 'Stage' in quality_df.columns else ["All"]
            sel_stage = c_f2.selectbox("Filter Production Stage", stages_opts, key="q_stage_filter")

            # منطق الفلترة
            f_qual = quality_df.copy()
            if sel_defect != "All" and 'Defect_Type' in f_qual.columns:
                f_qual = f_qual[f_qual['Defect_Type'] == sel_defect]
            if sel_stage != "All" and 'Stage' in f_qual.columns:
                f_qual = f_qual[f_qual['Stage'] == sel_stage]

            st.markdown("<br>", unsafe_allow_html=True)

            f_count = len(f_qual)
            f_loss = f_qual['Estimated_Loss_EGP'].sum() if 'Estimated_Loss_EGP' in f_qual.columns else 0
            f_rejected = f_qual['Rejected_Qty'].sum() if 'Rejected_Qty' in f_qual.columns else 0

            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered Inspections", f"{f_count:,.0f}", "Selected Records"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Filtered COPQ Loss", f"{f_loss:,.0f} EGP", "Financial Impact"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Filtered Rejected Units", f"{f_rejected:,.0f}", "Wasted Volume"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Active Filter Status", "Applied", "Custom View"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid #EF4444; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                    <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Quality Drill-Down:</b> Showing <b>{f_count} inspection records</b> with a financial loss impact of <b>{f_loss:,.0f} EGP</b>.</p>
                </div>
            """, unsafe_allow_html=True)

            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>📊 Rejected Qty vs Estimated Loss</p>", unsafe_allow_html=True)
                if 'Rejected_Qty' in f_qual.columns and 'Estimated_Loss_EGP' in f_qual.columns:
                    fig_c1 = px.scatter(f_qual, x='Rejected_Qty', y='Estimated_Loss_EGP', color='Stage' if 'Stage' in f_qual.columns else None,
                                        hover_name='Product_Name' if 'Product_Name' in f_qual.columns else None, template="plotly_dark")
                    fig_c1.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Rejected Quantity", yaxis_title="Loss (EGP)")
                    st.plotly_chart(fig_c1, use_container_width=True)

            with chart_col2:
                st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>⚡ Root Causes Breakdown</p>", unsafe_allow_html=True)
                if 'Root_Cause' in f_qual.columns:
                    rc_counts = f_qual['Root_Cause'].value_counts().reset_index()
                    rc_counts.columns = ['Root_Cause', 'Count']
                    fig_c2 = px.bar(rc_counts, x='Root_Cause', y='Count', color_discrete_sequence=['#F59E0B'], template="plotly_dark")
                    fig_c2.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="Count")
                    st.plotly_chart(fig_c2, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Export & Detailed Table
            t_head1, t_head2 = st.columns([8, 2])
            with t_head1:
                st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Quality Inspections & COPQ Directory</p>", unsafe_allow_html=True)
            with t_head2:
                st.download_button(
                    label="📥 Export Report (CSV)",
                    data=f_qual.to_csv(index=False).encode('utf-8'),
                    file_name="Quality_COPQ_Report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.dataframe(f_qual, use_container_width=True)
    else:
        st.warning("⚠️ جدول بيانات الجودة (Quality) غير متوفر في الداتا.")
# ------------------------------------------
# CARD 8: PRINTING PERFORMANCE & DOWNTIME (100% REAL COLUMNS)
# ------------------------------------------
elif selected_card == "Card 7":
    st.markdown("""
        <div class="card-header">
            <p class="card-title"> Printing Performance & Downtime Analysis</p>
            <p class="card-subtitle">Track printing job efficiency, machine output, ink/consumable costs, and rework expenses.</p>
        </div>
    """, unsafe_allow_html=True)
    
    print_df = dfs.get('Printing_Batches', pd.DataFrame())
    
    if not print_df.empty:
        tab1, tab2 = st.tabs(["📊 Executive Printing Story", "⚡ Interactive Printing & Cost Drill-Down"])

        # ==========================================
        # TAB 1: EXECUTIVE PRINTING STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            tot_planned = print_df['Planned_Qty'].sum() if 'Planned_Qty' in print_df.columns else 0
            tot_printed = print_df['Printed_Qty'].sum() if 'Printed_Qty' in print_df.columns else 0
            tot_ink_cost = print_df['Ink_or_Consumable_Cost_EGP'].sum() if 'Ink_or_Consumable_Cost_EGP' in print_df.columns else 0
            tot_rework_cost = print_df['Rework_Cost_EGP'].sum() if 'Rework_Cost_EGP' in print_df.columns else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Total Planned Qty", f"{tot_planned:,.0f} Units", "Target Print Volume"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Total Printed Qty", f"{tot_printed:,.0f} Units", "Actual Print Output"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Ink & Consumable Cost", f"{tot_ink_cost:,.2f} EGP", "Material Expenses"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Total Rework Cost", f"{tot_rework_cost:,.2f} EGP", "Correction Expenses"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Printing Types & Machine Output Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Output by Print Type (Digital, Water-Based, Heat Transfer)</p>", unsafe_allow_html=True)
                if 'Print_Type' in print_df.columns and 'Printed_Qty' in print_df.columns:
                    type_agg = print_df.groupby('Print_Type')['Printed_Qty'].sum().reset_index()
                    fig_p1 = px.bar(type_agg, x='Print_Type', y='Printed_Qty', text_auto='.2s',
                                    color_discrete_sequence=['#3B82F6'], template="plotly_dark")
                    fig_p1.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="Printed Volume")
                    st.plotly_chart(fig_p1, use_container_width=True)

            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Cost Distribution by Machine ID</p>", unsafe_allow_html=True)
                if 'Machine_ID' in print_df.columns and 'Ink_or_Consumable_Cost_EGP' in print_df.columns:
                    mach_agg = print_df.groupby('Machine_ID')['Ink_or_Consumable_Cost_EGP'].sum().reset_index()
                    fig_p2 = px.pie(mach_agg, names='Machine_ID', values='Ink_or_Consumable_Cost_EGP', hole=0.55,
                                     color_discrete_sequence=px.colors.qualitative.Pastel, template="plotly_dark")
                    fig_p2.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_p2, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE DRILL-DOWN
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2 = st.columns(2)
            
            # فلاتر تفاعلية حقيقية
            machines = ["All"] + list(print_df['Machine_ID'].dropna().unique()) if 'Machine_ID' in print_df.columns else ["All"]
            sel_mach = c_f1.selectbox("Filter Machine ID", machines, key="print_mach_filter")
            
            print_types = ["All"] + list(print_df['Print_Type'].dropna().unique()) if 'Print_Type' in print_df.columns else ["All"]
            sel_type = c_f2.selectbox("Filter Print Type", print_types, key="print_type_filter")

            f_print = print_df.copy()
            if sel_mach != "All" and 'Machine_ID' in f_print.columns:
                f_print = f_print[f_print['Machine_ID'] == sel_mach]
            if sel_type != "All" and 'Print_Type' in f_print.columns:
                f_print = f_print[f_print['Print_Type'] == sel_type]

            st.markdown("<br>", unsafe_allow_html=True)

            f_count = len(f_print)
            f_printed = f_print['Printed_Qty'].sum() if 'Printed_Qty' in f_print.columns else 0
            f_ink = f_print['Ink_or_Consumable_Cost_EGP'].sum() if 'Ink_or_Consumable_Cost_EGP' in f_print.columns else 0

            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered Batches", f"{f_count:,.0f}", "Selected Runs"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Filtered Printed Qty", f"{f_printed:,.0f} Units", "Output Volume"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Filtered Ink Cost", f"{f_ink:,.2f} EGP", "Material Cost"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Status", "Active", "Filter Applied"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid #3B82F6; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                    <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Printing Drill-Down:</b> Showing <b>{f_count} print batches</b> with total output of <b>{f_printed:,.0f} units</b>.</p>
                </div>
            """, unsafe_allow_html=True)

            # Export & Detailed Table
            t_head1, t_head2 = st.columns([8, 2])
            with t_head1:
                st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Printing Operations Directory</p>", unsafe_allow_html=True)
            with t_head2:
                st.download_button(
                    label="📥 Export Report (CSV)",
                    data=f_print.to_csv(index=False).encode('utf-8'),
                    file_name="Printing_Operations_Report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.dataframe(f_print, use_container_width=True)
    else:
        st.warning("⚠️ جدول بيانات الطباعة (Printing) غير متوفر في الداتا.")
# ------------------------------------------
# CARD 8: SUPPLIERS & SUPPLY CHAIN ANALYSIS 
# ------------------------------------------
elif selected_card in ["Supply Chain & BOM", "Card 8"]:
    st.markdown("""
        <div class="card-header">
            <p class="card-title"> Suppliers & Supply Chain Logistics</p>
            <p class="card-subtitle">Analyze supplier categories, geographical distribution across governorates, payment terms, and contracts.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # جلب جدول الموردين الفعلي
    sup_df = dfs.get('Suppliers', dfs.get('Supply_Chain', pd.DataFrame()))
    if sup_df.empty and len(dfs) > 0:
        sup_df = list(dfs.values()[0]) # كاحتياطي

    if not sup_df.empty:
        tab1, tab2 = st.tabs(["📊 Executive Suppliers Story", "⚡ Interactive Supplier Drill-Down"])

        # ==========================================
        # TAB 1: EXECUTIVE SUPPLIERS STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            total_suppliers = len(sup_df)
            contracted_count = len(sup_df[sup_df['Contracted'].astype(str).str.lower() == 'yes']) if 'Contracted' in sup_df.columns else 0
            avg_payment_terms = sup_df['Payment_Terms_Days'].mean() if 'Payment_Terms_Days' in sup_df.columns else 0
            total_governorates = sup_df['Governorate'].nunique() if 'Governorate' in sup_df.columns else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Total Suppliers", f"{total_suppliers:,.0f}", "Approved Vendors"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Contracted Suppliers", f"{contracted_count:,.0f}", "Official Contracts"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Avg Payment Terms", f"{avg_payment_terms:.1f} Days", "Credit Period"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Governorates Covered", f"{total_governorates:,.0f}", "Geographic Spread"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Suppliers Categories & Governorate Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Suppliers Distribution by Primary Category</p>", unsafe_allow_html=True)
                if 'Primary_Category' in sup_df.columns:
                    cat_agg = sup_df['Primary_Category'].value_counts().reset_index()
                    cat_agg.columns = ['Category', 'Count']
                    fig_s1 = px.bar(cat_agg, x='Category', y='Count', text_auto=True,
                                    color_discrete_sequence=['#10B981'], template="plotly_dark")
                    fig_s1.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="Supplier Count")
                    st.plotly_chart(fig_s1, use_container_width=True)

            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Suppliers Spread by Governorate</p>", unsafe_allow_html=True)
                if 'Governorate' in sup_df.columns:
                    gov_agg = sup_df['Governorate'].value_counts().reset_index()
                    gov_agg.columns = ['Governorate', 'Count']
                    fig_s2 = px.pie(gov_agg, names='Governorate', values='Count', hole=0.55,
                                     color_discrete_sequence=px.colors.qualitative.Pastel, template="plotly_dark")
                    fig_s2.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_s2, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE SUPPLIER DRILL-DOWN
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2 = st.columns(2)
            
            categories = ["All"] + list(sup_df['Primary_Category'].dropna().unique()) if 'Primary_Category' in sup_df.columns else ["All"]
            sel_cat = c_f1.selectbox("Filter Primary Category", categories, key="sup_cat_filter")
            
            governorates = ["All"] + list(sup_df['Governorate'].dropna().unique()) if 'Governorate' in sup_df.columns else ["All"]
            sel_gov = c_f2.selectbox("Filter Governorate", governorates, key="sup_gov_filter")

            f_sup = sup_df.copy()
            if sel_cat != "All" and 'Primary_Category' in f_sup.columns:
                f_sup = f_sup[f_sup['Primary_Category'] == sel_cat]
            if sel_gov != "All" and 'Governorate' in f_sup.columns:
                f_sup = f_sup[f_sup['Governorate'] == sel_gov]

            st.markdown("<br>", unsafe_allow_html=True)

            f_count = len(f_sup)
            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered Suppliers", f"{f_count:,.0f}", "Selected Vendors"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Contracted Share", f"{len(f_sup[f_sup['Contracted'].astype(str).str.lower() == 'yes']) if 'Contracted' in f_sup.columns else 0}", "Active Contracts"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Avg Payment Terms", f"{f_sup['Payment_Terms_Days'].mean() if 'Payment_Terms_Days' in f_sup.columns else 0:.1f} Days", "Credit Period"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Status", "Active", "Filter Applied"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid #10B981; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                    <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Suppliers Drill-Down:</b> Showing <b>{f_count} suppliers</b> matching selected criteria.</p>
                </div>
            """, unsafe_allow_html=True)

            # Export & Detailed Table
            t_head1, t_head2 = st.columns([8, 2])
            with t_head1:
                st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Suppliers Directory</p>", unsafe_allow_html=True)
            with t_head2:
                st.download_button(
                    label="📥 Export Report (CSV)",
                    data=f_sup.to_csv(index=False).encode('utf-8'),
                    file_name="Suppliers_Logistics_Report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.dataframe(f_sup, use_container_width=True)
    else:
        st.warning("⚠️ جدول بيانات الموردين (Suppliers) غير متوفر في الداتا.")
# ------------------------------------------
# CARD: MARKETING ROAS & CAC ANALYSIS (ULTRA ENTERPRISE)
# ------------------------------------------
elif selected_card in ["Marketing ROAS & CAC", "Card 9"]:
    st.markdown("""
        <div class="card-header">
            <p class="card-title">Card: Marketing ROAS & Customer Acquisition Cost (CAC)</p>
            <p class="card-subtitle">Evaluate campaign expenditure, revenue generated, ROAS, and platform performance.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # جلب جدول التسويق الحقيقي
    mkt_df = dfs.get('Marketing', dfs.get('Ads', dfs.get('Campaigns', pd.DataFrame())))
    if mkt_df.empty and len(dfs) > 0:
        for k in dfs.keys():
            if 'market' in k.lower() or 'ad' in k.lower() or 'campaign' in k.lower():
                mkt_df = dfs[k]
                break

    if not mkt_df.empty:
        tab1, tab2 = st.tabs(["📊 Executive Marketing Story", "⚡ Interactive Campaign Drill-Down"])

        # ==========================================
        # TAB 1: EXECUTIVE MARKETING STORY
        # ==========================================
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            total_campaigns = len(mkt_df)
            tot_spend = mkt_df['Spend_EGP'].sum() if 'Spend_EGP' in mkt_df.columns else 0
            tot_rev = mkt_df['Attributed_Revenue_EGP'].sum() if 'Attributed_Revenue_EGP' in mkt_df.columns else 0
            avg_roas = (tot_rev / tot_spend) if tot_spend > 0 else 0
            
            # حساب تكلفة الاستحواذ على العميل (CAC) تقريبياً بناءً على المصروفات والطلبات
            total_orders = mkt_df['Orders_Attributed'].sum() if 'Orders_Attributed' in mkt_df.columns else 1
            avg_cac = (tot_spend / total_orders) if total_orders > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(render_kpi("Total Ad Spend", f"{tot_spend:,.2f} EGP", "Campaign Budget"), unsafe_allow_html=True)
            col2.markdown(render_kpi("Total Attributed Revenue", f"{tot_rev:,.2f} EGP", "Ad-Driven Sales"), unsafe_allow_html=True)
            col3.markdown(render_kpi("Overall ROAS", f"{avg_roas:.2f}x", "Return on Ad Spend"), unsafe_allow_html=True)
            col4.markdown(render_kpi("Average CAC", f"{avg_cac:.2f} EGP", "Acquisition Cost"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="border-bottom: 1px solid #1F2937; padding-bottom: 6px; margin-bottom: 15px;">
                    <h4 style="color: #F8FAFC; font-size: 1rem; font-weight: 700; margin: 0;">📖 Spend vs Revenue by Platform Story</h4>
                </div>
            """, unsafe_allow_html=True)

            story_c1, story_c2 = st.columns(2)
            
            with story_c1:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Spend vs Revenue by Platform (Executive Summary)</p>", unsafe_allow_html=True)
                
                if 'Platform' in mkt_df.columns and 'Spend_EGP' in mkt_df.columns and 'Attributed_Revenue_EGP' in mkt_df.columns:
                    # 1. تجميع البيانات حسب المنصة لضمان الوضوح وعدم ازدحام الشاشة
                    platform_summary = mkt_df.groupby('Platform')[['Spend_EGP', 'Attributed_Revenue_EGP']].sum().reset_index()
                    
                    # 2. رسم أفقياً (Horizontal Bar Chart) لنظافة الرؤية
                    fig_m1 = px.bar(
                        platform_summary, 
                        y='Platform', 
                        x=['Spend_EGP', 'Attributed_Revenue_EGP'], 
                        barmode='group',
                        orientation='h',
                        labels={'value': 'Amount (EGP)', 'Platform': 'Platform', 'variable': 'Metric'},
                        color_discrete_map={'Spend_EGP': '#EF4444', 'Attributed_Revenue_EGP': '#10B981'},
                        template="plotly_dark"
                    )
                    
                    fig_m1.update_layout(
                        height=320, 
                        margin=dict(l=10, r=10, t=10, b=10),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        xaxis_title="Amount (EGP)",
                        yaxis_title=""
                    )
                    st.plotly_chart(fig_m1, use_container_width=True)

                elif 'Campaign_Name' in mkt_df.columns:
                    # خيار تاني: لو حابب نعرض الحملات نفسها، بناخد Top 7 فقط عشان الشاشة تفضل نظيفة
                    top_campaigns = mkt_df.sort_values(by='Spend_EGP', ascending=False).head(7)
                    fig_m1 = px.bar(
                        top_campaigns,
                        y='Campaign_Name',
                        x=['Spend_EGP', 'Attributed_Revenue_EGP'],
                        barmode='group',
                        orientation='h',
                        color_discrete_map={'Spend_EGP': '#EF4444', 'Attributed_Revenue_EGP': '#10B981'},
                        template="plotly_dark"
                    )
                    fig_m1.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig_m1, use_container_width=True)
            with story_c2:
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>Campaigns Distribution by Platform</p>", unsafe_allow_html=True)
                if 'Platform' in mkt_df.columns:
                    plat_counts = mkt_df['Platform'].value_counts().reset_index()
                    plat_counts.columns = ['Platform', 'Count']
                    fig_m2 = px.pie(plat_counts, names='Platform', values='Count', hole=0.55, color_discrete_sequence=px.colors.qualitative.Pastel, template="plotly_dark")
                    fig_m2.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_m2, use_container_width=True)

        # ==========================================
        # TAB 2: INTERACTIVE CAMPAIGN DRILL-DOWN
        # ==========================================
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_f1, c_f2 = st.columns(2)
            platforms = ["All"] + list(mkt_df['Platform'].dropna().unique()) if 'Platform' in mkt_df.columns else ["All"]
            sel_plat = c_f1.selectbox("Filter by Platform", platforms, key="mkt_platform_filter")
            
            sort_cols = list(mkt_df.columns)
            sel_sort = c_f2.selectbox("Sort Records By", sort_cols, key="mkt_sort_metric")

            f_mkt = mkt_df.copy()
            if sel_plat != "All" and 'Platform' in f_mkt.columns:
                f_mkt = f_mkt[f_mkt['Platform'] == sel_plat]
            
            try:
                f_mkt = f_mkt.sort_values(by=sel_sort, ascending=False)
            except:
                pass

            st.markdown("<br>", unsafe_allow_html=True)

            f_count = len(f_mkt)
            f_spend = f_mkt['Spend_EGP'].sum() if 'Spend_EGP' in f_mkt.columns else 0
            f_rev = f_mkt['Attributed_Revenue_EGP'].sum() if 'Attributed_Revenue_EGP' in f_mkt.columns else 0
            
            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.markdown(render_kpi("Filtered Campaigns", f"{f_count:,.0f}", "Selected Rows"), unsafe_allow_html=True)
            fc2.markdown(render_kpi("Filtered Spend", f"{f_spend:,.2f} EGP", "Budget"), unsafe_allow_html=True)
            fc3.markdown(render_kpi("Filtered Revenue", f"{f_rev:,.2f} EGP", "Sales"), unsafe_allow_html=True)
            fc4.markdown(render_kpi("Status", "Active", "Filter Applied"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid #EF4444; padding: 12px 18px; border-radius: 6px; margin-bottom: 20px;">
                    <p style="color: #F8FAFC; font-size: 0.85rem; margin: 0;">💡 <b>Marketing Drill-Down:</b> Displaying <b>{f_count} campaigns</b> matching selected criteria.</p>
                </div>
            """, unsafe_allow_html=True)

            # Export & Detailed Table
            t_head1, t_head2 = st.columns([8, 2])
            with t_head1:
                st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 1rem; margin-top: 10px;'>📋 Marketing Campaigns Directory</p>", unsafe_allow_html=True)
            with t_head2:
                st.download_button(
                    label="📥 Export Report (CSV)",
                    data=f_mkt.to_csv(index=False).encode('utf-8'),
                    file_name="Marketing_Campaigns_Report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.dataframe(f_mkt, use_container_width=True)
    else:
        st.warning("⚠️ جدول بيانات التسويق (Marketing) غير متوفر في الداتا.")        
# ------------------------------------------
# CARD 10: EXECUTIVE STORY & ADVANCED ENTERPRISE FORECASTING
# ------------------------------------------
elif selected_card in ["Executive Story & Forecast", "Card 10"]:
    st.markdown("""
        <div class="card-header">
            <p class="card-title"> Executive Strategic Story & Enterprise AI Forecasting Suite</p>
            <p class="card-subtitle">Granular SARIMAX time-series forecasting across branches/products and interactive stress-testing simulations.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    sales_df = dfs.get('Sales_Transactions', pd.DataFrame())

    # تنظيم الكارد في 4 تابات احترافية
    tab_sarimax, tab_multidim, tab_whatif = st.tabs([
        "📈 Global SARIMAX Model", 
        "🌐 Granular Branch & Product SARIMAX", 
        "🔀 AI What-If Simulation Engine"
    ])

    # ==========================================
    # TAB 1: GLOBAL SARIMAX MODEL
    # ==========================================
    with tab_sarimax:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>📊 Global Net Sales SARIMAX Forecasting Model</p>", unsafe_allow_html=True)
        
        try:
            if not sales_df.empty and 'Order_Date' in sales_df.columns and 'Net_Sales_EGP' in sales_df.columns:
                df_clean = sales_df[['Order_Date', 'Net_Sales_EGP']].copy()
                df_clean['Order_Date'] = pd.to_datetime(df_clean['Order_Date'], errors='coerce')
                df_clean = df_clean.dropna(subset=['Order_Date', 'Net_Sales_EGP']).sort_values(by='Order_Date')
                df_clean.set_index('Order_Date', inplace=True)
                
                monthly_ts = df_clean['Net_Sales_EGP'].resample('ME').sum()
                
                if len(monthly_ts) >= 4:
                    from statsmodels.tsa.statespace.sarimax import SARIMAX
                    model = SARIMAX(monthly_ts, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), enforce_stationarity=False, enforce_invertibility=False)
                    fitted_model = model.fit(disp=False)
                    
                    forecast_obj = fitted_model.get_forecast(steps=6)
                    forecast_mean = forecast_obj.predicted_mean
                    conf_int = forecast_obj.conf_int()
                    
                    import plotly.graph_objects as go
                    fig_sarimax = go.Figure()
                    ci_dates = pd.Series(conf_int.index)
                    
                    fig_sarimax.add_trace(go.Scatter(
                        x=pd.concat([ci_dates, ci_dates[::-1]]),
                        y=pd.concat([conf_int.iloc[:, 1], conf_int.iloc[:, 0][::-1]]),
                        fill='toself', fillcolor='rgba(16, 185, 129, 0.15)',
                        line=dict(color='rgba(255,255,255,0)'), name='95% Confidence Interval'
                    ))
                    fig_sarimax.add_trace(go.Scatter(
                        x=forecast_mean.index, y=forecast_mean, mode='lines+markers',
                        name='SARIMAX Forecast', line=dict(color='#10B981', width=3)
                    ))
                    fig_sarimax.add_trace(go.Scatter(
                        x=monthly_ts.index, y=monthly_ts, mode='lines+markers',
                        name='Historical Actuals', line=dict(color='#3B82F6', width=2)
                    ))
                    fig_sarimax.update_layout(
                        template='plotly_dark', height=400, margin=dict(l=10, r=10, t=10, b=10),
                        xaxis_title="Timeline", yaxis_title="Net Sales (EGP)",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_sarimax, use_container_width=True)
                    st.success(f"🚀 تم تشغيل موديل SARIMAX العام بنجاح على **{len(monthly_ts)} شهراً تاريخياً**!")
                else:
                    st.warning("⚠️ البيانات التاريخية غير كافية (أقل من 4 أشهر متصلة).")
        except Exception as ex:
            st.error(f"⚠️ خطأ في تشغيل موديل SARIMAX: {ex}")

    # ==========================================
    # TAB 2: GRANULAR BRANCH & PRODUCT SARIMAX
    # ==========================================
    with tab_multidim:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>🌐 Granular Branch & Product Family SARIMAX Forecasting</p>", unsafe_allow_html=True)
        
        if not sales_df.empty and 'Location_Name' in sales_df.columns:
            col_d1, col_d2, col_d3 = st.columns(3)
            
            locs = ["All Locations"] + list(sales_df['Location_Name'].dropna().unique())
            chosen_loc = col_d1.selectbox("Select Branch / Location", locs, key="real_loc_filter_v2")
            
            fams = ["All Families"] + list(sales_df['Product_Family'].dropna().unique()) if 'Product_Family' in sales_df.columns else ["All Families"]
            chosen_fam = col_d2.selectbox("Select Product Family", fams, key="real_fam_filter_v2")
            
            horizon_steps = col_d3.slider("Forecast Horizon (Months)", min_value=3, max_value=12, value=6, step=3, key="real_horizon_v2")
            
            sub_df = sales_df.copy()
            sub_df['Order_Date'] = pd.to_datetime(sub_df['Order_Date'], errors='coerce')
            sub_df = sub_df.dropna(subset=['Order_Date', 'Net_Sales_EGP'])
            
            if chosen_loc != "All Locations":
                sub_df = sub_df[sub_df['Location_Name'] == chosen_loc]
            if chosen_fam != "All Families" and 'Product_Family' in sub_df.columns:
                sub_df = sub_df[sub_df['Product_Family'] == chosen_fam]
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            if not sub_df.empty:
                sub_monthly = sub_df.set_index('Order_Date')['Net_Sales_EGP'].resample('ME').sum()
                
                if len(sub_monthly) >= 3:
                    try:
                        from statsmodels.tsa.statespace.sarimax import SARIMAX
                        sub_model = SARIMAX(sub_monthly, order=(1, 1, 1), enforce_stationarity=False, enforce_invertibility=False)
                        sub_fit = sub_model.fit(disp=False)
                        
                        sub_fc = sub_fit.get_forecast(steps=horizon_steps)
                        sub_mean = sub_fc.predicted_mean
                        sub_ci = sub_fc.conf_int()
                        
                        import plotly.graph_objects as go
                        fig_sub = go.Figure()
                        ci_sub_dates = pd.Series(sub_ci.index)
                        
                        fig_sub.add_trace(go.Scatter(
                            x=pd.concat([ci_sub_dates, ci_sub_dates[::-1]]),
                            y=pd.concat([sub_ci.iloc[:, 1], sub_ci.iloc[:, 0][::-1]]),
                            fill='toself', fillcolor='rgba(59, 130, 246, 0.15)',
                            line=dict(color='rgba(255,255,255,0)'), name='Confidence Interval'
                        ))
                        fig_sub.add_trace(go.Scatter(
                            x=sub_mean.index, y=sub_mean, mode='lines+markers',
                            name='Branch/Product SARIMAX Forecast', line=dict(color='#F59E0B', width=3)
                        ))
                        fig_sub.add_trace(go.Scatter(
                            x=sub_monthly.index, y=sub_monthly, mode='lines+markers',
                            name='Filtered Historical Actuals', line=dict(color='#3B82F6', width=2)
                        ))
                        fig_sub.update_layout(
                            template='plotly_dark', height=400, margin=dict(l=10, r=10, t=10, b=10),
                            xaxis_title="Timeline", yaxis_title="Net Sales (EGP)",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        st.plotly_chart(fig_sub, use_container_width=True)
                        st.success(f"📍 تم تشغيل محرك SARIMAX المخصص بنجاح للفرع: **{chosen_loc}** | العائلة: **{chosen_fam}** لمسافة {horizon_steps} شهور قادمة!")
                    except Exception as err:
                        st.warning(f"⚠️ تعذر تشغيل الموديل على هذه التصفية المحددة نظراً لقلة نقاط البيانات: {err}")
                else:
                    st.warning("⚠️ البيانات غير كافية تحت الفلتر المختار لتشغيل التنبؤ الزمني (يلزم 3 شهور على الأقل).")
            else:
                st.warning("⚠️ لا توجد سجلات مطابقة لخيارات التصفية الحالية.")
        else:
            st.warning("⚠️ عمود `Location_Name` غير متوفر في الجدول.")

    # ==========================================
    # TAB 3: AI WHAT-IF SIMULATION ENGINE
    # ==========================================
    with tab_whatif:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F8FAFC; font-weight: 600; font-size: 0.95rem;'>🔀 AI What-If Scenario Simulation Engine (Deterministic Econometric Modeling)</p>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: #1E293B; border: 1px solid #334155; padding: 20px; border-radius: 10px; margin-bottom: 22px; text-align: center;">
                <p style="color: #94A3B8; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; font-weight: 600;">Simulation Core Equation</p>
                <h3 style="color: #38BDF8; font-family: monospace; font-size: 1.25rem; font-weight: 700; margin: 0;">
                    Simulated Sales = Actual Sales × (1 + Price Change %) × (1 + Demand Growth %)
                </h3>
            </div>
        """, unsafe_allow_html=True)
        if not sales_df.empty and 'Net_Sales_EGP' in sales_df.columns and 'Estimated_COGS_EGP' in sales_df.columns:
            w_col1, w_col2, w_col3 = st.columns(3)
            price_change_pct = w_col1.slider("Price / Discount Adjustment (%)", min_value=-30, max_value=30, value=0, step=5, key="sc_price_v2")
            demand_growth_pct = w_col2.slider("Demand Growth Shift (%)", min_value=-20, max_value=50, value=0, step=5, key="sc_demand_v2")
            cogs_shift_pct = w_col3.slider("COGS / Raw Material Inflation (%)", min_value=-10, max_value=40, value=0, step=5, key="sc_cogs_v2")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # محاكاة ذكية مبنية على نماذج مرونة الطلب والاقتصاد القياسي (Econometric Elasticity Simulation)
            sim_df = sales_df[['Order_Date', 'Net_Sales_EGP', 'Estimated_COGS_EGP', 'Gross_Profit_EGP']].copy()
            sim_df['Order_Date'] = pd.to_datetime(sim_df['Order_Date'], errors='coerce')
            sim_df = sim_df.dropna(subset=['Order_Date', 'Net_Sales_EGP', 'Estimated_COGS_EGP'])
            
            # تطبيق معادلة المحاكاة الرياضية المعتمدة في التخطيط المالي:
            # Net Sales = Base Sales * (1 + Price Change) * (1 + Demand Growth)
            sim_df['Simulated_Net_Sales'] = sim_df['Net_Sales_EGP'] * (1 + (price_change_pct / 100)) * (1 + (demand_growth_pct / 100))
            sim_df['Simulated_COGS'] = sim_df['Estimated_COGS_EGP'] * (1 + (cogs_shift_pct / 100))
            sim_df['Simulated_Gross_Profit'] = sim_df['Simulated_Net_Sales'] - sim_df['Simulated_COGS']
            sim_df['Simulated_Margin'] = (sim_df['Simulated_Gross_Profit'] / sim_df['Simulated_Net_Sales']) * 100
            
            monthly_actual = sales_df.set_index(pd.to_datetime(sales_df['Order_Date'], errors='coerce'))['Net_Sales_EGP'].resample('ME').sum()
            monthly_sim = sim_df.set_index('Order_Date')['Simulated_Net_Sales'].resample('ME').sum()
            
            comp_df = pd.DataFrame({'Actual Net Sales': monthly_actual, 'Simulated What-If Sales': monthly_sim}).dropna()
            
            tot_act = monthly_actual.sum()
            tot_sim = monthly_sim.sum()
            diff_pct = ((tot_sim - tot_act) / tot_act) * 100 if tot_act > 0 else 0
            avg_margin = sim_df['Simulated_Margin'].mean()
            
            k1, k2, k3 = st.columns(3)
            k1.markdown(render_kpi("Baseline Net Sales", f"{tot_act:,.0f} EGP", "Historical Actuals"), unsafe_allow_html=True)
            k2.markdown(render_kpi("Simulated Scenario Sales", f"{tot_sim:,.0f} EGP", f"Delta: {diff_pct:+.1f}%"), unsafe_allow_html=True)
            k3.markdown(render_kpi("Projected Profit Margin", f"{avg_margin:.1f}%", "Stress-Tested"), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            import plotly.express as px
            fig_sim = px.line(comp_df, markers=True, template='plotly_dark', color_discrete_map={'Actual Net Sales': '#3B82F6', 'Simulated What-If Sales': '#10B981'})
            fig_sim.update_traces(line=dict(width=3))
            fig_sim.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Timeline", yaxis_title="Net Sales (EGP)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_sim, use_container_width=True)
            
            if diff_pct >= 0:
                st.success(f"📈 سيناريو المحاكاة يظهر نمواً متوقعاً في الإيرادات بنسبة **{diff_pct:+.1f}%** بناءً على المتغيرات المدخلة.")
            else:
                st.warning(f"⚠️ تحذير استراتيجي: السيناريو المدخل يتسبب في انكماش الإيرادات بنسبة **{diff_pct:+.1f}%**.")
        else:
            st.warning("⚠️ بيانات المعاملات غير مكتملة لتشغيل محرك المحاكاة.")

   
