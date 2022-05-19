import json
from random import sample

class QCM():
    def __init__(self, quiz:str, length=10):
        with open('quizDB.json', encoding="utf8") as quizFile:
            self.quizDB = json.load(quizFile)
        if (quiz in self.quizDB):
            self.current = self.quizDB[quiz]
            self.name = quiz
            if (length > len(self.current['questions'])) : length = len(self.current['questions'])
            self.current['questions'] = sample(self.current['questions'], length)
            for question in self.current['questions']:
                if ('questions' in question):
                    length += len(question['questions']) - 1
                    # prevent length from being too long
                    if (length > 20):
                        length -= len(question['questions']) + 1
                        self.current['questions'].remove(question)
                elif (len(question['answers']) == 0):
                    self.current['questions'].remove(question)
                    length -= 1
            for i in range(0, length):
                if ('questions' in self.current['questions'][i]):
                    self.current['questions'][i]['questions'][0]['text'] = self.current['questions'][i]['text'] + '\n\n' + self.current['questions'][i]['questions'][0]['text'] 
                    k = 0
                    for j in range(len(self.current['questions'][i]['questions'])-1, -1, -1):
                        self.current['questions'].insert(i, self.current['questions'][i + k]['questions'][j])
                        k += 1
                    self.current['questions'].pop(i + k)
            self.maxScore = len(self.current['questions'])
        else:
            self.current = None
        self.questionIndex = -1
        self.score = 0
        self.playing = False
        self.errors = []
        self.answers = []
    
    def betterguess(self, guessList:list):
        rightGuesses = []
        wrongGuesses = []
        score = 0
        for guess in guessList:
            if (guess == -1):
                break 
            elif (self.question['answers'][guess] in self.question['rightAnswers']):
                rightGuesses.append(self.question['answers'][guess])
                score += round(float(self.current['rightScore']) / self.question['coeff'], 2)
            else:
                wrongGuesses.append(self.question['answers'][guess])
                score -= round(float(self.current['wrongScore']) / self.question['coeff'], 2)
        self.answers.append({
            'question' : self.question['text'],
            'rightAnswers' : self.question['rightAnswers'],
            'rightGuesses' : rightGuesses,
            'wrongGuesses' : wrongGuesses
        })
        if (score > 0): self.score += score

    def guess(self, guessList:list):
        rightAnswer = []
        if (guessList[0] == -1):
            for answer in self.question['answers']:
                if ('*' in answer):
                    rightAnswer.append(answer.removesuffix('*'))
                    self.errors.append({'question':self.question['text'], 'error':"", 'answers':rightAnswer})
            return False
        score = 0
        rightGuesses = []
        try:
            # Dans un premier temps, on fait la liste des bonnes et mauvaises réponses cochées
            for guess in guessList:
                if ('*' in self.question['answers'][guess]):
                    score += round(float(self.current['rightScore']) / self.question['coeff'], 2)
                    rightGuesses.append(self.question['answers'][guess])
                else:
                    score -= round(float(self.current['wrongScore']) / self.question['coeff'], 2)
                    for answer in self.question['answers']:
                        if ('*' in answer):
                            rightAnswer.append(answer.removesuffix('*'))
                            self.errors.append({'question':self.question['text'], 'error':self.question['answers'][guess], 'answers':rightAnswer})
            # Ensuite, on compare la liste des bonnes réponses cochées et celle des bonnes réponses
            if (score > 0): self.score += score
        except Exception as e:
            print(e)
            return False

    def next_question(self):
        self.playing = True
        self.questionIndex += 1
        if (len(self.current['questions']) == self.questionIndex):
            self.end()
            return
        self.question = self.current['questions'][self.questionIndex]
        self.question['answers'] = sample(self.question['answers'], len(self.question['answers']))
        self.question['coeff'] = 0
        self.question['rightAnswers'] = []
        for answer in self.question['answers']:
            if ('*' in answer):
                self.question['coeff'] += 1
                self.question['rightAnswers'].append(answer)
            
    def end(self):
        self.playing = False
