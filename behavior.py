import discord
import random
from quizInstance import QCM

class Chats():
    def __init__(self):
        self.instances = {}
    def add(self, user:discord.User):
        self.instances[user] = DM(user)

class InServer():
    def __init__(self, chats:Chats):
        self.chats = chats
    async def on_message(self, message:discord.Message):
        if ('qcm' in message.content.lower()):
            if (message.author in self.chats.instances):
                await message.reply("Nous avons déjà une discussion en DMs, non ?")
            else:
                self.chats.add(message.author)
                help = "Je suis un bot conçu par Théo Lartigau pour t'aider dans tes révisions. Je peux préparer des QCMs à partir des différentes annales sur commande, essaye d'écrire **'!qcm microéconomie'** pour voir !"\
                    "\nVoici la liste de mes QCMs :"\
                    "\n - **microéconomie**: mélange les exercices et les questions de cours des l'annales de 2020 (2019 BIENTOT)"\
                    "\n - **microéconomie_cours**: ne contient que les questions de cours"\
                    "\n - **maths**: mélange les exerices et les questions de cours de l'annale de 2019"\
                    "\nUne fois un QCM lancé, il te suffit d'écrire **'![ta réponse]'** pour répondre aux questions. '!A' pour la réponse A, par exemple. En cas de réponses multiples pour une même question, tu peux par exemple écrire **'!ACD'**"\
                    "\nEcrire **'!N'** te permet de sauter une question et **'!quit'** arrête le quiz en cours."\
                    "\nEcris ***'!help'* à tout moment pour revoir les informations utiles"\
                    "\nSi tu n'es pas d'accord avec une de mes corrections n'hésite pas à le dire à Théo !"
                if (random.randrange(0, 4) == 0): help += "\ns\o Samuel Favre le prince"
                await message.author.send(help)
                
        else:
            await message.reply("Ecris '!qcm' pour que je slide dans tes DMs pour t'aider à t'entraîner (officiellement :wink:))")

class DM():
    letterToNumber = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'n':-1}
    numberToLetter = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f'}
    def __init__(self, user:discord.User):
        self.user = user
        self.qcm = None
        self.help = "Je suis un bot conçu par Théo Lartigau pour t'aider dans tes révisions. Je peux préparer des QCMs à partir des différentes annales sur commande, essaye d'écrire **'!qcm microéconomie'** pour voir !"\
                    "\nVoici la liste de mes QCMs :"\
                    "\n - **microéconomie**: mélange les exercices et les questions de cours des l'annales de 2020 (2019 BIENTOT)"\
                    "\n - **microéconomie_cours**: ne contient que les questions de cours"\
                    "\n - **maths**: mélange les exerices et les questions de cours de l'annale de 2019"\
                    "\nTu peux choisir la longueur d'un qcm en le spécifiant à la fin de ton message, par exemple '!qcm maths 15'. La longueur par défaut est de 10 et elle est au plus de 20 pour la microéconomie (la faute aux exercices très longs)"\
                    "\nUne fois un QCM lancé, il te suffit d'écrire **'![ta réponse]'** pour répondre aux questions. '!A' pour la réponse A, par exemple. En cas de réponses multiples pour une même question, tu peux par exemple écrire **'!ACD'**"\
                    "\nEcrire **'!N'** te permet de sauter une question et **'!quit'** arrête le quiz en cours."\
                    "\nSi tu n'es pas d'accord avec une de mes corrections n'hésite pas à le dire à Théo !"
    async def on_message(self, message:discord.Message):
        if (message.author != self.user): return
        if ('qcm microéconomie_cours' in message.content.lower()):
            args = (message.content.lower()).split()
            if (len(args) > 2 and args[2].isnumeric()):
                self.qcm = QCM('micro_cours', int(args[2]))
            else:
                self.qcm = QCM('micro_cours')
            await self.send_rules()
            await self.handle_question()
        elif ('qcm microéconomie cours' in message.content.lower()):
            args = (message.content.lower()).split()
            if (len(args) > 3 and args[3].isnumeric()):
                self.qcm = QCM('micro_cours', int(args[3]))
            else:
                self.qcm = QCM('micro_cours')
            await self.send_rules()
            await self.handle_question()
        elif ('qcm microéconomie' in message.content.lower()):
            args = (message.content.lower()).split()
            if (len(args) > 2 and args[2].isnumeric()):
                self.qcm = QCM('micro', int(args[2]))
            else:
                self.qcm = QCM('micro')
            await self.send_rules()
            await self.handle_question()
        elif (message.content.lower() == 'qcm maths'):
            args = (message.content.lower()).split()
            if (len(args) > 2 and args[2].isnumeric()):
                self.qcm = QCM('maths', int(args[2]))
            else:
                self.qcm = QCM('maths')
            await self.send_rules()
            await self.handle_question()
        elif (message.content.lower() == ('help')):
            if (self.qcm != None):
                await self.send_rules()
            else:
                await self.user.send(self.help)
                if (random.randrange(0, 4) == 0): 
                    await self.user.send("\ns\o Samuel Favre le boss")
        elif (message.content.lower() == 'quit'):
            self.qcm = None
        elif (self.qcm != None):
            await self.handle_guess(message.content.lower())
        else:
            await self.user.send("Je n'ai pas compris, écris '!help' pour savoir ce que tu peux me demander.")   

    async def handle_guess(self, guess):
        if (not self.qcm.playing): 
            await self.user.send(f"Le QCM est déjà fini ! Ton score final est de **{self.qcm.score}/{self.qcm.maxScore}** !\nEcris '!quit' puis '!help' pour avoir la liste des QCM ou directement '!qcm [ton choix]' pour recommencer un QCM")
            return
        guessList = []
        for letter in guess:
            if (letter not in self.letterToNumber) : 
                await self.user.send("C'est pas une réponse ça :shrug:")
                return
            guessList.append(self.letterToNumber[letter])
        self.qcm.betterguess(guessList)
        await self.handle_question()

    async def handle_question(self):
        self.qcm.next_question()
        if (not self.qcm.playing):
            await self.qcm_over()
            return
        await self.user.send(f"**Question {self.qcm.questionIndex + 1} :**\n{self.qcm.question['text']}")
        i = -1
        answers = ""
        for answer in self.qcm.question['answers']:
            i += 1
            answers += f"\n**{self.numberToLetter[i].upper()}.** {answer.removesuffix('*')}"
        await self.user.send(answers)

    async def qcm_over(self):
        msg = f"Le QCM est fini ! Ton score final est de **{self.qcm.score}/{self.qcm.maxScore}** !"
        await self.user.send(msg)
        if (self.qcm.score == int(self.qcm.maxScore)):
            await self.user.send("Tu n'as fait aucune faute, bravo !")
        else:
            await self.user.send("Voici la liste de tes erreurs:")
            i = -1
            speech = ""
            for answer in self.qcm.answers:
                i += 1
                rightGuesses = answer['rightGuesses']
                wrongGuesses = answer['wrongGuesses']
                rightAnswers = answer['rightAnswers']
                if (len(rightGuesses) == len(rightAnswers) and len(wrongGuesses) == 0):
                    continue
                else:
                    speech += f"\n---------------\n - A la question **{answer['question']}**"
                if (len(rightGuesses) == 0 and len(wrongGuesses) == 0):
                    speech += f"\nTu n'as pas répondu"
                else:
                    speech += "\nTu as répondu :"
                    for right in rightGuesses:
                        speech += f"\n:white_check_mark: *{right[:-1]}*"
                    for wrong in wrongGuesses:
                        speech += f"\n:red_square: *{wrong}*"
                if (len(rightGuesses) == 0):
                    speech += "\nLa bonne réponse était :"
                else:
                    speech += "\nIl te manquait :"
                for rightAnswer in rightAnswers:
                    if (rightAnswer not in rightGuesses):
                        speech += f"\n - **{rightAnswer[:-1]}**"
                await self.user.send(speech)
                speech = ""
            if (len(speech) > 1):
                await self.user.send(speech)

    async def send_rules(self):
        rules = f"Ce qcm de {self.qcm.current['name']} comporte {len(self.qcm.current['questions'])} questions et est évalué sur {self.qcm.maxScore} points"
        rules += f"\nUne bonne réponse vaut **+{self.qcm.current['rightScore']}** point, "
        if (self.qcm.current['wrongScore'] == "0"):
            rules += "il n'y a **pas de points négatifs**. "
        else:
            rules += f"une mauvaise réponse vaut **-{self.qcm.current['wrongScore']}** point. "
        if (self.qcm.current['type'] != 'one_answer'):
            rules += "\nIl peut y avoir** plusieurs réponses possibles** pour une question, "
            rules += "donne ta réponse en écrivant '!AC' ou '!BEA'"
        else:
            rules += "\nIl n'y a qu'**une seule réponse possible** par question, "
            rules += "donne ta réponse en écrivant '!A' ou '!B', par exemple"
        rules += "\nBonne chance!"
        await self.user.send(rules)
