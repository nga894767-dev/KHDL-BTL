import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# TIÊU ĐỀ WEB
# =========================

st.title("🔍 Hệ Thống Phát Hiện Gian Lận Kế Toán")

st.write(
    "📂 Tải file CSV hoặc Excel để phân tích giao dịch bất thường"
)

# =========================
# SIDEBAR
# =========================

st.sidebar.header("⚙️ Bộ lọc dữ liệu")

risk_filter = st.sidebar.selectbox(
    "Chọn mức độ rủi ro",
    ["Tất cả", "🔴 Cao", "🟠 Trung bình", "🟢 Thấp"]
)

amount_filter = st.sidebar.slider(
    "Lọc giao dịch theo số tiền",
    0,
    10000,
    1000
)

# =========================
# UPLOAD FILE
# =========================

uploaded_file = st.file_uploader(
    "Chọn file dữ liệu",
    type=["csv", "xlsx"]
)

# =========================
# ĐỌC FILE
# =========================

if uploaded_file is not None:

    try:

        # CSV
        if uploaded_file.name.endswith(".csv"):

            data = pd.read_csv(uploaded_file)

        # Excel
        else:

            data = pd.read_excel(uploaded_file)

        # =========================
        # HIỂN THỊ DỮ LIỆU
        # =========================

        st.subheader("📄 Dữ liệu giao dịch")

        st.dataframe(data.head(20))

        # =========================
        # KIỂM TRA CỘT
        # =========================

        required_columns = [
            'Time',
            'Amount',
            'Class'
        ]

        missing_columns = []

        for col in required_columns:

            if col not in data.columns:

                missing_columns.append(col)

        # =========================
        # THIẾU CỘT
        # =========================

        if len(missing_columns) > 0:

            st.error(
                f"❌ Thiếu cột dữ liệu: {missing_columns}"
            )

        else:

            # =========================
            # THỐNG KÊ
            # =========================

            fraud_count = data['Class'].sum()

            total_transactions = len(data)

            normal_count = (
                total_transactions
                - fraud_count
            )

            st.subheader("📊 Thống kê giao dịch")

            col1, col2, col3 = st.columns(3)

            col1.success(
                f"✅ Bình thường\n\n{normal_count}"
            )

            col2.error(
                f"🚨 Gian lận\n\n{fraud_count}"
            )

            col3.info(
                f"📌 Tổng giao dịch\n\n{total_transactions}"
            )

            # =========================
            # LỌC GIAO DỊCH GIAN LẬN
            # =========================

            suspicious = data[
                data['Class'] == 1
            ].copy()

            # =========================
            # PHÂN TÍCH RỦI RO
            # =========================

            reasons = []

            risk_levels = []

            for index, row in suspicious.iterrows():

                reason = []

                score = 0

                # Số tiền lớn
                if row['Amount'] > amount_filter:

                    reason.append(
                        "💰 Số tiền lớn"
                    )

                    score += 1

                # Giao dịch đêm
                if row['Time'] > 50000:

                    reason.append(
                        "🌙 Giao dịch đêm"
                    )

                    score += 1

                # Mức độ rủi ro
                if score >= 2:

                    risk = "🔴 Cao"

                elif score == 1:

                    risk = "🟠 Trung bình"

                else:

                    risk = "🟢 Thấp"

                reasons.append(
                    ", ".join(reason)
                )

                risk_levels.append(risk)

            # =========================
            # THÊM CỘT
            # =========================

            suspicious[
                'Mức độ rủi ro'
            ] = risk_levels

            suspicious[
                'Lý do nghi ngờ'
            ] = reasons

            # =========================
            # FILTER RISK
            # =========================

            if risk_filter != "Tất cả":

                suspicious = suspicious[
                    suspicious[
                        'Mức độ rủi ro'
                    ] == risk_filter
                ]

            # =========================
            # HIỂN THỊ GIAO DỊCH
            # =========================

            st.subheader(
                "⚠️ Danh sách giao dịch đáng ngờ"
            )

            st.dataframe(

                suspicious[
                    [
                        'Time',
                        'Amount',
                        'Mức độ rủi ro',
                        'Lý do nghi ngờ'
                    ]
                ]

            )

            # =========================
            # BIỂU ĐỒ CỘT
            # =========================

            st.subheader(
                "📈 Biểu đồ giao dịch"
            )

            fig, ax = plt.subplots()

            ax.bar(
                ['Bình thường', 'Gian lận'],
                [normal_count, fraud_count]
            )

            ax.set_ylabel(
                "Số lượng"
            )

            ax.set_title(
                "Phân bố giao dịch"
            )

            st.pyplot(fig)

            # =========================
            # BIỂU ĐỒ SCATTER
            # =========================

            st.subheader(
                "📉 Phân bố giao dịch theo Time và Amount"
            )

            fig2, ax2 = plt.subplots()

            normal = data[
                data['Class'] == 0
            ]

            fraud = data[
                data['Class'] == 1
            ]

            ax2.scatter(
                normal['Time'],
                normal['Amount'],
                label='Normal',
                alpha=0.5
            )

            ax2.scatter(
                fraud['Time'],
                fraud['Amount'],
                label='Fraud',
                alpha=0.8
            )

            ax2.set_xlabel("Time")

            ax2.set_ylabel("Amount")

            ax2.legend()

            st.pyplot(fig2)

            # =========================
            # GIAO DỊCH GIÁ TRỊ LỚN
            # =========================

            st.subheader(
                "💸 Giao dịch giá trị lớn"
            )

            high_amount = data[
                data['Amount'] > 5000
            ]

            st.dataframe(

                high_amount[
                    [
                        'Time',
                        'Amount',
                        'Class'
                    ]
                ]

            )

            # =========================
            # DOWNLOAD CSV
            # =========================

            csv = suspicious.to_csv(
                index=False
            ).encode('utf-8')

            st.download_button(
                "⬇️ Tải kết quả CSV",
                csv,
                "fraud_result.csv",
                "text/csv"
            )

    except Exception as e:

        st.error(
            f"❌ Lỗi xử lý file: {e}"
        )