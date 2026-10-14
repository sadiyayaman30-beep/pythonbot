import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ১. আপনার বট টোকেন দিন
BOT_TOKEN = "8644146332:AAHDmBqtGsD3hJYjXJ4HZdtgBvL0nIUeT7U"

# আপনার টেলিগ্রাম আইডি (যাতে শুধু আপনিই ভিডিও লিংক পরিবর্তন করতে পারেন)
ADMIN_USER_ID = 7137792443  # আপনার আসল টেলিগ্রাম ইউজার আইডি এখানে বসাবেন

# ডিফল্ট লিংকসমূহ
adsterra_link = "https://www.profitableratecpmnetwork.com/kawsnwkqtp?key=8a2b200ee165f5bb3f8f4f4f245bddba"
cpagrip_landing_page = "https://offer-oasis-video.lovable.app"

# গ্লোবাল ভেরিয়্যাবল (ভিডিও লিংক স্টোর করার জন্য)
current_video_link = "https://t.me/c/3841955949/6"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ২. /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Play Video (Watch Ad)", callback_data='watch_ad')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption_text = (
        "🔥 নতুন ভিডিও চলে এসেছে! 🔥\n\n"
        "👀 ভিডিওটি দেখতে নিচের বাটনে ক্লিক করুন।"
    )
    await update.message.reply_text(text=caption_text, reply_markup=reply_markup, parse_mode='Markdown')

# ৩. বাটন ক্লিক হ্যান্ডলার
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'watch_ad':
        # প্রথমে ইউজারকে Adsterra লিংকে পাঠানো (CPM Income)
        ad_keyboard = [
            [InlineKeyboardButton("▶️ বিজ্ঞাপন দেখুন (Click Here)", url=adsterra_link)],
            [InlineKeyboardButton("✅ বিজ্ঞাপন দেখা শেষ, ভিডিও নিন", callback_data='get_final_video')]
        ]
        reply_markup = InlineKeyboardMarkup(ad_keyboard)
        await query.message.reply_text(
            text="⚠️ ভিডিও আনলক করতে প্রথমে নিচের লিংকে ক্লিক করে বিজ্ঞাপনটি দেখুন:",
            reply_markup=reply_markup
        )
        
    elif query.data == 'get_final_video':
        # বিজ্ঞাপন দেখার পর CPAGrip ল্যান্ডিং পেজ এবং মূল ভিডিও লিংক দেওয়া (Lead Income)
        final_keyboard = [
            [InlineKeyboardButton("🎁 Claim $1000 Cash App Reward", url=cpagrip_landing_page)],
            [InlineKeyboardButton("📥 Direct Video Link", url=current_video_link)]
        ]
        reply_markup = InlineKeyboardMarkup(final_keyboard)
        await query.message.reply_text(
            text="🎉 অভিনন্দন! আপনার ভিডিও এবং বিশেষ অফার নিচে দেওয়া হলো:",
            reply_markup=reply_markup
        )

# ৪. অ্যাডমিন কমান্ড: টেলিগ্রাম চ্যাট থেকেই নতুন ভিডিও লিংক সেট করা
async def set_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_video_link
    user_id = update.message.from_user.id
    
    # চেক করা ইউজার আসল অ্যাডমিন কি না
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ আপনার এই কমান্ডটি ব্যবহার করার অনুমতি নেই!")
        return

    # কমান্ডের সাথে দেওয়া নতুন লিংকটি নেওয়া (যেমন: /setvideo https://t.me/.../456)
    args = context.args
    if args:
        current_video_link = args[0]
        await update.message.reply_text(f"✅ সফলভাবে নতুন ভিডিও লিংক আপডেট করা হয়েছে:\n{current_video_link}")
    else:
        await update.message.reply_text("⚠️ দয়া করে লিংকসহ লিখুন। যেমন:\n/setvideo https://t.me/your_channel/456", parse_mode='Markdown')

# ৫. বট রান করার ফাংশন
if name == 'main':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setvideo", set_video))
    app.add_handler(CallbackQueryHandler(button_click))

    print("বট সফলভাবে রান হচ্ছে...")
    app.run_polling()
