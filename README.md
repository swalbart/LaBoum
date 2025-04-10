# LaBoum_v2
## <#>-------------<=======[ Description ]=======>-------------<#>

English:  
    LaBoum is a One Piece themed dice-rolling bot for Discord.  
    Its main function is to roll dice.
    The bot is currently only available in english. A german translation is already planned for a future update.  
    The rest of the README.md is only available in english language for the time being.  

Deutsch:  
    LaBoum ist ein, an One Piece thematisch angepasster Würfel-Bot für Discord.  
    Seine Hauptfunktion ist es zu würfeln.
    Der Bot ist aktuell nur in englisch verfügbar. Eine Deutsch-übersetzung ist bereits in planung.
    Der Rest der README.md ist vorerst nur in englisch verfügbar.  


## <#>-------------<=======[ Disclaimer ]=======>-------------<#>

This bot is NOT a simple plug-and-play installation.  
There is no invite-link for just joining on a discord server.  
You need to set it up yourself!  

To create a bot you first have to create an application in the 'Discord Developer Portal' and then add a bot to your application.
Next you need to add the bot to your server. Simply replace the '##################' with your application ID.
(Bot invite link: https://discord.com/oauth2/authorize?client_id=##################&scope=bot)  
Now you need a place to host the bot. If you need it running 24/7 you should consider hosting it on a own or rented server. For short time use you can also run it in an IDE or in a terminal.  
Optional: You can give your bot a discord-role for better rights management.  

## <#>-------------<=======[ Commands ]=======>-------------<#> 
    All listed bot commands are slash-commands.
    This means discord will automaticly list the available commands as part of its built-in commands after typing a "/" (slash) as first character of the command.  
    
  
### Help:

| Command | Description |
| --- | ---|
/help      | displays all LaBoum commands

  
### Dice:  
  
To roll dice you have to follow the following input-pattern:
| Command | Explanation |
| --- | --- |
/XdY{#Z}| / is needed to be recogniced as a command
/<b>4</b>d2+6| X is the amount of dice
/4d<b>2</b>+6| Y is the kind of dice
/4d2<b>+</b>6| # is the operand (+, -, *, /)
/4d2+<b>6</b>| Z is the value
/4d2<b>+6</b>| {} from pattern means it is optional input
/4d2| here is the example without the optional input operation

The output for the last example would get an output like this:  
4d6: [5, 1, 4, 1] +6 = 17 
4d6: [5, 4, 6, 3] = 18

All rolled dice always get added up for the result. By using an operand you are able to modify this result.

  
### Other dice:

| Command | Description |
| --- | ---|
/advantage   | rolls with advantage: 2d20, greater one counts
/disadvantage| rolls with disadvantage: 2d20, lower one counts

  
### Other useful commands:

| Command | Description |
| --- | ---|
/credits  | information about me and links to this repository

  
## <#>-------------<=======[ Token safety ]=======>-------------<#>
The token of a discord bot is unique and should not be readable to others.  

To clarify:  
Someone who is able to get the token of your discord bot will not be able to access your sourcecode or be able to gain immediate access to your server or computer.
Someone who is able to get the token of your discord bot will be able to controll your bot from writing text messages up to deleting content, channels and even banning people from the server. This is due to the fact that any owner of the token can write own code - most times with malicious intentions - to be executed by your bot.  

The token is most likely like a password. Anyone who sees your password (=token) can use it to controll the corresponding account/Device. So do not leak it!

**If your token ever gets leaked, head immediately to the 'Discord Developer Portal' to change the token.**  

This is the reason the token should not be visible in the code, so you are not in danger of accedently revealing it to someone or even uploade it.
The first time you use LaBoum, it will automaticly ask you for the token to get saved locally in a file named 'token.txt'.

In case you want to code with this bot and use git, the token.txt is also listed in the .gitignore.