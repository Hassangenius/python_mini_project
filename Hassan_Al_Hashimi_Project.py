import streamlit as st
import pandas as pd
import json
import os

os.makedirs("plant_photos", exist_ok=True)

CSV_FILE = "plants_data.csv"


st.title("My Project")


# --- main part i did ----

text = st.selectbox(
    "Plants",
    (
        "Add a new plant to the collection",
        "Record a plant care activity",
        "Record plant growth",
        "Plants due for care",
        "Search plants by name or location",
        "View all plants",
        "View growth history",
        "Diagnose a plant",
        "Plant type tips"
    )
)


# --- Add Plant part ---
if text == "Add a new plant to the collection":

    name_plant = st.text_input("Plant name")
    plant_type = st.selectbox(
    "Plant type",
    [
        "Tree",
        "Herb",
        "Flowering Plant",
        "Succulent"
    ]
)

    plant_location = st.text_input("Location in Home")

    plant_date = st.date_input("Date acquired")

    watering = st.number_input(
        "Watering frequency (days)",
        min_value=1,
        step=1
    )

    fertilizing = st.number_input(
        "Fertilizing frequency (days)",
        min_value=1,
        step=1
    )

    pruning = st.number_input(
        "Pruning frequency (days)",
        min_value=1,
        step=1
    )

    repotting = st.number_input(
        "Repotting frequency (days)",
        min_value=1,
        step=1
    )

    sunlight_needs = st.selectbox(
        "Sunlight needs",
        ["Low", "Medium", "High"]
    )

    plant_photo = st.file_uploader(
        "Upload a photo of the plant",
        type=["jpg", "jpeg", "png"],
        key="plant_photo_uploader"
    )

    if st.button("Save"):

        
        photo_path = ""

        if plant_photo is not None:

            photo_filename = plant_photo.name

            photo_path = os.path.join(
                "plant_photos",
                photo_filename
            )

            with open(photo_path, "wb") as f:
                f.write(plant_photo.getbuffer())

        
        new_data = pd.DataFrame({
            "Plant": [name_plant],
            "Plant_Type": [plant_type],
            "Location": [plant_location],
            "Date": [plant_date],
            "Watering": [watering],
            "Fertilizing": [fertilizing],
            "Pruning": [pruning],
            "Repotting": [repotting],
            "Sunlight": [sunlight_needs],
            "Photo": [photo_path],
            "Last_Watering": [pd.NaT],
            "Last_Fertilizing": [pd.NaT],
            "Last_Pruning": [pd.NaT],
            "Last_Repotting": [pd.NaT]
        })

     

                

        try:
            existing_data = pd.read_csv(CSV_FILE)

        except FileNotFoundError:
            existing_data = pd.DataFrame()

        if existing_data.empty:

            updated_data = new_data

        else:

            updated_data = pd.concat(
                [existing_data, new_data],
                ignore_index=True
            )

        updated_data = updated_data.drop_duplicates(
            subset=["Plant", "Location"],
            keep="first"
        )

        

        updated_data.to_csv(
            CSV_FILE,
            index=False
        )

        st.success("Plant saved!")



# --- Record Care Activity code i wrote---
elif text == "Record a plant care activity":

    try:
        df = pd.read_csv("plants_data.csv")

        

        # Ensure Last_ columns exist
        for col in [
            "Last_Watering",
            "Last_Fertilizing",
            "Last_Pruning",
            "Last_Repotting"
        ]:
            if col not in df.columns:
                df[col] = pd.NaT

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

        plant_name = st.selectbox(
            "Which plant was cared for?",
            df["Plant"].unique()
        )

        activity = st.selectbox(
            "What activity was performed?",
            [
                "Watering",
                "Fertilizing",
                "Repotting",
                "Pruning"
            ]
        )

        if st.button("Save activity"):

            today = pd.Timestamp.today().floor("s")

            df.loc[
                df["Plant"] == plant_name,
                f"Last_{activity}"
            ] = today

            
            df.to_csv(
                CSV_FILE,
                index=False
)


            st.success(
                f"{activity} recorded for "
                f"{plant_name} on {today.date()}!"
            )

    except (FileNotFoundError, pd.errors.EmptyDataError):


        st.warning(
            "No plant data found. Please add plants first."
        )



# --- Record Plant Growth my favorite part ---
elif text == "Record plant growth":

    try:
        df = pd.read_csv(CSV_FILE)


        if df.empty:
            st.warning(
                "No plants found. Please add plants first."
            )

        else:
            plant_name = st.selectbox(
                "Which plant grew?",
                df["Plant"].unique()
            )

            growth_cm = st.number_input(
                "Increased height (cm)",
                min_value=0.0,
                step=0.1,
                format="%.1f"
            )

            growth_date = st.date_input(
                "Measurement date"
            )

            if st.button("Save growth"):

                
                if "Growth_Date" not in df.columns:
                    df["Growth_Date"] = pd.NaT
                else:
                    df["Growth_Date"] = pd.to_datetime(
                        df["Growth_Date"],
                        errors="coerce"
                    )

               
                if "Growth_cm" not in df.columns:
                    df["Growth_cm"] = 0.0
                else:
                    df["Growth_cm"] = pd.to_numeric(
                        df["Growth_cm"],
                        errors="coerce"
                    )

                
                plant_index = df[
                    df["Plant"] == plant_name
                ].index

                if len(plant_index) > 0:

                    
                    df.loc[
                        plant_index,
                        "Growth_Date"
                    ] = pd.Timestamp(growth_date)

                   
                    df.loc[
                        plant_index,
                        "Growth_cm"
                    ] = growth_cm

                    
                    df.to_csv(
                        CSV_FILE,
                        index=False
)


                    st.success(
                        f"{growth_cm:.1f} cm growth recorded "
                        f"for {plant_name}!"
                    )

    except FileNotFoundError:

        st.warning(
            "No plant data found. Please add plants first."
        )




            

# --- Plants Due for Care section---

# --- below is not functional yet , no enough time ----

elif text == "Plants due for care":

    try:

        df = pd.read_csv(CSV_FILE)

        if df.empty:

            st.warning(
                "No plants found. Please add plants first."
            )

        else:

          
            current_month = pd.Timestamp.now().month

            if current_month in [3, 4, 5]:
                season = "Spring"

            elif current_month in [6, 7, 8]:
                season = "Summer"

            elif current_month in [9, 10, 11]:
                season = "Autumn"

            else:
                season = "Winter"

            st.subheader(
                f"🌱 Care Schedule - {season}"
            )

            st.info(
                f"Current season: **{season}**"
            )

           

            def get_seasonal_frequency(
                plant_type,
                activity,
                base_frequency,
                season
            ):

                frequency = base_frequency

                

                if plant_type == "Tree":

                    if activity == "Watering":

                        if season == "Summer":
                            frequency = base_frequency * 0.7

                        elif season == "Winter":
                            frequency = base_frequency * 1.5

                    elif activity == "Fertilizing":

                        if season == "Spring":
                            frequency = base_frequency * 0.7

                        elif season == "Summer":
                            frequency = base_frequency * 0.8

                        elif season == "Winter":
                            frequency = base_frequency * 2

                    elif activity == "Pruning":

                        if season == "Winter":
                            frequency = base_frequency * 1.5

                    elif activity == "Repotting":

                        if season != "Spring":
                            frequency = base_frequency * 1.5

              

                elif plant_type == "Herb":

                    if activity == "Watering":

                        if season == "Summer":
                            frequency = base_frequency * 0.7

                        elif season == "Winter":
                            frequency = base_frequency * 1.5

                    elif activity == "Fertilizing":

                        if season == "Spring":
                            frequency = base_frequency * 0.7

                        elif season == "Summer":
                            frequency = base_frequency * 0.8

                        elif season == "Winter":
                            frequency = base_frequency * 2

                    elif activity == "Pruning":

                        if season in ["Spring", "Summer"]:
                            frequency = base_frequency * 0.8

                        elif season == "Winter":
                            frequency = base_frequency * 1.5

                    elif activity == "Repotting":

                        if season != "Spring":
                            frequency = base_frequency * 1.5

                

                elif plant_type == "Flowering Plant":

                    if activity == "Watering":

                        if season == "Summer":
                            frequency = base_frequency * 0.7

                        elif season == "Winter":
                            frequency = base_frequency * 1.5

                    elif activity == "Fertilizing":

                        if season in ["Spring", "Summer"]:
                            frequency = base_frequency * 0.7

                        elif season == "Autumn":
                            frequency = base_frequency * 1.5

                        elif season == "Winter":
                            frequency = base_frequency * 2

                    elif activity == "Pruning":

                        if season == "Spring":
                            frequency = base_frequency * 0.8

                        elif season == "Winter":
                            frequency = base_frequency * 1.5

                    elif activity == "Repotting":

                        if season != "Spring":
                            frequency = base_frequency * 1.5

                

                elif plant_type == "Succulent":

                    if activity == "Watering":

                        if season == "Summer":
                            frequency = base_frequency * 0.9

                        elif season == "Winter":
                            frequency = base_frequency * 2

                        elif season == "Autumn":
                            frequency = base_frequency * 1.5

                    elif activity == "Fertilizing":

                        if season == "Spring":
                            frequency = base_frequency * 0.8

                        elif season == "Summer":
                            frequency = base_frequency

                        elif season in ["Autumn", "Winter"]:
                            frequency = base_frequency * 2

                    elif activity == "Pruning":

                        if season == "Winter":
                            frequency = base_frequency * 1.5

                    elif activity == "Repotting":

                        if season != "Spring":
                            frequency = base_frequency * 1.5

               
                return max(1, round(frequency))

            

            today = pd.Timestamp.now().normalize()

            care_types = [
                "Watering",
                "Fertilizing",
                "Pruning",
                "Repotting"
            ]

            df["Date"] = pd.to_datetime(
                df["Date"],
                errors="coerce"
            ).dt.normalize()

            # --------------------------------
            # Make sure Last columns exist
            # --------------------------------

            for activity in care_types:

                last_col = f"Last_{activity}"

                if last_col not in df.columns:

                    df[last_col] = pd.NaT

                df[last_col] = pd.to_datetime(
                    df[last_col],
                    errors="coerce"
                ).dt.normalize()

            

            due_rows = []

            for index, row in df.iterrows():

                plant_name = row["Plant"]
                plant_type = row["Plant_Type"]

                due_activities = []

                for activity in care_types:

                    base_frequency = pd.to_numeric(
                        row[activity],
                        errors="coerce"
                    )

                    if pd.isna(base_frequency):
                        continue

                    
                    seasonal_frequency = get_seasonal_frequency(
                        plant_type,
                        activity,
                        base_frequency,
                        season
                    )

                    last_col = f"Last_{activity}"

                    last_date = row[last_col]

                    
                    if pd.isna(last_date):

                        last_date = row["Date"]

                    if pd.isna(last_date):
                        continue

                    
                    next_date = (
                        last_date
                        + pd.Timedelta(
                            days=seasonal_frequency
                        )
                    )

                   
                    if next_date <= today:

                        due_activities.append(
                            f"{activity} "
                            f"(every {seasonal_frequency} days)"
                        )

                if due_activities:

                    due_rows.append({
                        "Plant": plant_name,
                        "Plant Type": plant_type,
                        "Location": row["Location"],
                        "Season": season,
                        "Due": ", ".join(
                            due_activities
                        )
                    })

            

            if not due_rows:

                st.success(
                    "🌱 No plants are currently due for care."
                )

            else:

                due_df = pd.DataFrame(
                    due_rows
                )

                st.warning(
                    "🌱 Plants due for care:"
                )

                st.dataframe(
                    due_df,
                    use_container_width=True
                )

    except FileNotFoundError:

        st.warning(
            "No plant data found. Please add plants first."
        )
# --- the part above above does't work partially 

# --- here's my search input part---
elif text == "Search plants by name or location":

    search_query = st.text_input(
        "Enter plant name or location"
    )

    if search_query:

        try:

            df = pd.read_csv(CSV_FILE)


            results = df[
                (
                    df["Plant"].str.contains(
                        search_query,
                        case=False,
                        na=False
                    )
                )
                |
                (
                    df["Location"].str.contains(
                        search_query,
                        case=False,
                        na=False
                    )
                )
            ]

            st.write("Search results:")
            st.dataframe(results)

        except (FileNotFoundError, pd.errors.EmptyDataError):


            st.write("")


# --- View All Plants section ---
elif text == "View all plants":

    try:

        df = pd.read_csv(CSV_FILE)


        st.write("Plants:")
        st.dataframe(
            df,
            use_container_width=True
        )

    except FileNotFoundError:

        st.write("")




# --- View Growth History i did---

elif text == "View growth history":

    try:
        df = pd.read_csv(CSV_FILE)


        if "Growth_Date" not in df.columns or "Growth_cm" not in df.columns:

            st.info(
                "No growth measurements recorded yet."
            )

        else:

            growth_df = df[
                [
                    "Plant",
                    "Growth_Date",
                    "Growth_cm"
                ]
            ].copy()

            
            growth_df = growth_df[
                growth_df["Growth_Date"].notna()
            ]

            if growth_df.empty:

                st.info(
                    "No growth measurements recorded yet."
                )

            else:

                st.write(
                    "🌱 Plant Growth History"
                )

                st.dataframe(
                    growth_df,
                    use_container_width=True
                )

    except (FileNotFoundError, pd.errors.EmptyDataError):


        st.info(
            "No growth measurements recorded yet."
        )

# --- Diagnose Plant part ---

elif text == "Diagnose a plant":

    st.subheader("🌱 Plant Diagnosis")

    symptoms = st.multiselect(
    "Select the symptoms you see:",
    [
        "Yellow leaves",
        "Slow growth",
        "Brown/black spots",
        "Root problems"
    ]
)


    if st.button("Diagnose"):

        if not symptoms:

            st.warning(
                "Please select at least one symptom."
            )

        else:

            
            diagnoses = []

            
            if "Yellow leaves" in symptoms:

                diagnoses.append({
                    "Cause": "Overwatering",
                    "Why": "Yellow leaves can occur when the soil remains too wet for too long.",
                    "What to check": "Check whether the soil is constantly wet and whether the pot has drainage holes.",
                    "Action": "Allow the soil to dry appropriately between waterings and check drainage."
                })

                diagnoses.append({
                    "Cause": "Nutrient deficiency",
                    "Why": "A lack of nutrients can cause leaves to become pale or yellow.",
                    "What to check": "Check when the plant was last fertilized and whether the older leaves are affected first.",
                    "Action": "Consider an appropriate fertilizer if the plant has not been fertilized for a long time."
                })

                diagnoses.append({
                    "Cause": "Insufficient light",
                    "Why": "Some plants can develop yellowing leaves when they do not receive enough light.",
                    "What to check": "Check how much natural or artificial light the plant receives.",
                    "Action": "Move the plant to a location with suitable light for its species."
                })

           
            if "Slow growth" in symptoms:

                diagnoses.append({
                    "Cause": "Insufficient light",
                    "Why": "Plants need adequate light for photosynthesis and healthy growth.",
                    "What to check": "Check whether the plant is receiving enough light for its species.",
                    "Action": "Move it to a brighter suitable location if necessary."
                })

                diagnoses.append({
                    "Cause": "Insufficient nutrients",
                    "Why": "A lack of nutrients can reduce new growth.",
                    "What to check": "Check the plant's fertilizing history.",
                    "Action": "Consider an appropriate fertilizer during the plant's active growing period."
                })

                diagnoses.append({
                    "Cause": "Root problems",
                    "Why": "Damaged, crowded, or unhealthy roots can restrict growth.",
                    "What to check": "Check for root crowding, poor drainage, or signs of root damage.",
                    "Action": "Inspect the roots if other symptoms suggest a root problem."
                })



                        
            if "Brown/black spots" in symptoms:

                diagnoses.append({
                    "Cause": "Fungal or bacterial leaf infection",
                    "Why": "Brown or black spots can occur when fungal or bacterial pathogens affect the leaves.",
                    "What to check": "Look for spots that are spreading, have defined edges, or occur on multiple leaves.",
                    "Action": "Remove severely affected leaves, avoid getting water on the foliage, and improve air circulation around the plant."
                })

                diagnoses.append({
                    "Cause": "Overwatering or poor drainage",
                    "Why": "Excess moisture around the roots can contribute to stress and conditions that encourage leaf spotting.",
                    "What to check": "Check whether the soil remains wet for long periods and whether the pot drains properly.",
                    "Action": "Check drainage and allow the soil to dry appropriately between waterings."
                })

                diagnoses.append({
                    "Cause": "Leaf damage or environmental stress",
                    "Why": "Sunburn, cold damage, or physical damage can produce brown or dark areas on leaves.",
                    "What to check": "Consider whether the plant was recently moved, exposed to strong direct sunlight, or exposed to cold.",
                    "Action": "Move the plant to a suitable environment and avoid sudden changes in light or temperature."
                })


            
            if "Root problems" in symptoms:

                diagnoses.append({
                    "Cause": "Root rot",
                    "Why": "Persistently wet soil can damage roots and cause them to become soft, brown, or black.",
                    "What to check": "If you inspect the roots, healthy roots are generally firm, while rotting roots may be soft, dark, or have an unpleasant smell.",
                    "Action": "Check drainage and reduce excessive watering. Severely damaged roots may need to be removed."
                })

                diagnoses.append({
                    "Cause": "Poor drainage",
                    "Why": "Water that cannot drain away from the root zone can deprive roots of oxygen.",
                    "What to check": "Check whether the container has drainage holes and whether water remains in the bottom of the pot.",
                    "Action": "Improve drainage and make sure the plant is growing in an appropriate potting medium."
                })

                diagnoses.append({
                    "Cause": "Root-bound plant",
                    "Why": "A plant with roots tightly filling its container can have difficulty accessing water, nutrients, and growing space.",
                    "What to check": "Look for roots circling densely around the inside of the pot.",
                    "Action": "Consider repotting into an appropriately sized container if the plant is severely root-bound."
                })

            
            if diagnoses:

                st.write("### Possible causes")

                for diagnosis in diagnoses:

                    st.write(
                        f"**{diagnosis['Cause']}**"
                    )

                    st.write(
                        f"**Why:** {diagnosis['Why']}"
                    )

                    st.write(
                        f"**What to check:** "
                        f"{diagnosis['What to check']}"
                    )

                    st.write(
                        f"**Suggested action:** "
                        f"{diagnosis['Action']}"
                    )

                    st.divider()


# --- Plant Type Tips part---

elif text == "Plant type tips":

    st.subheader("🌱 Plant Type Tips")

    plant_type = st.selectbox(
        "Choose a plant type",
        [
            "Tree",
            "Herb",
            "Flowering Plant",
            "Succulent"
        ]
    )

    tips = {

        "Tree": [
            "Water deeply when the soil is dry.",
            "Prune dead or damaged branches.",
            "Make sure the roots have enough space.",
            "Check regularly for pests."
        ],

        "Herb": [
            "Provide plenty of suitable light.",
            "Water when the soil begins to dry.",
            "Harvest regularly to encourage new growth.",
            "Remove yellow or damaged leaves."
        ],

        "Flowering Plant": [
            "Provide enough light for flowering.",
            "Remove faded flowers.",
            "Avoid overwatering.",
            "Fertilize during active growth."
        ],

        "Succulent": [
            "Allow the soil to dry between watering.",
            "Use well-draining soil.",
            "Avoid standing water.",
            "Provide plenty of suitable sunlight."
        ]
    }

    st.write(f"### Tips for {plant_type}")

    for tip in tips[plant_type]:
        st.write(f"🌱 {tip}")

# --- API part is not completed yet ----

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= "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"
)

def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="cohere/north-mini-code:free",
        messages=[
            {
                "role": "system",
                "content": "Plants Doctor",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response


    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= "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"
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= "usr-LzZDWq6FDlRdmmo4yj-pqmo1KVHuPJKvYz4sff5sTic"
)

def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="cohere/north-mini-code:free",
        messages=[
            {
                "role": "system",
                "content": "Plants Doctor",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response
