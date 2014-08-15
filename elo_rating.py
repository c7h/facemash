'''
Created on 14.08.2014

@author: christoph
'''
from random import choice

INITIAL_SCORE = 1500.0
K = 10

class Player(object):
    def __init__(self, ident, score=INITIAL_SCORE):
        self.id = ident
        self.score = score
        self.wins = 0
        self.matches = 0
        
        self.imgurl="http://img.thesun.co.uk/aidemitlum/archive/01643/_Mila_Kunis_1643489a.jpg"
    
    def set_score(self, new_score):
        self.score = new_score
    
    def __eq__(self, other):
        return self.score==other.score
    
    def __str__(self, *args, **kwargs):
        return "Player %s - [%04f] %2i/%2i" % (str(self.id), self.score, self.wins, self.matches)
    

class Elo:
    def __init__(self, players):
        self.players = players
        
    def choose(self):
        '''choose 2 players for a match'''
        #strategy: random choice
        p1 = choice(self.players)
        p2 = p1
        while p1 is p2:
            p2 = choice(self.players)
            
        #call algorithm
        self._match(p1, p2, algo_func=self.__match_algo_strict)    
    
    
    def _match(self, p1, p2, algo_func):
        algo_func(p1, p2)
    
    def __match_algo_strict(self, p1, p2):
        #elo algorithm - simple modifications
        r1 = max(min(p2.score - p1.score, 400), -400)
        r2 = max(min(p1.score - p2.score, 400), -400)
        e1 = 1.0 / (1+10**(r1 / 400))
        e2 = 1.0 / (1+10**(r2 / 400))
        
        
        winner, looser = self.decide(p1, p2)
        
        if winner is p1:
            s1 = 1
            s2 = 0
        elif winner is p2:
            s1 = 0
            s2 = 1
        else: #TODO: implement
            s1 = 0.5
            s2 = 0.5
            
        
        p1.set_score(p1.score + K*(s1-e1))
        p2.set_score(p2.score + K*(s2-e2))
        
        #increase wincounter        
        winner.wins +=1
        
        #increase matchcounter
        p1.matches +=1
        p2.matches +=1
        
    def __match_algo_experimental(self, p1, p2):
        #elo algorithm - simple modifications
        r1 = max(min(p2.score - p1.score, 400), -400)
        r2 = max(min(p1.score - p2.score, 400), -400)
        e1 = 1.0 / (1+10**(r1 / 400))
        e2 = 1.0 / (1+10**(r2 / 400))
        
        winner, looser = self.decide(p1, p2)
        
        if winner is p1:
            exp_value = e2
        else:
            exp_value = e1    
            
        winner.set_score(winner.score+K*exp_value)
        looser.set_score(looser.score-K*exp_value)
        
        #increase wincounter        
        winner.wins +=1
        
        #increase matchcounter
        p1.matches +=1
        p2.matches +=1
    
    
    def decide(self, p1, p2):
        '''decision function - who should win? @return: (winner, looser)'''
        #strategy: manual decision
        print "hard decision: %s vs %s" % (p1, p2)
        while True:
            decision = input("1 or 2? > ")
            if decision == 1:
                return (p1, p2)
            elif decision == 2:
                return (p2, p1)
            else:
                print "1 or 2..."
    
    def print_ranking(self):
        sorted_players = sorted(self.players, reverse=True, key=lambda x: x.score)
        for v, player in enumerate(sorted_players):
            print "%03i: %s" % (v, player)
    
if __name__ == "__main__":
    #players = [Player(1, 100), Player(2, 101), Player(3, 99), Player(4, 102)]
    players = [Player("Kasparov", 2806.0), Player("Polgar", 2577.0)]
    elo = Elo(players)
    
    elo.print_ranking()
    
    for i in range(1):
        print "round %i ..." % i
        elo.choose()
    
    elo.print_ranking()
    
    
    
    