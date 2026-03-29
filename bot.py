from telegram import Update
import imghdr
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime # Import datetime
from operator import itemgetter # Import itemgetter for sorting

TOKEN = "Your_Token_Here"

# ================= DATA =================

bus_data = [

    # ===== Galle → Kandy =====
    {"from": "galle", "to": "kandy", "time": "6:15 AM", "price": "Rs.1500", "duration": "4h 30min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kandy", "time": "2:30 PM", "price": "Rs.1500", "duration": "4h 30min", "boarding": "Galle Highway Bus Stand"},

    # ===== Kandy → Galle =====
    {"from": "kandy", "to": "galle", "time": "5:20 AM", "price": "Rs.1500", "duration": "4h 30min", "boarding": "Kandy Bus Stand"},

    # ===== Galle → Kadawatha =====
    {"from": "galle", "to": "kadawatha", "time": "4:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "7:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "2:00 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},

    # ===== Kadawatha → Galle =====
    {"from": "kadawatha", "to": "galle", "time": "5:00 AM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "1:00 PM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},

    # ===== Galle → Makumbura =====
    {"from": "galle", "to": "makumbura", "time": "4:30 AM", "price": "Rs.870", "duration": "1h 30min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "5:00 AM", "price": "Rs.870", "duration": "1h 30min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "6:00 AM", "price": "Rs.870", "duration": "1h 30min", "boarding": "Galle Highway Bus Stand"},

    # ===== Makumbura → Galle =====
    {"from": "makumbura", "to": "galle", "time": "5:00 AM", "price": "Rs.870", "duration": "1h 30min", "boarding": "Makumbura Multimodal Center"},

    # ===== Galle → Kaduwela =====
    {"from": "galle", "to": "kaduwela", "time": "4:30 AM", "price": "", "duration": "1h 45min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kaduwela", "time": "10:30 AM", "price": "", "duration": "1h 45min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kaduwela", "time": "6:00 PM", "price": "", "duration": "1h 45min", "boarding": "Galle Highway Bus Stand"},

    # ===== Kaduwela → Galle =====
    {"from": "kaduwela", "to": "galle", "time": "5:00 AM", "price": "", "duration": "1h 45min", "boarding": "Kaduwela Bus Stand"},
]


# ================= FUNCTION =================

def get_next_bus(buses):
    now = datetime.now()

    future_buses = []
    all_buses = []

    for bus_dict in buses:
        try:
            bus_time = datetime.strptime(bus_dict["time"], "%I:%M %p")
            bus_time = bus_time.replace(year=now.year, month=now.month, day=now.day)

            all_buses.append((bus_time, bus_dict))

            if bus_time > now:
                future_buses.append((bus_time, bus_dict))
        except ValueError: # Catch specific error for strptime if time format is unexpected
            continue
        except Exception as e: # Catch other potential errors during processing
            print(f"Error processing bus data: {bus_dict}, Error: {e}")
            continue

    if future_buses:
        future_buses.sort(key=itemgetter(0)) # Sort by the datetime object
        return future_buses[0][1], "today"
    elif all_buses: # Only if there are buses in all_buses (after filtering invalid times)
        all_buses.sort(key=itemgetter(0)) # Sort by the datetime object
        return all_buses[0][1], "tomorrow"
    else:
        return None, None # Return None for both if no valid bus data could be processed

# ================= BOT =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    want_next = "next" in text
    want_price = "price" in text
    want_time = "time" in text

    found = []

    for bus_dict in bus_data:
        # Check if both 'from' and 'to' keywords are in the user's text
        from_loc_in_text = bus_dict["from"].lower() in text
        to_loc_in_text = bus_dict["to"].lower() in text

        if from_loc_in_text and to_loc_in_text: # Ensure both from and to are present
            found.append(bus_dict)

    reply = ""

    if found:
        # Unpack the returned tuple into bus_info (dict) and day_str (string)
        bus_info, day_str = get_next_bus(found)

        if bus_info: # Check if a bus was successfully found
            bus = bus_info # 'bus' is now the dictionary as intended

            price = bus["price"] if bus["price"] else "Price not available yet"
            boarding = bus["boarding"] if bus["boarding"] else "Boarding point not available yet"

            if want_price:
                reply = f"💰 Price: {price}"
            elif want_time:
                reply = f"⏰ Time: {bus['time']}"
            else:
                reply = f"""
🟢 Next Bus ({day_str.title()})

🚌 {bus['from'].title()} → {bus['to'].title()}
⏰ Time: {bus['time']}
💰 Price: {price}
📍 Boarding: {boarding}
🕒 Duration: {bus['duration']}
"""
        else:
            reply = "No bus information available for this route today or tomorrow 😢"
    else:
        reply = "No buses found for this route."

    await update.message.reply_text(reply)

# ================= RUN =================

import nest_asyncio
import asyncio

nest_asyncio.apply()

# Global variable to hold the running application instance
running_app = None

async def main():
    global running_app

    # If an app instance is already running, attempt to stop and shutdown
    if running_app:
        print("Stopping existing bot instance...")
        try:
            await running_app.stop()
            await running_app.shutdown()
        except Exception as e:
            print(f"Error gracefully stopping previous app instance: {e}")
        running_app = None # Reset the running app

    # Create a new application instance
    running_app = ApplicationBuilder().token(TOKEN).build()
    if running_app is None: # Added check for None
        print("Error: ApplicationBuilder().build() returned None. Check TOKEN or environment setup.")
        return # Exit main() if app creation failed

    running_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    # Run polling. This will block until the bot is stopped.
    await running_app.run_polling(close_loop=False) # Changed here: close_loop=False
    print("Bot stopped.")

# This block ensures that the asyncio loop is properly handled in Colab
# If the cell is executed multiple times, it tries to restart the bot.
try:
    asyncio.run(main())
except RuntimeError as e:
    if "Cannot run a second event loop while the first is still running" in str(e):
        print("An event loop is already running. Attempting to stop and restart the bot...")
        if running_app:
            try:
                # Running stop/shutdown within a new event loop might be needed in some Colab scenarios
                # However, for simple restarts, the main() logic should handle it now.
                asyncio.run(running_app.stop()) # Ensure the current running app is stopped
                asyncio.run(running_app.shutdown()) # Shutdown the application properly
                print("Previous bot instance stopped. Restarting main...")
                asyncio.run(main()) # Attempt to run main again
            except Exception as restart_e:
                print(f"Failed to restart bot gracefully: {restart_e}. You might need to restart the Colab runtime.")
        else:
            print(f"RuntimeError: {e}. No running_app instance to stop. Please restart Colab runtime.")
    else:
        raise
except KeyboardInterrupt:
    print("Bot stopped by user via KeyboardInterrupt.")
    if running_app:
        try:
            asyncio.run(running_app.stop())
            asyncio.run(running_app.shutdown())
        except Exception as e:
            print(f"Error during shutdown after KeyboardInterrupt: {e}")
