import streamlit as st
import datetime
import pandas as pd
import time
from shared_data import meals, meal_nutrition, meal_allergens, gluten_meals, status_colors

# ---------- Page Setup ----------
st.set_page_config(page_title="Hospital Meal Substitution", layout="centered")
st.title("🏥 Danville Hospital Meal App")

# ---------- Session State Init ----------
if "login_complete" not in st.session_state:
    st.session_state.login_complete = False
if "qr_shown" not in st.session_state:
    st.session_state.qr_shown = False
    st.session_state.qr_verified = False
if "meal_schedule" not in st.session_state:
    st.session_state.meal_schedule = {}
if "caregiver_patients" not in st.session_state:
    st.session_state.caregiver_patients = {
        "Mr. Perry (Family)": {
            "meal_schedule": {},
            "meal_times": {},
            "meal_time_preferences": {
                "Breakfast": "08:00",
                "Lunch": "12:00",
                "Dinner": "18:00"
            },
            "diet_preference": "None",
            "allergies": ["Gluten"]
        },
        "Ms. Candace (Friend)": {
            "meal_schedule": {},
            "meal_times": {},
            "meal_time_preferences": {
                "Breakfast": "08:00",
                "Lunch": "12:00",
                "Dinner": "18:00"
            },
            "diet_preference": "Vegetarian",
            "allergies": []
        }
    }

# ---------- Login Section ----------
def login_section():
    st.sidebar.title("🔐 Login")

    # Show logout if already logged in
    if st.session_state.get("login_complete"):
        role = st.session_state.get("role")
        name_map = {
            "patient": "Mr. Perry",
            "staff": "Hospital Staff",
            "caregiver": "Caregiver"
        }
        st.sidebar.success(f"Welcome, {name_map.get(role, 'User')}")
        if st.sidebar.button("🚪 Log Out"):
            st.session_state.clear()
            st.rerun()
        return

    # Role selection with true default placeholder
    role_options = {
        "": "Select Role",
        "patient": "Patient",
        "staff": "Hospital Staff",
        "caregiver": "Caregiver"
    }
    selected_role_key = st.sidebar.selectbox("Login as", list(role_options.keys()), format_func=lambda x: role_options[x])

    if selected_role_key == "":
        return

    if selected_role_key == "patient":
        login_method = st.sidebar.selectbox(
            "Choose Login Method",
            ["", "QR Code Scan", "Manual Wristband Entry"],
            format_func=lambda x: "Select Login Method" if x == "" else x
        )

        if login_method == "":
            return

        if login_method == "QR Code Scan" and not st.session_state.get("qr_verified"):
            st.sidebar.image("jhfO2hPKTO.gif", caption="Scanning QR Code...", use_container_width=True)
            st.session_state.qr_shown = True
            time.sleep(3)
            st.session_state.qr_verified = True
            st.session_state.login_complete = True
            st.session_state.role = "patient"
            st.rerun()

        elif login_method == "Manual Wristband Entry":
            wristband_id = st.sidebar.text_input("Enter Wristband ID")
            if wristband_id:
                st.session_state.login_complete = True
                st.session_state.role = "patient"
                st.sidebar.success(f"✅ Wristband ID '{wristband_id}' accepted")

    elif selected_role_key == "staff":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if username and password:
            # Placeholder logic
            st.session_state.login_complete = True
            st.session_state.role = "staff"
            st.sidebar.success("✅ Login successful")

    elif selected_role_key == "caregiver":
        invite_code = st.sidebar.text_input("Enter Invite Code")
        if invite_code:
            st.session_state.login_complete = True
            st.session_state.role = "caregiver"
            st.sidebar.success("✅ Login successful")

def render_meal_selection_for_type(meal_type, selected_date, meals, meal_nutrition, meal_allergens, status_colors):
    date_str = selected_date.isoformat()
    meal_data = st.session_state.meal_schedule[date_str][meal_type]
    selected_meal = meal_data["meal"]

    # Time + status check
    meal_pref_default = st.session_state.meal_time_preferences.get(meal_type, "08:00")
    meal_time = st.session_state.meal_times.get(date_str, {}).get(meal_type, meal_pref_default)
    if isinstance(meal_time, str):
        meal_time = datetime.datetime.strptime(meal_time, "%H:%M").time()
    scheduled_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=meal_time.hour, minute=meal_time.minute
    )
    is_past = scheduled_dt < datetime.datetime.now()
    if is_past and meal_data["status"] == "Scheduled":
        meal_data["status"] = "Past"

    st.markdown(f"### 🍽️ {meal_type}")
    st.markdown(f"**Current Meal:** {selected_meal}")
    st.markdown(f"**Status:** :{status_colors[meal_data['status']]}[\u25cf] {meal_data['status']}")
    st.markdown(f"**Rating:** ⭐ {meal_data['rating']} / 5")

    if not is_past and st.session_state.get("can_edit_meals", True):
        col1, col2, col3 = st.columns([5, 3, 3])
        with col1:
            if st.session_state.get("can_edit_meals", True):
                if st.button(f"✏️Edit {meal_type}", key=f"edit_{meal_type}_{date_str}"):
                    st.session_state[f"{meal_type}_edit_mode_{date_str}"] = True

                if st.session_state.get(f"{meal_type}_edit_mode_{date_str}", False):
                    raw_options = meals[meal_type]
                    display_options = []

                    for meal in raw_options:
                        allergens = meal_allergens.get(meal, [])
                        matching_allergens = [a for a in allergens if a in st.session_state.allergies]
                        label = f"⚠️ {meal} ({', '.join(matching_allergens)})" if matching_allergens else meal
                        display_options.append(label)

                    current_allergens = meal_allergens.get(selected_meal, [])
                    current_matching = [a for a in current_allergens if a in st.session_state.allergies]
                    current_display = f"⚠️ {selected_meal} ({', '.join(current_matching)})" if current_matching else selected_meal
                    selected_idx = display_options.index(current_display) if current_display in display_options else 0

                    selected_label = st.selectbox(
                        "",
                        options=display_options,
                        index=selected_idx,
                        key=f"{meal_type}_selectbox_{date_str}",
                        label_visibility="collapsed"
                    )

                    cleaned_meal = selected_label.replace("⚠️ ", "").split(" (")[0]
                    selected_allergens = meal_allergens.get(cleaned_meal, [])

                    if st.button(f"Confirm {meal_type} Change", key=f"confirm_{meal_type}_{date_str}"):
                        if any(a in st.session_state.allergies for a in selected_allergens):
                            st.error("This meal contains ingredients you're allergic to and cannot be selected.")
                        else:
                            st.session_state.meal_schedule[date_str][meal_type]["meal"] = cleaned_meal
                            st.session_state[f"{meal_type}_edit_mode_{date_str}"] = False
                            st.rerun()

        done_key = f"done_{meal_type}_{date_str}"
        if done_key not in st.session_state:
            st.session_state[done_key] = False
        with col2:
            if st.session_state.get("can_edit_meals", True):
                if st.button("✅ Received Meal", key=done_key + "_btn"):
                    st.session_state[done_key] = True
        if st.session_state[done_key]:
            st.session_state.meal_schedule[date_str][meal_type]["status"] = "Completed"
            st.session_state[done_key] = False
            st.rerun()

        skip_key = f"skip_{meal_type}_{date_str}"
        if skip_key not in st.session_state:
            st.session_state[skip_key] = False
        with col3:
            if st.session_state.get("can_edit_meals", True):
                if st.button("🚫 Skip Meal", key=skip_key + "_btn"):
                    st.session_state[skip_key] = True
        if st.session_state[skip_key]:
            st.session_state.meal_schedule[date_str][meal_type]["status"] = "Skipped"
            st.session_state[skip_key] = False
            st.rerun()

        # Time input
        if "meal_times" not in st.session_state:
            st.session_state.meal_times = {}
        if date_str not in st.session_state.meal_times:
            st.session_state.meal_times[date_str] = {}

        meal_pref_default = st.session_state.meal_time_preferences.get(meal_type, datetime.time(8, 0))
        raw_time = st.session_state.meal_times[date_str].get(meal_type, meal_pref_default)
        if isinstance(raw_time, str):
            raw_time = datetime.datetime.strptime(raw_time, "%H:%M").time()

        widget_key = f"schedule_time_{meal_type}_{date_str}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = raw_time

        selected_time = st.time_input(
            f"⏰ Schedule {meal_type}",
            value=st.session_state[widget_key],
            key=widget_key
        )
        st.session_state.meal_times[date_str][meal_type] = selected_time

    elif is_past:
        if st.session_state.get("can_edit_meals", True):
            st.info(
                f"⏳ This meal is in the past (scheduled for {scheduled_dt.strftime('%I:%M %p')}). No further changes allowed.")

    if st.session_state.get("can_edit_meals", True):
        meal_data["rating"] = st.slider(
            f"Rate {meal_type}", 0, 5, meal_data["rating"],
            key=f"{meal_type}_rating_{date_str}"
        )

    with st.expander("🔍 View Nutrition Info"):
        if selected_meal in meal_nutrition:
            image_url = meal_nutrition[selected_meal].get("Image")
            if image_url:
                st.image(image_url, width=300, caption=selected_meal)
            st.write("### Nutrition Facts")
            for key, value in meal_nutrition[selected_meal].items():
                if key != "Image":
                    st.write(f"- **{key}**: {value}")
        else:
            st.info("Nutrition info for this meal is not available.")

    st.markdown("---")


# ---------- Main App ---------- (USED FOR BOTH PATIENT AND CAREGIVER, )
def main_app():

    # Ensure preferences have defaults early
    # --- Initialize session state defaults early ---
    if "diet_preference" not in st.session_state:
        st.session_state.diet_preference = "None"

    if "allergies" not in st.session_state:
        st.session_state.allergies = ["Gluten"]

    if "meal_time_preferences" not in st.session_state:
        st.session_state.meal_time_preferences = {
            "Breakfast": "08:00",
            "Lunch": "12:00",
            "Dinner": "18:00"
        }

    if "meal_times" not in st.session_state:
        st.session_state.meal_times = {}

    allergies = st.session_state.get("allergies", [])
    if st.session_state.get("role") != "caregiver":
        if allergies:
            st.warning(f"⚠️ Chart indicates this patient has allergies: **{', '.join(allergies)}**")
        else:
            st.success("✅ No known allergies.")

    diet = st.session_state.get("diet_preference", "None")
    if st.session_state.get("role") != "caregiver":
        if diet and diet != "None":
            st.info(f"🍽️ Dietary preference: **{diet}**")
        else:
            st.success("✅ No dietary restrictions selected.")

    selected_date = st.date_input("📅 Select a Date", datetime.date.today())
    date_str = selected_date.isoformat()

    if date_str not in st.session_state.meal_schedule:
        st.session_state.meal_schedule[date_str] = {
            "Breakfast": {"meal": meals["Breakfast"][0], "status": "Scheduled", "rating": 0},
            "Lunch": {"meal": meals["Lunch"][0], "status": "Scheduled", "rating": 0},
            "Dinner": {"meal": meals["Dinner"][0], "status": "Scheduled", "rating": 0}
        }

    if "selected_meal_for_nutrition" not in st.session_state:
        st.session_state.selected_meal_for_nutrition = None

    # ----------------------------
    # TABS
    # ----------------------------
    if st.session_state.get("role") == "caregiver":
        tab1, tab2, tab3 = st.tabs(["🍽️ Meal Selection", "📊 Nutrition Info", "🔑 Manage Permissions"])
    else:
        tab1, tab2, tab3 = st.tabs(["🍽️ Meal Selection", "📊 Nutrition Info", "⚙️ User Preferences"])

    # ----------------------------
    # MEAL SELECTION
    # ----------------------------
    with tab1:
        st.subheader(f"Meals for {selected_date.strftime('%A, %B %d, %Y')}")

        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            render_meal_selection_for_type(meal_type, selected_date, meals, meal_nutrition, meal_allergens,
                                           status_colors)

    # ----------------------------
    # NUTRITION INFO
    # ----------------------------
    with tab2:
        st.subheader("🔍 View Meal Nutrition Info")

        meal_list = list(meal_nutrition.keys())
        default_meal = (
            st.session_state.selected_meal_for_nutrition
            if st.session_state.selected_meal_for_nutrition in meal_nutrition
            else meal_list[0]
        )
        selected_info_meal = st.selectbox(
            "Select a Meal",
            meal_list,
            index=meal_list.index(default_meal)
        )

        # ✅ Show image if available
        image_url = meal_nutrition[selected_info_meal].get("Image")
        if image_url:
            st.image(image_url, width=300, caption=selected_info_meal)
        else:
            st.write("_No image available for this meal._")

        st.write("### Nutrition Facts")
        for key, value in meal_nutrition[selected_info_meal].items():
            if key != "Image":
                st.write(f"- **{key}**: {value}")

    # ----------------------------
    # USER PREFERENCES
    # ----------------------------
    with tab3:
        if st.session_state.get("role") == "patient":
            st.subheader("⚙️ Dietary Preferences")

            # Ensure defaults are initialized
            if "diet_preference" not in st.session_state:
                st.session_state.diet_preference = "None"
            if "allergies" not in st.session_state:
                st.session_state.allergies = ["Gluten"]

            # Let widgets directly manage the state
            st.radio(
                "Dietary Preference",
                ["None", "Vegetarian", "Vegan", "Keto", "Low Sodium", "Diabetic", "Halal", "Kosher"],
                index=["None", "Vegetarian", "Vegan", "Keto", "Low Sodium", "Diabetic", "Halal", "Kosher"].index(
                    st.session_state.diet_preference
                ),
                key="diet_preference"
            )

            st.multiselect(
                "Known Allergies",
                ["Gluten", "Dairy", "Nuts", "Shellfish", "Soy", "Eggs"],
                default=st.session_state.allergies,
                key="allergies"
            )

            st.subheader("🕒 Preferred Meal Times")

            # Defaults if not already set
            if "meal_time_preferences" not in st.session_state:
                st.session_state.meal_time_preferences = {
                    "Breakfast": "08:00",
                    "Lunch": "12:00",
                    "Dinner": "18:00"
                }

            for meal_type in ["Breakfast", "Lunch", "Dinner"]:
                st.time_input(
                    f"{meal_type} Time",
                    value=st.session_state.meal_time_preferences[meal_type],
                    key=f"pref_time_{meal_type}"
                )

            st.success("Your preferences are saved for this session.")
            st.markdown(f"**Diet:** {st.session_state.diet_preference}")
            st.markdown(f"**Allergies:** {', '.join(st.session_state.allergies) if st.session_state.allergies else 'None'}")

        if st.session_state.get("role") == "caregiver":
            st.subheader("🔑 Manage Permissions")

            current_patient = st.session_state.get("current_patient_name", "Unknown")
            current_permission = "Full Access" if st.session_state.get("can_edit_meals", False) else "View Only"

            st.markdown(f"**Currently Viewing:** `{current_patient}`")
            st.markdown(f"**Your Permission Level:** `{current_permission}`")

            st.markdown("---")
            st.subheader("📬 Request Additional Permissions")

            # Define all possible permission options
            base_permissions = [
                "View Meal Selection",
                "View Nutritional Details",
                "Schedule Meals",
                "Change Dietary Preferences",
                "Edit Meal Ratings",
                "Access Preferences Tab"
            ]

            # Determine which are already granted based on patient
            already_granted = []
            if "Perry" in current_patient:
                already_granted = base_permissions  # Full access
            elif "Candace" in current_patient:
                already_granted = ["View Meal Selection", "View Nutritional Details"]

            # Build display options
            dropdown_options = []
            option_map = {}  # maps display string -> raw permission string

            for perm in base_permissions:
                if perm in already_granted:
                    label = f"{perm} ✅(already granted)"
                else:
                    label = perm
                dropdown_options.append(label)
                option_map[label] = perm

            # Add a blank first entry for clarity
            selected_display = st.selectbox("Select permission to request", [""] + dropdown_options)

            if st.button("Request More Access"):
                if selected_display and selected_display in option_map:
                    perm_requested = option_map[selected_display]
                    if perm_requested in already_granted:
                        st.info(f"ℹ️ You already have access to '{perm_requested}'.")
                    else:
                        st.success(f"✅ Request to add '{perm_requested}' permission has been submitted.")
                else:
                    st.error("Please select a permission to request.")

            st.markdown("---")
            st.subheader("🗑️ Remove This Patient")
            if st.button("Remove This Patient from My Care List"):
                st.session_state.caregiver_patients.pop(current_patient, None)
                st.success("✅ Patient removed from your dashboard.")
                st.rerun()

            st.markdown("---")
            st.subheader("➕ Request Access to New Patient")
            new_patient_name = st.text_input("Enter patient name")
            if st.button("Request Access"):
                if new_patient_name.strip():
                    st.success(f"✅ Request submitted to manage patient: {new_patient_name.strip()}")
                else:
                    st.error("Please enter a valid patient name.")

# ---------- Caregiver Dashboard ----------
def caregiver_dashboard():
    st.subheader("👩‍👦 Caregiver Dashboard")
    patient_names = list(st.session_state.caregiver_patients.keys())
    dropdown_options = [""] + patient_names + ["➕ Add New Patient"]

    selected_patient = st.selectbox(
        "Select a patient to view",
        dropdown_options,
        format_func=lambda x: "Select a patient..." if x == "" else x
    )

    # Handle Add New Patient
    if selected_patient == "➕ Add New Patient":
        st.subheader("📝 Request Access to New Patient")

        new_name = st.text_input("Patient Full Name")
        new_relationship = st.selectbox("Relationship", ["", "Family", "Friend", "Legal Guardian", "Conservator",
                                                         "Other (explain below)"])
        request_message = st.text_area("Justification (Optional)")

        if st.button("Submit Request"):
            if new_name.strip():
                st.success(
                    f"✅ Request submitted to manage patient: **{new_name.strip()}** as **{new_relationship}**.")
                st.info("You’ll be notified when access is granted.")
            else:
                st.error("Patient name is required.")

    # Handle Existing Patient
    elif selected_patient:
        # Permissions logic
        if "Perry" in selected_patient:
            permissions = {
                "can_edit": True,
                "description": "Permissions: View Meal Schedule, Schedule Meals, Change Preferences"
            }
        else:
            permissions = {
                "can_edit": False,
                "description": "Permissions: View Meal Schedule"
            }

        st.session_state.can_edit_meals = permissions["can_edit"]
        st.session_state.current_patient_name = selected_patient

        st.info(f"🔒 {permissions['description']}", icon="🔐")

        # Load patient data
        patient_data = st.session_state.caregiver_patients[selected_patient]
        st.session_state.meal_schedule = patient_data["meal_schedule"]
        st.session_state.meal_times = patient_data["meal_times"]
        st.session_state.meal_time_preferences = patient_data["meal_time_preferences"]
        st.session_state.diet_preference = patient_data["diet_preference"]
        st.session_state.allergies = patient_data["allergies"]

        # Render dashboard
        main_app()

        # Save any updates (only if editable)
        if st.session_state.can_edit_meals:
            st.session_state.caregiver_patients[selected_patient] = {
                "meal_schedule": st.session_state.meal_schedule,
                "meal_times": st.session_state.meal_times,
                "meal_time_preferences": st.session_state.meal_time_preferences,
                "diet_preference": st.session_state.diet_preference,
                "allergies": st.session_state.allergies
            }

# ---------- Hospital Staff Dashboard ----------
def staff_dashboard():
    st.subheader("🧑‍⚕️ Hospital Staff Dashboard")

    # Initialize session state for staff patients
    if "staff_patients" not in st.session_state:
        st.session_state.staff_patients = {
            "Mr. Perry": {
                "room": "A101",
                "diet_preference": "None",
                "allergies": ["Gluten"],
                "restrictions": ["No pork"],
                "caregiver": "Phineas (Family)",
                "time_blocks": [{"start": "12:00", "end": "14:00", "reason": "Fasting required"}]
        },
            "Ms. Candace": {
                "room": "B205",
                "diet_preference": "Vegetarian",
                "allergies": [],
                "restrictions": ["Fasting until noon"],
                "caregiver": "Baljeet (Friend)",
                "time_blocks": [{"start": "14:00", "end": "18:00", "reason": "Operation"}]
            }
        }

    tab1, tab2, tab3 = st.tabs(["📋 Patient Overview", "➕ Admit Patient", "🛠️ Manage Restrictions"])

    # --------------------------
    # Tab 1: Patient Overview
    # --------------------------
    with tab1:
        st.markdown("### 👥 All Patients")
        search = st.text_input("Search by patient name")

        for name, info in st.session_state.staff_patients.items():
            if search and search.lower() not in name.lower():
                continue

            col1, col2 = st.columns([9, 1])
            with col1:
                with st.expander(f"🧍 {name} - Room {info['room']}"):
                    st.markdown(f"**Dietary Preference:** {info['diet_preference']}")
                    st.markdown(f"**Allergies:** {', '.join(info['allergies']) if info['allergies'] else 'None'}")
                    st.markdown(
                        f"**Restrictions:** {', '.join(info['restrictions']) if info['restrictions'] else 'None'}")
                    st.markdown(f"**Assigned Caregiver:** {info['caregiver'] if info['caregiver'] else 'None'}")

                    col_schedule, col_order = st.columns(2)
                    with col_schedule:
                        schedule_key = f"show_schedule_{name}"
                        if schedule_key not in st.session_state:
                            st.session_state[schedule_key] = False

                        if st.button(f"View Schedule for {name}", key=f"view_schedule_{name}"):
                            st.session_state[schedule_key] = not st.session_state[schedule_key]

                        if st.session_state[schedule_key]:
                            st.markdown(f"### 🗓️ Schedule for {name} — Room {info['room']}")

                            time_blocks = info.get("time_blocks", [])
                            if not time_blocks:
                                st.info("No restricted time windows have been added.")
                            else:
                                for block in sorted(time_blocks, key=lambda b: datetime.datetime.strptime(b['start'], '%H:%M')):
                                    st.markdown(
                                        f"- **{block['start']} – {block['end']}** &nbsp;&nbsp; | &nbsp;&nbsp; _{block['reason']}_"
                                    )

                    with col_order:
                        if st.button(f"Order Meal for {name}", key=f"prompt_order_{name}"):
                            st.session_state[f"show_order_{name}"] = not st.session_state.get(f"show_order_{name}",
                                                                                              False)

                    if st.session_state.get(f"show_order_{name}", False):
                        st.markdown("---")
                        st.markdown(f"### 🍽️  Order a Meal for {name}")
                        order_date = st.date_input("Select date", datetime.date.today(), key=f"order_date_{name}")
                        meal_type_order = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner"],
                                                       key=f"order_type_{name}")
                        meal_choice = st.selectbox("Meal", meals[meal_type_order], key=f"order_meal_{name}")

                        order_time = st.time_input("Select time", value=datetime.time(12, 0), key=f"order_time_{name}")

                        # Check against restricted time blocks
                        restriction_blocks = info.get("time_blocks", [])
                        selected_minutes = order_time.hour * 60 + order_time.minute
                        time_conflict = False

                        for block in restriction_blocks:
                            start = datetime.datetime.strptime(block["start"], "%H:%M")
                            end = datetime.datetime.strptime(block["end"], "%H:%M")
                            start_min = start.hour * 60 + start.minute
                            end_min = end.hour * 60 + end.minute
                            if start_min <= selected_minutes < end_min:
                                time_conflict = True
                                conflict_reason = block["reason"]
                                break

                        # Check for allergens
                        selected_allergens = meal_allergens.get(meal_choice, [])
                        allergies = info.get("allergies", [])
                        matching_allergies = [a for a in selected_allergens if a in allergies]

                        if time_conflict:
                            st.error(f"⛔ Cannot schedule during restricted time block: {block['start']} – {block['end']} ({conflict_reason})")

                        elif matching_allergies:
                            st.error(
                                f"🚫 Cannot order '{meal_choice}' due to {name}'s allergies: {', '.join(matching_allergies)}")

                        elif st.button("Order Meal", key=f"order_btn_{name}"):
                            if "staff_orders" not in st.session_state:
                                st.session_state.staff_orders = {}
                            key = (name, order_date.isoformat())
                            if key not in st.session_state.staff_orders:
                                st.session_state.staff_orders[key] = {}
                            st.session_state.staff_orders[key][meal_type_order] = meal_choice
                            st.success(
                                f"✅ Ordered {meal_choice} for {name} on {order_date.strftime('%b %d')} ({meal_type_order})")

            with col2:
                with st.container():
                    if st.button("🗑️", key=f"delete_icon_{name}"):
                        st.session_state["confirm_delete_patient"] = name

            # Inline warning confirmation if flagged
            if st.session_state.get("confirm_delete_patient") == name:
                st.warning(f"⚠️ You are about to permanently delete **{name}**. This action cannot be undone.")
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("Yes, Delete Patient", key=f"confirm_{name}"):
                        del st.session_state.staff_patients[name]
                        st.session_state.pop("confirm_delete_patient", None)
                        st.success(f"✅ Patient {name} has been removed.")
                        st.rerun()
                with col_cancel:
                    if st.button("Cancel Deletion", key=f"cancel_{name}"):
                        st.session_state.pop("confirm_delete_patient", None)
                        st.rerun()
                st.markdown("---")
                continue

    # --------------------------
    # Tab 2: Admit New Patient
    # --------------------------
    with tab2:
        st.markdown("### 🏥 Admit a New Patient")
        new_name = st.text_input("Patient Full Name")
        new_room = st.text_input("Room Number")
        new_diet = st.selectbox("Dietary Preference", ["None", "Vegetarian", "Vegan", "Keto", "Low Sodium", "Diabetic", "Halal", "Kosher"])
        new_allergies = st.multiselect("Allergies", ["Gluten", "Dairy", "Nuts", "Shellfish", "Soy", "Eggs"])
        new_restrictions = st.text_area("Medical/Dietary Restrictions (comma separated)")
        new_caregiver = st.text_input("Assigned Caregiver (if any)")

        if st.button("Admit Patient"):
            if not new_name or not new_room:
                st.error("Patient name and room number are required.")
            else:
                st.session_state.staff_patients[new_name] = {
                    "room": new_room,
                    "diet_preference": new_diet,
                    "allergies": new_allergies,
                    "restrictions": [r.strip() for r in new_restrictions.split(",") if r.strip()],
                    "caregiver": new_caregiver
                }
                st.success(f"✅ {new_name} has been admitted to Room {new_room}.")

    # --------------------------
    # Tab 3: Manage Restrictions
    # --------------------------
    with tab3:
        st.markdown("### 🧾 Manage Patient Restrictions")
        patient_list = list(st.session_state.staff_patients.keys())
        selected_patient = st.selectbox("Select a patient", [""] + patient_list)

        if selected_patient:
            patient_info = st.session_state.staff_patients[selected_patient]

            updated_diet = st.selectbox("Update Dietary Preference", ["None", "Vegetarian", "Vegan", "Keto", "Low Sodium", "Diabetic", "Halal", "Kosher"], index=["None", "Vegetarian", "Vegan", "Keto", "Low Sodium", "Diabetic", "Halal", "Kosher"].index(patient_info["diet_preference"]))
            updated_allergies = st.multiselect("Update Allergies", ["Gluten", "Dairy", "Nuts", "Shellfish", "Soy", "Eggs"], default=patient_info["allergies"])
            updated_restrictions = st.text_area("Update Restrictions (comma separated)", value=", ".join(patient_info["restrictions"]))

            if st.button("Save Changes"):
                patient_info["diet_preference"] = updated_diet
                patient_info["allergies"] = updated_allergies
                patient_info["restrictions"] = [r.strip() for r in updated_restrictions.split(",") if r.strip()]
                st.success(f"✅ Restrictions updated for {selected_patient}.")

            st.markdown("---")
            st.markdown("### ⏰ Time-Based Restrictions")

            patient_info.setdefault("time_blocks", [])

            # Show existing time blocks
            if patient_info["time_blocks"]:
                for i, block in enumerate(sorted(patient_info["time_blocks"],
                                                 key=lambda b: datetime.datetime.strptime(b["start"], "%H:%M"))):
                    st.markdown(f"- `{block['start']} – {block['end']}` | **{block['reason']}**")
            else:
                st.info("No time-based restrictions.")

            # Add a new one
            st.markdown("#### ➕ Add New Time Block")
            start_time = st.time_input("Start Time", key="time_block_start")
            end_time = st.time_input("End Time", key="time_block_end")
            reason = st.selectbox("Reason", ["Fasting required", "In operation", "Scheduled procedure", "Other"])

            if st.button("Add Time Restriction"):
                if start_time >= end_time:
                    st.error("End time must be after start time.")
                else:
                    patient_info["time_blocks"].append({
                        "start": start_time.strftime("%H:%M"),
                        "end": end_time.strftime("%H:%M"),
                        "reason": reason
                    })
                    st.success("✅ Time restriction added.")
                    st.rerun()


# ---------- Run App ----------
login_section()

if not st.session_state.get("login_complete"):
    st.subheader("Welcome, order here.")
    st.info("Please log in using the sidebar to continue.")
else:
    role = st.session_state.get("role")
    if role == "patient":
        main_app()
    elif role == "caregiver":
        caregiver_dashboard()
    elif role == "staff":
        staff_dashboard()
