from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext
import requests as re
from time import sleep

TOKEN = '<<INSERT TELEGRAM BOT TOKEN>>'
BOT_USERNAME: Final = '@<<INSERT TELEGRAM BOT NAME>>'

# Default user's State
user_state = 'US'

if __name__ == '__main__':
    
    app = Application.builder().token(TOKEN).build()
    
    def format_movie(movie):
        message = f"{movie['title']}\n\n"
        message += f"({movie['genre']})\n\n"
        message += f"{movie['plot']}\n\n\n"
        hours, minutes = divmod(int(movie['runtime']),60)
        runtime_formatted = f"{hours:01d}h {minutes:02d} minutes"                 
        message += f"{runtime_formatted}\n" 
        message += f"Released on: {movie['year']}\n\n"
        message += f"{movie['poster']}\n\n"    
        #add like / dislike buttons
        like = 'True', movie['imdbid']
        dislike = 'False', movie['imdbid']
        like_button = InlineKeyboardButton('❤️', callback_data=f'like_{like}')
        dislike_button = InlineKeyboardButton('❌', callback_data=f'dislike_{dislike}')
        more_button = InlineKeyboardButton('More...', callback_data=f"more_{movie['imdbid']}")
        like_dislike =[[like_button, more_button, dislike_button]]
        likeDislike = InlineKeyboardMarkup(like_dislike)
        return message, likeDislike
    
    
    async def send_filtered_movie(update: Update, context: CallbackContext, gen: str, runtime: int):
        # Change the API route based on your desired IP
        movie = re.get(f'http://127.0.0.1:5000/api/filter_movies/?state={user_state}&gen={gen}&runtime={runtime}').json()
        message, likeDislike = format_movie(movie)
        await context.bot.send_message(chat_id=update.effective_chat.id, #type: ignore
                                    text=message,
                                    reply_markup=likeDislike)      
        
        

            
# Commands
###################
    # Start Command
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, # type: ignore
                                       text="Ciao, sono il tuo suggeritore di film: Jimmy 2000!")  # type: ignore
        await context.bot.send_message(chat_id=update.effective_chat.id, # type: ignore
                                       text="Scrivi '/movie' per generare un film casuale oppure menzionami e scrivi 'film'.\n Ad esempio '@Jimmee_BOT film', buona visione 🎞🕶🍿")  # type: ignore

    # Help Command
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        for i in range(3):
            sleep(10) # trovare alternativa a sleep(non mettere il programma a dormire!!)
            await movie_command(update, context)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="Scrivi '/movie' per generare un film casuale oppure menzionami e scrivi 'film'.\n Ad esempio '@Jimmee_BOT film', buona visione 🎞🕶🍿")  # type: ignore


    # Random Moive Command
    async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Change the API route based on your desired IP
        movie = re.get(f'http://127.0.0.1:5000/api/random_movie/?state={user_state}').json()
        message, likeDislike = format_movie(movie)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=message,
                                    reply_markup=likeDislike)


    # Random Filtered Movie Command
    async def filter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Change the API route based on your desired IP
        response = re.get('http://127.0.0.1:5000/api/top_genres')
        genres = response.json()   
        await context.bot.send_message(chat_id=update.effective_chat.id, text='What movie genre do you want to watch?')
        keyboard = []
        for genre in genres['Genre'].values():
            button = InlineKeyboardButton(text=genre, callback_data=f'genre_{genre}')
            keyboard.append([button])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Choose a genre:', reply_markup=reply_markup)


# Callbacks
####################################
    # "More Details Button" Callback - def: format_movie()
    async def handle_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        choice = query.data 
        if choice: 
            imdb_id = query.data.split('_')[1] 
            # Change the API route based on your desired IP
            movie = re.get(f'http://127.0.0.1:5000/api/get_movie/{imdb_id}/?state={user_state}').json() 
            details = f"Directed by: {movie['director']}\n"
            details += f"Written by: {movie['writer']}\n"
            details += f"Cast: {movie['cast']}\n"
            details += f"Nation: {movie['country']}\n"
            details += f"Production: {movie['production']}\n\n"  
            details += f"Watch now: {movie['link']}" 
            await context.bot.send_message(chat_id=update.effective_chat.id, text=details) 
        # Reply to the callback query to remove the "pending" state
        await query.answer() 
  
  
    # Like/Dislike Button Callback -  def: format_movie()
    async def like_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        if 'True' in query.data:
            print(query.data)
        else:
            print(query.data)
       
           
    # Genre Button Callback - def: filter_command - + Send Duration Duttons        
    async def filter_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        choice = query.data 
        gen = choice.split('_')[1]
        context.user_data['selected_genre'] = gen  
        await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Good! I love {gen} movies.")
        keyboard = [
            [InlineKeyboardButton("1h", callback_data="duration_60")],
            [InlineKeyboardButton("1h30", callback_data="duration_90")],
            [InlineKeyboardButton("2h", callback_data="duration_120")],
            [InlineKeyboardButton("2h30", callback_data="duration_150")],
            [InlineKeyboardButton("3h", callback_data="duration_180")],
            [InlineKeyboardButton("3h+", callback_data="duration_1000")] 
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='How much time do you have (max)?', reply_markup=reply_markup)


    # Duration Button Callback - def: filter_callback
    async def duration_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        choice = query.data 
        duration_minutes = 0
        if choice == "duration_60":
            duration_minutes = 60
        elif choice == "duration_90":
            duration_minutes = 90
        elif choice == "duration_120":
            duration_minutes = 120
        elif choice == "duration_150":
            duration_minutes = 150
        elif choice == "duration_180":
            duration_minutes = 180
        elif choice == "duration_1000":
            # 3h = +1000 minutes
            duration_minutes = 1000 
        gen = context.user_data.get('selected_genre') 
        await send_filtered_movie(update, context, gen, duration_minutes)


    # Responses
    def handle_response(text):
        processed: str = text.lower()
        if BOT_USERNAME in processed:
            return # add the function to generate movies if needed


    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type 
        text: str = update.message.text 
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"') 
        if message_type == 'group':
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text) 
            else:
                return
        else:
            response: str = handle_response(text) 

        print('Bot: ', response)
        await update.message.reply_text(response) 


    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f"Update {update} caused error {context.error}")


    # Commands Handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('random', movie_command))
    app.add_handler(CommandHandler('filter', filter_command))


    # Callbacks Handlers
    app.add_handler(CallbackQueryHandler(handle_callback, pattern=r'^more_'))
    app.add_handler(CallbackQueryHandler(like_callback, pattern=r'^like_'))
    app.add_handler(CallbackQueryHandler(like_callback, pattern=r'^dislike_'))
    app.add_handler(CallbackQueryHandler(filter_callback, pattern=r'^genre_'))
    app.add_handler(CallbackQueryHandler(duration_callback, pattern=r'^duration_'))
    

    # Messages Handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Start the bot
    print('Starting the bot...')
    app.run_polling(poll_interval=3)