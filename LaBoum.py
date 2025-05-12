import discord
import random
import os
import re
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
    #response += "\n Command       | Description |"
    #response += "\n---------------+------------------------------"
    response += "\n /advantage    | Rolls 2d20 for you and highlights the greater one"
    response += "\n /credits      | Displays creator credits"
    response += "\n /disadvantage | Rolls 2d20 for you and highlights the lower one"
    response += "\n /help         | Displays all LaBoum commands"
    response += "\n /roll _d_+_   | Roll any dice combination (optional modify with '+-*/')"
    response += "\n  Example      : 2d8+2+d4-3 or d12+4 + 3d8+2 + d4"
    response += "\n```"
    await interaction.response.send_message(response)

@app_commands.command(name="roll", description="Roll any dice combination")
@app_commands.describe(dice="Z. B. (2d6+4)/2 + d4 + 2*d8")
async def roll_dynamic(interaction: discord.Interaction, dice: str):
    try:
        secure_random = random.SystemRandom()
        expr = dice.lower().replace(" ", "")
        roll_log = []
        total = 0

        # Formatierfunktion für die ursprüngliche Benutzereingabe
        def format_user_expression(expr_raw: str) -> str:
            expr = expr_raw.lower().strip()
            dice_parts = re.findall(r'(\d*d\d+(?:[+\-*/]\d+)?)', expr)
            formatted_parts = []

            last_index = 0
            for part in dice_parts:
                start = expr.find(part, last_index)
                end = start + len(part)
                prefix = expr[last_index:start]
                formatted_parts.append(prefix.strip())

                if part.startswith("1d"):
                    part = part[1:]
                formatted_parts.append(part)
                last_index = end

            formatted_parts.append(expr[last_index:].strip())
            final = ' '.join(p for p in formatted_parts if p)
            return final

        # Muster für Teilausdrücke: z.B. "2d6+4", "1d8", "d12", etc.
        dice_pattern = re.compile(r'((\d*)d(\d+))([+\-*/]\d+)?')

        # Ausdruck parsen & ersetzen
        def replace_group(match):
            nonlocal total
            dice_expr = match.group(1)  # z.B. "2d6"
            count = int(match.group(2)) if match.group(2) else 1
            sides = int(match.group(3))
            mod_expr = match.group(4)  # z.B. "+4"

            if not (1 <= count <= 100 and 2 <= sides <= 1000):
                raise ValueError(f"Ungültiger Würfel: {dice_expr}")

            rolls = [secure_random.randint(1, sides) for _ in range(count)]
            rolls_sum = sum(rolls)

            mod_str = ""
            mod_val = 0
            if mod_expr:
                operator = mod_expr[0]
                operand = int(mod_expr[1:])
                mod_val = {
                    '+': rolls_sum + operand,
                    '-': rolls_sum - operand,
                    '*': rolls_sum * operand,
                    '/': round(rolls_sum / operand, 2)
                }[operator]
                mod_str = f" {operator}{operand}"
            else:
                mod_val = rolls_sum

            total += mod_val

            # Ausdrucks-Darstellung
            roll_line = f"• {count}d{sides}{mod_str} → {rolls}"
            if mod_str:
                roll_line += f" = {mod_val}"
            else:
                roll_line += f" = {rolls_sum}"
            roll_log.append(roll_line)

            return str(mod_val)  # Rückgabe für spätere eval(), falls nötig

        # Ausdruck analysieren und alle Teildice ersetzen
        parsed_expr = dice_pattern.sub(replace_group, expr)

        # Sichere letzte Prüfung (z. B. bei Restzeichen wie "+2" am Ende)
        if not re.fullmatch(r'[\d\+\-\*/\(\)\.]+', parsed_expr):
            raise ValueError("Ungültige Zeichen im Ausdruck")

        # Optional auswerten, wenn Klammern da sind
        if '(' in parsed_expr or ')' in parsed_expr or any(op in parsed_expr for op in '*/-+'):
            total = eval(parsed_expr)

        total = round(total, 2) if isinstance(total, float) else total

        # Ausdruck des Users formatiert anzeigen
        formatted_input = format_user_expression(dice)

        antwort = f'## {interaction.user.mention}: {total}\n>>> '
        antwort += "\n".join(roll_log)
        antwort += f'\n```/roll dice: {formatted_input}```'

        await interaction.response.send_message(antwort)

    except Exception as e:
        await interaction.response.send_message(f'⚠️ Fehler: {str(e)}')


@app_commands.command(name="advantage", description="Rolls a 20-sided dice with advantage.")
async def advantage_command(interaction: discord.Interaction):
    secure_random = random.SystemRandom()

    rolls = [secure_random.randint(1, 20) for _ in range(2)]
    roll_higher = rolls[0]
    if rolls[1] > rolls[0]:
        roll_higher = rolls[1]
    #response = f'2d20 with advantage: {rolls} => {roll_higher}'
    response = f'## {interaction.user.mention}: {roll_higher}\n>>> '
    response += f'• 2d20 → {rolls}'
    response += f'\n```/advantage```'
    await interaction.response.send_message(response)

@app_commands.command(name="disadvantage", description="Rolls a 20-sided dice with disadvantage.")
async def disadvantage_command(interaction: discord.Interaction):
    secure_random = random.SystemRandom()

    rolls = [secure_random.randint(1, 20) for _ in range(2)]
    roll_lower = rolls[0]
    if rolls[1] < rolls[0]:
        roll_lower = rolls[1]
    #response = f'2d20 with disadvantage: {rolls} => {roll_lower}'
    response = f'## {interaction.user.mention}: {roll_lower}\n>>> '
    response += f'• 2d20 → {rolls}'
    response += f'\n```/disadvantage```'
    await interaction.response.send_message(response)

@app_commands.command(name="credits", description="Displays credits")
async def credits(interaction: discord.Interaction):
    response = "### LaBoum Credits"
    response += "\n[LaBoum](<https://github.com/swalbart/LaBoum>) by [Swali (swalbart)](<https://github.com/swalbart>)"
    response += "\nUsed ressources: Visual Studio Code; Pyhton3; coffee"
    response += "\nLicense: [MIT License](<https://choosealicense.com/licenses/mit/>)"
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
