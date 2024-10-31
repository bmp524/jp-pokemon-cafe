# jp-pokemon-cafe
This is a time slot booking bot for the Pokémon Café in Japan, inspired by https://medium.com/@patrickgwl/how-to-get-a-pok%C3%A9mon-cafe-reservation-in-japan-daccd1835237 article. The bot is a Python script leveraging Selenium. It can book time slots for both the Tokyo and Osaka Pokémon Café branches.

Bookings open daily at 10 AM Japan time for dates 31 days ahead. New batches of available time slots are released at 10:20 AM and 10:40 AM. The main challenge is that during peak times (10:00, 10:20, 10:40), the café's server often gets overloaded. When this happens, you'll receive a temporary message to refresh the page, and you'll be redirected to the main page.

The script handles this by validating such redirections and repeatedly refreshing the page until you reach the booking page. You have 15 minutes to complete the booking. It's not fully automated; you'll need to manually input your name, email, and other details to complete the reservation. Once done, you'll receive a confirmation email.

Using this approach, I successfully booked a time slot in September 2024.
