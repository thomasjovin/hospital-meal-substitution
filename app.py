import streamlit as st
import datetime
import time

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


# ---------- Main App ----------
def main_app():
    # Ensure preferences have defaults early
    if "diet_preference" not in st.session_state:
        st.session_state.diet_preference = "None"
    if "allergies" not in st.session_state:
        st.session_state.allergies = ["Gluten"]
    allergies = st.session_state.get("allergies", [])
    # Allergies warning
    allergies = st.session_state.get("allergies", [])
    if allergies:
        st.warning(f"⚠️ Chart indicates this patient has allergies: **{', '.join(allergies)}**")
    else:
        st.success("✅ No known allergies.")

    # Dietary preference warning
    diet = st.session_state.get("diet_preference", "None")
    if diet and diet != "None":
        st.info(f"🍽️ Dietary preference: **{diet}**")
    else:
        st.success("✅ No dietary restrictions selected.")

    # ----------------------------
    # Shared Data + Setup
    # ----------------------------
    meals = {
        "Breakfast": [
            "Eggs Benedict, Orange",
            "Oatmeal with Berries",
            "Scrambled Eggs and Toast",
            "Greek Yogurt Parfait",
            "Pancakes with Banana"
        ],
        "Lunch": [
            "Tuna Salad, Brussel Sprouts",
            "Chicken Fajitas",
            "Turkey Sandwich",
            "Grilled Chicken and Salad",
            "Tofu Stir-Fry",
            "Bone Broth Soup"
        ],
        "Dinner": [
            "Shrimp Linguine and Jello",
            "Japanese Curry",
            "Baked Salmon with Quinoa",
            "Spaghetti and Meatballs",
            "Vegetable Stir-Fry"
        ]
    }

    meal_nutrition = {
        "Eggs Benedict, Orange": {
            "Calories": 400,
            "Protein": "18g",
            "Total Fat": "25g",
            "Carbs": "25g",
            "Image": "https://www.allrecipes.com/thmb/QVMaPhXnj1HQ70C7Ka9WYtuipHg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/17205-eggs-benedict-DDMFS-4x3-a0042d5ae1da485fac3f468654187db0.jpg"
        },
        "Oatmeal with Berries": {
            "Calories": 300,
            "Protein": "6g",
            "Total Fat": "4g",
            "Carbs": "50g",
            "Image": "https://media.post.rvohealth.io/wp-content/uploads/2024/06/oatmeal-bowl-blueberries-strawberries-breakfast-732x549-thumbnail.jpg"
        },
        "Scrambled Eggs and Toast": {
            "Calories": 350,
            "Protein": "15g",
            "Total Fat": "20g",
            "Carbs": "30g",
            "Image": "https://whereismyspoon.co/wp-content/uploads/2019/07/scrambled-eggs-on-toast-1.jpg"
        },
        "Greek Yogurt Parfait": {
            "Calories": 180,
            "Protein": "12g",
            "Sugar": "10g",
            "Fat": "3g",
            "Image": "https://i1.wp.com/www.kiwiandcarrot.com/wp-content/uploads/2018/01/BLOG-4-4.jpg?fit=680%2C958&ssl=1"
        },
        "Pancakes with Banana": {
            "Calories": 350,
            "Protein": "9g",
            "Carbs": "60g",
            "Total Fat": "7g",
            "Image": "https://www.allrecipes.com/thmb/6x0Lw9L4MEU8INHnK4tXGRV9XWI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20334-banana-pancakes-i-DDMFS-4x3-9f291f03044247d48c9ec26917952402.jpg"
        },
        "Tuna Salad, Brussel Sprouts": {
            "Calories": 450,
            "Protein": "30g",
            "Total Fat": "22g",
            "Carbs": "20g",
            "Image": "https://starkist.com/wp-content/uploads/2019/09/recipes_lemon_tuna_shaved_brussel_sprout_salad_910x445.jpg"
        },
        "Chicken Fajitas": {
            "Calories": 500,
            "Protein": "30g",
            "Total Fat": "4g",
            "Carbs": "10g",
            "Image": "https://www.everydayfamilycooking.com/wp-content/uploads/2022/03/chicken-fajita-wrap11.jpg"
        },
        "Turkey Sandwich": {
            "Calories": 420,
            "Protein": "26g",
            "Carbs": "40g",
            "Total Fat": "15g",
            "Image": "https://www.eatingonadime.com/wp-content/uploads/2022/03/eod-turkey-sandwich-5-2.jpg"
        },
        "Grilled Chicken and Salad": {
            "Calories": 380,
            "Protein": "35g",
            "Total Fat": "10g",
            "Carbs": "15g",
            "Image": "https://www.eatingbirdfood.com/wp-content/uploads/2023/06/grilled-chicken-salad-hero.jpg"
        },
        "Tofu Stir-Fry": {
            "Calories": 350,
            "Protein": "18g",
            "Carbs": "30g",
            "Fat": "15g",
            "Image": "https://www.wellplated.com/wp-content/uploads/2022/03/Tofu-Broccoli-Stir-Fry-Recipe.jpg"
        },
        "Bone Broth Soup": {
            "Calories": 200,
            "Protein": "14g",
            "Fat": "5g",
            "Carbs": "10g",
            "Image": "https://freshwaterpeaches.com/wp-content/uploads/2022/01/Chicken-Bone-Broth-Soup-6.jpg"
        },
        "Shrimp Linguine and Jello": {
            "Calories": 600,
            "Protein": "25g",
            "Carbs": "50g",
            "Fat": "20g",
            "Image": "https://www.melskitchencafe.com/wp-content/uploads/2023/02/creamy-garlic-shrimp-pasta12-640x878.jpg"
        },
        "Japanese Curry": {
            "Calories": 550,
            "Protein": "22g",
            "Carbs": "60g",
            "Fat": "18g",
            "Image": "https://sudachirecipes.com/wp-content/uploads/2022/08/Japanese-curry-using-roux-thumbnail.jpg"
        },
        "Baked Salmon with Quinoa": {
            "Calories": 520,
            "Protein": "35g",
            "Fat": "25g",
            "Carbs": "30g",
            "Image": "https://www.jessicagavin.com/wp-content/uploads/2016/02/mediterranean-spiced-salmon-over-vegetable-quinoa-1200.jpg"
        },
        "Spaghetti and Meatballs": {
            "Calories": 640,
            "Protein": "30g",
            "Fat": "28g",
            "Carbs": "60g",
            "Image": "https://embed.widencdn.net/img/beef/lkfopyh4v0/1120x630px/classic%20spaghetti%20&%20meatballs%2002.tif?keep=c&u=nvwl20"
        },
        "Vegetable Stir-Fry": {
            "Calories": 320,
            "Protein": "10g",
            "Fat": "12g",
            "Carbs": "40g",
            "Image": "https://www.dinneratthezoo.com/wp-content/uploads/2019/02/vegetable-stir-fry-3.jpg"
        }
    }

    gluten_meals = [
        "Pancakes with Banana",
        "Spaghetti and Meatballs",
        "Scrambled Eggs and Toast"
    ]

    status_colors = {
        "Pending": "gray",
        "Completed": "green",
        "Skipped": "red"
    }
    meal_allergens = {
        "Pancakes with Banana": ["Gluten", "Eggs"],
        "Spaghetti and Meatballs": ["Gluten"],
        "Scrambled Eggs and Toast": ["Gluten", "Eggs"],
        "Tuna Salad, Brussel Sprouts": ["Eggs"],
        "Bone Broth Soup": ["Shellfish"],
        "Greek Yogurt Parfait": ["Dairy"],
        # Add more mappings as needed
    }

    selected_date = st.date_input("📅 Select a Date", datetime.date.today())
    date_str = selected_date.isoformat()

    if date_str not in st.session_state.meal_schedule:
        st.session_state.meal_schedule[date_str] = {
            "Breakfast": {"meal": meals["Breakfast"][0], "status": "Pending", "rating": 0},
            "Lunch": {"meal": meals["Lunch"][0], "status": "Pending", "rating": 0},
            "Dinner": {"meal": meals["Dinner"][0], "status": "Pending", "rating": 0}
        }

    if "selected_meal_for_nutrition" not in st.session_state:
        st.session_state.selected_meal_for_nutrition = None

    # ----------------------------
    # TABS
    # ----------------------------
    tab1, tab2, tab3 = st.tabs(["🍽️ Meal Selection", "📊 Nutrition Info", "⚙️ User Preferences"])

    # ----------------------------
    # MEAL SELECTION
    # ----------------------------
    with tab1:
        st.subheader(f"Meals for {selected_date.strftime('%A, %B %d, %Y')}")

        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            meal_data = st.session_state.meal_schedule[date_str][meal_type]
            selected_meal = meal_data["meal"]

            st.markdown(f"### 🍽️ {meal_type}")
            st.markdown(f"**Current Meal:** {selected_meal}")
            st.markdown(f"**Status:** :{status_colors[meal_data['status']]}[●] {meal_data['status']}")
            st.markdown(f"**Rating:** ⭐ {meal_data['rating']} / 5")

            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                if st.button(f"✏️ Edit {meal_type}", key=f"edit_{meal_type}_{date_str}"):
                    st.session_state[f"{meal_type}_edit_mode_{date_str}"] = True

                if st.session_state.get(f"{meal_type}_edit_mode_{date_str}", False):
                    raw_options = meals[meal_type]
                    display_options = []

                    for meal in raw_options:
                        allergens = meal_allergens.get(meal, [])
                        matching_allergens = [a for a in allergens if a in st.session_state.allergies]
                        if matching_allergens:
                            label = f"⚠️ {meal} ({', '.join(matching_allergens)})"
                        else:
                            label = meal
                        display_options.append(label)

                    # Determine currently selected meal label
                    current_allergens = meal_allergens.get(selected_meal, [])
                    current_matching = [a for a in current_allergens if a in st.session_state.allergies]
                    current_display = f"⚠️ {selected_meal} ({', '.join(current_matching)})" if current_matching else selected_meal
                    selected_idx = display_options.index(current_display) if current_display in display_options else 0

                    # Selection + Confirm Button
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
                            st.rerun()  # force update to apply change

            done_key = f"done_{meal_type}_{date_str}"
            if done_key not in st.session_state:
                st.session_state[done_key] = False

            with col2:
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
                if st.button("🚫 Skip Meal", key=skip_key + "_btn"):
                    st.session_state[skip_key] = True

            if st.session_state[skip_key]:
                st.session_state.meal_schedule[date_str][meal_type]["status"] = "Skipped"
                st.session_state[skip_key] = False
                st.rerun()

            meal_data["rating"] = st.slider(
                f"Rate {meal_type}", 0, 5, meal_data["rating"],
                key=f"{meal_type}_rating_{date_str}"
            )

            # Nutrition Info Dropdown
            with st.expander("🔍 View Nutrition Info"):
                if selected_meal in meal_nutrition:
                    image_url = meal_nutrition[selected_meal].get("Image")
                    if image_url:
                        st.image(image_url, width=300, caption=selected_meal)
                    else:
                        st.write("_No image available for this meal._")

                    st.write("### Nutrition Facts")
                    for key, value in meal_nutrition[selected_meal].items():
                        if key != "Image":
                            st.write(f"- **{key}**: {value}")
                else:
                    st.info("Nutrition info for this meal is not available.")

            st.markdown("---")

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

        st.success("Your preferences are saved for this session.")
        st.markdown(f"**Diet:** {st.session_state.diet_preference}")
        st.markdown(f"**Allergies:** {', '.join(st.session_state.allergies) if st.session_state.allergies else 'None'}")


# ---------- Run App ----------
login_section()

if not st.session_state.get("login_complete"):
    st.subheader("Welcome to the Danville Hospital Meal App")
    st.info("Please log in using the sidebar to continue.")
else:
    role = st.session_state.get("role")
    if role == "patient":
        main_app()
    elif role == "staff":
        st.subheader("🧑‍⚕️ Hospital Staff Dashboard (Coming Soon)")
        st.info("This section is under construction.")
    elif role == "caregiver":
        st.subheader("👩‍👦 Caregiver Meal View (Coming Soon)")
        st.info("This section is under construction.")
