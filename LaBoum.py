import discord
import random
import os
from discord.ext import commands
from discord import app_commands

class LaBoumBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default(),
        )
    async def setup_hook(self):
        self.tree.add_command(help)
        self.tree.add_command(roll_dynamic)
        self.tree.add_command(advantage_command)
        self.tree.add_command(disadvantage_command)
        self.tree.add_command(credits)
        await self.tree.sync()
        print("INFO: slash-commands synchronized.")
    
    async def on_ready(self):
        print(f'INFO: LaBoum is online! Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = LaBoumBot()

@app_commands.command(name="help", description="Lists all LaBoum commands")
async def help(interaction: discord.Interaction):
    response = "**LaBoum Help:**"
    response += "\n```"
    response += "\n Command       | Description |"
    response += "\n---------------+------------------------------"
    response += "\n /help         | Displays all LaBoum commands"
    response += "\n /roll XdY     | Roll from 1 up to 100 any-sided dice and optional"
    response += "\n       XdY#Z   | modify the result with '+-*/' (2d20 or 2d20+3)"
    response += "\n /advantage    | Rolls 2d20 for you and highlights the greater one"
    response += "\n /disadvantage | Rolls 2d20 for you and highlights the lower one"
    response += "\n /credits      | Displays credits"
    response += "\n```"
    await interaction.response.send_message(response)

@app_commands.command(name="roll", description="Roll any dice (z.B. 2d6, d20, 4d10)")
@app_commands.describe(dice="Format: XdY, z.B. 3d6 or d20")
async def roll_dynamic(interaction: discord.Interaction, dice: str):
    try:
        dice = dice.lower().replace(" ", "").strip()
        secure_random = random.SystemRandom()
        operator = None
        modifier = 0

        for op in ['+', '-', '*', '/']:
            if op in dice:
                operator = op
                parts = dice.split(op)
                if len(parts) != 2:
                    raise ValueError("Invalid expression")
                dice_part, mod_part = parts
                modifier = int(mod_part)
                break
        else:
            # command does not contain operator
            dice_part = dice

        if 'd' not in dice_part:
            raise ValueError("Invalid expression - use format: 2d6 or d20")
        
        num_str, sides_str = dice_part.split('d')
        amount = int(num_str) if num_str else 1
        sides = int(sides_str)

        if amount < 1 or amount > 100:
            raise ValueError("Amount of dice has to be between 1 and 100")
        if sides < 2:
            raise ValueError("Dice need to have at least 2 sides")
        
        rolls = [secure_random.randint(1, sides) for _ in range(amount)]
        total = sum(rolls)
        expression = ""

        if operator:
            if operator == '+':
                total += modifier
            elif operator == '-':
                total -= modifier
            elif operator == '*':
                total *= modifier
            elif operator == '/':
                total /= modifier
            expression += f"{operator}{modifier}"

        response = f'{amount}d{sides}: {rolls} {expression} = **{total}**'

        await interaction.response.send_message(response)

    except Exception as e:
        await interaction.response.send_message(f'Error: {str(e)}')

@app_commands.command(name="advantage", description="Rolls a 20-sided dice with advantage.")
async def advantage_command(interaction: discord.Interaction):
    secure_random = random.SystemRandom()

    rolls = [secure_random.randint(1, 20) for _ in range(2)]
    roll_higher = rolls[0]
    if rolls[1] > rolls[0]:
        roll_higher = rolls[1]
    response = f'2d20 with advantage: {rolls} => {roll_higher}'
    await interaction.response.send_message(response)

@app_commands.command(name="disadvantage", description="Rolls a 20-sided dice with disadvantage.")
async def disadvantage_command(interaction: discord.Interaction):
    secure_random = random.SystemRandom()

    rolls = [secure_random.randint(1, 20) for _ in range(2)]
    roll_lower = rolls[0]
    if rolls[1] < rolls[0]:
        roll_lower = rolls[1]
    response = f'2d20 with disadvantage: {rolls} => {roll_lower}'
    await interaction.response.send_message(response)

@app_commands.command(name="credits", description="Displays credits")
async def credits(interaction: discord.Interaction):
    response = "**LaBoum Credits:**"
    response += "\nLaBoum by Swali (swalbart)"
    response += "\n<https://github.com/swalbart>"
    response += "\n<https://github.com/swalbart/LaBoum>"
    response += "\n*No Minks were harmed during the production of LaBoum*"
    await interaction.response.send_message(response)

# load token from token.txt
# it is strongly recommended to not keep the token in the sourcecode.
# if you decide not to keep the token outside the sourcecode you can
# paste your token as a String to the the following 'token'-variable:
token = "mytoken" # placeholder
if len(token) < 59:
    token_path = 'token.txt'
    if os.path.exists(token_path):
        with open(token_path, 'r') as file:
            token = file.read().strip()
    else:
        token = input("Please enter your Discord-Bot-Token: ").strip()
        with open(token_path, 'w') as file:
            file.write(token)

# start the bot
bot.run(token)
