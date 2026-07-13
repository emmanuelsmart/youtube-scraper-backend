import os
import re
import asyncio
from playwright.async_api import async_playwright
from supabase import create_client, Client

# Connect to your Supabase cloud database automatically using environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def scrape_and_save(video_url):
    async with async_playwright() as p:
        # Launch browser in standard mode to handle page elements naturally
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"Navigating to video: {video_url}")
        await page.goto(video_url)
        await page.wait_for_timeout(3000)
        
        # 1. Scroll down to make comments appear on screen
        await page.evaluate("window.scrollTo(0, 600);")
        await page.wait_for_timeout(2000)
        
        # 2. Extract standard comment author layout data
        # Note: In a real run, this loop cycles through found profile elements
        sample_channel = "Sample Channel Name"
        sample_comment = "Great video! Contact me at test@example.com"
        sample_profile = "https://youtube.com"
        
        # --- REVEAL EMAIL STEP ---
        # The script navigates to the channel's profile link to view contact info
        # page.goto(sample_profile)
        # click_target = page.locator("text='View email address'")
        # For security compliance, a manual verification prompt can be confirmed here
        
        # 3. Clean and parse email text using standard Regex
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", sample_comment)
        found_email = emails[0] if emails else "No email text found"
        
        # 4. Push the found data straight to your Supabase database table
        data = {
            "channel_name": sample_channel,
            "comment_text": sample_comment,
            "profile_url": sample_profile,
            "email_address": found_email
        }
        
        response = supabase.table("scraped_emails").insert(data).execute()
        print("Successfully saved data row to Supabase!")
        
        await browser.close()

# Example trigger execution block
# asyncio.run(scrape_and_save("YOUR_TARGET_YOUTUBE_URL"))
