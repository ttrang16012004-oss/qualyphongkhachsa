import streamlit as st
from datetime import datetime, date
import pandas as pd
import os

# =========================================================
# CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="Hotel Room Manager",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #f6f8fb;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .hotel-title {
        font-size: 32px;
        font-weight: 700;
        color: #16324F;
        margin-bottom: 0;
    }

    .hotel-subtitle {
        color: #6B7280;
        margin-top: 0;
    }

    .room-card {
        background: white;
        border-radius: 14px;
        padding: 16px;
        border: 1px solid #e5e7eb;
        margin-bottom: 12px;
    }

    .room-number {
        font-size: 22px;
        font-weight: 700;
        color: #16324F;
    }

    .small-text {
        color: #6B7280;
        font-size: 14px;
    }

    .status-available {
        color: #15803D;
        font-weight: 700;
    }

    .status-occupied {
        color: #DC2626;
        font-weight: 700;
    }

    .status-cleaning {
        color: #D97706;
        font-weight: 700;
    }

    .status-maintenance {
        color: #7C3AED;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DỮ LIỆU PHÒNG
# =========================================================

ROOM_TYPES = {
    "Standard": 800000,
    "Deluxe": 1200000,
    "Premier": 1600000,
    "Suite": 2200000,
}

if "rooms" not in st.session_state:

    st.session_state.rooms = pd.DataFrame([
        ["101", "Standard", 1, 800000, "Trống", "", "", "", ""],
        ["102", "Standard", 1, 800000, "Đang ở",
         "Nguyễn Văn An", "0901234567", "2026-09-27", "2026-09-29"],
        ["103", "Standard", 1, 800000, "Đang dọn", "", "", "", ""],
        ["104", "Standard", 1, 800000, "Trống", "", "", "", ""],

        ["201", "Deluxe", 2, 1200000, "Trống", "", "", "", ""],
        ["202", "Deluxe", 2, 1200000, "Đang ở",
         "Trần Thị Mai", "0912345678", "2026-09-26", "2026-09-30"],
        ["203", "Deluxe", 2, 1200000, "Bảo trì", "", "", "", ""],
        ["204", "Deluxe", 2, 1200000, "Trống", "", "", "", ""],

        ["301", "Premier", 3, 1600000, "Trống", "", "", "", ""],
        ["302", "Premier", 3, 1600000, "Đang ở",
         "Lê Minh Hoàng", "0987654321", "2026-09-28", "2026-10-01"],
        ["303", "Premier", 3, 1600000, "Trống", "", "", "", ""],
        ["304", "Premier", 3, 1600000, "Đang dọn", "", "", "", ""],

        ["401", "Suite", 4, 2200000, "Trống", "", "", "", ""],
        ["402", "Suite", 4, 2200000, "Trống", "", "", "", ""],
        ["403", "Suite", 4, 2200000, "Đang ở",
         "Phạm Gia Huy", "0933333333", "2026-09-27", "2026-10-02"],
        ["404", "Suite", 4, 2200000, "Trống", "", "", "", ""],
    ], columns=[
        "Phòng",
        "Loại phòng",
        "Tầng",
        "Giá/đêm",
        "Trạng thái",
        "Khách",
        "SĐT",
        "Ngày nhận",
        "Ngày trả"
    ])

# =========================================================
# DỮ LIỆU ĐẶT PHÒNG
# =========================================================

if "bookings" not in st.session_state:

    st.session_state.bookings = pd.DataFrame(
        columns=[
            "Mã đặt phòng",
            "Khách hàng",
            "SĐT",
            "Phòng",
            "Loại phòng",
            "Ngày nhận",
            "Ngày trả",
            "Số khách",
            "Trạng thái",
            "Ngày tạo"
        ]
    )

# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def money(value):
    return f"{int(value):,}".replace(",", ".") + " đ"


def status_class(status):

    mapping = {
        "Trống": "status-available",
        "Đang ở": "status-occupied",
        "Đang dọn": "status-cleaning",
        "Bảo trì": "status-maintenance"
    }

    return mapping.get(status, "")


def update_room(room_number, **kwargs):

    for key, value in kwargs.items():

        st.session_state.rooms.loc[
            st.session_state.rooms["Phòng"] == room_number,
            key
        ] = value


def generate_booking_id():

    return "BK" + datetime.now().strftime("%Y%m%d%H%M%S")


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🏨 HOTEL MANAGER")

st.sidebar.caption(
    "Hệ thống quản lý phòng khách sạn"
)

menu = st.sidebar.radio(
    "MENU",
    [
        "📊 Tổng quan",
        "🛏️ Quản lý phòng",
        "📋 Đặt phòng",
        "👤 Nhận phòng",
        "🚪 Trả phòng"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "💡 Hệ thống quản lý phòng khách sạn.\n\n"
    "Dữ liệu được lưu trong phiên Streamlit."
)

# =========================================================
# HEADER + HÌNH ẢNH
# =========================================================

col_logo, col_title = st.columns([1, 4])

with col_logo:

    # ẢNH IMG_4249.JPG
    if os.path.exists("IMG_4249.jpg"):

        st.image(
            "IMG_4249.jpg",
            width=180
        )

    else:

        st.warning(
            "Không tìm thấy IMG_4249.jpg"
        )

with col_title:

    st.markdown(
        '<p class="hotel-title">'
        '🏨 HOTEL ROOM MANAGER'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="hotel-subtitle">'
        'Hệ thống quản lý phòng khách sạn'
        '</p>',
        unsafe_allow_html=True
    )

st.divider()

# =========================================================
# TRANG TỔNG QUAN
# =========================================================

if menu == "📊 Tổng quan":

    rooms = st.session_state.rooms

    total_rooms = len(rooms)

    available = len(
        rooms[rooms["Trạng thái"] == "Trống"]
    )

    occupied = len(
        rooms[rooms["Trạng thái"] == "Đang ở"]
    )

    cleaning = len(
        rooms[rooms["Trạng thái"] == "Đang dọn"]
    )

    maintenance = len(
        rooms[rooms["Trạng thái"] == "Bảo trì"]
    )

    denominator = total_rooms - maintenance

    occupancy_rate = (
        occupied / denominator * 100
        if denominator > 0
        else 0
    )

    st.subheader("📊 Tổng quan hoạt động")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "🏨 Tổng phòng",
        total_rooms
    )

    c2.metric(
        "🟢 Phòng trống",
        available
    )

    c3.metric(
        "🔴 Đang ở",
        occupied
    )

    c4.metric(
        "🟠 Đang dọn",
        cleaning
    )

    c5.metric(
        "🟣 Bảo trì",
        maintenance
    )

    st.write("")

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # BIỂU ĐỒ TRẠNG THÁI
    # -----------------------------------------------------

    with col1:

        st.subheader("📈 Tình trạng phòng")

        chart_data = pd.DataFrame({
            "Trạng thái": [
                "Trống",
                "Đang ở",
                "Đang dọn",
                "Bảo trì"
            ],

            "Số phòng": [
                available,
                occupied,
                cleaning,
                maintenance
            ]
        })

        st.bar_chart(
            chart_data.set_index(
                "Trạng thái"
            )
        )

        st.metric(
            "Công suất phòng hiện tại",
            f"{occupancy_rate:.1f}%"
        )

    # -----------------------------------------------------
    # BIỂU ĐỒ LOẠI PHÒNG
    # -----------------------------------------------------

    with col2:

        st.subheader("🏷️ Phòng theo loại")

        type_count = (
            rooms
            .groupby("Loại phòng")
            .size()
            .reset_index(name="Số phòng")
            .set_index("Loại phòng")
        )

        st.bar_chart(type_count)

    st.divider()

    # -----------------------------------------------------
    # DANH SÁCH PHÒNG
    # -----------------------------------------------------

    st.subheader("🛎️ Tình trạng phòng")

    for _, room in rooms.iterrows():

        status = room["Trạng thái"]

        st.markdown(
            f"""
            <div class="room-card">

                <span class="room-number">
                    Phòng {room["Phòng"]}
                </span>

                &nbsp;&nbsp;

                <span class="{status_class(status)}">
                    {status}
                </span>

                <br>

                <span class="small-text">
                    {room["Loại phòng"]}
                    · Tầng {room["Tầng"]}
                    · {money(room["Giá/đêm"])}
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.subheader("🛏️ Quản lý phòng")

    rooms = st.session_state.rooms

    col1, col2, col3 = st.columns(3)

    with col1:

        filter_status = st.selectbox(
            "Lọc trạng thái",
            [
                "Tất cả",
                "Trống",
                "Đang ở",
                "Đang dọn",
                "Bảo trì"
            ]
        )

    with col2:

        filter_type = st.selectbox(
            "Lọc loại phòng",
            [
                "Tất cả"
            ] + list(ROOM_TYPES.keys())
        )

    with col3:

        search = st.text_input(
            "🔎 Tìm phòng",
            placeholder="Nhập số phòng..."
        )

    filtered = rooms.copy()

    if filter_status != "Tất cả":

        filtered = filtered[
            filtered["Trạng thái"] == filter_status
        ]

    if filter_type != "Tất cả":

        filtered = filtered[
            filtered["Loại phòng"] == filter_type
        ]

    if search:

        filtered = filtered[
            filtered["Phòng"]
            .astype(str)
            .str.contains(
                search,
                case=False
            )
        ]

    st.write(
        f"Hiển thị **{len(filtered)}** phòng"
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("⚙️ Cập nhật trạng thái phòng")

    room_number = st.selectbox(
        "Chọn phòng",
        rooms["Phòng"].tolist()
    )

    current_room = rooms[
        rooms["Phòng"] == room_number
    ].iloc[0]

    new_status = st.selectbox(
        "Trạng thái mới",
        [
            "Trống",
            "Đang ở",
            "Đang dọn",
            "Bảo trì"
        ],
        index=[
            "Trống",
            "Đang ở",
            "Đang dọn",
            "Bảo trì"
        ].index(
            current_room["Trạng thái"]
        )
    )

    if st.button(
        "💾 Lưu thay đổi",
        type="primary"
    ):

        update_room(
            room_number,
            **{
                "Trạng thái": new_status
            }
        )

        st.success(
            f"Đã cập nhật phòng {room_number}."
        )

        st.rerun()

# =========================================================
# ĐẶT PHÒNG
# =========================================================

elif menu == "📋 Đặt phòng":

    st.subheader("📋 Đặt phòng")

    rooms = st.session_state.rooms

    available_rooms = rooms[
        rooms["Trạng thái"] == "Trống"
    ]

    if len(available_rooms) == 0:

        st.warning(
            "Hiện tại không có phòng trống."
        )

    else:

        with st.form("booking_form"):

            st.markdown(
                "### 👤 Thông tin khách hàng"
            )

            col1, col2 = st.columns(2)

            with col1:

                customer_name = st.text_input(
                    "Họ và tên *"
                )

            with col2:

                phone = st.text_input(
                    "Số điện thoại *"
                )

            col3, col4 = st.columns(2)

            with col3:

                check_in = st.date_input(
                    "Ngày nhận phòng",
                    value=date.today()
                )

            with col4:

                check_out = st.date_input(
                    "Ngày trả phòng",
                    value=date.today()
                )

            col5, col6 = st.columns(2)

            with col5:

                number_of_guests = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=10,
                    value=2
                )

            with col6:

                room_number = st.selectbox(
                    "Chọn phòng",
                    available_rooms["Phòng"].tolist()
                )

            submit_booking = st.form_submit_button(
                "📌 Tạo đặt phòng",
                type="primary"
            )

            if submit_booking:

                if not customer_name.strip():

                    st.error(
                        "Vui lòng nhập tên khách."
                    )

                elif not phone.strip():

                    st.error(
                        "Vui lòng nhập số điện thoại."
                    )

                elif check_out <= check_in:

                    st.error(
                        "Ngày trả phải sau ngày nhận."
                    )

                else:

                    room_info = rooms[
                        rooms["Phòng"] == room_number
                    ].iloc[0]

                    booking = pd.DataFrame([{

                        "Mã đặt phòng":
                            generate_booking_id(),

                        "Khách hàng":
                            customer_name,

                        "SĐT":
                            phone,

                        "Phòng":
                            room_number,

                        "Loại phòng":
                            room_info["Loại phòng"],

                        "Ngày nhận":
                            str(check_in),

                        "Ngày trả":
                            str(check_out),

                        "Số khách":
                            number_of_guests,

                        "Trạng thái":
                            "Đã đặt",

                        "Ngày tạo":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            )
                    }])

                    st.session_state.bookings = pd.concat(
                        [
                            st.session_state.bookings,
                            booking
                        ],
                        ignore_index=True
                    )

                    update_room(
                        room_number,

                        **{
                            "Trạng thái": "Đang ở",
                            "Khách": customer_name,
                            "SĐT": phone,
                            "Ngày nhận": str(check_in),
                            "Ngày trả": str(check_out)
                        }
                    )

                    st.success(
                        f"Đặt phòng {room_number} thành công!"
                    )

    st.divider()

    st.subheader(
        "📑 Danh sách đặt phòng"
    )

    if len(st.session_state.bookings) > 0:

        st.dataframe(
            st.session_state.bookings,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Chưa có đặt phòng nào."
        )

# =========================================================
# NHẬN PHÒNG
# =========================================================

elif menu == "👤 Nhận phòng":

    st.subheader("👤 Nhận phòng")

    rooms = st.session_state.rooms

    available_rooms = rooms[
        rooms["Trạng thái"] == "Trống"
    ]

    if len(available_rooms) == 0:

        st.warning(
            "Không còn phòng trống để nhận phòng."
        )

    else:

        with st.form("checkin_form"):

            customer_name = st.text_input(
                "Họ và tên khách *"
            )

            phone = st.text_input(
                "Số điện thoại *"
            )

            col1, col2 = st.columns(2)

            with col1:

                room_number = st.selectbox(
                    "Phòng",
                    available_rooms["Phòng"].tolist()
                )

            with col2:

                check_in = st.date_input(
                    "Ngày nhận",
                    value=date.today()
                )

            check_out = st.date_input(
                "Ngày trả",
                value=date.today()
            )

            guests = st.number_input(
                "Số lượng khách",
                min_value=1,
                max_value=10,
                value=2
            )

            submit = st.form_submit_button(
                "🔑 Xác nhận nhận phòng",
                type="primary"
            )

            if submit:

                if not customer_name.strip():

                    st.error(
                        "Vui lòng nhập tên khách."
                    )

                elif not phone.strip():

                    st.error(
                        "Vui lòng nhập số điện thoại."
                    )

                elif check_out <= check_in:

                    st.error(
                        "Ngày trả phải sau ngày nhận."
                    )

                else:

                    update_room(
                        room_number,

                        **{
                            "Trạng thái": "Đang ở",
                            "Khách": customer_name,
                            "SĐT": phone,
                            "Ngày nhận": str(check_in),
                            "Ngày trả": str(check_out)
                        }
                    )

                    st.success(
                        f"Đã nhận phòng {room_number} "
                        f"cho {customer_name}."
                    )

                    st.rerun()

# =========================================================
# TRẢ PHÒNG
# =========================================================

elif menu == "🚪 Trả phòng":

    st.subheader("🚪 Trả phòng")

    rooms = st.session_state.rooms

    occupied_rooms = rooms[
        rooms["Trạng thái"] == "Đang ở"
    ]

    if len(occupied_rooms) == 0:

        st.info(
            "Hiện không có phòng đang được sử dụng."
        )

    else:

        room_number = st.selectbox(
            "Chọn phòng trả",
            occupied_rooms["Phòng"].tolist()
        )

        room = occupied_rooms[
            occupied_rooms["Phòng"] == room_number
        ].iloc[0]

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🏨 Phòng",
                room["Phòng"]
            )

        with c2:

            st.metric(
                "👤 Khách",
                room["Khách"]
            )

        with c3:

            st.metric(
                "💰 Giá/đêm",
                money(room["Giá/đêm"])
            )

        st.write("")

        st.info(
            f"Khách **{room['Khách']}** đang ở "
            f"phòng **{room['Phòng']}**."
        )

        if st.button(
            "🚪 Xác nhận trả phòng",
            type="primary",
            use_container_width=True
        ):

            update_room(
                room_number,

                **{
                    "Trạng thái": "Đang dọn",
                    "Khách": "",
                    "SĐT": "",
                    "Ngày nhận": "",
                    "Ngày trả": ""
                }
            )

            st.success(
                f"Phòng {room_number} đã trả phòng."
            )

            st.rerun()

        st.divider()

        st.subheader(
            "🧹 Cập nhật sau khi dọn phòng"
        )

        if st.button(
            "✅ Đã dọn xong – phòng sẵn sàng",
            use_container_width=True
        ):

            update_room(
                room_number,

                **{
                    "Trạng thái": "Trống"
                }
            )

            st.success(
                f"Phòng {room_number} đã sẵn sàng bán."
            )

            st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🏨 Hotel Room Manager | "
    "Ứng dụng quản lý phòng khách sạn bằng Streamlit"
)
