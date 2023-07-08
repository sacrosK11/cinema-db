from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext
import pandas as pd
import random
#from deep_translator import GoogleTranslator


TOKEN = '<<TOKEN>>'
BOT_USERNAME: Final = '@<<BOT_NAME>>'

# Load data from CSV files
movies_providers = pd.read_csv('Movies_Providers.csv')
mdb = pd.read_csv('2023_Movies_DB.csv')
regions = pd.read_csv('Regions.csv')

quiz_data = {}

# Define a function to generate a random movie

def generate_movie():
    # set the state for movie providers to be == Italy (IT)
    #random_row = movies_providers.loc[movies_providers['State'] == 'IT'].sample(n=1)
    random_row = movies_providers.loc[movies_providers['State']].sample(n=1)
    imdb_id = random_row.iloc[0]['imdbID']
    movie = mdb.loc[mdb['imdbID'] == imdb_id]

    # Translate the plot to Italian using Google Translator

    #to_translate = str(movie['Plot'].iloc[0])
    #translated = GoogleTranslator(source='auto', target='it').translate(to_translate)

    # Build the message to send
    message = f"⚡⚡ MOVIE OF THE DAY ⚡⚡\n\n"
    message += f"{movie['Title'].iloc[0]}\n\n"
    message += f"({movie['Genre'].iloc[0]} - {movie['Runtime'].iloc[0]} minuti)\n\n"
    #message += f"{translated}\n\n\n"
    message += str(movie['Plot'].iloc[0])
    message += f"Released: {movie['Released'].iloc[0]}\n\n"
    message += f"{movie['Poster'].iloc[0]}\n\n"


    # Create the 'More' button
    more_button = InlineKeyboardButton('More...', callback_data='more')

    # Create the keyboard markup with the 'More' button
    keyboard = [[more_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return message, reply_markup, movie, random_row


def get_full_movie_details(movie, random_row):

    # Build the full movie details message
    details = f"More about...\n\n"
    details += f"Director: {movie['Director'].iloc[0]}\n"
    details += f"Writer: {movie['Writer'].iloc[0]}\n"
    details += f"Cast: {movie['Actors'].iloc[0]}\n"
    details += f"Country: {movie['Country'].iloc[0]}\n"
    details += f"Production: {movie['Production'].iloc[0]}\n\n"
    details += f"Flatrate ✔ \n" if random_row['Flatrate'].notna().any() else '\n'
    details += f"Free ✔\n" if random_row['Free'].notna().any() else '\n'
    details += f"Rent ✔\n" if random_row['Rent'].notna().any() else '\n'
    details += f"Buy ✔\n" if random_row['Buy'].notna().any() else '\n'
    details += f"Watch now: {random_row['Link'].iloc[0]}"
    return details






if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, # type: ignore
                                       text=f"Hey, I'm your best movie suggestor: {BOT_USERNAME}")  # type: ignore

        await context.bot.send_message(chat_id=update.effective_chat.id, # type: ignore
                                       text="Write '/movie' to generate a random movie.\n Good film! 🎞🕶🍿")  # type: ignore

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, # type: ignore
                                       text="Write '/movie' to generate a random movie.\n Good film! 🎞🕶🍿")  # type: ignore                                       text="Scrivi '/movie' per generare un film casuale oppure menzionami e scrivi 'film'.\n Ad esempio '@Jimmee_BOT film', buona visione 🎞🕶🍿")  # type: ignore

    async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message, reply_markup, movie_obj, random_row_obj = generate_movie()
        # Add the ID of the movie as part of the data of "More..." button
        more_button = InlineKeyboardButton('More...', callback_data=f'more_{movie_obj["imdbID"].iloc[0]}')
        keyboard = [[more_button]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, #type: ignore
                                    text=message,
                                    reply_markup=reply_markup)


    async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        right = mdb.sample(n=1)
        right_title = right['Title'].iloc[0]
        context.user_data['right_title_quiz'] = right_title #type:ignore
        quiz_data['right_title'] = right_title
        right_plot = right['Plot'].iloc[0]
        #to_translate = str(right_plot)
        #translated = GoogleTranslator(source='auto', target='it').translate(to_translate)
        right_year = right['Released'].iloc[0]
        right_director = right['Director'].iloc[0]
        right_cast = right['Actors'].iloc[0]
        wrongs = mdb['Title'].sample(n=2).tolist()
        options = [right_title] + wrongs
        random.shuffle(options)

        # Create the quiz 
        message = f"Can you guess the movie based on its plot, director and cast?\n\n"
        message = str(right_plot)
        #message += f"Plot: {translated}\n\n"
        message += f"Director: {right_director}\n"
        message += f"Cast: {right_cast}\n\n"
        message += f"Released on: {right_year}\n\n"

        # Create the reply buttons + join them in a keyboard
        buttons = []
        for option in options:
            button = InlineKeyboardButton(text=option, callback_data=f'->_{option}')
            buttons.append([button])

        keyboard = buttons
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the message
        await context.bot.send_message(
            chat_id=update.effective_chat.id, #type:ignore
            text=message,
            reply_markup=reply_markup
        )


    async def quiz_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        choice = query.data #type:ignore

        right_title_quiz = quiz_data['right_title']
        if choice == f'->_{right_title_quiz}':
            # Right answer
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Right Answer! 🎉") #type:ignore
        else:
            # Wrong answer
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong Answer ❌") #type:ignore

        await query.answer() #type:ignore



    async def handle_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        choice = query.data #type:ignore
        
        if choice: 
            imdb_id = query.data.split('_')[1] #type:ignore

            # Retrieve the movie by its id
            movie = mdb.loc[mdb['imdbID'] == imdb_id]
            random_row = movies_providers.loc[movies_providers['imdbID'] == imdb_id]

            # Obtain the full movie details
            movie_details = get_full_movie_details(movie, random_row)

            # Send the details in a separate message
            await context.bot.send_message(chat_id=update.effective_chat.id, #type: ignore
                                           text=movie_details
                                           )

        # Reply to the callback query to remove the "pending" state
        await query.answer() #type: ignore


    # Responses
    def handle_response(text):
        processed: str = text.lower()
        if BOT_USERNAME in processed:
            return generate_movie()


    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type # type:ignore
        text: str = update.message.text # type:ignore
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"') # type:ignore

        if message_type == 'group':
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text) # type:ignore
            else:
                return
        else:
            response: str = handle_response(text) # type:ignore

        print('Bot: ', response)
        await update.message.reply_text(response) # type:ignore


    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f"Update {update} caused error {context.error}")



    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('movie', movie_command))
    app.add_handler(CommandHandler('quiz', quiz_command))

    # Callbacks
    app.add_handler(CallbackQueryHandler(handle_callback, pattern=r'^more_'))
    app.add_handler(CallbackQueryHandler(quiz_callback, pattern=r'^->_'))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error) # type:ignore

    # Start the bot
    print('Starting the bot...')
    app.run_polling(poll_interval=3)