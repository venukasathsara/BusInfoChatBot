from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta # Import datetime
from operator import itemgetter # Import itemgetter for sorting
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


TOKEN = "TOKEN"

# ================= DATA =================

bus_data = [

    # ===== Galle → Kandy =====
    {"from": "galle", "to": "kandy", "time": "6:15 AM", "price": "Rs.1500", "duration": "4h 30min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kandy", "time": "2:30 PM", "price": "Rs.1500", "duration": "4h 30min", "boarding": "Galle Highway Bus Stand"},

    # ===== Kandy → Galle =====
    {"from": "kandy", "to": "galle", "time": "5:20 AM", "price": "Rs.1500", "duration": "4h 30min", "boarding": "Kandy Bus Stand"},
    {"from": "kandy", "to": "galle", "time": "3:00 PM", "price": "Rs.1500", "duration": "4h 30min", "boarding": "Kandy Bus Stand"},

    # ===== Galle → Kadawatha =====
    {"from": "galle", "to": "kadawatha", "time": "5:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "5:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "6:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "6:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "7:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "7:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "8:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "8:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "9:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "9:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "10:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "10:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "11:00 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "11:30 AM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "12:00 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "12:30 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "1:00 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "1:30 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "2:15 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "2:45 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "3:15 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "3:45 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "4:15 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "4:30 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "5:00 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "5:30 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "6:00 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "6:30 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "7:00 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "7:30 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kadawatha", "time": "8:00 PM", "price": "", "duration": "1h 40min", "boarding": "Galle Highway Bus Stand"},

    # ===== Kadawatha → Galle =====
    {"from": "kadawatha", "to": "galle", "time": "6:00 AM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "7:00 AM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "8:00 AM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "9:00 AM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "10:00 AM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "11:00 AM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "12:00 PM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "1:00 PM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "2:00 PM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "3:00 PM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "4:15 PM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},
    {"from": "kadawatha", "to": "galle", "time": "5:30 PM", "price": "", "duration": "1h 40min", "boarding": "Kadawatha Bus Stand"},

    # ===== Galle → Makumbura =====
    {"from": "galle", "to": "makumbura", "time": "5:20 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "5:50 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "6:20 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "6:50 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "7:20 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "7:50 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "8:20 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "8:50 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "9:20 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "9:50 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "10:20 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "10:50 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "11:20 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "11:50 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "12:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "12:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "1:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "1:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "2:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "2:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "3:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "3:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "4:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "4:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "5:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "5:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "6:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "6:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "7:20 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "makumbura", "time": "7:50 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Galle Highway Bus Stand"},


    # ===== Makumbura → Galle =====
    {"from": "makumbura", "to": "galle", "time": "5:30 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "6:00 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "6:30 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "7:00 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "7:30 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "8:00 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "8:30 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "9:00 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "9:30 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "10:00 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "10:30 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "11:00 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "11:30 AM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "12:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "12:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "1:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "1:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "2:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "2:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "3:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "3:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "4:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "4:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "5:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "5:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "6:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "6:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "7:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "7:30 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},
    {"from": "makumbura", "to": "galle", "time": "8:00 PM", "price": "Rs.870", "duration": "1h 20min", "boarding": "Makumbura Multimodal Center"},

    # ===== Galle → Kaduwela =====
    {"from": "galle", "to": "kaduwela", "time": "4:30 AM", "price": "", "duration": "1h 45min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kaduwela", "time": "10:30 AM", "price": "", "duration": "1h 45min", "boarding": "Galle Highway Bus Stand"},
    {"from": "galle", "to": "kaduwela", "time": "6:00 PM", "price": "", "duration": "1h 45min", "boarding": "Galle Highway Bus Stand"},

    # ===== Kaduwela → Galle =====
    {"from": "kaduwela", "to": "galle", "time": "5:00 AM", "price": "", "duration": "1h 45min", "boarding": "Kaduwela Bus Stand"},
]


# ================= FUNCTION =================

def get_next_bus(buses):
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)

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

def get_next_buses(buses, count=3):
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)

    future = []

    for b in buses:
        try:
            t = datetime.strptime(b["time"], "%I:%M %p")
            t = t.replace(year=now.year, month=now.month, day=now.day)

            if t > now:
                future.append((t, b))
        except:
            continue

    future.sort(key=itemgetter(0))

    return [b for _, b in future[:count]]

# ================= BOT =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Galle → Makumbura", "Makumbura → Galle"],
        ["Galle → Kadawatha", "Kadawatha → Galle"],
        ["Galle → Kandy", "Kandy → Galle"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🚌 Smart Bus Info Bot\n\nSelect a route 👇",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    want_next = "next" in text
    want_price = "price" in text
    want_time = "time" in text
    want_all = text.startswith("all")
    want_many = "3" in text or "many" in text

    found = []

    # 🔥 FIXED route detection (IMPORTANT)
    route = text.replace("→", "to").replace("-", "to").strip()

    for bus_dict in bus_data:
        if f"{bus_dict['from']} to {bus_dict['to']}" in route:
            found.append(bus_dict)

    if not found:
        await update.message.reply_text("❌ No buses found for this route.")
        return

    bus_info, day_str = get_next_bus(found)

    if not bus_info:
        await update.message.reply_text("😢 No bus information available for this route today or tomorrow")
        return

    bus = bus_info

    price = bus["price"] if bus["price"] else "Price not available yet"
    boarding = bus["boarding"] if bus["boarding"] else "Boarding point not available yet"

    # ================= ALL =================
    if want_all:
        reply = "🚌 All Buses:\n\n"
        for b in found:
            price = b["price"] if b["price"] else "Price not available yet"
            boarding = b["boarding"] if b["boarding"] else "Boarding point not available yet"

            reply += f"""🚌 {b['from'].title()} → {b['to'].title()}
⏰ Time: {b['time']}
💰 Price: {price}
📍 Boarding: {boarding}
------------------\n"""

        await update.message.reply_text(reply)
        return

    # ================= NEXT 3 =================
    if want_many:
        buses = get_next_buses(found, 3)

        if not buses:
            await update.message.reply_text("😢 No upcoming buses")
            return

        reply = "🟢 Next 3 Buses:\n\n"
        for b in buses:
            price = b["price"] if b["price"] else "Price not available yet"
            boarding = b["boarding"] if b["boarding"] else "Boarding point not available yet"

            reply += f"""🚌 {b['from'].title()} → {b['to'].title()}
⏰ Time: {b['time']}
💰 Price: {price}
📍 Boarding: {boarding}
------------------\n"""

        await update.message.reply_text(reply)
        return

    # ================= PRICE =================
    if want_price:
        await update.message.reply_text(f"💰 Price: {price}")
        return

    # ================= TIME =================
    if want_time:
        await update.message.reply_text(f"⏰ Time: {bus['time']}")
        return

    # ================= DEFAULT (NEXT BUS + BUTTONS) =================
    reply = f"""🟢 Next Bus ({day_str.title()})

🚌 {bus['from'].title()} → {bus['to'].title()}
⏰ Time: {bus['time']}
💰 Price: {price}
📍 Boarding: {boarding}
🕒 Duration: {bus['duration']}"""

    keyboard = [
        [
            InlineKeyboardButton("Next 3 🕒", callback_data=f"next3|{bus['from']}|{bus['to']}"),
            InlineKeyboardButton("All 🚌", callback_data=f"all|{bus['from']}|{bus['to']}")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(reply, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")
    action = data[0]
    from_city = data[1]
    to_city = data[2]

    found = []

    for b in bus_data:
        if b["from"] == from_city and b["to"] == to_city:
            found.append(b)

    if action == "next3":
        buses = get_next_buses(found, 3)

        if not buses:
            reply = "😢 No upcoming buses"
        else:
            reply = "🟢 Next 3 Buses:\n\n"
            for b in buses:
                price = b["price"] if b["price"] else "Price not available yet"
                boarding = b["boarding"] if b["boarding"] else "Boarding point not available yet"

                reply += f"""🚌 {b['from'].title()} → {b['to'].title()}
⏰ Time: {b['time']}
💰 Price: {price}
📍 Boarding: {boarding}
------------------\n"""

    elif action == "all":
        reply = "🚌 All Buses:\n\n"

        for b in found:
            price = b["price"] if b["price"] else "Price not available yet"
            boarding = b["boarding"] if b["boarding"] else "Boarding point not available yet"

            reply += f"""🚌 {b['from'].title()} → {b['to'].title()}
⏰ Time: {b['time']}
💰 Price: {price}
📍 Boarding: {boarding}
------------------\n"""

    await query.edit_message_text(reply)

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
    try:
        app_instance = ApplicationBuilder().token(TOKEN).build()
    except Exception as e:
        print(f"Error building Telegram Application: {e}. Check TOKEN or environment setup.")
        return # Exit main() if app creation failed

    if app_instance is None:
        print("Error: ApplicationBuilder().build() returned None. Check TOKEN or environment setup.")
        return # Exit main() if app creation failed

    running_app = app_instance
    from telegram.ext import CommandHandler
    running_app.add_handler(CommandHandler("start", start))
    running_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    running_app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    try:
        await running_app.run_polling(close_loop=False)
    except Exception as e:
        print(f"Error during bot polling: {e}")
    finally:
        # Ensure cleanup even if polling fails or is interrupted
        if running_app:
            print("Stopping and shutting down bot...")
            try:
                await running_app.stop()
                await running_app.shutdown()
            except Exception as e:
                print(f"Error during graceful stop/shutdown: {e}")
            running_app = None # Reset global variable after cleanup

    print("Bot stopped.")

# This block ensures that the asyncio loop is properly handled in Colab
# If the cell is executed multiple times, it tries to restart the bot.
try:
    asyncio.run(main())
except RuntimeError as e:
    if "Cannot run a second event loop while the first is still running" in str(e):
        print("An event loop is already running. Attempting to stop previous instance and restart the bot...")
        if running_app: # Check if there's an instance to stop/shutdown
            try:
                # The main() function already handles stopping and shutdown if the app was running via run_polling.
                # This outer block is primarily for when asyncio.run(main()) fails due to an already running loop.
                # In such cases, if running_app still holds an instance from a *previous* execution of the cell,
                # we should try to stop it before retrying main.
                asyncio.run(running_app.stop())
                asyncio.run(running_app.shutdown())
                print("Previous bot instance stopped. Retrying main...")
                asyncio.run(main()) # Attempt to run main again
            except Exception as restart_e:
                print(f"Failed to restart bot gracefully after RuntimeError: {restart_e}. Please restart the Colab runtime if issues persist.")
        else:
            print(f"RuntimeError: {e}. No active bot instance to stop. Please restart the Colab runtime if you frequently encounter this.")
    else:
        raise
except KeyboardInterrupt:
    print("Bot stopped by user via KeyboardInterrupt.")
    if running_app:
        print("Initiating graceful shutdown due to KeyboardInterrupt...")
        try:
            asyncio.run(running_app.stop())
            asyncio.run(running_app.shutdown())
        except Exception as e:
            print(f"Error during shutdown after KeyboardInterrupt: {e}")
        finally:
            running_app = None # Reset global variable after cleanup
