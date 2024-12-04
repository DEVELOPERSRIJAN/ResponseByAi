from pyrogram import Client, filters
import aiohttp
from info import *

# Generate a detailed prompt for image creation
def generate_long_query(query):
    return f"{query}."

@Client.on_message(filters.command("draw"))
async def draw_image(client, message):
    if FSUB and not await get_fsub(client, message):
        return
    if len(message.command) < 2:
        await message.reply_text("To generate an image, write /draw and your prompt next to it. 😊")
        return

    # Generate a long query for better image results
    user_query = message.text.split(" ", 1)[1]
    query = generate_long_query(user_query)

    # Send initial message
    wait_message = await message.reply_text("⏳")

    # Asynchronous request using aiohttp
    url = f"https://text2img.codesearch.workers.dev/?prompt={query}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.json()
                    if "imageUrl" in image_data:
                        image_url = image_data["imageUrl"]
                        await wait_message.delete()  # Delete wait message
                        await message.reply_photo(photo=image_url, caption=f"Generated Image for: {user_query} 🖼️")
                    else:
                        await wait_message.edit_text("Oops! Something's wrong here! ❌")
                else:
                    await wait_message.edit_text("Error: Unable to generate image at this time. Please try later. 🚫")
    except Exception as e:
        # Try to edit or delete the message only if it exists
        try:
            await wait_message.edit_text(f"An error occurred: {e} ⚠️")
        except Exception:
            await message.reply_text(f"An error occurred: {e} ⚠️")
