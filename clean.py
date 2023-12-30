import pandas as pd
import json
import ast

# Load the CSV file
file_path = "telegram_messages_views.csv"
df = pd.read_csv(file_path)

# Check the first few rows of the dataframe to understand its structure
df.head()


def format_text_entities_to_markdown(text_entities):
    """Formats the text entities into markdown string."""
    formatted_text = ""

    try:
        # Convert the string representation of list to a Python list
        entities = ast.literal_eval(text_entities)

        # Format each entity
        for entity in entities:
            if entity["type"] == "text_link":
                formatted_text += f"[{entity['text']}]({entity['href']})"
            else:
                formatted_text += entity["text"]
        # remove the line with 频道：@NewlearnerChannel
        formatted_text = formatted_text.replace("频道：@NewlearnerChannel", "")
        formatted_text = formatted_text.replace("频道： @NewlearnerChannel", "")
        # remove with label #news
        if (
            formatted_text.find("#News") != -1
            or formatted_text.find("#Newsletter") != -1
            or formatted_text.find("#Keyboards") != -1
            or formatted_text.find("#days") != -1
            or formatted_text.find("#羊毛") != -1
            or formatted_text.find("#") == -1
            or len(formatted_text) < 100
        ):
            return pd.NA
        # remove excess \n at the end of text
        formatted_text = formatted_text.rstrip("\n")
        # remove excess \n at the beginning of text
        formatted_text = formatted_text.lstrip("\n")
    except:
        # Return original text if formatting fails
        return text_entities

    return formatted_text


# Apply the formatting to the 'text_entities' column
df["formatted_text_entities"] = df["text_entities"].apply(
    lambda x: format_text_entities_to_markdown(x)
    if pd.notnull(x) and x != "[]"
    else pd.NA
)

# Filter out rows with NaN in 'formatted_text_entities'
formatted_texts_entities = df["formatted_text_entities"].dropna()


# Combine texts into one string separated by '==='
combined_formatted_text = "\n===\n".join(
    formatted_texts_entities
)  # Display first 1000 characters for preview
# save combined text to file
with open("texts.txt", "w") as f:
    f.write(combined_formatted_text)
